from django.conf.urls import include, url

from rest_framework_nested import routers

from etools.applications.field_monitoring.planning import views

root_api = routers.SimpleRouter()
root_api.register(r'year-plan', views.YearPlanViewSet, base_name='year-plan')
root_api.register(r'questions/templates', views.QuestionTemplateViewSet, base_name='question-templates')
root_api.register(r'activities', views.MonitoringActivitiesViewSet, base_name='activities')

app_name = 'field_monitoring_planning'
urlpatterns = [
    url(r'^', include(root_api.urls)),
]
