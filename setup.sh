#!/bin/bash

# Setup the proxy for all the machine
cd pre_setup_proxy/
ansible-playbook -i inventory setup.yml

# Setup the OpenVswitch
cd ../kubernetes-ansible/old-network-config/
ansible-playbook -i inventory hack-ovs.yml

#Install kubernetes 
cd ..
ansible-playbook -i inventory setup.yml
