from ansible.hostvars import HostVars

def ip_from_inventory(hostname):
    """
    replace this ``{{ hostvars[hostname]['ansible_host'] }}``
    with something nicer such as `` {{ hostname | ip_from_inventory }}``
    """
    return HostVars[hostname]['ansible_host']

class FilterModule(object):
    def filter(self):
        return {
                'ip_from_inventory': ip_from_inventory,
        }

