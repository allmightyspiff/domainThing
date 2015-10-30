## MySQL setup


```mysql
create user 'domains'@'%' IDENTIFIED BY 'ThisistheDomains)('; 
create database domainThing;
grant all privileges on domainThing.* to 'domains'@'%';

create table ip_address (
    ip int unsigned
    ) engine = innodb;

create table ip_address_unique (
    ip int unsigned,
    primary key(`ip`)
    ) engine = innodb;

SELECT DISTINCT * INTO ip_address_unique FROM ip_address;
```