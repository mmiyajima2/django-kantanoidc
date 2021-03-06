
=====================
KANTAN oidc (KAOC) 
=====================
.. image:: https://travis-ci.org/mmiyajima2/django-kantanoidc.svg?branch=master
    :target: https://travis-ci.org/mmiyajima2/django-kantanoidc
.. image:: https://coveralls.io/repos/github/mmiyajima2/django-kantanoidc/badge.svg?branch=master
    :target: https://coveralls.io/github/mmiyajima2/django-kantanoidc?branch=master

KAOC behaves like OpenID Connect client as Django helper application.
KANTAN means "naive" or, "very simple".

Installation
=====================

.. code-block:: bash

   shell>pip install djangokantanoidc


Usage
=====================

Installed apps:

.. code-block:: python

   INSTALLED_APPS = (
       ...
       'kantanoidc.apps.KantanoidcConfig',
       ...
   )
   
URLconfs for Django project:

.. code-block:: python

    urlpatterns = [
        ...
        path('kantanoidc/', include('kantanoidc.urls')),
    ]


Settings
=====================

KAOC_SERVER
---------------

Default: ``''``

OpenID Connect Authorization Server URL.

KAOC_CLIENT_ID
---------------

Default: ``''``

Client ID.

KAOC_CLIENT_SECRET
------------------

Default: ``''``

Client secret.


KAOC_EXTENDER (Optional)
-------------------------

Default: ``None``

Extend a basic authentication flow.
