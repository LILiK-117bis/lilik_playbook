def ip_from_inventory(hostvars, hostname):
    """
    replace this ``{{ hostvars[hostname]['ansible_host'] }}``
    with something nicer such as `` {{ hostvars | ip_from_inventory(hostname) }}``
    """
    return hostvars[hostname]['ansible_host']

class FilterModule(object):
    def filters(self):
        return {
                'ip_from_inventory': ip_from_inventory,
        }

