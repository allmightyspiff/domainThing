consumerServiceFile:
  file.managed:
    - name: '/etc/init.d/domainConsumer'
    - source: salt://domainThing/domainConsumer.sh


consumerServiceRunner:
  service.running:
    - name: domainConsumer
    - require: 
      - git: git_domainThing
