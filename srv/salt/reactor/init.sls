reactor_conf:
  file.managed:
    - name: '/etc/salt/master.d/reactor.conf'
    - source: salt://reactor/reactor.conf
    - makedirs: True
