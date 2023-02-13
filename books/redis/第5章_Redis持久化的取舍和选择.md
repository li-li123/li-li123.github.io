## 持久化的作用 

### 什么是持久化

`Redis`所有数据保存在内存中,对数据的更新将异步地保存到磁盘上

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129191035945.png" alt="image-20210129191035945" style="zoom: 33%;" />

### 持久化的实现方式

持久化共有两种方式

快照

> * MySQL Dump 
>
> * Redis RDB

2. 写日志

> * MySQL Binlog
> * Hbase HLog
> * Redis AOF

## RDB

### RDB 介绍

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129191321761.png" alt="image-20210129191321761" style="zoom:50%;" />

Redis会把当前数据库中所有的数据复制到RDB文件中,当重启时从RDB文件加载之前的数据

### RDB 触发方式

Redis 触发RDB快照以下三种机制

* `save`(同步)

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129191953078.png" alt="image-20210129191953078" style="zoom: 50%;" />

客户端向Redis服务器发送`save`命令即可完成快照的保存,但这个命令会阻塞其他命令,直至快照保存完成

文件策略是: 如果存在老的RDB文件,新的文件会替换老的文件,**复杂度O(N)**

------

* `bgsave`(异步)

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129192223603.png" alt="image-20210129192223603" style="zoom:50%;" />

客户端向服务端发送`bgsave`命令即可,文件策略和时间复杂度与`save`相同



`save` 和`bgsave`的区别

| 命令   | save             | bgsave                     |
| ------ | ---------------- | -------------------------- |
| IO类型 | 同步             | 异步                       |
| 阻塞   | 是               | 是(阻塞发生在进程fork阶段) |
| 复杂度 | O(N)             | O(N)                       |
| 优点   | 不会消耗额外内存 | 不阻塞客户端命令           |
| 缺点   | 阻塞客户端命令   | 需要fork,消耗内存          |

-----

* 自动

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129193531199.png" alt="image-20210129193531199" style="zoom:67%;" />

`Redis`提供根据改变次数自动触发备份的机制,默认参数是

| 配置 | seconds | changes |
| ---- | ------- | ------- |
| save | 900     | 1       |
| save | 300     | 10      |
| save | 60      | 10000   |

以上参数分别是,如果1分钟发生10000次、5分钟发生10次更改或15分钟内发生1次更改，Redis将触发`bgsave`命令

### 相关配置

* `dbfilename 文件名`: RDB文件名
* `save 秒数 变更次数`: RDB文件触发机制
* `dir 路径`: RDB 文件存储位置
* `stop-writes-on-bgsave-error yes|no`: 当`bgsave`发生错误是,停止写入
* `rdbcompression yes`|no: RDB是否采用压缩格式
* `rdbchecksum yes|no`: 是否对RDB文件进行校验和检验

### 触发机制

除了手动或者自动备份操作,还有以下几种方式会触发RDB文件生成

* 全量复制的时候
* `debug reload`
* shutdown



## AOF

### RDB的问题

RDB主要有两个问题1. 耗时耗性能 2. 不可能,容易丢失数据

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129200410519.png" alt="image-20210129200410519" style="zoom: 67%;" />

### AOF 介绍

Redis 将所有对数据库进行过写入的命令（及其参数）记录到 AOF 文件， 以此达到记录数据库状态的目的， 为了方便起见， 我们称呼这种记录过程为同步。

> 详细内容, 请参考链接: [Reis设计与实现-AOF](https://redisbook.readthedocs.io/en/latest/internal/aof.html)

### AOF三种策略

1. `always`

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129201333341.png" alt="image-20210129201333341" style="zoom:50%;" />

Redis在执行写命令的时候,会将我们的一个写命令先写入一个文件缓存中,然后根据设定的策略同步到文件中. 而`alayws`策略是每次写命令,都会立刻同步到磁盘,这样数据不会丢失,但是会很影响性能

-----

2. `everysec`

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129201420322.png" style="zoom:50%;" />

每秒同步数据到磁盘中.

----

3. `no`

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129201515155.png" alt="image-20210129201515155" style="zoom:50%;" />

`Redis`不控制文件同步,转而由系统进行控制

三种策略的比较

| 命令 | always                               | everysec                | no     |
| ---- | ------------------------------------ | ----------------------- | ------ |
| 优点 | 不丢失数据                           | 每秒一次`fync`丢1秒数据 | 不用管 |
| 缺点 | IO开销比较大,一般的sata盘只有几百TPS | 丢1秒数据               | 不可控 |
|      |                                      |                         |        |

### AOF 重写

AOF 文件通过同步 Redis 服务器所执行的命令， 从而实现了数据库状态的记录， 但是， 这种同步方式会造成一个问题： 随着运行时间的流逝， AOF 文件会变得越来越大。举个例子， 如果服务器执行了以下命令：

```shell
RPUSH list 1 2 3 4      // [1, 2, 3, 4]

RPOP list               // [1, 2, 3]

LPOP list               // [2, 3]

LPUSH list 1            // [1, 2, 3]
```

那么光是记录 `list` 键的状态， AOF 文件就需要保存四条命令。另一方面， 有些被频繁操作的键， 对它们所调用的命令可能有成百上千、甚至上万条， 如果这样被频繁操作的键有很多的话， AOF 文件的体积就会急速膨胀， 对 Redis 、甚至整个系统的造成影响。

为了解决以上的问题， Redis 需要对 AOF 文件进行重写（rewrite）： **创建一个新的 AOF 文件来代替原有的 AOF 文件， 新 AOF 文件和原有 AOF 文件保存的数据库状态完全一样， 但新 AOF 文件的体积小于等于原有 AOF 文件的体积**。

AOF重写可以减少磁盘占用量、加快恢复速度.

### AOF重写方式

AOF重写有触发两种方式

1. 客户端执行`bgrewriteaof` 命令

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129202557326.png" alt="image-20210129202557326" style="zoom:50%;" />

**注意: 这里的AOF重写是指根据当前的内存数据,重新生成AOF文件,跟优化AOF文件大小不同**

-----

2. AOF重写配置

| 配置名                        | 含义                           |
| ----------------------------- | ------------------------------ |
| `auto-aof-rewrite-min-size`   | AOF文件重写需要的尺寸          |
| `auto-aof-rewrite-percentage` | AOF文件增长率,(下次重写的大小) |
|                               |                                |

统计项

| 统计名             | 含义                              |
| ------------------ | --------------------------------- |
| `aof_current_size` | AOF当前尺寸(单位: 字节)           |
| `aof_base_size`    | AOF上次启动和重写的尺寸(单位字节) |
|                    |                                   |

`Redis`需要同时满足以下两个条件才会自动触发AOF重写

1. `aof_current_size > auto-aof-rewrite-min-size`
2. `(aof_current_size - aof_base_size)/aof_base_size > auto-aof-rewrite-percentage`

### AOF 重写流程

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129203434224.png" alt="image-20210129203434224" style="zoom:67%;" />

### AOF 配置

* `appendonly yes|no`: 是否启动AOF
* `appendfilename 文件名`: AOF文件名
* `appendfysnc everysec|always|no`: 同步策略
* `dir 路径`: AOF文件存储文件夹
* `no-appendfsync-on-rewrite yes|no`:   当AOF重写时,是否允许进行AOF操作
* `auto-aof-rewrite-percentange 100`: AOF 文件增长率
* `auto-aof-rewrite-min-size`: AOF文件重写大小



## RDB 和AOF的选择

### RDB 和AOF比较

| 命令       | RDB    | AOF          |
| ---------- | ------ | ------------ |
| 启动优先级 | 低     | 高           |
| 体积       | 小     | 大           |
| 恢复速度   | 快     | 慢           |
| 数据安全性 | 丢数据 | 根据策略决定 |
| 轻重       | 重     | 轻           |
|            |        |              |



### RDB最佳策略

* 建议RDB"关掉"
* RDB需要继续集中管理
* 需要主节点关闭,从节点关闭

### AOF最佳策略

* 大部分情况下AOF需要开,当Redis里面的数据只是缓存,可以关掉
* AOF重写集中管理
* AOF的策略建议为: `eversec`

### 最佳策略

* 内存需要小分片
* 适当监控硬盘、内存、复载、网络
* 部署Redis机器需要足够的内存

