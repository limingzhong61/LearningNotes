# 花一个周末，掌握 SpringCloud OpenFeign 核心原理



## **前言**

现在的微服务在互联网圈子里应用已经相关广泛了，SpringCloud 是微服务领域当之无愧的 "头牌"

加上现在的一些轮子项目，新建一个全套的 SpringCloud 项目分分钟的事情，而我们要做的事情，就是不把认知停留在使用层面，所以要深入到源码中去理解 SpringCloud

**为什么要选择 OpenFien？** 因为它足够的 "小"，符合我们的标题：**一个周末搞定**

Feign 的源代码中，Java 代码才 3w 多行，放眼现在热门的开源项目，包括不限于 Dubbo、Naocs、Skywalking 中 Java 代码都要 30w 行起步

通过本篇文章，希望读者朋友可以掌握如下知识

- 什么是 Feign
- Feign 和 Openfeign 的区别
- OpenFeign 的启动原理
- OpenFeign 的工作原理
- OpenFeign 如何负载均衡

> spring-cloud-starter-openfeign version：2.2.6.RELEASE

## **什么是 Feign**

Feign 是声明式 Web 服务客户端，它使编写 Web 服务客户端更加容易

Feign 不做任何请求处理，通过处理注解相关信息生成 Request，并对调用返回的数据进行解码，从而实现 **简化 HTTP API 的开发**

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-c117870db6e72775ffe7c1e30745be69_1440w.webp)

如果要使用 Feign，需要创建一个接口并对其添加 Feign 相关注解，另外 Feign **还支持可插拔编码器和解码器**，致力于打造一个轻量级 HTTP 客户端

```text
微信搜索【源码兴趣圈】，关注龙台，回复【资料】领取涵盖 GO、Netty、
SpringCloud Alibaba、Seata、开发规范、面试宝典、数据结构等电子书 or 视频学习资料！
```

## **Feign 和 Openfeign 的区别**

Feign 最早是由 **Netflix 公司进行维护的**，后来 Netflix 不再对其进行维护，最终 **Feign 由社区进行维护**，更名为 Openfeign

> 为了少打俩字，下文简称 Opefeign 为 Feign

并将原项目迁移至新的仓库，所以我们在 Github 上看到 Feign 的坐标如下

```xml
<groupId>io.github.openfeign</groupId>
<artifactId>parent</artifactId>
<version>...</version>
```

### **Starter Openfeign**

当然了，基于 SpringCloud 团队对 Netflix 的情有独钟，你出了这么好用的轻量级 HTTP 客户端，我这老大哥不得支持一下，所以就有了基于 Feign 封装的 Starter

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

Spring Cloud 添加了对 Spring MVC 注解的支持，并支持使用 Spring Web 中默认使用的相同 HttpMessageConverters

另外，Spring Cloud 老大哥同时集成了 Ribbon 和 Eureka 以及 Spring Cloud LoadBalancer，以在使用 Feign 时提供负载均衡的 HTTP 客户端

> 针对于注册中心的支持，包含但不限于 Eureka，比如 Consul、Naocs 等注册中心均支持

在我们 SpringCloud 项目开发过程中，使用的大多都是这个 Starter Feign

## **环境准备**

为了方便大家理解，这里写出对应的生产方、消费方 Demo 代码，以及使用的注册中心

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-4cfc2f3f9d53cf7a4ba88d501cc57e0a_1440w.webp)

注册中心使用的 Nacos，生产、消费方代码都比较简单。另外为了阅读体验感，**文章原则是少放源码**，更多的是给大家梳理核心逻辑

### **生产者服务**

添加 Nacos 服务注册发现注解以及发布出 HTTP 接口服务

```java
@EnableDiscoveryClient @SpringBootApplication
public class NacosProduceApplication {
    public static void main(String[] args) {
        SpringApplication.run(NacosProduceApplication.class, args);
    }
    @RestController
    static class TestController {
        @GetMapping("/hello")
        public String hello(@RequestParam("name") String name) {
            return "hello " + name;
        }
    }
}
```

### **消费者服务**

定义 FeignClient 消费服务接口

```java
@FeignClient(value = "nacos-produce")
public interface DemoFeignClient {
    @RequestMapping(value = "/hello", method = RequestMethod.GET)
    String sayHello(@RequestParam("name") String name);
}
```

因为生产者使用 Nacos，所以消费者除了开启 Feign 注解，同时也要开启 Naocs 服务注册发现

```java
@RestController @EnableFeignClients
@EnableDiscoveryClient @SpringBootApplication
public class NacosConsumeApplication {
    public static void main(String[] args) {
        SpringApplication.run(NacosConsumeApplication.class, args);
    }

    @Autowired private DemoFeignClient demoFeignClient;

    @GetMapping("/test")
    public String test() {
        String result = demoFeignClient.sayHello("公号-源码兴趣圈");
        return result;
    }
}
```

## **Feign 的启动原理**

我们在 SpringCloud 的使用过程中，如果想要启动某个组件，一般都是 **@Enable...** 这种方式注入，Feign 也不例外，我们需要在类上标记此注解 `@EnableFeignClients`

```java
@EnableFeignClients
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

继续深入看一下注解内部都做了什么。注解内部的方法就不说明了，不加会有默认的配置，感兴趣可以跟下源码

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
@Import(FeignClientsRegistrar.class)
public @interface EnableFeignClients {...}
```

前三个注解看着平平无奇，重点在第四个 @Import 上，一般使用此注解都是想要动态注册 Spring Bean 的

### **注入@Import**

通过名字也可以大致猜出来，这是 Feign 注册 Bean 使用的，使用到了 Spring 相关的接口，一起看下起了什么作用

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-c0c21395583fe9733504791d9fad3d33_1440w.webp)

ResourceLoaderAware、EnvironmentAware 为 FeignClientsRegistrar 中两个属性 **resourceLoader、environment** 赋值，对 Spring 了解的小伙伴理解问题不大

ImportBeanDefinitionRegistrar 负责动态注入 IOC Bean，分别注入 Feign 配置类、FeignClient Bean

```java
// 资源加载器，可以加载 classpath 下的所有文件
private ResourceLoader resourceLoader;
// 上下文，可通过该环境获取当前应用配置属性等
private Environment environment;

@Override
public void setEnvironment(Environment environment) {
    this.environment = environment;
}

@Override
public void setResourceLoader(ResourceLoader resourceLoader) {
    this.resourceLoader = resourceLoader;
}

@Override
public void registerBeanDefinitions(AnnotationMetadata metadata, BeanDefinitionRegistry registry) {
   // 注册 ＠EnableFeignClients 提供的自定义配置类中的相关 Bean 实例
    registerDefaultConfiguration(metadata,registry);
    // 扫描 packge，注册被 @FeignClient 修饰的接口类为 IOC Bean
    registerFeignClients(metadata, registry);
}
```

### **添加全局配置**

registerDefaultConfiguration 方法流程如下

1. 获取 @EnableFeignClients 注解上的属性以及对应 Value
2. 生成 **FeignClientSpecification**（存储 Feign 中的配置类） 对应的构造器 BeanDefinitionBuilder
3. FeignClientSpecification Bean 名称为 default. + @EnableFeignClients 修饰类全限定名称 + FeignClientSpecification
4. @EnableFeignClients defaultConfiguration 默认为 {}，如果没有相关配置，`默认使用 FeignClientsConfiguration` 并结合 name 填充到 FeignClientSpecification，最终注册为 IOC Bean

### **注册 FeignClient 接口**

将重点放在 registerFeignClients 上，该方法主要就是将修饰了 @FeignClient 的接口注册为 IOC Bean

1. 扫描 @EnableFeignClients 注解，如果有 clients，则加载指定接口，为空则根据 scanner 规则扫描出修饰了 @FeignClient 的接口
2. 获取 @FeignClient 上对应的属性，根据 configuration 属性去创建接口级的 **FeignClientSpecification** 配置类 IOC Bean
3. 将 @FeignClient 的属性设置到 **FeignClientFactoryBean** 对象上，并注册 IOC Bean

@FengnClient 修饰的接口实际上使用了 Spring 的代理工厂生成代理类，所以这里会把修饰了 @FeignClient 接口的 BeanDefinition 设置为 FeignClientFactoryBean 类型，而 **FeignClientFactoryBean 继承自 FactoryBean**

也就是说，当我们定义 @FeignClient 修饰接口时，注册到 IOC 容器中 Bean 类型变成了 FeignClientFactoryBean

在 Spring 中，FactoryBean 是一个工厂 Bean，用来创建代理 Bean。**工厂 Bean 是一种特殊的 Bean**，对于需要获取 Bean 的消费者而言，它是不知道 Bean 是普通 Bean 或是工厂 Bean 的。**工厂 Bean 返回的实例不是工厂 Bean 本身**，而是会返回执行了工厂 Bean 中 `FactoryBean#getObject` 逻辑的实例

## **Feign 的工作原理**

说 Feign 的工作原理，核心点围绕在被 @FeignClient 修饰的接口，如何发送及接收 HTTP 网络请求

上面说到 @FeignClient 修饰的接口最终填充到 IOC 容器的类型是 FeignClientFactoryBean，先来看下它是什么

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-d76a3187db4933a6f86a47f1c9019038_1440w.webp)

### **FactoryBean 接口特征**

这里说一下 FeignClientFactoryBean 都有哪些特征

1. 它会在类初始化时执行一段逻辑，依据 Spring **InitializingBean** 接口
2. 如果它被别的类 @Autowired 进行注入，返回的不是它本身，而是 `FactoryBean#getObject` 返回的类，依据 Spring **FactoryBean** 接口
3. 它能够获取 Spring 上下文对象，依据 Spring **ApplicationContextAware** 接口

先来看它的初始化逻辑都执行了什么

```java
@Override
public void afterPropertiesSet() {
    Assert.hasText(contextId, "Context id must be set");
    Assert.hasText(name, "Name must be set");
}
```

没有特别的操作，只是使用断言工具类判断两个字段不为空。ApplicationContextAware 也没什么说的，获取上下文对象赋值到对象的局部变量里，重点以及关键就是 `FactoryBean#getObject` 方法

```java
@Override
public Object getObject() throws Exception {
    return getTarget();
}
```

getTarget 源码方法还是挺长的，这里采用分段的形式展示

```java
<T> T getTarget() {
   // 从 IOC 容器获取 FeignContext
    FeignContext context = applicationContext.getBean(FeignContext.class);
   // 通过 context 创建 Feign 构造器
    Feign.Builder builder = feign(context);
  ...
}
```

这里提出一个疑问？FeignContext 什么时候、在哪里被注入到 Spring 容器里的？

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-05596c34022bd38e6e22c1616860359f_1440w.webp)

看到图片小伙伴就明了了，用了 SpringBoot 怎么会不使用自动装配的功能呢，FeignContext 就是在 FeignAutoConfiguration 中被成功创建

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-6e0e52825df29912083704757f74b190_1440w.webp)

### **初始化父子容器**

feign 方法里日志工厂、编码、解码等类均是通过 get(...) 方法得到

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-e70f31cc0117edcd93ead7b2454db0f8_1440w.webp)

这里涉及到 Spring 父子容器的概念，**默认子容器 Map 为空**，获取不到服务名对应 Context 则新建

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-1639b96b629f42de60a9b97860bb474c_1440w.webp)

从下图中看到，注册了一个 **FeignClientsConfiguration** 类型的 Bean，我们上述方法 feign 中的获取的编码、解码器等组件都是从此类中获取默认

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-cc5bdd458f11f14cda07e9491fbbe6b8_1440w.webp)

默认注册如下，FeignClientsConfiguration 是由创建 FeignContext 调用父类 Super 构造方法传入的

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-7c430b668c81068e0332011b3ac2807f_1440w.webp)

关于父子类容器对应关系，以及提供 @FeignClient 服务对应子容器的关系（每一个服务对应一个子容器实例）

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-791c51e062b5be5aed0ae067eb958ba6_1440w.webp)

回到 getInstance 方法，子容器此时已加载对应 Bean，直接通过 getBean 获取 **FeignLoggerFactory**

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-5b1cbb15dc83770926ce84c0a2dfb8da_1440w.webp)

如法炮制，Feign.Builder、Encoder、Decoder、Contract 都可以通过子容器获取对应 Bean

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-189bf296e59aff78791dbf0889107523_1440w.webp)

configureFeign 方法主要进行一些配置赋值，**比如超时、重试、404 配置等**，就不再细说赋值代码了

到这里有必要总结一下创建 Spring 代理工厂的前半场代码

1. 注入@FeignClient 服务时，其实注入的是 `FactoryBean#getObject` 返回代理工厂对象
2. 通过 IOC 容器获取 FeignContext 上下文
3. 创建 Feign.Builder 对象时会创建 Feign 服务对应的子容器
4. 从子容器中获取日志工厂、编码器、解码器等 Bean
5. 为 Feign.Builder 设置配置，比如超时时间、日志级别等属性，每一个服务都可以个性化设置

### **动态代理生成**

继续嗑，上面都是开胃菜，接下来是最最最重要的地方了，小板凳坐板正了..

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-ece80c6cb3de2b0599d38bbc1a9ee786_1440w.webp)

因为我们在 @FeignClient 注解是使用 name 而不是 url，所以会执行负载均衡策略的分支

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-59460fe19618f681b7efc5e28d578f84_1440w.webp)

Client： Feign 发送请求以及接收响应等都是由 Client 完成，该类默认 Client.Default，另外支持 HttpClient、OkHttp 等客户端

代码中的 Client、Targeter 在自动装配时注册，配合上文中的父子容器理论，这两个 Bean 在父容器中存在

因为我们并没有对 Hystix 进行设置，所以走入此分支

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-62e40497bc125f8479c5c06faac8239c_1440w.webp)

创建反射类 ReflectiveFeign，然后执行创建实例类

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-5f65947a47d62b424b91923e3355f0be_1440w.webp)

newInstance 方法对 @FeignClient 修饰的接口中 SpringMvc 等配置进行解析转换，对接口类中的方法进行归类，生成动态代理类

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-c0a894f64c4e2f83ea9e6665d255f4d6_1440w.webp)

可以看出 Feign 创建动态代理类的方式和 Mybatis Mapper 处理方式是一致的，因为两者都没有实现类

根据 newInstance 方法按照行为大致划分，共做了四件事

1. 处理 @FeignCLient 注解（SpringMvc 注解等）封装为 **MethodHandler** 包装类
2. 遍历接口中所有方法，过滤 Object 方法，并将默认方法以及 FeignClient 方法分类
3. 创建动态代理对应的 **InvocationHandler** 并创建 Proxy 实例
4. 接口内 default 方法 **绑定动态代理类**

MethodHandler 将方法参数、方法返回值、参数集合、请求类型、请求路径进行解析存储

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-002dea2e65375c3bd1d84f61702c668f_1440w.webp)

到这里我们也就可以 Feign 的工作方式了。前面那么多封装铺垫，封装个性化配置等等，最终确定收尾的是创建动态代理类

也就是说在我们调用 @FeignClient 接口时，会被 `FeignInvocationHandler#invoke` 拦截，并在动态代理方法中执行下述逻辑

1. 接口注解信息封装为 HTTP Request
2. 通过 Ribbon 获取服务列表，并对服务列表进行负载均衡调用（**服务名转换为 ip+port**）
3. 请求调用后，将返回的数据封装为 HTTP Response，继而转换为接口中的返回类型

既然已经明白了调用流程，那就正儿八经的试一哈，试过才知有没有...

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-1895a2df5ad2739869f2d455514f78e8_1440w.webp)

RequestTemplate：构建 Request 模版类

Options：存放连接、超时时间等配置类

Retryer：失败重试策略类

> 重试这一块逻辑看了很多遍，但是怎么看，一个 continue 关键字放到 while 的最后面都有点多余...

执行远端调用逻辑中使用到了 **Rxjava （响应式编程）**，可以看到通过底层获取 server 后将服务名称转变为 ip+port 的方式

这种响应式编程的方式在 SpringCloud 中很常见，**Hystix 源码底层也有使用**

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-bfd211af980f952990e31ce86ee4cf49_1440w.webp)

网络调用默认使用 **HttpURLConnection**，可以配置使用 HttpClient 或者 OkHttp

调用远端服务后，再将返回值解析正常返回，到这里一个完成的 Feign 调用链就聊明白了

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-2b2d7f7222de6b178cde89ecb7f86114_1440w.webp)

## **Feign 如何负载均衡**

一般而言，我们生产者注册多个服务，消费者调用时需要使用负载均衡从中 **选取一个健康并且可用的生产者服务**

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-cd503dcf36feb0ed270ffa0a5f4bd39f_1440w.webp)

因为 Feign 内部集成 Ribbon，所以也支持此特性，一起看下它是怎么做的

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-a1fe59424d9c6a2c86172373e541af46_1440w.webp)

我们在 Nacos 上注册了两个服务，端口号 8080、8081。在获取负载均衡器时就可以获取服务集合

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-3e31d18e008a679c6519302dbbd5d797_1440w.webp)

然后通过 chooseServer 方法选择一个健康实例返回，后面会新出一篇文章对 Ribbon 的负载均衡详细说明

![img](img/img_SpringCloud%20OpenFeign%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86/v2-78f4f754e14ff461ce8dca7f9358b999_1440w.webp)

通过返回的 Server 替换 URL 中的服务名，最后使用网络调用服务进行远端调用，完美的一匹

## **结语**

文章从最基础的知识介绍什么是 Feign？继而从源码的角度上说明 Feign 的底层原理，总结如下：

1. 通过 @EnableFeignCleints 注解启动 Feign Starter 组件
2. Feign Starter 在项目启动过程中注册全局配置，扫描**包下所有的 @FeignClient 接口类，并进行注册 IOC 容器**
3. @FeignClient 接口类被注入时，通过 `FactoryBean#getObject` 返回动态代理类
4. **接口被调用时被动态代理类逻辑拦截**，**将 @FeignClient 请求信息通过编码器生成 Request**
5. **交由 Ribbon 进行负载均衡**，挑选出一个健康的 Server 实例
6. 继而**通过 Client 携带 Request 调用远端服务返回请求响应**
7. 通过**解码器生成 Response 返回客户端，将信息流解析成为接口返回数据**

虽然 Feign 体量相对小，但是想要一篇文章完全描述，也不太现实，所以这里都是挑一些核心点讲解，没有写到的地方还请见谅

另外，由于作者水平有限, 欢迎大家能够反馈指正文章中错误不正确的地方, 感谢

### fegin如何获取到他要调用的服务完整地址

feign没有再实现一遍，而是整合了ribbon，因为在springcloud中使用feign的时候，其实我们只在@FeignClient中配置了服务的名称，没有具体的地址，所以feign如果想调用远程的服务，肯定得知道地址，而ribbon刚好是一个负载均衡的组件，所以feign就通过整合ribbon，从ribbon中获取一个服务的地址调用，ribbon的中的服务实例信息来自注册中心，所以ribbon要想知道服务实例的数据，需要注册中心（nacos等）来适配ribbon，nacos只是提供服务实例的数据，ribbon是从这个服务实例中选择一个给feign，feign就用这个选择的实例来进行远程调用。

## 参考文章：

- 原文：https://zhuanlan.zhihu.com/p/346273428

- [https://blog.csdn.net/forezp/article/details/73480304](https://link.zhihu.com/?target=https%3A//blog.csdn.net/forezp/article/details/73480304)
- [https://www.cnblogs.com/yangxiaohui227/p/12965340.html](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/yangxiaohui227/p/12965340.html)
- [https://www.cnblogs.com/crazymakerc](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/crazymakercircle/p/11965726.html)