# Role: ssh_server

This role congigure an *OpenSSH* server configured with certifcates
provided by a local *ca_manager* instance.

Root password login in disabled and *certificate authentication* is
enabled for users with certificate issued by the authorized authorities,
listed in the variables `user_ca_keys`.

For the role to work the local certification authority must be
configured and reachable from the Ansible controller machine.

The local user must be able to automatically login as the `request` use
to the *ca_manager* instance.

## Configuration variables

| Name            | Description                                                     |
|-----------------|-----------------------------------------------------------------|
| `user_ca_keys`* | List of allowed CA certificate. First entry is the default one. |
| `host_fqdn`     | Used for the host certificate. [`$host.dmz.$domain`]            |


**Note: The *ca_manager* instance should be present in the inventory.

## Minimal example

group_vars/all.yaml:

	---
	domain: 'example.com'
	user_ca_keys:
	 - 'ssh-ed25519 ############## Production CA'
	 - 'ssh-ed25519 ############## Backup CA'

hosts:

	vm_gateay             ansible_host=10.0.2.1   ansible_user=root
	authorities_request   ansible_host=10.0.1.8   ansible_user=request
	host1                 ansible_host=10.0.1.1   ansible_user=root
	virtual1              ansible_host=10.0.2.2   ansible_user=root    ansible_lxc_host=host1

playbook.yaml:

	---
	# Configure SSH on a Physical Host
	- hosts: host1
      roles:
	    - role: ssh_server

	# Configure SSH on a new LXC Guest with ssh_lxc proxy
	- hosts: virtual1
	  gather_facts: false # host may not exist yet
	  tasks:
	    - import_role: name='lxc_guest'
		  vars:
		   vm_name: '{{ inventory_hostname }}'
		   vm_size: '1G'
	      delegate_to: '{{ ansible_lxc_host }}'
        - set_fact: ansible_connection='ssh_lxc'
		- setup: # gather facts
		- include_role: name='ssh_server'
		# Now the guest is ssh-reachable, don't need proxy anymore.
		- set_fact: ansible_connection='ssh'

Command line:

	ansible-playbook -i hosts playbook.yaml


## Requirements

On Ansible controller:

- tasks/ca-dialog.yaml

