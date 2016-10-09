#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: container_file_content
author: Edoardo Putti
short_description: Return the content of a file
description:
    - Retrieve the content for the given path on the given container
options:
    name:
        required: true
        description:
            - Name of the container
    path:
        required: true
        description:
            - path of the file to check
'''

def read_file_in_container(path):
    import json
    with open(path, 'r') as lines:
        print(json.dump({ key_data: lines.read()}))
    return 0

def main():
    module = AnsibleModule(
            argument_spec = dict(
                name = dict(
                    required = True,
                    type = 'str',
                    ),
                path = dict(
                    required = True,
                    type = 'str',
                    ),
            ),
    )

    try:
        import lxc

    except ImportError:
        module.fail_json(
                changed = False,
                failed = True,
                msg = 'Error importing lxc, is python-lxc installed?',
                )

    container_name = module.params.get('name')
    file_path = module.params.get('path')

    result = {}
    result['name'] = container_name
    result['path'] = file_path

    if container_name in lxc.list_containers():

        container = lxc.Container(container_name)

        file_exists = container.attach_wait(
                read_file_in_container,
                file_path,
                env_policy = lxc.LXC_ATTACH_CLEAR_ENV,
                )

    else:
        result['changed'] = False
        result['failed'] = True
        result['msg'] = "Target container does not exists"

    module.exit_json(**result)

if __name__ == '__main__':
    main()
