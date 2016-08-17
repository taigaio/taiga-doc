#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='generate-api-documents',
    version="0.0.1",
    description="Helper app to generate requests and responses from taiga API",
    long_description="",
    keywords='taiga, documentation, api',
    author='Jesús Espino García',
    author_email='jesus.espino@kaleidos.net',
    url='https://github.com/taigaio/taiga-doc',
    license='AGPL',
    packages=[
        "generate_api_documents"
    ],
    package_data={
        "generate_api_documents": [
            "management/commands/*.json",
            "management/commands/*.py",
            "management/commands/*.png",
        ]
    },
    install_requires=[
        'django >= 1.7',
    ],
    classifiers=[
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
