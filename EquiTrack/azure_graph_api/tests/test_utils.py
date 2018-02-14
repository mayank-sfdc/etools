from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.auth import get_user_model

from azure_graph_api.utils import handle_record, handle_records
from mock import patch

from EquiTrack.factories import GroupFactory, UserFactory
from EquiTrack.tests.cases import EToolsTenantTestCase


class TestClient(EToolsTenantTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.group = GroupFactory(name='UNICEF User')

    @patch('azure_graph_api.utils.handle_record')
    def test_handle_records(self, handle_function):
        handle_records({'value': range(3)})
        self.assertEqual(handle_function.call_count, 3)
        self.assertEqual(handle_function.call_args[0], (2, ))

    def test_handle_record_create(self):
        self.assertEqual(get_user_model().objects.count(), 0)
        user_record = {
            'givenName': 'Joe',
            'mail': 'jdoe@unicef.org',
            'surname': 'Doe',
            'userPrincipalName': 'jdoe@unicef.org'
        }
        handle_record(user_record)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_handle_record_update(self):
        UserFactory(username='jdoe@unicef.org', email='jdoe@unicef.org')
        self.assertEqual(get_user_model().objects.count(), 1)
        user_record = {
            'givenName': 'Joe',
            'mail': 'jdoe@unicef.org',
            'surname': 'Doe',
            'userPrincipalName': 'jdoe@unicef.org'
        }
        handle_record(user_record)
        self.assertEqual(get_user_model().objects.count(), 1)
