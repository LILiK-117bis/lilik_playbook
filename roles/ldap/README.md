# Role: ldap

Set-up a LDAP server

## Configuration variables

| Name                   | Description                                        |
|------------------------|----------------------------------------------------|
| `host_fqdn`            | FQDN of the host [`$hostname.dmz.$domain`]         |
| `ldap_domain`          | Dot-form domain name. [`$domain`]                  |
| `ldap_organization`    | Organization [`$organization`]                     |
| `ldap_check_tree`      | Populate tree with initial configuration. [`true`] |
| `ldap_tls_enabled`     | Enables TLS, requires a *ca_manager*. [`true`]     |
| `ldap_tls_server_ca`   | CA to check slapd cert [`$tls_root_ca`]            |
| `ldap_tls_user_ca`     | CA to authenticate users [`$tls_root_ca`]          |
| `virtual_domains`      | Required with `check_tree`: list of vds to init.   |


**Note:** If `ldap_tls_enabled` the *ca_manager* host should be configured
and TLS Root CA should be set in vars.

## Minimal example

group_vars/all.yaml:

	---
	domain: 'example.com'
	organization: 'LILiK'
	x509_subj_prefix:
	  C: 'IT'
	  L: 'Firenze'
	  O: '{{ organization }}'

	user_ca_keys:
	  - "ssh-ed25519 ################### CA"
	tls_root_ca: |
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
		  virtual_domains:
		    - 'example.com'

Command line:

	ansible-playbook -i hosts playbook.yaml


## Requirements

On Ansible controller:

- tasks/ca-dialog.yaml

