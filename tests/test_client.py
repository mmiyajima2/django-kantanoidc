# -*- coding: utf8 -*-
from django.test import TestCase
from unittest.mock import patch
from logging import getLogger
from kantanoidc.client import KaocClient
from kantanoidc.errors import IdTokenVerificationError
from tests.mocks import post_normal, get_normal
from tests.mocks import post_abn_aud
from tests.mocks import post_abn_exp


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

    @patch('kantanoidc.client.requests.post', new=post_normal)
    @patch('kantanoidc.client.requests.get', new=get_normal)
    def test_get_sub(self):

        redirect_uri = 'https://test'
        client = KaocClient(redirect_uri)
        sub = client.get_sub('codevalue', 'noncevalue')
        self.assertEquals("me", sub)

    @patch('kantanoidc.client.requests.post', new=post_abn_aud)
    @patch('kantanoidc.client.requests.get', new=get_normal)
    def test_get_sub_abn_aud(self):

        redirect_uri = 'https://test'
        client = KaocClient(redirect_uri)
        with self.assertRaises(
                IdTokenVerificationError, msg='aud <> client_id'):
            client.get_sub('codevalue', 'noncevalue')

    @patch(
        'kantanoidc.client.requests.post',
        new=post_normal
    )
    @patch('kantanoidc.client.requests.get', new=get_normal)
    def test_get_sub_abn_nonce(self):

        redirect_uri = 'https://test'
        client = KaocClient(redirect_uri)
        with self.assertRaises(
                IdTokenVerificationError, msg='nonce <> stored_nonce'):
            client.get_sub('codevalue', '1noncevalue')

    @patch(
        'kantanoidc.client.requests.post',
        new=post_abn_exp
    )
    @patch('kantanoidc.client.requests.get', new=get_normal)
    def test_get_sub_abn_exp(self):

        redirect_uri = 'https://test'
        client = KaocClient(redirect_uri)
        with self.assertRaises(
                IdTokenVerificationError, msg='now > exp'):
            client.get_sub('codevalue', 'noncevalue')
