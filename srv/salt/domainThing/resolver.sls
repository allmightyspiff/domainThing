resolverServiceFile:
  file.managed:
    - name: '/etc/init.d/domainResolver'
    - source: salt://domainThing/domainResolver.sh

domainResolverFile:
  file.managed:
    - name: '/domainThing/domainResolver2.py'
    - mode: 

