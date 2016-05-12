#!/bin/bash

# Setup the OpenVswitch
/kubernetes-ansible/old-network-config/ansible-playbook -i inventory hack-ovs.yml

