#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: container_exists
author: Edoardo Putti
short_description: Check existance for container
description:
    - Check if a container with the given name exists
options:
    name:
        required: true
        description:
            - Name of the container
'''

from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
            argument_spec=dict(
                name= dict(
                    required= True,
                    type= 'str',
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
        result['exists'] = True
    else:
        result['exists'] = False


    result['changed'] = False
    module.exit_json(**result)


if __name__ == '__main__':
    main()
