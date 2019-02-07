import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as rme:
    README = rme.read()


setup(
    name='django-kantanoidc',
    version='0.5.0',
    packages=['kantanoidc'],
    license='MIT',
    description='Helper app as oidc client',
    long_description=README,
    url='https://github.com/mmiyajima2/django-kantanoidc',
    author='Masafumi Miyajima',
    author_email='mmiyajima2@gmail.com',
    install_requires=[
        'django',
        'requests',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 2.1',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
