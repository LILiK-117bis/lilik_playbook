from ansible.errors import AnsibleError, AnsibleParserError

def ip_from_inventory(hostvars, hostname):
    """
    replace this ``{{ hostvars[hostname]['ansible_host'] }}``
    with something nicer such as `` {{ hostvars | ip_from_inventory(hostname) }}``
    """
    if not hostname in hostvars:
        raise AnsibleError('<ip_from_inventory> hostname "{hostname}" not found in inventory'.format(hostname=hostname))

    return hostvars[hostname]['ansible_host']

class FilterModule(object):
    def filters(self):
        return {
                'ip_from_inventory': ip_from_inventory,
        }

