sjc01:
  - parser-00:
      minion:
        mine_functions:
          network.ip_addrs:
            interface: eth0
        grains:
          roles: parser
