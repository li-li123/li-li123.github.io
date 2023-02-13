使用Netty 的 ChannelOption 和属性
====

比较麻烦的是创建通道后不得不手动配置每个通道，为了避免这种情况，Netty 提供了 ChannelOption 来帮助引导配置。这些选项会自动应用到引导创建的所有通道，可用的各种选项可以配置底层连接的详细信息，如通道“keep-alive(保持活跃)”或“timeout(超时)”的特性。

Netty 应用程序通常会与组织或公司其他的软件进行集成，在某些情况下，Netty 的组件如 Channel 在 Netty 正常生命周期外使用；Netty 的提供了抽象 AttributeMap 集合,这是由 Netty　的管道和引导类,和　AttributeKey<T>，常见类用于插入和检索属性值。属性允许您安全的关联任何数据项与客户端和服务器的Channel。

例如,考虑一个服务器应用程序跟踪用户和　Channel　之间的关系。这可以通过存储用户　ID　作为　Channel　的一个属性。类似的技术可以用来路由消息到基于用户　ID　或关闭基于用户活动的一个管道。

清单9.7展示了如何使用　ChannelOption　配置　Channel　和一个属性来存储一个整数值。

Listing 9.7 Using Attributes

```java
final AttributeKey<Integer> id = new AttributeKey<Integer>("ID");　//1

Bootstrap bootstrap = new Bootstrap(); //2
bootstrap.group(new NioEventLoopGroup()) //3
		.channel(NioSocketChannel.class) //4
        .handler(new SimpleChannelInboundHandler<ByteBuf>() { //5
            @Override
            public void channelRegistered(ChannelHandlerContext ctx) throws Exception {
               Integer idValue = ctx.channel().attr(id).get();  //6
                // do something  with the idValue
            }

            @Override
            protected void channelRead0(ChannelHandlerContext channelHandlerContext, ByteBuf byteBuf) throws Exception {
                System.out.println("Reveived data");
            }
        });
bootstrap.option(ChannelOption.SO_KEEPALIVE, true).option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000);   //7
bootstrap.attr(id, 123456); //8

ChannelFuture future = bootstrap.connect(new InetSocketAddress("www.manning.com", 80));   //9
future.syncUninterruptibly();
```

1. 新建一个 AttributeKey 用来存储属性值
2. 新建 Bootstrap 用来创建客户端管道并连接他们
3. 指定 EventLoopGroups 从和接收到的管道来注册并获取 EventLoop
4. 指定 Channel 类
5. 设置处理器来处理管道的 I/O 和数据
6. 检索 AttributeKey 的属性及其值
7. 设置 ChannelOption 将会设置在管道在连接或者绑定
8. 存储 id 属性
9. 通过配置的 Bootstrap 来连接到远程主机

## Option 参数设置说明

### 通用参数

| 参数名                           | 说明                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| `CONNECT_TIMEOUT_MILLIS`         | Netty参数，连接超时毫秒数，默认值30000毫秒即30秒。           |
| `MAX_MESSAGES_PER_READ`          | Netty参数，一次Loop读取的最大消息数，对于ServerChannel或者NioByteChannel，默认值为16，其他Channel默认值为1。默认值这样设置，是因为：ServerChannel需要接受足够多的连接，保证大吞吐量，NioByteChannel可以减少不必要的系统调用select。 |
| `WRITE_SPIN_COUNT`               | Netty参数，一个Loop写操作执行的最大次数，默认值为16。也就是说，对于大数据量的写操作至多进行16次，如果16次仍没有全部写完数据，此时会提交一个新的写任务给EventLoop，任务将在下次调度继续执行。这样，其他的写请求才能被响应不会因为单个大数据量写请求而耽误。 |
| `ALLOCATOR`                      | Netty参数，ByteBuf的分配器，默认值为ByteBufAllocator.DEFAULT，4.0版本为UnpooledByteBufAllocator，4.1版本为PooledByteBufAllocator。该值也可以使用系统参数io.netty.allocator.type配置，使用字符串值："unpooled"，"pooled"。 |
| `RCVBUF_ALLOCATOR`               | Netty参数，用于Channel分配接受Buffer的分配器，默认值为AdaptiveRecvByteBufAllocator.DEFAULT，是一个自适应的接受缓冲区分配器，能根据接受到的数据自动调节大小。可选值为FixedRecvByteBufAllocator，固定大小的接受缓冲区分配器。 |
| `AUTO_READ`                      | Netty参数，自动读取，默认值为True。**Netty只在必要的时候才设置关心相应的I/O事件**。对于读操作，需要调用channel.read()设置关心的I/O事件为OP_READ，这样若有数据到达才能读取以供用户处理。该值为True时，每次读操作完毕后会自动调用channel.read()，从而有数据到达便能读取；否则，需要用户手动调用channel.read()。需要注意的是：当调用config.setAutoRead(boolean)方法时，如果状态由false变为true，将会调用channel.read()方法读取数据；由true变为false，将调用config.autoReadCleared()方法终止数据读取。 |
| `WRITE_BUFFER_HIGH_WATER_MARK`   | Netty参数，写高水位标记，默认值64KB。如果Netty的写缓冲区中的字节超过该值，Channel的isWritable()返回False。 |
| `WRITE_BUFFER_LOW_WATER_MARK`    | Netty参数，写低水位标记，默认值32KB。当Netty的写缓冲区中的字节超过高水位之后若下降到低水位，则Channel的isWritable()返回True。写高低水位标记使用户可以控制写入数据速度，从而实现流量控制。推荐做法是：每次调用channl.write(msg)方法首先调用channel.isWritable()判断是否可写。 |
| `MESSAGE_SIZE_ESTIMATOR`         | Netty参数，消息大小估算器，默认为DefaultMessageSizeEstimator.DEFAULT。估算ByteBuf、ByteBufHolder和FileRegion的大小，其中ByteBuf和ByteBufHolder为实际大小，FileRegion估算值为0。该值估算的字节数在计算水位时使用，FileRegion为0可知FileRegion不影响高低水位。 |
| `SINGLE_EVENTEXECUTOR_PER_GROUP` | Netty参数，单线程执行ChannelPipeline中的事件，默认值为True。该值控制执行ChannelPipeline中执行ChannelHandler的线程。如果为Trye，整个pipeline由一个线程执行，这样不需要进行线程切换以及线程同步，是Netty4的推荐做法；如果为False，ChannelHandler中的处理过程会由Group中的不同线程执行。 |
### SocketChannel参数

| 参数名               | 说明                                                         |
| -------------------- | ------------------------------------------------------------ |
| `SO_RCVBUF`          | Socket参数，TCP数据接收缓冲区大小。该缓冲区即TCP接收滑动窗口，linux操作系统可使用命令：`cat /proc/sys/net/ipv4/tcp_rmem`查询其大小。一般情况下，该值可由用户在任意时刻设置，但当设置值超过64KB时，需要在连接到远端之前设置。 |
| `SO_SNDBUF`          | Socket参数，TCP数据接收缓冲区大小。该缓冲区即TCP接收滑动窗口，linux操作系统可使用命令：cat /proc/sys/net/ipv4/tcp_rmem查询其大小。一般情况下，该值可由用户在任意时刻设置，但当设置值超过64KB时，需要在连接到远端之前设置。 |
| `TCP_NODELAY`        | TCP参数，立即发送数据，默认值为Ture（Netty默认为True而操作系统默认为False）。该值设置Nagle算法的启用，改算法将小的碎片数据连接成更大的报文来最小化所发送的报文的数量，如果需要发送一些较小的报文，则需要禁用该算法。Netty默认禁用该算法，从而最小化报文传输延时。 |
| `SO_KEEPALIVE`       | Socket参数，连接保活，默认值为False。启用该功能时，TCP会主动探测空闲连接的有效性。可以将此功能视为TCP的心跳机制，需要注意的是：默认的心跳间隔是7200s即2小时。Netty默认关闭该功能。 |
| `SO_REUSEADDR`       | Socket参数，地址复用，默认值False。有四种情况可以使用：(1).当有一个有相同本地地址和端口的socket1处于`TIME_WAIT`状态时，而你希望启动的程序的socket2要占用该地址和端口，比如重启服务且保持先前端口。(2).有多块网卡或用IP Alias技术的机器在同一端口启动多个进程，但每个进程绑定的本地IP地址不能相同。(3).单个进程绑定相同的端口到多个socket上，但每个socket绑定的ip地址不同。(4).完全相同的地址和端口的重复绑定。但这只用于UDP的多播，不用于TCP。 |
| `SO_LINGER`          | Socket参数，关闭Socket的延迟时间，默认值为-1，表示禁用该功能。-1表示socket.close()方法立即返回，但OS底层会将发送缓冲区全部发送到对端。0表示socket.close()方法立即返回，OS放弃发送缓冲区的数据直接向对端发送RST包，对端收到复位错误。非0整数值表示调用socket.close()方法的线程被阻塞直到延迟时间到或发送缓冲区中的数据发送完毕，若超时，则对端会收到复位错误。 |
| `IP_TOS`             | IP参数，设置IP头部的Type-of-Service字段，用于描述IP包的优先级和QoS选项。 |
| `ALLOW_HALF_CLOSURE` | Netty参数，一个连接的远端关闭时本地端是否关闭，默认值为False。值为False时，连接自动关闭；为True时，触发`ChannelInboundHandler的userEventTriggered()`方法，事件为`ChannelInputShutdownEvent`。 |
|                      |                                                              |

### ServerSocketChannel参数

| 参数名         | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| `SO_RCVBUF`    | 已说明，需要注意的是：当设置值超过64KB时，需要在绑定到本地端口前设置。该值设置的是由ServerSocketChannel使用accept接受的SocketChannel的接收缓冲区。 |
| `SO_REUSEADDR` | Socket参数，地址复用，默认值False。有四种情况可以使用：(1).当有一个有相同本地地址和端口的socket1处于`TIME_WAIT`状态时，而你希望启动的程序的socket2要占用该地址和端口，比如重启服务且保持先前端口。(2).有多块网卡或用IP Alias技术的机器在同一端口启动多个进程，但每个进程绑定的本地IP地址不能相同。(3).单个进程绑定相同的端口到多个socket上，但每个socket绑定的ip地址不同。(4).完全相同的地址和端口的重复绑定。但这只用于UDP的多播，不用于TCP。 |
| `SO_BACKLOG`   | Socket参数，服务端接受连接的队列长度，如果队列已满，客户端连接将被拒绝。默认值，Windows为200，其他为128。 |
|                |                                                              |

### DatagramChannel参数

| 参数名                       | 说明                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `SO_BROADCAST`               | Socket参数，设置广播模式。                                   |
| `SO_RCVBUF`                  | Socket参数，TCP数据接收缓冲区大小。该缓冲区即TCP接收滑动窗口，linux操作系统可使用命令：`cat /proc/sys/net/ipv4/tcp_rmem`查询其大小。一般情况下，该值可由用户在任意时刻设置，但当设置值超过64KB时，需要在连接到远端之前设置。 |
| `SO_SNDBUF`                  | Socket参数，TCP数据接收缓冲区大小。该缓冲区即TCP接收滑动窗口，linux操作系统可使用命令：cat /proc/sys/net/ipv4/tcp_rmem查询其大小。一般情况下，该值可由用户在任意时刻设置，但当设置值超过64KB时，需要在连接到远端之前设置。 |
| `SO_REUSEADDR`               | Socket参数，地址复用，默认值False。有四种情况可以使用：(1).当有一个有相同本地地址和端口的socket1处于`TIME_WAIT`状态时，而你希望启动的程序的socket2要占用该地址和端口，比如重启服务且保持先前端口。(2).有多块网卡或用IP Alias技术的机器在同一端口启动多个进程，但每个进程绑定的本地IP地址不能相同。(3).单个进程绑定相同的端口到多个socket上，但每个socket绑定的ip地址不同。(4).完全相同的地址和端口的重复绑定。但这只用于UDP的多播，不用于TCP。 |
| `IP_MULTICAST_LOOP_DISABLED` | 对应IP参数`IP_MULTICAST_LOOP`，设置本地回环接口的多播功能。由于`IP_MULTICAST_LOOP`返回True表示关闭，所以`Netty`加上后缀`_DISABLED`防止歧义。 |
| `IP_MULTICAST_ADDR`          | 对应IP参数IP_MULTICAST_IF，设置对应地址的网卡为多播模式。    |
| `IP_MULTICAST_IF`            | 对应IP参数IP_MULTICAST_IF2，同上但支持IPV6。                 |
|                              |                                                              |

