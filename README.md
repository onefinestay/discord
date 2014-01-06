Discord
=======

Discord is a tool for determining dependency version conflicts in complex
Python projects.

Installation
------------

pip install --upgrade git+https://github.com/onefinestay/discord.git

Usage
-----

Discord scans a requirements file and checks out and inspects all packages
required by this file and all subpackages recursively.

```bash
$ python -m discord <requirements_file>
```

If no requirements file is specified, the script will look for a a file called
`requirements.txt` in the current directory.

Verbose mode can be enabled by adding a `-v` switch before or after the file
name.

Example output
--------------

```
Mako
    0.9.0 is required by <requirements.txt>
    0.9.1 is required by alembic 0.6.0
SQLAlchemy
    0.8.1 is required by taal 0.4.2
    0.8.3 is required by nameko 1.1.2, <requirements.txt>
    0.9.1 is required by alembic 0.6.0
six
    1.4.1 is required by <requirements.txt>
    1.5.1 is required by python-dateutil 2.1
iso8601
    0.1.4 is required by kaiso 0.13.4
    0.1.8 is required by nameko 1.1.2, <requirements.txt>
lxml
    3.2.4 is required by <requirements.txt>
    3.2.5 is required by premailer 1.13
ipython
    0.13.1 is required by <requirements.txt>
    1.1.0 is required by jira-python 0.12
requests
    0.14.2 is required by <requirements.txt>
    2.1.0 is required by mandrill 1.0.51, jira-python 0.12, kaiso 0.13.4
```

