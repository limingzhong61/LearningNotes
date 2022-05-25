---
title: SpringCloud01

date: 2021-9-12 10:40:06

categories: Java



---

# SpringCloud01

# 1.认识微服务

随着互联网行业的发展，对服务的要求也越来越高，服务架构也从单体架构逐渐演变为现在流行的微服务架构。这些架构之间有怎样的差别呢？

## 1.0.学习目标

了解微服务架构的优缺点



### 微服务技术栈

![image-20210819105714890](SpringCloud/image-20210819105714890.png)

![image-20210819105849852](SpringCloud/image-20210819105849852.png)

![image-20210819110034400](SpringCloud/image-20210819110034400.png)

![image-20210819110130382](SpringCloud/image-20210819110130382.png)

![image-20210819110930997](SpringCloud/image-20210819110930997.png)

![image-20210914095159453](SpringCloud/image-20210914095159453.png)



## 1.1.单体架构

**单体架构**：将业务的所有功能集中在一个项目中开发，打成一个包部署。

![image-20210713202807818](SpringCloud/image-20210713202807818.png)

单体架构的优缺点如下：

**优点：**

- 架构简单
- 部署成本低

**缺点：**

- 耦合度高（维护困难、升级困难）



## 1.2.分布式架构

**分布式架构**：根据**业务功能**对系统做拆分，每个业务功能模块作为独立项目开发，称为一个服务。

![image-20210713203124797](SpringCloud/image-20210713203124797.png)



分布式架构的优缺点：

**优点：**

- 降低服务耦合
- 有利于服务升级和拓展

**缺点：**

- 服务**调用关系错综复杂**



分布式架构虽然降低了服务耦合，但是服务拆分时也有很多问题需要思考：

- 服务拆分的粒度如何界定？
- 服务之间如何调用？
- 服务的调用关系如何管理？

人们需要制定一套行之有效的标准来约束分布式架构。



## 1.3.微服务

微服务的架构特征：

- 单一职责：微服务**拆分粒度更小**，**每一个服务都对应唯一的业务能力**，做到单一职责
- 自治：团队独立、技术独立、数据独立，独立部署和交付
- 面向服务：服务提供统一标准的接口，与语言和技术无关
- 隔离性强：服务调用做好隔离、容错、降级，避免出现级联问题

![image-20210713203753373](SpringCloud/image-20210713203753373.png)

微服务的上述特性其实是在给分布式架构制定一个标准，进一步降低服务之间的耦合度，提供服务的独立性和灵活性。做到高内聚，低耦合。

因此，可以认为**微服务**是一种经过良好架构设计的**分布式架构方案** 。

但方案该怎么落地？选用什么样的技术栈？全球的互联网公司都在积极尝试自己的微服务落地方案。

其中在Java领域最引人注目的就是SpringCloud提供的方案了。

![image-20210819112409833](SpringCloud/image-20210819112409833.png)

![image-20210819112852009](SpringCloud/image-20210819112852009.png)

## 1.4.SpringCloud

SpringCloud是目前国内使用最广泛的**微服务框架**。官网地址：https://spring.io/projects/spring-cloud。

SpringCloud集成了各种微服务功能组件，并基于SpringBoot实现了这些组件的自动装配，从而提供了良好的开箱即用体验。

其中常见的组件包括：

![image-20210713204155887](SpringCloud/image-20210713204155887.png)



另外，SpringCloud底层是依赖于SpringBoot的，并且有版本的兼容关系，如下：

![image-20210713205003790](SpringCloud/image-20210713205003790.png)

笔记使用的版本是 **Hoxton.SR10，因此对应的SpringBoot版本是2.3.x版本**。



## 1.5.总结

- 单体架构：简单方便，高度耦合，扩展性差，适合小型项目。例如：学生管理系统

- 分布式架构：松耦合，扩展性好，但架构复杂，难度大。适合大型互联网项目，例如：京东、淘宝

- 微服务：一种良好的**分布式架构方案**

  ①优点：拆分粒度更小、服务更独立、耦合度更低

  ②缺点：架构非常复杂，运维、监控、部署难度提高

- SpringCloud是微服务架构的一站式解决方案，集成了各种优秀微服务功能组件





# 2.服务拆分和远程调用

任何分布式架构都离不开服务的拆分，微服务也是一样。

## 2.1.服务拆分原则

这里我总结了微服务拆分时的几个原则：

- 不同微服务，不要**重复开发相同业务**
- 微服务**数据独立，不要访问其它微服务的数据库**
- 微服务可以将自己的业务暴露为接口，供其它微服务调用

![image-20210713210800950](SpringCloud/image-20210713210800950.png)



## 2.2.服务拆分示例

以课前资料中的微服务cloud-demo为例，其结构如下：

![image-20210713211009593](SpringCloud/image-20210713211009593.png)

cloud-demo：父工程，管理依赖

- order-service：订单微服务，负责订单相关业务
- user-service：用户微服务，负责用户相关业务

要求：

- 订单微服务和用户微服务都必须有各自的数据库，相互独立
- 订单服务和用户服务都对外暴露Restful的接口
- 订单服务如果需要查询用户信息，只能调用用户服务的Restful接口，不能查询用户数据库



### 2.2.1.导入demo工程

用IDEA导入课前资料提供的Demo：

![image-20210713211814094](SpringCloud/image-20210713211814094.png)



项目结构如下：

![image-20210713212656887](SpringCloud/image-20210713212656887.png)





导入后，会在IDEA右下角出现弹窗：

![image-20210713212349272](SpringCloud/image-20210713212349272.png)

点击弹窗，然后按下图选择：

![image-20210713212336185](SpringCloud/image-20210713212336185.png)

会出现这样的菜单：

![image-20210713212513324](SpringCloud/image-20210713212513324.png)



配置下项目使用的JDK：

![image-20210713220736408](SpringCloud/image-20210713220736408.png)



## 2.3.实现远程调用案例



在order-service服务中，有一个根据id查询订单的接口：

![image-20210713212749575](SpringCloud/image-20210713212749575.png)

根据id查询订单，返回值是Order对象，如图：

![image-20210713212901725](SpringCloud/image-20210713212901725.png)

其中的user为null





在user-service中有一个根据id查询用户的接口：

![image-20210713213146089](SpringCloud/image-20210713213146089.png)

查询的结果如图：

![image-20210713213213075](SpringCloud/image-20210713213213075.png)





### 2.3.1.案例需求：

修改order-service中的根据id查询订单业务，要求在查询订单的同时，根据订单中包含的userId查询出用户信息，一起返回。

![image-20210713213312278](SpringCloud/image-20210713213312278.png)



因此，我们需要在order-service中 向user-service发起一个http的请求，调用http://localhost:8081/user/{userId}这个接口。

大概的步骤是这样的：

- 注册一个RestTemplate的实例到Spring容器
- 修改order-service服务中的OrderService类中的queryOrderById方法，根据Order对象中的userId查询User
- 将查询的User填充到Order对象，一起返回



### 2.3.2.注册RestTemplate

首先，我们在order-service服务中的OrderApplication启动类中，注册RestTemplate实例：

```java
package cn.itcast.order;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

@MapperScan("cn.itcast.order.mapper")
@SpringBootApplication
public class OrderApplication {

    public static void main(String[] args) {
        SpringApplication.run(OrderApplication.class, args);
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```



### 2.3.3.实现远程调用

修改order-service服务中的cn.itcast.order.service包下的OrderService类中的queryOrderById方法：

![image-20210713213959569](SpringCloud/image-20210713213959569.png)







## 2.4.提供者与消费者

在服务调用关系中，会有两个不同的角色：

**服务提供者**：一次业务中，被其它微服务调用的服务。（提供接口给其它微服务）

**服务消费者**：一次业务中，调用其它微服务的服务。（调用其它微服务提供的接口）

![image-20210713214404481](SpringCloud/image-20210713214404481.png)



但是，服务提供者与服务消费者的角色并不是绝对的，而是相对于业务而言。

如果服务A调用了服务B，而服务B又调用了服务C，服务B的角色是什么？

- 对于A调用B的业务而言：A是服务消费者，B是服务提供者
- 对于B调用C的业务而言：B是服务消费者，C是服务提供者



因此，服务B既可以是服务提供者，也可以是服务消费者。





# 3.Eureka注册中心





假如我们的服务提供者user-service部署了多个实例，如图：

即问题是：一个服务消费者(order-service)向有多个服务提供者(user-service)的**服务名称**发起远程调用时.....

![image-20210713214925388](SpringCloud/image-20210713214925388.png)



大家思考几个问题：

- order-service在发起远程调用的时候，该如何得知user-service实例的ip地址和端口？
- 有多个user-service实例地址，order-service调用时该如何选择？
- order-service如何得知某个user-service实例是否依然健康，是不是已经宕机？



## 3.1.Eureka的结构和作用

**==Eureka作用==**：记录服务名称和多个服务实例的**映射关系**，从而使得通**过服务名称向一个服务发起远程调用**时，

能**找到相应的实际服务地址。**

这些问题都需要利用**SpringCloud中的注册中心**来解决，其中最广为人知的注册中心就是Eureka，其结构如下：

![image-20210713220104956](SpringCloud/image-20210713220104956.png)



回答之前的各个问题。

问题1：order-service如何得知user-service实例地址？

获取地址信息的流程如下：

- user-service服务实例启动后，将**自己的信息注册到eureka-server（Eureka服务端**）。这个叫**服务注册**
- eureka-server保存**服务名称到服务实例地址列表的映射关系**
- order-service根据服务名称，拉取实例地址列表。这个叫**服务发现或服务拉取**



问题2：order-service如何从多个user-service实例中选择具体的实例？

- order-service从实例列表中**利用负载均衡算法选中一个实例地址**
- 向该实例地址发起远程调用



问题3：order-service如何得知某个user-service实例是否依然健康，是不是已经宕机？

- user-service会**每隔一段时间（默认30秒）向eureka-server发起请求**，报告自己状态，称为**心跳**
- 当超过一定时间没有发送心跳时，eureka-server会认为微服务实例故障，将该实例从服务列表中剔除
- order-service拉取服务时，就能将故障实例排除了



> 注意：一个微服务，既可以是服务提供者，又可以是服务消费者，因此**eureka将服务注册、服务发现等功能统一封装到了eureka-client端**

### 总结

在Eureka架构中，微服务角色有两类:

- EurekaServer:服务端，注册中心
  - 记录**服务信息**：服务名称和多个服务实例的**映射关系**等内容
  - 心跳监控：保证记录的服务实例能正常使用。
- EurekaClient:客户端
  - Provider:服务提供者，例如案例中的user-service
    - 注册自己的信息到EurekaServer
    - 每隔30秒向EurekaServer发送心跳
  - consumer:服务消费者，例如案例中的order-service
    - 根据服务名称从EurekaServer拉取服务列表
    - 基于服务列表做负载均衡，选中一个微服务（服务实例）后发起远程调用

因此，接下来我们动手实践的步骤包括：

![image-20210713220509769](SpringCloud/image-20210713220509769.png)



## 3.2.搭建eureka-server

首先大家注册中心服务端：eureka-server，这**必须是一个独立的微服务**

### 3.2.1.创建eureka-server服务

在cloud-demo父工程下，创建一个子模块：

![image-20210713220605881](SpringCloud/image-20210713220605881.png)

填写模块信息：

![image-20210713220857396](SpringCloud/image-20210713220857396.png)



然后填写服务信息：eureka-server

![image-20210713221339022](SpringCloud/image-20210713221339022.png)



### 3.2.2.引入eureka依赖

引入SpringCloud为eureka提供的starter依赖：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```



### 3.2.3.编写启动类

给eureka-server服务编写一个启动类，一定要添加一个`@EnableEurekaServer`注解，**开启eureka的注册中心功能**：

```java
package cn.itcast.eureka;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@SpringBootApplication
@EnableEurekaServer
public class EurekaApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaApplication.class, args);
    }
}
```



### 3.2.4.编写配置文件

编写一个`application.yml`文件，内容如下：

```yaml
server:
  port: 10086
spring:
  application:
    name: eureka-server
eureka:
  client:
    service-url: 
      defaultZone: http://127.0.0.1:10086/eureka
```



### 3.2.5.启动服务

启动微服务，然后在浏览器访问：http://127.0.0.1:10086

看到下面结果应该是成功了：

![image-20210713222157190](SpringCloud/image-20210713222157190.png)



## 3.3.服务注册

下面，我们将user-service注册到eureka-server中去。

### 1）引入依赖

在user-service的pom文件中，引入下面的eureka-client依赖：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```



### 2）配置文件

在user-service中，修改`application.yml`文件，添加服务名称、eureka地址：

```yaml
spring:
  application:
    name: userservice  # user服务的服务名称
eureka:
  client:
    service-url:  # eureka的地址信息
      defaultZone: http://127.0.0.1:10086/eureka
```



### 3）启动多个user-service实例

为了演示一个服务有多个实例的场景，我们添加一个SpringBoot的启动配置，再启动一个user-service。



首先，复制原来的user-service启动配置：

![image-20210713222656562](SpringCloud/image-20210713222656562.png)

然后，在弹出的窗口中，填写信息：

![image-20210713222757702](SpringCloud/image-20210713222757702.png)



现在，SpringBoot窗口会出现两个user-service启动配置：

![image-20210713222841951](SpringCloud/image-20210713222841951.png)

不过，第一个是8081端口，第二个是8082端口。

启动两个user-service实例：

![image-20210713223041491](SpringCloud/image-20210713223041491.png)

查看eureka-server管理页面：

![image-20210713223150650](SpringCloud/image-20210713223150650.png)

### 总结

- 1.服务注册
  - 引入eureka-client依赖
  - 在application.yml中配置eureka地址
- 2．无论是消费者还是提供者，引入eureka-client依赖、知道eureka地址（eureka服务端）后，都可以完成服务注册



## 3.4.服务发现

下面，我们将order-service的逻辑修改：向eureka-server拉取user-service的信息，实现服务发现。

### 1）引入依赖

之前说过，**服务发现、服务注册统一都封装在eureka-client依赖**，因此这一步与服务注册时一致。

在order-service的pom文件中，引入下面的eureka-client依赖：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```



### 2）配置文件

服务发现也需要知道eureka地址，因此第二步与服务注册一致，都是配置eureka信息：

在order-service中，修改application.yml文件，添加服务名称、eureka地址：

```yaml
server:
  port: 10086 # 服务端口
spring:
  application:
    name: eurekaserver # eureka的服务名称
eureka:
  client:
    service-url:  # eureka的地址信息
      defaultZone: http://127.0.0.1:10086/eureka
```



### 3）服务拉取和负载均衡

最后，我们要去eureka-server中拉取user-service服务的实例列表，并且实现负载均衡。

不过这些动作不用我们去做，只需要添加一些注解即可。



在order-service的`OrderApplication`中，给`RestTemplate`这个Bean添加一个`@LoadBalanced`注解：

![image-20210713224049419](SpringCloud/image-20210713224049419.png)



修改order-service服务中的cn.itcast.order.service包下的OrderService类中的queryOrderById方法。修改访问的url路径，用服务名代替ip、端口：

![image-20210713224245731](SpringCloud/image-20210713224245731.png)



spring会自动帮助我们从eureka-server端，根据userservice这个服务名称，获取实例列表，而后完成负载均衡。

### 总结

- 1．搭建EurekaServer
  - 引入eureka-server依赖
  - 添加`@EnableEurekaServer`注解·在application.yml中配置eureka地址
- 2．服务注册
  - 引入eureka-client依赖
  - 在application.yml中配置eureka地址
- 3．服务发现
  - 引入eureka-client依赖
  - 在application.yml中配置eureka地址
  - 给`RestTemplate`添加`@LoadBalanced`注解
  - 用**服务提供者的服务名称远程调用**

# 4.Ribbon负载均衡

上一节中，我们添加了**`@LoadBalanced`注解，即可实现负载均衡功能**，这是什么原理呢？



## 4.1.负载均衡原理

SpringCloud底层其实是利用了一个名为Ribbon的组件，来实现负载均衡功能的。

![image-20210713224517686](SpringCloud/image-20210713224517686.png)

那么我们发出的请求明明是http://userservice/user/1，怎么变成了http://localhost:8081的呢？



## 4.2.源码跟踪

为什么我们只输入了service名称就可以访问了呢？之前还要获取ip和端口。

显然有人帮我们根据service名称，获取到了服务实例的ip和端口。它就是`LoadBalancerInterceptor`，这个类会在对`RestTemplate`的请求进行拦截，然后从Eureka根据服务id获取服务列表，随后利用负载均衡算法得到真实的服务地址信息，替换服务id。

我们进行源码跟踪：

### 1）LoadBalancerInterceptor

![1525620483637](SpringCloud/1525620483637.png)

可以看到这里的intercept方法，拦截了用户的`HttpRequest`请求，然后做了几件事：

- `request.getURI()`：获取请求uri，本例中就是 http://user-service/user/8
- `originalUri.getHost()`：获取uri路径的主机名，其实就是服务id，`user-service`
- `this.loadBalancer.execute()`：处理服务id，和用户请求。

这里的**`this.loadBalancer`是`LoadBalancerClient`类型**，我们继续跟入。



### 2）LoadBalancerClient

继续跟入execute方法：

![1525620787090](SpringCloud/1525620787090.png)

代码是这样的：

- getLoadBalancer(serviceId)：根据服务id获取ILoadBalancer，而ILoadBalancer会拿着服务id去eureka中获取服务列表并保存起来。
- **getServer(loadBalancer)：利用内置的负载均衡算法**，从服务列表中选择一个。本例中，可以看到获取了8082端口的服务



放行后，再次访问并跟踪，发现获取的是8081：

 ![1525620835911](SpringCloud/1525620835911.png)

果然实现了负载均衡。



### 3）负载均衡策略IRule

在刚才的代码中，可以看到获取服务使通过一个`getServer`方法来做负载均衡:

 ![1525620835911](SpringCloud/1525620835911.png)

我们继续跟入：

![1544361421671](SpringCloud/1544361421671.png)

继续跟踪源码chooseServer方法，发现这么一段代码：

BaseLoadBalancer

 ![1525622652849](SpringCloud/1525622652849.png)

我们看看这个rule是谁：

 ![1525622699666](SpringCloud/1525622699666.png)

这里的rule默认值是一个`RoundRobinRule`，看类的介绍：

 ![1525622754316](SpringCloud/1525622754316.png)

这不就是**轮询的意思**嘛。

`RoundRobin`轮询（调度）

到这里，整个负载均衡的流程我们就清楚了。



### 4）总结

SpringCloudRibbon的底层采用了一个拦截器，拦截了RestTemplate发出的请求，对地址做了修改。用一幅图来总结一下：

![image-20210713224724673](SpringCloud/image-20210713224724673.png)



基本流程如下：

- 拦截我们的RestTemplate请求http://userservice/user/1
- **RibbonLoadBalancerClient**会从请求url中获取服务名称，也就是user-service
- **DynamicServerListLoadBalancer**根据user-service到**eureka拉取服务列表**
- eureka返回列表，localhost:8081、localhost:8082
- IRule利用**内置负载均衡规则**，从列表中选择一个，例如localhost:8081
- RibbonLoadBalancerClient修改请求地址，用localhost:8081替代userservice，得到http://localhost:8081/user/1，发起真实请求



## 4.3.负载均衡策略



### 4.3.1.负载均衡策略

负载均衡的规则都定义在IRule接口中，而IRule有很多不同的实现类：

![image-20210713225653000](SpringCloud/image-20210713225653000.png)

不同规则的含义如下：

| **内置负载均衡规则类**    | **规则描述**                                                 |
| ------------------------- | ------------------------------------------------------------ |
| RoundRobinRule            | **简单轮询服务列**表来选择服务器。它是**Ribbon默认的负载均衡规则**。 |
| AvailabilityFilteringRule | 对以下两种服务器进行忽略：   （1）在默认情况下，这台服务器如果3次连接失败，这台服务器就会被设置为“短路”状态。短路状态将持续30秒，如果再次连接失败，短路的持续时间就会几何级地增加。  （2）并发数过高的服务器。如果一个服务器的并发连接数过高，配置了AvailabilityFilteringRule规则的客户端也会将其忽略。并发连接数的上限，可以由客户端的`<clientName>.<clientConfigNameSpace>.ActiveConnectionsLimit`属性进行配置。 |
| WeightedResponseTimeRule  | 为每一个服务器赋予一个权重值。服务器响应时间越长，这个服务器的权重就越小。这个规则会随机选择服务器，这个权重值会影响服务器的选择。 |
| **ZoneAvoidanceRule**     | 以区域可用的服务器为基础进行服务器的选择。使用Zone对服务器进行分类，这个Zone可以理解为一个机房、一个机架等。而后再对Zone内的多个服务做轮询。 |
| BestAvailableRule         | 忽略那些短路的服务器，并选择并发数较低的服务器。             |
| RandomRule                | 随机选择一个可用的服务器。                                   |
| RetryRule                 | 重试机制的选择逻辑                                           |



默认的实现就是**ZoneAvoidanceRule，是一种轮询方案**



### 4.3.2.自定义负载均衡策略

通过定义IRule实现可以修改负载均衡规则，有两种方式：

1. 代码方式：在order-service中的OrderApplication类中，定义一个新的IRule：

```java
@Bean
public IRule randomRule(){
    return new RandomRule();
}
```

这个针对全体服务

2. 配置文件方式：在order-service的application.yml文件中，添加新的配置也可以修改规则：

```yaml
userservice: # 给某个微服务配置负载均衡规则，这里是userservice服务
  ribbon:
    NFLoadBalancerRuleClassName: com.netflix.loadbalancer.RandomRule # 负载均衡规则 
```

这个针对某一个服务userservice

> **注意**，**一般用默认的负载均衡规则**，不做修改。



## 4.4.饥饿加载

Ribbon**默认是采用懒加载**，即第一次访问时才会去创建LoadBalanceClient，**请求时间会很长**。

而饥饿加载则会在项目启动时创建，降低第一次访问的耗时，通过**下面配置开启饥饿加载**：

```yaml
ribbon:
  eager-load:
    enabled: true # 开启饥饿加载
    clients: # 指定饥饿加载的服务名称
      - userservice
```

**总结**

![image-20210822173230846](SpringCloud/image-20210822173230846.png)

# 5.Nacos注册中心

国内公司一般都推崇阿里巴巴的技术，比如注册中心，SpringCloudAlibaba也推出了一个名为Nacos的注册中心。

## 5.1.认识和安装Nacos

[Nacos](https://nacos.io/)是阿里巴巴的产品，现在是[SpringCloud](https://spring.io/projects/spring-cloud)中的一个组件。相比[Eureka](https://github.com/Netflix/eureka)功能更加丰富，在国内受欢迎程度较高。

![image-20210713230444308](SpringCloud/image-20210713230444308.png)



安装方式可以参考课前资料《Nacos安装指南.md》

## 5.2.服务注册到nacos

Nacos是SpringCloudAlibaba的组件，而SpringCloudAlibaba也遵循SpringCloud中定义的服务注册、服务发现规范。因此使用Nacos和使用Eureka对于微服务来说，并没有太大区别。

主要差异在于：

- 依赖不同
- 服务地址不同

### 1）引入依赖

在cloud-demo父工程的pom文件中的`<dependencyManagement>`中引入SpringCloudAlibaba的依赖：

```xml
<!--nacos的管理依赖-->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-alibaba-dependencies</artifactId>
    <version>2.2.6.RELEASE</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

然后在user-service和order-service中的pom文件中引入nacos-discovery依赖：

```xml
<!--nacos的配置管理依赖-->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>
```



> **注意**：不要忘了注释掉eureka的依赖。



### 2）配置nacos地址

在user-service和order-service的application.yml中添加nacos地址：

```yaml
spring:
  cloud:
    nacos:
      server-addr: localhost:8848  #nacos服务地址
```



> **注意**：不要忘了注释掉eureka的地址



### 3）重启

重启微服务后，登录nacos管理页面，可以看到微服务信息：

![image-20210713231439607](SpringCloud/image-20210713231439607.png)

**总结**

![image-20210822181240493](SpringCloud/image-20210822181240493.png)

## 5.3.服务分级存储模型

一个**服务**可以有多个**实例**，例如我们的user-service，可以有:

- 127.0.0.1:8081
- 127.0.0.1:8082
- 127.0.0.1:8083

假如这些实例分布于全国各地的不同机房，例如：

- 127.0.0.1:8081，在上海机房
- 127.0.0.1:8082，在上海机房
- 127.0.0.1:8083，在杭州机房

Nacos就将**同一机房内的实例** 划分为一个**集群**。

也就是说，user-service是服务，一个服务可以包含多个集群，如杭州、上海，每个集群下可以有多个实例，形成分级模型，如图：

![image-20210713232522531](SpringCloud/image-20210713232522531.png)



微服务互相访问时，应该**尽可能访问同集群实例，因为本地访问速度更快**。当本集群内不可用时，才访问其它集群。例如：

![image-20210713232658928](SpringCloud/image-20210713232658928.png)

杭州机房内的order-service应该优先访问同机房的user-service。





### 5.3.1.给user-service配置集群



修改user-service的application.yml文件，添加集群配置：

```yaml
spring:
  cloud:
    nacos:
      server-addr: localhost:8848
      discovery:
        cluster-name: HZ # 集群名称
```

重启两个user-service实例后，我们可以在nacos控制台看到下面结果：

![image-20210713232916215](SpringCloud/image-20210713232916215.png)



我们再次复制一个user-service启动配置，添加属性：

```sh
-Dserver.port=8083 -Dspring.cloud.nacos.discovery.cluster-name=SH
```

配置如图所示：

![image-20210713233528982](SpringCloud/image-20210713233528982.png)



启动UserApplication3后再次查看nacos控制台：

![image-20210713233727923](SpringCloud/image-20210713233727923.png)

**总结**

![image-20210822193648606](SpringCloud/image-20210822193648606.png)

### 5.3.2.同集群优先的负载均衡

## 失败https://www.bilibili.com/video/BV1LQ4y127n4?p=20

默认的`ZoneAvoidanceRule`并不能实现根据同集群优先来实现负载均衡。

因此**Nacos中提供了一个`NacosRule`的实现**，可以优先从同集群中挑选实例。

1）给order-service配置集群信息

修改order-service的application.yml文件，添加集群配置：

```sh
spring:
  cloud:
    nacos:
      server-addr: localhost:8848
      discovery:
        cluster-name: HZ # 集群名称
```



2）**修改负载均衡规则**

修改order-service的application.yml文件，修改负载均衡规则：

```yaml
userservice:
  ribbon:
    NFLoadBalancerRuleClassName: com.alibaba.cloud.nacos.ribbon.NacosRule # 负载均衡规则 
```

2. 代码方式：在order-service中的OrderApplication类中，定义一个新的IRule：

```java
@Bean
public IRule randomRule(){
    return new NacosRule();
}
```

这个针对全体服务

**成功**

![image-20210828165751129](SpringCloud/image-20210828165751129.png)

## 5.4.权重配置

实际部署中会出现这样的场景：

服务器设备性能有差异，部分实例所在机器性能较好，另一些较差，我们希望性能好的机器承担更多的用户请求。

但默认情况下NacosRule是同集群内随机挑选，不会考虑机器的性能问题。



因此，**Nacos提供了权重配置来控制访问频率，权重越大则访问频率越高**。



在nacos控制台，找到user-service的实例列表，点击编辑，即可修改权重：

![image-20210713235133225](SpringCloud/image-20210713235133225.png)

在弹出的编辑窗口，修改权重：

![image-20210713235235219](SpringCloud/image-20210713235235219.png)





> **注意**：如果**权重修改为0，则该实例永远不会被访问**

![image-20210828171001714](SpringCloud/image-20210828171001714.png)

## 5.5.环境隔离

Nacos提供了namespace来实现环境隔离功能。

- nacos中可以有多个namespace
- namespace下可以有group、service等
- 不同namespace之间相互隔离，例如不同namespace的服务互相不可见



![image-20210714000101516](SpringCloud/image-20210714000101516.png)



### 5.5.1.创建namespace

默认情况下，所有service、data、group都在同一个namespace，名为public：

![image-20210714000414781](SpringCloud/image-20210714000414781.png)



我们可以点击页面新增按钮，添加一个namespace：

![image-20210714000440143](SpringCloud/image-20210714000440143.png)



然后，填写表单：

![image-20210714000505928](SpringCloud/image-20210714000505928.png)

就能在页面看到一个新的namespace：

![image-20210714000522913](SpringCloud/image-20210714000522913.png)



### 5.5.2.给微服务配置namespace

给微服务配置namespace只能通过修改配置来实现。

例如，修改order-service的application.yml文件：

```yaml
spring:
  cloud:
    nacos:
      server-addr: localhost:8848 #nacos服务地址
      discovery:
        cluster-name: HZ # 集群名称
        namespace: 492a7d5d-237b-46a1-a99a-fa8e98e4b0f9 # 命名空间，填ID
```



重启order-service后，访问控制台，可以看到下面的结果：

![image-20210714000830703](SpringCloud/image-20210714000830703.png)



![image-20210714000837140](SpringCloud/image-20210714000837140.png)

此时访问order-service，因为namespace不同，会导致找不到userservice，控制台会报错：

![image-20210714000941256](SpringCloud/image-20210714000941256.png)

![image-20210828171712343](SpringCloud/image-20210828171712343.png)

## 5.6.Nacos与Eureka的区别

Nacos的**服务实例分为两种l类型**：

- 临时实例：如果实例宕机超过一定时间，会从服务列表剔除，默认的类型。

- 非临时实例：如果**实例宕机，不会从服务列表剔除**，也可以叫永久实例。



配置一个服务实例为永久实例：

```yaml
spring:
  cloud:
    nacos:
      discovery:
        ephemeral: false # 设置为非临时实例，是否是临时实例
```





Nacos和Eureka整体结构类似，服务注册、服务拉取、心跳等待，但是也存在一些差异：

![image-20210714001728017](SpringCloud/image-20210714001728017.png)

**总结**

- Nacos与eureka的共同点
  - 都支持服务注册和服务拉取
  - 都支持服务提供者心跳方式做健康检测

- Nacos与Eureka的区别
  - Nacos支持**服务端主动检测提供者状态**：临时实例采用心跳模式，非临时实例采用主动检测模式
  - 临时实例心跳不正常会被剔除，非临时实例则不会被剔除
  - Nacos支持**服务列表变更的消息推送模式**，**服务列表更新更及时**，eureka时效性就相对而言比较差
  - Nacos集群默认采用AP方式，当集群中存在非临时实例时，采用CP模式；Eureka采用AP方式

# SpringCloud实用篇02

# 1.Nacos配置管理

Nacos除了可以做注册中心，同样可以做配置管理来使用。

## 1.1.统一配置管理

当微服务部署的实例越来越多，达到数十、数百时，逐个修改微服务配置就会让人抓狂，而且很容易出错。我们需要一种统一配置管理方案，可以集中管理所有实例的配置。

![image-20210714164426792](SpringCloud/image-20210714164426792-1630225333418.png)



Nacos一方面可以将配置集中管理，另一方可以在配置变更时，及时通知微服务，实现**配置的热更新**。



### 1.1.1.在nacos中添加配置文件

如何在nacos中管理配置呢？

![image-20210714164742924](SpringCloud/image-20210714164742924-1630225333419.png)

然后在弹出的表单中，填写配置信息：

![image-20210714164856664](SpringCloud/image-20210714164856664-1630225333419.png)



> 注意：项目的核心配置，需要**热更新的配置**才有放到nacos管理的必要。基本不会变更的一些配置还是保存在微服务本地比较好。



### 1.1.2.从微服务拉取配置

微服务要拉取nacos中管理的配置，并且与本地的application.yml配置合并，才能完成项目启动。

但如果尚未读取application.yml，又如何得知nacos地址呢？

因此spring引入了一种新的配置文件：**bootstrap.yaml文件，会在application.yml之前被读取**，流程如下：

![img](SpringCloud/L0iFYNF-1630225333419.png)



1）引入nacos-config依赖

首先，**在user-service服务中**，引入nacos-config的客户端依赖：

```xml
<!--nacos配置管理依赖-->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
</dependency>
```

2）添加**bootstrap.yaml**

然后，在user-service中添加一个bootstrap.yaml文件，内容如下：

```yaml
spring:
  application:
    name: userservice # 服务名称
  profiles:
    active: dev #开发环境，这里是dev 
  cloud:
    nacos:
      server-addr: localhost:8848 # Nacos地址
      config:
        file-extension: yaml # 文件后缀名
```

这里会根据**spring.cloud.nacos.server-addr获取nacos地址**，再根据

`${spring.application.name}-${spring.profiles.active}.${spring.cloud.nacos.config.file-extension}`作为**文件id**，来读取配置。

本例中，就是去读取`userservice-dev.yaml`：

![image-20210714170845901](SpringCloud/image-20210714170845901-1630225333422.png)

服务名称-开发环境.文件后缀名

3）读取nacos配置

在user-service中的UserController中添加业务逻辑，读取pattern.dateformat配置：

完整代码：

```java
package cn.itcast.user.web;

import cn.itcast.user.pojo.User;
import cn.itcast.user.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Slf4j
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    @Value("${pattern.dateformat}")
    private String dateformat;
    
    @GetMapping("now")
    public String now(){
        return LocalDateTime.now().format(DateTimeFormatter.ofPattern(dateformat));
    }
    // ...略
}
```



在页面访问，可以看到效果：

![image-20210714170449612](SpringCloud/image-20210714170449612-1630225333419.png)

### 总结-配置交给Nacos管理

将配置交给Nacos管理的步骤

- ①在Nacos中添加配置文件
- ②在微服务中引入nacos的config依赖
- ③在**微服务中添加bootstrap.yml**,配置nacos地址 、当前环境、服务名称、文件后缀名。这些决定了程序
  启动时去nacos读取哪个文件

## 1.2.配置热更新

我们最终的目的，是修改nacos中的配置后，微服务中无需重启即可让配置生效，也就是**配置热更新**。



要实现配置热更新，可以使用两种方式：

### 1.2.1.方式一

在@Value注入的变量所在类上添加注解@RefreshScope：

![image-20210714171036335](SpringCloud/image-20210714171036335-1630225333422.png)



### 1.2.2.方式二

使用**@ConfigurationProperties注解代替@Value注解**。

注:在使用**@ConfigurationProperties**时**不需要@RefreshScope**，**推荐使用这种方式**

在user-service服务中，添加一个类，读取patterrn.dateformat属性：

```java
package cn.itcast.user.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@Data
@ConfigurationProperties(prefix = "pattern")
public class PatternProperties {
    private String dateformat;
}
```



在UserController中使用这个类代替@Value：

完整代码：

```java
package cn.itcast.user.web;

import cn.itcast.user.config.PatternProperties;
import cn.itcast.user.pojo.User;
import cn.itcast.user.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Slf4j
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private PatternProperties patternProperties;

    @GetMapping("now")
    public String now(){
        return LocalDateTime.now().format(DateTimeFormatter.ofPattern(patternProperties.getDateformat()));
    }

    // 略
}
```

![image-20210829111728529](SpringCloud/image-20210829111728529-1630225333422.png)



## 1.3.配置共享

其实微服务启动时，会去nacos读取多个配置文件，例如：

- `[spring.application.name]-[spring.profiles.active].yaml`，例如：userservice-dev.yaml

- `[spring.application.name].yaml`，例如：userservice.yaml

而`[spring.application.name].yaml`不包含环境，**因此可以被多个环境共享。**



下面我们通过案例来测试配置共享



### 1）添加一个环境共享配置

我们在nacos中添加一个userservice.yaml文件：

![image-20210714173233650](SpringCloud/image-20210714173233650-1630225333422.png)



### 2）在user-service中读取共享配置

在user-service服务中，修改PatternProperties类，读取新添加的属性：

![image-20210714173324231](SpringCloud/image-20210714173324231-1630225333422.png)

在user-service服务中，修改UserController，添加一个方法：

![image-20210714173721309](SpringCloud/image-20210714173721309-1630225333422.png)



### 3）运行两个UserApplication，使用不同的profile

修改UserApplication2这个启动项，改变其profile值：

![image-20210714173538538](SpringCloud/image-20210714173538538-1630225333422.png)



![image-20210714173519963](SpringCloud/image-20210714173519963-1630225333422.png)



这样，UserApplication(8081)使用的profile是dev，UserApplication2(8082)使用的profile是test。

启动UserApplication和UserApplication2

访问http://localhost:8081/user/prop，结果：

![image-20210714174313344](SpringCloud/image-20210714174313344-1630225333422.png)

访问http://localhost:8082/user/prop，结果：

![image-20210714174424818](SpringCloud/image-20210714174424818-1630225333422.png)

可以看出来，不管是dev，还是test环境，都读取到了envSharedValue这个属性的值。





### 4）配置共享的优先级

当nacos、服务本地同时出现相同属性时，优先级有高低之分：

![image-20210714174623557](SpringCloud/image-20210714174623557-1630225333422.png)



![image-20210829114709139](SpringCloud/image-20210829114709139-1630225333422.png)

### bug：

注：**如果没能读取到nacos的共享配置**，**重启nacos可解决**

## 1.4.搭建Nacos集群

Nacos生产环境下一定要部署为集群状态，部署方式参考课前资料中的文档：

**nacos集群搭建.md**

https://www.bilibili.com/video/BV1LQ4y127n4?p=29

![image-20210829122807270](SpringCloud/image-20210829122807270-1630225333422.png)

# 



# 2.Feign远程调用



先来看我们以前利用RestTemplate发起远程调用的代码：

![image-20210714174814204](SpringCloud/image-20210714174814204.png)

存在下面的问题：

•代码可读性差，编程体验不统一

•参数复杂URL难以维护



Feign是一个**声明式的http客户端**，官方地址：https://github.com/OpenFeign/feign

其作用就是帮助我们优雅的实现http请求的发送，解决上面提到的问题。

![image-20210714174918088](SpringCloud/image-20210714174918088.png)





## 2.1.Feign替代RestTemplate

Fegin的使用步骤如下：

### 1）引入依赖

我们在order-service服务的pom文件中引入feign的依赖：

```xml
<!--feign客户端依赖-->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```



### 2）添加注解

在order-service的启动类添加注解开启Feign的功能：

```java
@EnableFeignClients
```

![image-20210714175102524](SpringCloud/image-20210714175102524.png)



### 3）编写Feign的客户端

在order-service中新建一个接口，内容如下：

```java
package cn.itcast.order.client;

import cn.itcast.order.pojo.User;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient("userservice")
public interface UserClient {
    @GetMapping("/user/{id}")
    User findById(@PathVariable("id") Long id);
}
```



这个客户端主要是基于SpringMVC的注解来声明远程调用的信息，比如：

- 服务名称：userservice
- 请求方式：GET
- 请求路径：/user/{id}
- 请求参数：Long id
- 返回值类型：User

这样，Feign就可以帮助我们发送http请求，无需自己使用RestTemplate来发送了。





### 4）测试

修改order-service中的OrderService类中的queryOrderById方法，使用Feign客户端代替RestTemplate：

![image-20210714175415087](SpringCloud/image-20210714175415087.png)

是不是看起来优雅多了。





### 5）总结

使用Feign的步骤：

① 引入依赖

② 添加@EnableFeignClients注解

③ 编写FeignClient接口

④ 使用FeignClient中定义的方法代替RestTemplate



## 2.2.自定义配置

Feign可以支持很多的自定义配置，如下表所示：

| 类型                   | 作用             | 说明                                                   |
| ---------------------- | ---------------- | ------------------------------------------------------ |
| **feign.Logger.Level** | 修改日志级别     | 包含四种不同的级别：NONE、BASIC、HEADERS、FULL         |
| feign.codec.Decoder    | 响应结果的解析器 | http远程调用的结果做解析，例如解析json字符串为java对象 |
| feign.codec.Encoder    | 请求参数编码     | 将请求参数编码，便于通过http请求发送                   |
| feign. Contract        | 支持的注解格式   | 默认是SpringMVC的注解                                  |
| feign. Retryer         | 失败重试机制     | 请求失败的重试机制，默认是没有，不过会使用Ribbon的重试 |

一般情况下，默认值就能满足我们使用，如果要自定义时，只需要**创建自定义的@Bean覆盖默认Bean即可**。

**平时建议用NONE或者BASIC**，记录日志会消耗一定的性能

下面以日志为例来演示如何自定义配置。

### 2.2.1.配置文件方式

基于配置文件修改feign的日志级别可以针对单个服务：

```yaml
feign:  
  client:
    config: 
      userservice: # 针对某个微服务的配置
        loggerLevel: FULL #  日志级别 
```

也可以针对所有服务：

```yaml
feign:  
  client:
    config: 
      default: # 这里用default就是全局配置，如果是写服务名称，则是针对某个微服务的配置
        loggerLevel: FULL #  日志级别 
```



而日志的级别分为四种：

- NONE：不记录任何日志信息，这是默认值。
- BASIC：仅记录请求的方法，URL以及响应状态码和执行时间
- HEADERS：在BASIC的基础上，额外记录了请求和响应的头信息
- FULL：记录所有请求和响应的明细，包括头信息、请求体、元数据。



### 2.2.2.Java代码方式

也可以基于Java代码来修改日志级别，先声明一个类，然后声明一个Logger.Level的对象：

```java
public class DefaultFeignConfiguration  {
    @Bean
    public Logger.Level feignLogLevel(){
        return Logger.Level.BASIC; // 日志级别为BASIC
    }
}
```



如果要**全局生效**，将其放到启动类的@EnableFeignClients这个注解中：

```java
@EnableFeignClients(defaultConfiguration = DefaultFeignConfiguration .class) 
```



如果是**局部生效**，则把它放到对应的@FeignClient这个注解中：

```java
@FeignClient(value = "userservice", configuration = DefaultFeignConfiguration .class) 
```



![image-20210829164437154](SpringCloud/image-20210829164437154.png)



## 2.3.Feign使用优化

Feign底层发起http请求，依赖于其它的框架。其底层客户端实现包括：

•URLConnection：**默认实现**，不支持连接池

•Apache HttpClient ：支持连接池

•OKHttp：支持连接池



因此提高Feign的性能主要手段就是使用**连接池**代替默认的URLConnection。



这里我们用Apache的HttpClient来演示。

1）引入依赖

在order-service的pom文件中引入Apache的HttpClient依赖：

```xml
<!--httpClient的依赖 -->
<dependency>
    <groupId>io.github.openfeign</groupId>
    <artifactId>feign-httpclient</artifactId>
</dependency>
```



2）配置连接池

在order-service的application.yml中添加配置：

```yaml
feign:
  client:
    config:
      default: # default全局的配置
        loggerLevel: BASIC # 日志级别，BASIC就是基本的请求和响应信息
  httpclient:
    enabled: true # 开启feign对HttpClient的支持
    max-connections: 200 # 最大的连接数
    max-connections-per-route: 50 # 每个路径的最大连接数
```



接下来，在FeignClientFactoryBean中的loadBalance方法中打断点：

![image-20210714185925910](SpringCloud/image-20210714185925910.png)

Debug方式启动order-service服务，可以看到这里的client，底层就是Apache HttpClient：

![image-20210714190041542](SpringCloud/image-20210714190041542.png)



如果上面操作完成后，未更新为Apache HttpClient，查看已经下载好对应依赖，有可能是Maven未加载对应的依赖，用maven reload一下project，重新加载对应依赖或可解决

![image-20210829170814915](SpringCloud/image-20210829170814915.png)

总结，Feign的优化：

1.**日志级别尽量用basic**

2.使用HttpClient或OKHttp代替URLConnection

①  引入feign-httpClient依赖

②  配置文件开启httpClient功能，设置连接池参数



## 2.4.最佳实践

所谓最近实践，就是使用过程中总结的经验，**最好的一种使用方式。**

自习观察可以发现，Feign的客户端与服务提供者的controller代码非常相似：

feign客户端：

![image-20210714190542730](SpringCloud/image-20210714190542730.png)

UserController：

![image-20210714190528450](SpringCloud/image-20210714190528450.png)



有没有一种办法简化这种重复的代码编写呢？





### 2.4.1.继承方式

**抽象客服端和服务端的共同方法**到一个接口中

一样的代码可以通过继承来共享：

1）定义一个API接口，利用定义方法，并基于SpringMVC注解做声明。

2）Feign客户端和Controller都**集成该接口**



![image-20210714190640857](SpringCloud/image-20210714190640857.png)

官方不推荐使用

![image-20210829171704131](SpringCloud/image-20210829171704131.png)

优点：

- 简单
- 实现了代码共享

缺点：

- 服务提供方、服务消费方**紧耦合**

- **参数列表中的注解映射并不会继承**，因此Controller中必须再次声明方法、参数列表、注解





### 2.4.2.抽取方式

将Feign的Client抽取为独立模块，并且把接口有关的POJO、默认的Feign配置都放到这个模块中，提供给所有消费者使用。

例如，将UserClient、User、Feign的默认配置都抽取到一个feign-api包中，所有微服务引用该依赖包，即可直接使用。

![image-20210714214041796](SpringCloud/image-20210714214041796.png)



![image-20210829172053596](SpringCloud/image-20210829172053596.png)

### 2.4.3.实现基于抽取的最佳实践

#### 1）抽取

首先创建一个module，命名为feign-api：

![image-20210714204557771](SpringCloud/image-20210714204557771.png)

项目结构：

![image-20210714204656214](SpringCloud/image-20210714204656214.png)

在feign-api中然后引入feign的starter依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```



然后，order-service中编写的UserClient、User、DefaultFeignConfiguration都复制到feign-api项目中

![image-20210714205221970](SpringCloud/image-20210714205221970.png)



#### 2）在order-service中使用feign-api

首先，删除order-service中的UserClient、User、DefaultFeignConfiguration等类或接口。



在order-service的pom文件中中引入feign-api的依赖：

```xml
<!--引入feign的统一api-->
<dependency>
    <groupId>cn.itcast.demo</groupId>
    <artifactId>feign-api</artifactId>
    <version>1.0</version>
</dependency>
```



修改order-service中的所有与上述三个组件有关的导包部分，改成导入feign-api中的包



#### 3）重启测试

重启后，发现服务报错了：

![image-20210714205623048](SpringCloud/image-20210714205623048.png)



这是因为UserClient现在在cn.itcast.feign.clients包下，

而order-service的@EnableFeignClients注解是在cn.itcast.order包下，不在同一个包，无法扫描到UserClient。



#### 4）解决扫描包问题

方式一：

指定Feign应该扫描的包：

```java
@EnableFeignClients(basePackages = "cn.itcast.feign.clients")
```



方式二：

指定需要加载的Client接口：

```java
@EnableFeignClients(clients = {UserClient.class})
```

推荐用第二种





# 3.Gateway服务网关

Spring Cloud Gateway 是 Spring Cloud 的一个全新项目，该项目是基于 Spring 5.0，Spring Boot 2.0 和 Project Reactor 等响应式编程和事件流技术开发的网关，它旨在为微服务架构提供一种简单有效的统一的 API 路由管理方式。



## 3.1.为什么需要网关

Gateway网关是我们服务的守门神，所有微服务的统一入口。

网关的**核心功能特性**：

- 请求路由
- 权限控制
- 限流

架构图：

![image-20210714210131152](SpringCloud/image-20210714210131152.png)



**权限控制**：网关作为微服务入口，需要**校验用户是是否有请求资格**，如果没有则进行拦截。

**路由和负载均衡**：一切请求都必须先经过gateway，但网关不处理业务，而是根据某种规则，把请求转发到某个微服务，这个过程叫做路由。当然路由的目标服务有多个时，还需要做负载均衡。

**限流**：当请求流量过高时，在网关中按照下流的微服务能够接受的速度来放行请求，避免服务压力过大。



在SpringCloud中网关的实现包括两种：

- gateway
- zuul

Zuul是基于Servlet的实现，属于阻塞式编程。而SpringCloudGateway则是基于**Spring5中提供的WebFlux**，属于响应式编程的实现，**具备更好的性能。**

![image-20210829223448857](SpringCloud/image-20210829223448857.png)



## 3.2.gateway快速入门

下面，我们就演示下网关的基本路由功能。基本步骤如下：

1. 创建SpringBoot工程gateway，引入网关依赖
2. 编写启动类
3. 编写基础配置和路由规则
4. 启动网关服务进行测试



### 1）创建gateway服务，引入依赖

创建服务：

![image-20210714210919458](SpringCloud/image-20210714210919458.png)

引入依赖：

```xml
<!--网关gateway依赖-->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
<!--nacos服务发现依赖-->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>
```



### 2）编写启动类

```java
package cn.itcast.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class GatewayApplication {

	public static void main(String[] args) {
		SpringApplication.run(GatewayApplication.class, args);
	}
}
```



### 3）编写基础配置和路由规则

创建application.yml文件，内容如下：

```yaml
server:
  port: 10010 # 网关端口
spring:
  application:
    name: gateway # 服务名称
  cloud:
    nacos:
      server-addr: localhost:8848 # nacos地址
    gateway:
      routes: # 网关路由配置
        - id: user-service # 路由id，自定义，只要唯一即可
          # uri: http://127.0.0.1:8081 # 路由的目标地址 http就是固定地址
          uri: lb://userservice # 路由的目标地址 lb（LoadBalance）就是负载均衡，后面跟服务名称
          predicates: # 路由断言，也就是判断请求是否符合路由规则的条件
            - Path=/user/** # 这个是按照路径匹配，只要以/user/开头就符合要求
```



我们将符合`Path` 规则的一切请求，都代理到 `uri`参数指定的地址。

本例中，我们将 `/user/**`开头的请求，代理到`lb://userservice`，lb是负载均衡，根据服务名拉取服务列表，实现负载均衡。

注意：gateway中配置rui的useservice和自己声明的服务名称**一致**，否则可能发生网管不能访问，但单独访问一个服务（ip）是可行的

### 4）重启测试

重启网关，访问http://localhost:10010/user/1时，符合`/user/**`规则，请求转发到uri：http://userservice/user/1，得到了结果：

![image-20210714211908341](SpringCloud/image-20210714211908341.png)

### 5）网关路由的流程图

整个访问的流程如下：

![image-20210714211742956](SpringCloud/image-20210714211742956.png)







总结：

网关搭建步骤：

1. 创建项目，引入nacos服务发现和gateway依赖

2. 配置application.yml，包括服务基本信息、nacos地址、路由

路由配置包括：

1. 路由id：路由的唯一标示

2. 路由目标（uri）：路由的目标地址，http代表固定地址，lb代表根据服务名负载均衡

3. 路由断言（predicates）：判断路由的规则，

4. 路由过滤器（filters）：对请求或响应做处理



接下来，就重点来学习路由断言和路由过滤器的详细知识





## 3.3.断言工厂

我们在配置文件中写的断言规则只是字符串，这些字符串会被Predicate Factory读取并处理，转变为路由判断的条件

例如Path=/user/**是按照路径匹配，这个规则是由

`org.springframework.cloud.gateway.handler.predicate.PathRoutePredicateFactory`类来

处理的，像这样的断言工厂在SpringCloudGateway还有十几个:

官方文档有案例

https://docs.spring.io/spring-cloud-gateway/docs/3.0.4-SNAPSHOT/reference/html/#gateway-request-predicates-factories

| **名称**   | **说明**                       | **示例**                                                     |
| ---------- | ------------------------------ | ------------------------------------------------------------ |
| After      | 是某个时间点后的请求           | -  After=2037-01-20T17:42:47.789-07:00[America/Denver]       |
| Before     | 是某个时间点之前的请求         | - Before=2031-04-13T15:14:47.433+08:00[Asia/Shanghai]        |
| Between    | 是某两个时间点之前的请求       | -  Between=2037-01-20T17:42:47.789-07:00[America/Denver],  2037-01-21T17:42:47.789-07:00[America/Denver] |
| Cookie     | 请求必须包含某些cookie         | - Cookie=chocolate, ch.p                                     |
| Header     | 请求必须包含某些header         | - Header=X-Request-Id, \d+                                   |
| Host       | 请求必须是访问某个host（域名） | -  Host=**.somehost.org,**.anotherhost.org                   |
| Method     | 请求方式必须是指定方式         | - Method=GET,POST                                            |
| Path       | 请求路径必须符合指定规则       | - Path=/red/{segment},/blue/**                               |
| Query      | 请求参数必须包含指定参数       | - Query=name, Jack或者-  Query=name                          |
| RemoteAddr | 请求者的ip必须是指定范围       | - RemoteAddr=192.168.1.1/24                                  |
| Weight     | 权重处理                       |                                                              |



我们只需要掌握Path这种路由工程就可以了。

![image-20210830143614342](SpringCloud/image-20210830143614342.png)

## 3.4.过滤器工厂

GatewayFilter是网关中提供的一种过滤器，可以对进入网关的请求和微服务返回的响应做处理：

![image-20210714212312871](SpringCloud/image-20210714212312871.png)



### 3.4.1.路由过滤器的种类

Spring提供了31种不同的路由过滤器工厂。例如：

https://docs.spring.io/spring-cloud-gateway/docs/3.0.4-SNAPSHOT/reference/html/#gatewayfilter-factories

| **名称**             | **说明**                     |
| -------------------- | ---------------------------- |
| AddRequestHeader     | 给当前请求添加一个请求头     |
| RemoveRequestHeader  | 移除请求中的一个请求头       |
| AddResponseHeader    | 给响应结果中添加一个响应头   |
| RemoveResponseHeader | 从响应结果中移除有一个响应头 |
| RequestRateLimiter   | 限制请求的流量               |



### 3.4.2.请求头过滤器

下面我们以AddRequestHeader 为例来讲解。

> **需求**：给所有进入userservice的请求添加一个请求头：Truth=itcast is freaking awesome!



只需要修改gateway服务的application.yml文件，添加路由过滤即可：

```yaml
spring:
  cloud:
    gateway:
      routes:
      - id: user-service 
        uri: lb://userservice 
        predicates: 
        - Path=/user/** 
        filters: # 过滤器
        - AddRequestHeader=Truth, Itcast is freaking awesome! # 添加请求头
```

当前过滤器写在userservice路由下，因此仅仅对访问userservice的请求有效。



### 3.4.3.默认过滤器

如果要对所有的路由都生效，则可以将过滤器工厂写到default下。格式如下：

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service 
          uri: lb://userservice 
          predicates: 
          - Path=/user/**
      default-filters: # 默认过滤项
        - AddRequestHeader=Truth, Itcast is freaking awesome! 
```



### 3.4.4.总结

过滤器的作用是什么？

① 对路由的请求或响应做加工处理，比如添加请求头

② 配置在路由下的过滤器只对当前路由的请求生效

**defaultFilters**的作用是什么？

① **对所有路由都生效的过滤器**



## 3.5.全局过滤器

上一节学习的过滤器，网关提供了31种，但每一种过滤器的作用都是固定的。如果我们希望拦截请求，做自己的业务逻辑则没办法实现。

### 3.5.1.全局过滤器作用

全局过滤器的作用也是处理一切进入网关的请求和微服务响应，与GatewayFilter的作用一样。区别在于GatewayFilter通过配置定义，处理逻辑是固定的；而GlobalFilter的逻辑需要自己写代码实现。

定义方式是实现GlobalFilter接口。

```java
public interface GlobalFilter {
    /**
     *  处理当前请求，有必要的话通过{@link GatewayFilterChain}将请求交给下一个过滤器处理
     *
     * @param exchange 请求上下文，里面可以获取Request、Response等信息
     * @param chain 用来把请求委托给下一个过滤器 
     * @return {@code Mono<Void>} 返回标示当前过滤器业务结束
     */
    Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain);
}
```



在filter中编写自定义逻辑，可以实现下列功能：

- 登录状态判断
- 权限校验
- 请求限流等





### 3.5.2.自定义全局过滤器

需求：定义全局过滤器，拦截请求，判断请求的参数是否满足下面条件：

- 参数中是否有authorization，

- authorization参数值是否为admin

如果同时满足则放行，否则拦截



实现：

在gateway中定义一个过滤器：

```java
package cn.itcast.gateway.filters;

import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

@Order(-1)
@Component
public class AuthorizeFilter implements GlobalFilter {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        // 1.获取请求参数
        MultiValueMap<String, String> params = exchange.getRequest().getQueryParams();
        // 2.获取authorization参数
        String auth = params.getFirst("authorization");
        // 3.校验
        if ("admin".equals(auth)) {
            // 放行
            return chain.filter(exchange);
        }
        // 4.拦截
        // 4.1.禁止访问，设置状态码
        exchange.getResponse().setStatusCode(HttpStatus.FORBIDDEN);
        // 4.2.结束处理
        return exchange.getResponse().setComplete();
    }
}
```

![image-20210830151636748](SpringCloud/image-20210830151636748.png)



### 3.5.3.过滤器执行顺序

请求进入网关会碰到三类过滤器：当前路由的过滤器、DefaultFilter、GlobalFilter

请求路由后，会将当前路由过滤器和DefaultFilter、GlobalFilter，合并到一个过滤器链（集合）中，排序后依次执行每个过滤器：

![image-20210714214228409](SpringCloud/image-20210714214228409.png)



排序的规则是什么呢？

- 每一个过滤器都必须指定一个int类型的order值，**order值越小，优先级越高，执行顺序越靠前**。
- GlobalFilter通过实现Ordered接口，或者添加@Order注解来指定order值，由我们自己指定
- 路由过滤器和defaultFilter的order由Spring指定，默认是**按照声明顺序从1递增。**
- 当**过滤器的order值一样**时，会按照 **defaultFilter > 路由过滤器 > GlobalFilter**的顺序执行。



详细内容，可以查看源码：

`org.springframework.cloud.gateway.route.RouteDefinitionRouteLocator#getFilters()`方法是先加载defaultFilters，然后再加载某个route的filters，然后合并。



`org.springframework.cloud.gateway.handler.FilteringWebHandler#handle()`方法会加载全局过滤器，与前面的过滤器合并后根据order排序，组织过滤器链

![image-20210830152420162](SpringCloud/image-20210830152420162.png)

## 3.6.跨域问题



### 3.6.1.什么是跨域问题

跨域：域名不一致就是跨域，主要包括：

- **域名不同**： www.taobao.com 和 www.taobao.org 和 www.jd.com 和 miaosha.jd.com

- 域名相同，端口不同：localhost:8080和localhost:8081

跨域问题：**浏览器禁止**请求的发起者与服务端发生**跨域ajax请求**，请求被浏览器拦截的问题



解决方案：CORS，这个以前应该学习过，这里不再赘述了。不知道的小伙伴可以查看https://www.ruanyifeng.com/blog/2016/04/cors.html

**CORS**是一个W3C标准，全称是**"跨域资源共享"（Cross-origin resource sharing）**。

它允许浏览器向跨源服务器，发出[`XMLHttpRequest`](https://www.ruanyifeng.com/blog/2012/09/xmlhttprequest_level_2.html)请求，从而克服了AJAX只能[同源](https://www.ruanyifeng.com/blog/2016/04/same-origin-policy.html)使用的限制。

### 3.6.2.模拟跨域问题

找到课前资料的页面文件：

![image-20210714215713563](SpringCloud/image-20210714215713563.png)

放入tomcat或者nginx这样的web服务器中，启动并访问。

可以安装npm，再安装live-server，再执行

```cmd
live-server --port 8090
```

live-server一款npm工具，全局npm i -g live-server后，项目目录使用live-server命令行命令便可直接在浏览器中预览（默认找index.html，其他请自行带上文件名空格后跟在后面），并且自动全局监听实时更新。



可以在浏览器控制台看到下面的错误：

![image-20210714215832675](SpringCloud/image-20210714215832675.png)



从localhost:8090访问localhost:10010，端口不同，显然是跨域的请求。



### 3.6.3.解决跨域问题

在gateway服务的application.yml文件中，添加下面的配置：

```yaml
spring:
  cloud:
    gateway:
      # 。。。
      globalcors: # 全局的跨域处理
        add-to-simple-url-handler-mapping: true # 解决options请求被拦截问题
        corsConfigurations:
          '[/**]': #/**表示拦截一切请求
            allowedOrigins: # 允许哪些网站的跨域请求 
              - "http://localhost:8090"
            allowedMethods: # 允许的跨域ajax的请求方式
              - "GET"
              - "POST"
              - "DELETE"
              - "PUT"
              - "OPTIONS"
            allowedHeaders: "*" # 允许在请求中携带的头信息
            allowCredentials: true # 是否允许携带cookie
            maxAge: 360000 # 这次跨域检测的有效期
```


## 相关链接
> 来源Bilibili黑马程序员的学习视频： [点我传送](https://www.bilibili.com/video/BV1LQ4y127n4?spm_id_from=333.999.0.0)
















