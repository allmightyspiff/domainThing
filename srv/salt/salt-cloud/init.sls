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
