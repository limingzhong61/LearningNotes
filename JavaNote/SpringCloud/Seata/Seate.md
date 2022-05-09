---

title: 分布式事务seata
date: 2021-10-24 10:40:06

categories: Java


---

# 分布式事务seata

## 事务的ACID原则

![image-20211021104413170](seate/image-20211021104413170.png)



## 演示分布式事务问题

1. 创建数据库，名为seata_demo，然后导入课前资料提供的SQL文件：

   ```
   seata-demo.sql
   ```

2. 导入课前资料提供的微服务:

   seata-demo（文件夹）

   ![image-20211021105841040](seate/image-20211021105841040.png)

3. 启动nacos、所有微服务

4. 测试下单功能，发出Post请求:

   ```
   curl --location --
   request POST 'http://localhost:8082/order?userId=user202103032042012&commodityCode=100202003032041&count=2&money=200'
   ```

## 分布式服务的事务问题

在分布式系统下，一个业务跨越多个服务或数据源，每个服务都是一个分支事务，要保证所有分支事务最终状态一致，这样的事务就是分布式事务。

![image-20211021124118539](seate/image-20211021124118539.png)

学习目标

![image-20211021124208030](seate/image-20211021124208030.png)

# 1理论基础

## CAP定理

1998年，加州大学的计算机科学家 Eric Brewer 提出，分布式系统有三个指标：

- Consistency（一致性）
- Availability（可用性）
- Partition tolerance （分区容错性）

Eric Brewer 说，分布式系统无法同时满足这三个指标。
这个结论就叫做 CAP 定理。

![image-20211021124800252](seate/image-20211021124800252.png)



### CAP定理- Consistency

Consistency（一致性）：用户访问分布式系统中的任意节点，得到的数据必须一致

![image-20211021124940177](seate/image-20211021124940177.png)

### CAP定理- Availability

Availability （可用性）：用户访问集群中的任意健康节点，必须能得到响应，而不是超时或拒绝

![image-20211021125054217](seate/image-20211021125054217.png)



### CAP定理-Partition tolerance

Partition（分区）：因为网络故障或其它原因导致分布式系统中的部分节点与其它节点失去连接，形成独立分区。
Tolerance（容错）：在集群出现分区时，整个系统也要持续对外提供服务

![image-20211021125301465](seate/image-20211021125301465.png)

### 总结

简述CAP定理内容？

- 分布式系统节点通过网络连接，一定会出现分区问题（P）
  当分区出现时，系统的一致性（C）和可用性（A）就无法同时满足

思考：elasticsearch集群是CP还是AP？

- ES集群出现分区时，故障节点会被剔除集群，数据分片会重新分配到其它节点，保证数据一致。因此是低可用性，高一致性，**属于CP**

## BASE理论

BASE理论是对CAP的一种解决思路，包含三个思想：

- **Basically Available （基本可用）**：分布式系统在出现故障时，允许损失部分可用性，即保证核心可用。
- Soft State（软状态）：在一定时间内，允许出现中间状态，比如临时的不一致状态。
- Eventually Consistent（最终一致性）：虽然无法保证强一致性，但是在软状态结束后，最终达到数据一致。

而分布式事务最大的问题是各个子事务的一致性问题，因此可以借鉴CAP定理和BASE理论：

- AP模式：各子事务分别执行和提交，允许出现结果不一致，然后采用弥补措施恢复数据即可，实现**最终一致。**
- CP模式：各个子事务执行后互相等待，同时提交，同时回滚，达成**强一致**。但事务等待过程中，处于弱可用状态。

## 分布式事务模型

解决分布式事务，各个子系统之间必须能感知到彼此的事务状态，才能保证状态一致，因此需要一个事务协调者来协调每一个事务的参与者（子系统事务）。
这里的子系统事务，称为**分支事务**；有关联的各个分支事务在一起称为**全局事务**

![image-20211021130501293](seate/image-20211021130501293.png)

总结

简述BASE理论三个思想：

- 基本可用
- 软状态
- 最终一致

解决分布式事务的思想和模型：

- 全局事务：整个分布式事务
- 分支事务：分布式事务中包含的每个子系统的事务

- 最终一致思想：各分支事务分别执行并提交，如果有不一致的情况，再想办法恢复数据
- 强一致思想：各分支事务执行完业务不要提交，等待彼此结果。而后统一提交或回滚

# 2初识Seata

Seata是 2019 年 1 月份蚂蚁金服和阿里巴巴共同开源的分布式事务解决方案。致力于提供高性能和简单易用的分布式事务服务，为用户打造一站式的分布式解决方案。
官网地址：http://seata.io/，其中的文档、播客中提供了大量的使用说明、源码分析。

## Seata架构

Seata事务管理中有三个重要的角色：

- **TC (Transaction Coordinator) - 事务协调者**：维护全局和分支事务的状态，协调全局事务提交或回滚。
- **TM (Transaction Manager) - 事务管理器**：定义全局事务的范围、开始全局事务、提交或回滚全局事务。
- **RM (Resource Manager) - 资源管理器**：管理分支事务处理的资源，与TC交谈以注册分支事务和报告分支事务的状态，并驱动分支事务提交或回滚。

![image-20211021153718032](seate/image-20211021153718032.png)

### 初识Seata

Seata提供了四种不同的分布式事务解决方案：

- XA模式：强一致性分阶段事务模式，牺牲了一定的可用性，无业务侵入
- TCC模式：最终一致的分阶段事务模式，有业务侵入
  AT模式：最终一致的分阶段事务模式，无业务侵入，也是Seata的默认模式
  SAGA模式：长事务模式，有业务侵入

## 部署TC服务

参考课前资料提供的文档《 seata的部署和集成》：

# 3动手实践

## XA模式

### XA模式原理

XA 规范 是 X/Open 组织定义的分布式事务处理（DTP，Distributed Transaction Processing）标准，XA 规范 描述了全局的TM与局部的RM之间的接口，几乎所有主流的数据库都对 XA 规范 提供了支持。

![image-20211023101642737](seate/image-20211023101642737.png)

### seata的XA模式

seata的XA模式做了一些调整，但大体相似：

TM (Transaction Manager) - 事务管理器RM一阶段的工作：

1. 注册分支事务到TC
2. 执行分支业务sql但不提交
3. 报告执行状态到TC

TC(**TC (Transaction Coordinator) - 事务协调者**)二阶段的工作：

- TC检测各分支事务执行状态
  a. 如果都成功，通知所有RM提交事务
  b. 如果有失败，通知所有RM回滚事务

RM二阶段的工作：

- 接收TC指令，提交或回滚事务

![image-20211023103311730](seate/image-20211023103311730.png)

XA模式的优点是什么？

- 事务的**强一致性，满足ACID原则**。
- **常用数据库都支持，实现简单**，并且没有代码侵入 

XA模式的缺点是什么？ 

- 因为一阶段需要锁定数据库资源，等待二阶段结束才释放，**性能较差** 
- 依赖**关系型数据库**实现事务

### 实现XA模式

Seata的starter已经完成了XA模式的自动装配，实现非常简单，步骤如下：

1. 修改application.yml文件（每个参与事务的微服务），开启XA模式：

   ```yaml
   seata:
   	data-source-proxy-mode: XA #开启数据源代理的XA模式
   ```

2.给发起全局事务的入口方法添加@GlobalTransactional注解，本例中是OrderServiceImpl中的create方法：

```java
    @Override
    @GlobalTransactional
    public Long create(Order order) {
        // 创建订单
        orderMapper.insert(order);
        try {
            // 扣用户余额
            accountClient.deduct(order.getUserId(), order.getMoney());
            // 扣库存
            storageClient.deduct(order.getCommodityCode(), order.getCount());

        } catch (FeignException e) {
            log.error("下单失败，原因:{}", e.contentUTF8(), e);
            throw new RuntimeException(e.contentUTF8(), e);
        }
        return order.getId();
    }
```



3.重启服务并测试

postman上测试

![image-20211023141217696](seate/image-20211023141217696.png)

count=10时，数据库数据均未修改

![image-20211023142634138](seate/image-20211023142634138.png)



![image-20211023142659710](seate/image-20211023142659710.png)



![image-20211023142708852](seate/image-20211023142708852.png)



## AT模式

### AT模式原理

AT模式同样是分阶段提交的事务模型，不过缺弥补了XA模型中资源锁定周期过长的缺陷。

阶段一RM的工作：

- 注册分支事务
- **记录undo-log（数据快照）**
- 执行业务sql并**提交**
- 报告事务状态

阶段二**提交时R**M的工作：

- 删除undo-log即可

阶段二**回滚时**RM的工作：
- 根据undo-log恢复数据到更新前

![image-20211023143110867](seate/image-20211023143110867.png)

例如，一个分支业务的SQL是这样的：update tb_account set money = money - 10 where id = 1

![image-20211023143607998](seate/image-20211023143607998.png)

#### 简述AT模式与XA模式最大的区别是什么？

- XA模式一阶段**不提交事务，锁定资源**；AT模式一阶段**直接提交，不锁定资源**。
- XA模式依赖数据库机制实现回滚；AT模式利用**数据快照实现数据回滚。**
- **XA模式强一致**；**AT模式最终一致**

### AT模式的脏写问题

**脏写**

脏写，意思是说有两个事务，事务 A 和事务 B 同时在更新一条数据，事务 A 先把它更新为 A 值，事务 B 紧接着就把它更新为 B 值。如图：

![img](https://pic3.zhimg.com/80/v2-d5c096c722332efdc187f5af5a0f923e_720w.jpg)



可以看到，此时事务 B 是后更新那行数据的值，所以此时那行数据的值是 B。而且此时事务 A 更新之后会记录一条 undo log 日志。因为事务 A 是先更新的，它在更新之前，这行数据的值为 `NULL`。所以此时事务 A 的 undo log 日志大概就是：更新之前这行数据的值为 NULL，主键为 XX

那么此时事务 B 更新完数据的值为 B，此时事务 A 突然回滚了，就会用它的 undo log 日志去回滚。此时事务 A 一回滚，直接就会把那行数据的值更新回 NULL 值。如图：



![img](https://pic1.zhimg.com/80/v2-e047504a8f3ff8d968d04b720fdd0f9c_720w.jpg)



然后就尴尬了，事务 B 一看，为什么我更新的 B 值没了？就因为你事务 A 反悔了把数据值回滚成 NULL 了，结果我更新的 B 值也不见 了。所以对于事务 B 看到的场景而言，就是自己**明明更新了，结果值却没了**，**这就是脏写。**

所谓脏写，就是我刚才明明写了一个数据值，结果过了一会却没了。而它的本质就是事务 B 去修改了事务 A 修改过的值，但是此时事务 A 还没提交，所以事务 A 随时会回滚，导致事务 B 修改的值也没了，这就是脏写的定义。

![image-20211023144005710](seate/image-20211023144005710.png)

![image-20211023144454904](seate/image-20211023144454904.png)

![image-20211023144624139](seate/image-20211023144624139.png)

AT模式的优点：

- 一阶段完成直接提交事务，释放数据库资源，性能比较好
- 利用全局锁实现读写隔离
- 没有代码侵入，框架自动完成回滚和提交

AT模式的缺点：

- 两阶段之间属于软状态，属于最终一致
- 框架的快照功能会影响性能，但比XA模式要好很多

### 实现AT模式

AT模式中的快照生成、回滚等动作都是由框架自动完成，没有任何代码侵入，因此实现非常简单。
1.导入课前资料提供的Sql文件：`seata-at.sql`，其中lock_table导入到TC服务关联的数据库，undo_log表导入到微服务关联的数据库：

```
seata-at.sql
```

lock_table导入到TC服务关联的数据库

```sql
-- ----------------------------
-- Table structure for lock_table
-- ----------------------------
DROP TABLE IF EXISTS `lock_table`;
CREATE TABLE `lock_table`  (
  `row_key` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `xid` varchar(96) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `transaction_id` bigint(20) NULL DEFAULT NULL,
  `branch_id` bigint(20) NOT NULL,
  `resource_id` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `table_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pk` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `gmt_create` datetime NULL DEFAULT NULL,
  `gmt_modified` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`row_key`) USING BTREE,
  INDEX `idx_branch_id`(`branch_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;
```

![image-20211023145853386](seate/image-20211023145853386.png)

undo_log表导入到微服务关联的数据库

```sql
-- ----------------------------
-- Table structure for undo_log
-- ----------------------------
DROP TABLE IF EXISTS `undo_log`;
CREATE TABLE `undo_log`  (
  `branch_id` bigint(20) NOT NULL COMMENT 'branch transaction id',
  `xid` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'global transaction id',
  `context` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'undo_log context,such as serialization',
  `rollback_info` longblob NOT NULL COMMENT 'rollback info',
  `log_status` int(11) NOT NULL COMMENT '0:normal status,1:defense status',
  `log_created` datetime(6) NOT NULL COMMENT 'create datetime',
  `log_modified` datetime(6) NOT NULL COMMENT 'modify datetime',
  UNIQUE INDEX `ux_undo_log`(`xid`, `branch_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'AT transaction mode undo table' ROW_FORMAT = Compact;

-- ----------------------------
-- Records of undo_log
-- ----------------------------
```

![image-20211023150122051](seate/image-20211023150122051.png)

2.修改application.yml文件，将事务模式修改为AT模式即可：

```yaml
seata:
  data-source-proxy-mode: AT#开启数据源代理的AT模式
```

3.重启服务并测试

测试内容同XA

## TCC模式

### TCC模式原理

TCC模式与AT模式非常相似，每阶段都是独立事务，不同的是TCC通过人工编码来实现数据恢复。需要实现三个方法：

- Try：资源的检测和预留； 
- Confirm：完成资源操作业务；要求 Try 成功 Confirm 一定要能成功。
- Cancel：预留资源释放，可以理解为try的反向操作。

举例，一个扣减用户余额的业务。假设账户A原来余额是100，需要余额扣减30元。

![image-20211023151258461](seate/image-20211023151258461.png)

#### TCc的工作模型图:

![image-20211023151758187](seate/image-20211023151758187.png)

TCC模式的每个阶段是做什么的？

- Try：资源检查和预留
- Confirm：业务执行和提交
- Cancel：预留资源的释放

TCC的优点是什么？

- 一阶段完成直接提交事务，释放数据库资源，性能好
- 相比AT模型，无需生成快照，无需使用全局锁，性能最强
- 不依赖数据库事务，而是依赖补偿操作，可以用于非事务型数据库

TCC的缺点是什么？

- **有代码侵入**，**需要人为编写try、Confirm和Cancel接口**，太麻烦
- 软状态，事务是最终一致
- 需要考虑Confirm和Cancel的失败情况，做好幂等处理

### 案例实现

**改造account-service服务，利用TCC实现分布式事务**

需求如下：

- 修改account-service，编写try、confirm、cancel逻辑
  try业务：添加冻结金额，扣减可用金额
  confirm业务：删除冻结金额
  cancel业务：删除冻结金额，恢复可用金额
  保证confirm、cancel接口的**幂等性**
  允许**空回滚**
  拒绝**业务悬挂**

#### TCC的空回滚和业务悬挂

当某分支事务的try阶段阻塞时，可能导致全局事务超时而触发二阶段的cancel操作。在未执行try操作时先执行了cancel操作，这时cancel不能做回滚，就是**空回滚**。

对于已经空回滚的业务，如果以后继续执行try，就永远不可能confirm或cancel，这就是**业务悬挂**。应当阻止执行空回滚后的try操作，避免悬挂

![image-20211023153412933](seate/image-20211023153412933.png)

#### 业务分析

![image-20211023154042887](seate/image-20211023154042887.png)



#### 声明TCC接口

TCC的Try、Confirm、Cancel方法都需要在接口中基于注解来声明，语法如下：



```java
@LocalTCC
public interface TCCService {
    /**
     * Try逻辑，@TwoPhaseBusinessAction中的name属性要与当前方法名一致，用于指定Try逻辑对应的方法
     */
    @TwoPhaseBusinessAction(name = "prepare", commitMethod = "confirm", rollbackMethod = "cancel")
    void prepare(@BusinessActionContextParameter(paramName = "param") String param);

    /**
     * 二阶段confirm确认方法、可以另命名，但要保证与commitMethod一致       *      * @param context 上下文,可以传递try方法的参数      * @return boolean 执行是否成功
     */
    boolean confirm(BusinessActionContext context);

    /**
     * 二阶段回滚方法，要保证与rollbackMethod一致
     */
    boolean cancel(BusinessActionContext context);
}
```

#### 1.编写AccountTCCService接口

```java
package cn.itcast.account.service;

import io.seata.rm.tcc.api.BusinessActionContext;
import io.seata.rm.tcc.api.BusinessActionContextParameter;
import io.seata.rm.tcc.api.LocalTCC;
import io.seata.rm.tcc.api.TwoPhaseBusinessAction;

@LocalTCC
public interface AccountTCCService {

    @TwoPhaseBusinessAction(name = "deduct", commitMethod = "confirm", rollbackMethod = "cancel")
    void deduct(@BusinessActionContextParameter(paramName = "userId") String userId,
                @BusinessActionContextParameter(paramName = "money")int money);

    boolean confirm(BusinessActionContext ctx);

    boolean cancel(BusinessActionContext ctx);
}

```

#### 2.创建account_freeze_tbl表

```sql
/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50622
 Source Host           : localhost:3306
 Source Schema         : seata_demo

 Target Server Type    : MySQL
 Target Server Version : 50622
 File Encoding         : 65001

 Date: 23/06/2021 16:23:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for account_freeze_tbl
-- ----------------------------
DROP TABLE IF EXISTS `account_freeze_tbl`;
CREATE TABLE `account_freeze_tbl`  (
  `xid` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `freeze_money` int(11) UNSIGNED NULL DEFAULT 0,
  `state` int(1) NULL DEFAULT NULL COMMENT '事务状态，0:try，1:confirm，2:cancel',
  PRIMARY KEY (`xid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of account_freeze_tbl
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
```

![image-20211023155018491](seate/image-20211023155018491.png)

![image-20211023155248424](seate/image-20211023155248424.png)

```java
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("account_freeze_tbl")
public class AccountFreeze {
    @TableId(type = IdType.INPUT)
    private String xid;
    private String userId;
    private Integer freezeMoney;
    private Integer state;

    public static abstract class State {
        public final static int TRY = 0;
        public final static int CONFIRM = 1;
        public final static int CANCEL = 2;
    }
}
```

因为money是unsigned int ，所以不用检查是否为负数（余额判断）



![image-20211023155724065](seate/image-20211023155724065.png)

#### 3.编写接口实现

```java
package cn.itcast.account.service.impl;

import cn.itcast.account.entity.AccountFreeze;
import cn.itcast.account.mapper.AccountFreezeMapper;
import cn.itcast.account.mapper.AccountMapper;
import cn.itcast.account.service.AccountTCCService;
import io.seata.core.context.RootContext;
import io.seata.rm.tcc.api.BusinessActionContext;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Slf4j
public class AccountTCCServiceImpl implements AccountTCCService {

    @Autowired
    private AccountMapper accountMapper;
    @Autowired
    private AccountFreezeMapper freezeMapper;

    @Override
    @Transactional
    public void deduct(String userId, int money) {
        // 0.获取事务id
        String xid = RootContext.getXID();
        // 1.扣减可用余额
        accountMapper.deduct(userId, money);
        // 2.记录冻结金额，事务状态
        AccountFreeze freeze = new AccountFreeze();
        freeze.setUserId(userId);
        freeze.setFreezeMoney(money);
        freeze.setState(AccountFreeze.State.TRY);
        freeze.setXid(xid);
        freezeMapper.insert(freeze);
    }

    // 删除操作，执行多次没区别，天生幂等，没必要判断  
    @Override
    public boolean confirm(BusinessActionContext ctx) {
        // 1.获取事务id
        String xid = ctx.getXid();
        // 2.根据id删除冻结记录
        int count = freezeMapper.deleteById(xid);
        return count == 1;
    }

    @Override
    public boolean cancel(BusinessActionContext ctx) {
        // 0.查询冻结记录
        String xid = ctx.getXid();
        String userId = ctx.getActionContext("userId").toString();
        AccountFreeze freeze = freezeMapper.selectById(xid);
        // 1.空回滚的判断，判断freeze是否为null，为null证明try没执行,需要空回滚
        if(freeze == null){
            // 证明try没有执行，需要空回滚
            freeze = new AccountFreeze();
            freeze.setUserId(userId);
            freeze.setFreezeMoney(0);
            freeze.setState(AccountFreeze.State.CANCEL);
            freeze.setXid(xid);
            freezeMapper.insert(freeze);
            return  true;
        }
        //2.幂等判断
        if(freeze.getState() == AccountFreeze.State.CANCEL){
            // 已经处理过一次CANCEL了，无需重复处理
            return true;
        }
        // 1.恢复可用余额
        accountMapper.refund(freeze.getUserId(), freeze.getFreezeMoney());
        // 2.将冻结金额清零，状态改为CANCEL
        freeze.setFreezeMoney(0);
        freeze.setState(AccountFreeze.State.CANCEL);
        int count = freezeMapper.updateById(freeze);
        return count == 1;
    }
}

```

修改web中AccountService为AccountTCCService

```java
@Autowired
private AccountService accountService;
@Autowired
private AccountTCCService accountService;
```

#### 4.重启服务测试

![image-20211023164102558](seate/image-20211023164102558.png)



![image-20211023164300355](seate/image-20211023164300355.png)

![image-20211023164249986](seate/image-20211023164249986.png)

![image-20211023164335739](seate/image-20211023164335739.png)

## Saga模式

Saga模式是SEATA提供的长事务解决方案。也分为两个阶段：

•一阶段：直接提交本地事务

•二阶段：成功则什么都不做；失败则通过编写补偿业务来回滚

Saga模式优点：

•事务参与者可以基于事件驱动实现异步调用，吞吐高

•一阶段直接提交事务，无锁，性能好

•不用编写TCC中的三个阶段，实现简单

缺点：

•软状态持续时间不确定，时效性差

•没有锁，没有事务隔离，会有脏写



![image-20211023164828531](seate/image-20211023164828531.png)

四种模式对比

|              | **XA**                         | **AT**                                       | **TCC**                                                  | **SAGA**                                                     |
| ------------ | ------------------------------ | -------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------ |
| **一致性**   | 强一致                         | 弱一致                                       | 弱一致                                                   | 最终一致                                                     |
| **隔离性**   | 完全隔离                       | 基于全局锁隔离                               | 基于资源预留隔离                                         | 无隔离                                                       |
| **代码侵入** | 无                             | 无                                           | 有，要编写三个接口                                       | 有，要编写状态机和补偿业务                                   |
| **性能**     | 差                             | 好                                           | 非常好                                                   | 非常好                                                       |
| **场景**     | 对一致性、隔离性有高要求的业务 | 基于关系型数据库的大多数分布式事务场景都可以 | •对性能要求较高的事务。  •有非关系型数据库要参与的事务。 | •业务流程长、业务流程多  •参与者包含其它公司或遗留系统服务，无法提供  TCC  模式要求的三个接口 |





















# seata的部署和集成

## 一、部署Seata的tc-server

### 1.下载

首先我们要下载seata-server包，地址在[http](http://seata.io/zh-cn/blog/download.html)[://seata.io/zh-cn/blog/download](http://seata.io/zh-cn/blog/download.html)[.](http://seata.io/zh-cn/blog/download.html)[html](http://seata.io/zh-cn/blog/download.html) 

当然，课前资料也准备好了：

```
seata-server-1.4.2.zip
```



### 2.解压

在非中文目录解压缩这个zip包，其目录结构如下：

![image-20210622202515014](seate/image-20210622202515014.png)

### 3.修改配置

修改conf目录下的registry.conf文件：

![image-20210622202622874](seate/image-20210622202622874.png)

内容如下：

```properties
registry {
  # 注册中心类型 file 、nacos 、eureka、redis、zk、consul、etcd3、sofa
  # tc服务的注册中心类，这里选择nacos，也可以是eureka、zookeeper等
  type = "nacos"

  nacos {
    # seata tc 服务注册到 nacos的服务名称，可以自定义
    application = "seata-tc-server"
    serverAddr = "127.0.0.1:8848"
    group = "DEFAULT_GROUP"
    namespace = ""
    cluster = "SH"
    username = "nacos"
    password = "nacos"
  }
}

config {
  # 配置中心 file、nacos 、apollo、zk、consul、etcd3
  # 读取tc服务端的配置文件的方式，这里是从nacos配置中心读取，这样如果tc是集群，可以共享配置
  type = "nacos"
  # 配置nacos地址等信息
  nacos {
    serverAddr = "127.0.0.1:8848"
    namespace = ""
    group = "SEATA_GROUP"
    username = "nacos"
    password = "nacos"
    dataId = "seataServer.properties"
  }
}
```

![image-20211021160716787](seate/image-20211021160716787.png)



### 4.在nacos添加配置

特别注意，为了让tc服务的集群可以共享配置，我们选择了nacos作为统一配置中心。因此服务端配置文件seataServer.properties文件需要在nacos中配好。

格式如下：

![image-20210622203609227](seate/image-20210622203609227.png)



配置内容如下：

```properties
# 数据存储方式，db代表数据库
store.mode=db
store.db.datasource=druid
store.db.dbType=mysql
store.db.driverClassName=com.mysql.cj.jdbc.Driver
store.db.url=jdbc:mysql://127.0.0.1:3306/seata?useUnicode=true&rewriteBatchedStatements=true&serverTimezone=UTC
store.db.user=root
store.db.password=root
store.db.minConn=5
store.db.maxConn=30
store.db.globalTable=global_table
store.db.branchTable=branch_table
store.db.queryLimit=100
store.db.lockTable=lock_table
store.db.maxWait=5000
# 事务、日志等配置
server.recovery.committingRetryPeriod=1000
server.recovery.asynCommittingRetryPeriod=1000
server.recovery.rollbackingRetryPeriod=1000
server.recovery.timeoutRetryPeriod=1000
server.maxCommitRetryTimeout=-1
server.maxRollbackRetryTimeout=-1
server.rollbackRetryTimeoutUnlockEnable=false
server.undo.logSaveDays=7
server.undo.logDeletePeriod=86400000

# 客户端与服务端传输方式
transport.serialization=seata
transport.compressor=none
# 关闭metrics功能，提高性能
metrics.enabled=false
metrics.registryType=compact
metrics.exporterList=prometheus
metrics.exporterPrometheusPort=9898
```



==其中的数据库地址、用户名、密码都需要修改成你自己的数据库信息。==



### 5.创建数据库表

特别注意：tc服务在管理分布式事务时，需要记录事务相关数据到数据库中，你需要提前创建好这些表。

新建一个名为seata的数据库，运行课前资料提供的sql文件：

![image-20210622204145159](seate/image-20210622204145159.png)

这些表主要记录全局事务、分支事务、全局锁信息：

```mysql
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- 分支事务表
-- ----------------------------
DROP TABLE IF EXISTS `branch_table`;
CREATE TABLE `branch_table`  (
  `branch_id` bigint(20) NOT NULL,
  `xid` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `transaction_id` bigint(20) NULL DEFAULT NULL,
  `resource_group_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `resource_id` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `branch_type` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` tinyint(4) NULL DEFAULT NULL,
  `client_id` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `application_data` varchar(2000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `gmt_create` datetime(6) NULL DEFAULT NULL,
  `gmt_modified` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`branch_id`) USING BTREE,
  INDEX `idx_xid`(`xid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- 全局事务表
-- ----------------------------
DROP TABLE IF EXISTS `global_table`;
CREATE TABLE `global_table`  (
  `xid` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `transaction_id` bigint(20) NULL DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  `application_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `transaction_service_group` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `transaction_name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `timeout` int(11) NULL DEFAULT NULL,
  `begin_time` bigint(20) NULL DEFAULT NULL,
  `application_data` varchar(2000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `gmt_create` datetime NULL DEFAULT NULL,
  `gmt_modified` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`xid`) USING BTREE,
  INDEX `idx_gmt_modified_status`(`gmt_modified`, `status`) USING BTREE,
  INDEX `idx_transaction_id`(`transaction_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
```



### 6.启动TC服务

进入bin目录，运行其中的seata-server.bat即可：

![image-20210622205427318](seate/image-20210622205427318.png)

启动成功后，seata-server应该已经注册到nacos注册中心了。



打开浏览器，访问nacos地址：http://localhost:8848，然后进入服务列表页面，可以看到seata-tc-server的信息：

![image-20210622205901450](seate/image-20210622205901450.png)







## 二、微服务集成seata

### 1.引入依赖

首先，我们需要在微服务(pom.xml)中引入seata依赖：

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-seata</artifactId>
    <exclusions>
        <!--版本较低，1.3.0，因此排除-->
        <exclusion>
            <artifactId>seata-spring-boot-starter</artifactId>
            <groupId>io.seata</groupId>
        </exclusion>
    </exclusions>
</dependency>
<!--seata starter 采用1.4.2版本-->
<dependency>
    <groupId>io.seata</groupId>
    <artifactId>seata-spring-boot-starter</artifactId>
    <version>${seata.version}</version>
</dependency>
```



### 2.修改配置文件

需要修改application.yml文件，添加一些配置：

然后，配置application.yml，让微服务通过注册中心找到seata-tc-server：

```yaml
seata:
  registry: 
    # TC服务注册中心的配置，微服务根据这些信息去注册中心获取tc服务地址
    # 参考tc服务自己的registry.conf中的配置
    type: nacos
    nacos: # tc
      server-addr: 127.0.0.1:8848
      namespace: ""
      group: DEFAULT_GROUP
      application: seata-tc-server # tc服务在nacos中的服务名称
      cluster: SH
  tx-service-group: seata-demo # 事务组，根据这个获取tc服务的cluster名称
  service:
    vgroup-mapping: # 事务组与TC服务cluster的映射关系
      seata-demo: SH
```

![image-20211021163723045](seate/image-20211021163723045.png)

## 三、TC服务的高可用和异地容灾

### 1.模拟异地容灾的TC集群3

计划启动两台seata的tc服务节点：

| 节点名称 | ip地址    | 端口号 | 集群名称 |
| -------- | --------- | ------ | -------- |
| seata    | 127.0.0.1 | 8091   | SH       |
| seata2   | 127.0.0.1 | 8092   | HZ       |

之前我们已经启动了一台seata服务，端口是8091，集群名为SH。

现在，将seata目录复制一份，起名为seata2

修改seata2/conf/registry.conf内容如下：

```nginx
registry {
  # tc服务的注册中心类，这里选择nacos，也可以是eureka、zookeeper等
  type = "nacos"

  nacos {
    # seata tc 服务注册到 nacos的服务名称，可以自定义
    application = "seata-tc-server"
    serverAddr = "127.0.0.1:8848"
    group = "DEFAULT_GROUP"
    namespace = ""
    cluster = "HZ"
    username = "nacos"
    password = "nacos"
  }
}

config {
  # 读取tc服务端的配置文件的方式，这里是从nacos配置中心读取，这样如果tc是集群，可以共享配置
  type = "nacos"
  # 配置nacos地址等信息
  nacos {
    serverAddr = "127.0.0.1:8848"
    namespace = ""
    group = "SEATA_GROUP"
    username = "nacos"
    password = "nacos"
    dataId = "seataServer.properties"
  }
}
```



进入seata2/bin目录，然后运行命令：

```powershell
seata-server.bat -p 8092
```



打开nacos控制台，查看服务列表：

![image-20210624151150840](seate/image-20210624151150840.png)

点进详情查看：

![image-20210624151221747](seate/image-20210624151221747.png)



### 2.将事务组映射配置到nacos

接下来，我们需要将tx-service-group与cluster的映射关系都配置到nacos配置中心。

新建一个配置：

![image-20210624151507072](seate/image-20210624151507072.png)

配置的内容如下：

```properties
# 事务组映射关系
service.vgroupMapping.seata-demo=SH

service.enableDegrade=false
service.disableGlobalTransaction=false
# 与TC服务的通信配置
transport.type=TCP
transport.server=NIO
transport.heartbeat=true
transport.enableClientBatchSendRequest=false
transport.threadFactory.bossThreadPrefix=NettyBoss
transport.threadFactory.workerThreadPrefix=NettyServerNIOWorker
transport.threadFactory.serverExecutorThreadPrefix=NettyServerBizHandler
transport.threadFactory.shareBossWorker=false
transport.threadFactory.clientSelectorThreadPrefix=NettyClientSelector
transport.threadFactory.clientSelectorThreadSize=1
transport.threadFactory.clientWorkerThreadPrefix=NettyClientWorkerThread
transport.threadFactory.bossThreadSize=1
transport.threadFactory.workerThreadSize=default
transport.shutdown.wait=3
# RM配置
client.rm.asyncCommitBufferLimit=10000
client.rm.lock.retryInterval=10
client.rm.lock.retryTimes=30
client.rm.lock.retryPolicyBranchRollbackOnConflict=true
client.rm.reportRetryCount=5
client.rm.tableMetaCheckEnable=false
client.rm.tableMetaCheckerInterval=60000
client.rm.sqlParserType=druid
client.rm.reportSuccessEnable=false
client.rm.sagaBranchRegisterEnable=false
# TM配置
client.tm.commitRetryCount=5
client.tm.rollbackRetryCount=5
client.tm.defaultGlobalTransactionTimeout=60000
client.tm.degradeCheck=false
client.tm.degradeCheckAllowTimes=10
client.tm.degradeCheckPeriod=2000

# undo日志配置
client.undo.dataValidation=true
client.undo.logSerialization=jackson
client.undo.onlyCareUpdateColumns=true
client.undo.logTable=undo_log
client.undo.compress.enable=true
client.undo.compress.type=zip
client.undo.compress.threshold=64k
client.log.exceptionRate=100
```

### 3.微服务读取nacos配置

接下来，需要修改每一个微服务的application.yml文件，让微服务读取nacos中的client.properties文件：

```yaml
seata:
  config:
    type: nacos
    nacos:
      server-addr: 127.0.0.1:8848
      username: nacos
      password: nacos
      group: SEATA_GROUP
      data-id: client.properties
```



重启微服务，现在微服务到底是连接tc的SH集群，还是tc的HZ集群，都统一由nacos的client.properties来决定了。

# 