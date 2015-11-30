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
  'role:resolver':
    - match: grain
    - domainThing/resolver