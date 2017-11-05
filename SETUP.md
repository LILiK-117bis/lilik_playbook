SETUP
=========

1. Copy `group_vars/all.yaml.example` to `group_vars/all.yaml`
2. Fill `group_vars/all.yaml` with the gateway hostname, the content of the `user_ca_key`, the public ip you are using and the domain you use
3. Add to the *inventory* the `gateway`, `reverse_proxy`, `authorities` and `authorities_request` entry. Follow the `inventory.example` format. These are the minimum entry that you neeed to make everything work in this playbook. 
