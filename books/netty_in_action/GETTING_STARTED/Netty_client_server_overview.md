Netty 客户端/服务器 总览
=========

在本节中，我们将构建一个完整的的 Netty客 户端和服务器。虽然你可能集中在写客户端是浏览器的基于 Web 的服务，接下来你将会获得更完整了解 Netty 的 API 是如何实现客户端和服务器的。

Figure 2.1.Echo client / server

![Figure_2.1.Echo_client_server](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/Figure_2.1.Echo_client_server.jpg)

图中显示了连接到服务器的多个并发的客户端。在理论上，客户端可以支持的连接数只受限于使用的 JDK 版本中的制约。

echo（回声）客户端和服务器之间的交互是很简单的;客户端启动后，建立一个连接发送一个或多个消息发送到服务器，其中每相呼应消息返回给客户端。诚然，这个应用程序并不是非常有用。但这项工作是为了更好的理解请求 - 响应交互本身，这是一个基本的模式的客户端/服务器系统。

我们将通过检查服务器端代码开始。