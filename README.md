# 实验三 动态编程

## 实验目的

掌握动态Web编程框架，实现数据库在Web编程中的应用

## 实验内容及其要求

**(一)**  **实验内容**

根据小组选择的研究对象和场景（视频，专利，企业创新，其它），设计数据库应用系统，并实现动态Web编程框架（Vue+Flask-restful+Mysql）

**(二) 实验要求**

1. 定义至少三个存储过程或者函数，其中至少一个定时任务
2. 设计数据看板，并展示数据库中的数据
3. 将综合实验一和综合实验二定义的内容体现在框架上
4. 提供测试样例
5. 进阶要求：支持动态交互
6. 基于上述内容**形成课程报告。**

## 实验重点和难点

- 实验重点：Web编程、数据库应用，使用后端程序操作数据库。

- 实验难点：动态交互 

## 实验报告

```
  ____       _             _    ____  ____  _   _  ____ 
 |  _ \ __ _| |_ ___ _ __ | |_ / __ \|  _ \| | | |/ ___|
 | |_) / _` | __/ _ \ '_ \| __/ / _` | |_) | | | | |    
 |  __/ (_| | ||  __/ | | | || | (_| |  _ <| |_| | |___ 
 |_|   \__,_|\__\___|_| |_|\__\ \__,_|_| \_\\___/ \____|
                               \____/                   
```

题目：Patent@RUC

成员：梁浩贤 杜玥潼 孙代平 张云峰

实验环境：macOS Ventura 13.6.1，Mysql 8.2.0 arm64

### 安装指南

1. 通过source运行patent_2022_240106.sql文件

2. 修改__init__.py的参数，将密码字段修改为您的密码

   ![配置-修改密码](./pics/配置-修改密码.png)

3. 在终端中运行python(或python3)  <地址>/run.py 即可登陆

   ![配置-运行](./pics/配置-运行.png)

### 数据内容简介

我们选择的数据来自于PatentView数据库中2022年审批通过的专利数据，总数约18万条。通过csv文件函数进行导入，并进行了一定的数据清洗和格式化（包括但不限于缺失值处理、去重、调整国家名称等）。其中部分字段解释如下：

- IPC分类：国际专利分类（IPC），通常根据其section被分为以下八类：A- 人类生活必需品，B- 执行操作、运输，C- 化学和冶金，D- 纺织品、纸张，E- 固定建筑，F- 机械工程、照明、加热、武器，G- 物理学，H- 电学（具体信息可以查看[相关网页](https://www.j-platpat.inpit.go.jp/cache/classify/patent/PMGS_HTML/jpp/IPC/en/ipcSection/ipcSection_en.html)）
- Wipo：世界知识产权组织（World Intellectual Property Organisation），其中wipo kind指的是该专利在知识产权中的分类，详细标准参考[相关网页](https://www.wipo.int/classifications/ipc/en/)
- 专利分类Patent Type：
  - 实用新型（Utility）：这是一种专利类型，通常用于保护新的、有用的、非显而易见的技术改进或发明。实用新型专利主要关注于技术的功能性方面，而不是外观。
  - 外观设计（Design）：这是用于保护产品外观或外观设计的专利类型。它强调产品的外观、形状、装饰等方面的创新，而不是技术功能。
  - 补发（Reissue）：补发专利是指已经授予的专利，后来经审查发现有误或不完整，需要对其进行修正或补充的情况。通常，补发专利用于纠正原专利的错误或不准确的声明。
  - 植物（Plant）：在专利领域，"发明"通常指的是新的、有用的、非显而易见的技术发明。在植物领域，"发明"指的是对植物的新品种或变种的保护。这通常涉及到对植物的繁育或培育工作。

### 需求分析：

#### 专利申请者Applicant

对于申请者来说，本系统应该满足以下几个基本需求：

- 登陆账号：注册后可以用邮箱和密码登录系统
- 修改个人信息：成功登陆后可以修改个人信息，便于管理
- 浏览目前的专利信息：成功登陆后可以使用关键词、作者等信息搜索现有的专利
- 申请专利：填写专利申请，并提交
- 查看专利申请情况：查看自己账户所提交的申请（包括细节）
- 查看数据看板

#### 访客Visitor

- 登陆账号：注册后可以用邮箱和密码登录系统
- 修改个人信息：成功登陆后可以修改个人信息，便于管理
- 浏览目前的专利信息：成功登陆后可以使用关键词、作者等信息搜索现有的专利
- 查看数据看板

#### 管理员Inspector

- 登陆账号：注册后可以用邮箱和密码登录系统
- 修改个人信息：成功登陆后可以修改个人信息，便于管理
- 浏览目前的专利信息：成功登陆后可以使用关键词、作者等信息搜索现有的专利
- 查看数据看板
- 审批专利信息：查看所有申请者提交的专利申请，并审批（通过/不通过）

### 数据结构和数据项

### User

包含所有的用户信息

| 列名       | 数据类型 | 长度 | 约束条件                   | 描述                   |
| ---------- | -------- | ---- | -------------------------- | ---------------------- |
| id         | INT      | -    | AUTO_INCREMENT PRIMARY KEY | 用户ID                 |
| username   | VARCHAR  | 20   | NOT NULL DEFAULT '私密'    | 用户名，缺省值为"私密" |
| email      | VARCHAR  | 120  | NOT NULL                   | 电子邮箱地址           |
| table_name | VARCHAR  | 20   | NOT NULL                   | 关联的表名             |
| table_id   | INT      | -    | NOT NULL                   | 关联的表的ID           |

### appli_delay

| 列名               | 数据类型 | 长度 | 约束条件              | 描述     |
| ------------------ | -------- | ---- | --------------------- | -------- |
| application_number | VARCHAR  | 20   | NOT NULL, PRIMARY KEY | 申请编号 |
| patent_number      | VARCHAR  | 36   | NOT NULL              | 专利编号 |
| application_year   | INT      | -    | DEFAULT NULL          | 申请年份 |
| grant_year         | INT      | -    | DEFAULT NULL          | 授权年份 |

### beyond_inventor

### g_application

| 列名               | 数据类型 | 长度 | 约束条件                                      | 描述         |
| ------------------ | -------- | ---- | --------------------------------------------- | ------------ |
| application_number | VARCHAR  | 20   | PRIMARY KEY                                   | 申请编号     |
| application_year   | INT      | -    | -                                             | 申请年份     |
| patent_number      | VARCHAR  | 36   | NOT NULL                                      | 专利编号     |
| grant_year         | INT      | -    | -                                             | 授予年份     |
| d_application      | INT      | -    | CHECK(d_application = 0 or d_application = 1) | 申请分类标志 |

### g_application_in_progress

| 列名                    | 数据类型 | 长度 | 约束条件                                 | 描述               |
| ----------------------- | -------- | ---- | ---------------------------------------- | ------------------ |
| table_number            | INT      | -    | NOT NULL, AUTO_INCREMENT, PRIMARY KEY    | 表格编号           |
| applicant_id            | INT      | -    | DEFAULT NULL                             | 申请人ID           |
| patent_application_date | DATETIME | -    | DEFAULT NULL                             | 专利申请日期       |
| ipc_section             | VARCHAR  | 32   | DEFAULT NULL                             | IPC分类部分        |
| patent_type             | VARCHAR  | 10   | DEFAULT NULL                             | 专利类型           |
| patent_date             | DATETIME | -    | DEFAULT NULL                             | 专利授予日期       |
| patent_title            | TEXT     | -    | -                                        | 专利标题           |
| patent_abstract         | TEXT     | -    | -                                        | 专利摘要           |
| wipo_kind               | VARCHAR  | 3    | DEFAULT NULL                             | WIPO种类           |
| status                  | INT      | -    | DEFAULT NULL                             | 状态               |
| Inventor_name1          | VARCHAR  | 20   | DEFAULT NULL                             | 第一发明人姓名     |
| male_flag1              | INT      | -    | DEFAULT '1', CHECK(male_flag1 IN (0, 1)) | 第一发明人性别标志 |
| Inventor_name2          | VARCHAR  | 20   | DEFAULT NULL                             | 第二发明人姓名     |
| male_flag2              | INT      | -    | DEFAULT '1', CHECK(male_flag2 IN (0, 1)) | 第二发明人性别标志 |
| Inventor_name3          | VARCHAR  | 20   | DEFAULT NULL                             | 第三发明人姓名     |
| male_flag3              | INT      | -    | DEFAULT '1', CHECK(male_flag3 IN (0, 1)) | 第三发明人性别标志 |
| Inventor_name4          | VARCHAR  | 20   | DEFAULT NULL                             | 第四发明人姓名     |
| male_flag4              | INT      | -    | DEFAULT '1', CHECK(male_flag4 IN (0, 1)) | 第四发明人性别标志 |
| Inventor_name5          | VARCHAR  | 20   | DEFAULT NULL                             | 第五发明人姓名     |
| male_flag5              | INT      | -    | DEFAULT '1', CHECK(male_flag5 IN (0, 1)) | 第五发明人性别标志 |
| Inventor_name6          | VARCHAR  | 20   | DEFAULT NULL                             | 第六发明人姓名     |
| male_flag6              | INT      | -    | DEFAULT '1', CHECK(male_flag6 IN (0, 1)) | 第六发明人性别标志 |
| Inventor_name7          | VARCHAR  | 20   | DEFAULT NULL                             | 第七发明人姓名     |
| male_flag7              | INT      | -    | DEFAULT '1', CHECK(male_flag7 IN (0, 1)) | 第七发明人性别标志 |
| Inventor_name8          | VARCHAR  | 20   | DEFAULT NULL                             | 第八发明人姓名     |
| male_flag8              | INT      | -    | DEFAULT '1', CHECK(male_flag8 IN (0, 1)) | 第八发明人性别标志 |
| Inventor_name9          | VARCHAR  | 20   | DEFAULT NULL                             | 第九发明人姓名     |
| male_flag9              | INT      | -    | DEFAULT '1', CHECK(male_flag9 IN (0, 1)) | 第九发明人性别标志 |
| assignee                | VARCHAR  | 50   | DEFAULT NULL                             | 受让人             |
| country                 | VARCHAR  | 50   | DEFAULT NULL                             | 国家               |
| state                   | VARCHAR  | 50   | DEFAULT NULL                             | 州/省              |
| county                  | VARCHAR  | 50   | DEFAULT NULL                             | 县/区              |
| city                    | VARCHAR  | 50   | DEFAULT NULL                             | 城市               |

### g_assignee

| 列名              | 数据类型 | 长度 | 约束条件    | 描述       |
| ----------------- | -------- | ---- | ----------- | ---------- |
| patent_number     | VARCHAR  | 20   | PRIMARY KEY | 专利编号   |
| assignee          | VARCHAR  | 160  | -           | 受让人     |
| assignee_sequence | INT      | -    | -           | 受让人序列 |

### g_inventor_detailed

| 列名           | 数据类型 | 长度 | 约束条件    | 描述            |
| -------------- | -------- | ---- | ----------- | --------------- |
| patent_number  | VARCHAR  | 20   | PRIMARY KEY | 专利编号        |
| inventor_id1   | VARCHAR  | 128  | -           | 发明人1 ID      |
| male_flag1     | INT      | -    | -           | 发明人1性别标志 |
| inventor_name1 | VARCHAR  | 128  | -           | 发明人1姓名     |
| inventor_id2   | VARCHAR  | 128  | -           | 发明人2 ID      |
| male_flag2     | INT      | -    | -           | 发明人2性别标志 |
| inventor_name2 | VARCHAR  | 128  | -           | 发明人2姓名     |
| ...            | ...      | ...  | ...         | ...             |
| inventors      | INT      | -    | -           | 发明人总数      |

### g_inventor_general

| 列名            | 数据类型 | 长度 | 约束条件    | 描述           |
| --------------- | -------- | ---- | ----------- | -------------- |
| patent_number   | VARCHAR  | 20   | PRIMARY KEY | 专利编号       |
| team_size       | INT      | -    | -           | 团队大小       |
| inventors       | INT      | -    | -           | 发明人总数     |
| men_inventors   | INT      | -    | -           | 男性发明人数量 |
| women_inventors | INT      | -    | -           | 女性发明人数量 |

### g_location

| 列名          | 数据类型 | 长度 | 约束条件    | 描述     |
| ------------- | -------- | ---- | ----------- | -------- |
| patent_number | VARCHAR  | 20   | PRIMARY KEY | 专利编号 |
| country       | VARCHAR  | 36   | -           | 国家     |
| city          | VARCHAR  | 100  | -           | 城市     |
| state         | VARCHAR  | 36   | -           | 州/省    |
| county        | VARCHAR  | 72   | -           | 县/地区  |

### g_patent

| 列名               | 数据类型 | 长度 | 约束条件                                                     | 描述        |
| ------------------ | -------- | ---- | ------------------------------------------------------------ | ----------- |
| patent_number      | VARCHAR  | 20   | PRIMARY KEY                                                  | 专利编号    |
| ipc_section        | VARCHAR  | 32   | -                                                            | IPC分类部分 |
| application_number | VARCHAR  | 36   | -                                                            | 申请编号    |
| patent_type        | VARCHAR  | 10   | CHECK(patent_type IN ('utility', 'design', 'plant', 'reissue')) | 专利类型    |
| patent_date        | DATETIME | -    | -                                                            | 专利日期    |
| patent_title       | TEXT     | -    | -                                                            | 专利标题    |
| patent_abstract    | TEXT     | -    | -                                                            | 专利摘要    |
| wipo_kind          | VARCHAR  | 100  | -                                                            | WIPO种类    |

### inspector

| 列名      | 数据类型 | 长度 | 约束条件                              | 描述     |
| --------- | -------- | ---- | ------------------------------------- | -------- |
| id        | INT      | -    | NOT NULL, AUTO_INCREMENT, PRIMARY KEY | 检查员ID |
| username  | VARCHAR  | 20   | NOT NULL                              | 用户名   |
| email     | VARCHAR  | 120  | NOT NULL                              | 电子邮件 |
| password  | VARCHAR  | 60   | NOT NULL                              | 密码     |
| telephone | VARCHAR  | 20   | NOT NULL DEFAULT 'null'               | 电话号码 |

### inventor_alert

| 列名            | 数据类型 | 长度 | 约束条件              | 描述           |
| --------------- | -------- | ---- | --------------------- | -------------- |
| patent_number   | VARCHAR  | 20   | NOT NULL, PRIMARY KEY | 专利编号       |
| inventors       | INT      | -    | DEFAULT NULL          | 发明家总数     |
| men_inventors   | INT      | -    | DEFAULT NULL          | 男性发明家数量 |
| women_inventors | INT      | -    | DEFAULT NULL          | 女性发明家数量 |

### Visitor

| 列名      | 数据类型 | 长度 | 约束条件                              | 描述     |
| --------- | -------- | ---- | ------------------------------------- | -------- |
| id        | INT      | -    | NOT NULL, AUTO_INCREMENT, PRIMARY KEY | 访客ID   |
| username  | VARCHAR  | 20   | NOT NULL, UNIQUE                      | 用户名   |
| email     | VARCHAR  | 120  | NOT NULL, UNIQUE                      | 电子邮件 |
| password  | VARCHAR  | 60   | NOT NULL                              | 密码     |
| Telephone | VARCHAR  | 20   | NOT NULL                              | 电话     |



### 概念设计

#### ER图

如图所示是本实验的ER图

![ER图](./pics/ER图.jpg)

#### 实体属性

- Inspector: {<u>id</u>, username, email, password, telephone }

- User: {<u>id</u>, username, email, table_name, table_id }

- appli_delay: {<u>application_number</u>, patent_number, application_year, grant_year }

- inventor_alert: {<u>patent_number</u>, inventors, men_inventors, women_inventors }

- g_patent: {<u>patent_number</u>, d_ipc, ipc_section, application_number, patent_type, patent_date, patent_title, patent_abstract, wipo_kind, num_claims }

- g_inventor_general: {<u>patent_number</u>, team_size, inventors, men_inventors, women_inventors, d_inventor }

- g_inventor_detailed: {<u>patent_number</u>, inventor_id1, male_flag1, inventor_name1, inventor_id2, male_flag2, inventor_name2, ... }

- g_application: {<u>application_number</u>, application_year, patent_number, grant_year, d_application }

- g_assignee: {<u>patent_number</u>, d_assignee, assignee, assignee_sequence, assignee_ind }

- g_location: {<u>patent_number</u>, country, city, state, county, d_location }

- g_application_in_progress: {<u>table_number</u>, applicant_id, patent_application_date, d_ipc, ipc_section, patent_type, patent_date, patent_title, patent_abstract, wipo_kind, status, Inventor_name1, male_flag1, Inventor_name2, male_flag2, Inventor_name3, male_flag3, Inventor_name4, male_flag4, Inventor_name5, male_flag5, Inventor_name6, male_flag6, Inventor_name7, male_flag7, Inventor_name8, male_flag8, Inventor_name9, male_flag9, assignee, country, state, county, city }

由于最小的数据单元都是专利本身，因此我们的数据库模式符合BCNF。

### 用户端逻辑分析与功能解释

首页上会显示目前数据库的基本信息，并要求用户登陆。

![](./pics/首页.png)

#### Visitor访客

1. 访客可以进行注册![visitor注册](./pics/visitor注册.png)
   - 此处的测试数据为：username = visitor, email = visitor@ruc.edu.cn, password = 123456

2. 进行登陆![](./pics/visitor登陆.png)

3. 登陆成功后，functions栏目中就会出现可以使用的功能

   ![](./pics/visitor登陆成功界面.png)

4. 更新个人信息

   - 首先，点击settings，由于信息不完全，会有信息提示需要更新个人信息（telephone）

   ![](./pics/visitor更新信息.png)

   - 更新详细信息之后，访客可以再次点击settings调整username/password等信息

   ![](./pics/visitor setting.png)

   - 更新电话示例：电话12345678901

   ![](./pics/visitor更新详细信息.png)

   - 更新数据示例：username-visitor01, email-visitor01@ruc.edu.cn

   ![visitor更新信息](./pics/visitor更新信息.png)

   - 更新密码示例：111111

   ![](./pics/visitor更新密码.png)

   - 更新成功后返回界面

   ![](./pics/visitor更新成功后返回页面.png)

   

5. 搜索专利：网站支持搜索D-IPC, IPC-section, 专利类别，专利标题关键词搜索，专利摘要关键词搜索，WIPOkind， 专利作者信息（支持搜索所有位次的作者），所在地区（国家、省、地区、城市），专利受让人，最少应用数，每页显示的专利数量。

   ![](./pics/搜索页面1.png)

   ![搜索页面2](./pics/搜索页面2.png)

   1. 测试数据1:D-ipc=1, IPC section:A, 专利类别：Utility，专利标题关键词：drive

   ![](./pics/搜索示例1.png)

   - 搜索结果1：可以查看对应专利的详细信息，也可以claim（应用，对应的专利num_claims会增加1）

   ![](./pics/搜索示例结果1.png)

   如果专利数字较多，可以进行翻页

   ![翻页](./pics/翻页.png)

   可以看到，在专利搜索页面，网站支持显示搜索到的专利总数量，并且会按照时间顺序（默认）每页10个专利的方式显示（这样可以提升加载速度），在每个专利的显示中，可以查看专利的细节（details）并引用（claim），后者会更改数据库内的信息，使得其专利应用次数增加1。
   
   ![搜索结果详细信息](./pics/搜索结果详细信息.png)
   
   ![引用后返回主界面](./pics/引用后返回主界面.png)
   
   - 测试数据2: 搜索专利设置在中国大陆-北京市的专利
   
   ![搜索示例2-北京](./pics/搜索示例2-北京.png)
   
   - 搜索结果：共有2493条专利结果
   
   ![搜索结果示例2-北京](./pics/搜索结果示例2-北京.png)
   
   - 可以点击查看详细信息：
   
   ![搜索结果示例2-北京搜索结果详细信息](./pics/搜索结果示例2-北京搜索结果详细信息.png)
   
   - 搜索示例3：受让人名称包含Stanford的专利
   
   ![搜索示例3-assignee为stanford](./pics/搜索示例3-assignee为stanford.png)
   
   ![搜索结果示例3-stanford](./pics/搜索结果示例3-stanford.png)					![搜索结果示例3-stanford搜索结果详细信息](./pics/搜索结果示例3-stanford搜索结果详细信息.png)
   
   - 搜索示例4: 搜索inventor为‘haoxian ’（注意此处为了排除haoxiang的inventor，关键词的结尾是‘ ’），搜索到了一个专利，是来自北京大学深圳研究院的Zhang, Haoxian同学的专利信息，专利标题是视频帧插值的方法和装置。
   
     ![搜索示例4-发明人为haoxian](./pics/搜索示例4-发明人为haoxian.png)

![搜索结果示例4-发明人为haoxian](./pics/搜索结果示例4-发明人为haoxian.png)

​			![搜索结果示例-haoxian详细信息](./pics/搜索结果示例-haoxian详细信息.png)

6. 查看数据面板：点击functions的中patent dashboard，即可查看。![dashboard](./pics/dashboard.png)

#### Applicant申请者

1. visitor所有的功能对申请者都开放

   ![applicant登陆界面](./pics/applicant登陆界面.png)

2. 申请专利：点击右侧function中的申请专利/上方的申请专利链接，在申请页面会被要求填写所有信息，也可以选择点击按钮添加发明人信息（最多可以添加9个）。申请成功后会返回首页。

   ![applicant专利申请界面](./pics/applicant专利申请界面.png)

   ![applicant专利申请信息2](./pics/applicant专利申请信息2.png)

   ![applicant申请结果提交界面](./pics/applicant申请结果提交界面.png)

3. 查看专利申请进度：在进度页面可以查看自己已经提交的信息，申请的状态分为：审批中（pending），审批通过（Approved）和审批不通过（Rejected)。

   ![applicant查看专利申请结果界面](./pics/applicant查看专利申请结果界面.png)

   ![applicant查看申请结果](./pics/applicant查看申请结果.png)

   ![applicant申请专利查看详细信息](./pics/applicant申请专利查看详细信息.png)

#### Inspector管理员

1. 访客的功能全部开放

   ![inspector登陆界面](./pics/inspector登陆界面.png)

2. 管理员可以进行审批，审批通过后的数据会被添加到数据库里（后者在数据看板中可以显示出来，专利总数会加1）![inspector审批专利](./pics/inspector审批专利.png)

   ![inspector审批专利结束](./pics/inspector审批专利结束.png)	

#### 其他功能

1. 追踪表查看：在之前的综合实验中，我们设置了三个追踪表，并设置了触发器

   ```sql
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
   end;
   //
   
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
   ```

   - 网页支持在搜索相关专利的时候，如果搜到属于这三个专利表的信息，我们会在详细页面进行显示

   ![追踪表展示](./pics/追踪表展示.png)

2. 定时任务：我们在首页上会显示现在的时间，每秒钟更新一次

   ![定时任务](./pics/定时任务.png)

### 总结

在本次数据库大作业中，我们组按照老师的要求设计开发了专利系统，并根据实际情况添加许多实用的拓展功能。从最初的需求分析，数据库设计，功能实现，到最后的系统实施，测试，我们结合课堂上学到的理论知识，从零开始开发设计了整个系统，收获丰富。

在设计过程中，我们也遇到了许多问题，比如概念结构设计阶段纠结如何平衡范式等级与查询效率，比如如何构建用户的关系模式等等。其中，对我们小组挑战最大的是前端开发。因为我们都没有学习过VUE、html以及javascript，所以在最开始的摸索过程中异常艰难，只能通过网上丰富的教学资源边动手边学习，但最后还是完整地敲出了现在这个较为完善的页面。

受限于时间，我们的系统并未将我们想到的所有功能一并实现，还有进一步完善的空间，具体表现为：

- 搜索结果页面支持进行多种字段的排序或再次搜索的功能
- 支持inspector为applicant留言，applicant可以基于之前的评价重新提交等等
- 支持引用专利的时候由applicant/inventor审批，并支持专利使用费用转账等等
- 支持信息中心：如applicant可以收到专利审批发生变化的显式通知
- ……

### 小组分工

- 专利数据查找与下载：张云峰、杜玥潼
- 专利数据清洗与导入：张云峰、梁浩贤
- 专利数据解读、触发器、追踪表设计：梁浩贤
- 数据库搭建与功能实现
  - 数据库搭建与汇总：杜玥潼
  - 基础功能实现与优化：杜玥潼、张云峰
  - 功能修改、优化（页面设置、优化搜索速度与方式、追踪表展示方式）：张云峰
  - sql代码撰写：张云峰
  - 定时器功能实现：张云峰
  - 专利数据看板设计与实现：孙代平、梁浩贤、杜玥潼
- 设置文档写作：杜玥潼、孙代平

