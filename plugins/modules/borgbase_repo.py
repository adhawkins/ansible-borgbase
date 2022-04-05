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
module: borgbase_repo

short_description: Module for managing repos in borgbase.

version_added: "1.0.0"

description:
    "Module for managing repos in borgbase."

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
        description:
            "'present' to ensure the repo exists, 'absent' to ensure it doesn't."
        default: present
        type: str
        choices: [ absent, present ]
    alert_days:
        description:
            "Number of days to send alerts if no activity detected."
        required: false
        default: 7
        type: int
    append_only:
        description:
            "True if repo is append only."
        required: false
        default: false
        type: bool
    append_only_keys:
        description:
            "List of keys for append only access."
        required: false
        type: list
        elements: int
    borg_version:
        description:
            "Version of borg to run on this repo."
        required: false
        type: str
        choices: [ latest, 1.1.x, 1.2.x ]
        default: latest
    full_access_keys:
        description:
            "List of keys for full access."
        required: false
        type: list
        elements: int
    name:
        description:
            "Repo name."
        required: true
        type: str
    quota:
        description:
            "Disk quota for this repo (MB)."
        required: false
        type: int
        default: 0
    quota_enabled:
        description:
            "Whether quota is enabled for this repo."
        required: false
        type: bool
        default: false
    region:
        description:
            "Repo region."
        type: str
        choices: [ eu, us ]
        required: false
        default: eu
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

- name: Create repo
  borgbase_repo:
    state: present
    email: "{{ borgbase_email }}"
    password: "{{ borgbase_password }}"
    name: "{{ ansible_hostname }}"
    full_access_keys: [ "{{ borgbase_key.key_id }}" ]
    quota_enabled: false
    alert_days: 1
  register: borgbase_repo

- name: Set borgbase repo id
  set_fact:
    borgbackup_borgbase_repo: "{{ borgbase_repo.repo_id }}"

- name: Set borgbackup_ssh_host
  set_fact:
    borgbackup_ssh_host: "{{ borgbackup_borgbase_repo }}.repo.borgbase.com"
'''

RETURN = '''
repo_id:
    description: The ID of the repo that was created or deleted.
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


def readRepos(apiKey=None):
    readResult = dict(
        success=True,
        errors=[],
        repos=[]
    )

    repos = client.execute(BorgBaseClient.REPO_LIST, apiKey=apiKey)
    if 'errors' in repos:
        readResult['success'] = False
        for error in repos['errors']:
            readResult['errors'].append(error['message'])
    else:
        for repo in repos['data']['repoList']:
            readResult['repos'].append(repo)

    return readResult


def addRepo(repoParams, apiKey=None):
    addResult = dict(
        success=True,
        errors=[]
    )

    repo = client.execute(BorgBaseClient.REPO_ADD, repoParams, apiKey=apiKey)

    if 'errors' in repo:
        addResult['success'] = False
        for error in repo['errors']:
            addResult['errors'].append(error['message'])
    else:
        addResult['repoID'] = repo['data']['repoAdd']['repoAdded']['id']

    return addResult


def editRepo(repoParams, apiKey=None):
    editResult = dict(
        success=True,
        errors=[]
    )

    repo = client.execute(BorgBaseClient.REPO_EDIT, repoParams, apiKey=apiKey)

    if 'errors' in repo:
        editResult['success'] = False
        for error in repo['errors']:
            editResult['errors'].append(error['message'])

    return editResult


def deleteRepo(id, apiKey=None):
    deleteResult = dict(
        success=True,
        errors=[]
    )

    result = client.execute(BorgBaseClient.REPO_DELETE, dict(id=id), apiKey=apiKey)
    if 'errors' in result:
        deleteResult['success'] = False
        for error in result['errors']:
            deleteResult['errors'].append(error['message'])

    return deleteResult


def findRepo(repos, name):
    for repo in repos:
        if name == repo['name']:
            return repo

    return None


def stringListToIntList(list):
    return [int(s) for s in list]


def reposMatch(repo1, repo2):
    if repo1['quotaEnabled'] and repo2['quotaEnabled']:
        if repo1['quota'] != repo2['quota']:
            return False

    return repo1['quotaEnabled'] == repo2['quotaEnabled'] and \
        repo1['appendOnly'] == repo2['appendOnly'] and \
        stringListToIntList(repo1['appendOnlyKeys']) == stringListToIntList(repo2['appendOnlyKeys']) and \
        stringListToIntList(repo1['fullAccessKeys']) == stringListToIntList(repo2['fullAccessKeys']) and \
        repo1['alertDays'] == repo2['alertDays'] and \
        repo1['region'] == repo2['region'] and \
        repo1['borgVersion'] == repo2['borgVersion']


def runModule():
    borgbaseVersions = {
        'latest': 'LATEST',
        '1.1.x': 'V_1_1_X',
        '1.2.x': 'V_1_2_X'
    }

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        email=dict(type='str', default=None),
        password=dict(type='str', default=None, no_log=True),
        apikey=dict(type='str', default=None, no_log=True),
        state=dict(type='str', required=False, choices=['absent', 'present'], default='present'),
        alert_days=dict(type='int', required=False, default=7),
        append_only=dict(type='bool', required=False, default=False),
        append_only_keys=dict(type='list', elements='int', required=False, default=[], no_log=False),
        borg_version=dict(type='str', required=False, choices=list(borgbaseVersions.keys()), default='latest'),
        full_access_keys=dict(type='list', elements='int', required=False, no_log=False),
        name=dict(type='str', required=True),
        quota=dict(type='int', required=False),
        quota_enabled=dict(type='bool', required=False, default=False),
        region=dict(type='str', required=False, choices=['us', 'eu'], default='eu'),
    )

    required_if = [
        ('quota_enabled', True, ['quota']),
    ]

    required_one_of = [
        ('email', 'apikey'),
        ('full_access_keys', 'append_only_keys')
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
        required_if=required_if,
        required_one_of=required_one_of,
        required_together=required_together,
        mutually_exclusive=mutually_exclusive,
    )

    stateExists = (module.params['state'] == 'present')

    if module.params['email'] and module.params['password']:
        loginResult = login(module.params['email'], module.params['password'])

    if (module.params['apikey'] and (not module.params['email'] and not module.params['password'])) or loginResult['success']:
        # Get a list of keys in the account

        repos = readRepos(apiKey=module.params['apikey'])

        if repos['success']:
            newParams = dict(
                name=module.params['name'],
                quota=module.params['quota'] if module.params['quota'] else "0",
                quotaEnabled=module.params['quota_enabled'],
                appendOnly=module.params['append_only'],
                appendOnlyKeys=module.params['append_only_keys'],
                fullAccessKeys=module.params['full_access_keys'],
                alertDays=module.params['alert_days'],
                region=module.params['region'],
                borgVersion=borgbaseVersions[module.params['borg_version']],
            )

            foundRepo = findRepo(repos['repos'], module.params['name'])
            if foundRepo:
                newParams['id'] = foundRepo['id']

                result['repo_id'] = foundRepo['id']

                if stateExists:
                    if not reposMatch(newParams, foundRepo):
                        result['changed'] = True

                        if not module.check_mode:
                            editResult = editRepo(newParams, apiKey=module.params['apikey'])

                            if not editResult['success']:
                                result['msg'] = ''

                                for error in editResult['errors']:
                                    result['msg'] += error

                                module.fail_json(**result)
                else:
                    result['changed'] = True

                    if not module.check_mode:
                        deleteResult = deleteRepo(foundRepo['id'], apiKey=module.params['apikey'])
                        if not deleteResult['success']:
                            result['msg'] = ''

                            for error in deleteResult['errors']:
                                result['msg'] += error

                            module.fail_json(**result)
            else:
                if stateExists:
                    result['changed'] = True
                    if not module.check_mode:
                        addResult = addRepo(newParams, apiKey=module.params['apikey'])

                        if addResult['success']:
                            result['repo_id'] = addResult['repoID']
                        else:
                            result['msg'] = ''

                            for error in addResult['errors']:
                                result['msg'] += error

                            module.fail_json(**result)
        else:
            result['msg'] = ''

            for error in repos['errors']:
                result['msg'] += error

            module.fail_json(**result)
    else:
        result['msg'] = ''

        for error in loginResult['errors']:
            result['msg'] += error

        module.fail_json(**result)

    module.exit_json(**result)


def main():
    runModule()


if __name__ == '__main__':
    main()
