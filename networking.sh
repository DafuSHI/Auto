#!/bin/bash

# Setup the OpenVswitch
ansible-playbook -i /kubernetes-ansible/old-network-config/inventory hack-ovs.yml

