from unittest.mock import Mock

from etools.applications.audit.models import UNICEFAuditFocalPoint
from etools.applications.audit.tests.factories import AuditPartnerFactory
from etools.applications.core.tests.cases import BaseTenantTestCase
from etools.applications.psea import serializers
from etools.applications.psea.models import Assessment, Assessor
from etools.applications.psea.tests.factories import AnswerFactory, AssessmentFactory, AssessorFactory, RatingFactory
from etools.applications.users.tests.factories import GroupFactory, UserFactory


def expected_status_list(statuses):
    return [s for s in Assessment.STATUS_CHOICES if s[0] in statuses]


class TestAssessmentSerializer(BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mock_view = Mock(action="retrieve")
        cls.focal_user = UserFactory()
        cls.focal_user.groups.add(
            GroupFactory(name=UNICEFAuditFocalPoint.name),
        )
        cls.mock_request = Mock(user=cls.focal_user)
        cls.serializer = serializers.AssessmentSerializer(
            context={"view": cls.mock_view, "request": cls.mock_request},
        )

    def setUp(self):
        self.mock_view.action = "retrieve"
        self.mock_request.user = self.focal_user

    def test_get_overall_rating_none(self):
        assessment = AssessmentFactory()
        overall_rating = self.serializer.get_overall_rating(assessment)
        self.assertEqual(overall_rating, {
            "value": None,
            "display": "",
        })

    def test_get_overall_rating_high(self):
        assessment = AssessmentFactory()
        rating = RatingFactory(weight=1)
        AnswerFactory(assessment=assessment, rating=rating)
        overall_rating = self.serializer.get_overall_rating(assessment)
        self.assertEqual(overall_rating, {
            "value": 1,
            "display": "High",
        })

    def test_get_overall_rating_moderate(self):
        assessment = AssessmentFactory()
        rating = RatingFactory(weight=5)
        for _ in range(3):
            AnswerFactory(assessment=assessment, rating=rating)
        overall_rating = self.serializer.get_overall_rating(assessment)
        self.assertEqual(overall_rating, {
            "value": 15,
            "display": "Moderate",
        })

    def test_get_overall_rating_low(self):
        assessment = AssessmentFactory()
        rating = RatingFactory(weight=5)
        for _ in range(5):
            AnswerFactory(assessment=assessment, rating=rating)
        overall_rating = self.serializer.get_overall_rating(assessment)
        self.assertEqual(overall_rating, {
            "value": 25,
            "display": "Low",
        })

    def test_get_assessor_none(self):
        assessment = AssessmentFactory()
        self.assertEqual(self.serializer.get_assessor(assessment), "")

    def test_get_assessor_user(self):
        assessment = AssessmentFactory()
        user = UserFactory(first_name="First", last_name="Last")
        AssessorFactory(
            assessment=assessment,
            user=user,
            assessor_type=Assessor.TYPE_EXTERNAL,
        )
        self.assertEqual(
            self.serializer.get_assessor(assessment),
            "First Last",
        )

    def test_get_assessor_firm(self):
        assessment = AssessmentFactory()
        firm = AuditPartnerFactory(name="Firm Name")
        AssessorFactory(
            assessment=assessment,
            auditor_firm=firm,
            assessor_type=Assessor.TYPE_VENDOR,
        )
        self.assertEqual(self.serializer.get_assessor(assessment), "Firm Name")

    def test_get_status_list_default(self):
        assessment = AssessmentFactory()
        status_list = self.serializer.get_status_list(assessment)
        self.assertEqual(status_list, expected_status_list([
            assessment.STATUS_DRAFT,
            assessment.STATUS_IN_PROGRESS,
            assessment.STATUS_SUBMITTED,
            assessment.STATUS_FINAL,
        ]))

    def test_get_status_list_cancelled(self):
        assessment = AssessmentFactory()
        assessment.status = assessment.STATUS_CANCELLED
        assessment.save()
        status_list = self.serializer.get_status_list(assessment)
        self.assertEqual(status_list, expected_status_list([
            assessment.STATUS_DRAFT,
            assessment.STATUS_CANCELLED,
        ]))

    def test_get_status_list_rejected(self):
        assessment = AssessmentFactory()
        assessment.status = assessment.STATUS_REJECTED
        assessment.save()
        status_list = self.serializer.get_status_list(assessment)
        self.assertEqual(status_list, expected_status_list([
            assessment.STATUS_DRAFT,
            assessment.STATUS_REJECTED,
            assessment.STATUS_IN_PROGRESS,
            assessment.STATUS_SUBMITTED,
            assessment.STATUS_FINAL,
        ]))

    def test_get_available_actions_view_list(self):
        assessment = AssessmentFactory()
        self.assertEqual(assessment.status, assessment.STATUS_DRAFT)
        self.serializer.context["view"].action = "list"
        self.assertEqual(
            self.serializer.get_available_actions(assessment),
            [],
        )

    def test_get_available_actions_draft_focal(self):
        assessment = AssessmentFactory()
        self.assertEqual(assessment.status, assessment.STATUS_DRAFT)
        self.assertEqual(
            self.serializer.get_available_actions(assessment),
            ["assign", "cancel"],
        )

    def test_get_available_actions_submitted_focal(self):
        assessment = AssessmentFactory()
        assessment.status = assessment.STATUS_SUBMITTED
        assessment.save()
        self.assertEqual(assessment.status, assessment.STATUS_SUBMITTED)
        self.assertEqual(
            self.serializer.get_available_actions(assessment),
            ["reject", "finalize"],
        )

    def test_get_available_actions_assessor_in_progress(self):
        assessment = AssessmentFactory()
        assessment.status = assessment.STATUS_IN_PROGRESS
        assessment.save()
        assessor = AssessorFactory(assessment=assessment)
        self.assertEqual(assessment.status, assessment.STATUS_IN_PROGRESS)
        self.serializer.context["request"].user = assessor.user
        self.assertEqual(
            self.serializer.get_available_actions(assessment),
            ["submit"],
        )