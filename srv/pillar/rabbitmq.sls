rabbitmq:
  plugin:
    rabbitmq_management:
      - enabled

  user:
    domainThing:
      - password: thisDomainThingy
      - force: True
      - tags: monitoring, user
      - perms:
        - '/':
          - '.*'
          - '.*'
          - '.*'
      - runas: root

  config:
    - username: domainThing
    - password: thisDomainThingy
    - host: domain-master-private.lablayer.info

