
git:
  pkg.installed:
    - name: git

git_domainThing:
  git.latest:
    - name: https://github.com/allmightyspiff/domainThing.git
    - target: /domainThing
    - require:
      - pkg: git
