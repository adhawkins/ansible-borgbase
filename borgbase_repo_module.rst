.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-entry
.. role:: ansible-option-default
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.adhawkins.borgbase.borgbase_repo_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

adhawkins.borgbase.borgbase_repo module -- Module for managing repos in borgbase.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `adhawkins.borgbase collection <https://galaxy.ansible.com/adhawkins/borgbase>`_ (version 1.0.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install adhawkins.borgbase`.

    To use it in a playbook, specify: :code:`adhawkins.borgbase.borgbase_repo`.

.. version_added

.. versionadded:: 2.4 of adhawkins.borgbase

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Module for managing repos in borgbase.


.. Aliases


.. Requirements


.. Options

Parameters
----------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-alert_days"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-alert_days:

      .. rst-class:: ansible-option-title

      **alert_days**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-alert_days" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Number of days to send alerts if no activity detected.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-apikey"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-apikey:

      .. rst-class:: ansible-option-title

      **apikey**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-apikey" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The borgbase API key.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-append_only"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-append_only:

      .. rst-class:: ansible-option-title

      **append_only**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-append_only" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      True if repo is append only.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-append_only_keys"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-append_only_keys:

      .. rst-class:: ansible-option-title

      **append_only_keys**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-append_only_keys" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of keys for append only access.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-borg_version"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-borg_version:

      .. rst-class:: ansible-option-title

      **borg_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-borg_version" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Version of borg to run on this repo.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`latest`
      - :ansible-option-choices-entry:`1.1.x`
      - :ansible-option-choices-entry:`1.2.x`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-email"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-email:

      .. rst-class:: ansible-option-title

      **email**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-email" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The email address associated with the borgbase account.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-full_access_keys"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-full_access_keys:

      .. rst-class:: ansible-option-title

      **full_access_keys**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-full_access_keys" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of keys for full access.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Repo name.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The password for the borgbase account.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-quota"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-quota:

      .. rst-class:: ansible-option-title

      **quota**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-quota" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Disk quota for this repo (MB).


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-quota_enabled"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-quota_enabled:

      .. rst-class:: ansible-option-title

      **quota_enabled**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-quota_enabled" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Whether quota is enabled for this repo.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-region"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-region:

      .. rst-class:: ansible-option-title

      **region**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-region" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Repo region.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`eu` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`us`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      'present' to ensure the repo exists, 'absent' to ensure it doesn't.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`absent`
      - :ansible-option-default-bold:`present` :ansible-option-default:`← (default)`

      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
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




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-repo_id"></div>

      .. _ansible_collections.adhawkins.borgbase.borgbase_repo_module__return-repo_id:

      .. rst-class:: ansible-option-title

      **repo_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-repo_id" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The ID of the repo that was created or deleted.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Andy Hawkins (@adhawkinsgh)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="http://example.com/issue/tracker" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="http://example.com" aria-role="button" target="_blank" rel="noopener external">Homepage</a>
    <a href="http://github.com/adhawkins/ansible-borgbase" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

