# 2.JVM进程缓存—本地缓存

为了演示多级缓存的案例，我们先准备一个商品查询的业务。

## 2.1.导入案例

参考本笔记文件中         [案例导入说明](#案例导入说明)章节笔记

## 2.2.初识Caffeine

中文官网：https://github.com/ben-manes/caffeine/wiki/Home-zh-CN



**本地进程缓存**

缓存在日常开发中启动至关重要的作用，由于是存储在内存中，数据的读取速度是非常快的，能大量减少对数据库的访问，减少数据库的压力。我们把缓存分为两类：

- 分布式缓存，例如Redis：
  - 优点：**存储容量更大、可靠性更好**、可以在集群间共享
  - 缺点：访问缓存有网络开销
  - 场景：缓存数据量较大、可靠性要求较高、需要在集群间共享
- 进程本地缓存，例如HashMap、GuavaCache：
  - 优点：读取本地内存，没有网络开销，速度更快
  - 缺点：存储容量有限、可靠性较低、无法共享
  - 场景：性能要求较高，缓存数据量较小

我们今天会利用Caffeine框架来实现JVM进程缓存。



**Caffeine**是一个基于Java8开发的，提供了近乎最佳命中率的高性能的本地缓存库。目前Spring内部的缓存使用的就是Caffeine。GitHub地址：https://github.com/ben-manes/caffeine

Caffeine的性能非常好，下图是官方给出的性能对比：

![image-20210821081826399](img/img_JVM%E8%BF%9B%E7%A8%8B%E7%BC%93%E5%AD%98-Caffeine/image-20210821081826399.png)

可以看到Caffeine的性能遥遥领先！



### 缓存使用的基本API



```java
@Test
void testBasicOps() {
    // 构建cache对象
    Cache<String, String> cache = Caffeine.newBuilder().build();

    // 存数据
    cache.put("gf", "迪丽热巴");

    // 取数据
    String gf = cache.getIfPresent("gf");
    System.out.println("gf = " + gf);

    // 取数据，包含两个参数：
    // 参数一：缓存的key
    // 参数二：Lambda表达式，表达式参数就是缓存的key，方法体是查询数据库的逻辑
    // 优先根据key查询JVM缓存，如果未命中，则执行参数二的Lambda表达式
    String defaultGF = cache.get("defaultGF", key -> {
        // 根据key去数据库查询数据
        return "柳岩";
    });
    System.out.println("defaultGF = " + defaultGF);
}
```



### Caffeine缓存的清除策略

Caffeine既然是缓存的一种，肯定需要有缓存的清除策略，不然的话内存总会有耗尽的时候。

Caffeine提供了三种缓存驱逐策略：

- **基于容量**：**设置缓存的数量上限**

  ```java
  // 创建缓存对象
  Cache<String, String> cache = Caffeine.newBuilder()
      .maximumSize(1) // 设置缓存大小上限为 1
      .build();
  ```

- **基于时间**：设置缓存的有效时间

  ```java
  // 创建缓存对象
  Cache<String, String> cache = Caffeine.newBuilder()
      // 设置缓存有效期为 10 秒，从最后一次写入开始计时 
      .expireAfterWrite(Duration.ofSeconds(10)) 
      .build();
  
  ```

- **基于引用**：设置**缓存为软引用或弱引用，利用GC来回收缓存数据**。性能较差，不建议使用。

- 基于权重：

> **注意**：在默认情况下，当一个缓存元素过期的时候，Caffeine不会自动立即将其清理和驱逐。而是在一次读或写操作后，或者在空闲时间完成对失效数据的驱逐。



```java
/*
      基本用法测试
     */
@Test
void testBasicOps() {
    // 创建缓存对象
    Cache<String, String> cache = Caffeine.newBuilder().build();

    // 存数据
    cache.put("gf", "迪丽热巴");

    // 取数据，不存在则返回null
    String gf = cache.getIfPresent("gf");
    System.out.println("gf = " + gf);

    // 取数据，不存在则去数据库查询
    String defaultGF = cache.get("defaultGF", key -> {
        // 这里可以去数据库根据 key查询value
        return "柳岩";
    });
    System.out.println("defaultGF = " + defaultGF);

    Cache<Integer, String> testCache = Caffeine.newBuilder()
        .initialCapacity(100)
        .maximumSize(10_000)
        .expireAfterWrite(Duration.ofDays(1))
        .expireAfterAccess(Duration.ofDays(1))
        .build();
}

/*
     基于大小设置驱逐策略：
     */
@Test
void testEvictByNum() throws InterruptedException {
    // 创建缓存对象
    Cache<String, String> cache = Caffeine.newBuilder()
        // 设置缓存大小上限为 1
        .maximumSize(2)
        .softValues()
        .build();
    // 存数据
    cache.put("gf1", "柳岩");
    cache.put("gf2", "范冰冰");
    cache.put("gf3", "迪丽热巴");
    // 延迟10ms，给清理线程一点时间
    //Thread.sleep(10L);
    cache.cleanUp();
    // 获取数据
    System.out.println("gf1: " + cache.getIfPresent("gf1"));
    System.out.println("gf2: " + cache.getIfPresent("gf2"));
    System.out.println("gf3: " + cache.getIfPresent("gf3"));
}

/*
     基于时间设置驱逐策略：
     */
@Test
void testEvictByTime() throws InterruptedException {
    // 创建缓存对象
    Cache<String, String> cache = Caffeine.newBuilder()
        .expireAfterWrite(Duration.ofSeconds(1)) // 设置缓存有效期为 10 秒
        .build();
    // 存数据
    cache.put("gf", "柳岩");
    // 获取数据
    System.out.println("gf: " + cache.getIfPresent("gf"));
    // 休眠一会儿
    Thread.sleep(1200L);
    System.out.println("gf: " + cache.getIfPresent("gf"));
}
```

## 使用Caffeine

### 导入依赖

注： JDK8只能使用2.x版本

```java
<dependency>
    <groupId>com.github.ben-manes.caffeine</groupId>
    <artifactId>caffeine</artifactId>
    <version>2.8.8</version>
</dependency>
```



## 2.3.实现JVM进程缓存

### 2.3.1.需求

利用Caffeine实现下列需求：

- 给根据id查询商品的业务添加缓存，缓存未命中时查询数据库
- 给根据id查询商品库存的业务添加缓存，缓存未命中时查询数据库
- 缓存初始大小为100
- 缓存上限为10000



### 2.3.2.实现

首先，我们需要定义两个Caffeine的缓存对象，分别保存商品、库存的缓存数据。

在item-service的`com.heima.item.config`包下定义`CaffeineConfig`类：

```java
package com.heima.item.config;

import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import com.heima.item.pojo.Item;
import com.heima.item.pojo.ItemStock;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CaffeineConfig {

    @Bean
    public Cache<Long, Item> itemCache(){
        return Caffeine.newBuilder()
                .initialCapacity(100)
                .maximumSize(10_000)
                .build();
    }

    @Bean
    public Cache<Long, ItemStock> stockCache(){
        return Caffeine.newBuilder()
                .initialCapacity(100)
                .maximumSize(10_000)
                .build();
    }
}
```



然后，修改item-service中的`com.heima.item.web`包下的ItemController类，添加缓存逻辑：

```java
@RestController
@RequestMapping("item")
public class ItemController {

    @Autowired
    private IItemService itemService;
    @Autowired
    private IItemStockService stockService;

    @Autowired
    private Cache<Long, Item> itemCache;
    @Autowired
    private Cache<Long, ItemStock> stockCache;
    
    // ...其它略
    
    @GetMapping("/{id}")
    public Item findById(@PathVariable("id") Long id) {
        return itemCache.get(id, key -> itemService.query()
                .ne("status", 3).eq("id", key)
                .one()
        );
    }

    @GetMapping("/stock/{id}")
    public ItemStock findStockById(@PathVariable("id") Long id) {
        return stockCache.get(id, key -> stockService.getById(key));
    }
}
```


