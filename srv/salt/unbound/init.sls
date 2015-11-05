
unbound:
  pkg.installed:
    - name: unbound
  service.running:
    - name: unbound
    - enable: True
    - watch:
      - pkg: unbound

unbound_config:
  file.managed:
    - name: /etc/unbound/unbound.conf
    - source: salt://unbound/unbound.conf
    - watch_in:
      - service: unbound
    - user: root
    - group: root
    - mode: 644

unbound_named_root:
  file.managed:
    - name: /etc/unbound/named.root
    - source: salt://unbound/named.root
    - watch_in:
      - service: unbound
    - user: root
    - group: root
    - mode: 644

resolve_conf:
  file.managed:
    - name: /etc/resolv.conf
    - source: salt://unbound/resolv.conf
    - watch_in:
      - service: unbound
    - user: root
    - group: root
    - mode: 644
