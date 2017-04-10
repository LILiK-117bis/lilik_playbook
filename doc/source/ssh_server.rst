.. highlight:: yaml

ssh_server
=========

SSH Certificate
---------------

During the execution of this role the vm host key will be used to create a certificate signin request.

This requests will be "posted" to the service known as ca manager and ansible will then wait for a certificate from the same service.

This is accomplished using ssh as a mean of transport, the specific task for a signin requests is alwasys like this

.. code-block:: yaml

        - name: generate host request
          set_fact:
            cert_request:
              type: 'sign_request'
              request:
                keyType: 'ssh_host'
                hostName: '{{ vm_name }}'
                keyData: '{{ vm_public_key.text}}'

        - name: start sign request
          raw: "{{ cert_request | to_json }}"
          delegate_to: ca_request
          register: request_result
          failed_when: "( request_result.stdout | from_json ).failed"

To sign this certificate an admin must log onto the ca manager machine with the user *sign* and follow the procedure to sign a request with an appropriate certification authority.
