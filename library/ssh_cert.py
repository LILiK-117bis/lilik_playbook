#! /usr/bin/env python3

from datetime import datetime
import string
import subprocess

from ansible.module_utils.basic import AnsibleModule

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
#            return l.split().pop()
#       Starting from OpenSSH v8 the output format of ssh-keygen
#       has changed, this should work for all versions:
            return l.split()[3]

def principals(lines):
    principals = []
    reading = False
    for l in lines:
        if l.startswith('Critical Options:'):
            reading = False
        if reading:
            principals.append(l)
        if l == 'Principals:':
            reading = True
    return principals

def still_valid(cert_timestamps):
    t = datetime.today()
    return t < cert_timestamps['valid']['to'] and t > cert_timestamps['valid']['from']


def expired(cert_timestamps):
    t = datetime.today()
    return t > cert_timestamps['valid']['to']


def not_valid(cert_timestamps):
    t = datetime.today()
    return t < cert_timestamps['valid']['from']


def cert_type(lines):
    for l in lines:
        if l.startswith('Type'):
            return l.split(maxsplit=2)[1:]


def valid_from(lines):
    for l in lines:
        if l.startswith('Valid'):
            return datetime.strptime(l.split()[2], CERT_TIME_FORMAT)


def valid_to(lines):
    for l in lines:
        if l.startswith('Valid'):
            return datetime.strptime(l.split()[4], CERT_TIME_FORMAT)


def main():
    module = AnsibleModule(
               argument_spec=dict(
                   principals=dict(
                       required=True,
                       type='list',
                   ),
                   path=dict(
                       required=False,
                       type='str',
                       default='/etc/ssh/ssh_host_ed25519_key-cert.pub',
                   ),
                   ca_path=dict(
                       required=False,
                       type='str',
                       default='/etc/ssh/user_ca.pub',
                   ),
               ),
               supports_check_mode=False,
    )
    result = {}
    result['rc'] = 0
    result['msg'] = ''
    result['failed'] = False
    result['ca'] = {}
    result['ca']['path'] = module.params.get('ca_path')
    result['certificate'] = {}
    result['certificate']['path'] = module.params.get('path')

    ca_output = subprocess.check_output([
            'ssh-keygen',
            '-l',
            '-f', result['ca']['path'],
        ])

    # If multiple CA are present verify cert against the first one
    ca_output = ca_output.splitlines()[0]
    ca_lines = ca_output.decode().split(maxsplit=2)
    result['ca']['fingerprint'] = ca_lines[1]
    result['ca']['comment'] = ca_lines[2]

    cert_output = subprocess.check_output([
                                           'ssh-keygen',
                                           '-L',
                                           '-f', result['certificate']['path'],
                                          ])
    cert_lines = [line.strip() for line in cert_output.decode().split('\n')]

    result['certificate']['signin_ca'] = signin_ca(cert_lines)
    result['certificate']['principals'] = principals(cert_lines)
    result['certificate']['valid'] = {
                'from': valid_from(cert_lines),
                'to': valid_to(cert_lines),
                'remaining_days': (valid_to(cert_lines)-datetime.now()).days
            }

    if not still_valid(result['certificate']):
        result['failed'] = True
        result['msg'] += 'The certificate is not valid now. '
        if not_valid(result['certificate']):
            result['rc'] += 2
        if expired(result['certificate']):
            result['rc'] += 4

    result['certificate']['serial'] = serial(cert_lines)
    result['certificate']['type'] = cert_type(cert_lines)

    if not result['certificate']['signin_ca'] == result['ca']['fingerprint']:
        result['failed'] = True
        result['msg'] = 'The provided CA did not sign the certificate specified. '
        result['rc'] += 1

    principal_mismatch = False
    for principal in module.params.get('principals'):
        if not principal in result['certificate']['principals']:
          principal_mismatch = True
          result['msg'] += 'Principal {} not found in cert. '.format(principal)
    if principal_mismatch:
        result['failed'] = True
        result['rc'] += 8
    module.exit_json(**result)


if __name__ == '__main__':
    main()
