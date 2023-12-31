Buffer（缓冲）
=====

正如我们先前所指出的，网络数据的基本单位永远是 byte(字节)。`Java NIO` 提供 `ByteBuffer` 作为字节的容器，但它的作用太有限，也没有进行优化。使用`ByteBuffer`通常是一件繁琐而又复杂的事。

幸运的是，Netty提供了一个强大的缓冲实现类用来表示字节序列以及帮助你操作字节和自定义的`POJO`。这个新的缓冲类，`ByteBuf`,效率与JDK的`ByteBuffer`相当。设计`ByteBuf`是为了在Netty的`pipeline`中传输数据。它是为了解决`ByteBuffer`存在的一些问题以及满足网络程序开发者的需求，以提高他们的生产效率而被设计出来的。

请注意，在本书剩下的章节中，为了帮助区分，我将使用数据容器指代Netty的缓冲接口及实现，同时仍然使用Java的缓冲API指代JDK的缓冲实现。

在本章中，你将会学习Netty的缓冲API,为什么它能够超过JDK的实现，它是如何做到这一点，以及为什么它会比JDK的实现更加灵活。你将会深入了解到如何在Netty框架中访问被交换数据以及你能对它做些什么。这一章是之后章节的基础，因为几乎Netty框架的每一个地方都用到了缓冲。

因为数据需要经过`ChannelPipeline`和`ChannelHandler`进行传输，而这又离不开缓冲，所以缓冲在Netty应用程序中是十分普遍的。我们将在第6章学习`ChannelHandler`和`ChannelPipeline`。
