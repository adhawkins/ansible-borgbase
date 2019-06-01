#!/usr/bin/python

from pprint import pprint

ANSIBLE_METADATA = {
		'metadata_version': '1.1',
		'status': ['preview'],
		'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: borgbase_sshkeys

short_description: Module for managing SSH keys in borgbase.

version_added: "2.4"

description:
		- "Module for managing SSH keys in borgbase."

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
						- 'present' to ensure the key exists, 'absent' to ensure it doesn't. When removing key
						match is carried out based on key name only.
				default: present
				choices: [ absent, present ]
		name:
				description:
						- The SSH key name
				required: true
		key:
				description:
						- The SSH public key (required if state is 'present')
				required: false

author:
		- Andy Hawkins (@adhawkinsgh)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
	my_new_test_module:
		name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
	my_new_test_module:
		name: hello world
		new: true

# fail the module
- name: Test failure of the module
	my_new_test_module:
		name: fail me
'''

RETURN = '''
key_id:
		description: The ID of the key that was created or deleted
		type: int
		returned: always
'''

from ansible.module_utils.basic import AnsibleModule

REQUESTS_IMP_ERR = None
try:
		import requests
		HAS_REQUESTS = True
except:
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

SSH_LIST = '''
query data {
	sshList {
		id
		name
		keyData
	}
}
'''

SSH_ADD = '''
mutation sshAdd(
	$name: String!
	$keyData: String!
	) {
		sshAdd(
			name: $name
			keyData: $keyData
		) {
			keyAdded {
				id
				name
				hashMd5
				keyType
				bits
			}
		}
}
'''

SSH_DELETE = '''
mutation sshDelete($id: Int!) {
  sshDelete(id: $id) {
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

def readKeys():
	readResult=dict(
			success=True,
			errors=[],
			keys=[]
		)

	keys = client.execute(SSH_LIST)
	if 'errors' in res:
		readResult['success']=False
		for error in res['errors']:
			readResult['errors'].append(error['message'])
	else:
		for key in keys['data']['sshList']:
			readResult['keys'].append(key)

	return readResult

def addKey(name, key):
	addResult=dict(
			success=True,
			errors=[]
		)

	key = client.execute(SSH_ADD, dict(name=name, keyData=key))

	if 'errors' in key:
		addResult['success']=False
		for error in key['errors']:
			addResult['errors'].append(error['message'])
	else:
		addResult['keyID']=key['data']['sshAdd']['keyAdded']['id']

	return addResult

def deleteKey(id):
	deleteResult=dict(
			success=True,
			errors=[]
		)

	result = client.execute(SSH_DELETE, dict(id=id))
	if 'errors' in result:
		deleteResult['success']=False
		for error in result['errors']:
			deleteResult['errors'].append(error['message'])

	return deleteResult

def findKey(keys, name):
	for key in keys:
		if name ==key['name']:
			return key

	return None

def runModule():
		# define available arguments/parameters a user can pass to the module
		module_args = dict(
				email=dict(type='str', required=True),
				password=dict(type='str', required=True, no_log=True),
				state=dict(type='str', required=False, choices=['absent', 'present'], default='present'),
				name=dict(type='str', required=True),
				key=dict(type='str', required=False)
		)

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
				supports_check_mode=True
		)

		stateExists= module.params['state']=='present'
		# Get a list of keys in the account

		loginResult = login(module.params['email'], module.params['password'])
		if loginResult['success']:
			keys = readKeys()

			if keys['success']:
				foundKey = findKey(keys['keys'], module.params['name'])
				keyExists = foundKey != None
				if keyExists:
					result['key_id']=int(foundKey['id'])

				result['changed']=keyExists!=stateExists

				if keyExists != stateExists and not module.check_mode:
					if stateExists:
						addResult = addKey(module.params['name'], module.params['key'])
						if addResult['success']:
							result['key_id']=addResult['keyID']
						else:
							result['msg']=''

							for error in addResult['errors']:
								result['msg']+=error

							module.fail_json(**result)
					else:
						deleteResult = deleteKey(int(foundKey['id']))
						if not deleteResult['success']:
							result['msg']=''

							for error in deleteResult['errors']:
								result['msg']+=error

							module.fail_json(**result)

				module.exit_json(**result)
			else:
				result['msg']=''

				for error in keys['errors']:
					result['msg']+=error

				module.fail_json(**result)
		else:
			result['msg']=''

			for error in loginResult['errors']:
				result['msg']+=error

			module.fail_json(**result)

def main():
	if not HAS_REQUESTS:
			module.fail_json(msg=missing_required_lib("requests"),
										 exception=LIB_REQUESTS_ERR)

	runModule()

if __name__ == '__main__':
		main()
