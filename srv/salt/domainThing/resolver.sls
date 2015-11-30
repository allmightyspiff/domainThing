resolverServiceFile:
  file.managed:
    - name: '/etc/init.d/domainResolver'
    - source: salt://domainThing/domainResolver.sh


resolverServiceRunner:
  service.running:
    - name: domainResolver
    - require: 
      - pkg: git_domainThing


