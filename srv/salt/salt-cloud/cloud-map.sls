etc_salt_maps:
  file.managed:
    - name: /etc/salt/cloud.maps.d/bigMap.conf
    - template: jinja
    - source: salt://salt-cloud/cloud.map.d/bigMap.sls
    - makedirs: True


etc_salt_maps_parser:
  file.managed:
    - name: /etc/salt/cloud.maps.d/parser.conf
    - source: salt://salt-cloud/cloud.map.d/parser.sls
    - makedirs: True


etc_salt_maps_consumer:
  file.managed:
    - name: /etc/salt/cloud.maps.d/consumer.conf
    - source: salt://salt-cloud/cloud.map.d/consumer.sls
    - makedirs: True