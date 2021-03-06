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

import unittest

import requests
import responses

import restgate
import restgate.exceptions
from restgate import RestGate


class TestRestGate(unittest.TestCase):

    def setUp(self):
        self.endpoint = 'http://example.com'
        self.api_key = 'TEST000apikey000'
        self.rg = RestGate(self.endpoint, self.api_key)

    def tearDown(self):
        pass

    def test___init__(self):
        self.assertEqual(self.rg.endpoint, self.endpoint)
        self.assertEqual(self.rg.api_key, self.api_key)
        self.assertEqual(self.rg.timeout, 5)

    def test__default_headers(self):
        h = self.rg._default_headers()
        self.assertEqual(len(h.keys()), 2)
        self.assertEqual(h['user-agent'], 'restgate/{}'.format(
            restgate.__version__))
        self.assertEqual(h['X-Api-Key'], self.api_key)

    @responses.activate
    def test_list(self):
        responses.add(
            responses.GET, 'http://example.com/res',
            body='[{"id": 1, "field2": "val2"},{"id": 2, "field4": "val4"}]',
            status=200)

        rlist = self.rg.list('res')
        self.assertEqual(type(rlist), list)
        self.assertEqual(len(rlist), 2)
        self.assertEqual(rlist[0]['id'], 1)
        self.assertEqual(rlist[0]['field2'], 'val2')
        self.assertEqual(rlist[1]['id'], 2)
        self.assertEqual(rlist[1]['field4'], 'val4')

    @responses.activate
    def test_get(self):
        responses.add(
            responses.GET, 'http://example.com/res/1',
            body='{"id": 1, "field2": "val2"}',
            status=200)

        res = self.rg.get('res', 1)
        self.assertEqual(type(res), dict)
        self.assertEqual(res['id'], 1)
        self.assertEqual(res['field2'], 'val2')

    @responses.activate
    def test_post(self):
        responses.add(
            responses.POST, 'http://example.com/res',
            body='{"id": 1, "field1": "val1", "field2": "val2"}',
            status=200)

        res = self.rg.post('res', {'field1': 'val1', 'field2': 'val2'})
        self.assertEqual(type(res), dict)
        self.assertEqual(res['id'], 1)
        self.assertEqual(res['field1'], 'val1')
        self.assertEqual(res['field2'], 'val2')

    @responses.activate
    def test_put(self):
        responses.add(
            responses.PUT, 'http://example.com/res/123',
            body='{"id": 123, "field1": "val1", "field2": "val3"}',
            status=200)

        res = self.rg.put('res', 123, {'field1': 'val1', 'field2': 'val3'})
        self.assertEqual(type(res), dict)
        self.assertEqual(res['id'], 123)
        self.assertEqual(res['field1'], 'val1')
        self.assertEqual(res['field2'], 'val3')

    @responses.activate
    def test_restgate_connection_error(self):
        def request_callback(request):
            raise requests.exceptions.ConnectionError

        responses.add_callback(
            responses.GET, 'http://example.com/res/1',
            callback=request_callback
        )

        with self.assertRaises(restgate.exceptions.ConnectionError) as cm:
            self.rg.get('res', 1)

    @responses.activate
    def test_restgate_http_error(self):
        responses.add(
            responses.GET, 'http://example.com/res/1',
            status=500)

        with self.assertRaises(restgate.exceptions.HTTPError) as cm:
            self.rg.get('res', 1)
