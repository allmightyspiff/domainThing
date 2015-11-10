base:
  '*':
    - vim
    - unbound
    - domainThing
  'host:domain-master':
    - match: grain
    - python
    - mysql
    - rabbitmq.latest
    - elk
    - salt-cloud