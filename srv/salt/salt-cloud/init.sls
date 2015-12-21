include:
  - salt-cloud.cloud-map



etc_salt_provider:
  file.managed:
    - name: /etc/salt/cloud.providers
    - template: jinja
    - source: salt://salt-cloud/cloud-providers.conf

etc_salt_profiles:
  file.managed:
    - name: /etc/salt/cloud.profiles.d/gen00.conf
    - template: jinja
    - source: salt://salt-cloud/cloud.profiles.d/gen00.conf
    - makedirs: True


etc_salt_profiles_sjc01:
  file.managed:
    - name: /etc/salt/cloud.profiles.d/sjc01-parser.conf
    - template: jinja
    - source: salt://salt-cloud/cloud.profiles.d/sjc01-parser.conf
    - makedirs: True

etc_salt_profiles_rabbit:
  file.managed:
    - name: /etc/salt/cloud.profiles.d/rabbit.conf
    - template: jinja
    - source: salt://salt-cloud/cloud.profiles.d/dal-07-rabbit.conf
    - makedirs: True