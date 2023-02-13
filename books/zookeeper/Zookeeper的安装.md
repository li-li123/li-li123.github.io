## 安装文档

1. 安装 JDK

2. 下载 Zookeeper 官方安装包-[官方网址](https://zookeeper.apache.org/releases.html)

3. zookeeper 目录结构

   > * `bin`: `Zookeeper` 的可执行文件
   > * `conf`: `Zookeeper` 的配置文件
   > * `docs`: 文档
   > * `lib`: `Zookeeper` 所需依赖
   > * `recipes`: 官方示例

3. 修改配置文件

> * 配置文件位于  `<zookeeper>/conf/zoo.cfg`
>
> * 常用配置选项
>   * `tickTime`: 用于计算的时间单元, 单位为毫秒( `milliseconds` ), 比如 session 超时:  `N * tickTime`
>   * `initLimit`: 用于集群, 允许从节点连接并同步到 master 节点的初始化连接时间, 以 `tickTime` 的倍数表示
>   * `syncLimit`: 用于集群, master 主节点与从节点之间发送消息, 请求和应答时间长度(心跳机制)
>   * `dataDir`: 数据目录, **必须配置**
>   * `logDir`: 日志目录, 如果不配置, 将使用  `dataDir` 目录
>   * `clientPort`: 服务器的连接端口, 默认 2181
>
> * 示例 配置文件
>
>   ```properties
>   # The number of milliseconds of each tick
>   tickTime=2000
>   # The number of ticks that the initial
>   # synchronization phase can take
>   initLimit=10
>   # The number of ticks that can pass between
>   # sending a request and getting an acknowledgement
>   syncLimit=5
>   # the directory where the snapshot is stored.
>   # do not use /tmp for storage, /tmp here is just
>   # example sakes.
>   dataDir=/opt/zookeeper/data
>   # the port at which the clients will connect
>   clientPort=2181
>   # the maximum number of client connections.
>   # increase this if you need to handle more clients
>   #maxClientCnxns=60
>   #
>   # Be sure to read the maintenance section of the
>   # administrator guide before turning on autopurge.
>   #
>   # http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
>   #
>   # The number of snapshots to retain in dataDir
>   #autopurge.snapRetainCount=3
>   # Purge task interval in hours
>   # Set to "0" to disable auto purge feature
>   #autopurge.purgeInterval=1
>   
>   ## Metrics Providers
>   #
>   # https://prometheus.io Metrics Exporter
>   #metricsProvider.className=org.apache.zookeeper.metrics.prometheus.PrometheusMetricsProvider
>   #metricsProvider.httpPort=7000
>   #metricsProvider.exportJvmInfo=true
>   # 以下为个节点的 IP
>   server.1=192.168.0.63:2888:3888 
>   server.2=192.168.0.64:2888:3888
>   server.3=192.168.0.65:2888:3888
>   ```

4. 设置各节点ID

> 在每个节点的 `dataDir` 中新建文件 `myid` 并填入 `ID`

5. 启动各节点的 `Zookeeper` 

> `<zookeeper>/bin/zkServer.sh start`

