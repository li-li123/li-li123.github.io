## 简介

简单日志门面(Simple Logging Facade For Java) SLF4J 主要是为了给Java日志访问提供一套标准、规范的API框架，其主要意义在于提供接口，具体的实现可以交由其他日志框架，例如log4j和logback等。当然slf4j自己也提供了功能较为简单的实现，但是一般很少用到。对于一般的Java项目而言，日志框架会选择 slf4j-api 作为门面，配上具体的实现框架（log4j、logback等），中间使用桥接器完成桥接。

官方网站： https://www.slf4j.org/

SLF4J是目前市面上最流行的日志门面。现在的项目中，基本上都是使用SLF4J作为我们的日志系统。SLF4J日志门面主要提供两大功能：

1. 日志框架的绑定
2. 日志框架的桥接

-----

## 入门

1. 添加依赖

   ```xml
   <!--slf4j core 使用slf4j必須添加-->
   <dependency>
       <groupId>org.slf4j</groupId>
       <artifactId>slf4j-api</artifactId>
       <version>1.7.27</version>
   </dependency>
   
   <!--slf4j 自带的简单日志实现 -->
   <dependency>
       <groupId>org.slf4j</groupId>
       <artifactId>slf4j-simple</artifactId>
       <version>1.7.27</version>
   </dependency>
   ```

   2. 编写代码

   ```java
   public class Slf4jTest {
       // 声明日志对象
       public final static Logger LOGGER =LoggerFactory.getLogger(Slf4jTest.class);
       
       @Test
       public void testQuick() throws Exception {
           
           //打印日志信息
           LOGGER.error("error");
           LOGGER.warn("warn");
           LOGGER.info("info");
           LOGGER.debug("debug");
           LOGGER.trace("trace");
           
           // 使用占位符输出日志信息
           String name = "jack";
           Integer age = 18;
           LOGGER.info("用户：{},{}", name, age);
           
           // 将系统异常信息写入日志
           try {
               int i = 1 / 0;
           } catch (Exception e) {
               // e.printStackTrace();
               LOGGER.info("出现异常：", e);
           }
       }
   }
   ```

   ## 为什么要使用SLF4J作为日志门面？

   

1. 使用SLF4J框架，可以在部署时迁移到所需的日志记录框架。
2. SLF4J提供了对所有流行的日志框架的绑定，例如log4j，JUL，Simple logging和NOP。因此可以在部署时切换到任何这些流行的框架。
3. 无论使用哪种绑定，SLF4J都支持参数化日志记录消息。由于SLF4J将应用程序和日志记录框架分离，因此可以轻松编写独立于日志记录框架的应用程序。而无需担心用于编写应用程序的日志记录框架。
4. SLF4J提供了一个简单的Java工具，称为迁移器。使用此工具，可以迁移现有项目，这些项目使用日志框架(如Jakarta Commons Logging(JCL)或log4j或Java.util.logging(JUL))到SLF4J

