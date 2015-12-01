parserServiceFile:
  file.managed:
    - name: '/etc/init.d/domainParser'
    - source: salt://domainThing/domainParser.sh
    - mode: 755


