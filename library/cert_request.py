#! /usr/bin/env python

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: cert_request
author: Edoardo Putti
short_description: generate a host certificate request
options:
    host:
        required: true
        description: FQDN for the host
    path:
        required: true
        description: path to key to be signed
    proto:
        required: true
        description:
        choices:
          - ssh
          - ssl
'''

EXAMPLES = '''
- name: Generate ssl host request
  cert_request:
    host: "gandalf.lilik.it"
    path: "/etc/openvpn/openvpn.csr"
    proto: "ssl"

- name: Generate ssh host request
  cert_request:
    host: ""
    path: "/etc/ssh/ssh_host_ed25519_key.pub"
    proto: "ssh"
'''

RETURN = '''
type
  description: protocol used for the key
  returned: always
  sample: sign_request
  type: string
keyType
  description: which type of key we are requesting
  returned: always
  sample:
    ssh_host
    ssl_host
hostName
  description: FQDN of the host requesting a cert
  returned: always
  sample:
    example.lilik.it
keyData:
  description: string representation of the key
  returned: always
'''


def main():
    module = AnsibleModule(
                argument_spec=dict(
                    host=dict(
                        required=True,
                        type='str',
                    ),
                    path=dict(
                        required=True,
                        type='str',
                    ),
                    proto=dict(
                        required=True,
                        choices=['ssh', 'ssl'],
                    ),
                ),
                supports_check_mode=False,
            )

    host = module.params.get('host')
    path = module.params.get('path')
    proto = module.params.get('proto')

    with open(path, 'r') as src:
        result = {
            'type': 'sign_request',
            'request': {
                'keyType': '{}_host'.format(proto),
                'hostName': host,
                'keyData': src.read(),
            },
        }
        module.exit_json(**result)


if __name__ == '__main__':
    main()
