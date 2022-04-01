from ansible.module_utils.urls import Request

import json

class BorgBaseClient:
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
  $id: String!
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

	def __init__(self, endpoint='https://api.borgbase.com/graphql'):
		self.endpoint = endpoint
		self.session = Request()

	def login(self, **kwargs):
		return self._send(self.LOGIN, kwargs)

	def execute(self, query, variables=None):
		return self._send(query, variables)

	def _send(self, query, variables):
		data = {'query': query,
				'variables': variables}

		headers = {'Accept': 'application/json',
				'Content-Type': 'application/json'}

		request = self.session.open('POST', self.endpoint, data=json.dumps(data), headers=headers)

		if request.getcode() != 200:
			raise Exception("Query failed to run by returning code of {}. {}".format(request.getcode(), query))

		return json.loads(request.read())
