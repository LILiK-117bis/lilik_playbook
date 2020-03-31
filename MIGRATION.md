# State of migration of each role

Each new role will be tested against:

On the controller:

- `python==3.7.3` (Debian Stable)
- `python==3.8.2`
- `ansible==2.9.6`

On the hosts:

- `python==3.7.3`
- `debian==buster` (physical hosts and containers)
- `openwrt` (firewall)

# Current status

## Roles

| Role name          | Modified? | Tested?  | Production? | Notes                                                                                    |
|--------------------|:---------:|:--------:|:-----------:|------------------------------------------------------------------------------------------|
|`roles/service`     | **YES**   | **YES**  | NO          | Changes in Ansible built-in `apt` module.                                                |
|`roles/ssh_server`  | **YES**   | **YES**  | NO          | `lxc_ssh.py` --> `ssh_lxc.py`.                                                           |
|`roles/ca`          | **YES**   | ReadNote | NO          | Changes in Ansible built-in `apt` module. Needs update of `ca_manager` to [1] to work.   |
|`prepare_host.yaml` | **YES**   | **YES**  | NO          | Debian stretch --> buster and Python 2 --> 3                                             |
|`roles/ldap`        | NO        | NO       | NO          |                                                                                          |
|`roles/nginx`       | NO        | NO       | NO          |                                                                                          |
|`roles/projects`    | NO        | NO       | NO          |                                                                                          |
|`roles/dns_record`  | NO        | NO       | NO          |                                                                                          |
|`roles/openvpn`     | NO        | NO       | NO          |                                                                                          |


## Plugins and Modules

| Plugin/Module name     | Modified? | Tested?   | Production? | Notes                                |
|------------------------|:---------:|:---------:|:-----------:|--------------------------------------|
|`connection/lxc_ssh.py` | *REMOVED* |           |             |                                      |
|`connection/ssh_lxc.py` | **NEW**   | **YES**   |    NO       | Replace `lxc_ssh.py`.                |
|`library/ssh_cert.py`   | **YES**   | **YES**   |    NO       | Migrate from `python2` to `python3`. |

[1]: https://github.com/LILiK-117bis/ca_manager/tree/peewee3%2Brfc5280
