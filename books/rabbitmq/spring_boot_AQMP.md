Spring Boot + AQMP
-----

## POM 依赖

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.6.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>org.ning</groupId>
    <artifactId>rabbitmq_spring_boot</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>rabbitmq_spring_boot</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-amqp</artifactId>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>org.springframework.amqp</groupId>
            <artifactId>spring-rabbit-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

## application

```java
spring:
  rabbitmq:
    addresses: 192.168.1.48:5672
    username: guest
    password: guest
    virtual-host: /
    connection-timeout: 15000
    # 实现一个监听器，用户监听Broker端给我们返回的确认请求(RabbitTemplate.ConfirmCallback)
    publisher-confirm-type: correlated
    # 保证消息对Broker端时可达的，如果出现路由键不可达的情况，则使用监听器对不可达的消息进行后续处理，保证消息的路由成功
    # RabbitTemplate.ReturnCallback
    publisher-returns: true
    template:
      # 必须设置该属性，保证消息不被删除才能后保证监听有效
      mandatory: true

    # 消费端设置
    listener:
      simple:
        # 签收模式
        acknowledge-mode: manual
        # 限流策略
        prefetch: 10
        concurrency: 5
        max-concurrency: 10

consumer:
  exchange: exchange-2
  queue: queue-2
  routingKey: springboot.#
```

### 生产者

```java
package org.ning.rabbitmq_spring_boot.producer;


import org.ning.rabbitmq_spring_boot.entity.Order;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageProperties;
import org.springframework.amqp.rabbit.connection.CorrelationData;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;


import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.UUID;

/**
 * @author WangNing
 * @version 1.0
 * @date 2020/4/29 15:04
 */
@Component
public class RabbitSender implements RabbitTemplate.ConfirmCallback , RabbitTemplate.ReturnCallback {


    static private final String EXCHANGE = "exchange-1";

    static private final String ROUTE_KEY = "springboot.hello";

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void send(byte[] rawMessage, MessageProperties properties) throws Exception {

        Message message = new Message(rawMessage, properties);
        CorrelationData correlationData = new CorrelationData();
        correlationData.setId(UUID.randomUUID().toString());
        rabbitTemplate.convertAndSend(EXCHANGE, ROUTE_KEY, message, correlationData);
        rabbitTemplate.setConfirmCallback(this);
        rabbitTemplate.setReturnCallback(this);
    }

    public void send(byte[] rawMessage, Map<String, Object> headers) throws Exception {
        MessageProperties properties = new MessageProperties();
        headers.forEach(properties::setHeader);
        send(rawMessage, properties);
    }


    @Value("${consumer.exchange}")
    private String exchange2;

    public void sendOrder(Order order) throws Exception {

        CorrelationData correlationData = new CorrelationData();
        correlationData.setId(UUID.randomUUID().toString());
        rabbitTemplate.convertAndSend(exchange2, "springboot.222", order);
        rabbitTemplate.setConfirmCallback(this);
        rabbitTemplate.setReturnCallback(this);
    }

    // 确认消息, 监听器
    @Override
    public void confirm(CorrelationData correlationData, boolean ack, String cause) {
        System.out.println("############## Confirm ##############");
        System.out.println("CorrelationData: "+correlationData);
        System.out.println("cause: "+cause);
        System.out.println("ACK: "+ack);
        if(!ack){
            System.out.println("  NACK 异常处理");
        }
    }

    // 消息不可达, 监听器
    @Override
    public void returnedMessage(org.springframework.amqp.core.Message message, int replyCode, String replyText, String exchange, String routingKey) {
        System.out.println("############## Return ##############");
        System.out.println("return exchange:  "+ exchange);
        System.out.println("return routingKey: "+ routingKey);
        System.out.println("return messageBody: "+ new String(message.getBody()));
        System.out.println("return replyCode: "+ replyCode);
        System.out.println("return replyText: "+ replyText);
    }

}

```

### 消费者

```java
@Component

public class RabbitMQReceiver {


    @RabbitListener(bindings = {@QueueBinding(
            value = @Queue(value = "queue-1", durable = "true", exclusive = "false", autoDelete = "false"),
            exchange = @Exchange(value = "exchange-1", durable = "true", type = "topic", autoDelete = "false"),
            key = "springboot.#"
    )})
    @RabbitHandler
    public void onMessage(Message message, Channel channel) throws Exception{
        System.out.println("------------------ Consumer(rawMessage) -----------------");
        System.out.println("消费端：" + new String(message.getBody()));
        long tag = message.getMessageProperties().getDeliveryTag();
        channel.basicAck(tag, true);
    }


    @RabbitListener(bindings = {@QueueBinding(
            value = @Queue(value = "${consumer.queue}", durable = "true", exclusive = "false", autoDelete = "false", ignoreDeclarationExceptions = "true"),
            exchange = @Exchange(value = "${consumer.exchange}", durable = "true", type = "topic", autoDelete = "false", ignoreDeclarationExceptions = "true"),
            key = "${consumer.routingKey}"
    )})
    @RabbitHandler
    public void onMessage(@Payload Order order, Channel channel, @Headers Map<String , Object> headers) throws Exception{
        System.out.println("------------------ Consumer(Order) -----------------");
        System.out.println("消费端：" +order);
        long tag = (long)headers.get(AmqpHeaders.DELIVERY_TAG);
        channel.basicAck(tag, true);
    }

}
```