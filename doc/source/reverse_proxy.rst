.. highlight:: yaml

reverse_proxy
=============

This role provides the mean of exposing a machine to the web (http and https), it is currently bound to the *reverse_proxy* host but it will be extended to be available to other as well.

Usage
-----

To expose the web services to the internet (http and https) for the resource pippo (a machine or a group) add the role **reverse_proxy** to the playbook.

This will first connect to the `pippo` hosts, execute the `role1` and then connect to the `reverse_proxy` host to add the proxy rules for `pippo`.

.. code-block:: yaml

    - hosts: pippo
      roles:
        - role: role1
        - role: reverse_proxy

By default the domain exposed is created from the resource name, i.e. `pippo.lilik.it` but this can be changed by setting the `hostname` variable for the role `reverse_proxy`.

.. code-block:: yaml

    - hosts: pippo
      roles:
        - role: role1
        - role: reverse_proxy
          hostname: pluto

Rationale behind this role
--------------------------

We have choosen to use **nginx** as our reverse proxy and because of the number of targets this can't be accomplished using a unique configuration file for nginx as it would need to know every rule every time it's configuration changes.

Nginx provides the featuer to load configuration files from multiple directories and then merge the into one so we have choose to use three different directories.

.. code-block:: bash

    nginx.conf
    map.conf.d/
    upstream.conf.d/
    http.conf.d/

`nginx.conf` is the nginx configuration file, there we specify to include the the three directories in specific directives.

`http.conf.d` contains the files for the *http* reverse proxy directive.

`upstream.conf.d` contains the files where we specify a map from an id to the pool of the machines associated.

`map.conf.d` contains the files where we specify the list of domains and their mappings to a resource id.

We have choosen to separate this relation domain <-> machine by using an id because it will be used to make fun things such as high-availability or mapping more domains to the same resource id (but in different files) without the assle of checking if the nginx configuration will be broken by our automation.

As an example take the mapping from `ca.lilik.it` to the machine `10.150.42.x`, we can have another mapping from `certificationauthority.lilik.it` to the same machine without the hassle of checking if a upstream rule is used by some mappings when we want to deprecate `certificationauthority.lilik.it`
