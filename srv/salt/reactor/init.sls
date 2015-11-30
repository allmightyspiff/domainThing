reactor_conf:
  file.managed:
    - name: '/etc/salt/master.d/reactor'
    - source: salt://reactor/reactor.conf
