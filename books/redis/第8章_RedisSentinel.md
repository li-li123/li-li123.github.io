## 主从复制高可用?

主从复制的架构存2个问题

1. 需要手动故障转移.
2. 写能力和存储能力收到限制

## 架构说明

`Redis Sentinel`依然是基于主从模式, 存在一个`sentinel`进程监控master的状态,并在`master`掉线后,自动选举新的master,并通知客户端.

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-2021020141347317.png" alt="image-2021020141347317" style="zoom:50%;" />

故障转移机制如下图

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/Redis 哨兵.gif" alt="Redis 哨兵" style="zoom: 67%;" />



同时`Redis Sentinel`支持监控多个集群

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210201142355426.png" alt="image-20210201142355426" style="zoom:50%;" />



## 安装配置

1. 配置开启主节点

> 具体配置细节参考 第7 章

2. 配置开启`sentinel`监控节点(sentinel是特殊的redis)

> 1. 首先编写 `redis-sentinel.conf`配置文件
>
> ```text
> port 26379 # 端口号
> dir '/opt/soft/redis/data/' # 数据目录
> logfile 26379.log # 日志文件
> sentinel monitor mymaster 127.0.0.1 6379 2 # 监控主节点IP 端口, 2个sentinel认为主节点失败,才会认为该节点失败
> sentinel down-after-milliseconds mymaster 30000 
> sentinel parallel-syncs mymaster 1
> sentinel failover-timeout mymaster 180000
> ```
>
> 2. 启动
>
> ```shell
> redis-sentinel ./redis-sentinel.conf
> ```
>
> 3. 查看信息
>
> ```shell
> redis-cli -p 26379 # 连入redis-sentinel
> > info # 输入info查看状态
> ```
>
> 4. 配置多个`redis-sentinel`

## 客户端连接

客户端实现高可用原理

1. 遍历`Sentinel`节点集合,获取一个可用的sentinel节点

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210201154437787.png" alt="image-20210201154437787" style="zoom: 50%;" />

2. 通过`sentinel`获取实际master节点

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210201154643741.png" alt="image-20210201154643741" style="zoom: 50%;" />

3.  验证master信息

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210201154732523.png" alt="image-20210201154732523" style="zoom: 50%;" />

4. 节点变化通知,`sentinel`会产生一个频道,客户端订阅该频道,就是实时得知实际的master地址变化

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210201154931716.png" alt="image-20210201154931716" style="zoom:50%;" />



客户端接入流程

1. 配置sentinel地址集合
2. 配置masterName

### Jedis 连入代码

```java
public class TestJedis {
    private static JedisSentinelPool pool = null;

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
        
        HashSet<String> sentinelIps = new HashSet<>();
        sentinelIps.add(new HostAndPort("127.0.0.1",26379).toString());
        sentinelIps.add(new HostAndPort("127.0.0.1",26380).toString());
        sentinelIps.add(new HostAndPort("127.0.0.1",26381).toString());
        String password = "123456";

        pool = new JedisSentinelPool("mymaster", sentinelIps, config, TIMEOUT, password);


        try(Jedis redis = pool.getResource()){
            Set<String> keys = redis.keys("*");
            keys.forEach(System.out::println);
        }

    }
}
```

> 注意: **虽然Redis sentinel 可以配置密码,但是Jedis连入Sentinel是只支持master密码**, 也就是说上述代码中的密码指的是master的密码

## 实现原理

故障转移流程如下

1. 定时任务不断更新节点状态
2. 发现master异常, 选举Leader(主观下线,和领导者选举)
3. Leader 进行故障转移和恢复(客观下线和故障转移)

### 三个定时任务

`Redis Sentinel`内部有3个定时任务来完成,故障的发现和自动转移的.

1. 每10秒每个sentinel对master和slave执行`info`
   * 可以通过该命令发现slave命令
   * 确认主从关系

> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210201163102551.png" alt="image-20210201163102551" style="zoom: 67%;" />

2. 每2秒每个sentinel通过master节点的`channel`交换信息(pub/sub)
   * 实际上是通过`__sentinel__:hello`频道交换信息的
   * 交互的信息包含: 对节点的看法, 和节点自身的信息

> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210201163359419.png" alt="image-20210201163359419" style="zoom:67%;" />

3. 每1秒每个sentinel对其他sentinel和redis执行`ping`

> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210201163601349.png" alt="image-20210201163601349" style="zoom:67%;" />

### 主观下线和客观下线

`sentinel`配置文件中有以下机项

* `sentinel monitor <masterName> <ip> <port> <quorum>`

>  例如`sentinel monitor master 127.0.0.1 6379 2`, 最后一个是投票数,即大于等于多少个票数时,客观下线当前master

* `sentinel down-after-milliseconds <masterName> <timeout>`>

> 例如: `sentinel down-after-milliseconds mymaster 30000`, 意思是: 超过多少**微秒**没有得到相应的话, `sentinel`做下线状态处理(主观下线)

主观下线: 每个sentinel节点对Redis节点失败的"偏见",

客观下线:所有sentinel节点对Redis节点失败"达成共识",(超过上述配置文件中的投票数) 

> <center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/86883a42gy1ff70pfr5jsj206o06odg0.jpg" alt="86883a42gy1ff70pfr5jsj206o06odg0"  /></center>

当某个`sentinel`认为master宕机后, 他会向其他`sentinel`发送`sentinel is-master-down-by-addr`命令,来计算当前的投票数

### 领导者选举

选举的原因:

​	因为只有一个`sentinel`节点就可以完成故障转移,所以多个`sentinel`需要选择一个节点当作领导者,执行故障转移操作.. 

选举的流程:

​	通过`sentinel is-master-down-by-addr`命令都希望成为领导者,

1. 每个做主观下线的`sentinel`节点向其他`sentinel`节点发送命令,要求将他设置为领导之
2. 收到命令的`sentinel`节点如果没有同意通过其他`sentinel`节点发送的命令,那么将同意该请求, 否则拒绝

> 保证总票数不变

3. 如果该`sentinel`节点发现自己的票数已经超过`sentinel`集合半数且超过`quorum`,那么它将成为领导者
4. 如果此过程有多个`sentinel`节点成为了领导者,那么将等待一段时间重新进行选举

> 该选举流程是一个`Raft`算法,更多详细信息参考[Raft 算法动画演示中文讲解](https://www.bilibili.com/video/BV1GV411U7tv)

### 故障转移

故障转移的顺序为:

1. 从slave节点中选一个"合适的"节点作为新的master节点

> 什么是合适的slave节点:
>
> 1. 选择`slave-priority`(slave优先级)最高的slave节点,如果存在则返回,不存在则继续
> 2. 选择复制偏移量最大的slave节点(复制最完整),如果存在则返回,不存在则继续
> 3. 选择runid最小的节点

1. 对上面的slave节点执行`slaveof no one`命令,让其成为master节点
2.  对剩余的slave节点发送命令, 让他们成为新的master节点的slave节点,复制规则和`parellel-syncs`参数相关

>  `parellel-syncs`: 表示同时发送`RDB`文件的个数

4. 更新对原来的master节点配置为`slave`, 并保持对其关注, 当其恢复后命名它去复制新的master节点



## 高可用读写分离

参考`JedisPool`的`Sentilnel`实现细节, 我们需要自定义实现一个客户端去监听三个消息:

1. `+switch-master`: 切换主节点(从节点晋升主节点)
2. `+cover-to-slave`: 切换从节点(原主节点降为从节点)
3. `+sdown`: 主观下线

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210201172731246.png" alt="image-20210201172731246" style="zoom:50%;" />

然后客户端去连接当前可用的`slave`节点,就可以做到读写分离