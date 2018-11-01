from datetime import date, timedelta

from django.urls import reverse

from rest_framework import status

from etools.applications.EquiTrack.tests.cases import BaseTenantTestCase
from etools.applications.field_monitoring.settings.models import CPOutputConfig
from etools.applications.field_monitoring.settings.tests.factories import (
    CPOutputConfigFactory, LocationSiteFactory, MethodTypeFactory, PlannedCheckListItemFactory, CheckListItemFactory,
    MethodFactory)
from etools.applications.field_monitoring.tests.base import FMBaseTestCaseMixin
from etools.applications.partners.models import PartnerType
from etools.applications.partners.tests.factories import PartnerFactory
from etools.applications.reports.models import ResultType
from etools.applications.reports.tests.factories import ResultFactory


class MethodsViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    fixtures = ('field_monitoring_methods',)

    def test_fixture_list(self):
        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:methods-list'),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)


class MethodTypesViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    def test_list(self):
        MethodTypeFactory()

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:method-types-list'),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class MethodSitesViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    def test_list(self):
        LocationSiteFactory()

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:sites-list'),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_cached(self):
        LocationSiteFactory()

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:sites-list'),
            user=self.unicef_user
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        etag = response["ETag"]

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:sites-list'),
            user=self.unicef_user, HTTP_IF_NONE_MATCH=etag
        )
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_list_modified(self):
        LocationSiteFactory()

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:sites-list'),
            user=self.unicef_user
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        etag = response["ETag"]

        LocationSiteFactory()

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:sites-list'),
            user=self.unicef_user, HTTP_IF_NONE_MATCH=etag
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create(self):
        site = LocationSiteFactory()

        response = self.forced_auth_req(
            'post', reverse('field_monitoring_settings:sites-list'),
            user=self.unicef_user,
            data={
                'name': site.name,
                'security_detail': site.security_detail,
                'point': {
                    "type": "Point",
                    "coordinates": [125.6, 10.1]
                }
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['parent'])


class CPOutputsConfigViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.active_result = ResultFactory(result_type__name=ResultType.OUTPUT)
        cls.inactive_result = ResultFactory(result_type__name=ResultType.OUTPUT, to_date=date.today() - timedelta(days=1))  # inactual
        cls.default_config = CPOutputConfigFactory(is_monitored=True)

    def test_list(self):
        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:cp_outputs-list'),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertIn('interventions', response.data['results'][0])

    def test_list_filter_active(self):
        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:cp_outputs-list'),
            user=self.unicef_user,
            data={'is_active': True}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_filter_inactive(self):
        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:cp_outputs-list'),
            user=self.unicef_user,
            data={'is_active': False}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_filter_monitored(self):
        monitored_config = CPOutputConfigFactory(is_monitored=True)
        CPOutputConfigFactory(is_monitored=False)

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:cp_outputs-list'),
            user=self.unicef_user,
            data={'fm_config__is_monitored': True}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            sorted([c['fm_config']['id'] for c in response.data['results']]),
            [self.default_config.id, monitored_config.id]
        )

    def test_create(self):
        cp_output = ResultFactory(result_type__name=ResultType.OUTPUT)

        self.assertFalse(CPOutputConfig.objects.filter(cp_output=cp_output).exists())

        response = self.forced_auth_req(
            'patch', reverse('field_monitoring_settings:cp_outputs-detail', args=[cp_output.id]),
            user=self.unicef_user,
            data={
                'fm_config': {
                    'is_monitored': True,
                    'government_partners': [PartnerFactory(partner_type=PartnerType.GOVERNMENT).id]
                }
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CPOutputConfig.objects.filter(cp_output=cp_output).exists())

    def test_update(self):
        cp_output_config = CPOutputConfigFactory(is_monitored=False)

        partners_num = cp_output_config.government_partners.count()
        response = self.forced_auth_req(
            'patch', reverse('field_monitoring_settings:cp_outputs-detail', args=[cp_output_config.cp_output.id]),
            user=self.unicef_user,
            data={
                'fm_config': {
                    'is_monitored': True,
                    'government_partners': list(cp_output_config.government_partners.values_list('id', flat=True)) + [
                        PartnerFactory(partner_type=PartnerType.GOVERNMENT).id]
                }
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fm_config']['government_partners']), partners_num + 1)
        self.assertEqual(response.data['fm_config']['is_monitored'], True)


class CheckListCategoriesViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    fixtures = ['field_monitoring_checklist']

    def test_categories(self):
        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:checklist-categories-list'),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 6)


class CheckListViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    fixtures = ['field_monitoring_checklist']

    def test_checklist(self):
        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:checklist-items-list'),
            user=self.unicef_user,
            data={'page_size': 'all'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 20)


class PlannedCheckListItemViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    def test_create(self):
        response = self.forced_auth_req(
            'post',
            reverse('field_monitoring_settings:planned-checklist-items-list', args=[CPOutputConfigFactory().pk]),
            user=self.unicef_user,
            data={
                'checklist_item': CheckListItemFactory().id,
                'methods': [MethodFactory().pk, MethodFactory().pk],
                'partners_info': [{
                    'partner': PartnerFactory().pk,
                    'specific_details': 'test',
                    'standard_url': 'test',
                }]
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['methods']), 2)
        self.assertEqual(len(response.data['partners_info']), 1)

    def test_create_without_partner(self):
        response = self.forced_auth_req(
            'post',
            reverse('field_monitoring_settings:planned-checklist-items-list', args=[CPOutputConfigFactory().pk]),
            user=self.unicef_user,
            data={
                'checklist_item': CheckListItemFactory().id,
                'partners_info': [{
                    'partner': None,
                    'specific_details': 'test',
                    'standard_url': 'test',
                }]
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_partner_info(self):
        item = PlannedCheckListItemFactory(partners_info__count=1)
        partner_info_id = item.partners_info.first().id

        response = self.forced_auth_req(
            'patch', reverse('field_monitoring_settings:planned-checklist-items-detail',
                             args=[item.cp_output_config.pk, item.pk]),
            user=self.unicef_user,
            data={
                'partners_info': [{
                    'id': partner_info_id,
                    '_delete': True
                }, {
                    'partner': None,
                    'specific_details': 'test',
                    'standard_url': 'test',
                }]
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['partners_info']), 1)
        self.assertNotEqual(response.data['partners_info'][0]['id'], partner_info_id)

    def test_list(self):
        item = PlannedCheckListItemFactory(methods__count=1, partners_info__count=1)

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_settings:planned-checklist-items-list', args=[item.cp_output_config.pk]),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
