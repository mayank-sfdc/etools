from django.contrib import admin

from etools.applications.travel.models import Activity, Trip, Report


class ActivityInline(admin.TabularInline):
    model = Activity


class ReportInline(admin.TabularInline):
    model = Report


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        'reference_number',
        'status',
        'traveller',
        'start_date',
        'end_date',
    )
    list_filter = ('reference_number', 'status',)
    search_fields = ('reference_number', 'traveller__email',)
    inlines = [
        ActivityInline,
        ReportInline,
    ]