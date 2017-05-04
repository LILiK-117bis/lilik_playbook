..

`prepare_host.yaml`
===================

This playbook provides the necessary setup for a phisical server to become a server in the lilik architecture.

This is not a role as the requirements for this step are very simple and not sophisticated.

The configuration of the phisical server touches the following features.

- Installation of the lxc binaries, python bindings and network bridge utilities.
- Installation of the vlan module
- Configuration of bridge network with vlans for management and virtual machine segregation
- Installation of packages required by humans such as `htop` and `vim`- Configuration to use user ssh certificates as credentials

The only variables that are specified in here are the vlans ids, `9` for the management vlan and `13` for the virtual machine vlan.

