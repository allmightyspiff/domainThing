{% set kibana_wwwroot = '/opt/kibana' %}

include:
  - java

elastic_repo:
  pkgrepo.managed:
    - humanname: Elastic Search
    - name: deb http://packages.elastic.co/elasticsearch/2.x/debian stable main
    - file: /etc/apt/sources.list.d/elasticsearch.list
    - key_url: https://packages.elastic.co/GPG-KEY-elasticsearch
    - require_in:
      - pkg: elasticsearch


elasticsearch_pkg:
  pkg.installed:
    - name: elasticsearch
  service:
    - name: elasticsearch
    - running
    - enable: True
    - watch:
      - pkg: elasticsearch


elastic_conf:
  file.managed:
    - name: '/etc/elasticsearch/elasticsearch.yml'
    - contents: |+
          network.bind_host: {{ salt['network.interfaces']()['bond0']['inet'][0]['address'] }}
    - mode: 644
    - watch_in:
      - service: elasticsearch

kibana_static_dir:
  file.directory:
    - name: {{ kibana_wwwroot }}
    - user: www-data
    - group: www-data
    - makedirs: True

kibana:
  archive.extracted:
    - name: {{ kibana_wwwroot }}
    - if_missing: {{ kibana_wwwroot }}/kibana-4.2.0-linux-x64
    - source_hash: md5=51a5c6fc955636b817ec99bf6ec86c90
    - source: https://download.elastic.co/kibana/kibana/kibana-4.2.0-linux-x64.tar.gz
    - archive_format: tar
    - tar_options: xf
