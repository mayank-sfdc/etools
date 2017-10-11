from __future__ import unicode_literals

from rest_framework import serializers

from funds.models import (
    Donor,
    FundsCommitmentHeader,
    FundsCommitmentItem,
    FundsReservationHeader,
    FundsReservationItem,
    Grant,
)


class FRHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundsReservationHeader
        fields = '__all__'


class FRsSerializer(serializers.Serializer):
    frs = FRHeaderSerializer(source="*", many=True)
    total_frs_amt = serializers.SerializerMethodField()
    total_outstanding_amt = serializers.SerializerMethodField()
    total_intervention_amt = serializers.SerializerMethodField()
    total_actual_amt = serializers.SerializerMethodField()
    earliest_start_date = serializers.SerializerMethodField()
    latest_end_date = serializers.SerializerMethodField()

    def get_earliest_start_date(self, obj):
        seq = [i.start_date for i in obj.all()]
        return min(seq) if seq else None

    def get_latest_end_date(self, obj):
        seq = [i.end_date for i in obj.all()]
        return max(seq) if seq else None

    def get_total_frs_amt(self, obj):
        return sum([i.total_amt for i in obj.all()])

    def get_total_outstanding_amt(self, obj):
        return sum([i.outstanding_amt for i in obj.all()])

    def get_total_intervention_amt(self, obj):
        return sum([i.intervention_amt for i in obj.all()])

    def get_total_actual_amt(self, obj):
        return sum([i.actual_amt for i in obj.all()])


class FundsReservationHeaderExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundsReservationHeader
        fields = '__all__'


class FundsReservationHeaderExportFlatSerializer(FundsReservationHeaderExportSerializer):
    intervention = serializers.CharField(source="intervention.number")


class FundsReservationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundsReservationItem
        fields = "__all__"


class FundsReservationItemExportSerializer(FundsReservationItemSerializer):
    intervention = serializers.CharField(source="fund_reservation.intervention.pk")


class FundsReservationItemExportFlatSerializer(FundsReservationItemExportSerializer):
    intervention = serializers.CharField(source="fund_reservation.intervention.number")
    fund_reservation = serializers.CharField(source="fund_reservation.fr_number")


class FundsCommitmentHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundsCommitmentHeader
        fields = "__all__"


class FundsCommitmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundsCommitmentItem
        fields = "__all__"


class FundsCommitmentItemExportFlatSerializer(FundsCommitmentItemSerializer):
    fund_commitment = serializers.CharField(source="fund_commitment.fc_number")


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = "__all__"


class GrantExportFlatSerializer(GrantSerializer):
    donor = serializers.CharField(source="donor.name")


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = "__all__"


class DonorExportSerializer(DonorSerializer):
    grant = serializers.SerializerMethodField()

    def get_grant(self, obj):
        return ", ".join([str(g.pk) for g in obj.grant_set.all()])


class DonorExportFlatSerializer(DonorExportSerializer):
    def get_grant(self, obj):
        return ", ".join([g.name for g in obj.grant_set.all()])
