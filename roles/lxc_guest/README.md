# Role: lxc_guest

This role creates a debian LXC container on an host previously with LXC
and network in bridged mode, connecting the container to the interface
`br0` on the host.

The ip address and gateway of the container are automatically discovered
from the ansible inventory. The `vm_gateway` entry IP is used as gateway
while the entry associated with `vm_name` IP is used as static IP
address.

## Configuration variables

| Name         | Description                             |
|--------------|-----------------------------------------|
| `vm_name`*   | Name of the LXC container.              |
| `vm_size`    | Size of the VM logical volume. [`'5G'`] |
| `distro`     | Debian release name. [`'buster'`]       |
| `auto_start` | Auto-start container. [`true`]          |
| `domain`*    | The VM domain is set to dmz.$domain     |
| `vg_name`**  | LVM volume group name on the host.      |

**Note: If `vg_name` is not provided it will be derived from the
        `ansible_lxc_host` variable in the inventory entry of the guest.
		If the entry pointed by `ansible_lxc_host` doesn't set has an
		alterntive `vg_name` set, it will default to `ansible_lxc_host`+'-vg'.

## Minimal example

group_vars/all.yaml:

	---
	domain: 'example.com'

hosts:

	vm_gateway  ansible_host=10.0.2.1   ansible_user=root
	physical1   ansible_host=10.0.1.1   ansible_user=root  vm_name=test-vg
	vm1         ansible_host=10.0.2.10  ansible_user=root  ansible_lxc_host=physical1

vm1.yaml:

	---
	- hosts: vm1
	  gather_facts: false # host may not exist yet
	  tasks:
	    - import_role: name='lxc_guest'
		  vars:
		   vm_name: '{{ inventory_hostname }}'
		   vm_size: '1G'
	      delegate_to: '{{ ansible_lxc_host }}'

Command line:

	ansible-playbook -i hosts vm1.yaml

## Requirements

On Ansible controller:

- connection_plugins/ssh_lxc.py

On LXC host:

- python3-lxc module.


## See also

The playbook `prepare_host.yaml` provides a working configuration for
the physical machine running LXC.

