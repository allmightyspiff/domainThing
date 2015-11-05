base:
  '*':
    - vim
    - unbound
  'host:domain-master':
    - match: grain
    - python
    - mysql
    - rabbitmq.latest
    - elk
