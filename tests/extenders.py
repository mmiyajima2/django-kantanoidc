# -*- coding: utf8 -*-
from kantanoidc.errors import IdTokenVerificationError


class KaocExtender:

    def prepare(self, request):
        ...

    def acr_values(self):
        return 'ext'

    def verify_acr(self, values):
        if values == 'ext':
            return
        raise IdTokenVerificationError('invalid acr')

    def build_nexturl(self, request):
        return 'https://ext'
