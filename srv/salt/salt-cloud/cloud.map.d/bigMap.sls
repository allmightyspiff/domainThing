{% for name,location in salt["pillar.get"]("cloud-profiles:datacenters", {}).items() %}
{{ name }}:
  {% for number in range(location.number) %}
  - resolver-{{ name }}-{{ number }}:
      minion:
        mine_functions:
          network.ip_addrs:
            interface: eth0
        grains:
          roles: resolver
  - consumer-{{ name }}-{{ number }}:
      minion:
        mine_functions:
          network.ip_addrs:
            interface: eth0
        grains:
          roles: consumer
  {% endfor %}
{% endfor %}

sjc01-parser:
  - parser-00:
      minion:
        mine_functions:
          network.ip_addrs:
            interface: eth0
        grains:
          roles: parser

dal-09-rabbit:
  - rabbit-01:
      minion:
        mine_functions:
          network.ip_addrs:
            interface: eth0
        grains:
          roles: rabbit

