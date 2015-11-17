etc_salt_maps:
  file.managed:
    - name: /etc/salt/cloud.maps.d/bigMap.conf
    - template: jinja
    - source: salt://salt-cloud/cloud.map.d/bigMap.sls
    - makedirs: True