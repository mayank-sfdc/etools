from django.db import connection
from django.utils import timezone

from etools.applications.audit.tests.factories import AuditPartnerFactory
from etools.applications.core.tests.cases import BaseTenantTestCase
from etools.applications.psea.models import Answer, Assessment, Assessor
from etools.applications.psea.tests.factories import (
    AnswerEvidenceFactory,
    AnswerFactory,
    AssessmentFactory,
    AssessmentStatusHistoryFactory,
    AssessorFactory,
    EvidenceFactory,
    IndicatorFactory,
    RatingFactory,
)
from etools.applications.users.tests.factories import UserFactory


class TestRating(BaseTenantTestCase):
    def test_string(self):
        rating = RatingFactory(label="Test Rating")
        self.assertEqual(str(rating), "Test Rating")


class TestIndicator(BaseTenantTestCase):
    def test_string(self):
        indicator = IndicatorFactory(subject="Test Indicator")
        self.assertEqual(str(indicator), "Test Indicator")


class TestEvidence(BaseTenantTestCase):
    def test_string(self):
        evidence = EvidenceFactory(label="Test Evidence")
        self.assertEqual(str(evidence), "Test Evidence")


class TestAssessment(BaseTenantTestCase):
    def test_string(self):
        assessment = AssessmentFactory()
        self.assertEqual(str(assessment), f"{assessment.partner} [Draft] {assessment.reference_number}")

    def test_rating_none(self):
        assessment = AssessmentFactory()
        self.assertFalse(Answer.objects.filter(assessment=assessment).exists())
        self.assertIsNone(assessment.rating())

    def test_rating(self):
        assessment = AssessmentFactory()
        rating_high = RatingFactory(weight=10)
        rating_medium = RatingFactory(weight=5)
        rating_low = RatingFactory(weight=1)

        AnswerFactory(assessment=assessment, rating=rating_high)
        self.assertEqual(assessment.rating(), 10)

        AnswerFactory(assessment=assessment, rating=rating_medium)
        self.assertEqual(assessment.rating(), 15)

        AnswerFactory(assessment=assessment, rating=rating_low)
        self.assertEqual(assessment.rating(), 16)

        AnswerFactory(assessment=assessment, rating=rating_high)
        self.assertEqual(assessment.rating(), 26)

    def test_get_reference_number(self):
        assessment = AssessmentFactory()
        self.assertEqual(
            assessment.get_reference_number(),
            "{}/{}PSEA{}".format(
                connection.tenant.country_short_code,
                timezone.now().year,
                assessment.pk
            ),
        )


class TestAssessmentStatusHistory(BaseTenantTestCase):
    def test_string(self):
        status = AssessmentStatusHistoryFactory(status=Assessment.STATUS_DRAFT)
        self.assertEqual(str(status), f"Draft [{status.created}]")


class TestAnswer(BaseTenantTestCase):
    def test_string(self):
        answer = AnswerFactory()
        self.assertEqual(str(answer), f"{answer.assessment} [{answer.rating}]")


class TestAnswerEvidence(BaseTenantTestCase):
    def test_string(self):
        answer_evidence = AnswerEvidenceFactory()
        self.assertEqual(str(answer_evidence), f"{answer_evidence.evidence}")


class TestAssessor(BaseTenantTestCase):
    def test_string_unicef(self):
        user = UserFactory()
        assessor = AssessorFactory(
            assessor_type=Assessor.TYPE_UNICEF,
            user=user
        )
        self.assertEqual(str(assessor), f"{user}")

    def test_string_external(self):
        user = UserFactory()
        assessor = AssessorFactory(
            assessor_type=Assessor.TYPE_EXTERNAL,
            user=user
        )
        self.assertEqual(str(assessor), f"{user}")

    def test_string_vendor(self):
        auditor = AuditPartnerFactory()
        assessor = AssessorFactory(
            assessor_type=Assessor.TYPE_VENDOR,
            auditor_firm=auditor,
        )
        self.assertEqual(str(assessor), f"{auditor}")
