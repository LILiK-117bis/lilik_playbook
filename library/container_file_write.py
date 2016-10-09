#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: container_file_write
author: Edoardo Putti
short_description: Write to a file in a container
description:
    - Write the content to a file
options:
    name:
        required: true
        description:
            - Name of the container
    path:
        required: true
        description:
            - path of the file to check
    text:
        required: true
        description:
            - content to write
    append:
        required: false
        default: false
        description:
            - append instead of overwrite
'''
def write_file_in_container(args):
    (path, text) = args
    with open(path, 'w') as out:
        out.write(text)
    return 0

def append_file_in_container(path, text):
    with open(path, 'a') as out:
        out.write(text)
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
                text = dict(
                    required = True,
                    type = 'str',
                    ),
                append = dict(
                    default = False,
                    required = False,
                    type = 'bool',
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
    text = module.params.get('text')
    append = module.params.get('append')

    result = {}
    result['name'] = container_name
    result['path'] = file_path

    if container_name in lxc.list_containers():

        container = lxc.Container(container_name)

        if append:
            writing_function = append_file_in_container
        else:
            writing_function = write_file_in_container

        file_exists = container.attach_wait(
                writing_function,
                (file_path, text,),
                env_policy = lxc.LXC_ATTACH_CLEAR_ENV,
                )

    else:
        result['changed'] = False
        result['failed'] = True
        result['msg'] = "Target container does not exists"

    module.exit_json(**result)

if __name__ == '__main__':
    main()
