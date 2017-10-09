from django.conf.urls import url

from .views import (
    MyProfileAPIView,
    CountryView,
    CountriesViewSet,
)


urlpatterns = (
    # list all of the countries
    url(r'^workspaces/$', CountriesViewSet.as_view(http_method_names=['get']), name="list-workspaces"),

    url(r'^myprofile/$', MyProfileAPIView.as_view(), name="myprofile-detail"),
    url(r'^country/$', CountryView.as_view(http_method_names=['get']), name="country-detail"),
)
