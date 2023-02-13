## 集群伸缩

### 伸缩原理

**下图是集群伸缩的原理, `Redis`槽数固定, 节点上线下线, 槽再分配**

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203121300503.png" alt="image-20210203121300503" style="zoom: 50%;" /></center>



节点加入, 分配槽给该节点

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203121337623.png" alt="image-20210203121337623" style="zoom:50%;" /></center>

### 集群扩容

集群扩容顺序如下

1. 启动新节点

> 新节点以集群模式启动, 配置需要和其他节点统一. 启动后的节点是**孤儿节点**
>
> <center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203121912790.png" alt="image-20210203121912790" style="zoom:50%;" /></center>

2.  加入集群(进行`meet`操作)

> 例如: `cluster meet 127.0.0.1 8000`

3. 潜移槽和数据

------

Redis 官方提供了加入集群的命令

`redis-cli --cluster add-node <新节点IP>:<新节点端口> <集群任意节点IP>:<端口> -a <密码>`

重新分配槽

`redis-cli --cluster reshard  ip:port`



### 集群缩容

集群的缩容步骤如下

1. 下线迁移槽

> 使用`redis-cli --cluster reshard <集群地址>`进行迁移

2. 忘记节点

> 使用 ` redis-cli --cluster del-node <集群地址> <下线节点的nodeid>`: 如果节点持有槽, 将不能完成下线操作

3. 关闭节点

> `kill -9 <redisPID>`

## 客户端路由

### moved 重定向

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203133032425.png" alt="image-20210203133032425" style="zoom: 50%;" /></center>



Move重定向发送流程如下

1. 客户端向集群任意节点发送命令
2. 节点计算该key的CRC16的值并对16384取余
3. 如果节点持有该槽,则返回命令的执行结果,  否则返回Move重定向
4. 客户端向持有该槽的节点发送命令, 获取执行结果



### ask重定向

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203133356025.png" alt="image-20210203133356025" style="zoom: 50%;" /></center>

 当槽迁移时,会发生ASK重定向, 流程如下

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203133533964.png" alt="image-20210203133533964" style="zoom:50%;" /></center>

1. 客户端向节点发送命令
2. 节点回复ASK重定向, 该槽已经被迁移
3. 客户端向新节点发送ASK命令, 询问节点是否持有该槽
4. 节点回复持有该槽, 客户端向该节点发送指令



**MOVE和ASK的区别**

* 两种都是客户单重定向
* moved: 槽已经确定迁移
* ask: 槽还在迁移中

### smart客户端

#### smart客户端原理

1. 从集群中选一个可运行节点,使用`cluster slots`初始化槽和节点映射
2. 将`cluster slots`的结果映射到本地, 为每个节点创建JedisPool
3. 准备执行命名

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203134319415.png" alt="image-20210203134319415" style="zoom:67%;" />

##### smart客户端使用方法

-------

`JedisCluster`基本使用



```java
public class TestJedis {
    private static JedisCluster pool = null;

    //可用连接实例的最大数目，默认为8；
    //如果赋值为-1，则表示不限制，如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
    private static final Integer MAX_TOTAL = 1024;
    //控制一个pool最多有多少个状态为idle(空闲)的jedis实例，默认值是8
    private static final Integer MAX_IDLE = 200;
    //等待可用连接的最大时间，单位是毫秒，默认值为-1，表示永不超时。
    //如果超过等待时间，则直接抛出JedisConnectionException
    private static final Integer MAX_WAIT_MILLIS = 10000;
    //客户端超时时间配置
    private static final Integer TIMEOUT = 10000;
    //在borrow(用)一个jedis实例时，是否提前进行validate(验证)操作；
    //如果为true，则得到的jedis实例均是可用的
    private static final Boolean TEST_ON_BORROW = true;
    //在空闲时检查有效性, 默认false
    private static final Boolean TEST_WHILE_IDLE = true;
    //是否进行有效性检查
    private static final Boolean TEST_ON_RETURN = true;

    public static void main(String[] args) {

        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxTotal(MAX_TOTAL);
        config.setMaxIdle(MAX_IDLE);
        config.setMaxWaitMillis(MAX_WAIT_MILLIS);
        config.setTestOnBorrow(TEST_ON_BORROW);
        config.setTestWhileIdle(TEST_WHILE_IDLE);
        config.setTestOnReturn(TEST_ON_RETURN);

        Set<HostAndPort> nodeList = new HashSet<>();
        nodeList.add(new HostAndPort("192.168.0.64",6379));
        nodeList.add(new HostAndPort("192.168.0.64",6380));
        nodeList.add(new HostAndPort("192.168.0.64",6381));
        nodeList.add(new HostAndPort("192.168.0.65",6379));
        nodeList.add(new HostAndPort("192.168.0.65",6380));
        nodeList.add(new HostAndPort("192.168.0.65",6381));


        pool = new JedisCluster(nodeList, TIMEOUT, config);
        

    }
}

```

**注意`Redis Cluster`**必须使用单例, 因为里面内置了所有节点的连接池, 如果多实例的话, 会有过多的连接进入Redis集群

-------

多节点命令实现

```java
// 获取全部节点
Map<String, JedisPool> clusterNodes = pool.getClusterNodes();
clusterNodes.forEach((k, v)->{
    Jedis resource = v.getResource();
    // 遍历节点Key
    Set<String> keys = resource.keys("*");
    keys.forEach(System.out::println);
});
```

------

批量命令实现

因为`Redis Cluster`中`mget`和`mset`操作必须再一个槽上, 如何解决这个问题 

1. 串行IO

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203141140850.png" alt="image-20210203141140850" style="zoom:50%;" />

客户端分拣`Key`然后在执行命令

2. 并行IO

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203141220789.png" alt="image-20210203141220789" style="zoom:67%;" />

在串行IO的基础上,使用线程执行命令



## 故障转移

> 具体细节参考[redisCluster之主观下线与客观下线](https://blog.csdn.net/qq_32182461/article/details/82556295)

### 故障发现

故障发现通过`ping/pong`消息实现故障发现: 不需要`sentinel`, 故障发现同`Sentinel`一样也分为主观下线和客观下线.

主观下线流程

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203141621495.png" alt="image-20210203141621495" style="zoom: 67%;" />

客观下线: 当半数以上持有槽的主节点都标记某节点主观下线时, 就认为该节点已经实际宕机了,即客观下线, 流程如下.



<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203141842437.png" alt="image-20210203141842437" style="zoom:67%;" />

尝试客观下线流程如下: 

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203142004296.png" alt="image-20210203142004296" style="zoom:50%;" />

尝试客观下线的作用如下:

1. 通知集群内所有节点标记故障节点为客观下线
2. 通知故障节点的从节点触发故障转移流程

### 故障恢复

故障恢复是发生在故障发现之后,为了集群的高可用从节点会选举出一个新的主节点, 故障恢复流程有以下几个步骤

1. 资格检查

> 每个从节点检查与故障主节点的断线时间, 超过`cluster-node-timeout * cluster-slave-validity-factor`取消资格
>
> `cluster-slave-validity-fatory`默认值是10

2. 准备选举时间

> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203143150765.png" alt="image-20210203143150765" style="zoom:50%;" />
>
> 偏离量最大的节点的延迟选举时间越短, 该设计是为了与主节点数据一致性最高的节点成为新的master

3. 选举投票

> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203143317462.png" alt="image-20210203143317462" style="zoom: 50%;" />

4. 替换主节点

> 1. 当前从节点取消复制变为主节点(`slaveof no one`)
> 2. 执行`clusterDelSlot`撤销故障主节点复制的槽, 并执行`clusterAddSlot`把这些槽分配给自己
> 3. 向集群广播自己`pong`消息, 表明已经替换了故障从节点

## 开发运维常见问题

### 集群完整性

集群完整性的配置文件参数为`cluster-require-full-voverage`, 默认为yes.   这样设计是为了集群中16384个槽全部可用: 保证集群完整性, 当节点故障或者正在故障转移时操作Redis会报错: **CLUSTERDOWN The cluster is down**

这样的场景大多数业务无法容忍, `cluster-require-full-coverage`建议设置为no

### 带宽消耗

`Redis Cluster`采用P2P的协议(PING/PONG),当节点较多时对带宽消耗较多. 官方建议最多10000个节点,

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203145051096.png" alt="image-20210203145051096" style="zoom: 50%;" />

消息带宽主要有3个方面

1. 消息发送频率: 节点发现与其他节点最后通信时间超过`cluster-node-timeout/2`时会直接发送ping消息
2. 消息数据量: slots槽数组(2K空间)和整个集群1/10的状态数据(10个节点状态约1KB)
3. 节点部署的机器规模: 集群分布的机器越多且每台机器划分的节点越均匀, 则集群内整体的可用带宽越高

### Pub/Sub 广播

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210203145645122.png" alt="image-20210203145645122" style="zoom:50%;" />

publish在集群每个节点广播: 加重带宽.

解决方法: 单独走一套`Redis Sentinel`

### 集群倾斜

#### 数据倾斜: 内存不均

造成该问题主要有以下几个方面

1. 节点和槽分配不均

> `redis-cli cluster slots` 和`redis-cli --cluster reshard`

2. 不同槽对应键值数量差异较大

> * `CRC16`正常情况下比较均匀
> * 可能存在hash_tag
> * `cluster conutkeysinslot {slot}` 获取槽对应键值数

3. 包含bigkey

> 例如大字符串、几百万的元素`hash`、`set`等
>
> `redis-cli --bigkeys`

4. 内存配置不一致

> `hash-max-ziplist-value`, `set-max-intset-entries`等配置项不一致

------

#### 请求倾斜: 热点数据

* 热点key: 重要的key或者bigkey

优化: 

* 避免bigkey
* 热键不要用hash_tag
* 当一致性不高时,可以用本地缓存+MQ







### 读写分离

集群模式的从节点不接受任何读写请求, 当对从节点进行读取时, 从节点会重定向到复制该槽的主节点. 但是**readonly命令可以进行读请求(连接级别的命令)**

```java
// 获取全部节点
Map<String, JedisPool> clusterNodes = pool.getClusterNodes();
clusterNodes.forEach((k, v)->{

    Jedis resource = v.getResource();
    /* */
    resource.readonly();
    /* */

});
```

例如上述代码,切换为读模式

读写分离更加复杂, 成本会更高

### 数据迁移

在前迁移工具`redis-migrate-tool`

### 集群VS单机

集群限制

* key批量操作支持有限: 例如`mget、mset`必须在一个slot内
* key事务和Lua支持有限： 操作key必须在一个节点
* key时数据分区的最小粒度： 不支持bigkey分区
* 不支持多个数据库： 集群模式下只有一个`db 0`
* 复制只支持一层, 不支持树形结构



