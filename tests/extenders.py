# -*- coding: utf8 -*-
from django.conf import settings


class KaocExtender:

    def prepare(self, request, context_id):
        self.context_id = context_id
        self.request = request

    def acr_values(self):
        ...

    def verify_acr(self, values):
        ...

    def build_nexturl(self, request, context_id):
        return settings.LOGIN_REDIRECT_URL
