rabbitmq:
  plugin:
    rabbitmq_management:
      - enabled
  policy:
    rabbitmq_policy:
      - name: HA
      - pattern: '.*'
      - definition: '{"ha-mode": "all"}'
  vhost:
    virtual_host:
      - owner: rabbit_user
      - conf: .*
      - write: .*
      - read: .*
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

