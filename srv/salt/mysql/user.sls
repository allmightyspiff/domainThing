{% set mysql_root_user = salt['pillar.get']('mysql:server:root_user', 'root') %}
{% set mysql_root_pass = salt['pillar.get']('mysql:server:root_password', salt['grains.get']('server_id')) %}
{% set mysql_user = salt['pillar.get']('mysql:server:user', 'domains') %}
{% set mysql_user_password = salt['pillar.get']('mysql:server:user_password', salt['grains.get']('server_id')) %}


include:
  - mysql.python

domains:
  mysql_user.present:
    - host: 10.%
    - password: {{ mysql_user_password }}
    - connection_user: {{ mysql_root_user }}
    - connection_pass: {{ mysql_root_pass }}

domainThing_grant:
  mysql_grants.present:
    - grant: all privileges
    - database: domainThing.*
    - user: domains
    - host: 10.%
    - password: {{ mysql_user_password }}
    - connection_user: {{ mysql_root_user }}
    - connection_pass: {{ mysql_root_pass }}
