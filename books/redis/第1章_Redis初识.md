## Redis 是什么

* 开源
* 基于键值的存储服务系统

> 类似于Java中的
>
> ```java
> String value = map.get("key")
> ```

* 支持多种数据结构

![image-20210125155840187](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125155840187.png)

* 高性能，功能丰富

## Redis 的特性回顾

* 速度快

> 官方数据为： `10w OPS`(每秒10W次读写)，Redis 是内存数据库，它会把数据全部存储在内存中，这是它速度快的主要原因。

* 持久化

> `AOF`和`RDB`持久化存储

* 多种数据结构

> 除了传统支持的5种数据结构，新版本支持了`BitMaps`(位图)、`HyperLogLog`(超小内存唯一值计数)、`GEO`(地理信息定位)

* 支持多种编程语言
* 功能丰富

> * 发布订阅
> * Lua脚本
> * 支持事务
> * PipeLine ： 提升并发效率

* 使用简单

> * 安装简单： 不依赖外部库
> * 单线程模型

* 支持主从复制

> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125161101845.png" alt="image-20210125161101845" style="zoom:67%;" />

* 支持高可用、分布式

> * `Redis-Sentinel(v2.8)` 支持高可用
> * `Redis-Cluster(v3.0)`支持分布式

## Redis单机安装

### Redis 安装

1. `wget https://download.redis.io/releases/redis-6.0.10.tar.gz`
2. `tar -vxzf redis-6.0.10.tar.gz `
3. `ln -s redis-6.0.10 redis`
4. `cd redis`
5. `make && make install`

> 详细安装教程查看[CentOS 7.7系统安装Redis 6.0.3](https://www.cnblogs.com/sanduzxcvbnm/p/12955145.html)

### 可执行文件说明

* `redis-server`： Redis 服务器
* `redis-cli`: Redis 命令行客户端
* `redis-benchmark`: Redis性能测试
* `redis-check-aof`: 修复AOF文件
* `redis-check-dump`: RDB文件检查工具 
* `redis-sentinel`: `Sentinel`服务器(2.8以后)

### 三种启动方法

* 最简启动

> 直接运行`redis-server`启动

* 动态参数启动

> `redis-server --port  6380`

* 配置文件启动

> `redis-server <configPath>`

三种启动方式比较

1. 生产环境选择配置文件启动
2. 单机多实例配置文件可以用端口区分开

### 简单的客户端连接

```shell
$ redis-cli -h 127.0.0.1 -p 6379
127.0.0.1:6379> ping
PONG
127.0.0.1:6379> set hello world
OK
127.0.0.1:6379> get hello
"world"
127.0.0.1:6379> 
```

## Redis 典型应用场景



* 缓存系统

> ![image-20210125161456767](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125161456767.png)
>
> 常见的缓存系统的工作流程如上图
>
> 1. 用户向系统发出请求
> 2. 系统查询缓存是否有数据
> 3. 缓存是否命中
>    * 3.1 缓存命中，直接返回结果
>    * 3.2 缓存未命中，请求真实数据库
> 4. 把数据库返回的结果，存储至Redis，以便下次快速访问
> 5. 把结果返回给用户

* 计数器

> 常见的微博的转发量，评论量等

* 消息队列系统

> ![image-20210125161939651](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125161939651.png)

* 排行榜

> ![image-20210125162001500](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125162001500.png)

* 社交网络

> ![image-20210125162019445](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125162019445.png)

* 实时系统

## Redis 常用配置

1. `daemonzie`:  是否以守护进程启动
2. `port`： 端口号
3. `logfile`： Redis系统日志
4. `dir`： Redis 工作目录

5. `requirepass`:  密码
6. `bind`:  绑定地址

