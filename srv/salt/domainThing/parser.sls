parserServiceFile:
  file.managed:
    - name: '/etc/init.d/domainParser'
    - source: salt://domainThing/domainParser.sh
    - mode: 755

parserServiceRunner:
  service.running:
    - name: domainParser
    - require: 
      - git: git_domainThing
