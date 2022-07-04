---

title: Redis
date: 2021-11-2 10:40:06

categories: Redis

---

 Redis 是一个开源（BSD许可）的，**内存中的数据结构存储系统**，它可以用作数据库、**缓存**和消息中间件。

## Java中使用Redis

SpringBoot使用Redis，详见：

**[springBoot-high.md](../java-note/SpringBootHigh/springBoot-high.md)中的redis内容**

## My

### 1、安装redis：使用docker；

**启动redis，默认端口6379**

```shell
[root@MiWiFi-R3A-srv ~]# docker run -d -p 6379:6379 --name myredis redis
ba86c7f5d285b74828df3ec4f0179cfcd3682dc58f2cfabe354a63336d94919e
#开启持久化
docker run  -d -p 6379:6379 --name persistent-redis redis --appendonly yes

docker run --name="redis-2" -d -p 6378:6379 -v /home/fr/redis:/opt royfans/redis:v1 /usr/local/redis/bin/redis-server /usr/local/redis/redis.conf --appendonly yes

```

==**注意**==：**如果不开启持久化，会导致一段时间不用缓存之后，连接不上redis**

**start with persistent storage**

```shell
docker run -v /myredis/conf/redis.conf:/home/ubuntu/redis/redis.conf -d -p 6379:6379 --name config-redis redis --appendonly yes

$ docker run --name some-redis -d redis redis-server --appendonly yes

```



```shell
$ docker run -v /myredis/conf/redis.conf:/usr/local/etc/redis/redis.conf --name myredis redis redis-server /usr/local/etc/redis/redis.conf

```

Where /myredis/conf/ is a local directory containing your redis.conf file. Using this method means that there is no need for you to have a Dockerfile for your redis container.



```
这个问题我们在项目中遇到同样的问题，目前已经解决了。最终得到的答案是： 服务器不稳定造成的。
您可以尝试这样解决：
1.推荐使用生产环境的服务器，并且将redis 绑定生产环境的ip;因为云服务器的ip 地址是很稳定的，而本地服务的ip地址经常是变动的；经 
   过测试，这种每过10分就会重新请求连接，还会发生重试失败的情况，就是因为服务器不稳定造成的；
2.如果你在生产环境中，使用docker 部署，建议 不要在docker容器中 安装redis; 因为docker 容器 默认分配的ip 地址，也可能是变化的；
  您可以直接将redis 安装在 服务器目录下，即可；

```



redis desktop manager连接

![1565350310934](.\Redis\redis desktop manager连接.png)