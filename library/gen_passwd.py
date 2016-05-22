#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: gen_passwd
author: Daniele Baracchi
short_description: Generate a random password
description:
    - Generate a random password
options:
    length:
        required: true
        description:
            - Length of the generated password
'''

from random import SystemRandom
import string

from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
            argument_spec=dict(
                length=dict(required=True, type='int')
            ),
            supports_check_mode=True
    )

    length = module.params.get('length')

    result = {}
    result['length'] = length

    rng = SystemRandom()

    valid_chars = string.ascii_uppercase + string.ascii_lowercase + \
            string.digits

    passwd = [rng.choice(valid_chars) for _ in xrange(length)]

    result['passwd'] = ''.join(passwd)

    result['changed'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()
