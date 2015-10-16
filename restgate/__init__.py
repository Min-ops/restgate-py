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
"""Python library for communicating with a RESTful API hosted on AWS API
Gateway
"""

import json
import logging

import requests

__author__ = 'Peter Sankauskas'
__email__ = 'info@cloudnative.io'
__description__ = 'Library for using a RESTful API hosted on AWS API Gateway'
__url__ = 'https://github.com/cloudnative/restgate-py'
__version__ = '0.1.0'

LOG = logging.getLogger(__name__)


class RestGate:
    """Library for interacting with a RESTful AWS Gateway API.
    """

    def __init__(self, endpoint, api_key):
        """Creates a new REST client to an API

        Args:
            endpoint (str): The HTTP URL to the API
            api_key (str): The AWS API Gateway API Key

        Attributes:
            endpoint (str): The HTTP URL to the API
            api_key (str): The AWS API Gateway API Key
            timeout (int): The time to wait (in seconds) for the request to
                receive data back
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.timeout = 5  # seconds

    def list(self, resource, **kwargs):
        """Returns a list of a particular resource

        Args:
            resource (str): The name of the resource to get a list of
        """
        url = '{}/{}'.format(self.endpoint, resource)
        resp = self._send_request('get', url, **kwargs)
        return resp.json()

    def get(self, resource, resource_id, **kwargs):
        """Returns details about a specific resource

        Args:
            resource (str): The name of the resource to details for
            id (str): The ID of the resource
        """
        url = '{}/{}/{}'.format(self.endpoint, resource, resource_id)
        resp = self._send_request('get', url, **kwargs)
        return resp.json()

    def _default_headers(self):
        """Returns the default set of HTTP headers sent with every request
        """
        headers = {
            'user-agent': 'restgate/{}'.format(__version__),
            'X-Api-Key': self.api_key
        }
        return headers

    def _send_request(self, method, url, **kwargs):
        """All requests to the API go through here. This is where the default
        headers are applied and errors are handled

        Note:
            This does not do retried yet. It should
        """

        headers = kwargs.get('headers', {})
        for k, v in self._default_headers().items():
            headers.setdefault(k, v)
        kwargs['headers'] = headers

        try:
            resp = requests.request(method, url, **kwargs)
        except requests.exceptions.ConnectionError as e:
            LOG.warning('Could not connect to {}. Error: {}'.format(url, e))
            return self._error(e)
        except requests.exceptions.HTTPError as e:
            LOG.warning(
                'Invalid HTTP response received from {}. Error: {}'.format(
                    url, e))
            return self._error(e)
        except requests.exceptions.Timeout as e:
            LOG.warning('Timed out connecting to {}. Error: {}'.format(url, e))
            return self._error(e)
        except requests.exceptions.TooManyRedirects as e:
            LOG.warning('Too many redirects for {}. Error: {}'.format(url, e))
            return self._error(e)

        if resp.status_code != requests.codes.ok:
            LOG.warning('Bad response received from {}: Status: {}'.format(
                url, resp.status_code))
            resp.raise_for_status()

        return resp

    def _error(self, exception):
        # TODO Something a little more graceful
        raise exception
