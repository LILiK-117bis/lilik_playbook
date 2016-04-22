#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: json_file
author: Daniele Baracchi
short_description: Manipulate json files
description:
    - Manipulate json files
options:
    path:
        required: true
        description:
            - Path to the JSON file to be manipulated.
    key:
        required: true
        description:
            - Key to be checked.
    value:
        required: false
        description:
            - Value to set the key to.
    state:
        required: false
        default: "present"
        choices: [ "present", "absent" ]
        description:
            - Whether the key should exist or not, taking action if the state is different from what is stated.
'''

import json
import os.path

from ansible.module_utils.basic import *


class JsonFile(object):
    def __init__(self, path):
        self.path = path

        with open(path, 'r') as stream:
            self.contents = json.load(stream)

    def has_key(self, key):
        key_path = key.split('.')

        container = self.contents

        for part in key_path:
            if part in container:
                container = container[part]
            else:
                return False

        return True

    def has_pair(self, key, value):
        key_path = key.split('.')

        container = self.contents

        for part in key_path:
            if part in container:
                container = container[part]
            else:
                return False

        return container == value

    def drop_key(self, key):
        key_path = key.split('.')

        container = self.contents

        for part in key_path[:-1]:
            container = container[part]

        del container[key_path[-1]]

    def set_key(self, key, value):
        key_path = key.split('.')

        container = self.contents

        for part in key_path[:-1]:
            if part not in container:
                container[part] = {}
            container = container[part]

        container[key_path[-1]] = value

    def serialize(self):
        with open(self.path, 'w') as stream:
            json.dump(self.contents, stream, indent=4)


def main():
    module = AnsibleModule(
            argument_spec=dict(
                state=dict(default='present', choices=['present', 'absent'],
                    type='str'),
                path=dict(required=True, type='str'),
                key=dict(required=True, type='str'),
                value=dict(default=None, type='str')
            ),
            supports_check_mode=True
    )

    path = module.params.get('path')
    key = module.params.get('key')
    state = module.params.get('state')

    result = {}
    result['path'] = path
    result['key'] = key
    result['state'] = state

    if not os.path.exists(path):
        module.fail_json("File not found: %s" % path)

    the_file = JsonFile(path)

    if state == 'absent':
        if the_file.has_key(key):
            if module.check_mode:
                module.exit_json(changed=True)
            else:
                the_file.drop_key(key)
                the_file.serialize()
                result['changed'] = True
    elif state == 'present':
        value = module.params.get('value')
        result['value'] = value

        if not the_file.has_pair(key, value):
            if module.check_mode:
                module.exit_json(changed=True)
            else:
                the_file.set_key(key, value)
                the_file.serialize()
                result['changed'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()
