#!/usr/bin/env python3
import hashlib
import base64


class RcloneServeHtpasswd():
    @staticmethod
    def entry(username_password):
        hash = hashlib.new('sha1')
        hash.update(username_password[1].encode('utf-8'))
        return '{}:{{{}}}{}'.format(username_password[0], 'SHA', base64.standard_b64encode(hash.digest()).decode())


class FilterModule(object):
    def filters(self):
        return {
            'rclone_serve_htpasswd': RcloneServeHtpasswd.entry,
        }
