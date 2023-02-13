logback会依次读取以下类型配置文件：

* logback.groovy
* logback-test.xml
* logback.xml 如果均不存在会采用默认配置



1. logback组件之间的关系
   1. `Logger`: 日志的记录器，把它关联到应用的对应的context上后，主要用于存放日志对象，也
     可以定义日志类型、级别。
   2. `Appender`: 用于指定日志输出的目的地，目的地可以是控制台、文件、数据库等等。
   3. `Layout`: 负责把事件转换成字符串，格式化的日志信息的输出。在 `logback` 中 `Layout` 对象被封
     装在 `encoder` 中。

2. 基本配置信息

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>

    <!--
        配置集中管理属性
        我们可以直接改属性的 value 值
        格式：${name}
    -->
    
    <property name="pattern" value="[%-5level] %d{yyyy-MM-dd HH:mm:ss.SSS} %c %M %L [%thread] %m%n">
    </property>
    <!--
    日志输出格式：
        %-5level
        %d{yyyy-MM-dd HH:mm:ss.SSS}日期
        %c类的完整名称
        %M为method
        %L为行号
        %thread线程名称
        %m或者%msg为信息
        %n换行
      -->
    <!--定义日志文件保存路径属性-->
    <property name="log_dir" value="/logs"></property>


    <!--控制台日志输出的 appender-->
    <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
        <!--控制输出流对象 默认 System.out 改为 System.err-->
        <target>System.err</target>
        <!--日志消息格式配置-->
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <pattern>${pattern}</pattern>
        </encoder>
    </appender>

    <!--日志文件输出的 appender-->
    <appender name="file" class="ch.qos.logback.core.FileAppender">
        <!--日志文件保存路径-->
        <file>${log_dir}/logback.log</file>
        <!--日志消息格式配置-->
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <pattern>${pattern}</pattern>
        </encoder>
    </appender>

    <!--html 格式日志文件输出 appender-->
    <appender name="htmlFile" class="ch.qos.logback.core.FileAppender">
        <!--日志文件保存路径-->
        <file>${log_dir}/logback.html</file>
        <!--html 消息格式配置-->
        <encoder class="ch.qos.logback.core.encoder.LayoutWrappingEncoder">
            <layout class="ch.qos.logback.classic.html.HTMLLayout">
                <pattern>%-5level%d{yyyy-MM-dd HH:mm:ss.SSS}%c%M%L%thread%m</pattern>
            </layout>
        </encoder>
    </appender>


    <!--日志拆分和归档压缩的 appender 对象-->
    <appender name="rollFile" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!--日志文件保存路径-->
        <file>${log_dir}/roll_logback.log</file>
        <!--日志消息格式配置-->
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <pattern>${pattern}</pattern>
        </encoder>
        <!--指定拆分规则-->
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <!--按照时间和压缩格式声明拆分的文件名-->
            <fileNamePattern>${log_dir}/rolling.%d{yyyy-MM-dd}.log%i.gz</fileNamePattern>
            <!--按照文件大小拆分-->
            <maxFileSize>1MB</maxFileSize>
        </rollingPolicy>
        <!--日志级别过滤器-->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <!--日志过滤规则-->
            <level>ERROR</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <!--异步日志-->
    <appender name="async" class="ch.qos.logback.classic.AsyncAppender">
        <!--指定某个具体的 appender-->
        <appender-ref ref="rollFile"/>
    </appender>


    <!--root logger 配置-->
    <root level="ALL">
        <appender-ref ref="console"/>
        <appender-ref ref="async"/>
    </root>

    <!--自定义 looger 对象
        additivity="false" 自定义 logger 对象是否继承 rootLogger
     -->
    <logger name="com.itheima" level="info" additivity="false">
        <appender-ref ref="console"/>
    </logger>
    
</configuration>
```

