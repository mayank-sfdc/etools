from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from social_core import exceptions as social_exceptions
from social_django.middleware import SocialAuthExceptionMiddleware


class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, 'AuthCanceled'):
            return HttpResponseRedirect(reverse(settings.LOGIN_URL))
        else:
            raise exception