.. highlight:: yaml

lxc_guest
=========

This role provides the building blocks to create a virtual machine using lxc containers on a phisical server:: 

    - hosts: phisical_host
      roles:
        - role: lxc_guest
          vm_name: virtual_machine_name

Additional parameter can be specified, the defaults are documented into the `lxc_guest` default folder::

    - hosts: phisical_host
      roles:
        - role: lxc_guest
          vm_name: virtual_machine_name
          auto_start: true
          container_state: started
          distro: jessie
          vm_size: 5G

During the role execution there are multiple phases

- Create the container and assign the configuration
- Update the container dns configuration
- Creation of the host ssh certificate if needed
- Update the container network configuration
- Install python and openssh-server
- Update of the user ssh certification authority public key
