drop database if exists speedMonitor;
create database if not exists speedMonitor;

use speedMonitor;
create table if not exists SpeedRecords
(
id int(11) unsigned not null auto_increment,
driver int(11) default null,
ctime bigint(11) default null,
speed int(11) default null
) engine=InnoDB auto_increment=0 default charset=utf8;ﬁ