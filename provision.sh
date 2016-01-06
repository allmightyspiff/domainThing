#!/bin/bash
apt-get -y install curl python-pip git
curl -L https://bootstrap.saltstack.com -o install_salt.sh
sh install_salt.sh -A 127.0.0.1 -M -P stable
mkdir /domainThing
mkdir /srv

git clone https://github.com/allmightyspiff/domainThing.git /domainThing
cp -r /domainThing/srv/* /srv



