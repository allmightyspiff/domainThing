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

## V1 Writeup
put shit here


## V2 TODO
https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-4-on-centos-7 - logging thing
http://www.celeryproject.org/ - queueing thingy
kafka  - apache queue 
https://www.unbound.net/ - speed up DNS
+ apt-get install unbound unbound-host
+ http://munin-monitoring.org/
Make domainParser put things into queue
Make a domainResolver script read from queue and look up DNS




       



