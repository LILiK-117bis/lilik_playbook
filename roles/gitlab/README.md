# Role: gitlab

Set-up a Omnibus GitLab server

## Configuration variables

| Name                           | Description                                     |
|--------------------------------|-------------------------------------------------|
| `host_fqdn`                    | [`$hostname.dmz.$domain`]                       |
| `gitlab_ssh_port`              | External SSH port. [`22`]                       |
| `ldap_server`                  | LDAP server fqdn [`'ldap1.dmz.$domain'`]        |
| `ldap_tls_server_ca`           | [`$tls_root_ca`]                                |
| `ldap_domain`                  | LDAP domain, used to derive base dn [`$domain`] |
| `gitlab_enable_https`          | Enable HTTPS. [`false`]                         |
| `gitlab_enable_mattermost`     |                                                 |
| `gitlab_nginx_main_fqdn`       | [`$hostname.$domain`]                           |
| `gitlab_nginx_mattermost_fqdn` | [`mattermost.$domain`]                          |
| `gitlab_nginx_proxy_protocol`  | [`true`]                                        |
| `ldap_admin_dn`                | DN of a LDAP user with admin privileges.        |
| `ldap_admin_pw`                | Bind password of that user.                     |
| `gitlab_initial_root_password` | Available only before initialization.           |

**Note**: The Ansible controller must have OpenLDAP properly configured
with root ca set in `~/.ldaprc`.

## Minimal example

group_vars/all.yaml:

	---
	domain: 'example.com'
	user_ca_keys:
	  - "ssh-ed25519 ################### CA"
	tls_root_ca: |
	  -----BEGIN CERTIFICATE-----
	  ###########################
	  -----END CERTIFICATE-----

hosts:

	vm_gateway            ansible_host=10.0.2.1   ansible_user=root
	authorities_request   ansible_host=10.0.1.8   ansible_user=request
	host1                 ansible_host=10.0.1.1   ansible_user=root
	ldap1                 ansible_host=10.0.2.2   ansible_user=root ansible_lxc_host=host1
	gitlab                ansible_host=10.0.2.3   ansible_user=root ansible_lxc_host=host1

playbook.yaml:

	---
	# Configure GitLab on a Physical Host
	- hosts: 'host1'
      roles:
	    - role: 'dns_record'
	    - role: 'reverse_proxy'
		  hostname: 'projects'
	    - role: 'gitlab'


Command line:

	ansible-playbook -i hosts playbook.yaml \
		-e ldap_admin_dn=<admin_dn> -e \
		-e ldap_amdin_pw=<admin_pw>


## Requirements

On Ansible controller:

- tasks/ca-dialog.yaml

