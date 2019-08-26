from datetime import date, timedelta

import factory
from factory import fuzzy
from unicef_locations.tests.factories import LocationFactory

from etools.applications.field_monitoring.fm_settings.tests.factories import QuestionFactory
from etools.applications.field_monitoring.planning.models import MonitoringActivity, YearPlan, QuestionTemplate
from etools.applications.field_monitoring.tests.factories import UserFactory
from etools.libraries.tests.factories import StatusFactoryMetaClass


class YearPlanFactory(factory.DjangoModelFactory):
    year = date.today().year

    prioritization_criteria = fuzzy.FuzzyText()
    methodology_notes = fuzzy.FuzzyText()
    target_visits = fuzzy.FuzzyInteger(0, 100)
    modalities = fuzzy.FuzzyText()
    partner_engagement = fuzzy.FuzzyText()

    class Meta:
        model = YearPlan
        django_get_or_create = ('year',)


class BaseMonitoringActivityFactory(factory.DjangoModelFactory):
    # tpm_partner = factory.SubFactory(TPMPartnerFactory)
    activity_type = 'staff'
    location = factory.SubFactory(LocationFactory)

    start_date = date.today()
    end_date = date.today() + timedelta(days=30)

    class Meta:
        model = MonitoringActivity

    @factory.post_generation
    def team_members(self, created, extracted, **kwargs):
        if extracted:
            self.team_members.add(*extracted)


class DraftActivityFactory(BaseMonitoringActivityFactory):
    status = MonitoringActivity.STATUSES.draft


class ChecklistActivityFactory(DraftActivityFactory):
    status = MonitoringActivity.STATUSES.checklist


class ReviewActivityFactory(ChecklistActivityFactory):
    status = MonitoringActivity.STATUSES.review


class AssignedActivityFactory(ReviewActivityFactory):
    status = MonitoringActivity.STATUSES.assigned


class PreDataCollectionActivityFactory(AssignedActivityFactory):
    person_responsible = factory.SubFactory(UserFactory, unicef_user=True)


class DataCollectionActivityFactory(PreDataCollectionActivityFactory):
    status = MonitoringActivity.STATUSES.data_collection


class ReportFinalizationActivityFactory(DataCollectionActivityFactory):
    status = MonitoringActivity.STATUSES.report_finalization


class SubmittedActivityFactory(ReportFinalizationActivityFactory):
    status = MonitoringActivity.STATUSES.submitted


class CompletedActivityFactory(SubmittedActivityFactory):
    status = MonitoringActivity.STATUSES.completed


class CancelledActivityFactory(DraftActivityFactory):
    status = MonitoringActivity.STATUSES.cancelled


class MonitoringActivityFactory(BaseMonitoringActivityFactory, metaclass=StatusFactoryMetaClass):
    status_factories = {
        'draft': DraftActivityFactory,
        'checklist': ChecklistActivityFactory,
        'review': ReviewActivityFactory,
        'assigned': AssignedActivityFactory,
        'pre_data_collection': PreDataCollectionActivityFactory,
        'data_collection': DataCollectionActivityFactory,
        'report_finalization': ReportFinalizationActivityFactory,
        'submitted': SubmittedActivityFactory,
        'completed': CompletedActivityFactory,
        'cancelled': CancelledActivityFactory,
    }


class QuestionTemplateFactory(factory.DjangoModelFactory):
    question = factory.SubFactory(QuestionFactory)
    specific_details = fuzzy.FuzzyText()

    class Meta:
        model = QuestionTemplate
