base:
  '*':
    - vim
    - unbound
    - domainThing
    - python
    - ssh
  'host:domain-master':
    - match: grain
    - mysql
    - rabbitmq.latest
    - elk
    - salt-cloud
  'roles:resolver':
    - match: grain
    - domainThing/resolver
  'roles:consumer':
    - match: grain
    - domainThing/consumer
  'roles:parser':
    - match: grain
    - domainThing/parser