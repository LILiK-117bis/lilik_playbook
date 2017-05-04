.. highlight:: yaml

lxc_ssh
=========

This connection plugin provides a mean of communication for a vm that does not trust (yet) the user certification authority.

Usage
-----

We can use the `lxc_ssh` connection to install the user certification authority on a newly created virtual machine like in the following example

.. code-block:: yaml

    - hosts: phisical_host
      roles:
        - role: lxc_guest
          vm_name: virtual_machine_name
        - role: ssh_server
          ansible_connection: lxc_ssh
          ansible_docker_extra_args: wiki
