# -*- coding: utf8 -*-
from django.test import TestCase
from unittest.mock import patch
from logging import getLogger
from kantanoidc.client import KaocClient
from tests.mocks import get_asmock, post_asmock


logger = getLogger(__name__)


class KaocClientTests(TestCase):

    def setUp(self):
        ...

    def test_init(self):

        redirect_uri = 'https://watashi.me.local/callback'
        client = KaocClient(redirect_uri)
        self.assertEquals(redirect_uri, client.redirect_uri)
        self.assertEquals('id', client.client_id)
        self.assertEquals('secret', client.client_secret)

        self.assertIsNotNone(client.authorization_endpoint)
        logger.debug(client.authorization_endpoint)
        self.assertIsNotNone(client.token_endpoint)
        logger.debug(client.token_endpoint)
        self.assertIsNotNone(client.userinfo_endpoint)
        logger.debug(client.userinfo_endpoint)

    def test_build_starturl(self):

        redirect_uri = 'https://test'
        client = KaocClient(redirect_uri)
        nonce = 'hogehoge'
        result = client.build_starturl(nonce)
        logger.debug(result)

    @patch('kantanoidc.client.requests.post', new=post_asmock)
    @patch('kantanoidc.client.requests.get', new=get_asmock)
    def test_get_sub(self):

        redirect_uri = 'https://test'
        client = KaocClient(redirect_uri)
        sub = client.get_sub('codevalue', 'noncevalue')
        self.assertEquals("me", sub)
