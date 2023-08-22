---
title: mysql
date: 2019-3-27 22:19:09
---
[TOC]

	六、DML语言的学习    ★             
		插入语句						
		修改语句						
		删除语句						
	七、DDL语言的学习  
		库和表的管理	 √				
		常见数据类型介绍  √          
		常见约束  	  √			
	八、TCL语言的学习
		事务和事务处理                 
	九、视图的讲解           √
	十、变量                      
	十一、存储过程和函数   
	十二、流程控制结构       

# 数据库简介

[MySQL - 菜鸟教程](https://www.runoob.com/mysql/mysql-tutorial.html)

## 数据库相关概念

### 数据库的好处

	1.持久化数据到 本地
	2.可以实现结构化查询，方便管理


### 数据库相关概念

	1、DB：数据库，保存一组有组织的数据的容器
	2、DBMS：数据库管理系统，又称为数据库软件（产品），用于管理DB中的数据
	3、SQL:结构化查询语言，用于和DBMS通信的语言

### 数据库存储数据的特点

	1、将数据放到表中，表再放到库中
	2、一个数据库中可以有多个表，每个表都有一个的名字，用来标识自己。表名具有唯一性。
	3、表具有一些特性，这些特性定义了数据在表中如何存储，类似java中 “类”的设计。
	4、表由列组成，我们也称为字段。所有表都是由一个或多个列组成的，每一列类似java 中的”属性”
	5、表中的数据是按行存储的，每一行类似于java中的“对象”。
##  MySQL产品的介绍和安装

###  MySQL服务的启动和停止

```
方式一：计算机——右击管理——服务
方式二：通过管理员身份运行
net start 服务名（启动服务）
net stop 服务名（停止服务）
```

###  MySQL服务的登录和退出   

```
方式一：通过mysql自带的客户端
只限于root用户
```

```
方式二：通过windows自带的客户端
登录：
mysql 【-h主机名 -P端口号 】-u用户名 -p密码

退出：
exit或ctrl+C	
```




##  SQL的语言分类

```
DQL（Data Query Language）：数据查询语言
	select 
DML(Data Manipulate Language):数据操作语言
	insert 、update、delete
DDL（Data Define Languge）：数据定义语言
	create、drop、alter
TCL（Transaction Control Language）：事务控制语言
	commit、rollback
```

##  MySQL的语法规范

1.不区分大小写,但建议关键字大写，表名、列名小写
2.每条命令最好用分号结尾
3.每条命令根据需要，可以进行缩进 或换行
4.注释

```mysql
单行注释：#注释文字
单行注释：-- 注释文字
多行注释：/* 注释文字  */
```

# 查询-DQL语言

## 基础查询

```sql
语法：
SELECT 要查询的东西【FROM 表名】;
```

```sql
类似于Java中 :System.out.println(要打印的东西);
特点：
①通过select查询完的结果 ，是一个虚拟的表格，不是真实存在
② 要查询的东西 可以是常量值、可以是表达式、可以是字段、可以是函数
```

### DISTINCT

**相同值只会出现一次**。它作用于所有列，也就是说**所有列的值都相同才算相同。**

```sql
SELECT DISTINCT col1, col2
FROM mytable;
```

## 计算字段

在**数据库服务器上完成数据的转换和格式化**的工作往往比客户端上快得多，并且转换和格式化后的**数据量更少的话可以减少网络通信量。**

计算字段通常需要使用  **AS**  来取别名，否则输出的时候字段名为计算表达式。

```sql
SELECT col1 * col2 AS alias
FROM mytable;

#起别名
#方式一：使用as
SELECT last_name AS 姓,first_name AS 名 FROM employees;
#方拾二：省略as(使用空格)
SELECT last_name 姓,first_name 名 FROM employees;
#包含特殊字符使用""('')标注为字符串
SELECT last_name "姓 X",first_name 名 FROM employees;
```

**CONCAT()**  用于**连接两个字段**。许多数据库会使用空格把一个值填充为列宽，因此连接的结果会出现一些不必要的空格，使用 **TRIM()** 可以去除首尾空格。

```sql
SELECT CONCAT(TRIM(col1), '(', TRIM(col2), ')') AS concat_col
FROM mytable;  

# +
#只要有一方为null，则+和拼接都为null
SELECT CONCAT(first_name,' ',last_name) `name` FROM emplyees;
```

## 条件查询

where 关键字

条件查询：根据条件过滤原始表的数据，查询到想要的数据
语法：

```sql
select 要查询的字段|表达式|常量值|函数
from 表
where 条件;
```

下表显示了 WHERE 子句可用的操作符

| 操作符  |     说明     |
| :-----: | :----------: |
|    =    |     等于     |
|    <    |     小于     |
|    >    |     大于     |
| <> , != |    不等于    |
| <= , !> |   小于等于   |
| >= , !< |   大于等于   |
| BETWEEN | 在两个值之间 |
| IS NULL |  为 NULL 值  |

应该注意到，**NULL 与 0、空字符串都不同。**

**AND 和 OR**  用于**连接多个过滤条件**。优先处理 AND，当一个过滤表达式涉及到多个 AND 和 OR 时，可以使用 () 来决定优先级，使得优先级关系更清晰。

**IN**  操作符用于**匹配一组值**，其后**也可以接一个 SELECT 子句**，从而匹配子查询得到的一组值。

**NOT**  操作符用于否定一个条件。

分类：

### 1条件表达式

​	示例：`salary > 10000`
​	条件运算符：
​	`> ,< ,>=, <=, =, !=, <>`

### 2逻辑表达式

示例：`salary >10000 && salary < 20000`

#### 逻辑运算符：

and（&&）:两个条件如果同时成立，结果为true，否则为false
or(||)：两个条件只要有一个成立，结果为true，否则为false
not(!)：如果条件成立，则not后为false，否则为true

`between and` 等价于并简化了 >=   <= 语句
`in` 判断某字段的值是否属于in列表中的某一项，in中列表值类型必须一致或兼容

```mysql
SELECT * FROM employees WHERE job_id IN('IT_PROT','AD_VP');
```

`is null| is not null`
只能判断null值，= 和<> 不能判断null值
安全等于`<=>`
既能判断是否为null，也能判断其他类型

### 3模糊查询

LIKE



#### 通配符

通配符也是用在过滤语句中，但它只能用于文本字段。

- **%**  匹配 >=0 个任意字符；
- **_**  匹配 ==1 个任意字符；
- **[ ]**  可以**匹配集合内的字符**，例如 [ab] 将匹配字符 a 或者 b。用脱字符 ^ 可以对其进行否定，也就是不匹配集合内的字符。
- 特殊字符：使用转义字符

使用 **Like 来进行通配符匹配。**

```sql
SELECT *
FROM mytable
WHERE col LIKE '[^AB]%'; -- 不以 A 和 B 开头的任意文本
```

> 不要滥用通配符，==**通配符位于开头处匹配会非常慢。**==

## 排序查询	

- **ASC** : 升序(默认)
- **DESC** : 降序

```sql
语法：
select
	要查询的东西
from 表
where 条件	
order by 排序的字段|表达式|函数|别名 【asc|desc】,次要排序内容(通前面格式一致)
#默认升序
```



## 常见函数

各个 DBMS 的函数都是不相同的，因此不可移植，以下主要是 MySQL 的函数。

- 调用

  ```sql
   select 函数名（实参列表）【form 表】 
  ```

- 函数可以嵌套

- **分组函数，聚合函数，汇总函数**，是**同一种概念的不同称呼**。都是指**对一组值执行计算并返回单一的值**。

### 1单行函数

单行函数分为：字符串函数、数值函数、日期函数、转换函数、通用函数。**所有的单行函数可以在SQL语句的任意位置上出现。**

####   	1、字符函数

  - concat()拼接（字符串）	
  - substr()截取子串
  - upper()转换成大写	
  - lower()转换成小写	
  - trim()去前后指定的空格和字符	
  - ltrim()去左边空格	
  - rtrim()去右边空格	
  - replace()替换	
  - lpad()左填充	
  - rpad()右填充	
  - instr()返回子串第一次出现的索引，如果找不到返回0		
  - length() 获取**字节**个数 
    
#### 2数值函数

|    函数    |                       说明                       |
| :--------: | :----------------------------------------------: |
|  round()   |                     四舍五入                     |
|  floor()   |                     向下取整                     |
|   ceil()   |                     向上取整                     |
|   ABS()    |                      绝对值                      |
|   SQRT()   |                      平方根                      |
|   MOD()    |                       余数                       |
|   EXP()    |                       指数                       |
|    PI()    |                      圆周率                      |
|   RAND()   |                      随机数                      |
|   SIN()    |                       正弦                       |
|   COS()    |                       余弦                       |
|   TAN()    |                       正切                       |
|   mod()    | 取余 mod(a,b) = a-a/b*b<br/>（有效解决负数问题） |
| truncate() |                       截断                       |




​    



#### 3日期函数

- 日期格式: YYYY-MM-DD
- 时间格式: HH:MM:SS

|     函 数     | 说 明                              |
| :-----------: | :--------------------------------- |
|   AddDate()   | 增加一个日期(天、周等)             |
|   AddTime()   | 增加一个时间(时、分等)             |
|   CurDate()   | 返回当前系统日期                   |
|   CurTime()   | 返回当前系统时间                   |
|    Date()     | 返回日期时间的日期部分             |
|  DateDiff()   | 计算两个日期之差                   |
|  Date_Add()   | 高度灵活的日期运算函数             |
| Date_Format() | 返回一个格式化的日期或时间(字符)串 |
|     Day()     | 返回一个日期的天数部分             |
|  DayOfWeek()  | 对于一个日期，返回对应的星期几     |
|    Hour()     | 返回一个时间的小时部分             |
|   Minute()    | 返回一个时间的分钟部分             |
|    Month()    | 返回一个日期的月份部分             |
|     Now()     | 返回当前（系统）日期和时间         |
|   Second()    | 返回一个时间的秒部分               |
|    Time()     | 返回一个日期时间的时间部分         |
|    Year()     | 返回一个日期的年份部分             |
| str_to_date() | 将字符转换成日期                   |
|               |                                    |

```sql
mysql> SELECT NOW();
2018-4-14 20:25:11 
```

#### 4、流程控制函数

​	if (条件表达式，成立值，false值)处理双分支 ，和三元运算符相当
​	case语句 处理多分支
​		情况1：处理等值判断

```sql
case 要判断的字段或表达式
when 常量1 then 要显示的值1或语句1;
when 常量2 then 要显示的值2或语句2;
···
else 要显示的值n或语句n;
end

SELECT salary	init,department_id,
CASE department_id
WHEN 30 THEN salary*1.1
WHEN 40 THEN salary*1.2
WHEN 50 THEN salary*1.3
ELSE salary
END AS `new`
FROM employees;
```



		情况2：处理条件判断

```sql
case
when 常量1 then 要显示的值1或语句1;
when 常量2 then 要显示的值2或语句2;
···
else 要显示的值n或语句n;
end
#相当于多重if语句
SELECT salary,
CASE
WHEN salary > 20000 THEN 'a'
WHEN salary > 15000 THEN 'b'
WHEN salary > 10000 THEN 'b'
ELSE 'd'
END AS  grade
FROM employees;
```



#### 5、其他函数

​	version版本
​	database当前库
​	user当前连接用户

### 2分组(汇总，聚合)函数

*聚合函数*：**对一组值执行计算并返回单一的值**

又称**统计函数**,也成**汇总函数**，也称为**聚合函数**;分组函数是对**表中一组记录进行操作**，每组值**返回一个结果**，即首先要对表记录进行分组，然后再进对表记录进行分组，然后在进行操作汇总，每组返回一个结果，**分组是可能是整个表分为一个组**，也可能根据条件分成多组。

|  函 数  |      说 明       |
| :-----: | :--------------: |
|  AVG()  | 返回某列的平均值 |
| COUNT() |  返回某列的行数  |
|  MAX()  | 返回某列的最大值 |
|  MIN()  | 返回某列的最小值 |
|  SUM()  |  返回某列值之和  |

AVG() 会忽略 NULL 行。

使用 DISTINCT 可以让汇总函数值汇总不同的值。

```sql
SELECT AVG(DISTINCT col1) AS avg_col
FROM mytable;
```

特点：

1. 以上五个分组函数都忽略null值，除了`count(*)`

2. sum和`avg`一般用于处理数值型
   max、min、count可以处理任何数据类型

3. 都可以**搭配distinct使用，用于统计去重后的结果**

4. count的参数可以支持：
   字段、`*`、常量值，一般放1
> **建议使用 count(*)**

5. 可以搭配group by使用

   ```sql
   SELECT MAX(column_name) FROM table_name GROUP BY column_name;
   ```

#### SQL MAX() 语法

```mysql
SELECT MAX(column_name) FROM table_name;
```

## 分组查询

GROUP BY 语句，分组就是把**具有相同的数据值的行**放在**同一组**中，即根据**一个或多个列对结果集进行分组**。

可以对同一分组数据**使用汇总(分组)函数进行处理**，在分组的列上我们**可以使用 COUNT, SUM, AVG,等函数**，例如求分组数据的平均值等。

GROUP BY **自动按分组字段进行排序**，ORDER BY **也可以按汇总字段来进行排序。**

WHERE 过滤行，HAVING 过滤分组，**行过滤应当先于分组过滤。**

```mysql
SELECT column_name, function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name 
HAVING  column_name operator;

```

**分组规定:**

- GROUP BY 子句出现在 WHERE 子句之后，ORDER BY 子句之前；
- 除了**汇总（分组）字段**外，SELECT 语句中的**每一字段都必须在 GROUP BY 子句中给出；**
- NULL 的行会**单独分为一组**；
- 大多数 SQL 实现不支持 GROUP BY 列具有可变长度的数据类型。
- having后可以支持别名



```
mysql> SELECT * FROM employee_tbl;
+----+--------+---------------------+--------+
| id | name   | date                | signin |
+----+--------+---------------------+--------+
|  1 | 小明 | 2016-04-22 15:25:33 |      1 |
|  2 | 小王 | 2016-04-20 15:25:47 |      3 |
|  3 | 小丽 | 2016-04-19 15:26:02 |      2 |
|  4 | 小王 | 2016-04-07 15:26:14 |      4 |
|  5 | 小明 | 2016-04-11 15:26:40 |      4 |
|  6 | 小明 | 2016-04-04 15:26:54 |      2 |
+----+--------+---------------------+--------+
6 rows in set (0.00 sec)
```

接下来我们使用 GROUP BY 语句 将数据表按名字进行分组，并统计每个人有多少条记录：

```
mysql> SELECT name, COUNT(*) FROM   employee_tbl GROUP BY name;
+--------+----------+
| name   | COUNT(*) |
+--------+----------+
| 小丽 |        1 |
| 小明 |        3 |
| 小王 |        2 |
+--------+----------+
3 rows in set (0.01 sec)
```

### 使用 WITH ROLLUP

WITH ROLLUP 可以实现在**分组统计数据基础上再进行相同的统计（SUM,AVG,COUNT…）。**

例如我们将以上的数据表按名字进行分组，再统计每个人登录的次数：

```
mysql> SELECT name, SUM(signin) as signin_count FROM  employee_tbl GROUP BY name WITH ROLLUP;
+--------+--------------+
| name   | signin_count |
+--------+--------------+
| 小丽 |            2 |
| 小明 |            7 |
| 小王 |            7 |
| NULL   |           16 |
+--------+--------------+
4 rows in set (0.00 sec)
```

其中记录 NULL 表示所有人的登录次数。

我们可以使用 coalesce 来设置一个可以取代 NULL 的名称，coalesce 语法：

```
select coalesce(a,b,c);
```

参数说明：如果`a==null,则选择b；如果b==null,则选择c；如果a!=null,则选择a；如果a b c 都为null ，则返回为null（没意义）。`

以下实例中如果名字为空我们使用总数代替：

```mysql
mysql> SELECT coalesce(name, '总数'), SUM(signin) as signin_count FROM  employee_tbl GROUP BY name WITH ROLLUP;
+--------------------------+--------------+
| coalesce(name, '总数') | signin_count |
+--------------------------+--------------+
| 小丽                   |            2 |
| 小明                   |            7 |
| 小王                   |            7 |
| 总数                   |           16 |
+--------------------------+--------------+
4 rows in set (0.01 sec)
```

group by能用于多列去重

```sql
SELECT solution_id,s.problem_id,user_id,user_name,score FROM solution s,contest_problem cp
 where s.contest_id = 19 AND s.problem_id = cp.problem_id 
AND s.contest_id = cp.contest_id AND result = 0 GROUP BY s.problem_id,user_id
```

参考链接：[菜鸟教程—MySQL GROUP BY 语句](https://www.runoob.com/mysql/mysql-group-by-statement.html)

## 连接查询

连接用于连接多个表，**使用 JOIN 关键字**，并且**条件语句使用 ON** 而不是 WHERE。

**连接可以替换子查询**，并且比子查询的**效率一般会更快。**

可以用 AS 给列名、计算字段和表名取别名，给表名取别名是为了简化 SQL 语句以及连接相同表。

> MySQL**中的inner和outer可以省略**
>
> **建议写上，可读性更好**
>
> 在MySQL中主要区分内连接和外链接的根本原因并不是这两个关键字 如果SQL语句中 带有left join或者 left outer join时 那这条SQL语句一定是外连接， 在写SQL语句时这两个关键字都可以省略 ，**写上这两个关键字只是意味着可读性好**（）

语法：

```sql
select 字段，...
from 表1
【inner|left outer|right outer|cross】join 表2 on  连接条件
【inner|left outer|right outer|cross】join 表3 on  连接条件
【where 筛选条件】
【group by 分组字段】
【having 分组后的筛选条件】
【order by 排序的字段或表达式】
```



### 内连接

**内连接又称等值连接**，使用 INNER JOIN 关键字。

```sql
SELECT A.value, B.value
FROM tablea AS A INNER JOIN tableb AS B
ON A.key = B.key;
```

> **尽量使用INNER JOIN**，好处：语句上，连接条件和筛选条件实现了分离，简洁明了！

可以不明确使用 INNER JOIN，而使用**普通查询并在 WHERE 中将两个表中要连接的列用等值方法连接起来。**

```sql
SELECT A.value, B.value
FROM tablea AS A, tableb AS B
WHERE A.key = B.key;
```



**在没有条件语句**的情况下**返回笛卡尔积**。

扩展：

Cross join：（很少用）

**cross join**，交叉连接，实际上就是将两个表进行笛卡尔积运算，结果表的行数等于两表行数之积

#### 笛卡尔积

笛卡尔乘积是指在数学中，两个[集合](https://baike.baidu.com/item/集合)*X*和*Y*的笛卡尔积（Cartesian product），又称[直积](https://baike.baidu.com/item/直积)，表示为*X*×*Y*，第一个对象是*X*的成员而第二个对象是*Y*的所有可能[有序对](https://baike.baidu.com/item/有序对)的其中一个成员 [3] 。

假设集合A={a, b}，集合B={0, 1, 2}，则两个集合的笛卡尔积为{(a, 0), (a, 1), (a, 2), (b, 0), (b, 1), (b, 2)}。

类似的例子有，如果A表示某学校学生的集合，B表示该学校所有课程的集合，则A与B的笛卡尔积表示所有可能的选课情况。A表示所有声母的集合，B表示所有韵母的集合，那么A和B的笛卡尔积就为所有可能的汉字全拼。

**设A,B为集合，用A中元素为第一元素，B中元素为第二元素构成有序对，所有这样的有序对组成的集合叫做A与B的笛卡尔积，记作AxB.**

笛卡尔积的符号化为：

A×B={(x,y)|x∈A∧y∈B}

例如，A={a,b}, B={0,1,2}，则

A×B={(a, 0), (a, 1), (a, 2), (b, 0), (b, 1), (b, 2)}

B×A={(0, a), (0, b), (1, a), (1, b), (2, a), (2, b)}

<img src="mysql/2934349b033b5bb57f0eb50b36d3d539b700bc6e.jpg" style="zoom:50%;" />

### [¶](#自连接) 自连接

**自连接可以看成内连接的一种**，只是**连接的表是自身而已。**

一张员工表，包含员工姓名和员工所属部门，要找出与 Jim 处在同一部门的所有员工姓名。

子查询版本

```sql
SELECT name
FROM employee
WHERE department = (
      SELECT department
      FROM employee
      WHERE name = "Jim");
```

自连接版本

```sql
SELECT e1.name
FROM employee AS e1 INNER JOIN employee AS e2
ON e1.department = e2.department
      AND e2.name = "Jim";
```

### [¶](#自然连接) 自然连接

自然连接是把**同名列通过等值测试连接起来的**，同名列可以有多个。

**内连接和自然连接的区别**: 内连接提供连接的列，而自然连接**自动连接==所有同名列==。**

```sql
SELECT A.value, B.value
FROM tablea AS A NATURAL JOIN tableb AS B;
```

### [¶](#外连接) 外连接

```mysql
LEFT|RIGHT OUTER JOIN
```

外连接保留了**没有关联的那些行**。分为**左外连接，右外连接以及全外连接**，左外连接就是**保留左表没有关联的行，右表选择列置为null**。

检索所有顾客的订单信息，包括还没有订单信息的顾客。

```sql
SELECT Customers.cust_id, Orders.order_num
FROM Customers LEFT OUTER JOIN Orders
ON Customers.cust_id = Orders.cust_id;    
```

customers 表:

| cust_id | cust_name |
| :-----: | :-------: |
|    1    |     a     |
|    2    |     b     |
|    3    |     c     |

orders 表:

| order_id | cust_id |
| :------: | :-----: |
|    1     |    1    |
|    2     |    1    |
|    3     |    3    |
|    4     |    3    |

结果:

| cust_id | cust_name | order_id |
| :-----: | :-------: | :------: |
|    1    |     a     |    1     |
|    1    |     a     |    2     |
|    3    |     c     |    3     |
|    3    |     c     |    4     |
|    2    |     b     |   Null   |

### 总结

![1.jpg](https://pic.leetcode-cn.com/ad3df1c4ecc7d2dbe85f92cdde8ec9a731fdd20dc4c5629ecb372b21de26c682-1.jpg)

## 子查询

子查询中只能返回一个字段的数据。

可以将子查询的结果作为 WHRER 语句的过滤条件:

```sql
SELECT *
FROM mytable1
WHERE col1 IN (SELECT col2
               FROM mytable2);
```

下面的语句可以检索出客户的订单数量，子**查询语句会对第一个查询检索出的每个客户执行一次**:

```sql
SELECT cust_name, (SELECT COUNT(*)
                   FROM Orders
                   WHERE Orders.cust_id = Customers.cust_id)
                   AS orders_num
FROM Customers
ORDER BY cust_name;
```



### 含义：

```
一条查询语句中又嵌套了另一条完整的select语句，其中被嵌套的select语句，称为子查询或内查询
在外面的查询语句，称为主查询或外查询
```

特点：

```
1、子查询都放在小括号内
2、子查询可以放在from后面、select后面、where后面、having后面，但一般放在条件的右侧
3、子查询优先于主查询执行，主查询使用了子查询的执行结果
4、子查询根据查询结果的行数不同分为以下两类：
① 单行子查询
	结果集只有一行
	一般搭配单行操作符使用：> < = <> >= <= 
	非法使用子查询的情况：
	a、子查询的结果为一组值
	b、子查询的结果为空
	
② 多行子查询
	结果集有多行
	一般搭配多行操作符使用：any、all、in、not in
	in： 属于子查询结果中的任意一个就行
	any和all往往可以用其他查询代替
```

```mysql
SELECT solution_id,problem_id,user_id,MIN(runtime) as runtime FROM solution
        WHERE contest_id = 19 AND result = 0 GROUP BY problem_id,user_id
```



## 联合查询，组合查询

使用  **UNION**  来组合两个查询，如果第一个查询返回 M 行，第二个查询返回 N 行，那么**组合查询的结果一般为 M+N 行**。

每个查询必须**包含相同的列、表达式和聚集函数。**

**默认会去除相同行**，如果**需要保留相同行，使用 UNION ALL。**

只能包含一个 ORDER BY 子句，并且必须位于语句的最后。

语法：

```sql
select 字段|常量|表达式|函数 【from 表】 【where 条件】 union 【all】
select 字段|常量|表达式|函数 【from 表】 【where 条件】 union 【all】
.....
select 字段|常量|表达式|函数 【from 表】 【where 条件】
```

```sql
SELECT col
FROM mytable
WHERE col = 1
UNION
SELECT col
FROM mytable
WHERE col =2; 
```

# 视图
**视图是虚拟的表**，本身不包含数据，也就不能对其进行索引操作。

对视图的操作**和对普通表的操作一样**。

视图具有如下好处:

- 简化复杂的 SQL 操作，比如复杂的连接；
- 只使用实际表的一部分数据；
- 通过**只给用户访问视图的权限，保证数据的安全性**；
- 更改数据格式和表示。

```sql
CREATE VIEW myview AS
SELECT Concat(col1, col2) AS concat_col, col3*col4 AS compute_col
FROM mytable
WHERE col5 = val;
```

### 视图的创建
​	语法：

```mysql
CREATE VIEW  视图名
AS
查询语句;
```

### 视图的增删改查
​	1、查看视图的数据 ★


```
SELECT * FROM my_v4;
SELECT * FROM my_v1 WHERE last_name='Partners';

2、插入视图的数据
INSERT INTO my_v4(last_name,department_id) VALUES('虚竹',90);

3、修改视图的数据

UPDATE my_v4 SET last_name ='梦姑' WHERE last_name='虚竹';
```


	4、删除视图的数据
	DELETE FROM my_v4;

### 某些视图不能更新
​	包含以下关键字的sql语句：分组函数、distinct、group  by、having、union或者union all
​	常量视图
​	Select中包含子查询
​	join
​	from一个不能更新的视图
​	where子句的子查询引用了from子句中的表
### 视图逻辑的更新
​	#方式一：
​	CREATE OR REPLACE VIEW test_v7
​	AS
​	SELECT last_name FROM employees
​	WHERE employee_id>100;
​	

	#方式二:
	ALTER VIEW test_v7
	AS
	SELECT employee_id FROM employees;
	
	SELECT * FROM test_v7;

### 视图的删除
​	DROP VIEW test_v1,test_v2,test_v3;
### 视图结构的查看	
​	DESC test_v7;
​	SHOW CREATE VIEW test_v7;

著作权归https://pdai.tech所有。 链接：https://pdai.tech/md/db/sql-lan/sql-lan.html

# 存储过程

存储**过程**可以看成是**对一系列 SQL 操作的批处理。**

使用存储过程的好处:

- 代码封装，保证了一定的安全性；
- 代码复用；
- 由于是**预先编译，因此具有很高的性能。**

命令行中创建存储过程需要自定义分隔符，因为命令行是以 ; 为结束符，而存储过程中也包含了分号，因此会错误把这部分分号当成是结束符，造成语法错误。

**包含 in、out 和 inout 三种参数。**

给**变量赋值都需要用 select into 语句。**

每次**只能给一个变量赋值，不支持集合的操作。**

## 创建存储过程

语法：

```mysql
create procedure 存储过程名(in|out|inout 参数名  参数类型,...)
begin
	存储过程体

end
```

类似于方法：

```mysql
修饰符 返回类型 方法名(参数类型 参数名,...){

	方法体;
}
```

参数类型：参数前面的符号的意思
in:该参数**只能作为输入** （该参数不能做返回值）
out：该参数**只能作为输出**（该参数只能做返回值）
inout：**既能做输入又能做输出**

> 注意：in、out、inout都可以在**一个存储过程中带多个**

### 注意

1、需要设置新的结束标记

```mysql
delimiter 新的结束标记
```

示例：

```mysql
delimiter $

CREATE PROCEDURE 存储过程名(IN|OUT|INOUT 参数名  参数类型,...)
BEGIN
	sql语句1;
	sql语句2;

END $
```

2、存储过程体中可以有多条sql语句，如果仅仅一条sql语句，则可以省略begin end

## 调用存储过程

```mysql
call 存储过程名(实参列表)
```

## 用例

```mysql
delimiter //

create procedure myprocedure( out ret int )
    begin
        declare y int;
        select sum(col1)
        from mytable
        into y;
        select y*y into ret;
    end //

delimiter ;  
```



```mysql
call myprocedure(@ret);
select @ret;
```

著作权归https://pdai.tech所有。 链接：https://pdai.tech/md/db/sql-lan/sql-lan.html

# 游标

在存储过程中使用游标可以**对一个结果集进行移动遍历。**

游标主要用于交互式应用，其中用户需要对数据集中的任意行进行浏览和修改。

使用游标的四个步骤:

1. 声明游标，这个过程没有实际检索出数据；
2. 打开游标；
3. 取出数据；
4. 关闭游标；

```mysql
delimiter //
create procedure myprocedure(out ret int)
    begin
        declare done boolean default 0;

        declare mycursor cursor for
        select col1 from mytable;
        # 定义了一个 continue handler，当 sqlstate '02000' 这个条件出现时，会执行 set done = 1
        declare continue handler for sqlstate '02000' set done = 1;

        open mycursor;

        repeat
            fetch mycursor into ret;
            select ret;
        until done end repeat;

        close mycursor;
    end //
 delimiter ; 
```

著作权归https://pdai.tech所有。 链接：https://pdai.tech/md/db/sql-lan/sql-lan.html

# 触发器

触发器会在某个表执行以下语句（修改语句）时而自动执行: DELETE、INSERT、UPDATE。

触发器必须指定在语句**执行之前还是之后**自动执行，之前执行使用 BEFORE 关键字，之后执行使用 AFTER 关键字。BEFORE 用于**数据验证和净化**，AFTER 用于**审计跟踪**，将修改记录到另外一张表中。

INSERT 触发器包含一个名为 **NEW 的虚拟表**。

```sql
CREATE TRIGGER mytrigger AFTER INSERT ON mytable
FOR EACH ROW SELECT NEW.col into @result;

SELECT @result; -- 获取结果   
```

DELETE 触发器包含一个名为 **OLD 的虚拟表**，并且是只读的。

UPDATE 触发器包含**一个名为 NEW 和一个名为 OLD 的虚拟表**，其中 **NEW 是可以被修改的**，而 OLD 是只读的。

MySQL 不允许在触发器中使用 CALL 语句，也就是不能调用存储过程。

著作权归https://pdai.tech所有。 链接：https://pdai.tech/md/db/sql-lan/sql-lan.html





# 函数

### 创建函数

学过的函数：LENGTH、SUBSTR、CONCAT等
语法：

```
CREATE FUNCTION 函数名(参数名 参数类型,...) RETURNS 返回类型
BEGIN
	函数体

END

```

### 调用函数
​	SELECT 函数名（实参列表）





### 函数和存储过程的区别

```
		关键字		调用语法	返回值			应用场景
函数		FUNCTION	SELECT 函数()	只能是一个		一般用于查询结果为一个值并返回时，当有返回值而且仅仅一个
存储过程	PROCEDURE	CALL 存储过程()	可以有0个或多个		一般用于更新
```

# 字符集

基本术语:

- 字符集为字母和符号的集合；
- 编码为某个字符集成员的内部表示；
- 校对字符指定如何比较，主要用于排序和分组。

除了给表指定字符集和校对外，也可以给列指定:

```mysql
CREATE TABLE mytable
(col VARCHAR(10) CHARACTER SET latin COLLATE latin1_general_ci )
DEFAULT CHARACTER SET hebrew COLLATE hebrew_general_ci;
```

可以在排序、分组时指定校对:

```sql
SELECT *
FROM mytable
ORDER BY col COLLATE latin1_general_ci;  
```

# 增删改，DML语言

DML（Data Manipulation Language），数据操纵语言，即增删改，INSERT、UPDATE、DELETE。

数据操纵语言DML主要有三种形式：
1) 插入：INSERT
2) 更新：UPDATE
3) 删除：DELETE

## 插入

语法：

```mysql
insert into 表名(字段名，...)
values(值1，...);
INSERT INTO mytable(col1, col2)
VALUES(val1, val2);
```

特点：

```
1、字段类型和值类型一致或兼容，而且一一对应
2、可以为空的字段，可以不用插入值，或用null填充
3、不可以为空的字段，必须插入值
4、字段个数和值的个数必须一致
5、字段可以省略，但默认所有字段，并且顺序和表中的存储顺序一致
```

插入检索出来的数据

```sql
INSERT INTO mytable1(col1, col2)
SELECT col1, col2
FROM mytable2;
```

将一个表的内容插入到一个新表

```sql
CREATE TABLE newtable AS
SELECT * FROM mytable;
```

## 修改（更新）

修改单表语法：

```mysql
update 表名 set 字段=新值,字段=新值
【where 条件】
UPDATE mytable
SET col = val
WHERE id = 1;
```

修改多表语法：

```mysql
update 表1 别名1,表2 别名2
set 字段=新值，字段=新值
where 连接条件
and 筛选条件
```



## 删除

方式1：delete语句 

单表的删除： ★

```mysql
delete from 表名
【where 筛选条件】
DELETE FROM mytable
WHERE id = 1;
```

多表的删除：

```
delete 别名1，别名2
from 表1 别名1，表2 别名2
where 连接条件
and 筛选条件;
```

方式2：truncate语句

**TRUNCATE TABLE** 可以清空表，也就是删除所有行。

> truncate v. 截断,截取

```mysql
truncate table 表名
TRUNCATE TABLE mytable;
```

两种方式的区别【面试题】删除

使用更新和删除操作时一定要用 WHERE 子句，不然会把整张表的数据都破坏。可以先用 SELECT 语句进行测试，防止错误删除。	

1.truncate不能加where条件，而delete可以加where条件

2.truncate的效率高一丢丢

3.truncate 删除带自增长的列的表后，如果再插入数据，数据从1开始
#delete 删除带自增长列的表后，如果再插入数据，数据从上一次的断点处开始

4.truncate删除不能回滚，delete删除可以回滚

# 定义-DDL语句，

DDL（data definition language）：数据库模式定义语言

数据定义语言，DDL用来**创建数据库中的各种对象--**---表、视图、索引、同义词、聚簇等如：CREATE TABLE / VIEW / INDEX / SYN / CLUSTER| 表 视图 索引 同义词 簇。DDL操作是隐性提交的！不能rollback。

DDL主要是用在**定义或改变**表（TABLE）的结构，数据类型，表之间的链接和约束等初始化工作上，他们大多在建立表时使用

##  数据库、表的操作(命令)

创建数据库

```mysql
CREATE DATABASE IF NOT EXISTS yoj DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

创建数据库，该命令的作用：

- \1. 如果数据库不存在则创建，存在则不创建。

- \2. 创建yoj数据库，并设定编码集为utf8

  

删除数据库。

```sql
DROP DATABASE dbName;
```

创建数据库。

```sql
create database yoj;
```

  1.查看当前所有的数据库

```mysql
show databases;
```

2.打开(使用)指定的库

```mysql
use 库名
```

3.查看当前库的所有表

```mysql
show tables;
```

4.查看其它库的所有表

```mysql
show tables from 库名;
```

5.创建表

```mysql
create table 表名(

	列名 列类型,
	列名 列类型，
	。。。

);

CREATE TABLE mytable (
  id INT NOT NULL AUTO_INCREMENT,
  col1 INT NOT NULL DEFAULT 1,
  col2 VARCHAR(45) NULL,
  col3 DATE NULL,
  PRIMARY KEY (`id`)
);
```

6.查看表结构

```mysql
desc 表名;
```

## 修改表结构

添加列

```sql
ALTER TABLE mytable
ADD col CHAR(20);
```

删除列

```sql
ALTER TABLE mytable
DROP COLUMN col;
```

删除表

```sql
DROP TABLE mytable;
```

### 修改字段类型和列级约束

```mysql
ALTER TABLE studentinfo MODIFY COLUMN borndate DATE ;
```

#### 唯一约束（UNIQUE KEY）

MySQL唯一约束（Unique Key）要求**该列唯一，允许为空**，但只能出现一个空值。唯一约束可以确保一列或者几列不出现重复值。

##### 在创建表时设置唯一约束

在定义完列之后直接使用 UNIQUE 关键字指定唯一约束，语法规则如下：

<字段名> <数据类型> UNIQUE

【实例 1】创建数据表 tb_dept2，指定部门的名称唯一，输入的 SQL 语句和运行结果如下所示。

CREATE TABLE tb_dept2
(
     id INT(11) PRIMARY KEY,
     name VARCHAR(22) UNIQUE,
     location VARCHAR(50)
);

查询tb_dept2结构

mysql> DESC tb_dept2;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| id       | int(11)     | NO   | PRI | NULL    |       |
| name     | varchar(22) | YES  | UNI | NULL    |       |
| location | varchar(50) | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+
3 rows in set (0.03 sec)

UNI 就是唯一约束

提示：UNIQUE 和 PRIMARY KEY 的区别：一个表可以有多个字段声明为 UNIQUE，但只能有一个 PRIMARY KEY 声明；声明为 PRIMAY KEY 的列不允许有空值，但是声明为 UNIQUE 的字段允许空值的存在。

因为是创建时候指定的所以他的唯一约束名称就是他本身

##### 在修改表时添加唯一约束

在修改表时添加唯一约束的语法格式为：

```mysql
ALTER TABLE <数据表名> ADD CONSTRAINT <唯一约束名> UNIQUE(<列名>);
```


【实例 2】修改数据表 tb_dept1，指定部门的名称唯一，输入的 SQL 语句和运行结果如下所示。
```mysql
ALTER TABLE tb_dept1 ADD CONSTRAINT unique_name UNIQUE(name);
```


查询tb_dept1结构

```bash
mysql>  DESC tb_dept1;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| id       | int(11)     | NO   | PRI | NULL    |       |
| name     | varchar(22) | NO   | UNI | NULL    |       |
| location | varchar(50) | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+
3 rows in set (0.04 sec)
```

删除唯一约束

在 MySQL 中删除唯一约束的语法格式如下：

ALTER TABLE <表名> DROP INDEX <唯一约束名>;
1
【实例 3】删除数据表 tb_dept1 中的唯一约束 unique_name，输入的 SQL 语句和运行结果如下所示。

ALTER TABLE tb_dept1
DROP INDEX unique_name;
1
2
查询tb_dept1结构

mysql> DESC tb_dept1;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| id       | int(11)     | NO   | PRI | NULL    |       |
| name     | varchar(22) | NO   |     | NULL    |       |
| location | varchar(50) | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+
3 rows in set (0.03 sec)


可以发现name的key 没有UNI了


参考链接：https://blog.csdn.net/weixin_45203607/article/details/120248076

```
7.查看服务器的版本
方式一：登录到mysql服务端
select version();
方式二：没有登录到mysql服务端
mysql --version
或
mysql --V
```

## 库和表的管理

库的管理：

```
一、创建库
create database 库名
二、删除库
drop database 库名
```

表的管理：

	# 1.创建表

```
CREATE TABLE IF NOT EXISTS stuinfo(
	stuId INT,
	stuName VARCHAR(20),
	gender CHAR,
	bornDate DATETIME
```


	);
	
	DESC studentinfo;

## 2.修改表 alter

```

语法：ALTER TABLE 表名 ADD|MODIFY|DROP|CHANGE COLUMN 字段名 【字段类型】;

#①修改字段名
ALTER TABLE studentinfo CHANGE  COLUMN sex gender CHAR;

#②修改表名
ALTER TABLE stuinfo RENAME [TO]  studentinfo;
#③修改字段类型和列级约束
ALTER TABLE studentinfo MODIFY COLUMN borndate DATE ;

#④添加字段

ALTER TABLE studentinfo ADD COLUMN email VARCHAR(20) first;
#⑤删除字段
ALTER TABLE studentinfo DROP COLUMN email;
```




​	# 3.删除表
​	
​	DROP TABLE [IF EXISTS] studentinfo;


​	

###  常见类型

```
整型：
	
小数：
	浮点型
	定点型
字符型：
日期型：
Blob类型：
```



### 常见约束

```
NOT NULL
DEFAULT
UNIQUE
CHECK
PRIMARY KEY
FOREIGN KEY
```

## 流程控制结构

### 系统变量
一、全局变量

作用域：针对于所有会话（连接）有效，但不能跨重启

```
查看所有全局变量
SHOW GLOBAL VARIABLES;
查看满足条件的部分系统变量
SHOW GLOBAL VARIABLES LIKE '%char%';
查看指定的系统变量的值
SELECT @@global.autocommit;
为某个系统变量赋值
SET @@global.autocommit=0;
SET GLOBAL autocommit=0;
```

二、会话变量

作用域：针对于当前会话（连接）有效

```
查看所有会话变量
SHOW SESSION VARIABLES;
查看满足条件的部分会话变量
SHOW SESSION VARIABLES LIKE '%char%';
查看指定的会话变量的值
SELECT @@autocommit;
SELECT @@session.tx_isolation;
为某个会话变量赋值
SET @@session.tx_isolation='read-uncommitted';
SET SESSION tx_isolation='read-committed';

```

###自定义变量
一、用户变量

声明并初始化：

```
SET @变量名=值;
SET @变量名:=值;
SELECT @变量名:=值;

```

赋值：

```
方式一：一般用于赋简单的值
SET 变量名=值;
SET 变量名:=值;
SELECT 变量名:=值;

```

```
方式二：一般用于赋表 中的字段值
SELECT 字段名或表达式 INTO 变量
FROM 表;

```

使用：

```
select @变量名;

```

二、局部变量

声明：

```
declare 变量名 类型 【default 值】;

```

赋值：

```
方式一：一般用于赋简单的值
SET 变量名=值;
SET 变量名:=值;
SELECT 变量名:=值;

```

```
方式二：一般用于赋表 中的字段值
SELECT 字段名或表达式 INTO 变量
FROM 表;

```

使用：

```
select 变量名
```



二者的区别：

```
		作用域			定义位置		语法
```

用户变量	当前会话		会话的任何地方		加@符号，不用指定类型
局部变量	定义它的BEGIN END中 	BEGIN END的第一句话	一般不用加@,需要指定类型

###分支
一、if函数
	语法：if(条件，值1，值2)
	特点：可以用在任何位置

二、case语句

语法：

```
情况一：类似于switch
case 表达式
when 值1 then 结果1或语句1(如果是语句，需要加分号) 
when 值2 then 结果2或语句2(如果是语句，需要加分号)
...
else 结果n或语句n(如果是语句，需要加分号)
end 【case】（如果是放在begin end中需要加上case，如果放在select后面不需要）

情况二：类似于多重if
case 
when 条件1 then 结果1或语句1(如果是语句，需要加分号) 
when 条件2 then 结果2或语句2(如果是语句，需要加分号)
...
else 结果n或语句n(如果是语句，需要加分号)
end 【case】（如果是放在begin end中需要加上case，如果放在select后面不需要）
```

特点：
	可以用在任何位置

三、if elseif语句

语法：

```
if 情况1 then 语句1;
elseif 情况2 then 语句2;
...
else 语句n;
end if;
```

特点：
	只能用在begin end中！！！！！！！！！！！！！！！

三者比较：
			应用场合
	if函数		简单双分支
	case结构	等值判断 的多分支
	if结构		区间判断 的多分支

###循环

语法：

```
【标签：】WHILE 循环条件  DO
	循环体
END WHILE 【标签】;
```

特点：

```
只能放在BEGIN END里面

如果要搭配leave跳转语句，需要使用标签，否则可以不用标签

leave类似于java中的break语句，跳出所在循环！！！
```

# DCL,数据控制，事务，权限

DCL,数据控制语言

数据控制语言DCL用来授予或回收访问数据库的某种特权，并控制**数据库操纵事务发生的时间及效果**，对数据库实行监视等。如：
1) GRANT：授权。
2) ROLLBACK [WORK] TO [SAVEPOINT]：回退到某一点。回滚---ROLLBACK回滚命令使数据库状态回到上次最后提交的状态。其格式为：SQL>ROLLBACK;
3) COMMIT [WORK]：提交。在数据库的插入、删除和修改操作时，只有当事务在提交到数据库时才算完成。在事务提交前，只有操作数据库的这个人才能有权看到所做的事情，别人只有在最后提交完成后才可以看到。提交数据有三种类型：显式提交、隐式提交及自动提交。下面分别说明这三种类型。

(1) 显式提交
用COMMIT命令直接完成的提交为显式提交。其格式为：SQL>COMMIT；

(2) 隐式提交
用SQL命令间接完成的提交为隐式提交。这些命令是：ALTER，AUDIT，COMMENT，CONNECT，CREATE，DISCONNECT，DROP，EXIT，GRANT，NOAUDIT，QUIT，REVOKE，RENAME。

(3) 自动提交
若把AUTOCOMMIT设置为ON，则在插入、修改、删除语句执行后，系统将自动进行提交，这就是自动提交。其格式为：SQL>SET AUTOCOMMIT ON；

## 事务管理

基本术语:

- 事务(transaction)指一组 SQL 语句；
- 回退(rollback)指撤销指定 SQL 语句的过程；
- 提交(commit)指将未存储的 SQL 语句结果写入数据库表；
- 保留点(savepoint)指事务处理中设置的临时占位符(placeholder)，你可以**对它发布回退(与回退整个事务处理不同)。**

不能回退 SELECT 语句，回退 SELECT 语句也没意义；也不能回退 CREATE 和 DROP 语句。

MySQL 的事务提交默认是**隐式提交**，每执行一条语句**就把这条语句当成一个事务然后进行提交**。当出现 `START TRANSACTION` 语句时，**会关闭隐式提交**；当 `COMMIT 或 ROLLBACK` 语句执行后，**事务会自动关闭，重新恢复隐式提交。**

通过**设置 autocommit 为 0 可以取消自动提交**；autocommit 标记是**针对每个连接**而不是针对服务器的。

如果没有设置保留点，ROLLBACK 会回退到 START TRANSACTION 语句处；如果设置了保留点，并且在 **ROLLBACK 中指定该保留点**，则会**回退到该保留点**。

```mysql
START TRANSACTION
// ...
SAVEPOINT delete1
// ...
ROLLBACK TO delete1
// ...
COMMIT   
```

## 数据库事务

### 含义

​	通过一组逻辑操作单元（一组DML——sql语句），将数据从一种状态切换到另外一种状态

### 特点

​	（ACID）

- 原子性：要么都执行，要么都回滚
- 一致性：保证数据的状态操作前和操作后保持一致
- 隔离性：多个事务同时操作相同数据库的同一个数据时，一个事务的执行不受另外一个事务的干扰
- 持久性：一个事务一旦提交，则数据将持久化到本地，除非其他事务对其进行修改

相关步骤：

```
1、开启事务
2、编写事务的一组逻辑操作单元（多条sql语句）
3、提交事务或回滚事务
```

###  事务的分类：

隐式事务，没有明显的开启和结束事务的标志

```
比如
insert、update、delete语句本身就是一个事务
```

显式事务，具有明显的开启和结束事务的标志

```
	1、开启事务
	取消自动提交事务的功能
	
	2、编写事务的一组逻辑操作单元（多条sql语句）
	insert
	update
	delete
	
	3、提交事务或回滚事务
```

###  使用到的关键字

```
set autocommit=0;
start transaction;
commit;
rollback;

savepoint  断点
commit to 断点
rollback to 断点
```

### 事务的隔离级别:

事务并发问题如何发生？

```
当多个事务同时操作同一个数据库的相同数据时
```

事务的并发问题有哪些？

```
脏读：一个事务读取到了另外一个事务未提交的数据
不可重复读：同一个事务中，多次读取到的数据不一致
幻读：一个事务读取数据时，另外一个事务进行更新，导致第一个事务读取到了没有更新的数据
```

如何避免事务的并发问题？

```
通过设置事务的隔离级别
1、READ UNCOMMITTED
2、READ COMMITTED 可以避免脏读
3、REPEATABLE READ 可以避免脏读、不可重复读和一部分幻读
4、SERIALIZABLE可以避免脏读、不可重复读和幻读
```

设置隔离级别：

```
set session|global  transaction isolation level 隔离级别名;
```

查看隔离级别：

```
select @@tx_isolation;
```

著作权归https://pdai.tech所有。 链接：https://pdai.tech/md/db/sql-lan/sql-lan.html

## 权限管理

MySQL 的账户信息保存在 mysql 这个数据库中。

```sql
USE mysql;
SELECT user FROM user;
```

**创建账户**

新创建的账户没有任何权限。

```sql
CREATE USER myuser IDENTIFIED BY 'mypassword';
```

**修改账户名**

```mysql
RENAME myuser TO newuser;
```

**删除账户**

```sql
DROP USER myuser;
```

**查看权限**

```mysql
SHOW GRANTS FOR myuser;
```

**授予权限**

账户用 username@host 的形式定义，username@% 使用的是默认主机名。

```mysql
GRANT SELECT, INSERT ON mydatabase.* TO myuser; 
```

**删除权限**

GRANT 和 REVOKE 可在几个层次上控制访问权限:

- 整个服务器，使用 GRANT ALL 和 REVOKE ALL；
- 整个数据库，使用 ON database.*；
- 特定的表，使用 ON database.table；
- 特定的列；
- 特定的存储过程。

```sql
REVOKE SELECT, INSERT ON mydatabase.* FROM myuser; 
```

**更改密码**

必须使用 Password() 函数

```sql
SET PASSWROD FOR myuser = Password('new_password'); 
```

# SQL语言 - SQL语句练习

[SQL语言 - SQL语句练习](https://pdai.tech/md/db/sql-lan/sql-lan-pratice.html)

[leetcode数据库相关练习](https://leetcode-cn.com/problemset/database/)

```
,[2,200],[3,300]
```

## 查看第N高的数据，没有则返回为null

```mysql
/*临时表解决null问题
select NULL，返回null值
n为数值
*/
SELECT
    (SELECT DISTINCT salary AS SecondHighestSalary 
    FROM Employee ORDER BY salary DESC LIMIT n-1,1)
    AS SecondHighestSalary
```



# SQL语言 - SQL语句优化

> 最后，再总结一些SQL语句的优化建议。@pdai

- SQL语言 - SQL语句优化
  - [负向查询不能使用索引](#负向查询不能使用索引)
  - [前导模糊查询不能使用索引](#前导模糊查询不能使用索引)
  - [数据区分不明显的不建议创建索引](#数据区分不明显的不建议创建索引)
  - [字段的默认值不要为 null](#字段的默认值不要为-null)
  - [在字段上进行计算不能命中索引](#在字段上进行计算不能命中索引)
  - [最左前缀问题](#最左前缀问题)
  - [如果明确知道只有一条记录返回](#如果明确知道只有一条记录返回)
  - [不要让数据库帮我们做强制类型转换](#不要让数据库帮我们做强制类型转换)
  - [如果需要进行 join 的字段两表的字段类型要相同](#如果需要进行-join-的字段两表的字段类型要相同)
- [参考](#参考)

## [¶](#负向查询不能使用索引) 负向查询不能使用索引

```sql
select name from user where id not in (1,3,4);
  
        @pdai: 代码已经复制到剪贴板
    
```

1

应该修改为:

```text
select name from user where id in (2,5,6);
  
        @pdai: 代码已经复制到剪贴板
    
```

1

## [¶](#前导模糊查询不能使用索引) 前导模糊查询不能使用索引

如:

```sql
select name from user where name like '%zhangsan'
  
        @pdai: 代码已经复制到剪贴板
    
```

1

非前导则可以:

```sql
select name from user where name like 'zhangsan%'
  
        @pdai: 代码已经复制到剪贴板
    
```

1

建议可以考虑使用 `Lucene` 等全文索引工具来代替频繁的模糊查询。

## [¶](#数据区分不明显的不建议创建索引) 数据区分不明显的不建议创建索引

如 user 表中的性别字段，可以明显区分的才建议创建索引，如身份证等字段。

## [¶](#字段的默认值不要为-null) 字段的默认值不要为 null

这样会带来和预期不一致的查询结果。

## [¶](#在字段上进行计算不能命中索引) 在字段上进行计算不能命中索引

```sql
select name from user where FROM_UNIXTIME(create_time) < CURDATE();
  
        @pdai: 代码已经复制到剪贴板
    
```

1

应该修改为:

```sql
select name from user where create_time < FROM_UNIXTIME(CURDATE());
  
        @pdai: 代码已经复制到剪贴板
    
```

1

## [¶](#最左前缀问题) 最左前缀问题

如果给 user 表中的 username pwd 字段创建了复合索引那么使用以下SQL 都是可以命中索引:

```sql
select username from user where username='zhangsan' and pwd ='axsedf1sd'

select username from user where pwd ='axsedf1sd' and username='zhangsan'

select username from user where username='zhangsan'
  
        @pdai: 代码已经复制到剪贴板
    
```

1
2
3
4
5

但是使用

```sql
select username from user where pwd ='axsedf1sd'
  
        @pdai: 代码已经复制到剪贴板
    
```

是不能命中索引的。

## [¶](#如果明确知道只有一条记录返回) 如果明确知道只有一条记录返回

```sql
select name from user where username='zhangsan' limit 1
```

可以提高效率，可以让数据库停止游标移动。

## [¶](#不要让数据库帮我们做强制类型转换) 不要让数据库帮我们做强制类型转换

```sql
select name from user where telno=18722222222
```

这样虽然可以查出数据，但是会导致全表扫描。

需要修改为

```text
select name from user where telno='18722222222'
```

## [¶](#如果需要进行-join-的字段两表的字段类型要相同) 如果需要进行 join 的字段两表的字段类型要相同

不然也不会命中索引。

## [¶](#参考) 参考

- https://github.com/realpdai/JCSprout/blob/master/MD/SQL-optimization.md
- http://blog.csdn.net/u010003835/article/details/54381080
- - [MySQL 大表优化方案](https://mp.weixin.qq.com/s/BMQC2oJlhLoeBDtveXgHpw)

# SQL的常见命令

```
show databases； 查看所有的数据库
use 库名； 打开指定 的库
show tables ; 显示库中的所有表
show tables from 库名;显示指定库中的所有表
create table 表名(
	字段名 字段类型,	
	字段名 字段类型
); 创建表

desc 表名; 查看指定表的结构
select * from 表名;显示表中的所有数据
```

```sql
create database db_name
```

## 修改字段编码

```sql
alter database name character set utf8;#修改数据库成utf8的.
alter table type character set utf8;#修改表用utf8.
alter table type modify type_name varchar(50) CHARACTER SET utf8;#修改字段用utf8
```

# mysqldump数据导出

## [MySQL mysqldump数据导出详解](https://www.cnblogs.com/chenmh/p/5300370.html)

mysqldump是导出数据过程中使用非常频繁的一个工具

**mysqldump备份**：

```
mysqldump -u用户名 -p密码 -h主机 数据库 a -w "sql条件" --lock-all-tables > 路径
```

案例：

```
mysqldump -uroot -p1234 -hlocalhost db1 a -w "id in (select id from b)" --lock-all-tables > c:\aa.txt
```

**mysqldump还原**：

mysqldump -u用户名 -p密码 -h主机 数据库 < 路径

案例：

mysql -uroot -p1234 db1 < c:\aa.txt

**mysqldump按条件导出**：

mysqldump -u用户名 -p密码 -h主机 数据库  a --where "条件语句" --no-建表> 路径

mysqldump -uroot -p1234 dbname a --where "tag='88'" --no-create-info> c:\a.sql

**mysqldump按导入**：

```
mysqldump -u用户名 -p密码 -h主机 数据库 < 路径
```

1.导出所有数据库

该命令会导出包括系统数据库在内的所有数据库

```
mysqldump -uroot -proot --all-databases >/tmp/all.sql
```

2.导出db1、db2两个数据库的所有数据

```
mysqldump -uroot -proot --databases db1 db2 >/tmp/user.sql
```

3.导出db1中的a1、a2表

注意导出指定表只能针对一个数据库进行导出，且导出的内容中和导出数据库也不一样，导出指定表的导出文本中没有创建数据库的判断语句，只有删除表-创建表-导入数据

```
mysqldump -uroot -proot --databases db1 --tables a1 a2  >/tmp/db1.sql
```

4.条件导出，导出db1表a1中id=1的数据

如果多个表的条件相同可以一次性导出多个表

字段是整形

```
mysqldump -uroot -proot --databases db1 --tables a1 --where='id=1'  >/tmp/a1.sql
```

# my

## mysql安装

本文mysql的安装环境为win10 64位，mysql版本为MySQL5.7

1、运行 —— [cmd](https://so.csdn.net/so/search?q=cmd&spm=1001.2101.3001.7020) ,打开面板，切换到mysql安装的bin目录下

![img](https://img-blog.csdnimg.cn/20181121113205147.jpg)

2、在[命令行](https://so.csdn.net/so/search?q=命令行&spm=1001.2101.3001.7020)输入 mysql -u root -p 登录 mysql，可以随意输入一个密码，返回”Can't connect to MySQL server on localhost (10061)”错误

![img](https://img-blog.csdnimg.cn/20181121113324478.jpg)

3、将mysql加入到Windows的服务中。切换到mysql安装目录下的bin文件夹，命令行运行"mysqld --install"

![img](https://img-blog.csdnimg.cn/20181121113528273.jpg)

4、初始化mysql数据库，输入“mysqld --initialize --user=root --console”。最后面的 root@localhost后的文字为初始化后的root 密码，一定要记住

![img](https://img-blog.csdnimg.cn/20181121113628764.jpg)

5、此时使用“net start mysql”成功启动msyql

![img](https://img-blog.csdnimg.cn/20181121113815360.jpg)

6、用生成的密码登录mysql

![img](https://img-blog.csdnimg.cn/20181121113949992.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L20wXzM3OTg3MTUx,size_16,color_FFFFFF,t_70)

7、通过“set password=password('root')”修改密码。此处将root密码设置为root

![img](https://img-blog.csdnimg.cn/20181121114058832.jpg)

mysql用户名、密码修改成功，均为 root

>  现在mysql密码 ：123456, 22-3-17

## 获取val最大值所在行的数据

### 方法一：子查询

首先，查找某[字段](https://so.csdn.net/so/search?q=字段&spm=1001.2101.3001.7020)的最大值

```csharp
select max(weight) from apple;
```


接着，根据最大值，查找其所在行


```csharp
select * from apple where weight =7888;
```

合并在一起就是

```csharp
select * from apple where weight = (select max(weight) from apple);
```

### 方法二：GROUP BY +LIMIT 1

```mysql
select * from apple GROUP BY weight LIMIT 1
```

### 其他

一、按name分组取val最大的值所在行的数据。--方法1：

select a.* from tb a where val = (select max(val) from tb where name = a.name) order by a.name

--方法2：

select a.* from tb a where not exists(select 1 from tb where name = a.name and val > a.val)

--方法3：

select a.* from tb a,(select name,max(val) val from tb group by name) b where a.name = b.name and a.val = b.val order by a.name

--方法4：

select a.* from tb a inner join (select name , max(val) val from tb group by name) b on a.name = b.name and a.val = b.val order by a.name

--方法5

select a.* from tb a where 1 > (select count(*) from tb where name = a.name and val > a.val ) order by a.name
————————————————
[其他方法原文链接：](https://blog.csdn.net/weixin_34738099/article/details/113139549)



## mysql命令行执行sql文件

说明：result.sql文件中是多条插入数据的sql语句。现将这些sql语句导入到数据库中，（不用打开文件拷贝然后粘贴执行，如果数据量大的话这种操作非常繁琐，应使用以下方法）。
注：提前将文件拷贝至当前目录下。如果文件不在当前目录，在source 后应加上文件的绝对路径
1、登录mysql

mysql -u root -p ;
1
2、输入密码，选择数据库

use my_database;
1
3、执行sql文件。

source result.sql ;


## 修改时区

**方法一：通过mysql命令行模式下动态修改**

```sql
show variables like "%time_zone%";
```

查看时区

```sql
+``------------------+--------+
| Variable_name  | Value |
+``------------------+--------+
| system_time_zone | CST  |
| time_zone    | SYSTEM |
+``------------------+--------+
2 ``rows` `in` `set` `(0.00 sec)
#time_zone说明mysql使用system的时区，system_time_zone说明system使用CST时区
```

 

修改时区

```sql
> set global time_zone = '+8:00'; ##修改mysql全局时区为北京时间，即我们所在的东8区
> set time_zone = '+8:00'; ##修改当前会话时区
> flush privileges; #立即生效
```

 

## my other

#### mysql jdbc 参数

MySQL Connector/J Driver

驱动程序包名：mysql-connector-java-x.x.xx-bin.jar

驱动程序类名: com.mysql.jdbc.Driver

JDBC URL: `jdbc:mysql://<host>:<port>/<database_name>`

默认端口3306，如果服务器使用默认端口则port可以省略

MySQL Connector/J Driver 允许在URL中添加额外的连接属性

`jdbc:mysql://<host>:<port>/<database_name>?property1=value1&property2=value2`

注意： 需要操作记录为了避免乱码应该加上属性 useUnicode=true&characterEncoding=utf8 ，比如

```
jdbc:mysql://192.168.177.129:3306/report?useUnicode=true&characterEncoding=utf8
```

#### mysql环境变量

如果添加到环境变量中还是无效，建议将mysql环境变量放在path路径的最前面

windows的**path路径是通过path文本从前往后找**，如果在最后有可能解析path失败

## mysql执行脚本命令

```mysql
show databases; 

create database xxx;

mysql> use yoj;

show tables;

##需要先选择数据库
source xxx.sql(sql文件的目录);
```

## mysql注意

#### null的判断都必须用is， = 没有用

```sql
DELETE FROM solution where submit_time is Null
```

## mysql导入数据时的外键约束问题

 这个问题可通过FOREIGN_KEY_CHECKS解决，用法如下：

    1、set FOREIGN_KEY_CHECKS=0;    #在导入的脚本命令行最前面设置为不检查外键约束
    2、。。。。。。。。。。。。              #导入数据的命令行
    3、set FOREIGN_KEY_CHECKS=1;    #在导入后恢复检查外键约束  



## mysql 索引

https://blog.csdn.net/liutong123987/article/details/79384395

索引不仅能提高查询速度，还**可以添加排序速度**，如果order by 后面的语句用到了索引，那么将会提高排序的速度。

主键具备索引的功能了。 当你创建或设置主键的时候,mysql会自动添加一个与主键对应的唯一索引,不需要再做额外的添加。

### 索引类型
Mysql目前主要有以下几种索引类型：FULLTEXT，HASH，BTREE，RTREE。

#### FULLTEXT

即为全文索引，目前只有MyISAM引擎支持。其可以在CREATE TABLE ，ALTER TABLE ，CREATE INDEX 使用，不过目前只有 CHAR、VARCHAR ，TEXT 列上可以创建全文索引。

全文索引并不是和MyISAM一起诞生的，它的出现是为了解决WHERE name LIKE “%word%"这类**针对文本的模糊查询效率较低的问题。**

#### HASH

  由于**HASH的唯一（几乎100%的唯一）**及类似键值对的形式，很适合作为索引。

HASH索引可以一次定位，不需要像树形索引那样逐层查找,因此**具有极高的效率。**但是，这种高效是有条件的，即**只在“=”和“in”条件下高效，对于范围查询、排序及组合索引仍然效率不高。**

#### BTREE

BTREE索引就是一种将索引值按一定的算法，存入一个树形的数据结构中（二叉树），每次查询都是从树的入口root开始，依次遍历node，获取leaf。这是MySQL里默认和最常用的索引类型。

#### RTREE
   RTREE在MySQL很少使用，仅支持geometry数据类型，支持该类型的存储引擎只有MyISAM、BDb、InnoDb、NDb、Archive几种。

相对于BTREE，RTREE的优势在于范围查找。

ps. 此段详细内容见此片博文：Mysql几种索引类型的区别及适用情况

### 三、索引种类

普通索引：仅加速查询

唯一索引：加速查询 + 列值唯一（可以有null）

主键索引：加速查询 + 列值唯一（不可以有null）+ 表中只有一个

组合索引：多列值组成一个索引，专门用于组合搜索，其效率大于索引合并

全文索引：对文本的内容进行分词，进行搜索

## count(*)和count(1)

**如果你要统计行数就用`count(*)`或者`count(1)`，推荐前者**

如果要统计某个字段不为NULL值的个数就用`count(字段)`

1.当mysql确认括号内的表达式值不可能为空时，实际上就是在统计行数

2.如果mysql知道某列col不可能为NULL值，那么mysql内部会将count(col)表达式优化为count(*)

这2句话出自`<<高性能MySQL>>`一书

也就是说count(1)和count(主键字段)还是要优化到count(*)的



## update使用select结果,count(distinct xx)

```sql
UPDATE user SET solved = (SELECT COUNT(DISTINCT problem_id) FROM solution WHERE user_id = #{userId}) WHERE user_id = #{userId}
```

## varchar()的长度问题

根据不同的字符集，解析中文占的位数是不一样的，如果是utf8的字符集，varchar(20)可以存放20个中文，这里中文跟英文存放的位数是一样的。但如果是latin字符集，中文估计解析不了，变成乱码

## mysql 导入时自己制定库名

在到处的sql文件中添加

```sql
DROP DATABASE IF EXISTS `ssm_crud`;
CREATE DATABASE ssm_crud;
USE ssm_crud;
```

## 修改用户的密码

## 方法1： 用SET PASSWORD命令 

首先登录MySQL。 

```
格式：mysql> set password for 用户名@localhost = password('新密码'); 
例子：mysql> 
```

```sql
set password for root@localhost = password('123'); 

set password for root@localhost = password('123456'); 
```



## 将表结构查询为表格

```mysql
SELECT
  COLUMN_NAME 列名,
  COLUMN_TYPE 数据类型,
    DATA_TYPE 字段类型,
  CHARACTER_MAXIMUM_LENGTH 长度,
	IF(IS_NULLABLE = 'YES','是','否') AS '是否为空',
  COLUMN_DEFAULT 默认值, 
	IF(COLUMN_KEY='PRI','是','否') AS '主键',
	IF(COLUMN_KEY='MUL','是','否') AS '外键',
  COLUMN_COMMENT 备注,
	COLUMN_KEY
FROM
 INFORMATION_SCHEMA.COLUMNS
where
-- yoj为数据库名称，到时候只需要修改成你要导出表结构的数据库即可
table_schema ='yoj'
AND
-- user为表名，到时候换成你要导出的表的名称
-- 如果不写的话，默认会查询出所有表中的数据，这样可能就分不清到底哪些字段是哪张表中的了，所以还是建议写上要导出的名名称
table_name  = 'problem'
```

# 参考资料

[**SQL语言 - SQL语法基础**](https://pdai.tech/md/db/sql-lan/sql-lan.html)










