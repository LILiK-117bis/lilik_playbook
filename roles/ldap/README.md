# Role: ldap

Set-up a LDAP server

## Configuration variables

| Name                 | Description                                                 |
|----------------------|-------------------------------------------------------------|
| `ldap_domain`*       | Dot-form domain name (i.e.: `'lilik.it'`).                  |
| `ldap_organization`* | Organization (i.e.: `'LILiK'`).                             |
| `ssl_subject_prefix` | X.509 TLS Cert Subject (i.e: `'/ST=IT/L=Firenze/O=LILiK'`). |
| `fqdn_domain`*       | Required for TLS certificate.                               |
| `x509_suffix`*       | The same in LDAP form (i.e: `'o=LILiK,l=Firenze/st=IT'`).   |
| `virtual_domains`    | Required with `check_tree`: list of vds to init.            |
| `ldap_tls_enabled`   | Enables TLS, requires a *ca_manager*. [`true`]              |
| `renew_rootdn_pw`    | Create a new random password for RooDN. [`true`]            |
| `check_tree`         | Deploy initial tree configuration. [`true`]                 |


**Note:** If `ldap_tls_enabled` the *ca_manager* host should be configured
and TLS Root CA should be set in vars.

## Minimal example

group_vars/all.yaml:

	---
	domain: 'example.com'
	ssl_subject_prefix: '/C=IT/L=Firenze/O=LILiK'
	x509_suffix: 'o=LILiK,l=Firenze,st=IT'
	user_ca_keys:
	  - "ssh-ed25519 ################### CA"
	ssl_ca_cert: |
	  -----BEGIN CERTIFICATE-----
	  ###########################
	  -----END CERTIFICATE-----

hosts:

	vm_gateay             ansible_host=10.0.2.1   ansible_user=root
	authorities_request   ansible_host=10.0.1.8   ansible_user=request
	host1                 ansible_host=10.0.1.1   ansible_user=root
	ldap1              ansible_host=10.0.2.2   ansible_user=root    ansible_lxc_host=host1

playbook.yaml:

	---
	# Configure LDAP on a Physical Host
	- hosts: 'host'
      roles:
	    - role: ldap
		  ldap_domain: 'example.com'
		  ldap_organization: 'Example'
		  fqdn_domain: '{{ domain }}'
		  virtual_domains:
		    - 'example.com'

	# Configure LDAP on a LXC container
	- hosts: 'ldap1'
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
	- hosts: 'ldap1'
	  roles:
	    - role: 'dns_record'
		- role: 'ldap'
		  ldap_domain: 'example.com'
	      ldap_organization: 'Example'
		  fqdn_domain: '{{ domain }}'
		  virtual_domains:
		    - 'example.com'

Command line:

	ansible-playbook -i hosts playbook.yaml


## Requirements

On Ansible controller:

- tasks/ca-dialog.yaml

