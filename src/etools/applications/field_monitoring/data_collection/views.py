from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.utils.translation import ugettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from unicef_attachments.models import Attachment
from unicef_restlib.views import NestedViewSetMixin

from etools.applications.field_monitoring.data_collection.models import (
    ActivityOverallFinding,
    ActivityQuestion,
    ActivityQuestionOverallFinding,
    ChecklistOverallFinding,
    Finding,
    StartedChecklist,
)
from etools.applications.field_monitoring.data_collection.offline.blueprint import get_blueprint_for_activity_and_method
from etools.applications.field_monitoring.data_collection.offline.helpers import (
    create_checklist,
    get_checklist_form_value,
    update_checklist,
)
from etools.applications.field_monitoring.data_collection.serializers import (
    ActivityDataCollectionSerializer,
    ActivityOverallFindingSerializer,
    ActivityQuestionOverallFindingSerializer,
    ActivityQuestionSerializer,
    ChecklistAttachmentSerializer,
    ChecklistOverallFindingSerializer,
    ChecklistSerializer,
    FindingSerializer,
)
from etools.applications.field_monitoring.fm_settings.models import Method
from etools.applications.field_monitoring.fm_settings.serializers import FMCommonAttachmentSerializer, MethodSerializer
from etools.applications.field_monitoring.permissions import (
    activity_field_is_editable_permission,
    IsEditAction,
    IsReadAction,
)
from etools.applications.field_monitoring.planning.models import MonitoringActivity
from etools.applications.field_monitoring.views import (
    AttachmentFileTypesViewMixin,
    BulkUpdateMixin,
    FMBaseViewSet,
    LinkedAttachmentsViewSet,
)
from etools.applications.offline.errors import ValidationError
from etools.applications.partners.views.helpers import set_tenant_or_fail

User = get_user_model()


class ActivityDataCollectionViewSet(
    FMBaseViewSet,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = MonitoringActivity.objects.all()
    serializer_class = ActivityDataCollectionSerializer

    def get_queryset(self, format=None):
        workspace = self.request.query_params.get('workspace', None)
        if workspace:
            set_tenant_or_fail(workspace)

        return super().get_queryset()

    @action(detail=True, url_path=r'offline/(?P<method_pk>\d+)', url_name='offline')
    def offline(self, request, *args, method_pk=None, **kwargs):
        method = get_object_or_404(Method.objects, pk=method_pk)
        user_email = self.request.query_params.get('user', '')
        user = get_object_or_404(User.objects, email=user_email)
        try:
            create_checklist(self.get_object(), method, user, request.data)
        except ValidationError as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=ex.detail)

        return Response(status=status.HTTP_201_CREATED)


class ActivityReportAttachmentsViewSet(LinkedAttachmentsViewSet):
    serializer_class = FMCommonAttachmentSerializer
    related_model = MonitoringActivity
    permission_classes = FMBaseViewSet.permission_classes + [
        IsReadAction | (IsEditAction & activity_field_is_editable_permission('report_attachments'))
    ]
    attachment_code = 'report_attachments'

    def get_view_name(self):
        return _('Report Attachments')


class ActivityQuestionsViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    BulkUpdateMixin,
    viewsets.GenericViewSet,
):
    permission_classes = FMBaseViewSet.permission_classes + [
        IsReadAction | (IsEditAction & activity_field_is_editable_permission('activity_question_set'))
    ]
    queryset = ActivityQuestion.objects.select_related(
        'question', 'partner', 'cp_output', 'intervention'
    ).prefetch_related(
        'cp_output__result_type',
        'question__methods',
        'question__sections',
        'question__options',
    ).order_by(
        'partner_id', 'cp_output_id', 'intervention_id', 'id'
    )
    serializer_class = ActivityQuestionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_enabled',)


class ActivityMethodsViewSet(
    FMBaseViewSet,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MethodSerializer

    def get_queryset(self):
        activity = get_object_or_404(MonitoringActivity.objects, pk=self.kwargs['monitoring_activity_pk'])
        return Method.objects.filter(
            pk__in=activity.questions.filter(
                is_enabled=True
            ).values_list('question__methods', flat=True)
        )


class ChecklistsViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = FMBaseViewSet.permission_classes + [
        IsReadAction | (IsEditAction & activity_field_is_editable_permission('started_checklist_set'))
    ]
    queryset = StartedChecklist.objects.prefetch_related('author')
    serializer_class = ChecklistSerializer
    filter_backend = (DjangoFilterBackend,)
    filter_fields = ('author',)

    def perform_create(self, serializer):
        serializer.save(monitoring_activity=self.get_parent_object())

    @action(detail=True, methods=['GET', 'POST'], url_name='blueprint')
    def blueprint(self, request, *args, **kwargs):
        checklist = self.get_object()
        if request.method.upper() != 'GET':
            update_checklist(checklist, request.data)
            checklist.refresh_from_db()

        return Response(
            data={
                'blueprint': get_blueprint_for_activity_and_method(
                    checklist.monitoring_activity,
                    checklist.method,
                ).to_dict(),
                'value': get_checklist_form_value(checklist)
            }
        )


class ChecklistOverallFindingsViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = FMBaseViewSet.permission_classes + [
        IsReadAction | (IsEditAction & activity_field_is_editable_permission('started_checklist_set'))
    ]
    queryset = ChecklistOverallFinding.objects.prefetch_related(
        'partner', 'cp_output', 'intervention', 'attachments'
    )
    serializer_class = ChecklistOverallFindingSerializer


class ChecklistOverallAttachmentsViewSet(LinkedAttachmentsViewSet):
    permission_classes = FMBaseViewSet.permission_classes + [
        IsReadAction | (IsEditAction & activity_field_is_editable_permission('started_checklist_set'))
    ]
    related_model = ChecklistOverallFinding
    serializer_class = FMCommonAttachmentSerializer
    attachment_code = 'attachments'


class ChecklistFindingsViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    BulkUpdateMixin,
    viewsets.GenericViewSet,
):
    permission_classes = FMBaseViewSet.permission_classes + [
        IsReadAction | (IsEditAction & activity_field_is_editable_permission('started_checklist_set'))
    ]
    queryset = Finding.objects.select_related(
        'activity_question__question',
        'activity_question__partner',
        'activity_question__intervention',
        'activity_question__cp_output',
    ).prefetch_related(
        'activity_question__question__options',
        'activity_question__question__methods',
        'activity_question__question__sections',
    )
    serializer_class = FindingSerializer


class ActivityOverallFindingsViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = FMBaseViewSet.permission_classes + [
        IsReadAction | (IsEditAction & activity_field_is_editable_permission('activity_overall_finding'))
    ]
    queryset = ActivityOverallFinding.objects.prefetch_related(
        'partner', 'cp_output', 'intervention',
        'monitoring_activity__checklists__overall_findings__attachments',
        'monitoring_activity__checklists__author',
    )
    serializer_class = ActivityOverallFindingSerializer


class ActivityFindingsViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    BulkUpdateMixin,
    viewsets.GenericViewSet,
):
    permission_classes = FMBaseViewSet.permission_classes + [
        IsReadAction | (IsEditAction & activity_field_is_editable_permission('activity_overall_finding'))
    ]
    queryset = ActivityQuestionOverallFinding.objects.select_related(
        'activity_question__question',
        'activity_question__partner',
        'activity_question__intervention',
        'activity_question__cp_output',
    ).prefetch_related(
        Prefetch(
            'activity_question__findings',
            Finding.objects.filter(value__isnull=False).prefetch_related(
                'started_checklist', 'started_checklist__author',
            ),
            to_attr='completed_findings'
        ),
        'activity_question__question__options',
    )
    serializer_class = ActivityQuestionOverallFindingSerializer

    def get_parent_filter(self):
        return {'activity_question__monitoring_activity_id': self.kwargs['monitoring_activity_pk']}


class ActivityChecklistAttachmentsViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    AttachmentFileTypesViewMixin,
    viewsets.ReadOnlyModelViewSet,
):
    serializer_class = ChecklistAttachmentSerializer
    queryset = Attachment.objects.filter(
        content_type__app_label=ChecklistOverallFinding._meta.app_label,
        content_type__model=ChecklistOverallFinding._meta.model_name,
    ).prefetch_related(
        'content_object__intervention',
        'content_object__cp_output',
        'content_object__partner',
    ).select_related('uploaded_by').order_by('object_id')

    def get_parent_filter(self):
        parent = self.get_parent_object()
        if not parent:
            return {}

        return {
            'object_id__in': ChecklistOverallFinding.objects.filter(
                started_checklist__monitoring_activity_id=parent.id
            ).values_list('pk', flat=True)
        }
