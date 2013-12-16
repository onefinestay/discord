Discord
=======

Discord is a tool for determining dependency version conflicts in complex
Python projects.

Installation
------------


Usage
-----

Discord scans a requirements file and checks out and inspects all packages
required by this file and all subpackages recursively.

$ python -m discord \<requirements_file\>

If no requirements file is specified, the script will look for a a file called
`requirements.txt` in the current directory.

Example output
--------------

ipython
    0.13.1 is required by local requirements
    1.1.0 is required by jira-python 0.12
SQLAlchemy
    0.8.1 is required by taal 0.4.2
    0.8.3 is required by nameko 1.1.2, local requirements
    0.8.4 is required by alembic 0.6.0
lxml
    3.2.4 is required by local requirements
    3.3 is required by premailer 1.13
requests
    0.14.2 is required by local requirements
    2.1.0 is required by jira-python 0.12, mandrill 1.0.51, kaiso 0.13.3
iso8601
    0.1.4 is required by kaiso 0.13.3
    0.1.8 is required by nameko 1.1.2, local requirements

