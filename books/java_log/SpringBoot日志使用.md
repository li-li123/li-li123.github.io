## 简单使用

```java
@SpringBootTest
class SpringbootLogApplicationTests {
    //记录器
    public static final Logger LOGGER = LoggerFactory.getLogger(SpringbootLogApplicationTests.class);
    
    @Test
    public void contextLoads() {
        // 打印日志信息
        LOGGER.error("error");
        LOGGER.warn("warn");
        LOGGER.info("info");  // 默认日志级别
        LOGGER.debug("debug");
        LOGGER.trace("trace");
     }
}
```

## 日志配置

```properties
logging.level.com.itheima=trace
# 在控制台输出的日志的格式 同logback

logging.pattern.console=%d{yyyy-MM-dd} [%thread] [%-5level] %logger{50} - %msg%n
# 指定文件中日志输出的格式

logging.file=D:/logs/springboot.log
logging.pattern.file=%d{yyyy-MM-dd} [%thread] %-5level %logger{50} - %msg%n
```

指定配置, 在类路径下放上每个日志框架自己的配置文件；SpringBoot就不使用默认配置的了

| 日志框架 | 配置文件                         |
| -------- | -------------------------------- |
| Logback  | logback-spring.xml , logback.xml |
| Log4j2   | log4j2-spring.xml ， log4j2.xml  |
| JUL      | logging.properties               |

> logback.xml：直接就被日志框架识别了

----

<center>将日志切换为log4j2</center>

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    
    <exclusions>
        <!--排除logback-->
        <exclusion>
            <artifactId>spring-boot-starter-logging</artifactId>
            <groupId>org.springframework.boot</groupId>
    	</exclusion>
    </exclusions>
    
</dependency>

<!-- 添加log4j2 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-log4j2</artifactId>
</dependency>  
```

