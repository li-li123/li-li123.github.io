## 什么是主从复制

主从复制可以很好的避免单点故障.Redis提供一主多从或者一主一从的功能

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210130151401666.png" alt="image-20210130151401666" style="zoom:50%;" />

主从复制可以增加数据副本,读写分离的功能.Redis主从复制有以下三个特点:

1. 一个master 可以配置多个slave
2. 一个slave只能有一个master
3. 数据流向是单项的, master到slave



## 主从配置复制

主从复制共有两种配置方式

1. `slaveof <host> <port>`

例如

`slaveof 127.0.0.1 6379`

> 主节点配置密码的时候,从节点的配置文件中要配置master的密码`masterauth <master密码>`

取消复制

`slaveof no one`

> 之前同步的数据不会删除

-----

2. 配置文件

添加配置文件

* `slaveof ip port`:  同步主节点
* `slave-read-only`:  从节点不允许写

-----

查看主从配置状态

`info replication`



### Run-id 和偏移量

每个`Redis`启动时都会生成一个`run-id`,当从节点发现主节点的`run-id`改变时会触发全量复制.

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210130161308816.png" alt="image-20210130161308816" style="zoom: 67%;" />

偏移量表示Redis同时的偏移量, 部分复制就是根据偏移量进行部分数据的获取

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210130161606382.png" alt="image-20210130161606382" style="zoom:80%;" />





## 全量复制和部分复制

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210130162703175.png" alt="image-20210130162703175" style="zoom: 50%;" />

1. salve 向master发送同步命令 `psync <run-id> <offset>`
2. master 收到命令后, 返回当前master的`run-id`和偏移量
3. slave收到master的信息后,保存到本地,供下次同步时使用
4. master启动bgsave,生成RDB文件
5. master会把新的写入命令存储到,命令缓冲区,以便slave进行部分复制
6. master向slave发送RDB文件
7. master向salve发送新增的写命令
8. slave清空旧数据
9. slave加载master数据



全量复制到开销如下

1. bgsave时间
2. RDB文件传输时间
3. 从节点清空数据的时间
4. 从节点加载RDB的时间
5. 可能的AOF重写时间

-------

部分复制流程

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210130163305362.png" alt="image-20210130163305362" style="zoom:67%;" />

1. 当slave与master之间的连接中断时
2. master会将新增的key,存储到缓冲区中
3. 当slave重新连接至master时
4. slave 发送同步命令
5. master 发现 可以进行部分复制
6. master发送部分数据

----

## 主从复制的问题

主从复制不能自动进行故障转移,为了解决这一问题.Redis提供了哨兵模式,可以自动进行故障转移.

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210130164025168.png" alt="image-20210130164025168" style="zoom: 50%;" />

除了无法自动故障转移之外,主从复制模式还有以下几个问题

1. 读写分离

主从复制是为了提高系统的并发量,读写分离可能会遇到: 复制数据延迟,  读到过期的数据(Redis 3.2 已经解决这一问题), 从节点故障

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210130164322078.png" alt="image-20210130164322078" style="zoom:50%;" />

------

2. 配置不一致

* 例如`maxmemory`不一致: 丢失数据
* 例如数据结构优化参数(例如`hash-max-ziplist-entries`): 内存不一致

---

3. 全量复制太频繁

以下的时机全量复制

* 第一次全量复制无可避免

> 数据进行分片,单个节点不要存过大的数据

* 节点ID不匹配

> 主节点重启后(ID发生变化), 可以使用哨兵或者集群规避这一问题

* 复制积压缓冲区不足

> 无法完成部分复制, 提高`rel_backlog_size`

------

4. 复制风暴

主节点挂掉后, 所有从节点都要进行复制,所以被称为**复制风暴**