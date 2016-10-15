#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: container_file_exists
author: Edoardo Putti
short_description: Return whether a file is present in the container
description:
    - Check if the given path exists on the given container
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

def check_file_in_container(args):
    (path, module) = args
    import os

    module.exit_json(
            exists = os.path.exists(path),
            path = path,
            )

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

    if container_name in lxc.list_containers():

        container = lxc.Container(container_name)

        file_exists = container.attach_wait(
                check_file_in_container,
                (file_path, module),
                env_policy = lxc.LXC_ATTACH_CLEAR_ENV,
                )

    else:
        module.fail_json(
                changed = False,
                msg = 'Target container does not exists',
                )

if __name__ == '__main__':
    main()
