#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os.path
import json
import pprint

import requests

class Conveyor(object):
    DEFAULT_ENDPOINT_PREFIX     = 'https://api.quarri.us'
    WORLD_OBJ_PATH              = '/authorize-upload/world/{api_key}'
    WORLD_ARCHIVE_PATH          = '/authorize-upload/world-archive/{api_key}'

    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT_PREFIX):
        self._api_key = api_key
        self._endpoint_prefix = endpoint

    def upload_world_archive(self, filename):
        req_data = self.request_world_archive_upload()
        with open(filename, 'rb') as upload_fd:
            resp = requests.post(req_data['url'], data=req_data['fields'],
                files={'file': (req_data['fields']['key'], upload_fd)})

            print resp
            if not resp.ok:
                print resp.text
                print
                pprint.pprint(json.loads(req_data['fields']['policy'].decode('base64')))

    def request_world_obj_upload(self):
        auth_url = self._get_world_obj_auth_url()
        auth_data = requests.get(auth_url).json()
        return auth_data

    def request_world_archive_upload(self):
        auth_url = self._get_world_archive_auth_url()
        auth_data = requests.get(auth_url).json()
        return auth_data

    def _get_world_obj_auth_url(self):
        return self._endpoint_prefix + self.WORLD_OBJ_PATH.format(api_key=self._api_key)

    def _get_world_archive_auth_url(self):
        return self._endpoint_prefix + self.WORLD_ARCHIVE_PATH.format(api_key=self._api_key)


if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser()

    parser.add_option('-k', '--api-key')

    opts, args = parser.parse_args()

    c = Conveyor(opts.api_key)

    c.upload_world_archive(args[0])
