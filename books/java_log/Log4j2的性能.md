## 性能

Log4j2最牛的地方在于异步输出日志时的性能表现，Log4j2在多线程的环境下吞吐量与Log4j和Logback的比较如下图。下图比较中Log4j2有三种模式：1）全局使用异步模式；2）部分Logger采用异步模式；3）异步Appender。可以看出在前两种模式下，Log4j2的性能较之Log4j和Logback有很大的优势。

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210302205642157.png" alt="image-20210302205642157"  /></center>

## 无垃圾记录

垃圾收集暂停是延迟峰值的常见原因，并且对于许多系统而言，花费大量精力来控制这些暂停。

许多日志库（包括以前版本的Log4j）在稳态日志记录期间分配临时对象，如日志事件对象，字符串，字符数组，字节数组等。这会对垃圾收集器造成压力并增加GC暂停发生的频率。

从版本2.6开始，默认情况下Log4j以“无垃圾”模式运行，其中重用对象和缓冲区，并且尽可能不分配临时对象。还有一个“低垃圾”模式，它不是完全无垃圾，但不使用ThreadLocal字段。

Log4j 2.6中的无垃圾日志记录部分通过重用ThreadLocal字段中的对象来实现，部分通过在将文本转换为字节时重用缓冲区来实现。

>  使用Log4j 2.5：内存分配速率809 MB /秒，141个无效集合

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210302205755152.png" alt="image-20210302205755152"  /></center>

Log4j 2.6没有分配临时对象：0（零）垃圾回收。

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210302205839135.png" alt="image-20210302205839135"  /></center>

有两个单独的系统属性可用于手动控制Log4j用于避免创建临时对象的机制：

* `log4j2.enableThreadlocals`  - 如果“true”（非Web应用程序的默认值）对象存储在ThreadLocal字段中并重新使用，否则将为每个日志事件创建新对象。
* `log4j2.enableDirectEncoders` - 如果将“true”（默认）日志事件转换为文本，则将此文本转换为字节而不创建临时对象。注意： 由于共享缓冲区上的同步，在此模式下多线程应用程序的同步日志记录性能可能更差。如果您的应用程序是多线程的并且日志记录性能很重要，请考虑使用异步记录器。