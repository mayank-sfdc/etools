import datetime

import factory
from factory import fuzzy

from etools.applications.action_points.tests.factories import BaseActionPointFactory
from etools.applications.partners.tests.factories import PartnerFactory
from etools.applications.travel import models
from etools.applications.users.tests.factories import UserFactory


class ItineraryFactory(factory.django.DjangoModelFactory):
    supervisor = factory.SubFactory(UserFactory)
    traveller = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Trip


class ItineraryItemFactory(factory.django.DjangoModelFactory):
    itinerary = factory.SubFactory(ItineraryFactory)

    class Meta:
        model = models.ItineraryItem


class ItineraryStatusHistoryFactory(factory.django.DjangoModelFactory):
    itinerary = factory.SubFactory(ItineraryFactory)
    status = fuzzy.FuzzyChoice(
        [x[0] for x in models.Trip.STATUS_CHOICES],
    )

    class Meta:
        model = models.TripStatusHistory


class ActivityFactory(factory.django.DjangoModelFactory):
    itinerary = factory.SubFactory(ItineraryFactory)
    activity_date = fuzzy.FuzzyDate(datetime.date.today())

    class Meta:
        model = models.Activity


class InvolvedFactory(factory.django.DjangoModelFactory):
    itinerary = factory.SubFactory(ItineraryFactory)
    involved_type = fuzzy.FuzzyChoice(
        [x[0] for x in models.Involved.TYPE_CHOICES],
    )
    related_object = factory.SubFactory(PartnerFactory)

    class Meta:
        model = models.Involved


class ActivityActionPointFactory(BaseActionPointFactory):
    activity = factory.SubFactory(ActivityFactory)

    class Meta:
        model = models.ActivityActionPoint


class ReportFactory(factory.django.DjangoModelFactory):
    itinerary = factory.SubFactory(ItineraryFactory)

    class Meta:
        model = models.Report
