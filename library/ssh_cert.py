#! /usr/bin/env python

from datetime import datetime
import string
import subprocess

from ansible.module_utils.basic import *

__doc__ = '''
module: ssh_cert
author: Edoardo Putti
short_description: Check ssh certificate validity
'''

CERT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def serial(lines):
    for l in lines:
        if l.startswith('Serial'):
            return int(l.split().pop(), 10)


def signin_ca(lines):
    for l in lines:
        if l.startswith('Signing CA'):
            return l.split().pop()


def still_valid(cert_timestamps):
    t = datetime.datetime.today()
    return t < cert_timestamps['valid']['to'] and t > cert_timestamps['valid']['from']


def cert_type(lines):
    for l in lines:
        if l.startswith('Type'):
            return string.split(l, maxsplit=2)[1:]


def valid_from(lines):
    for l in lines:
        if l.startswith('Valid'):
            return datetime.datetime.strptime(l.split()[2], CERT_TIME_FORMAT)


def valid_to(lines):
    for l in lines:
        if l.startswith('Valid'):
            return datetime.datetime.strptime(l.split()[4], CERT_TIME_FORMAT)


def main():
    module = AnsibleModule(
                argument_spec=dict(),
                supports_check_mode=False,
            )
    result = {}
    result['ca'] = {}
    result['ca']['path'] = '/etc/ssh/user_ca.pub'
    result['certificate'] = {}
    result['certificate']['path'] = '/etc/ssh/ssh_host_ed25519_key-cert.pub'

    ca_output = subprocess.check_output([
            'ssh-keygen',
            '-l',
            '-f', result['ca']['path'],
        ])

    ca_lines = string.split(ca_output, maxsplit=2)
    result['ca']['fingerprint'] = ca_lines[1]
    result['ca']['comment'] = ca_lines[2]

    cert_output = subprocess.check_output([
                                           'ssh-keygen',
                                           '-L',
                                           '-f', result['certificate']['path'],
                                          ])
    cert_lines = [line.strip() for line in cert_output.split('\n')]

    result['certificate']['signin_ca'] = signin_ca(cert_lines)
    result['certificate']['valid'] = {
                'from': valid_from(cert_lines),
                'to': valid_to(cert_lines),
            }

    if not still_valid(result['certificate']):
        result['failed'] = True
        result['msg'] = 'The certificate is not valid now'

    result['certificate']['serial'] = serial(cert_lines)
    result['certificate']['type'] = cert_type(cert_lines)


    if not result['certificate']['signin_ca'] == result['ca']['fingerprint']:
        result['failed'] = True
        result['msg'] = 'The provided CA did not sign the certificate specified'

    module.exit_json(**result)


if __name__ == '__main__':
    main()
