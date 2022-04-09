# Ansible Collection - adhawkins.borgbase

This repo hosts the `adhawkins.borgbase` Ansible Collection.

The collection includes modules for managing SSH keys and repositories on the [BorgBase](https://www.borgbase.com/) service.

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the collection, you need to install the collection with the `ansible-galaxy` CLI:

`ansible-galaxy collection install adhawkins.borgbase`

You can also include it in a `requirements.yml` file and install it through `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
- name: adhawkins.borgbase
```

### Playbooks

To use a module from the collection, please reference the full namespace, collection name, and module name that you want to use:

```yaml
---
- hosts: all

  tasks:
    - name: Read key from file
      slurp:
        src: ~/.ssh/id_rsa.pub
      register: ssh_key
      check_mode: yes

    - name: Create key
      adhawkins.borgbase.borgbase_ssh:
        state: present
        apikey: "{{ borgbase_email }}"
        name: "ANSIBLE-1"
        key: "{{ ssh_key['content'] | b64decode }}"
      register: borgbase_key

    - name: Dump create results
      debug:
        var: borgbase_key.key_id
```

Or you can add the full namespace and collection name in the `collections` element:

```yaml
---
- hosts: all

  collections:
    - adhawkins.borgbase

  tasks:
    - name: Read key from file
      slurp:
        src: ~/.ssh/id_rsa.pub
      register: ssh_key
      check_mode: yes

    - name: Create key
      borgbase_ssh:
        state: present
        apikey: "{{ borgbase_email }}"
        name: "ANSIBLE-1"
        key: "{{ ssh_key['content'] | b64decode }}"
      register: borgbase_key

    - name: Dump create results
      debug:
        var: borgbase_key.key_id
```

### Usage

See the collection docs:

* [adhawkins.borgbase collection docs](https://adhawkins.github.io/ansible-borgbase/)

## License

GNU General Public License v3.0 or later
