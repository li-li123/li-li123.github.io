## Jedis

jedis是基于Java的Redis客户端

  ## Maven 依赖

```xml
<dependency>
  <groupId>redis.clients</groupId>
  <artifactId>jedis</artifactId>
  <version>3.5.1</version>
</dependency>
```

## Jedis直连

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210127204957503.png" alt="image-20210127204957503" style="zoom: 67%;" />

```java
Jedis jedis = new Jedis("127.0.0.1", 6379); // 连接
jedis.auth("123456"); // 密码
jedis.select(0); // 选择数据库
```

## Jedis 连接池

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210127205041043.png" alt="image-20210127205041043" style="zoom:67%;" />

```java
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(brokerConfig.getRedisMaxActive());//最大连接数
config.setMaxIdle(brokerConfig.getRedisMaxIdle());//最大空闲连接数
config.setMaxWaitMillis(brokerConfig.getRedisMaxWait());//获取可用连接的最大等待时间
JedisPool jedisPool = new JedisPool(config, "127.0.0.1", 6379, 100000L);
Jedis jedis = jedisPool.getResource();
```

**使用连接池访问Redis时,一定要在用完之后close.否则连接池的所有连接都会耗尽,阻塞程序运行**

## 方案对比

|        | 优点                                                         | 缺点                                                         |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 直连   | 简单方便<br/>适用于少量长期连接的场景                        | 存在每次新建/关闭TCP开销<br/>资源无法控制,存在连接泄露的可能<br/>Jedis对象线程不安全 |
| 连接池 | Jedis预先生成,降低开销使用<br/>连接池的形式保护可控制资源的使用 | 相对于直连,使用相对麻烦,尤其在资源的管理上需要很多参数来保证,一旦规划不合理也会出现问题 |
|        |                                                              |                                                              |

