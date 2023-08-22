# Ribbon七种负载均衡策略详解

## Ribbon是什么？

主要负责请求分发，例如一个服务节点集群：六台服务器部署着订单服务，用户请求过来了就要根据不同的负载策略分发请求到不同机器上，起到一个缓解请求压力的作用。其自身不会发起请求，这个在源码中可以到，它起到一个“选择”的角色。真正发起请求的还是Feign / OpenFeign 。

## Ribbon与Nginx的区别？

看到上诉的描述跟nginx非常接近，两者都是做轮询，做负载分发请求。那么区别是什么？看图

![在这里插入图片描述](img/img_Ribbon%E4%B8%83%E7%A7%8D%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%E7%AD%96%E7%95%A5%E8%AF%A6%E8%A7%A3/20200921100312864.png)

可以看到，Nginx是属于服务器端的负载均衡，Ribbon是属于客户端的负载均衡，简而言之，Nginx的客户端发起请求不知道会被负载到哪台服务器上，但是Ribbon发起的请求都是非常明确的，就像调用本地服务一样，更广的范围说：Nginx是进程之间调用时候做的负载均衡，Ribbon是进程内部选择调用时候做的负载均衡～
所以微服务架构采用的就是Ribbon，两者还是有一定差距的。

## 怎么用？

由于在Eureka注册中心和OpenFeign中都已经集成了，所以我们连依赖都不用加了。

![在这里插入图片描述](img/img_Ribbon%E4%B8%83%E7%A7%8D%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%E7%AD%96%E7%95%A5%E8%AF%A6%E8%A7%A3/20200921102454260.png)

![在这里插入图片描述](img/img_Ribbon%E4%B8%83%E7%A7%8D%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%E7%AD%96%E7%95%A5%E8%AF%A6%E8%A7%A3/20200921102505162.png)

### （1）启动类上加：@RibbonClient

同时可以指定注册中心中的server name ，这样一个server name 列表下管理的全部集群服务就可以被负载策略自由选择

如果有多个服务的情况下：

（2）OpenFeign做服务调用那里再加上要请求的server name即可，不同的服务调用记得区分不同的接口。例如这里是CIRCULATE-SERVICE的，DEMO-SERVICE另写一个接口。

（3）如果还是用RestTemplate这种请求方式的话，就在RestTemplate的Config类中加上一个注解：


但是既然都用cloud了，应该都使用Feign组件了吧。。。

如何指定负载均衡的规则？



新增自己的RibbonRule，但是不能够和启动类同一个包下面。因为启动类中的@SpringBootApplication注解里面，有一个@ComponentScan，自动扫描跟启动类同级的类，这样我们定义多个@RibbonClient的时候，它们就会共用一种负载策略。如果一定放到同级目录下，也可以手动exclude排除掉。

## 上面一直说帮我们做负载，Ribbon具体有哪几种负载均衡？

### （1）RoundRobinRule轮询（默认）：

第一次到A，第二次就到B，第三次又到A，第四次又到B…
具体实现是一个负载均衡算法：第N次请求 % 服务器集群的总数 = 实际调用服务器位置的下标
那么怎么保证线程安全问题呢？因为N次请求次数会自增，怎么保证不会多次请求都拿到同一个N进行自增？答案就是简单的CAS：

关于CAS，有另外一篇记录：Lock锁+CAS+与Synchronized比较

### （2）RandomRule随机


再进去看（我看源码看到这一块看不懂了，求大佬赐教），只知道返回存活服务列表中的随机一个服务的下标，然后在存活列表upList.get(index) 这样去拿到随机的server返回：

### （3）RetryRule轮询重试（重试采用的默认也是轮询）

### （4）WeightedResponseTimeRule响应速度决定权重：

这个源码很长很复杂，就不放出来了，其实是对RoundRobbin的一种增强，加入了权重和计算响应时间的概念，其中响应速度最快的权重越大，权重越大则选中的概率越大。

### （5）BestAvailableRule最优可用（底层也有RoundRobinRule）：

最优可用，判断最优其实用的是并发连接数。选择并发连接数较小的server发送请求。

### （6）AvailabilityFilteringRule可用性过滤规则（底层也有RoundRobinRule）：

我直接翻译就是可用过滤规则，其实它功能是先过滤掉不可用的Server实例，再选择并发连接最小的实例。

### （7）ZoneAvoidanceRule区域内可用性能最优：

基于AvailabilityFilteringRule基础上做的，首先判断一个zone的运行性能是否可用，剔除不可用的区域zone的所有server，然后再利用AvailabilityPredicate过滤并发连接过多的server。
源码真的很长，我不跟下去了…大概就是这么个意思还挺好理解。

也可以自定义负载均衡规则，模仿它们的写法，继承RoundRibbonRule，重写一些方法，加上自己的Server即可。先总结到这里，如果有理解错误的希望指正，以后有更多领悟再补充进来分享～

## 链接

原文链接：https://blog.csdn.net/whiteBearClimb/article/details/108703356