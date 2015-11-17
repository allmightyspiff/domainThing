base:
  '*':
    - vim
    - unbound
    - domainThing
    - python
  'host:domain-master':
    - match: grain
    - mysql
    - rabbitmq.latest
    - elk
    - salt-cloud