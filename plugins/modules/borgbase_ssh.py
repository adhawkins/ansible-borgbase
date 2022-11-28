#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

# Copyright: (c) 2019, Andy Hawkins <andy@gently.org.uk>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: "borgbase_ssh"

short_description: "Module for managing SSH keys in borgbase."

version_added: "1.0.0"

description:
    "Module for managing SSH keys in borgbase."

options:
    email:
        description:
            "The email address associated with the borgbase account."
        required: false
        type: str
    password:
        description:
            "The password for the borgbase account."
        required: false
        type: str
    apikey:
        description:
            "The borgbase API key."
        required: false
        type: str
    state:
        description: >
            'present' to ensure the key exists, 'absent' to ensure it doesn't. When removing a key
            the match is carried out based on key name only. When adding a key, if a key exists with the
            same name but different content, the key will be silently replaced.
        default: present
        type: str
        choices: [ absent, present ]
    name:
        description:
            "The SSH key name."
        required: true
        type: str
    key:
        description:
            "The SSH public key (required if state is 'present')."
        required: false
        type: str

author:
    Andy Hawkins (@adhawkins)
'''

EXAMPLES = '''
- name: Read key from file
  slurp:
    src: ~/.ssh/id_rsa.pub
  register: ssh_key
  check_mode: yes

- name: Create key
  borgbase_ssh:
    state: present
    email: "{{ borgbase_email }}"
    password: "{{ borgbase_password }}"
    name: "{{ whoami.stdout }}@{{ ansible_hostname }}"
    key: "{{ ssh_key['content'] | b64decode }}"
  register: borgbase_key

- name: Dump create results
  debug:
    var: borgbase_key.key_id
'''

RETURN = '''
key_id:
    description: The ID of the key that was created or deleted.
    type: int
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.adhawkins.borgbase.plugins.module_utils.borgbase_client import BorgBaseClient

client = BorgBaseClient()


def login(email, password):
    loginResult = dict(
        success=True,
        errors=[]
    )

    res = client.login(email=email, password=password)
    if 'errors' in res:
        loginResult['success'] = False
        for error in res['errors']:
            loginResult['errors'].append(error['message'])

    return loginResult


def readKeys(apiKey=None):
    readResult = dict(
        success=True,
        errors=[],
        keys=[]
    )

    keys = client.execute(BorgBaseClient.SSH_LIST, apiKey=apiKey)
    if 'errors' in keys:
        readResult['success'] = False
        for error in keys['errors']:
            readResult['errors'].append(error['message'])
    else:
        for key in keys['data']['sshList']:
            readResult['keys'].append(key)

    return readResult


def addKey(name, key, apiKey=None):
    addResult = dict(
        success=True,
        errors=[]
    )

    key = client.execute(BorgBaseClient.SSH_ADD, dict(name=name, keyData=key), apiKey=apiKey)

    if 'errors' in key:
        addResult['success'] = False
        for error in key['errors']:
            addResult['errors'].append(error['message'])
    else:
        addResult['keyID'] = key['data']['sshAdd']['keyAdded']['id']

    return addResult


def deleteKey(id, apiKey=None):
    deleteResult = dict(
        success=True,
        errors=[]
    )

    result = client.execute(BorgBaseClient.SSH_DELETE, dict(id=id), apiKey=apiKey)
    if 'errors' in result:
        deleteResult['success'] = False
        for error in result['errors']:
            deleteResult['errors'].append(error['message'])

    return deleteResult


def findKey(keys, name):
    for key in keys:
        if name == key['name']:
            return key

    return None


def runModule():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        email=dict(type='str', default=None),
        password=dict(type='str', default=None, no_log=True),
        apikey=dict(type='str', default=None, no_log=True),
        state=dict(type='str', required=False, choices=['absent', 'present'], default='present'),
        name=dict(type='str', required=True),
        key=dict(type='str', required=False, no_log=False)
    )

    required_one_of = [
        ('email', 'apikey')
    ]

    required_together = [
        ('email', 'password')
    ]

    mutually_exclusive = [
        ('email', 'apikey')
    ]

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=required_one_of,
        required_together=required_together,
        mutually_exclusive=mutually_exclusive,
    )

    stateExists = (module.params['state'] == 'present')

    if module.params['email'] and module.params['password']:
        loginResult = login(module.params['email'], module.params['password'])

    if (module.params['apikey'] and (not module.params['email'] and not module.params['password'])) or loginResult['success']:
        # Get a list of keys in the account

        keys = readKeys(apiKey=module.params['apikey'])

        if keys['success']:
            foundKey = findKey(keys['keys'], module.params['name'])
            keyExists = foundKey is not None
            if keyExists:
                result['key_id'] = int(foundKey['id'])

            deleteRequired = False
            addRequired = False

            if keyExists and stateExists:
                # key provided can have a optional keyname, e.g.: "ssh-ed25519 AAAAC3Nd... root@localhost"
                # only keep algorithm and data
                providedKey = " ".join(module.params['key'].strip().split()[:2])
                if providedKey != foundKey['keyData']:
                    deleteRequired = True
                    addRequired = True

            if keyExists and not stateExists:
                deleteRequired = True

            if not keyExists and stateExists:
                addRequired = True

            result['changed'] = addRequired or deleteRequired

            if not module.check_mode:
                if deleteRequired:
                    deleteResult = deleteKey(int(foundKey['id']), apiKey=module.params['apikey'])
                    if not deleteResult['success']:
                        result['msg'] = ' '

                        for error in deleteResult['errors']:
                            result['msg'] += error

                        module.fail_json(**result)

                if addRequired:
                    addResult = addKey(module.params['name'], module.params['key'], apiKey=module.params['apikey'])
                    if addResult['success']:
                        result['key_id'] = addResult['keyID']
                    else:
                        result['msg'] = ' '

                        for error in addResult['errors']:
                            result['msg'] += error

                        module.fail_json(**result)
        else:
            result['msg'] = ' '

            for error in keys['errors']:
                result['msg'] += error

            module.fail_json(**result)
    else:
        result['msg'] = ' '

        for error in loginResult['errors']:
            result['msg'] += error

        module.fail_json(**result)

    module.exit_json(**result)


def main():
    runModule()


if __name__ == '__main__':
    main()
