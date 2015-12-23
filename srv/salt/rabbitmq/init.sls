include:
  - rabbitmq.install
  - rabbitmq.config

rabbit_config:
  file.managed:
    - name: /etc/rabbitmq/rabbitmq.config
    - source: salt://rabbitmq/rabbit.config
    - mode: 644
    - user: root
    - group: root
