# Find out who hosts what domains!

## Getting the domains
http://jordan-wright.com/blog/2015/09/30/how-to-download-a-list-of-all-registered-domain-names/ is worth reading.

.COM accounts for about 50% of all domains, but [here](http://w3techs.com/technologies/overview/top_level_domain/all) is a nice list of the statistics for the others, so you get a good idea of how much effort you want to put into getting the domains.

+ [.COM, .NET, .NAME](https://www.verisign.com/en_US/channel-resources/domain-registry-products/zone-file/index.xhtml)
+ [.ORG](http://w3techs.com/technologies/overview/top_level_domain/all)
+ [ALMOST EVERYTHING ELSE](https://czds.icann.org/en)
+ [.RU](https://www.nic.ru/dns/partners/en/all_lists_info.html)
    * Has to be sent by mail, in Russian
+ [viewdns](http://viewdns.info/data/)
    * Offers pay for zone data
+ [domain index](http://domainindex.com/tools/download-cctld-zone-files)
    * Another pay for zone data
+ [.DE](https://www.denic.de/en/faq-single/546/6/252.html?cHash=3f381e21588e73923150fe9097cb147d)
    * unavailable directly
+ [.JP](http://jprs.co.jp/en/regist.html#q17)
    * unavailable directly
+ [.BR](https://registro.br)
    * unclear




## Requirement
https://github.com/drkjam/netaddr
https://www.rabbitmq.com/install-debian.html
https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-repositories.html
https://download.elastic.co/kibana/kibana/kibana-4.2.0-linux-x64.tar.gz
https://download.elastic.co/kibana/kibana/kibana-4.1.2-linux-x64.tar.gz


# SALT-MASTER setup
use provision.sh as a postinstall script

+ make edits to /srv/pillar/softlayer.sls
server needs bond0 to work as expected. If not, replace bond0 with eth0 in domainThing/srv/salt/mysql/my.cnf and  domainThing/srv/salt/elk/init.sls
```
Rendering SLS 'base:elk' failed: Jinja variable 'dict object' has no attribute 'inet'
```
is the error you will get if the network card is different

```bash
service salt-master restart
service salt-minion restart
salt-key -A -y

salt '*' state.highstate
salt-cloud -y -m /etc/salt/cloud.maps.d/parser.conf
```

update your master host record to have the IP of your master
```bash
slcli dns record-edit --by-record domain-master-private --data 10.76.24.000 lablayer.info
```


copy your subnets.csv file to the master
```bash
cd /domainThing
python subnetsToSql.py
```
copy your zones to the parser

After your zones are copied to the parser, and your subnets are in mysql, its time to go!

set ready to 1
```
sed -i -e 's/ready: 0/ready: 1/' /srv/salt/domainThing/config-template.cfg
salt -G 'roles:parser' state.highstate
```

view the queue
```
rabbitmqctl list_queues name messages_ready messages_unacknowledged
```




