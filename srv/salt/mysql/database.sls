{% set mysql_root_user = salt['pillar.get']('mysql:server:root_user', 'root') %}
{% set mysql_root_pass = salt['pillar.get']('mysql:server:root_password', salt['grains.get']('server_id')) %}


include:
  - mysql.python

domainThing_db:
  mysql_database.present:
    - name: domainThing
    - connection_host: '127.0.0.1'
    - connection_user: {{ mysql_root_user }}
    - connection_pass: {{ mysql_root_pass }}


domainThing_schema:
  file.managed:
    - name: /etc/mysql/domainThing.schema
    - source: salt://mysql/domainThing.schema
    - user: mysql
    - makedirs: True


domainThing_Load:
  cmd.wait:
    - name: mysql -u {{ mysql_root_user }} -p{{ mysql_root_pass }} domainThing < /etc/mysql/domainThing.schema
    - watch:
      - file: domainThing_schema
      - mysql_database: domainThing
