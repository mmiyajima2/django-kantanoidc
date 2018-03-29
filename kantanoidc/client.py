# -*- condig: utf8 -*-
from logging import getLogger
from django.conf import settings
from urllib import parse
import requests
import base64
import json
import time
from .errors import IdTokenVerificationError


logger = getLogger(__name__)


AUTH_SERVER = settings.KAOC_SERVER
CLIENT_ID = settings.KAOC_CLIENT_ID
CLIENT_SECRET = settings.KAOC_CLIENT_SECRET
CONFIG_PATH = '/.well-known/openid-configuration'
AEP = None
TEP = None
UEP = None


class KaocClient(object):

    def __init__(self, redirect_uri):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_uri = redirect_uri
        self.authorization_endpoint = AEP
        self.token_endpoint = TEP
        self.userinfo_endpoint = UEP

    def build_starturl(self, stored_nonce):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'openid email',
            'nonce': stored_nonce,
        }
        return (
            '%s?%s' % (self.authorization_endpoint, parse.urlencode(params))
        )

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
        asobject = json.loads(base64.b64decode(payload.encode()))
        logger.debug(str(asobject))
        if (self.client_id != asobject['aud']):
            raise IdTokenVerificationError('aud <> client_id')
        if (stored_nonce != asobject['nonce']):
            raise IdTokenVerificationError('nonce <> stored_nonce')
        if (time.time() > asobject['exp']):
            raise IdTokenVerificationError('now > exp')


def initmod():
    global AEP
    global TEP
    global UEP
    r = requests.get(
        url=(AUTH_SERVER + CONFIG_PATH),
    )
    asobject = r.json()
    AEP = asobject['authorization_endpoint']
    TEP = asobject['token_endpoint']
    UEP = asobject['userinfo_endpoint']


initmod()
