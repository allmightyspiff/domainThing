sjc01:
  - minion-01:
      minion:
        mine_functions:
          network.ip_addrs:
            interface: eth0
        grains:
          roles: worker
