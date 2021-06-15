from copy import copy

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from unicef_attachments.fields import FileTypeModelChoiceField
from unicef_attachments.models import Attachment, FileType

from unicef_restlib.fields import SeparatedReadWriteField

from etools.applications.travel.models import (
    Activity,
    Trip,
    ItineraryItem,
    TripStatusHistory,
    Report,
)
from etools.applications.travel.permissions import TripPermissions
from etools.applications.users.serializers_v3 import MinimalUserSerializer


class BaseTripSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Trip

    def get_permissions(self, obj):
        # don't provide permissions for list view
        if self.context["view"].action == "list":
            return []

        ps = Trip.permission_structure()
        permissions = TripPermissions(
            self.context['request'].user,
            obj,
            ps,
        )
        return permissions.get_permissions()


class TripAttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    file_type = FileTypeModelChoiceField(
        label=_("Document Type"),
        queryset=FileType.objects.filter(code="travel_docs"),
    )

    class Meta:
        model = Attachment
        fields = ("id", "url", "file_type", "created")

    def update(self, instance, validated_data):
        validated_data["code"] = "travel_docs"
        return super().update(instance, validated_data)

    def get_url(self, obj):
        if obj.file:
            url = obj.file.url
            request = self.context.get("request", None)
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return ""


class ActivityBaseSerializer(serializers.ModelSerializer):
    partner_name = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()
    monitoring_activity_name = serializers.SerializerMethodField()
    section_name = serializers.SerializerMethodField()

    def get_partner_name(self, obj):
        if obj.partner:
            return obj.partner.name
        elif obj.monitoring_activity:
            return ', '.join([p.short_name or p.name for p in obj.monitoring_activity.partners.all()]) \
                if obj.monitoring_activity.partners.exists() else ''
        return ''

    def get_section_name(self, obj):
        if obj.section:
            return obj.section.name
        elif obj.monitoring_activity:
            return ', '.join([s.name for s in obj.monitoring_activity.sections.all()]) \
                if obj.monitoring_activity.sections.exists() else ''
        return ''

    def get_monitoring_activity_name(self, obj):
        ma = obj.monitoring_activity
        if ma:
            return ma.number
        return ''

    def get_location_name(self, obj):
        if obj.monitoring_activity:
            return obj.monitoring_activity.destination_str
        elif obj.location:
            return str(obj.location)
        return ''

    class Meta:
        model = Activity
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, "initial_data"):
            self.initial_data["trip"] = self._context.get(
                "request"
            ).parser_context["kwargs"].get("nested_1_pk")


class ActivityDetailSerializer(ActivityBaseSerializer):

    pass


class ItineraryItemBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, "initial_data"):
            self.initial_data["trip"] = self._context.get(
                "request"
            ).parser_context["kwargs"].get("nested_1_pk")


class ItineraryItemSerializer(ItineraryItemBaseSerializer):
    pass


class TripCreateUpdateSerializer(BaseTripSerializer):
    attachments = TripAttachmentSerializer(many=True, required=False)

    def _add_attachments(self, trip, attachment_data):
        print("setting attachments")
        content_type = ContentType.objects.get_for_model(Trip)
        file_type = FileType.objects.get(name="generic_trip_attachment")
        current = list(Attachment.objects.filter(
            object_id=trip.pk,
            content_type=content_type,
        ).all())
        used = []
        for attachment in attachment_data:
            for initial in self.initial_data.get("attachments"):
                pk = initial["id"]
                if pk not in used:
                    attachment = Attachment.objects.filter(pk=pk).update(
                        file_type=file_type,
                        code="travel_docs",
                        object_id=trip.pk,
                        content_type=content_type,
                    )
                    used.append(pk)
                    break

    def update(self, instance, validated_data):
        attachment_data = None
        if "attachments" in validated_data:
            attachment_data = validated_data.pop("attachments")
        instance.save()
        if attachment_data is not None:
            self._add_attachments(instance, attachment_data)
        return instance

    class Meta(BaseTripSerializer.Meta):
        fields = '__all__'
        read_only_fields = ["reference_number", "status"]


class TripSerializer(BaseTripSerializer):
    attachments = TripAttachmentSerializer(many=True, required=False)
    itinerary_items = ItineraryItemSerializer(many=True, required=False)
    activities = ActivityDetailSerializer(many=True, required=False)
    supervisor = MinimalUserSerializer()
    traveller = MinimalUserSerializer()
    status_list = serializers.SerializerMethodField()
    rejected_comment = serializers.SerializerMethodField()
    available_actions = serializers.SerializerMethodField()

    class Meta(BaseTripSerializer.Meta):
        fields = '__all__'
        read_only_fields = ["reference_number", "status"]

    def get_status_list(self, obj):
        if obj.status == obj.STATUS_REJECTED:
            status_list = [
                obj.STATUS_DRAFT,
                obj.STATUS_REJECTED,
                obj.STATUS_SUBMISSION_REVIEW,
                obj.STATUS_SUBMITTED,
                obj.STATUS_APPROVED,
                obj.STATUS_REVIEW,
                obj.STATUS_COMPLETED,
            ]
        elif obj.status == obj.STATUS_CANCELLED:
            status_list = [
                obj.STATUS_DRAFT,
                obj.STATUS_SUBMISSION_REVIEW,
                obj.STATUS_CANCELLED,
            ]
        else:
            status_list = [
                obj.STATUS_DRAFT,
                obj.STATUS_SUBMISSION_REVIEW,
                obj.STATUS_SUBMITTED,
                obj.STATUS_APPROVED,
                obj.STATUS_REVIEW,
                obj.STATUS_COMPLETED,
            ]
        return [s for s in obj.STATUS_CHOICES if s[0] in status_list]

    def get_rejected_comment(self, obj):
        return obj.get_rejected_comment() or ""

    def get_available_actions(self, obj):
        # don't provide available actions for list view
        if self.context["view"].action == "list":
            return []

        ACTION_MAP = {
            Trip.STATUS_DRAFT: "revise",
            Trip.STATUS_SUBMISSION_REVIEW: "subreview",
            Trip.STATUS_CANCELLED: "cancel",
            Trip.STATUS_SUBMITTED: "submit",
            Trip.STATUS_REJECTED: "reject",
            Trip.STATUS_APPROVED: "approve",
            Trip.STATUS_REVIEW: "review",
            Trip.STATUS_COMPLETED: "complete",
        }

        user = self.context['request'].user
        available_actions = []
        if user == obj.traveller:
            if obj.status in [obj.STATUS_DRAFT]:
                available_actions.append(
                    ACTION_MAP.get(obj.STATUS_SUBMISSION_REVIEW),
                )
            if obj.status in [obj.STATUS_SUBMISSION_REVIEW]:
                available_actions.append(ACTION_MAP.get(obj.STATUS_DRAFT))
                available_actions.append(ACTION_MAP.get(obj.STATUS_SUBMITTED))
            if obj.status in [obj.STATUS_APPROVED]:
                available_actions.append(ACTION_MAP.get(obj.STATUS_REVIEW))
            if obj.status in [obj.STATUS_APPROVED, obj.STATUS_REVIEW]:
                available_actions.append(ACTION_MAP.get(obj.STATUS_COMPLETED))
            if obj.status in [obj.STATUS_REJECTED]:
                available_actions.append(ACTION_MAP.get(obj.STATUS_DRAFT))
            if obj.status not in [
                    obj.STATUS_CANCELLED,
                    obj.STATUS_SUBMITTED,
                    obj.STATUS_REVIEW,
                    obj.STATUS_COMPLETED,
            ]:
                available_actions.append(ACTION_MAP.get(obj.STATUS_CANCELLED))
        if user == obj.supervisor:
            if obj.status in [obj.STATUS_SUBMITTED]:
                available_actions.append(ACTION_MAP.get(obj.STATUS_APPROVED))
                available_actions.append(ACTION_MAP.get(obj.STATUS_REJECTED))
        return available_actions


class ActivityCreateUpdateSerializer(ActivityBaseSerializer):
    trip = SeparatedReadWriteField(
        read_field=TripSerializer(),
    )


class ItineraryItemUpdateSerializer(ItineraryItemBaseSerializer):
    trip = SeparatedReadWriteField(
        read_field=TripSerializer(),
    )

    def validate(self, data):
        """
        Check that dates are not modified if monitoring_activity is present
        """
        # we only need to check on update since items are automatically created
        if self.instance:
            if self.instance.monitoring_activity:
                ma = self.instance.monitoring_activity
                if data["monitoring_activity"] and data["monitoring_activity"] != ma:
                    raise serializers.ValidationError(_("Monitoring Activity cannot be updated"))
                if data["start_date"] and data["start_date"] != ma.start_date:
                    # TODO: is this needed? Maybe the user has their own travel plans outside of the dates of the ma
                    pass
                if data["end_date"] and data["end_date"] != ma.end_date:
                    # TODO: is this needed? Maybe the user has their own travel plans outside of the dates of the ma
                    pass
                if data["destination"] and data["destination"] != ma.destination_str:
                    raise serializers.ValidationError(_("Destination cannot be edited as this item relates to a "
                                                        "Monitoring Activity, please update the record in FM module"))
        return data


class TripExportSerializer(TripSerializer):
    itinerary_items = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    class Meta(TripSerializer.Meta):
        fields = [
            "id",
            "reference_number",
            "status",
            "supervisor",
            "description",
            "start_date",
            "end_date",
            "traveller",
            "itinerary_items",
            "activities",
        ]

    def get_itinerary_items(self, obj):
        return ", ".join([str(a) for a in obj.items.all()])

    def get_activities(self, obj):
        return ", ".join([str(a) for a in obj.activities.all()])


class TripStatusSerializer(TripSerializer):
    class Meta(TripSerializer.Meta):
        read_only_fields = ["reference_number"]

    def validate(self, data):
        data = super().validate(data)
        if self.instance and self.instance.status == data.get("status"):
            raise serializers.ValidationError(
                f"Status is already {self.instance.status}"
            )
        return data


class TripStatusHistorySerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False)

    class Meta:
        model = TripStatusHistory
        fields = ["trip", "status", "comment"]

    def validate(self, data):
        data = super().validate(data)
        if data["status"] == Trip.STATUS_REJECTED:
            if not data.get("comment"):
                raise serializers.ValidationError(
                    _("Comment is required when rejecting."),
                )
        return data


class ReportAttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    file_type = FileTypeModelChoiceField(
        label=_("Document Type"),
        queryset=FileType.objects.filter(code="travel_report_docs"),
    )

    class Meta:
        model = Attachment
        fields = ("id", "url", "file_type", "created")

    def update(self, instance, validated_data):
        validated_data["code"] = "travel_report_docs"
        return super().update(instance, validated_data)

    def get_url(self, obj):
        if obj.file:
            url = obj.file.url
            request = self.context.get("request", None)
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return ""


class ReportSerializer(serializers.ModelSerializer):
    attachments = ReportAttachmentSerializer(many=True, required=False)

    class Meta:
        model = Report
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, "initial_data"):
            self.initial_data["trip"] = self._context.get(
                "request"
            ).parser_context["kwargs"].get("nested_1_pk")

    def _set_attachments(self, report, attachment_data):
        content_type = ContentType.objects.get_for_model(Report)
        current = list(Attachment.objects.filter(
            object_id=report.pk,
            content_type=content_type,
        ).all())
        used = []
        for attachment in attachment_data:
            for initial in self.initial_data.get("attachments"):
                pk = initial["id"]
                current = [a for a in current if a.pk != pk]
                file_type = initial.get("file_type")
                if pk not in used and file_type == attachment["file_type"].pk:
                    attachment = Attachment.objects.filter(pk=pk).update(
                        file_type=attachment["file_type"],
                        code="travel_report_docs",
                        object_id=report.pk,
                        content_type=content_type,
                    )
                    used.append(pk)
                    break
        for attachment in current:
            attachment.delete()

    def create(self, validated_data):
        attachment_data = None
        if "attachments" in validated_data:
            attachment_data = validated_data.pop("attachments")

        report = Report.objects.create(**validated_data)

        if attachment_data is not None:
            self._set_attachments(report, attachment_data)
        return report

    def update(self, instance, validated_data):
        attachment_data = None
        if "attachments" in validated_data:
            attachment_data = validated_data.pop("attachments")

        instance.narrative = validated_data.get(
            "narrative",
            instance.narrative,
        )
        instance.save()

        if attachment_data is not None:
            self._set_attachments(instance, attachment_data)
        return instance