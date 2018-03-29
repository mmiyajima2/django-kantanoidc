# -*- coding: utf8 -*-
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('kantanoidc/', include('kantanoidc.urls')),
]
