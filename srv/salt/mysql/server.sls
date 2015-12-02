# See https://github.com/saltstack-formulas/mysql-formula for a more OS generic config

{% set mysql_root_user = salt['pillar.get']('mysql:server:root_user', 'root') %}
{% set mysql_root_password = salt['pillar.get']('mysql:server:root_password', salt['grains.get']('server_id')) %}
{% set mysql_user = salt['pillar.get']('mysql:server:user', 'domains') %}
{% set mysql_user_password = salt['pillar.get']('mysql:server:user_password', salt['grains.get']('server_id')) %}

mysql_debconf_utils:
  pkg.installed:
    - name: debconf-utils

mysql_debconf:
  debconf.set:
    - name: mysql-server
    - data:
        'mysql-server/root_password': {'type': 'password', 'value': '{{ mysql_root_password }}'}
        'mysql-server/root_password_again': {'type': 'password', 'value': '{{ mysql_root_password }}'}
        'mysql-server/start_on_boot': {'type': 'boolean', 'value': 'true'}
    - require_in:
      - pkg: mysqld
    - require:
      - pkg: mysql_debconf_utils

mysql_root_password:
  cmd.run:
    - name: mysql -u root -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('{{ mysql_root_password}}');"
    - unless: mysql --user {{ mysql_root_user }} --password='{{ mysql_root_password}}' --execute="SELECT 1;"
    - require:
      - service: mysqld

mysqld:
  pkg.installed:
    - name: mysql-server
    - require:
      - debconf: mysql_debconf
  service.running:
    - name: mysql
    - enable: True
    - watch:
      - pkg: mysql-server

mysql_config:
  file.managed:
    - name: /etc/mysql/my.cnf
    - template: jinja
    - source: salt://mysql/my.cnf
    - watch_in:
      - service: mysql
    - user: root
    - group: root
    - mode: 644


# Only gets run with mysql_config is changed
cleanup_innodb_log:
  cmd.run:
    - name: rm -f /var/lib/mysql/ib_logfile*
    - prereq:
      - file: mysql_config

mysql_additional_config:
  file.managed:
    - name: /usr/my.cnf
    - source: salt://mysql/usr-my.cnf
    - create: False
    - watch_in:
      - service: mysql
