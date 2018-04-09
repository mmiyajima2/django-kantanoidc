# -*- coding: utf8 -*-
from logging import getLogger
import json
import time
import base64


logger = getLogger(__name__)


class MockTokenResponse(object):

    def __init__(self, exp, aud, nonce, b64pad=True):
        self.exp = exp
        self.aud = aud
        self.nonce = nonce
        self.b64pad = b64pad

    def json(self):
        data = {
            'exp': self.exp,
            'aud': self.aud,
            'nonce': self.nonce,
        }
        astext = json.dumps(data)
        asbin = base64.b64encode(astext.encode('utf8'))
        payload = asbin.decode()
        logger.debug("b payload=%s", payload)
        if not self.b64pad:
            payload = payload.replace("=", "")
        logger.debug("a payload=%s", payload)
        id_token = 'header.%s' % payload
        logger.debug('id_token=%s', id_token)
        return {'access_token': 'fugafuga', 'id_token': id_token}


class MockUserinfoResponse(object):

    def json(self):
        return {'sub': 'me'}


def post_normal(url, data=None):
    logger.debug('url=%s', url)
    return MockTokenResponse(
        (time.time() + 10000), 'id', 'noncevalue'
    )


def post_abn_nonce(url, data=None):
    logger.debug('url=%s', url)
    return MockTokenResponse(
        (time.time() + 10000),
        'id',
        'xxxxxxxxxxxxxxxxxxxxxxxx',
        False,
    )


def post_abn_aud(url, data=None):
    logger.debug('url=%s', url)
    return MockTokenResponse(
        (time.time() + 10000), 'abnid', 'noncevalue'
    )


def post_abn_exp(url, data=None):
    logger.debug('url=%s', url)
    return MockTokenResponse(
        (time.time() - 100), 'id', 'noncevalue'
    )


def get_normal(url, params=None):
    logger.debug('url=%s', url)
    return MockUserinfoResponse()
