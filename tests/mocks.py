# -*- coding: utf8 -*-
from logging import getLogger
import json
import time
import base64


logger = getLogger(__name__)


class MockTokenResponse(object):

    def json(self):
        data = {
            'exp': (time.time() + 1000000),
            'aud': 'id',
            'nonce': 'noncevalue',
        }
        astext = json.dumps(data)
        asbin = base64.b64encode(astext.encode('utf8'))
        payload = asbin.decode()
        id_token = 'header.%s' % payload
        logger.debug('id_token=%s', id_token)
        return {'access_token': 'fugafuga', 'id_token': id_token}


class MockUserinfoResponse(object):

    def json(self):
        return {'sub': 'me'}


def post_asmock(url, data=None):
    logger.debug('post_asmock')
    logger.debug('url=%s', url)
    return MockTokenResponse()


def get_asmock(url, params=None):
    logger.debug('get_asmock')
    logger.debug('url=%s', url)
    return MockUserinfoResponse()
