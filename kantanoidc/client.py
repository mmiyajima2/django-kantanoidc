# -*- condig: utf8 -*-
from logging import getLogger
from django.conf import settings
from django.utils import module_loading
from urllib import parse
import requests
import base64
import json
import time
from .errors import IdTokenVerificationError


__all__ = ['client']
logger = getLogger(__name__)


AUTH_SERVER = settings.KAOC_SERVER
CLIENT_ID = settings.KAOC_CLIENT_ID
CLIENT_SECRET = settings.KAOC_CLIENT_SECRET
CONFIG_PATH = '/.well-known/openid-configuration'
client = None


class KaocClient(object):

    def __init__(self, aep, tep, uep):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.authorization_endpoint = aep
        self.token_endpoint = tep
        self.userinfo_endpoint = uep
        if hasattr(settings, 'KAOC_EXPANDER'):
            Expander = module_loading.import_string(settings.KAOC_EXPANDER)
            self.expander = Expander()
        else:
            self.expander = None

    def prepare(self, request, context_id):
        if self.expander is None:
            return
        self.expander.prepare(request, context_id)

    def build_starturl(self, stored_nonce, stored_state):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'openid email',
            'nonce': stored_nonce,
            'state': stored_state,
        }
        if self.expander and hasattr(self.expander, 'acr_values'):
            params.update['acr_values'] = self.expander.acr_values()
        return (
            '%s?%s' % (self.authorization_endpoint, parse.urlencode(params))
        )

    def build_nexturl(self, request, context_id):
        if self.expander is None:
            return settings.LOGIN_REDIRECT_URL
        else:
            return self.build_nexturl(request, context_id)

    def get_sub(self, code, stored_nonce):
        token = self.__get_token(code, stored_nonce)
        userinfo = self.__get_userinfo(token)
        return userinfo['sub']

    def __get_token(self, code, stored_nonce):
        r = requests.post(
            url=self.token_endpoint,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri,
            }
        )
        asobject = r.json()
        id_token = asobject['id_token']
        self.__verify_id_token(id_token, stored_nonce)
        return asobject['access_token']

    def __get_userinfo(self, token):
        r = requests.get(
            url=self.userinfo_endpoint,
            params={'access_token': token}
        )
        return r.json()

    def __verify_id_token(self, id_token, stored_nonce):
        payload = id_token.split('.')[1]
        surplus = len(payload) % 4
        if surplus > 0:
            payload += ('=' * (4 - surplus))
        asobject = json.loads(base64.b64decode(payload.encode()))
        logger.debug('%s', asobject)
        if (self.client_id != asobject['aud']):
            raise IdTokenVerificationError('aud <> client_id')
        if (stored_nonce != asobject['nonce']):
            raise IdTokenVerificationError('nonce <> stored_nonce')
        if (time.time() > asobject['exp']):
            raise IdTokenVerificationError('now > exp')
        if self.expander and hasattr(self.expander, 'verify_acr'):
            self.expander.verify_acr()


def initmod():
    global client
    r = requests.get(
        url=(AUTH_SERVER + CONFIG_PATH),
    )
    asobject = r.json()
    client = KaocClient(
        asobject['authorization_endpoint'],
        asobject['token_endpoint'],
        asobject['userinfo_endpoint']
    )


initmod()
