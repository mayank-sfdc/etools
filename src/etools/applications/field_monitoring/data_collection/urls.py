from django.conf.urls import include, url

from rest_framework_nested import routers

from unicef_restlib.routers import NestedComplexRouter

from etools.applications.field_monitoring.data_collection.views import VisitsDataCollectionViewSet, \
    StartedMethodViewSet, TaskDataViewSet, VisitTasksDataCollectionViewSet, TasksOverallCheckListViewSet, \
    TasksOverallCheckListAttachmentsViewSet, StartedMethodCheckListViewSet, CheckListValueViewSet, \
    CheckListValueAttachmentsViewSet

root_api = routers.SimpleRouter()
root_api.register(r'visits', VisitsDataCollectionViewSet, base_name='visits')

visits_api = NestedComplexRouter(root_api, r'visits', lookup='visit')
visits_api.register(r'started-methods', StartedMethodViewSet, base_name='started-methods')
visits_api.register(r'tasks', VisitTasksDataCollectionViewSet, base_name='visit-tasks')

tasks_api = NestedComplexRouter(visits_api, r'tasks', lookup='visit_task')
tasks_api.register(r'checklist', TasksOverallCheckListViewSet, base_name='visit-tasks-overall-checklist')

task_checklist_api = NestedComplexRouter(tasks_api, r'checklist')
task_checklist_api.register('attachments', TasksOverallCheckListAttachmentsViewSet,
                            base_name='visit-tasks-overall-checklist-attachments')

started_methods_api = NestedComplexRouter(visits_api, r'started-methods', lookup='started_method')
started_methods_api.register(r'checklist', StartedMethodCheckListViewSet, base_name='started-method-checklist')
started_methods_api.register(r'tasks-data', TaskDataViewSet, base_name='task-data')

checklist_api = NestedComplexRouter(started_methods_api, r'checklist', lookup='checklist_item')
checklist_api.register(r'values', CheckListValueViewSet, base_name='checklist-values')

checklist_values_api = NestedComplexRouter(checklist_api, r'values')
checklist_values_api.register(r'attachments', CheckListValueAttachmentsViewSet, base_name='checklist-value-attachments')

app_name = 'field_monitoring_data_collection'
urlpatterns = [
    url(r'^', include(checklist_values_api.urls)),
    url(r'^', include(checklist_api.urls)),
    url(r'^', include(started_methods_api.urls)),
    url(r'^', include(tasks_api.urls)),
    url(r'^', include(visits_api.urls)),
    url(r'^', include(root_api.urls)),
]