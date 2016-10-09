#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: container_certificate_exists
author: Edoardo Putti
short_description: Return wheter a certificate is present in the container
description:
    - Look for the /etc/ssh/ssh_host_ed25519_key-cert.pub file
options:
    name:
        required: true
        description:
            - Name of the container
'''

from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
            argument_spec = dict(
                name = dict(
                    required = True,
                    type = 'str',
                    ),
            ),
            supports_check_mode=True
    )
    
    try:
        import lxc
    except ImportError:
        self.module.fail_json(
                changed= False,
                msg= 'Error importing lxc, is python-lxc installed?',
                )

    container_name = module.params.get('name')

    result = {}
    result['name'] = container_name

    if container_name in lxc.list_containers():

        container_certificate = container.attach_wait(
                lxc.attach_run_command,
                ['cat', '/etc/ssh/ssh_host_ed25519_key-cert.pub',],
                )
        result['changed'] = True
        result['msg'] = container_certificate
        
    else:
        result['changed'] = False
        result['failure'] = True
        result['msg'] = "Target container does not exists"

    module.exit_json(**result)

if __name__ == '__main__':
    main()
