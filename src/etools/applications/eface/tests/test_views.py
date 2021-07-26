from django.utils import timezone

from rest_framework import status

from etools.applications.eface.tests.factories import EFaceFormFactory, FormActivityFactory
from etools.applications.field_monitoring.tests.base import APIViewSetTestCase
from etools.applications.partners.tests.factories import (
    InterventionFactory,
    InterventionResultLinkFactory,
    PartnerStaffFactory,
)
from etools.applications.reports.models import ResultType
from etools.applications.reports.tests.factories import InterventionActivityFactory, ResultFactory
from etools.applications.users.tests.factories import UserFactory


class TestFormsView(APIViewSetTestCase):
    base_view = 'eface_v1:forms'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.unicef_user = UserFactory()

    def test_list(self):
        forms = [
            EFaceFormFactory(),
            EFaceFormFactory(),
        ]
        self._test_list(self.unicef_user, forms)

    def test_partner_list(self):
        form1 = EFaceFormFactory()
        EFaceFormFactory()
        staff_member = PartnerStaffFactory()
        form1.intervention.partner_focal_points.add(staff_member)
        self._test_list(staff_member.user, [form1])

    def test_detail_pd_activities_presented(self):
        form = EFaceFormFactory()
        activity = InterventionActivityFactory(
            result__result_link=InterventionResultLinkFactory(
                intervention=form.intervention,
                cp_output=ResultFactory(result_type__name=ResultType.OUTPUT),
            ),
        )
        response = self._test_retrieve(self.unicef_user, form)
        self.assertEqual(
            response.data['intervention']['result_links'][0]['ll_results'][0]['activities'][0]['id'],
            activity.id
        )

    def test_detail_activities_presented(self):
        form = EFaceFormFactory()
        activity = FormActivityFactory(form=form)
        response = self._test_retrieve(self.unicef_user, form)
        self.assertIn('activities', response.data)
        self.assertEqual(activity.id, response.data['activities'][0]['id'])

    def test_detail_user_title_presented(self):
        submitted_by = UserFactory()
        form = EFaceFormFactory(submitted_by=submitted_by)
        response = self._test_retrieve(self.unicef_user, form)
        self.assertEqual(response.data['submitted_by']['title'], submitted_by.profile.job_title)

    def test_update(self):
        form = EFaceFormFactory()
        staff_member = PartnerStaffFactory()
        form.intervention.partner_focal_points.add(staff_member)
        response = self._test_update(staff_member.user, form, {'title': 'new'})
        self.assertEqual(response.data['title'], 'new')
        form.refresh_from_db()
        self.assertEqual(form.title, 'new')

    def test_create(self):
        staff_member = PartnerStaffFactory()
        self._test_create(
            staff_member.user,
            {
                'intervention': InterventionFactory(agreement__partner=staff_member.partner).pk,
                'title': 'test',
                'request_type': 'dct',
            }
        )

    def test_flow(self):
        form = EFaceFormFactory()
        staff_member = PartnerStaffFactory()
        form.intervention.partner_focal_points.add(staff_member)
        form.intervention.unicef_focal_points.add(self.unicef_user)

        def goto(next_status, user, extra_data=None):
            data = {
                'status': next_status
            }
            if extra_data:
                data.update(extra_data)

            return self._test_update(user, form, data)

        response = goto('submitted', staff_member.user)
        self.assertEqual(response.data['status'], 'submitted')
        response = goto('rejected', self.unicef_user)
        self.assertEqual(response.data['status'], 'rejected')
        response = goto('submitted', staff_member.user)
        self.assertEqual(response.data['status'], 'submitted')
        response = goto('pending', self.unicef_user)
        self.assertEqual(response.data['status'], 'pending')
        response = goto('approved', self.unicef_user)
        self.assertEqual(response.data['status'], 'approved')

    def test_bad_transition(self):
        form = EFaceFormFactory()
        form.intervention.unicef_focal_points.add(self.unicef_user)
        self._test_update(self.unicef_user, form, {'status': 'finalized'}, expected_status=400)

    def test_month_year_input(self):
        form = EFaceFormFactory()
        staff_member = PartnerStaffFactory()
        form.intervention.partner_focal_points.add(staff_member)
        now = timezone.now().date()
        response = self._test_update(staff_member.user, form, {'authorized_amount_date_start': now.strftime('%m/%Y')})
        self.assertEqual(response.data['authorized_amount_date_start'], now.strftime('%m/%Y'))
        form.refresh_from_db()
        self.assertEqual(form.authorized_amount_date_start, now.replace(day=1))

    def test_change_activities(self):
        form = EFaceFormFactory()
        staff_member = PartnerStaffFactory()
        form.intervention.partner_focal_points.add(staff_member)
        activity = FormActivityFactory(form=form, kind='custom')
        response = self._test_update(
            staff_member.user, form,
            {
                'activities': [
                    {
                        'kind': 'custom',
                        'description': 'test',
                    },
                    {
                        'id': activity.id,
                        'description': 'new',
                    },
                    {
                        'kind': 'activity',
                        'pd_activity': InterventionActivityFactory(
                            result__result_link=InterventionResultLinkFactory(
                                intervention=form.intervention,
                                cp_output=ResultFactory(result_type__name=ResultType.OUTPUT),
                            ),
                        ).id,
                    }
                ],
            }
        )
        activity.refresh_from_db()
        self.assertEqual(activity.description, 'new')
        self.assertEqual(len(response.data['activities']), 3)
        self.assertEqual(form.activities.count(), 3)

        third_activity = form.activities.filter(kind='activity').first()
        self.assertIsNotNone(third_activity.pd_activity)


class UsersAPITestCase(APIViewSetTestCase):
    base_view = 'eface_v1:users'

    def test_list(self):
        user1 = UserFactory(is_staff=True)
        user = UserFactory(is_staff=True)
        UserFactory()
        self._test_list(user, [user1, user])

    def test_not_staff(self):
        self._test_list(UserFactory(is_staff=False), expected_status=status.HTTP_403_FORBIDDEN)
