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
    - reactor
    - domainThing/parser
  'roles:resolver':
    - match: grain
    - domainThing/resolver
  'roles:consumer':
    - match: grain
    - domainThing/consumer

    