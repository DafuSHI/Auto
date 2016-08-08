#!/usr/bin/python

import subprocess
import re

def main():
    module = AnsibleModule(
        argument_spec = dict(
        ),
    )

    facts = {}
    facts['kube_node_via_api'] = True
    facts['kube_node_v1'] = True
    facts['kubelet_use_pre_v10_vars'] = False
    facts['DNS_not_installed'] = True

    result = {}
    result['rc'] = 0
    result['changed'] = False
    result['ansible_facts'] = facts

    #args = ("kubectl", "version", "-c")
    args = ("kubectl", "version", "--client")
    #Flag shorthand -c has been deprecated; use --client instead
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

    output = popen.stdout.read()
    match = re.search("Major:\"(\d+)\"", output)
    if not match:
        module.fail_json(msg="Major not found!")
    major = int(match.group(1))

    match = re.search("Minor:\"(\d+)(\.\d+)?\+?\"", output)
    if not match:
        module.fail_json(msg="Minor not found!")
    minor = int(match.group(1))

    if minor < 10 and major < 0:
        facts['kube_node_via_api'] = False
        facts['kubelet_use_pre_v10_vars'] = True

    args = ("kubectl", "api-versions")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

    output = popen.stdout.read()
    if "v1" not in output:
        facts['kube_node_v1'] = False

    args = ("kubectl", "get", "pods", "--namespace=kube-system")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

    output = popen.stdout.read()
    if "dns" in output:
        facts['DNS_not_installed'] = False
    
    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()
