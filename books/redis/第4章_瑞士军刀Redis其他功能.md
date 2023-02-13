## 慢查询

### 生命周期

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210127210056406.png" alt="image-20210127210056406" style="zoom:67%;" />

* 慢查询只发生在第三阶段,其他过程不算.
* 客户端超时不一定慢查询,但慢查询时客户端超时的一个可能因素

### 两个配置

Redis关于慢查询有两个配置文件

1. `slowlog-max-len`

慢查询是一个先进先出的队列,  当命令执行时间过长时,Redis会把命令放到一个先进先出的队列中. 队列是一个固定长度,保存在内存中, 重启后会丢失.

2. `slowlog-log-slower-than`: 慢查询阈值(单位: 微秒)

*  如果想把所有的命令都计入慢查询,可以设置`slow-log-slower-than=0`
* 不记录任何命令`slowlog-log-slower-than<0`

-------

配置方法:

1. 默认值

* `config get slowlog-max-len=128`
* `config get slowlog-log-slower-than=10000`

2. 修改配置文件重启

3. 动态配置 : `config set slowlog-max-len 1000 `, `config set slowlog-log-slower-than 1000`

### 三个命令

1. `slowlog get [n]`: 获取慢查询队列, n为慢查询条数
2. `slowlog len`: 获取慢查询队列长度
3. `slowlog reset`: 清空慢查询队列

### 运维经验

1. `slowlog-max-len`不要设置过大,通常设置1000左右
2. `slowlog-log-slower-than`不要设置过小, 默认10ms,通常设置1ms
3. 理解命令的生命周期
4. 定期持久化慢查询

 

## pipeline

### 流水线介绍

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210127212106917.png" alt="image-20210127212106917" style="zoom: 50%;" />

Redis的命令执行时间非常短,当需要执行多次命令时,大部分时间都消耗在网络传输上.这样很耗费时间与性能.

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210127212307697.png" alt="image-20210127212307697" style="zoom:50%;" />

流水线功能可以把不同的命令打包成一个命令发送给服务器,这样大大节省了传输时间

| 命令   | N个命令操作       | 1次pipeline(n个命令) |
| ------ | ----------------- | -------------------- |
| 时间   | n个网络 + n次命令 | 1次网络 + 那次命令   |
| 数据量 | 1条命令           | n条命令              |
|        |                   |                      |

> Redis 的命令时间是微秒级别的
>
> pipeline每次条数要控制(网络)



### 客户端实现

```java
Jedis jedis = new Jedis("127.0.0.1", 6379);
for (int i = 0; i < 100; i++) {
    Pipeline pipeline = jedis.pipelined();
    for (int j = 0; j < 100; j++) {
        pipeline.hset("hashkey:"+j, "field"+j, "value"+j);
    }
    pipeline.syncAndReturnAll();
}
jedis.close();
```



### 与原生操作的对比

* 原生的操作是原子

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210127213343854.png" alt="image-20210127213343854" style="zoom:50%;" />

* `pipeline`里面的操作时**非原子的**,Redis执行时有可能拆分操作

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210127213259503.png" alt="image-20210127213259503" style="zoom:50%;" />

### 使用建议



1. 注意每次`pipeline`携带数据量
2. `pipeline`每次只能作用在一个Redis节点上
3. 注意M操作与pipeline的区别

## 发布订阅

### 角色

Redis发布订阅一共有3个角色分别是发布者、订阅者、频道。

### 模型

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129170655297.png" alt="image-20210129170655297" style="zoom:67%;" />

生产者往指定的Channel发送消息，消费者订阅指定的`Channel`,这样消费者就能获得发布者发布的消息,**Redis无法做到消息的堆积**,新来的消费者无法得到之前的消息.



### API

* `publish channel message`: 往指定的`Channel`发送消息
* `subscribe channel`: 订阅一个或多个频道
*  `unsubscribe [channel]`: 取消订阅一个或多个频道
* `psubscribe [pattern...]`: 通配符订阅
* `punsubscribe [pattern...]`: 推定指定的模式
* `pubsub chanels`: 列出至少有一个订阅者的频道
* `pubsub numsub [channel...]`: 列出指定频道的订阅者数量



## Bitmap

### 位图介绍

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129174036410.png" alt="image-20210129174036410" style="zoom:50%;" />

Redis可以对字符串按照位进行操作, **当操作偏移量过大的bit位值,可能会很耗时**



### API

* `setkey key offset value`: 给位图指定索引设置值
* `getbit key offset`: 获取位图指定索引的值
* `bitcount key [start end]`: 获取位图指定范围(start 到end,单位为字节,如果不指定就是获取全部)位值为1的个数
* `bitop op destkey key [key...]`: 做多个Bitmap的and(交集),or(并集),not(非),xor(异或)操作并将结果保存在destkey中

> 例如
>
> ```shell
> bitop and unique:users-1-2 unique:user-1 unuque:user-2
> ```
>
> 将 `unique:user-1`和`unique:user-2`的并集存储到`unque:users-1-2`

* `bitpos key targetBit [start] [end] `: 计算位图指定范围(start到end就,单位为字节,如果不指定就是获取全部)第一个偏移量对应的值等于`targetBit`的位置



## HyperLogLog

### 介绍

> 完整介绍参考连接: [HyperLogLog 算法的原理讲解以及 Redis 是如何应用它的](https://juejin.cn/post/6844903785744056333)

### API

* `pfadd key element [element...]`: 向hyperloglog 中添加元素
* `pfcount key [key...]`: 计算hyperloglog的独立总数
* `pfmerge destkey sourcekey [sourcekey ...]`: 合并多个hyperloglog

> 使用示例:
>
> ```shell
> pfadd unique:ids "uuid-1"  "uuid-2" "uuid-3" "uuid-4"
> > 1
> pfcount unique:ids
> > 4
> pfadd unique:ids "uuid-1"  "uuid-2" "uuid-3" "uuid-90"
> > 1
> pfcount unique:ids
> > 5
> ```
>
> 

### 使用经验

* `hyperloglog`的错误率是 0.81%, 如果需要精确数值存储,不能使用`hyperloglog`

## GEO

### 介绍

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129184935811.png" alt="image-20210129184935811" style="zoom: 50%;" />

以下用这个5个城市的经纬度做演示

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210129185030957.png" alt="image-20210129185030957" style="zoom:50%;" />

### API

* `geoadd key longitude latitude member`: 增加位置信息

> `geoadd  cityies:locations 116.28 39.55 beijing`
>
> `geoadd  cityies:locations 117.12 39.08 tianjin`
>
> `geoadd  cityies:locations 114.29 38.02 shijianzhuang`
>
> `geoadd  cityies:locations 118.01 39.38 tangshan`
>
> `geoadd  cityies:locations 115.29 38.51 baoding`

* `geopos key member`: 获取地理位置信息

> `geopos cities:locations tianjin`

* `geodist key member1 member2 [unit]`: 获取两个地址位置的距离(unit: m(米), km(千米), mi(英里), ft(尺))
* `georadius key longitude latitude radiusm|km|ft|mi [witchcoord] [witchdist] [witchhash] [COUNT count] [asc|desc] [store key][stroedist key]`

> 指定经纬度,获取周围的成员
>
> * `withcoord`: 返回结果中包含经纬度
> * `withdist`: 返回结果中包含距离中心节点位置
> * `withhash`: 返回结果中包含geohash
> * `COUNT count`: 指定返回结果的数量
> * `asc|desc`: 返回结果按照距离中心节点的激励做升序或者降序
> * `store key`: 将返回结果的地理位置信息保存到指定建
> * `storedist key`: 将饭hi结果距离中心节点的距离保存到指定键

* `georadiusbymemmber key member radiusm|km|ft|mi [witchcoord] [witchdist] [witchhash] [COUNT count] [asc|desc] [store key][stroedist key]`

> 获取指定范围内的地理位置信息集合
>
> 参数同上

### 注意事项

* Redis 3.2+ 才能够使用
* type geoKey = zset
* 没有删除API

