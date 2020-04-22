# Role: ldap

Set-up a LDAP server

## Configuration variables

| Name                   | Description                                                 |
|------------------------|-------------------------------------------------------------|
| `ldap_domain`          | Dot-form domain name. [`$domain`]                           |
| `ldap_organization`*   | Organization (i.e.: `'LILiK'`).                             |
| `x509_subject_prefix`* | X.509 TLS Cert Subject (i.e: `'/ST=IT/L=Firenze/O=LILiK'`). |
| `x509_ldap_suffix`*    | The same in LDAP form (i.e: `'o=LILiK,l=Firenze/st=IT'`).   |
| `server_fqdn`*         | Required for TLS certificate. [`'$hostname.dmz.$domain'`]   |
| `virtual_domains`      | Required with `check_tree`: list of vds to init.            |
| `ldap_tls_enabled`     | Enables TLS, requires a *ca_manager*. [`true`]              |
| `renew_rootdn_pw`      | Create a new random password for RooDN. [`true`]            |
| `check_tree`           | Deploy initial tree configuration. [`true`]                 |


**Note:** If `ldap_tls_enabled` the *ca_manager* host should be configured
and TLS Root CA should be set in vars.

## Minimal example

group_vars/all.yaml:

	---
	domain: 'example.com'
	x509_subject_prefix: '/C=IT/L=Firenze/O=LILiK'
	x509_ldap_suffix: 'o=LILiK,l=Firenze,st=IT'
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
		  #ldap_domain: '{{ domain }}'
		  #server_fqdn: '{{ ansible_hostname }}.dmz.{{ domain }}'
		  ldap_organization: 'Example'
		  virtual_domains:
		    - 'example.com'

Command line:

	ansible-playbook -i hosts playbook.yaml


## Requirements

On Ansible controller:

- tasks/ca-dialog.yaml

