from django.urls import include, path

from rest_framework_nested import routers
from unicef_restlib.routers import NestedComplexRouter

from etools.applications.psea import views

root_api = routers.SimpleRouter()

root_api.register(
    r'assessment',
    views.AssessmentViewSet,
    basename='assessment',
)
root_api.register(r'assessor', views.AssessorViewSet, basename='assessor')
root_api.register(r'indicator', views.IndicatorViewSet, basename='indicator')

answer_api = NestedComplexRouter(root_api, r'assessment')
answer_api.register(r'answer', views.AnswerViewSet, base_name='answer')

attachments_api = NestedComplexRouter(answer_api, r'answer')
attachments_api.register(
    r'attachments',
    views.AnswerAttachmentsViewSet,
    base_name='answer-attachments',
)

app_name = 'psea'
urlpatterns = [
    path('', include(root_api.urls)),
    path('', include(answer_api.urls)),
    path('', include(attachments_api.urls)),
]