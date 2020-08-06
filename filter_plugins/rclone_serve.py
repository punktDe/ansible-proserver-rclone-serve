#!/usr/bin/env python3

import unittest
from typing import List, Dict


class RcloneServe:
    @staticmethod
    def flatten_htpasswd(htpasswds: Dict) -> List:
        htpasswds_users = []
        for htpasswd, users in htpasswds.items():
            if 'daemon_user' in users and users['daemon_user']:
                daemon_user = users['daemon_user']
            else:
                daemon_user = None

            if not 'users' in users or not users['users']:
                continue
            users = users['users']

            for username, password in users.items():
                crypt_scheme = 'apr_md5_crypt'

                if not isinstance(password, str):
                    options = password
                    password = options['password']
                    if 'crypt_scheme' in options:
                        crypt_scheme = options['crypt_scheme']

                htpasswds_users.append({
                    'htpasswd': htpasswd,
                    'username': username,
                    'password': password,
                    'crypt_scheme': crypt_scheme,
                    'daemon_user': daemon_user,
                })
        return htpasswds_users


class RcloneServeTest(unittest.TestCase):
    def test_flatten_htpasswd(self):
        self.assertEqual(
            RcloneServe.flatten_htpasswd({
                "file1": {
                    "users": {
                        "user1": "password1",
                        "user2": {
                            "password": "password2",
                            "crypt_scheme": "plaintext"
                        },
                    },
                },
                "file2": {
                    "users": {
                        "user2": "password2",
                        "user3": {
                            "password": "password3"
                        },
                    },
                },
            }),
            [{'htpasswd': 'file1', 'username': 'user1', 'password': 'password1', 'crypt_scheme': 'apr_md5_crypt', 'daemon_user': None},
             {'htpasswd': 'file1', 'username': 'user2', 'password': 'password2', 'crypt_scheme': 'plaintext', 'daemon_user': None},
             {'htpasswd': 'file2', 'username': 'user2', 'password': 'password2', 'crypt_scheme': 'apr_md5_crypt', 'daemon_user': None},
             {'htpasswd': 'file2', 'username': 'user3', 'password': 'password3', 'crypt_scheme': 'apr_md5_crypt', 'daemon_user': None}]
        )


class FilterModule(object):
    def filters(self):
        return {
            'rclone_serve_flatten_htpasswd': RcloneServe.flatten_htpasswd,
        }


if __name__ == '__main__':
    unittest.main()
