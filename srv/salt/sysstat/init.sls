sysstat:
  pkg: 
    - installed
  service.running:
    - enabled: True
    - watch:
      - file: /etc/default/sysstat

/etc/default/sysstat:
  file.managed:
    - source: salt://sysstat/sysstat
    - mode: 644
    - user: root
    - group: root