my-softlayer:
    # Set up the location of the salt master
    minion:
      master: {{  salt['pillar.get']('softlayer:master')  }}

    user: {{  salt['pillar.get']('softlayer:user')  }}
    apikey: {{  salt['pillar.get']('softlayer:password')  }}

    provider: softlayer