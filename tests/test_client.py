# -*- coding: utf8 -*-
from django.test import TestCase
from unittest.mock import patch
from logging import getLogger
from kantanoidc.client import client
from kantanoidc.errors import IdTokenVerificationError
from .mocks import post_normal, get_normal
from .mocks import post_abn_aud
from .mocks import post_abn_exp
from .mocks import post_abn_nonce


logger = getLogger(__name__)


class KaocClientTests(TestCase):

    def setUp(self):
        ...

    def test_init(self):

        client.redirect_uri = 'https://watashi.me.local/callback'
        self.assertEquals('id', client.client_id)
        self.assertEquals('secret', client.client_secret)

        self.assertIsNotNone(client.authorization_endpoint)
        logger.debug(client.authorization_endpoint)
        self.assertIsNotNone(client.token_endpoint)
        logger.debug(client.token_endpoint)
        self.assertIsNotNone(client.userinfo_endpoint)
        logger.debug(client.userinfo_endpoint)

    def test_build_starturl(self):
        result = client.build_starturl('https://test', 'hogehoge', 'statevalue') # noqa
        logger.debug(result)
        self.assertTrue('acr_values=ext' in result)

    def test_build_nexturl(self):
        result = client.build_nexturl({})
        self.assertEquals('https://ext', result)

    @patch('kantanoidc.client.requests.post', new=post_normal)
    @patch('kantanoidc.client.requests.get', new=get_normal)
    def test_get_sub(self):

        client.redirect_uri = 'https://test'
        sub = client.get_sub('codevalue', 'noncevalue')
        self.assertEquals("me", sub)

    @patch('kantanoidc.client.requests.post', new=post_abn_aud)
    @patch('kantanoidc.client.requests.get', new=get_normal)
    def test_get_sub_abn_aud(self):

        client.redirect_uri = 'https://test'
        with self.assertRaises(
                IdTokenVerificationError, msg='aud <> client_id'):
            client.get_sub('codevalue', 'noncevalue')

    @patch(
        'kantanoidc.client.requests.post',
        new=post_abn_nonce
    )
    @patch('kantanoidc.client.requests.get', new=get_normal)
    def test_get_sub_abn_nonce(self):

        client.redirect_uri = 'https://test'
        with self.assertRaises(
                IdTokenVerificationError, msg='nonce <> stored_nonce'):
            client.get_sub('codevalue', 'noncevalue')

    @patch(
        'kantanoidc.client.requests.post',
        new=post_abn_exp
    )
    @patch('kantanoidc.client.requests.get', new=get_normal)
    def test_get_sub_abn_exp(self):

        client.redirect_uri = 'https://test'
        with self.assertRaises(
                IdTokenVerificationError, msg='now > exp'):
            client.get_sub('codevalue', 'noncevalue')
