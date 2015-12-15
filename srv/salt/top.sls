base:
  '*':
    - vim
    - unbound
    - domainThing
    - python
    - ssh
    - sysstat
  'host:domain-master':
    - match: grain
    - mysql
    - rabbitmq.latest
    - elk
    - salt-cloud
    - reactor
  'roles:resolver':
    - match: grain
    - domainThing/resolver
  'roles:consumer':
    - match: grain
    - domainThing/consumer
  'roles:parser':
    - match: grain
    - domainThing/parser

  'roles:rabbit':
    - match: grain
    - rabbitmq.latest
