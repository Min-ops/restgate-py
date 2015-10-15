#!/usr/bin/env python
# Copyright 2015 CloudNative, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""distutils/setuptools install script.
"""
import os
import re
import sys

from setuptools import setup, find_packages


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


requires = [
    'requests',
]


def get_version():
    init = open(os.path.join(ROOT, 'restgate', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='restgate',
    version=get_version(),
    description=(
        'Python library for communicating with a RESTful API hosted on AWS API'
        'Gateway'),
    long_description=open('README.rst').read(),
    author='Peter Sankauskas',
    author_email='info@cloudnative.io',
    url='https://github.com/cloudnative/restgate-py',
    packages=find_packages(exclude=['tests*']),
    install_requires=requires,
    license=open("LICENSE").read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
        'Programming Language :: Python :: 3.5'
    ),
    zip_safe=False,
)
