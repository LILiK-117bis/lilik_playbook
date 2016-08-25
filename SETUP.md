SETUP
=========

1. Copy `group_vars/all.yaml.example` to `group_vars/all.yaml`
2. Fill `all.yaml` with the gateway hostname and the content of the `user_ca_key`
3. Add the gateway hostname to `inventory`, set `ansible_host` and `ansible_user`
4. Add the ca hostname to `inventory`, set `ansible_host` and `ansible_user`

