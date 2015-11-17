python-pip:
  pkg:
    - installed

python-dev:
  pkg.installed: []

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
      - pkg: python-dev


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

softlayer:
  pip.installed:
    - require:
      - pkg: python-pip

requests:
  pip.installed:
    - name: requests =2.5.3
    - require:
      - pkg: python-pip

