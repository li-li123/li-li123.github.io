RabbitMQ with Spring 
--------------

##  整合Spring

spring 底层会自动扫描注入的Exchange、Queue和Binding。所以声明绑定、队列和交换机、只需要简短的注入Bean就可以了

### maven 依赖

```xml
<!-- https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-amqp -->
<dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-amqp</artifactId>
       <version>1.4.7.RELEASE</version>
</dependency>
```

### 注入Bean

```java
package org.ning.rabbitmq_spring.config;


import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.connection.CachingConnectionFactory;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitAdmin;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

/**
 * @author WangNing
 * @version 1.0
 * @date 2020/4/28 21:04
 */

@Configuration
public class RabbitMQConfig {

    @Bean
    public ConnectionFactory connectionFactory(){
        CachingConnectionFactory connectionFactory = new CachingConnectionFactory();
        connectionFactory.setAddresses("192.168.1.48:5672");
        connectionFactory.setUsername("guest");
        connectionFactory.setPassword("guest");
        connectionFactory.setVirtualHost("/");
        return connectionFactory;
    }

    @Bean
    public RabbitAdmin rabbitAdmin(ConnectionFactory connectionFactory){
        RabbitAdmin rabbitAdmin = new RabbitAdmin(connectionFactory);
        rabbitAdmin.setAutoStartup(true);
        return rabbitAdmin;
    }

    @Bean
    public RabbitTemplate rabbitTemplate(){
        RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory());
        return rabbitTemplate;
    }

    @Bean
    public TopicExchange exchange1(){
        return new TopicExchange("topic001", false, true);
    }

    @Bean
    public Queue queue1(){
        return new Queue("topic_001_queue", false);
    }

    @Bean
    public Binding binding1(){
        return  BindingBuilder.bind(queue1()).to(exchange1()).with("#");
    }

}

```

### Rabbit Admin简单使用

```java
package org.ning.rabbitmq_spring;

import com.rabbitmq.client.AMQP;
import org.junit.jupiter.api.Test;
import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.core.RabbitAdmin;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.HashMap;

@SpringBootTest
class RabbitmqSpringApplicationTests {

    @Autowired
    RabbitAdmin rabbitAdmin;

    @Test
    void contextLoads() {

        System.out.println(rabbitAdmin.getQueueInfo("dlx_queue"));
        // 声明交换机
        rabbitAdmin.declareExchange(new DirectExchange("test.direct", false, false));
        rabbitAdmin.declareExchange(new TopicExchange("test.topic", false, false));
        rabbitAdmin.declareExchange(new FanoutExchange("test.fanout", false, false));

        // 声明队列
        rabbitAdmin.declareQueue(new Queue("test.direct.queue", false));
        rabbitAdmin.declareQueue(new Queue("test.topic.queue", false));
        rabbitAdmin.declareQueue(new Queue("test.fanout.queue", false));

        // 绑定
        rabbitAdmin.declareBinding(new Binding("test.direct.queue",
                Binding.DestinationType.QUEUE, "test.direct", "direct", new HashMap<>()));
        rabbitAdmin.declareBinding(
                BindingBuilder
                        .bind(new Queue("test.topic.queue", false)) // 直接创建队列
                        .to(new TopicExchange("test.topic", false, false)) // 直接创建交换机
                        .with("#") // 设置绑定的Key

        );
        rabbitAdmin.declareBinding(BindingBuilder
                .bind(new Queue("test.fanout.queue", false)) // 直接创建队列
                .to(new FanoutExchange("test.fanout", false, false)) // 直接创建交换机
        );
        
        //清空队列
        rabbitAdmin.purgeQueue("test.topic.queue");
    }

}

```

### RabbitTemplate 发送消息

```java
@Autowired
    RabbitTemplate rabbitTemplate;

@Test
public void testSendMessage() throws Exception{
    MessageProperties properties = new MessageProperties();
        properties.getHeaders().put("desc", "信息描述:");
        properties.getHeaders().put("type", "信息类型:");

        Message message = new Message("Hello RabbitMQ".getBytes(), properties);

        rabbitTemplate.convertAndSend("test.direct", "direct", message, new MessagePostProcessor() {
            @Override
            public Message postProcessMessage(Message message) throws AmqpException {
                System.out.println("----------------添加额外设置-----------------");
                message.getMessageProperties().getHeaders().put("desc", "信息描述: + edit");
                message.getMessageProperties().getHeaders().put("attr", "额外设置");
                return message;
            }
        });

        rabbitTemplate.convertAndSend("test.direct", "direct", "hello this is simple message!");

        rabbitTemplate.send("test.direct","direct", message);
}
```

## SimpleMessageListenerContainer

**简单消息监听容器**

* 这个类非常强大，我们可以对他进行很多设置，对于消费者的配置项，这个类都可以满足
* 监听队列(多个队列)、自动启动、自动声明的功能
* 设置事务特性、事务管理器、事务属性、事务容量、是否开启事务、回滚消息
* 设置消费者数量，最大最小数量、批量消费

* 设置消息确认和自动确认模式、是否重回队列，异常捕获handler函数
* 设置消费者标签生成策略，是否独占模式、消费者属性等
* 设置具体的监听器和消息转化器等等

**注意: SimpleMessageListenerContainer可以进行动态设置，比如在运行中的应用可以动态的修改消费者数量的大小，接受消息的模式等**

**很多基于RabbitMQ的自制定制化后端管控台在进行动态设置的时候，也是根据这一特性去实现的。所以可以看出SpringAMQP非常强大**

**SimpleMessageListenerContainer为什么可以动态感知配置变更**

```java
@Bean
public SimpleMessageListenerContainer simpleMessageListenerContainer() {
    SimpleMessageListenerContainer container = new SimpleMessageListenerContainer(connectionFactory());
    container.setQueues(queue1());
    // 设置初始消费者数量
    container.setConcurrentConsumers(1);
    // 设置最大消费者数量
    container.setMaxConcurrentConsumers(5);
    // 设置是否重回模式
    container.setDefaultRequeueRejected(false);
    // 设置消息签收模式
    container.setAcknowledgeMode(AcknowledgeMode.AUTO);
    // 设置消费者标签生成策略(用于识别消费者)
    container.setConsumerTagStrategy(new ConsumerTagStrategy() {
        @Override
        public String createConsumerTag(String queue) {
            return queue + "_" + UUID.randomUUID().toString();
        }
    });
    // 设置消息的监听器
    container.setMessageListener(new ChannelAwareMessageListener() {
        @Override
        public void onMessage(Message message, Channel channel) throws Exception {
            String msg = new String(message.getBody());
            System.out.println("-----------------消费者: "+msg);

        }
    });
    return container;
}
```

## MessageListenerAdapter

### 消息适配器处理消息

**具体处理方法类**

```java
public class MessageDelegate {

    public void handleMessage(byte[] messageBody){
        System.out.println("默认方法, 消息内容:" + new String(messageBody));
    }

    public void handleMessage(String messageBody){
        System.out.println("String方法, 消息内容:" + messageBody);
    }

    public void queue001(byte[] messageBody){
        System.out.println("Queue001(byte), 消息内容:" + new String(messageBody));
    }

    public void queue001(String messageBody){
        System.out.println("Queue001(String), 消息内容:" + messageBody);
    }
}
```

**添加消息适配器**

```java
@Bean
    public SimpleMessageListenerContainer simpleMessageListenerContainer() {
        SimpleMessageListenerContainer container = new SimpleMessageListenerContainer(connectionFactory());
        container.setQueues(queue1());
        // 设置初始消费者数量
        container.setConcurrentConsumers(1);
        // 设置最大消费者数量
        container.setMaxConcurrentConsumers(5);
        // 设置是否重回模式
        container.setDefaultRequeueRejected(false);
        // 设置消息签收模式
        container.setAcknowledgeMode(AcknowledgeMode.AUTO);
        // 设置消费标签生成策略
        container.setConsumerTagStrategy(new ConsumerTagStrategy() {
            @Override
            public String createConsumerTag(String queue) {
                return queue + "_" + UUID.randomUUID().toString();
            }
        });
        // 设置消息的监听器
//        container.setMessageListener(new ChannelAwareMessageListener() {
//            @Override
//            public void onMessage(Message message, Channel channel) throws Exception {
//                String msg = new String(message.getBody());
//                System.out.println("-----------------消费者: "+msg);
//
//            }
//        });
        // 设置消息适配器
        MessageListenerAdapter adapter = new MessageListenerAdapter(new MessageDelegate() , "handleMessage");

        adapter.setMessageConverter(new TextMessageConvert());
        // 根据queue名指定方法名
        Map<String, String> map = new HashMap<>();
        map.put("topic_001_queue", "queue001");
        adapter.setQueueOrTagToMethodName(map);
        container.setMessageListener(adapter);

        return container;
    }
```

## 消息转换器

常用的转换器

* Json转换器 Jackson2JsonMessageConverter： 可以进行java对象的转换功能
* DefaultJack2JavaTypeMapper: 可以进行java对象的映射关系
* 自定义2进制转换器:

```java
public class TextMessageConvert implements MessageConverter {
	
    // java 转换 Message
    @Override
    public Message toMessage(Object object, MessageProperties messageProperties) throws MessageConversionException {
        return new Message(object.toString().getBytes(), messageProperties);
    }

    // Message to java
    @Override
    public Object fromMessage(Message message) throws MessageConversionException {
        String contentType = message.getMessageProperties().getContentType();
        if(null!= contentType&&contentType.contains("text")){
            return new String(message.getBody());
        }
        return message.getBody();
    }
}
```

```java
@Bean
    public SimpleMessageListenerContainer simpleMessageListenerContainer() {
        SimpleMessageListenerContainer container = new SimpleMessageListenerContainer(connectionFactory());
        container.setQueues(queue1());
        // 设置初始消费者数量
        container.setConcurrentConsumers(1);
        // 设置最大消费者数量
        container.setMaxConcurrentConsumers(5);
        // 设置是否重回模式
        container.setDefaultRequeueRejected(false);
        // 设置消息签收模式
        container.setAcknowledgeMode(AcknowledgeMode.AUTO);
        // 设置消费标签生成策略
        container.setConsumerTagStrategy(new ConsumerTagStrategy() {
            @Override
            public String createConsumerTag(String queue) {
                return queue + "_" + UUID.randomUUID().toString();
            }
        });
        // 设置消息的监听器
//        container.setMessageListener(new ChannelAwareMessageListener() {
//            @Override
//            public void onMessage(Message message, Channel channel) throws Exception {
//                String msg = new String(message.getBody());
//                System.out.println("-----------------消费者: "+msg);
//
//            }
//        });
        // 设置消息适配器
        MessageListenerAdapter adapter = new MessageListenerAdapter(new MessageDelegate() , "handleMessage");
        // 自定义消息转换
//        adapter.setMessageConverter(new TextMessageConvert());
        // json 对象转换
        Jackson2JsonMessageConverter jackson2JsonMessageConverter = new Jackson2JsonMessageConverter();

        DefaultJackson2JavaTypeMapper jackson2JavaTypeMapper = new DefaultJackson2JavaTypeMapper();
        // 设置可以映射成对象
        jackson2JavaTypeMapper.addTrustedPackages("org.ning.rabbitmq_spring.bean");
        jackson2JsonMessageConverter.setJavaTypeMapper(jackson2JavaTypeMapper);


        adapter.setMessageConverter(jackson2JsonMessageConverter);

        // 根据queue名指定方法名
        Map<String, String> map = new HashMap<>();
        adapter.setQueueOrTagToMethodName(map);
        container.setMessageListener(adapter);

        return container;
    }
```

### Json 转换器

**测试方法**

```java
@Test
    public void testSendMessage() throws Exception{
        MessageProperties properties = new MessageProperties();
        properties.getHeaders().put("desc", "信息描述:");
        properties.getHeaders().put("type", "信息类型:");
        properties.setContentType("text");

        Message message = new Message("Hello RabbitMQ".getBytes(), properties);

        rabbitTemplate.convertAndSend("test.direct", "direct", message, new MessagePostProcessor() {
            @Override
            public Message postProcessMessage(Message message) throws AmqpException {
                System.out.println("----------------添加额外设置-----------------");
                message.getMessageProperties().getHeaders().put("desc", "信息描述: + edit");
                message.getMessageProperties().getHeaders().put("attr", "额外设置");
                return message;
            }
        });

        rabbitTemplate.convertAndSend("test.direct", "direct", "hello this is simple message!");

        rabbitTemplate.send("test.direct","direct", message);

    }

    @Test
    public void testJson() throws JsonProcessingException {
        Order order = new Order();
        order.setDescription("lalalala");
        order.setName("heiheihei");
        order.setId(12);
        ObjectMapper mapper = new ObjectMapper();
        String json = mapper.writeValueAsString(order);
        System.out.println("json string is "+json);
        MessageProperties properties = new MessageProperties();
        properties.setContentType("application/json");
        rabbitTemplate.send("topic001", "topic_001_queue", new Message(json.getBytes(), properties));
    }
```

### 全局转换器

```java
@Bean
    public SimpleMessageListenerContainer simpleMessageListenerContainer() {
        SimpleMessageListenerContainer container = new SimpleMessageListenerContainer(connectionFactory());
        container.setQueues(queue1());
        // 设置初始消费者数量
        container.setConcurrentConsumers(1);
        // 设置最大消费者数量
        container.setMaxConcurrentConsumers(5);
        // 设置是否重回模式
        container.setDefaultRequeueRejected(false);
        // 设置消息签收模式
        container.setAcknowledgeMode(AcknowledgeMode.AUTO);
        // 设置消费标签生成策略
        container.setConsumerTagStrategy(new ConsumerTagStrategy() {
            @Override
            public String createConsumerTag(String queue) {
                return queue + "_" + UUID.randomUUID().toString();
            }
        });

        // 设置消息适配器
        MessageListenerAdapter adapter = new MessageListenerAdapter(new MessageDelegate() , "handleMessage");

        ContentTypeDelegatingMessageConverter contentTypeDelegatingMessageConverter = new ContentTypeDelegatingMessageConverter();
        
        // json 对象转换
        Jackson2JsonMessageConverter jackson2JsonMessageConverter = new Jackson2JsonMessageConverter();

        DefaultJackson2JavaTypeMapper jackson2JavaTypeMapper = new DefaultJackson2JavaTypeMapper();
        // 设置可以映射成对象
        jackson2JavaTypeMapper.addTrustedPackages("org.ning.rabbitmq_spring.bean");
        jackson2JsonMessageConverter.setJavaTypeMapper(jackson2JavaTypeMapper);

        contentTypeDelegatingMessageConverter.addDelegate("application/json", jackson2JsonMessageConverter);
        contentTypeDelegatingMessageConverter.addDelegate("html/text", new TextMessageConvert());
        adapter.setMessageConverter(contentTypeDelegatingMessageConverter);

        // 根据queue名指定方法名
        Map<String, String> map = new HashMap<>();
        adapter.setQueueOrTagToMethodName(map);
        container.setMessageListener(adapter);

        return container;
    }
```