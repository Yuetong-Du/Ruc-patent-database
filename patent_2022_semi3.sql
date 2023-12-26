CREATE database if not exists patent_2022;
use patent_2022;

##建表
CREATE table if not exists g_patent(
patent_number varchar(20) PRIMARY KEY,
d_ipc int CHECK(d_ipc = 0 or d_ipc = 1),
ipc_section varchar(32),
application_number varchar(36),
patent_type varchar(10) CHECK(patent_type = "utility" or
 patent_type = "design" or patent_type = "plant" or patent_type = "reissue"),
patent_date datetime,
patent_title text,
patent_abstract text,
wipo_kind varchar(3),
num_claims int
);
CREATE table if not exists g_inventor_general(
patent_number varchar(20) PRIMARY KEY,
team_size int,
inventors int,
men_inventors int,
women_inventors int,
d_inventor int CHECK(d_inventor = 0 or d_inventor = 1)
);
CREATE table if not exists g_inventor_detailed(
patent_number varchar(20) PRIMARY KEY,
inventor_id1 varchar(128),
male_flag1 int,
inventor_name1 varchar(128),
inventor_id2 varchar(128),
male_flag2 int,
inventor_name2 varchar(128),
inventor_id3 varchar(128),
male_flag3 int,
inventor_name3 varchar(128),
inventor_id4 varchar(128),
male_flag4 int,
inventor_name4 varchar(128),
inventor_id5 varchar(128),
male_flag5 int,
inventor_name5 varchar(128),
inventor_id6 varchar(128),
male_flag6 int,
inventor_name6 varchar(128),
inventor_id7 varchar(128),
male_flag7 int,
inventor_name7 varchar(128),
inventor_id8 varchar(128),
male_flag8 int,
inventor_name8 varchar(128),
inventor_id9 varchar(128),
male_flag9 int,
inventor_name9 varchar(128),
inventors int
);
CREATE table if not exists g_application(
application_number varchar(20) PRIMARY KEY,
application_year int,
patent_number varchar(36) not null,
grant_year int,
d_application int CHECK(d_application = 0 or d_application = 1),
KEY `K__appli_patent` (`patent_number`),
CONSTRAINT `FK__appli_patent` FOREIGN KEY (`patent_number`) 
REFERENCES `g_patent`(`patent_number`)
);
CREATE table if not exists g_assignee(
patent_number varchar(20) PRIMARY KEY,
d_assignee int,
assignee varchar(160),
assignee_sequence int,
assignee_ind int
);
CREATE table if not exists g_location(
patent_number varchar(20) PRIMARY KEY,
country varchar(36),
city varchar(100),
state varchar(36),
county varchar(72),
d_location int CHECK(d_location = 0 or d_location = 1)
);

##加入表级约束
ALTER table g_inventor_general add constraint inventor_num
CHECK(inventors = men_inventors + women_inventors and
team_size >= inventors);

##建立跟踪表
##男女发明人数量差大于10
CREATE table if not exists inventor_alert(
patent_number varchar(20) PRIMARY KEY,
inventors int,
men_inventors int,
women_inventors int);
##从申请到确定相隔8年以上
CREATE table if not exists appli_delay(
application_number varchar(20) PRIMARY KEY,
patent_number varchar(36) not null,
application_year int,
grant_year int);
##超大型非发明人团队（非发明人数量>10或有发明人时大于发明人数的五倍）
CREATE table if not exists beyond_inventor(
patent_number varchar(20) PRIMARY KEY,
not_inventors int,
inventors int);

##分别创建触发器
delimiter //
CREATE trigger inventor_warning
AFTER INSERT on g_inventor_general for each row
begin
if ((new.men_inventors - new.women_inventors > 10)
or (new.women_inventors - new.men_inventors > 10)) then
INSERT into inventor_alert
values(new.patent_number, new.inventors, new.men_inventors, new.women_inventors);
end if;
end;//

CREATE trigger application_long
AFTER INSERT on g_application for each row
begin
if(new.grant_year - new.application_year >8) then
INSERT into appli_delay
values(new.application_number, new.patent_number, new.application_year, new.grant_year);
end if;
end;//

CREATE trigger big_assistants
AFTER INSERT on g_inventor_general for each row
begin
if((new.team_size - new.inventors >10) or 
((new.team_size > 6*new.inventors) and (new.inventors > 0))) then
INSERT into beyond_inventor
values(new.patent_number, new.team_size - new.inventors, new.inventors);
end if;
end;//

delimiter ;

##导入数据，查看触发器执行情况
LOAD data infile 'C:/ProgramData/MySQL/MySQL Server 8.1/UpLOADs/g_patent.csv'
into table g_patent fields terminated by ','
IGNORE 1 LINES
(@`patent_number`,`d_ipc`,@`ipc_section`,@`application_number`,
@`patent_type`,`patent_date`,@`patent_title`,@`patent_abstract`,
@`wipo_kind`,@`num_claims`)
set
`patent_number` = replace(@patent_number,'"',''),
`ipc_section` = replace(@ipc_section,'"',''),
`application_number` = replace(@application_number,'"',''),
`patent_type` = replace(@patent_type,'"',''),
`patent_title` = replace(@patent_title,'"',''),
`patent_abstract` = replace(@patent_abstract,'"',''),
`wipo_kind` = replace(@wipo_kind,'"',''),
`num_claims` = nullif(@num_claims,'');

LOAD data infile 'C:/ProgramData/MySQL/MySQL Server 8.1/UpLOADs/g_inventor_general.csv'
into table g_inventor_general fields terminated by ','
IGNORE 1 LINES;

LOAD data infile 'C:/ProgramData/MySQL/MySQL Server 8.1/UpLOADs/g_inventor_detailed.csv'
into table g_inventor_detailed fields terminated by ','
IGNORE 1 LINES
(`patent_number`,`inventor_id1`,@`male_flag1`,`inventor_name1`,
`inventor_id2`,@`male_flag2`,`inventor_name2`,`inventor_id3`,@`male_flag3`,`inventor_name3`,
`inventor_id4`,@`male_flag4`,`inventor_name4`,`inventor_id5`,@`male_flag5`,`inventor_name5`,
`inventor_id6`,@`male_flag6`,`inventor_name6`,`inventor_id7`,@`male_flag7`,`inventor_name7`,
`inventor_id8`,@`male_flag8`,`inventor_name8`,`inventor_id9`,@`male_flag9`,`inventor_name9`,
`inventors`)
set 
`male_flag1` = nullif(@male_flag1,''),
`male_flag2` = nullif(@male_flag2,''),
`male_flag3` = nullif(@male_flag3,''),
`male_flag4` = nullif(@male_flag4,''),
`male_flag5` = nullif(@male_flag5,''),
`male_flag6` = nullif(@male_flag6,''),
`male_flag7` = nullif(@male_flag7,''),
`male_flag8` = nullif(@male_flag8,''),
`male_flag9` = nullif(@male_flag9,'');

LOAD data infile 'C:/ProgramData/MySQL/MySQL Server 8.1/UpLOADs/g_application.csv'
into table g_application fields terminated by ','
IGNORE 1 LINES;

LOAD data infile 'C:/ProgramData/MySQL/MySQL Server 8.1/UpLOADs/g_assignee.csv'
into table g_assignee fields terminated by ','
IGNORE 1 LINES
(`patent_number`,`d_assignee`,`assignee`,@`assignee_sequence`,`assignee_ind`)
set `assignee_sequence` = nullif(@assignee_sequence,'');

LOAD data infile 'C:/ProgramData/MySQL/MySQL Server 8.1/UpLOADs/g_location.csv'
into table g_location fields terminated by ','
IGNORE 1 LINES;

SELECT * from inventor_alert;
SELECT * from appli_delay
order by patent_number;
SELECT * from beyond_inventor;

delimiter //
CREATE PROCEDURE inventor2patent 
(IN inventor_name VARCHAR(128), OUT patent VARCHAR(20))
begin
SELECT g_patent.*,g_location.country,g_location.city,g_location.state,g_location.county
FROM g_inventor_detailed,g_patent,g_location
WHERE 
g_inventor_detailed.patent_number = g_patent.patent_number and
g_patent.patent_number = g_location.patent_number and
(inventor_name1 = inventor_name or 
inventor_name2 = inventor_name or
inventor_name3 = inventor_name or
inventor_name4 = inventor_name or
inventor_name5 = inventor_name or
inventor_name6 = inventor_name or
inventor_name7 = inventor_name or
inventor_name8 = inventor_name or
inventor_name9 = inventor_name);
END//
delimiter ;

CALL inventor2patent('John Fehr',@patent);