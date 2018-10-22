# -*- coding: utf8 -*-
from django.conf import settings


class NexturlBuilder:

    def prepare(self, request, context_id):
        ...

    def build(self, request, context_id):
        return settings.LOGIN_REDIRECT_URL
