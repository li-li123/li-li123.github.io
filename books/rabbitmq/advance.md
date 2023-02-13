## 消息如何保障100%投递成功

### 生产端的可靠性投递

* 保障消息的成功发出
* 保障MQ节点的成功接收
* 发送端收到MQ节点(Broken)确认应答
* 完善的消息补偿机制

### BAT/TMD 互联网大厂的解决方案

* 消息落库，对消息打标

  ![image-20200417144256674](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20200417144256674.png?x-oss-process=style/default)

* 消息的延迟投递，做二次确认，回调检查

![image-20200417145525683](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20200417145525683.png?x-oss-process=style/default)

## 如何避免消息的重复消费问题

消费端实现幂等性，就意味着，我们的消息永远不会消费多次，即使我们收到了多条一样的消息

### 业界主流的幂等性操作

* 唯一ID + 指纹码机制， 利用数据库主键去重
  * SELECT COUNT(1) FROM T_ORDER WHERE ID = 唯一ID + 指纹码
  * 好处： 实现简单
  * 坏处： 高并发下数据库写入的性能瓶颈
  * 解决方案: 跟进ID进行分库分表进行算法路由

* 利用Redis的原子性去实现
  * 利用Redis进行幂等，需要考虑的问题
  * 第一：我们是否要进行数据落库，如果落库的话，关键解决的问题是数据库与缓存的一致性问题
  * 第二： 如果不进行落库，那么都存储到缓存中，如何设置定时同步策略

## Confirm 确认消息
> 具体细节参阅[RabbitMQ之消息确认机制（事务+Confirm）](https://blog.csdn.net/u013256816/article/details/55515234)

* 消息的确认，是指生产者投递消息后，如果Broker收到消息，则会给我们生产者一个应答
* 生产者进行接受应答，用来确认这条消息能否正常发送到Broker，这种方式也是消息的可靠性投递的核心保障！

![image-20200417174714380](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20200417174714380.png?x-oss-process=style/default)

### 如何实现Confirm确认消息

1. 在Channel上开启确认模式: channel.confirmSelect()
2. 在channel上添加监听: addConfirmLinstener, 监听成功和失败的返回结果，根据具体的结果对消息进行重新发送、或记录日志等后续处理

### procuder

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConfirmListener;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class Producer {

    public static void main(String[] args) throws IOException, TimeoutException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        // 指定消息的确认模式
        channel.confirmSelect();

        String exchangeName = "test_confirm_exchange";
        String routingKey = "confirm_save";

        String msg = "Hello RabbitMQ send Confirm message!";
        channel.basicPublish(exchangeName, routingKey, null, msg.getBytes());

        // 添加监听器
        channel.addConfirmListener(new ConfirmListener() {
            // 成功处理，回调的方法
            @Override
            public void handleAck(long deliveryTag, boolean multiple) throws IOException {
                System.out.println("----------------- ack -----------------");
            }

            // 失败回调的方法
            @Override
            public void handleNack(long deliveryTag, boolean multiple) throws IOException {
                System.out.println("----------------- no ack -----------------");
            }
        });
        
        // 关闭连接，线程会退出，否则不会主动退出
        // channel.close();
        // connection.close();

    }

}

```

### consumer

```java
import com.rabbitmq.client.*;
import org.springframework.amqp.core.ExchangeTypes;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class Consumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        String exchangeName = "test_confirm_exchange";
        String queueName = "confirm_queue";
        channel.exchangeDeclare(exchangeName, ExchangeTypes.FANOUT, false, false, null);
        channel.queueDeclare(queueName, false, false, false, null);
        channel.queueBind(queueName, exchangeName, queueName);

        QueueingConsumer consumer = new QueueingConsumer(channel);
        channel.basicConsume(queueName, true, consumer);

        while (true){
            QueueingConsumer.Delivery delivery = consumer.nextDelivery();
            String msg = new String(delivery.getBody());
            System.out.println("消费端: "+msg);
        }
    }
}
```



## Return 返回消息

![image-20200417183031271](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20200417183031271.png?x-oss-process=style/default)

* Return Listener 用于处理一些不可路由的消息
* 我们的消费生产者，通过指定一个Exchange和RoutingKey把消息送达到某一个队列中去，然后我们的消费者监听队列，进行消费的处理

* 但是在某些情况下，如果我们在发送消息的时候，当前的exchange不存在或者指定的路由的key路由不到，这个时候如果我们需要监听这种不可达的消息，就要使用Return Listener

### Return 消息机制
> 消息的Confirm和消息的Return，**只有指定的交换机存在时才会生效**。

* 在基础API中有一个关键的配置项
* Mandatory： 如果为true，则监听器会接收到路由不可达的消息，然后进行后续处理，如果为false，那么broker端会自动删除消息

### producer

```java
import com.rabbitmq.client.*;

import java.io.IOException;
import java.util.Optional;
import java.util.concurrent.TimeoutException;

public class ReturnProducer {

    public static void main(String[] args) throws IOException, TimeoutException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        // 指定消息的确认模式
        channel.confirmSelect();

        String exchangeName = "test_return_exchange";
        String routingKey = "return_save";
        String routingERRKey = "no_save";

        // 添加监听器
        channel.addReturnListener(new ReturnListener() {
            /**
             *
             * @param replyCode 响应码
             * @param replyText 响应文本
             * @param exchange 消息指定的交换机
             * @param routingKey 消息指定的routingKEY
             * @param properties 消息的properties
             * @param body 消息的body
             * @throws IOException 可能抛出的异常
             */
            @Override
            public void handleReturn(int replyCode, String replyText, String exchange, String routingKey, AMQP.BasicProperties properties, byte[] body) throws IOException {
                System.out.println("----- handle ----return");
                System.out.println("replayCode: "+replyCode);
                System.out.println("replayText: "+replyText);
                System.out.println("exchange: "+ exchange);
                System.out.println("property: "+ Optional.of(properties).get());
                System.out.println("replayCode: "+new String(body));
            }
        });

        String msg = "Hello RabbitMQ send Return message!";
        // 第3个参数表示，如果路由不到broken是否自动删除该消息。只有设置为true ReturnListener才会生效
        channel.basicPublish(exchangeName, routingERRKey, true, null, msg.getBytes());

        // 关闭连接，线程会退出，否则不会主动退出
        // channel.close();
        // connection.close();

    }

}
```

### consumer

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.QueueingConsumer;
import org.springframework.amqp.core.ExchangeTypes;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class ReturnConsumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        String exchangeName = "test_return_exchange";
        String queueName = "return_queue";
        String routingKey = "return_save";
        channel.exchangeDeclare(exchangeName, ExchangeTypes.DIRECT, false, false, null);
        channel.queueDeclare(queueName, false, false, false, null);
        channel.queueBind(queueName, exchangeName, routingKey);

        QueueingConsumer consumer = new QueueingConsumer(channel);
        channel.basicConsume(queueName, true, consumer);

        while (true){
            QueueingConsumer.Delivery delivery = consumer.nextDelivery();
            String msg = new String(delivery.getBody());
            System.out.println("消费端: "+msg);
        }
    }
}

```



## 自定义消费者

```java
import com.rabbitmq.client.*;
import com.rabbitmq.client.Consumer;

import java.io.IOException;

public class MyConsumer extends DefaultConsumer {
    public MyConsumer(Channel channel) {
        super(channel);
    }

    /**
     *
     * @param consumerTag 消费标签
     * @param envelope 环境变量
     * @param properties properties
     * @param body 消息内容
     * @throws IOException 可能抛出的异常
     */
    @Override
    public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {

        System.out.println("------------- consumer message ---------------");
        System.out.println("consumerTag" + consumerTag);
        System.out.println("envelope" + envelope);
        System.out.println("properties" + properties);
        System.out.println("body" + new String(body));

    }
}

```

### producer

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConfirmListener;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class Producer {

    public static void main(String[] args) throws IOException, TimeoutException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        // 指定消息的确认模式
        channel.confirmSelect();

        String exchangeName = "test_consumer_exchange";
        String routingKey = "customer_save";
        for(int i=0;i<10;i++){
            String msg = "Hello RabbitMQ send customer Consumer message From " + i;
            channel.basicPublish(exchangeName, routingKey, null, msg.getBytes());
        }


        // 关闭连接，线程会退出，否则不会主动退出
         channel.close();
         connection.close();

    }

}

```

### consumer

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
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        String exchangeName = "test_consumer_exchange";
        String queueName = "consumer_queue";
        String routingKey = "customer_save";
        channel.exchangeDeclare(exchangeName, ExchangeTypes.FANOUT, false, false, null);
        channel.queueDeclare(queueName, false, false, false, null);
        channel.queueBind(queueName, exchangeName, routingKey);
        
        channel.basicConsume(queueName, true, new MyConsumer(channel));
        // 自定义 consumerTag
        // channel.basicConsume(queueName, true, "HelloWorld",new MyCustomConsumer(channel));


    }
}

```

## 消息的限流

假设一个场景，首先我们的RabbitMQ服务器有上万条未处理的消息，我们随便打开一个客户端，会出现巨量的消息推送到客户端中，但是我们单个客户端处理不过来这么多数据，导致系统崩溃。

RabbitMQ提供了一种**qos(服务质量保证)**功能，即在非确认自动消息的前提下，如果一定数目的消息(通过基于consume或者channel设置Qos值)未被确认前，不进行任何消息的消费

* * 

### 消费端限流

void BasicQos(unit prefetchSize , ushort prefetchCount, bool global)

* prefetchSize 消息的大小限制 。参数为0是不做限制
* prefetchCount 一次能处理的消息条数， 一般设置为1
* global 限流策略（true ：channel中使用，false：consumer中使用）

设置策略：

* prefetchSize: 0
* prefetchCount 会告诉RabbitMQ不要同时给一个消费者推送多余N个消息，即一旦有N个消息还没有ack，则该consumer将block掉，直到有消息ack
* global： ture\false 是否将在上面的设置应用于channel。简单点来说，就是上面的限制是channel级别的还是consumer级别的

注意：prefetchsize 和global这两个选项，rabbitmq没有实现，占不研究prefetch_count。在no_ack=false的情况下，限流策略才会生效，自动应答的情况下是不生效的

### 自定义 Consumer

```java
import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

public class LimitCustomerConsumer extends DefaultConsumer {
    private Channel channel;

    public LimitCustomerConsumer(Channel channel) {
        super(channel);
        this.channel = channel;
    }

    private List<Long> eTagList = new Vector<>();

    /**
     *
     * @param consumerTag 消费标签
     * @param envelope 环境变量
     * @param properties properties
     * @param body 消息内容
     * @throws IOException 可能抛出的异常
     */
    @Override
    public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {

        System.out.println("------------- consumer message ---------------");
        System.out.println("consumerTag: " + consumerTag);
        System.out.println("envelope: " + envelope);
        System.out.println("properties: " + properties);
        System.out.println("body: " + new String(body));

        eTagList.add(envelope.getDeliveryTag());


    }

    public void  sendACK(){
        if(eTagList.size()>0){
            System.out.println("正在签收消息......");
            eTagList.forEach(e-> {
                try {
                    channel.basicAck(e, false);
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            });
            eTagList.clear();
            System.out.println("签收成功........");
        }

    }
}
```

### Consuemr

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Consumer;
import org.springframework.amqp.core.ExchangeTypes;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class LimitConsumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        LimitCustomerConsumer consumer = new LimitCustomerConsumer(channel);
        Thread thread = new Thread(()->{
            while (true){
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                consumer.sendACK();
            }
        });
        thread.setDaemon(true);

        String exchangeName = "test_qos_exchange";
        String queueName = "qos_queue";
        String routingKey = "qos_save";
        channel.exchangeDeclare(exchangeName, ExchangeTypes.FANOUT, false, false, null);
        channel.queueDeclare(queueName, false, false, false, null);
        channel.queueBind(queueName, exchangeName, routingKey);

        // 1. autoAck 设置为false
        // 2. channel 设置限流策略
        channel.basicQos(0, 3, false);
        channel.basicConsume(queueName, false, consumer);
        thread.start();


    }
}
```

### producer

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class LimitProducer {

    public static void main(String[] args) throws IOException, TimeoutException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        // 指定消息的确认模式
        channel.confirmSelect();

        String exchangeName = "test_qos_exchange";
        String routingKey = "qos_save";
        for(int i=0;i<10000;i++){
            String msg = "Hello RabbitMQ send QOS message From " + i;
            channel.basicPublish(exchangeName, routingKey, null, msg.getBytes());
        }


        // 关闭连接，线程会退出，否则不会主动退出
         channel.close();
         connection.close();

    }

}
```

## 消息的ACK与重回队列

### ACK

* 消费端的手工ACK和NACK
  * ACK 消费成功
  * NACK 消费失败，重回队列
* 消费端进行消费的时候，如果由于业务异常我们可以进行日志的记录，然后进行补偿
* 如果由于服务器宕机等严重问题，那我们就需要手工进行ACK保障消费端消费成功！

### 重回队列

* 消费端重回队列是为了对没有处理成功的消息，把消息重新会递给Broker！
* 一般我们在实际应用中，都会关闭重回队列，也就是设置为false

### 自定义消费者

```java
import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;

import java.io.IOException;
import java.util.List;
import java.util.Vector;

public class MyACKConsumer extends DefaultConsumer {
    private Channel channel;
    private int zeroTime = 0;
    public MyACKConsumer(Channel channel) {
        super(channel);
        this.channel = channel;
    }


    /**
     *
     * @param consumerTag 消费标签
     * @param envelope 环境变量
     * @param properties properties
     * @param body 消息内容
     * @throws IOException 可能抛出的异常
     */
    @Override
    public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {

        System.out.println("------------- consumer message ---------------");
        System.out.println("body: " + new String(body));
        if((int)properties.getHeaders().get("num")==0&&zeroTime<10){
            zeroTime += 1;
            channel.basicNack(envelope.getDeliveryTag(), false, true);

        }else {
            channel.basicAck(envelope.getDeliveryTag(), false);
        }

    }


}
```

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

public class ACKProducer {

    public static void main(String[] args) throws IOException, TimeoutException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        // 指定消息的确认模式
        channel.confirmSelect();

        String exchangeName = "test_ack_exchange";
        String routingKey = "ack_save";
        for(int i=0;i<10;i++){
            Map<String, Object> headers = new HashMap<>();
            headers.put("num", i);

            String msg = "Hello RabbitMQ send ACK message From " + i;
            AMQP.BasicProperties properties = new AMQP.BasicProperties.Builder()
                    .deliveryMode(JmsProperties.DeliveryMode.PERSISTENT.getValue())
                    .contentEncoding("UTF-8")
                    .headers(headers)
                    .build();

            channel.basicPublish(exchangeName, routingKey, properties, msg.getBytes());
        }


        // 关闭连接，线程会退出，否则不会主动退出
         channel.close();
         connection.close();

    }

}

```

### 客户端

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.springframework.amqp.core.ExchangeTypes;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class ACKConsumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        MyACKConsumer consumer = new MyACKConsumer(channel);


        String exchangeName = "test_ack_exchange";
        String queueName = "ack_queue";
        String routingKey = "ack_save";
        channel.exchangeDeclare(exchangeName, ExchangeTypes.FANOUT, false, false, null);
        channel.queueDeclare(queueName, false, false, false, null);
        channel.queueBind(queueName, exchangeName, routingKey);

        // 1. autoAck 设置为false
        channel.basicConsume(queueName, false, consumer);


    }
}
```

## TTL消息

* TTL 是Time to Live的缩写，也就是生存时间
* RabbitMQ 支持消息的过期时间，在消息发送时可以指定
* RabbitMQ支持队列的过期时间，从消息入队列开始计算，只要超过队列的超时时间配置，那么消息会自动清除

### 声明代码

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.springframework.amqp.core.ExchangeTypes;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeoutException;

public class ACKConsumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        MyACKConsumer consumer = new MyACKConsumer(channel);

        Map<String, Object> arguments = new HashMap<>();
        arguments.put("x-message-ttl", 10000);
        arguments.put("x-max-length", 3000);
        String exchangeName = "test_ttl_exchange";
        String queueName = "ttl_queue";
        String routingKey = "ttl_save";
        channel.exchangeDeclare(exchangeName, ExchangeTypes.FANOUT, false, false, null);
        channel.queueDeclare(queueName, false, false, false, arguments);
        channel.queueBind(queueName, exchangeName, routingKey);

        // 1. autoAck 设置为false
        channel.basicConsume(queueName, false, consumer);


    }
}

```



## 死信队列(DLX)

* 利用DLX， 当消息在一个队列中变成死信(dead message)之后，它能重新publish到另一个Exchange，这个Exchange就是DLX

消息如何变成死信

* 消息被拒绝(basic.reject/basic.nack)并且requeue=false
* 消息TTL过期

### 特性

* DLX 也是一个正常的Exchange, 和一般的Exchange没有区别，它能在任何的队列上被指定，实际上就是设置队列的某个属性
* 当这个队列中，有死信时，RabbitMQ就会被自动的将这个消息重新发布到设置的Exchange上去，进而被路由到另一个队列
* 可以监听这个队列中消息做相应的处理，这个特性可以弥补RabbitMQ3.0以前支持的immediate参数的功能

### 如何设置死信队列

* 首先需要设置死信队列的exchange和queue，然后进行绑定
  * Exchange: dlx.exchange
  * Queue: dlx.queue
  * RoutingKey: #
* 然后正常声明一个交换机，队列、绑定。只不过我们需要在队列加上一个参数即可： arguments.put("x-dead-letter-exchange", "dlx.exchange")

* 这样我们的消息在过期、requeue、队列达到最大长度时，消息就可以被路由到死信队列！

### 自定消费者

```java
package org.ning.demo.dlx;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;

import java.io.IOException;

public class DLXCustomerConsumer extends DefaultConsumer {
    public DLXCustomerConsumer(Channel channel) {
        super(channel);
    }

    /**
     *
     * @param consumerTag 消费标签
     * @param envelope 环境变量
     * @param properties properties
     * @param body 消息内容
     * @throws IOException 可能抛出的异常
     */
    @Override
    public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {

        System.out.println("------------- consumer message ---------------");
        System.out.println("consumerTag: " + consumerTag);
        System.out.println("envelope: " + envelope);
        System.out.println("properties: " + properties);
        System.out.println("body: " + new String(body));

    }
}

```



### 客户端

```java
package org.ning.demo.dlx;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.springframework.amqp.core.ExchangeTypes;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeoutException;

public class DLXConsumer {

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        //1. 声明一个普通的队列和交换机
        String exchangeName = "test_dlx_exchange";
        String queueName = "dlx_queue";
        String routingKey = "dlx.save";

        //2. 设置死信队列属性,必须放在queue中
        Map<String, Object> arguments = new HashMap<>();
        arguments.put("x-dead-letter-exchange", "dlx.exchange");
        channel.exchangeDeclare(exchangeName, ExchangeTypes.FANOUT, false, false, null);
        channel.queueDeclare(queueName, true, false, false, arguments);
        channel.queueBind(queueName, exchangeName, routingKey);

        // 3. 声明死信队列
        channel.exchangeDeclare("dlx.exchange", ExchangeTypes.TOPIC, true,false, null);
        channel.queueDeclare("dlx.queque", true, false, false, null);
        channel.queueBind("dlx.queque", "dlx.exchange", "#");




        channel.basicConsume(queueName, true, new DLXCustomerConsumer(channel));


    }
}

```

### 生产者

```java
package org.ning.demo.dlx;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.springframework.boot.autoconfigure.jms.JmsProperties;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class DLXProducer {

    public static void main(String[] args) throws IOException, TimeoutException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.1.48");
        connectionFactory.setPort(5672);
        connectionFactory.setVirtualHost("/");

        Connection connection = connectionFactory.newConnection();

        Channel channel = connection.createChannel();

        // 指定消息的确认模式
        channel.confirmSelect();

        // 设置过期时间，测试死信队列
        AMQP.BasicProperties properties = new AMQP.BasicProperties.Builder()
                .deliveryMode(JmsProperties.DeliveryMode.PERSISTENT.getValue())
                .expiration("10000")
                .contentEncoding("UTF-8")
                .build();

        String exchangeName = "test_dlx_exchange";
        String routingKey = "dlx.save";
        for(int i=0;i<10;i++){
            String msg = "Hello RabbitMQ send DLX message From " + i;
            channel.basicPublish(exchangeName, routingKey, properties, msg.getBytes());
        }


        // 关闭连接，线程会退出，否则不会主动退出
         channel.close();
         connection.close();

    }

}

```