#!/usr/bin/python

from pprint import pprint

ANSIBLE_METADATA = {
		'metadata_version': '1.1',
		'status': ['preview'],
		'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: borgbase_repo

short_description: Module for managing repos in borgbase.

version_added: "2.4"

description:
		- "Module for managing repos in borgbase."

options:
		email:
				description:
						- The email address associated with the borgbase account
				required: true
		password:
				description:
						- The password for the borgbase account
				required: true
		state:
				description:
						- 'present' to ensure the repo exists, 'absent' to ensure it doesn't.
				default: present
				choices: [ absent, present ]
		alert_days:
				description:
						- Number of days to send alerts if no activity detected
				required: false
		append_only:
				description:
						- True if repo is append only
				required: false
		append_only_keys:
				description:
						- List of keys for append only access
				required: false
		borg_version:
				description:
						- Version of borg to run on this repo
				required: false
		full_access_keys:
				description:
						- List of keys for full access
				required: true
		name:
				description:
						- Repo name
				required: true
		quota:
				description:
						- Disk quota for this repo (MB)
				required: false
		quota_enabled:
				description:
						- Whether quota is enabled for this repo
				required: false
		region:
				description:
						- Repo region
				choices: [ eu, us ]
				required: false
				default: eu
author:
		- Andy Hawkins (@adhawkinsgh)
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
		description: The ID of the repo that was created or deleted
		type: int
		returned: always
'''

from ansible.module_utils.basic import AnsibleModule

REQUESTS_IMP_ERR = None
try:
	import requests
	HAS_REQUESTS = True
except:
	import traceback

	HAS_REQUESTS = False
	REQUESTS_IMP_ERR = traceback.format_exc()

LOGIN = '''
mutation login(
	$email: String!
	$password: String!
	$otp: String
	) {
		login(
			username: $email
			password: $password
			otp: $otp
		) {
			user {
				id
			}
		}
}
'''

REPO_LIST = '''
query repoList {
	repoList {
		id
		name
		quota
		quotaEnabled
		alertDays
		region
		borgVersion
		appendOnly
		appendOnlyKeys
		fullAccessKeys
	}
}
'''

REPO_ADD = '''
mutation repoAdd(
  $name: String
  $quota: Int
  $quotaEnabled: Boolean
  $appendOnlyKeys: [String]
  $fullAccessKeys: [String]
  $alertDays: Int
  $region: String
  $borgVersion: String
  ) {
    repoAdd(
      name: $name
      quota: $quota
      quotaEnabled: $quotaEnabled
      appendOnlyKeys: $appendOnlyKeys
      fullAccessKeys: $fullAccessKeys
      alertDays: $alertDays
      region: $region
      borgVersion: $borgVersion
    ) {
      repoAdded {
        id
        name
      }
    }
}
'''

REPO_EDIT = '''
mutation repoEdit(
  $id: String
  $name: String
  $quota: Int
  $quotaEnabled: Boolean
  $appendOnlyKeys: [String]
  $fullAccessKeys: [String]
  $alertDays: Int
  $region: String
  $borgVersion: String
  ) {
    repoEdit(
      id: $id
      name: $name
      quota: $quota
      quotaEnabled: $quotaEnabled
      appendOnlyKeys: $appendOnlyKeys
      fullAccessKeys: $fullAccessKeys
      alertDays: $alertDays
      region: $region
      borgVersion: $borgVersion
    ) {
      repoEdited {
        id
        name
      }
    }
}
'''

REPO_DELETE = '''
mutation repoDelete($id: String!) {
  repoDelete(id: $id) {
    ok
  }
}
'''

class GraphQLClient:
	def __init__(self, endpoint='https://api.borgbase.com/graphql'):
		self.endpoint = endpoint
		self.session = requests.session()

	def login(self, **kwargs):
		return self._send(LOGIN, kwargs)

	def execute(self, query, variables=None):
		return self._send(query, variables)

	def _send(self, query, variables):
		data = {'query': query,
										'variables': variables}
		headers = {'Accept': 'application/json',
												 'Content-Type': 'application/json'}

		request = self.session.post(self.endpoint, json=data, headers=headers)
		if request.status_code != 200:
			raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

		return request.json()

client = GraphQLClient()

def login(email, password):
	loginResult=dict(
			success=True,
			errors=[]
		)

	res = client.login(email=email, password=password)
	if 'errors' in res:
		loginResult['success']=False
		for error in res['errors']:
			loginResult['errors'].append(error['message'])

	return loginResult

def readRepos():
	readResult=dict(
			success=True,
			errors=[],
			repos=[]
		)

	repos = client.execute(REPO_LIST)
	if 'errors' in repos:
		readResult['success']=False
		for error in repos['errors']:
			readResult['errors'].append(error['message'])
	else:
		for repo in repos['data']['repoList']:
			readResult['repos'].append(repo)

	return readResult

def addRepo(repoParams):
	addResult=dict(
			success=True,
			errors=[]
		)

	repo = client.execute(REPO_ADD, repoParams)

	if 'errors' in repo:
		addResult['success']=False
		for error in repo['errors']:
			addResult['errors'].append(error['message'])
	else:
		addResult['repoID']=repo['data']['repoAdd']['repoAdded']['id']

	return addResult

def editRepo(repoParams):
	editResult=dict(
			success=True,
			errors=[]
		)

	repo = client.execute(REPO_EDIT, repoParams)

	if 'errors' in repo:
		editResult['success']=False
		for error in key['errors']:
			editResult['errors'].append(error['message'])

	return editResult

def deleteRepo(id):
	deleteResult=dict(
			success=True,
			errors=[]
		)

	result = client.execute(REPO_DELETE, dict(id=id))
	if 'errors' in result:
		deleteResult['success']=False
		for error in result['errors']:
			deleteResult['errors'].append(error['message'])

	return deleteResult

def findRepo(repos, name):
	for repo in repos:
		if name ==repo['name']:
			return repo

	return None

def stringListToIntList(list):
	return [int(s) for s in list]

def reposMatch(repo1, repo2):
	if repo1['quotaEnabled'] and repo2['quotaEnabled']:
		if repo1['quota']!=repo2['quota']:
			return False

	return repo1['quotaEnabled']==repo2['quotaEnabled'] and \
		repo1['appendOnly']==repo2['appendOnly'] and \
		stringListToIntList(repo1['appendOnlyKeys'])==stringListToIntList(repo2['appendOnlyKeys']) and \
		stringListToIntList(repo1['fullAccessKeys'])==stringListToIntList(repo2['fullAccessKeys']) and \
		repo1['alertDays']==repo2['alertDays'] and \
		repo1['region']==repo2['region'] and \
		repo1['borgVersion']==repo2['borgVersion']

def runModule():
		# define available arguments/parameters a user can pass to the module
		module_args = dict(
				email=dict(type='str', required=True),
				password=dict(type='str', required=True, no_log=True),
				state=dict(type='str', required=False, choices=['absent', 'present'], default='present'),
				alert_days=dict(type='int', required=False, default=7),
				append_only=dict(type='bool', required=False, default=False),
				append_only_keys=dict(type='list', required=False, default=[]),
				borg_version=dict(type='str', required=False, choices=['LATEST', '1.1.x'], default='LATEST'),
				full_access_keys=dict(type='list', required=True),
				name=dict(type='str', required=True),
				quota=dict(type='int', required=False),
				quota_enabled=dict(type='bool', required=False, default=False),
				region=dict(type='str', required=False, choices=['us', 'eu'], default='eu'),
		)

		required_if = [
			[ 'quota_enabled', True, ['quota']],
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
				required_if=required_if
		)

		stateExists= module.params['state']=='present'
		# Get a list of keys in the account

		loginResult = login(module.params['email'], module.params['password'])
		if loginResult['success']:
			repos = readRepos()

			if repos['success']:
				newParams = dict(
					  name=module.params['name'],
					  quota=module.params['quota'],
					  quotaEnabled=module.params['quota_enabled'],
					  appendOnly=module.params['append_only'],
					  appendOnlyKeys=module.params['append_only_keys'],
					  fullAccessKeys=module.params['full_access_keys'],
					  alertDays=module.params['alert_days'],
					  region=module.params['region'],
					  borgVersion=module.params['borg_version'],
					)

				foundRepo=findRepo(repos['repos'], module.params['name'])
				if foundRepo:
					newParams['id']=foundRepo['id']

					result['repo_id']=foundRepo['id']

					if stateExists:
						if not reposMatch(newParams,foundRepo):
							result['changed']=True

							if not module.check_mode:
								editResult = editRepo(newParams)

								if not editResult['success']:
									result['msg']=''

									for error in editResult['errors']:
										result['msg']+=error

									module.fail_json(**result)
					else:
						result['changed']=True

						if not module.check_mode:
							deleteResult = deleteRepo(foundRepo['id'])
							if not deleteResult['success']:
								result['msg']=''

								for error in deleteResult['errors']:
									result['msg']+=error

								module.fail_json(**result)
				else:
					if stateExists:
						result['changed']=True
						if not module.check_mode:
							addResult=addRepo(newParams)

							if addResult['success']:
								result['repo_id']=addResult['repoID']
							else:
								result['msg']=''

								for error in addResult['errors']:
									result['msg']+=error

								module.fail_json(**result)
			else:
				result['msg']=''

				for error in repos['errors']:
					result['msg']+=error

				module.fail_json(**result)
		else:
			result['msg']=''

			for error in loginResult['errors']:
				result['msg']+=error

			module.fail_json(**result)

		module.exit_json(**result)

def main():
	if not HAS_REQUESTS:
		module.fail_json(msg=missing_required_lib("requests"),
									 exception=REQUESTS_IMP_ERR)

	runModule()

if __name__ == '__main__':
		main()
