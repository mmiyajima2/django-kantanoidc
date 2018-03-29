from logging import getLogger
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from .client import KaocClient
import string
import random


logger = getLogger(__name__)


redirect_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')


class Start(View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        chars = string.ascii_letters + string.digits
        stored_nonce = ''.join([random.choice(chars) for i in range(6)])
        request.session['stored_nonce'] = stored_nonce
        client = KaocClient(
                request.build_absolute_uri(reverse('kantanoidc:callback')))
        return HttpResponseRedirect(client.build_starturl(stored_nonce))


class Callback(View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        stored_nonce = request.session['stored_nonce']
        code = request.GET.get('code')
        client = KaocClient(
                request.build_absolute_uri(reverse('kantanoidc:callback')))
        sub = client.get_sub(code, stored_nonce)
        logger.debug('sub=%s', sub)
        user = User.objects.get_by_natural_key(sub)
        login(request, user)
        return HttpResponseRedirect(redirect_url)
