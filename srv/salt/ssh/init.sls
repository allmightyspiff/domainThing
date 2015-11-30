christopher_keys:
  ssh_auth.present:
    - user: root
    - source: salt://ssh/keys
    - config: %h/.ssh/authorized_keys