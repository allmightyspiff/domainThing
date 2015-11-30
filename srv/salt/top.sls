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
  'role:resolver':
    - match: grain
    - domainThing/resolver