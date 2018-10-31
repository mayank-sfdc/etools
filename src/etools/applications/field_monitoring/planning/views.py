from datetime import date

from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from unicef_restlib.views import NestedViewSetMixin

from etools.applications.field_monitoring.planning.models import YearPlan, Task
from etools.applications.field_monitoring.planning.serializers import YearPlanSerializer, YearPlanAttachmentSerializer, \
    TaskSerializer, TaskListSerializer
from etools.applications.field_monitoring.settings.filters import CPOutputIsActiveFilter
from etools.applications.field_monitoring.views import FMBaseViewSet, FMBaseAttachmentsViewSet


class YearPlanViewSet(
    FMBaseViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = YearPlan.objects.all()
    serializer_class = YearPlanSerializer

    def get_view_name(self):
        return _('Annual Field Monitoring Rationale')

    def get_years_allowed(self):
        return map(str, [date.today().year, date.today().year + 1])

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(year__in=self.get_years_allowed())

    def get_object(self):
        """ get or create object for specified year. only current & next are allowed"""

        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if self.kwargs[lookup_url_kwarg] not in self.get_years_allowed():
            raise Http404

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = queryset.get_or_create(**filter_kwargs)[0]

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class YearPlanAttachmentsViewSet(FMBaseAttachmentsViewSet):
    serializer_class = YearPlanAttachmentSerializer
    related_model = YearPlan

    def get_view_name(self):
        return _('Attachments')


class TaskViewSet(NestedViewSetMixin, FMBaseViewSet, viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related(
        'cp_output_config', 'cp_output_config__cp_output',
        'partner', 'intervention', 'location', 'location_site',
    )
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend, CPOutputIsActiveFilter, OrderingFilter)
    filter_fields = ('cp_output_config', 'partner', 'intervention', 'location', 'location_site')
    ordering_fields = (
        'cp_output_config__cp_output__name',
        'partner__name', 'intervention__title',
        'location__name', 'location_site__name',
    )
    serializer_action_classes = {
        'list': TaskListSerializer
    }

    def get_view_name(self):
        return _('Plan By Task')

    def perform_create(self, serializer, **kwargs):
        serializer.save(year_plan=self.get_parent_object(), **kwargs)
