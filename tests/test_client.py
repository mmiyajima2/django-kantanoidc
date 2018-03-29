# -*- coding: utf8 -*-
from django.test import TestCase
from logging import getLogger
from kantanoidc.client import KaocClient


logger = getLogger(__name__)


class KaocClientTests(TestCase):

    def setUp(self):
        ...

    def test_initclient(self):

        redirect_uri = 'https://watashi.me.local/callback'
        client = KaocClient(redirect_uri)
        self.assertEquals(redirect_uri, client.redirect_uri)
