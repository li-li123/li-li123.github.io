## 通用命令

> [Redis 命令参考](http://redisdoc.com/)

* `keys`

> ```shell
> keys * # 遍历所有key
> key he* # 遍历he开头的key
> key he[h-l]* # 遍历he开头的,第三个字母是h到l前缀的key
> ```
>
> **`keys *`的算法复杂度是O(N),由于Redis是单线程架构，当`keys *`执行时间过长时，会阻塞其他命令的执行**，可以使用`scan`命令，或者从热备从节点上执行命令来规避这种问题

* `dbsize`： 算出key的总数
* `exists key`：检查key是否存在
* `del key [key ...]`： 删除指定key-value
* `expire key seconds`：key在seconds秒后过期
* `ttl key` ：查看key剩余的过期时间
* `persist key`：去掉key的过期时间
* `type key`：查询key的类型
* `info`: 查看redis状态

时间复杂度

| 命令      | 时间复杂度 |
| --------- | ---------- |
| `keys`    | O(n)       |
| `dbsize`  | O(1)       |
| `del`     | O(1)       |
| `exists`  | O(1)       |
| `expire`  | O(1)       |
| `ttl`     | O(1)       |
| `persist` | O(1)       |
| `type`    | O(1)       |
|           |            |



## 数据结构和内部编码

![image-20210125180607916](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125180607916.png)

![RedisObject](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/RedisObject.png)

## 单线程架构

> Redis  6.0 支持了 多线程，具体细节参考链接-[支持多线程的Redis 6.0终于发布了](https://stor.51cto.com/art/202005/616005.htm)

![Redis单线程](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/Redis单线程.gif)

> 如上图所示，Redis 在一瞬间只会执行一个命令，不会并发执行命令。当命名执行时间过长时，会阻塞之后的命令运行。

由于Redis是单线程所以有以下的注意事项

1. Redis一次只运行一条命令
2. 拒绝长(慢)命令

> `keys`,  `flushall`,  `flushdb`,   `slow lua script`,  `mutil/exec`,  `operate big value(collection)`

3. 其实Redis不是纯单线程，还有一些后台任务,但执行命令只有一个线程

> fysnc file descriptor, close file descriptor



## 单线程为什么这么快

1. Redis是纯内存，
2. 非阻塞IO，IO多路复用

> ![image-20210125182758052](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125182758052.png)
>
> Redis 基于Epoll 实现了自己的多路复用的IO模型

3. **避免线程切换和竞态消耗**

## 字符串

### 结构和命令

![image-20210125183632583](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125183632583.png)

如上图所示，Redis字符串支持: 纯文本，数值，二进制等格式的数据。**字符串的限制是：不得大于512MB**。字符串类型的使用场景一般为：缓存、计数器、分布式锁、等等。

字符串支持的命令如下：

* `get key`: 获取key对应的value

--------

* `set key value`: 不管key是否存在，都设置key-value
* `setnx key value`: key不存在才设置
* `setxx key value xx`: key存在才设置

--------

* `del key`: 删除key-value

--------------

* `incr key`: key自增1，如果key不存在，自增后`get(key)=1` 
* `decr key`: key自减一，如果key不存在，自减后`get(key)=-1`
* `incrby key k`: key自增k，如果key不存在，自增后`get(key)=k`
* `decrby key k`: key自减k，如果key不存在，自减后`get(key)=-k`

------

* `incrbyfloat key 3.5`: 增加key对应的值3.5

------

* `mget key1 key2 key3`: 批量获取key，原子操作
* `mset key1 value1 key2 value2`: 批量设置key-value

> 单次操作和多次操作的区别：
>
> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125193309722.png" alt="image-20210125193309722" style="zoom:67%;" />
>
> <div style="font-size:15px"><center>单次传输<span></span></center> </div>
>
> <img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125193558283.png" alt="image-20210125193558283" style="zoom:67%;" />
>
> <div style="font-size:15px"><center>多次命令传输<span></span></center> </div>

时间复杂度如下

| 命令          | 时间复杂度 |
| ------------- | ---------- |
| `get`         | O(1)       |
| `set`         | O(1)       |
| `setnx`       | O(1)       |
| `del`         | O(1)       |
| `incr`        | O(1)       |
| `decr`        | O(1)       |
| `incrby`      | O(1)       |
| `decrby`      | O(1)       |
| `incrbyfloat` | O(1)       |
| `mget`        | O(n)       |
| `mset`        | O(n)       |
|               |            |

### 不常用API

* `getset key newvalue`: 给key设置一个新的值，并返回旧的值
* `append key value`: 将value追加到旧的value
* `strlen key`: 计算字符串的长度(中文字符串长度不精确)
* `getrange key start end`: 获取字符串指定下标的所有值
* `setrange key index value`: 设置下标所有对应的值

时间复杂度

| 命令       | 时间复杂度 |
| ---------- | ---------- |
| `getset`   | O(1)       |
| `append`   | O(1)       |
| `strlen`   | O(1)       |
| `getrange` | O(1)       |
| `setrange` | O(1)       |

## 哈希 

### 特点

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125195247235.png" alt="image-20210125195247235" style="zoom:67%;" />

<div style="font-size:15px"><center>实际结构<span></span></center> </div>

Hash结构中, file不能相同，value可以相同。

### 常用API

> 所有哈希的命令都已h开头

* `hget key field`: 获取hash key对应的field的value
* `hset key field value`: 设置hash key对应field的value
* `hsetnx key field value`: 不存在hash key对应的field时，才设置value
* `hdel key field`: 删除key 对应field 的value
* `hexists key field`: 判断hash key是否有field
* `hlen key`: 获取hash key field的数量
* `hmget key field1 field2 ... fieldN`: 批量获取hash key的一批 field对应的值
* `hmset key  field1 value1 field2 value2 ... fieldN valueN`: 批量设置hash key的一批field value
* `hincrby key field value`: 给hash key中的field增加对应的值
* `hincrbyfload key field floadCounter`: hincrby 浮点数版



时间复杂度

| 命令           | 时间复杂度 |
| -------------- | ---------- |
| `hget`         | O(1)       |
| `hset`         | O(1)       |
| `hsetnx`       | O(1)       |
| `hdel`         | O(1)       |
| `hexists`      | O(1)       |
| `hlen`         | O(1)       |
| `hmget`        | O(n)       |
| `hmset`        | O(n)       |
| `hincrby`      | O(1)       |
| `hincrbyfload` | O(1)       |
|                |            |

### hash vs string

![image-20210125202526772](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125202526772.png)

<div style="font-size:15px"><center>相似API<span></span></center> </div>

### 不常用API

* `hgetall key`: 返回hash key对应所有field和value

> **`hgetall`复杂度是O(n), 太大的key会阻塞其他命令的执行**

* `hvals key`: 返回hash key对应所有field的value
* `hkeys key`: 返回hash key对应所有的field
* 



时间复杂度

| 命令      | 时间复杂度 |
| --------- | ---------- |
| `hgetall` | O(n)       |
| `hvals`   | O(n)       |
| `hkeys`   | O(n)       |
|           |     |

## 列表

### 特点

![image-20210125203412286](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210125203412286.png)

<div style="font-size:15px"><center>列表结构<span></span></center> </div>

列表是一个有序的,可以重复,支持左右两边弹出的列表数据结构. **从左到右以0开始, 从右到左以-1开始**

### 重要API

> 列表的API都是以L或R开头

-----

增加API

* `rpush key value1 value2 ... valueN`: 从列表右端插入值(1-N)个
* `lpush key value1 vlaue2 ... valueN`: 从列表左端插入值(1-N)个
* `linsert key before|after value newValue`: 在list指定的值前|后插入newValue

------

删除API

* `lpop key`: 从列表左侧弹出一个item
* `rpop key`: 从列表右侧弹出一个item
* `lrem key count value`: 根据count值,从列表中删除所有value相等的项

> 1. `count > 0`, 从左到右,删除最多count个value相等的项
> 2. `count < 0`, 从左到右,删除最多`|count|`个value相等的项
> 3. `count = 0`, 删除所有value相等的项

* `ltrim key start end`: 按照索引范围修剪列表

-------

修改API

* `lset key index newValue`: 设置列表指定索引值未newValue

-----

查询API

* `lrange key start end`: 获取列表指定索引范围所有item

>  包含end

* `lindex key index`: 获取列表指定索引的item
* `llen key`: 获取列表长度

-------

时间复杂度

| 命令      | 时间复杂度               |
| --------- | ------------------------ |
| `rpush`   | O(1~n)根据插入的元素决定 |
| `rpush`   | O(1~n)根据插入的元素决定 |
| `linsert` | O(n)                     |
| `lpop`    | O(1)                     |
| `rpop`    | O(1)                     |
| `lrem`    | O(n)                     |
| `ltrim`   | O(n)                     |
| `lrange`  | O(n)                     |
| `lindex`  | O(1)                     |
| `llen`    | O(1)                     |
| `lset`    | O(n)                     |
|           |                          |

### 不常用API



* `blpop key timeout`: lpop 阻塞版本,timeout是阻塞超时,`timeout = 0`为永远不阻塞
* `brpop key timeout`, rpop阻塞版本,timeout是阻塞超时,`timeout = 0`为永远不阻塞





| 命令    | 时间复杂度 |
| ------- | ---------- |
| `blpop` | O(1)       |
| `brpop` | O(1)       |
|         |            |

### 使用技巧

1. `LPUSH` + `LPOP` = `Stack`
2. `LPUSH` + `RPOP` =  `Queue`
3. `LPUSH` + `LTRIM` = `Capped Collection`(固定集合)
4. `LPUSH` + `BRPOP` = `Message Quue`(消息队列)

## 集合

> 所有API以S开头

### 特点

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210127190826000.png" alt="image-20210127190826000" style="zoom:50%;" />

集合内的元素是无序且无重复的,集合同时支持集合间的操作.

### 集合内API

* `sadd key element`:  向集合key添加element(如果element已经存在,则添加失败)
* `srem key element `:  将集合key中的element删除
* `scard key`: 算出集合key的元素个数 
* `sismember key element`: 判断element是否属于集合key 

* `srandmember key`:从集合key中随机取一个元素
* `smembers key`: 从集合中取出所有的元素

> **O(N)操作**

* `spop key`:从集合中随机弹出一个元素
* `scan key`: 扫描集合key中的元素

注意 **`spop`会从集合中减少元素,`srandmember`不会减少集合元素个数**



| 命令          | 时间复杂度 |
| ------------- | ---------- |
| `srem`        | O(1)       |
| `srem`        | O(1)       |
| `scard`       | O(1)       |
| `sismember`   | O(1)       |
| `srandmemebr` | O(N)       |
| `smembers`    | O(1)       |
| `spop`        | O(1)       |
| `scan`        | O(1  )     |
|               |            |

  ### 集合间API

* `sdiff key1 key2`: 集合key1 和集合key2的差集
* `sinter key1 key2`: 集合key1 和集合key2的交集
* `sunion key1 key2`: 集合key1和集合key2的并集   
* `sdiff | sinter | sunio key1 key2 store key3`: 把集合key1和集合key2的运算结果存储到key3中

| 命令     | 时间复杂度 |
| -------- | ---------- |
| `sidff`  | O(N)       |
| `sinter` | O(N*M)     |
| `sunion` | O(1)       |
|          |            |

## 有序集合

> 有序集合的命令以Z开头

### 特点

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210127202112848.png" alt="image-20210127202112848" style="zoom:50%;" />

集合于有序集合对比

| 集合       | 有序集合        |
| ---------- | --------------- |
| 无重复元素 | 无重复元素      |
| 无序       | 有序            |
| element    | element + score |
|            |                 |



### 重要API

* `zadd key score element`: 添加score和element
* `zrem key element`: 删除元素
* `zscore key element`: 返回元素的分数

* `zincrby key increScore element`: 增加或减少元素的分数
* `zcard key`: 返回元素总个数
* `zrange key  start-end [withscroes]`: 返回集合指定位置的元素
* `zrangebyscore key minScore maxScore`: 返回指定分数范围内的升序元素
* `zcount key minScore maxScore`: 返回有序集合内在指定分数范围内个数
* `zremrangebyrank key start end`: 删除指定排名内的升序元素
* `zremrangebyscore key minScore maxScore`: 删除指定分数内的升序元素



| 命令                            | 时间复杂度                        |
| ------------------------------- | --------------------------------- |
| `zadd`                          | O(logN)                           |
| `zrem`                          | O(log(N))                         |
| `zscore`                        | O(log(N))                         |
| `zincrby`                       | O(log(N))                         |
| `zcard`                         | O(1)                              |
| `zrange`                        | O(log(n) + m) n为元素个数,m为个数 |
| `zrangebyscore`                 | O(log(n)+m) 同上                  |
| `zcount`                        | O(log(n)+m)                       |
| `zremrangebyrank key start end` | O(log(n)+m)                       |
| `zremrangebyscore`              | O(log(n)+m)                       |

### 不常用API



* `zrevrank key`: 从高到底的element的排名
* `zrevrange key`
* 同时有序集合支持集合的交差并集操作






