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
META_FILE = open(os.path.join(ROOT, 'restgate', '__init__.py')).read()


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


requires = [
    'requests',
]


setup(
    name='restgate',
    version=find_meta('version'),
    description=find_meta("description"),
    long_description=open('README.rst').read(),
    author=find_meta('author'),
    author_email=find_meta('email'),
    url=find_meta('url'),
    maintainer=find_meta("author"),
    maintainer_email=find_meta("email"),
    packages=find_packages(exclude=['tests*']),
    install_requires=requires,
    license='Apache License, Version 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ),
    zip_safe=False,
)
