## 为什么需要集群

* 单节点的`Redis`可以达到10万/每秒, 但是某些业务需要100万/每秒.
* 单个Redis能支持16~256G, 但是某些业务需要500G等更高的内存

虽然可以通过升级硬件,但是硬件使用会有瓶颈, 所以需要水平扩展

> <center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202133334961.png" alt="image-20210202133334961" style="zoom: 33%;" /></center>

## 数据分布

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202133531919.png" alt="image-20210202133531919" style="zoom:67%;" />

如上图一般分布式数据库, 会对数据根据一定的规则把数据进行分区.常见的分区方式有两种: 顺序分区和哈希分区.

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202133741950.png" alt="image-20210202133741950" style="zoom:50%;" />

数据分布的对比

| 分布方式 | 特点                                                         | 典型产品                                                |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| 哈希分布 | 数据分散度高<br>键值分布与业务无关<br>无法顺序访问<br>支持批量操作 | 一致性哈希`Memcache`<br>`Redis Cluster`<br>其他缓存产品 |
| 顺序分布 | 数据分散度易倾斜<br>键值业务相关<br>可顺序访问<br>支持批量操作 | `BigTable`<br>`HBase`                                   |
|          |                                                              |                                                         |

这里介绍一下常用的哈希分布的方式,因为Redis就是基于哈希分布的

* 节点取余分区

> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202134455579.png" alt="image-20210202134455579" style="zoom:50%;" />
>
> 这个方式虽然可以把数据平局分布到每个节点,但是当集群增删节点时,数据需要进行迁移, 可能良妃过多的性能.建议一般进行多倍扩容.
>
> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202134652527.png" alt="image-20210202134652527" style="zoom:50%;" />
>
> 节点取余总结
>
> * 客户端分片: 哈希 + 取余
> * 节点伸缩: 数据节点关系变化, 导致数据迁移
> * 迁移数量和添加节点数量有关: 建议翻倍扩容

* 一致性哈希分区

> 一致性哈希解决了新增节点数据迁移量较大的问题,详细内容参考-[图解一致性哈希算法](https://segmentfault.com/a/1190000021199728)

* 虚拟槽分区

> * 预设虚拟槽: 每个槽映射一个数据集,一般比节点数大.
> * 良好的哈希函数: 例如CRC16
> * 服务端管理节点、槽、数据: 例如`Redis Cluster`
>
> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202141349612.png" alt="image-20210202141349612" style="zoom: 50%;" />
>
> 通过`CRC16`计算key应该属于哪一个槽,然后把结果发送给`Redis Cluster`中任意一个节点, 如果节点发现自己不负责这个槽, 节点将通知客户端管理这个槽的节点, 如果刚好自己管理这个槽,节点将处理这个数据

## 搭建集群

### 架构介绍

首先回顾一下单机版的Redis架构

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202141830293.png" alt="image-20210202141830293" style="zoom: 50%;" /></center>

`Redis Cluster`的架构如下: 集群中有多个节点, 彼此之间相互通信, 因而了解对方管理的槽, 客户端可以连接任何一个节点,就可以获得数据.

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202141928010.png" alt="image-20210202141928010" style="zoom: 50%;" /></center>

搭建`Redis Cluster`需要以下几个步骤

1. 搭建多个节点

> 配置文件中启用`cluster-enabled:yes`

2. 进行`meet`操作,连入集群

> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/meet-redis-cluster.png" alt="meet-redis-cluster" style="zoom:50%;" />

3. 指派槽位, 开始正常读写

> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202142850095.png" alt="image-20210202142850095" style="zoom:50%;" />
>
> `Redis Cluster`中的槽位有**16384**个槽, 每个节点复制一定的范围的槽

4. 复制数据, 保证高可用

> `Redis Cluster`本身就是支持数据分片和高可用模式

### 两种安装方式

`Redis Cluster`共有两种安装方式: 原生命令安装和官方工具安装.

----------

原生命令安装共有以下步骤:

1. 配置节点开启

> 1. 编写配置文件
>
> ```text
> port ${port}
> daemonize yes
> dir /root/redis/
> dbfilename dump-${port}.rdb
> logfile ${port}.log
> cluster-enabled yes # 开启集群模式
> cluster-config-file nodes-${port}.conf # 集群配置文件
> cluster-enables yes
> cluster-node-timeout 15000 # 集群主观下线超时时间
> cluster-config-file nodes.conf # 集群配置文件
> cluster-require-full-coverage no # 必须集群全部节点可用,才能够提供服务, 这里是测试环境开启, 生产环境应该关闭
> ```
>
> ​    需要开启多个节点, 根据上述模板填入不同的端口
>
> 2. 开启多个节点 `redis-sever redis-7000.conf`

2. meet

> 节点进行`meet`操作  例如: `redis-cli -h 127.0.0.1 -p 6379 cluster meet 127.0.0.1 6380`,(**一个节点 meet所有其他的节点即可**)

3. 指派槽

> **只有分配了所有槽, Redis 集群才会正常运行**
>
> 需要分配槽的节点执行命令:`cluster addslots solt [slot....]`
>
> 例如: `redis-cli -h 127.0.0.1 -p 6379 cluster addslots {0...5461}`
>
> `redis-cli -h 127.0.0.1 -p 6380 cluster addslots {5462...10922}`
>
> `redis-cli -h 127.0.0.1 -p 6381 cluster addslots {10923...16383}`

3. 配置主从分配

> 设置`cluster replicate node-id` (node-id是集群分配的ID, 跟run-id不同)
>
> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210202152811402.png" alt="image-20210202152811402"  />
>
> 例如: `redis-cli -h 127.0.0.1 -p 7003 cluster replicate ${node-id-7000}`

-------

高版本(Redis 5.0)使用`redis-cli`

`redis-cli --cluster create 192.168.0.64:6379 192.168.0.64:6380 192.168.64:6381 192.168.0.65:6379 192.168.0.65:6380  192.168.0.65:6381 --cluster-replicas 1`



## 集群相关命令

----

redis-cli 内命令

* `cluster info`: 查看集群信息
* `cluster nodes`: 查看集群节点
* `cluster slots`: 查看已经分配的槽
* `cluster meet`: 集群加入节点 
* `cluster replicate`: 集群配置主从关系
* `cluster delslots`: 删除槽
* `cluster conutkeysinslot {slot}`:  获取槽对应键值数

----

shell 命令

* `for i in {0..5000};do redis-cli -p 7000 cluster addslots $i;done`: 批量复制槽位
* `redis-cli -c -p`: 使用集群模式的`Redis-cli`
* `redis-cli --cluster create <ip:port>`:  创建集群
* `redis-cli --cluster add-node <新节点IP>:<新节点端口> <集群任意节点IP>:<端口> -a <密码>`: 加入新节点
* `redis-cli --cluster reshard  ip:port` : 重新分配槽
* `redis-cli --cluster del-node <集群地址> <下线节点的nodeid>`: 下线节点







