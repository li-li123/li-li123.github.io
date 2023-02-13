Log4J 除了可以制定 `RootLogger` , 还可以添加自定义 Logger

```properties
# RootLogger配置
log4j.rootLogger = trace,console

# 自定义Logger
log4j.logger.com.itheima = info,file
log4j.logger.org.apache = error
```

> 同一个类可以配置多个 logger

```java
@Test
public void testCustomLogger() throws Exception {
    
    // 自定义 com.itheima
    Logger logger1 = Logger.getLogger(com.itheima.Log4jTest.class);
    logger1.fatal("fatal"); // 严重错误，一般会造成系统崩溃和终止运行
    logger1.error("error"); // 错误信息，但不会影响系统运行
    logger1.warn("warn"); // 警告信息，可能会发生问题
    logger1.info("info"); // 程序运行信息，数据库的连接、网络、IO操作等
    logger1.debug("debug"); // 调试信息，一般在开发阶段使用，记录程序的变量、参数等
    logger1.trace("trace"); // 追踪信息，记录程序的所有流程信息
    // 自定义 org.apache

    Logger logger2 = Logger.getLogger(org.apache.Logger.class);
    logger2.fatal("fatal logger2"); // 严重错误，一般会造成系统崩溃和终止运行
    logger2.error("error logger2"); // 错误信息，但不会影响系统运行
    logger2.warn("warn logger2"); // 警告信息，可能会发生问题
    logger2.info("info logger2"); // 程序运行信息，数据库的连接、网络、IO操作等
    logger2.debug("debug logger2"); // 调试信息，一般在开发阶段使用，记录程序的变量、参数等
    logger2.trace("trace logger2"); // 追踪信息，记录程序的所有流程信息
}
```

