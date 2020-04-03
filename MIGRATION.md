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

| Role name            | Modified? | Tested?  | Production? | Notes                                                                |
|----------------------|:---------:|:--------:|:-----------:|----------------------------------------------------------------------|
|`roles/service`       | **YES**   | **YES**  | NO          | New `apt` module style for packages.                                 |
|`roles/ssh_server`    | **YES**   | **YES**  | NO          | `lxc_ssh.py` --> `ssh_lxc.py`, multi-key support.                    |
|`roles/ca`            | **YES**   | ReadNote | NO          | New `apt` module style for pacakges. Works with this [ca_manager].   |
|`prepare_host.yaml`   | **YES**   | **YES**  | NO          | Migrate Debian release to Buster and Python 2 to 3.                  |
|`roles/lxc_guest`     | **YES**   | **YES**  | NO          | Updated Debian and LXC. `xfs` ***broken***, `ext4` working.          |
|`roles/ldap`          | **YES**   | **YES**  | NO          | `phamm.schema` now provided locally.                                 |
|`roles/nginx`         | NO        | NO       | NO          |                                                                      |
|`roles/projects`      | NO        | NO       | NO          |                                                                      |
|`roles/dns_record`    | NO        | NO       | NO          |                                                                      |
|`roles/openvpn`       | NO        | NO       | NO          |                                                                      |


## Plugins and Modules

| Plugin/Module name     | Modified? | Tested?   | Production? | Notes                       |
|------------------------|:---------:|:---------:|:-----------:|-----------------------------|
|`connection/lxc_ssh.py` | *REMOVED* |           |             |                             |
|`connection/ssh_lxc.py` | **NEW**   | **YES**   | NO          | Replace `lxc_ssh.py`.       |
|`library/ssh_cert.py`   | **YES**   | **YES**   | NO          | Migrate Python 2 to 3.      |
|`library/gen_passwd.py` | **YES**   | **YES**   | NO          | Migrate Python 2 to 3.      |

[ca_manager]: https://github.com/LILiK-117bis/ca_manager/tree/peewee3%2Brfc5280
