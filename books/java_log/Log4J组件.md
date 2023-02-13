Log4J 主要由 `Loggers` (日志记录器)、`Appenders`（输出端）和 `Layout`（日志格式化器）组成。其中 `Loggers`  控制日志的输出级别与日志是否输出；`Appenders` 指定日志的输出方式（输出到控制台、文件等）；`Layout` 控制日志信息的输出格式。



## Loggers

日志记录器，负责收集处理日志记录，实例的命名就是类“XX”的 `full quailied name`（类的全限定名），`Logger` 的名字大小写敏感，其命名有继承机制：例如：`name` 为 `org.apache.commons` 的 logger 会继承 name 为 org.apache 的logger。

Log4J中有一个特殊的 logger 叫做“root”，他是所有 logger 的根，也就意味着其他所有的 logger 都会直接或者间接地继承自root。root logger 可以用 Logger.getRootLogger() 方法获取

但是，自log4j 1.2版以来， Logger 类已经取代了Category 类。对于熟悉早期版本的log4j的人来说，Logger 类可以被视为Category 类的别名。

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210302173228442.png" alt="image-20210302173228442" style="zoom:80%;" /></center>

## Appenders

`Appender` 用来指定日志输出到哪个地方，可以同时指定日志的输出目的地。`Log4j` 常用的输出目的地有以下几种：

| 输出端类型                 | 作用                                                         |
| -------------------------- | ------------------------------------------------------------ |
| `ConsoleAppender`          | 将日志输出到控制台                                           |
| `FileAppender`             | 将日志输出到文件中                                           |
| `DailyRollingFileAppender` | 将日志输出到一个日志文件，并且每天输出到一个新的文件         |
| `RollingFileAppender`      | 将日志信息输出到一个日志文件，并且指定文件的尺寸，当文件大<br/>小达到指定尺寸时，会自动把文件改名，同时产生一个新的文件 |
| `JDBCAppender`             | 把日志信息保存到数据库中                                     |

## Layouts

布局器 Layouts用于控制日志输出内容的格式，让我们可以使用各种需要的格式输出日志。Log4j常用的Layouts:

| 格式化器类型    | 作用                                                         |
| --------------- | ------------------------------------------------------------ |
| `HTMLLayout`    | 格式化日志输出为HTML表格形式                                 |
| `SimpleLayout`  | 简单的日志输出格式化，打印的日志格式为（info - message）     |
| `PatternLayout` | 最强大的格式化期，可以根据自定义格式输出日志，如果没有指定转换格式，就是用默认的转换格式 |





 

