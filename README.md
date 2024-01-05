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
| d_ipc                   | INT      | -    | DEFAULT NULL                             | IPC分类            |
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

| 列名              | 数据类型 | 长度 | 约束条件    | 描述           |
| ----------------- | -------- | ---- | ----------- | -------------- |
| patent_number     | VARCHAR  | 20   | PRIMARY KEY | 专利编号       |
| d_assignee        | INT      | -    | -           | 受让人分类标志 |
| assignee          | VARCHAR  | 160  | -           | 受让人         |
| assignee_sequence | INT      | -    | -           | 受让人序列     |
| assignee_ind      | INT      | -    | -           | 受让人指标     |

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

| 列名            | 数据类型 | 长度 | 约束条件                                | 描述           |
| --------------- | -------- | ---- | --------------------------------------- | -------------- |
| patent_number   | VARCHAR  | 20   | PRIMARY KEY                             | 专利编号       |
| team_size       | INT      | -    | -                                       | 团队大小       |
| inventors       | INT      | -    | -                                       | 发明人总数     |
| men_inventors   | INT      | -    | -                                       | 男性发明人数量 |
| women_inventors | INT      | -    | -                                       | 女性发明人数量 |
| d_inventor      | INT      | -    | CHECK(d_inventor = 0 or d_inventor = 1) | 发明人分类标志 |

### g_location

| 列名          | 数据类型 | 长度 | 约束条件                                | 描述         |
| ------------- | -------- | ---- | --------------------------------------- | ------------ |
| patent_number | VARCHAR  | 20   | PRIMARY KEY                             | 专利编号     |
| country       | VARCHAR  | 36   | -                                       | 国家         |
| city          | VARCHAR  | 100  | -                                       | 城市         |
| state         | VARCHAR  | 36   | -                                       | 州/省        |
| county        | VARCHAR  | 72   | -                                       | 县/地区      |
| d_location    | INT      | -    | CHECK(d_location = 0 or d_location = 1) | 地点分类标志 |

### g_patent

| 列名               | 数据类型 | 长度 | 约束条件                                                     | 描述         |
| ------------------ | -------- | ---- | ------------------------------------------------------------ | ------------ |
| patent_number      | VARCHAR  | 20   | PRIMARY KEY                                                  | 专利编号     |
| d_ipc              | INT      | -    | CHECK(d_ipc = 0 or d_ipc = 1)                                | IPC分类标志  |
| ipc_section        | VARCHAR  | 32   | -                                                            | IPC分类部分  |
| application_number | VARCHAR  | 36   | -                                                            | 申请编号     |
| patent_type        | VARCHAR  | 10   | CHECK(patent_type IN ('utility', 'design', 'plant', 'reissue')) | 专利类型     |
| patent_date        | DATETIME | -    | -                                                            | 专利日期     |
| patent_title       | TEXT     | -    | -                                                            | 专利标题     |
| patent_abstract    | TEXT     | -    | -                                                            | 专利摘要     |
| wipo_kind          | VARCHAR  | 100  | -                                                            | WIPO种类     |
| num_claims         | INT      | -    | -                                                            | 权利要求数量 |

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

如图所示是本实验的ER图，其中...

#### 实体属性

Inspector: {<u>id</u>, username, email, password, telephone }

User: {<u>id</u>, username, email, table_name, table_id }

appli_delay: {<u>application_number</u>, patent_number, application_year, grant_year }

inventor_alert: {<u>patent_number</u>, inventors, men_inventors, women_inventors }

g_patent: {<u>patent_number</u>, d_ipc, ipc_section, application_number, patent_type, patent_date, patent_title, patent_abstract, wipo_kind, num_claims }

g_inventor_general: {<u>patent_number</u>, team_size, inventors, men_inventors, women_inventors, d_inventor }

g_inventor_detailed: {<u>patent_number</u>, inventor_id1, male_flag1, inventor_name1, inventor_id2, male_flag2, inventor_name2, ... }

g_application: {<u>application_number</u>, application_year, patent_number, grant_year, d_application }

g_assignee: {<u>patent_number</u>, d_assignee, assignee, assignee_sequence, assignee_ind }

g_location: {<u>patent_number</u>, country, city, state, county, d_location }

g_application_in_progress: {<u>table_number</u>, applicant_id, patent_application_date, d_ipc, ipc_section, patent_type, patent_date, patent_title, patent_abstract, wipo_kind, status, Inventor_name1, male_flag1, Inventor_name2, male_flag2, Inventor_name3, male_flag3, Inventor_name4, male_flag4, Inventor_name5, male_flag5, Inventor_name6, male_flag6, Inventor_name7, male_flag7, Inventor_name8, male_flag8, Inventor_name9, male_flag9, assignee, country, state, county, city }

由于最小的数据单元都是专利本身，因此我们的数据库模式符合BCNF。

### 用户端逻辑分析与功能解释

首页上会显示目前数据库的基本信息，并要求用户登陆。

![](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/首页.png)

#### Visitor访客

1. 访客可以进行注册![visitor注册](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/visitor注册.png)
   - 此处的测试数据为：username = visitor, email = visitor@ruc.edu.cn, password = 123456

2. 进行登陆![](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/visitor登陆.png)

3. 登陆成功后，functions栏目中就会出现可以使用的功能

   ![](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/visitor登陆成功界面.png)

4. 更新个人信息

   - 首先，点击settings，由于信息不完全，会有信息提示需要更新个人信息（telephone）

   ![](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/visitor更新信息.png)

   - 更新详细信息之后，访客可以再次点击settings调整username/password等信息

   ![](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/visitor setting.png)

   - 更新电话示例：电话12345678901

   ![](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/visitor更新详细信息.png)

   - 更新数据示例：username-visitor01, email-visitor01@ruc.edu.cn

   ![visitor更新信息](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/visitor更新信息.png)

   - 更新密码示例：111111

   ![](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/visitor更新密码.png)

   - 更新成功后返回界面

   ![](/Users/tracydu/Documents/GitHub/Ruc-patent-database/pics/visitor更新成功后返回页面.png)

   

5. 查看数据面板：点击右侧的functions，第一项功能是进行搜索，第二项功能是查看数据看板

   1. 

