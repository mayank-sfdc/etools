# Python imports
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime

# Django imports

# 3rd party imports
# The DRF source code says, "The recommended style for using `ValidationError` is to keep it namespaced
# under `serializers`, in order to minimize potential confusion with Django's built in `ValidationError`."
from rest_framework import serializers

# Project imports
from EquiTrack.factories import (
    AgreementFactory,
    CountryProgrammeFactory,
    InterventionFactory,
    PartnerFactory,
    PartnerStaffFactory,
    UserFactory,
    )
from EquiTrack.tests.mixins import FastTenantTestCase
from partners.models import Agreement, PartnerType
from partners.serializers.agreements_v2 import AgreementCreateUpdateSerializer

_ALL_AGREEMENT_TYPES = [agreement_type[0] for agreement_type in Agreement.AGREEMENT_TYPES]


class TestAgreementCreateUpdateSerializer(FastTenantTestCase):
    '''Exercise the AgreementCreateUpdateSerializer.'''
    def setUp(self):
        self.user = UserFactory()

        self.partner = PartnerFactory(partner_type=PartnerType.CIVIL_SOCIETY_ORGANIZATION)

        self.today = datetime.date.today()

        this_year = self.today.year
        self.country_programme = CountryProgrammeFactory(from_date=datetime.date(this_year - 1, 1, 1),
                                                         to_date=datetime.date(this_year + 1, 1, 1))

        # The serializer examines context['request'].user during the course of its operation. If that's not set, the
        # serializer will fail. It doesn't need a real request object, just something with a .user attribute, so
        # that's what I create here.
        class Stub(object):
            pass
        self.fake_request = Stub()
        self.fake_request.user = self.user

    def test_simple_create(self):
        data = {
            "agreement_type": Agreement.MOU,
            "partner": self.partner.id,
        }
        serializer = AgreementCreateUpdateSerializer(data=data)

        serializer.context['request'] = self.fake_request

        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create_fail_country_programme_required_for_PCA(self):
        '''Ensure correct error is raised for PCAs with no country programme'''
        data = {
            "agreement_type": Agreement.PCA,
            "partner": self.partner.id,
        }
        serializer = AgreementCreateUpdateSerializer()
        serializer.context['request'] = self.fake_request

        with self.assertRaises(serializers.ValidationError) as context_manager:
            serializer.validate(data=data)

        exception = context_manager.exception

        self.assertIsInstance(exception.detail, dict)
        self.assertEqual(exception.detail.keys(), ['country_programme'])
        self.assertEqual(exception.detail['country_programme'], 'Country Programme is required for PCAs!')

    def test_create_fail_one_PCA_per_country_programme_and_partner(self):
        '''Ensure correct error is raised for PCAs with duplicate country programme & partner combo'''
        AgreementFactory(
            agreement_type=Agreement.PCA,
            partner=self.partner,
            country_programme=self.country_programme,
        )

        # Create an agreement of exactly the same type.
        data = {
            "agreement_type": Agreement.PCA,
            "partner": self.partner,
            "country_programme": self.country_programme,
        }
        serializer = AgreementCreateUpdateSerializer()
        serializer.context['request'] = self.fake_request

        with self.assertRaises(serializers.ValidationError) as context_manager:
            serializer.validate(data=data)

        exception = context_manager.exception

        self.assertIsInstance(exception.detail, dict)
        self.assertEqual(exception.detail.keys(), ['errors'])
        self.assertIsInstance(exception.detail['errors'], list)
        expected_msg = 'A different agreement of type PCA already exists for this Partner for this Country Programme'
        self.assertEqual(exception.detail['errors'], [expected_msg])

    def test_create_ok_non_PCA_with_same_programme_and_partner(self):
        '''Ensure it is OK to create non-PCA agreements that have the same country programme and partner.

        This is a sibling test to test_create_fail_one_PCA_per_country_programme_and_partner().
        '''
        agreement_types = [agreement_type for agreement_type in _ALL_AGREEMENT_TYPES if agreement_type != Agreement.PCA]

        for agreement_type in agreement_types:
            AgreementFactory(
                agreement_type=agreement_type,
                partner=self.partner,
                country_programme=self.country_programme,
            )

            # Create an agreement of exactly the same type.
            data = {
                "agreement_type": agreement_type,
                "partner": self.partner.id,
                "country_programme": self.country_programme.id,
            }
            serializer = AgreementCreateUpdateSerializer(data=data)
            serializer.context['request'] = self.fake_request

            self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create_fail_start_date_after_end_date(self):
        '''Ensure create fails if start date is after end date'''
        data = {
            "agreement_type": Agreement.PCA,
            "partner": self.partner,
            "country_programme": self.country_programme,
            "start": self.today + datetime.timedelta(days=5),
            "end": self.today,
        }
        serializer = AgreementCreateUpdateSerializer()
        serializer.context['request'] = self.fake_request

        with self.assertRaises(serializers.ValidationError) as context_manager:
            serializer.validate(data=data)

        exception = context_manager.exception

        self.assertIsInstance(exception.detail, dict)
        self.assertEqual(exception.detail.keys(), ['errors'])
        self.assertIsInstance(exception.detail['errors'], list)
        self.assertEqual(exception.detail['errors'], ['Agreement start date needs to be earlier than end date'])

    def test_create_ok_with_start_date_equal_end_date(self):
        '''Ensure it's OK to create an agreement where the start & end dates are the same.'''
        data = {
            "agreement_type": Agreement.PCA,
            "partner": self.partner.id,
            "country_programme": self.country_programme.id,
            "start": self.today,
            "end": self.today,
        }
        serializer = AgreementCreateUpdateSerializer(data=data)
        serializer.context['request'] = self.fake_request

        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create_ok_when_start_or_end_not_present(self):
        '''Ensure that date validation doesn't kick in when one date or another isn't present'''
        # Test w/start date present but not end date
        data = {
            "agreement_type": Agreement.SSFA,
            "partner": self.partner.id,
            "start": self.today + datetime.timedelta(days=5),
        }
        serializer = AgreementCreateUpdateSerializer(data=data)
        serializer.context['request'] = self.fake_request
        self.assertTrue(serializer.is_valid(raise_exception=True))

        # Test w/end date present but not start date
        data = {
            "agreement_type": Agreement.SSFA,
            "partner": self.partner.id,
            "end": self.today + datetime.timedelta(days=5),
        }
        serializer = AgreementCreateUpdateSerializer(data=data)
        serializer.context['request'] = self.fake_request

        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create_with_partner_type(self):
        '''Exercise create success & failure related to the rules regarding agreement type and partner type'''
        # Set partner to something other than civil society org.
        self.partner.partner_type = PartnerType.UN_AGENCY
        self.partner.save()

        # Create PCA & SSFA should fail now.
        for agreement_type in (Agreement.PCA, Agreement.SSFA):
            data = {
                "agreement_type": agreement_type,
                "country_programme": self.country_programme,
                "partner": self.partner,
            }
            serializer = AgreementCreateUpdateSerializer(data=data)
            serializer.context['request'] = self.fake_request

            with self.assertRaises(serializers.ValidationError) as context_manager:
                serializer.validate(data=data)

            exception = context_manager.exception

            self.assertIsInstance(exception.detail, dict)
            self.assertEqual(exception.detail.keys(), ['errors'])
            self.assertIsInstance(exception.detail['errors'], list)
            self.assertEqual(exception.detail['errors'], ['Partner type must be CSO for PCA or SSFA agreement types.'])

        # Test for all agreement types that are not PCA or SSFA. These should not fail.
        agreement_types = [agreement_type for agreement_type in _ALL_AGREEMENT_TYPES
                           if agreement_type
                           not in (Agreement.PCA, Agreement.SSFA)]

        for agreement_type in agreement_types:
            data = {
                "agreement_type": agreement_type,
                "country_programme": self.country_programme.id,
                "partner": self.partner.id,
            }
            serializer = AgreementCreateUpdateSerializer(data=data)
            serializer.context['request'] = self.fake_request

            self.assertTrue(serializer.is_valid(raise_exception=True))

        # Set partner to civil service org; create all agreement types should succeed
        self.partner.partner_type = PartnerType.CIVIL_SOCIETY_ORGANIZATION
        self.partner.save()

        for agreement_type in _ALL_AGREEMENT_TYPES:
            data = {
                "agreement_type": agreement_type,
                "country_programme": self.country_programme.id,
                "partner": self.partner.id,
            }
            serializer = AgreementCreateUpdateSerializer(data=data)
            serializer.context['request'] = self.fake_request

            self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create_fail_due_to_signatures_SSFA(self):
        '''Ensure signature validation works correctly for SSFA'''
        data = {
            "agreement_type": Agreement.SSFA,
            "partner": self.partner,
            "signed_by_unicef_date": self.today,
        }
        serializer = AgreementCreateUpdateSerializer()
        serializer.context['request'] = self.fake_request

        with self.assertRaises(serializers.ValidationError) as context_manager:
            serializer.validate(data=data)

        exception = context_manager.exception

        self.assertIsInstance(exception.detail, dict)
        self.assertEqual(exception.detail.keys(), ['errors'])
        self.assertIsInstance(exception.detail['errors'], list)
        msg = 'SSFA signatures are captured at the Document (TOR) level, please clear the' \
              'signatures and dates and add them to the TOR'
        self.assertEqual(exception.detail['errors'], [msg])

    def test_create_ok_and_fail_due_to_signatures_non_SSFA(self):
        '''Ensure signature validation works correctly for non-SSFA types'''
        signatory = UserFactory()
        partner_signatory = PartnerStaffFactory(partner=self.partner)

        # This should succeed; it's OK to have only one set of signatures (UNICEF)
        data = {
            "agreement_type": Agreement.MOU,
            "partner": self.partner.id,
            "signed_by_unicef_date": self.today,
            "signed_by": signatory.id,
        }
        serializer = AgreementCreateUpdateSerializer(data=data)
        serializer.context['request'] = self.fake_request

        self.assertTrue(serializer.is_valid(raise_exception=True))

        # This should succeed; it's OK to have only one set of signatures (partner)
        data = {
            "agreement_type": Agreement.MOU,
            "partner": self.partner.id,
            "signed_by_partner_date": self.today,
            "partner_manager": partner_signatory.id,
        }
        serializer = AgreementCreateUpdateSerializer(data=data)
        serializer.context['request'] = self.fake_request

        self.assertTrue(serializer.is_valid(raise_exception=True))

        # This should succeed; it's OK to have both sets of signatures (UNICEF & partner)
        data = {
            "agreement_type": Agreement.MOU,
            "partner": self.partner.id,
            "signed_by_unicef_date": self.today,
            "signed_by": signatory.id,
            "signed_by_partner_date": self.today,
            "partner_manager": partner_signatory.id,
        }
        serializer = AgreementCreateUpdateSerializer(data=data)
        serializer.context['request'] = self.fake_request

        self.assertTrue(serializer.is_valid(raise_exception=True))

        # This should fail because signed_by_unicef_date is set but not signed_by
        data = {
            "agreement_type": Agreement.MOU,
            "partner": self.partner,
            "signed_by_unicef_date": self.today,
        }
        serializer = AgreementCreateUpdateSerializer()
        serializer.context['request'] = self.fake_request

        with self.assertRaises(serializers.ValidationError) as context_manager:
            serializer.validate(data=data)

        exception = context_manager.exception

        self.assertIsInstance(exception.detail, dict)
        self.assertEqual(exception.detail.keys(), ['errors'])
        self.assertIsInstance(exception.detail['errors'], list)
        msg = 'Agreement needs to be signed by UNICEF and Partner; None of the dates can be in the future; ' \
              'If dates are set, signatories are required'
        self.assertEqual(exception.detail['errors'], [msg])

        # This should fail because signed_by_unicef_date and signed_by are both set, but the signed by date is
        # in the future.
        data = {
            "agreement_type": Agreement.MOU,
            "partner": self.partner,
            "signed_by_unicef_date": self.today + datetime.timedelta(days=5),
            "signed_by": signatory,
        }

        with self.assertRaises(serializers.ValidationError) as context_manager:
            serializer.validate(data=data)

        exception = context_manager.exception

        self.assertIsInstance(exception.detail, dict)
        self.assertEqual(exception.detail.keys(), ['errors'])
        self.assertIsInstance(exception.detail['errors'], list)
        msg = 'Agreement needs to be signed by UNICEF and Partner; None of the dates can be in the future; ' \
              'If dates are set, signatories are required'
        self.assertEqual(exception.detail['errors'], [msg])

        # This should fail because signed_by_partner_date is set but not partner_manager
        data = {
            "agreement_type": Agreement.MOU,
            "partner": self.partner,
            "signed_by_partner_date": self.today,
        }
        with self.assertRaises(serializers.ValidationError) as context_manager:
            serializer.validate(data=data)

        exception = context_manager.exception

        self.assertIsInstance(exception.detail, dict)
        self.assertEqual(exception.detail.keys(), ['errors'])
        self.assertIsInstance(exception.detail['errors'], list)
        msg = 'Agreement needs to be signed by UNICEF and Partner; None of the dates can be in the future; ' \
              'If dates are set, signatories are required'
        self.assertEqual(exception.detail['errors'], [msg])

        # This should fail because signed_by_partner_date and partner_manager are both set, but the signed by date is
        # in the future.
        data = {
            "agreement_type": Agreement.MOU,
            "partner": self.partner,
            "signed_by_partner_date": self.today + datetime.timedelta(days=5),
            "partner_manager": partner_signatory,
        }

        with self.assertRaises(serializers.ValidationError) as context_manager:
            serializer.validate(data=data)

        exception = context_manager.exception

        self.assertIsInstance(exception.detail, dict)
        self.assertEqual(exception.detail.keys(), ['errors'])
        self.assertIsInstance(exception.detail['errors'], list)
        msg = 'Agreement needs to be signed by UNICEF and Partner; None of the dates can be in the future; ' \
              'If dates are set, signatories are required'
        self.assertEqual(exception.detail['errors'], [msg])

