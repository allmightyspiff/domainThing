base:
  'host:domain-master':
    - match: grain
    - mysql
    - rabbitmq
    - softlayer
    - cloud-profiles
    - elasticsearch
  'roles:resolver':
    - match: grain
    - rabbitmq
    - mysql
    - elasticsearch
  'roles:parser':
    - match: grain
    - rabbitmq
    - mysql
    - elasticsearch
  'roles:consumer':
    - match: grain
    - rabbitmq
    - mysql
    - elasticsearch
