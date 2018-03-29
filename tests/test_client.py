# -*- coding: utf8 -*-
from django.test import TestCase
from logging import getLogger
from kantanoidc.client import KaocClient


logger = getLogger(__name__)


class KaocClientTests(TestCase):

    def setUp(self):
        ...

    def test_init(self):

        redirect_uri = 'https://watashi.me.local/callback'
        client = KaocClient(redirect_uri)
        self.assertEquals(redirect_uri, client.redirect_uri)
        self.assertIsNotNone(client.authorization_endpoint)
        logger.debug(client.authorization_endpoint)
        self.assertIsNotNone(client.token_endpoint)
        logger.debug(client.token_endpoint)
        self.assertIsNotNone(client.userinfo_endpoint)
        logger.debug(client.userinfo_endpoint)
