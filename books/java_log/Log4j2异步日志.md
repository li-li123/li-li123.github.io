log4j2 最大的特点就是异步日志，其性能的提升主要也是从异步日志中受益，我们来看看如何使用 log4j2 的异步日志。

<center>同步日志</center>

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210302204706050.png" alt="image-20210302204706050"  /></center>

---

<center>异步日志</center>

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210302204751315.png" alt="image-20210302204751315"  /></center>

Log4j2提供了两种实现日志的方式，一个是通过AsyncAppender，一个是通过AsyncLogger，分别对应前面我们说的Appender组件和Logger组件。

>  注意：配置异步日志需要添加依赖
>
> ```xml
> <!--异步日志依赖-->
> <dependency>
>     <groupId>com.lmax</groupId>
>     <artifactId>disruptor</artifactId>
>     <version>3.3.4</version>
> </dependency>
> ```

1.  `Appender` 组件方式

```xml
<?xml version="1.0" encoding="UTF-8"?>

<Configuration status="debug" monitorInterval="5">


    <properties>
        <property name="LOG_HOME">/logs</property>
    </properties>


    <Appenders>
        <!--日志文件输出 appender-->
        <File name="file" fileName="${LOG_HOME}/myfile.log">
            <PatternLayout pattern="[%d{yyyy-MM-dd HH:mm:ss.SSS}] [%-5level] %l %c{36} - %m%n" />
        </File>
        <Async name="Async">
            <AppenderRef ref="file"/>
        </Async>
    </Appenders>
    

    <Loggers>
        <Root level="trace">
            <!--使用异步 appender-->
            <AppenderRef ref="Async" />
        </Root>
    </Loggers>
        
 </Configuration>
```

2. AsyncLogger方式

AsyncLogger才是log4j2 的重头戏，也是官方推荐的异步方式。它可以使得调用Logger.log返回的更快。你可以有两种选择：全局异步和混合异步。

* 全局异步就是，所有的日志都异步的记录，在配置文件上不用做任何改动，只需要添加一个`log4j2.component.properties`  配置；

  ```properties
  Log4jContextSelector=org.apache.logging.log4j.core.async.AsyncLoggerContextSelector
  ```

* 混合异步就是，你可以在应用中同时使用同步日志和异步日志，这使得日志的配置方式更加灵活。

```xml
<?xml version="1.0" encoding="UTF-8"?>

<Configuration status="debug" monitorInterval="5">


    <properties>
        <property name="LOG_HOME">/logs</property>
    </properties>


    <Appenders>
        <!--日志文件输出 appender-->
        <File name="file" fileName="${LOG_HOME}/myfile.log">
            <PatternLayout pattern="[%d{yyyy-MM-dd HH:mm:ss.SSS}] [%-5level] %l %c{36} - %m%n" />
        </File>
        <Async name="Async">
            <AppenderRef ref="file"/>
        </Async>
    </Appenders>
    

    <Loggers>
        
        <AsyncLogger name="com.itheima" level="trace" includeLocation="false" additivity="false">
            <AppenderRef ref="Console"/>
        </AsyncLogger>
        
        <Root level="trace">
           <AppenderRef ref="file"/>
        </Root>
        
    </Loggers>
        
 </Configuration>
```

如上配置： `com.itheima` 日志是异步的，`root` 日志是同步的。



使用异步日志需要注意的问题：
1. 如果使用异步日志，**AsyncAppender、AsyncLogger和全局日志，不要同时出现**。性能会和 AsyncAppender 一致，降至最低。
2. 设置 includeLocation=false ，打印位置信息会急剧降低异步日志的性能，比同步日志还要慢