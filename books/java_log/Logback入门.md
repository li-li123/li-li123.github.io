Logback是由log4j创始人设计的另一个开源日志组件，性能比log4j要好。

官方网址: https://logback.qos.ch/index.html



Logback主要分为三个模块：

* logback-core：其它两个模块的基础模块
* logback-classic：它是log4j的一个改良版本，同时它完整实现了slf4j API
* logback-access：访问模块与Servlet容器集成提供通过Http来访问日志的功能



后续的日志代码都是通过SLF4J日志门面搭建日志系统，所以在代码是没有区别，主要是通过修改配置文件和 `pom.xml` 依赖



1. 添加依赖

```xml
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-api</artifactId>
    <version>1.7.25</version>
</dependency>

<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.2.3</version>
</dependency>
```

2. java 代码

```java
//  定义日志对象
public final static Logger LOGGER = LoggerFactory.getLogger(LogBackTest.class);

@Test
public void testSlf4j(){
    //  打印日志信息
    LOGGER.error("error");
    LOGGER.warn("warn");
    LOGGER.info("info");
    LOGGER.debug("debug");
    LOGGER.trace("trace");
}
```

