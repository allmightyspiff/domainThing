resolverServiceFile:
  file.managed:
    - name: '/etc/init.d/domainResolver'
    - source: salt://domainThing/domainResolver.sh
    - mode: 755


resolverServiceRunner:
  service.running:
    - name: domainResolver
    - require: 
      - git: git_domainThing


