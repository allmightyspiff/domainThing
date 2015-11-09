python-pip:
  pkg:
    - installed

netaddr:
  pip.installed:
    - require:
      - pkg: python-pip

pika:
  pip.installed:
    - require:
      - pkg: python-pip

multiprocessing:
  pip.installed:
    - require:
      - pkg: python-pip


mysql-connector-python:
  pip.installed:
    - require:
      - pkg: python-pip
    - allow_external: mysql-connector-python


elasticsearch:
  pip.installed:
    - require:
      - pkg: python-pip

configparser:
  pip.installed:
    - require:
      - pkg: python-pip
