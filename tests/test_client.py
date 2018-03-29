# -*- coding: utf8 -*-
from django.test import TestCase
from logging import getLogger
from kantanoidc.client import KaocClient


logger = getLogger(__name__)


class KaocClientTests(TestCase):

    def setUp(self):
        logger.debug('KaocClientTests setup')
