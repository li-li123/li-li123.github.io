Calls
=======

HTTP客户端的工作是接受您的请求并产生响应。 理论上这很简单，但在实践中却很棘手。

## Requests

每个HTTP请求都包含一个URL，一个方法（如GET或POST）和标头列表。 请求可能还包含`Body`：特定内容类型的数据流。

## Response

响应使用代码（例如200表示成功或404表示找不到），`Headers`和其自己的可选`Body`来回答请求。

## Rewriting Requests

当您向OkHttp提供HTTP请求时，就是在高层次上描述该请求："使用这些`headers`向我获取此URL" 为了确保正确性和效率，OkHttp在传输请求之前会先对其进行重写。

OkHttp可以添加原始请求中不存在的标头，包括`Content-Length`，`Transfer-Encoding`，`User-Agent`，`Host`，`Connection`和`Content-Type`。 它将添加用于透明响应压缩的`Accept-Encoding`标头，除非该`header`已经存在。 如果您有`Cookie`，`OkHttp`会在其中添加一个`Cookie`标头。

一些请求将具有缓存的响应。 如果缓存的响应不是最新，OkHttp可以执行条件GET来下载更新的响应(如果缓存没有命中)。 这要求添加诸如`If-Modified-Since`和`If-None-Match`的标题。

## Rewriting Responses

如果使用透明压缩，则OkHttp将删除相应的响应标头`Content-Encoding`和`Content-Length`，因为它们不适用于解压缩的响应正文。

## Follow-up Requests

当您请求的URL移动后，网络服务器将返回响应代码(例如302)，以指示文档的新URL。 OkHttp将遵循重定向以检索最终响应。

如果响应发出授权要求，OkHttp将要求`Authenticator`(如果已配置)满足授权请求。 如果身份验证器提供了凭据，则将使用该凭据重试请求。

## Retrying Requests

有时连接失败：池化连接已被标注过时且已断开连接，或者无法访问网络服务器本身。当请求存在另外一个路由时，`OkHttp`会从另外一个路由重试请求。

## Calls

您的简单请求当遇到`rewrites`、重定型、`follow-ups`、重试时可能会产生多个请求或者响应。OkHttp使用Call来建模通过许多中间请求和响应来满足您的请求的任务(通常任务不多)。但是，URL重定向或故障转移到备用IP地址后，代码将继续有效。

`Call` 有两种方式执行

* **`Synchronous`** 您的线程将阻塞，直到响应可读为止。
* **`Asynchronous`** 您可以将请求放入任何线程中，并在响应可读时在另一个线程上被调用。

可以从任何线程取消呼叫。 如果尚未完成，将导致呼叫失败！ 当取消调用时，编写请求正文或读取响应正文的代码将发生`IOException`。

## Dispatch

对于**`Synchronous`** (同步调用)，您需要带上自己的线程，并负责管理发出的同时请求数量。 同时连接过多会浪费资源。 太少会损害延迟。

对于异步调用，分派器实现最大并发请求的策略。 **您可以设置每个Web服务器(host)的最大值(默认为5)和整体(默认为64)**。

