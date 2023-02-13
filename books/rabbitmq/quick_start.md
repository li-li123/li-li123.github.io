## 概念解析

### Virtual Host 虚拟主机

* 虚拟地址，用于进行逻辑隔离，最上层的消息路由
* 一个Virtual Host 里面可以有若干个Exchange 和Queue
* 同一个Virtual Host里面不能有相同名称的Exchange 或Queue

### Exchange 交换机

Exchange 的作用是接受消息，并根据路由键转发消息所绑定的队列

### Binding 绑定

* Exchange和Exchange、Queue之间的关系

* Binding 中可以包含RoutingKey或者参数

### Queue消息队列

* 消息队列，实际存储消息数据
* Durability： 是否持久化  (Durable：是, Transient： 否)
* Auto： 如果选yes，代表当最后一个监听被移除之后，该Queue会被自动删除

### Message

* 服务器和应用程序之间传送的数据
* 本职上就是一段数据 由Properties和Payload(Body)组成
* 常用属性: delivery mode、 headers(自定义属性)
* 其他属性
  * content_type 
  * content_encoding
  * priority
  * correlation_id 消息的唯一ID，之类的属性
  * replay_to 返回到哪个队列
  * expiration 过期事件
  * message_id
  * timestamp
  * type
  * user_id
  * app_id
  * cluster_id

## 基础消息的发布与消费

## 代码基本步骤

1. ConnectionFactory: 获取连接工厂
2. Connection： 获取连接
3. Channel： 数据通信信道，可发送和接收消息
4. Queue： 具体的消息存储队列
5. Producer & Consumer: 生产和消费者

### 依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
<!-- 或者 --->
<dependency>
     <groupId>com.rabbitmq</groupId>
     <artifactId>amqp-client</artifactId>
</dependency>
```

### 生产者

```shell
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class Producer {

    public static void main(String[] args) throws IOException, TimeoutException {

        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        for(int i=0;i<10;i++){
            // 4. 通过Channel发送数据
            // 不指定交换机时，rabbitmq会把消息自动转发到，与routeKey相同的queue中
            channel.basicPublish("", "test001", null, ("Hello RabbitMQ-"+i).getBytes());
        }


        // 5. 关闭连接
        channel.close();
        connection.close();
    }



}

```

### 消费者

```shell
public class Consumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        // 4. 声明一个队列
        String queueName = "test001";
        // 参数1: 队列名
        // 参数2: 是否开启持久化(即同步到磁盘)
        // 参数3: 是否独占(开启后, 该队列只允许用于本连接)
        // 参数4: 是否自动删除(当队列不再使用时，集群自动删除该队列)
        // 参数5: 可选参数
        channel.queueDeclare(queueName, true, false, false, null);

        // 5. 创建消费者
        QueueingConsumer queueingConsumer = new QueueingConsumer(channel);

        // 6. 设置channel
        channel.basicConsume(queueName, true, queueingConsumer);

        // 7. 获取消息
        while (true){

            QueueingConsumer.Delivery delivery = queueingConsumer.nextDelivery();
            String msg = new String(delivery.getBody());
            System.out.println("消费端: "+msg);

        }


    }
}
```
> 队列，交换机都可以重复申请，当申请的属性和集群中已经存在的属性不一致时，会报错。
>
> ```java
> Caused by: com.rabbitmq.client.ShutdownSignalException: channel >error; protocol method: #method<channel.close>(reply-code=406, >reply-text=PRECONDITION_FAILED - inequivalent arg 'durable' for queue 'test001' in vhost '/': >received 'false' but current is 'true', class-id=50, method-id=10)
> 	at com.rabbitmq.client.impl.ChannelN.asyncShutdown(ChannelN.java:483)
> 	at com.rabbitmq.client.impl.ChannelN.processAsync(ChannelN.java:320)
> 	at com.rabbitmq.client.impl.AMQChannel.handleCompleteInboundCommand(AMQChannel.java:143)
> 	at com.rabbitmq.client.impl.AMQChannel.handleFrame(AMQChannel.java:90)
> 	at com.rabbitmq.client.impl.AMQConnection$MainLoop.run(AMQConnection.java:559)
> 	at java.lang.Thread.run(Thread.java:748)
> ```

## 交换机

Exchange 的作用是接受消息，并根据路由键转发消息所绑定的队列

![image-20200417112324781](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20200417112324781.png?x-oss-process=style/default)

### 交换机的属性

* Name 交换机的名称
* Type 交换机的类型 direct、topic、fanout、header
* Durability： 是否持久化， true为持久化
* Auto Delete： 当最后绑定到Exchange上的队列删除后， 自动删除该Exchange
* Internal： 当前Exchange是否用户RabbitMQ内部使用， 默认为False
* Arguments： 扩展参数，用户扩展AMQP协议自制定化使用

### Direct Exchange

所有发送到Direct Exchange的消息被转发到RouteKey中指定的Queue

注意：Direct 模式可以使用RabbitMQ自带的Exchange：default Exchange，所以不需要将Exchange进行任何绑定操作，消息传递时，RouteKey必须完全匹配才会被队列接收，否则该消息会被抛弃

####  Producer 代码

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class Producer {

    public static void main(String[] args) throws IOException, TimeoutException {

        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        // 4. 声明
        String exchangeName = "test_direct_exchange";
        String routingKey = "test.direct";

        String msg = "Hello World RabbitMQ 4 Direct Exchange Message...";
        channel.basicPublish(exchangeName, routingKey, null,msg.getBytes());

        // 5. 关闭连接
        channel.close();
        connection.close();
    }



}
```

#### Consumber 代码

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.QueueingConsumer;
import org.springframework.amqp.core.ExchangeTypes;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class Consumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        // 设置自动重连
        connectionFactory.setAutomaticRecoveryEnabled(true);
        connectionFactory.setNetworkRecoveryInterval(3000);

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        // 4. 声明
        String exchangeName = "test_direct_exchange";
        String queueName = "test_direct_queue";
        String routingKey = "test.direct";
        // 声明交换机
        // 参数1: 交换机的名称
        // 参数2: 交换机的类型 direct、topic、fanout、header
        // 参数3: 是否持久化， true为持久化
        // 参数4: 当最后绑定到Exchange上的队列删除后， 自动删除该Exchange
        // 参数5: 当前Exchange是否用户RabbitMQ内部使用， 默认为False
        // 参数6:  扩展参数，用户扩展AMQP协议自制定化使用
        channel.exchangeDeclare(exchangeName, ExchangeTypes.DIRECT, true, false, false, null);
        // 声明queue
        channel.queueDeclare(queueName, false, false, false, null);
        // 绑定 Exchange
        channel.queueBind(queueName, exchangeName, routingKey);

        // 5. 创建消费者
        QueueingConsumer queueingConsumer = new QueueingConsumer(channel);
        // 6. 设置channel
        channel.basicConsume(queueName, true, queueingConsumer);

        // 7. 获取消息
        while (true){

            QueueingConsumer.Delivery delivery = queueingConsumer.nextDelivery();
            String msg = new String(delivery.getBody());
            System.out.println("消费端: "+msg);

        }
        
    }
}
```
> Queue可以同时Bind多个Exchange和RoutingKey。但是绑定Exchange时，Exchange必须存在

### Topic Exchange

![image-20200417122305249](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20200417122305249.png?x-oss-process=style/default)

* 所有发送到Topic Exchange 的消息被转发到所有关心RouteKey中指定Topic的Queue上

* Exchange 将RouteKey 和某 Topic 进行模糊匹配，此时队列需要绑定一个Topic

注意： 可以使用通配符进行模糊匹配

* “#” 可以匹配一个或多个词
* “*” 匹配不多不少一个词

   例如 “log.#” 能够匹配到 “log.info.oa”

			"log.*" 只会匹配到 “log.erro”

**Consumer能够接收到的消息是全部topic的合集**

#### Producer 代码

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class TopicProducer {

    public static void main(String[] args) throws IOException, TimeoutException {

        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        // 4. 声明
        String exchangeName = "test_topic_exchange";
        String routingKey1 = "user.save";
        String routingKey2 = "user.update";
        String routingKey3 = "user.delete.abc";

        String msg = "Hello World RabbitMQ 4 Topic Exchange Message...";
        channel.basicPublish(exchangeName, routingKey1, null,msg.getBytes());
        channel.basicPublish(exchangeName, routingKey2, null,msg.getBytes());
        channel.basicPublish(exchangeName, routingKey3, null,msg.getBytes());

        // 5. 关闭连接
        channel.close();
        connection.close();
    }


}

```

#### Consumer 代码

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.QueueingConsumer;
import org.springframework.amqp.core.ExchangeTypes;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class TopicConsumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        // 设置自动重连
        connectionFactory.setAutomaticRecoveryEnabled(true);
        connectionFactory.setNetworkRecoveryInterval(3000);

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        // 4. 声明
        String exchangeName = "test_topic_exchange";
        String queueName = "test_topic_queue_*";
        String routingKey = "user.*";
        // 声明交换机
        channel.exchangeDeclare(exchangeName, ExchangeTypes.TOPIC, true, false, false, null);
        // 声明queue
        channel.queueDeclare(queueName, false, false, false, null);
        // 绑定 Exchange
        channel.queueBind(queueName, exchangeName, routingKey);

        // 5. 创建消费者
        QueueingConsumer queueingConsumer = new QueueingConsumer(channel);
        // 6. 设置channel
        channel.basicConsume(queueName, true, queueingConsumer);

        // 7. 获取消息
        while (true){

            QueueingConsumer.Delivery delivery = queueingConsumer.nextDelivery();
            String msg = new String(delivery.getBody());
            System.out.println("消费端: "+msg);

        }

    }
}
```
> 每条消息都有一个内部ID，不会被重复消费

### Fanout Exchange

* 不处理路由键，只需要简单的将队列绑定到交换机上
* 发送到交换机的消息都会转发到与该交换机绑定的所有队列上
* Fanout交换及转发消息是最快的

![image-20200417125030254](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20200417125030254.png?x-oss-process=style/default)



#### procuder 代码

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class FanoutProducer {

    public static void main(String[] args) throws IOException, TimeoutException {

        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        // 4. 声明
        String exchangeName = "test_fanout_exchange";


        String routingKey = "fanout";

        String msg = "Hello World RabbitMQ 4 Fanout Exchange Message...";

        channel.basicPublish(exchangeName, routingKey, null,msg.getBytes());

        // 5. 关闭连接
        channel.close();
        connection.close();
    }

}
```

#### Consumer 代码

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.QueueingConsumer;
import org.springframework.amqp.core.ExchangeTypes;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class FanoutConsumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        // 设置自动重连
        connectionFactory.setAutomaticRecoveryEnabled(true);
        connectionFactory.setNetworkRecoveryInterval(3000);

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        // 4. 声明
        String exchangeName = "test_fanout_exchange";
        String queueName = "test_fanout_queue";
        String routingKey = "";
        // 声明交换机
        channel.exchangeDeclare(exchangeName, ExchangeTypes.FANOUT, true, false, false, null);
        // 声明queue
        channel.queueDeclare(queueName, false, false, false, null);
        // 绑定 Exchange
        channel.queueBind(queueName, exchangeName, routingKey);

        // 5. 创建消费者
        QueueingConsumer queueingConsumer = new QueueingConsumer(channel);
        // 6. 设置channel
        channel.basicConsume(queueName, true, queueingConsumer);

        // 7. 获取消息
        while (true){

            QueueingConsumer.Delivery delivery = queueingConsumer.nextDelivery();
            String msg = new String(delivery.getBody());
            System.out.println("消费端: "+msg);

        }

    }
}
```
### Header Exchange
Header Exchange使用较少，具体参阅[RabbitMQ之header exchange(头交换机)用法](https://blog.csdn.net/hry2015/article/details/79188615)
## 消息的附加属性

### producer

```java
import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.springframework.boot.autoconfigure.jms.JmsProperties;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeoutException;

public class Producer {

    public static void main(String[] args) throws IOException, TimeoutException {

        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        Map<String, Object> customerHeader = new HashMap<>();
        customerHeader.put("my1", "111");
        customerHeader.put("my2", "222");

        AMQP.BasicProperties properties = new AMQP.BasicProperties.Builder()
                .deliveryMode(2) //1- 代表持久化 2-代表不持久化
                .expiration("10000") // 消息的过期时间
                .contentEncoding("UTF-8") // 消息的编码
                .headers(customerHeader)
                .build();


        for(int i=0;i<10;i++){
            // 4. 通过Channel发送数据
            channel.basicPublish("", "test001", properties, ("Hello RabbitMQ-"+i).getBytes());
        }

        // 5. 关闭连接
        channel.close();
        connection.close();
    }
    
}
```
> 队列持久化和消息持久化不是一个概念！！！！！！！！！！！
>
> 队列设置持久化后，集群重启后。队列还会存在集群中，但是里面的未发送的消息是否还存在，就跟消息的持久化设置相关。**默认消息并不会自动持久化**。
>
> 总结一下就是，队列不设置持久化，集群重启后消息一定会消失(因为队列都已经不存在了),当队列设置持久化后，集群重启后，只有设置持久化的消息才会存在。
### consumer

```java
import com.rabbitmq.client.*;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class Consumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        //1. 创建连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        //2. 通过连接工厂创建连接
        Connection connection = connectionFactory.newConnection();

        // 3. 通过Connection创建Channel
        Channel channel = connection.createChannel();

        // 4. 声明一个队列
        String queueName = "test001";
        channel.queueDeclare(queueName, true, false, false, null);

        // 5. 创建消费者
        QueueingConsumer queueingConsumer = new QueueingConsumer(channel);

        // 6. 设置channel
        channel.basicConsume(queueName, true, queueingConsumer);

        // 7. 获取消息
        while (true){

            QueueingConsumer.Delivery delivery = queueingConsumer.nextDelivery();
            System.out.println("#########################");
            String msg = new String(delivery.getBody());
            System.out.println("消费端: "+msg);
            AMQP.BasicProperties properties = delivery.getProperties();
            System.out.println("my1: "+ properties.getHeaders().getOrDefault("my1", "None"));
            System.out.println("my2: "+ properties.getHeaders().getOrDefault("my2", "None"));


        }



    }
}

```