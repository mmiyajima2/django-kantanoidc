# -*- coding: utf8 -*-
from kantanoidc.errors import IdTokenVerificationError


class KaocExtender:

    def prepare(self, request):
        ...

    def acr_values(self):
        return 'ext'

    def verify_id_token(self, id_token):
        if 'acr' in id_token and id_token['acr'] == 'ext':
            return
        raise IdTokenVerificationError('invalid acr')

    def build_nexturl(self, request):
        return 'https://ext'
