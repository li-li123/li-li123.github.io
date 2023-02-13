拦截器
------

拦截器是一个非常强大的机制，可以监视，重写和重试call。这里是一个简单的拦截器，用来打印出去的请求和收到的响应。

```java
class LoggingInterceptor implements Interceptor {
  @Override public Response intercept(Interceptor.Chain chain) throws IOException {
    Request request = chain.request();

    long t1 = System.nanoTime();
    logger.info(String.format("Sending request %s on %s%n%s",
        request.url(), chain.connection(), request.headers()));

    Response response = chain.proceed(request);

    long t2 = System.nanoTime();
    logger.info(String.format("Received response for %s in %.1fms%n%s",
        response.request().url(), (t2 - t1) / 1e6d, response.headers()));

    return response;
  }
}
```

调用`chain.proceed(request)`是每个拦截器实现的一个主要部分。这个简单的方法是HTTP工作发生，产出满足请求的响应之处，**如果不止一次调用`chain.proceed(request)`，则必须关闭以前的响应主体(`response.body`)。**

拦截器可以链接。假如有一个压缩拦截器和一个检验和拦截器：你需要决定是先数据进行压缩然后检验和，还是先检验和然后进行压缩。`OkHttp`使用列表来跟踪拦截器，并且拦截器按顺序被调用。

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/interceptors-1.png" alt="interceptors-1" style="zoom:50%;" />

## 应用拦截器

拦截器可以注册为应用拦截器和网络拦截器。我们使用上面定义的`LoggingInterceptor`来展示它们的不同。

通过在`OkHttpCleint.Builder`上调用`addInterceptor()`来注册一个应用拦截器：

```java
OkHttpClient client = new OkHttpClient.Builder()
    .addInterceptor(new LoggingInterceptor())
    .build();

Request request = new Request.Builder()
    .url("http://www.publicobject.com/helloworld.txt")
    .header("User-Agent", "OkHttp Example")
    .build();

Response response = client.newCall(request).execute();
response.body().close();
```

[http://www.publicobject.com/helloworld.txt](http://www.publicobject.com/helloworld.txt)这个URL重定向到[https://publicobject.com/helloworld.txt](https://publicobject.com/helloworld.txt)，`OkHttp`会自动跟进这个重定向。我们的应用拦截器会被调用一次，并且从`chain.proceed()`返回的响应是重定向后的响应：

```java
INFO: Sending request http://www.publicobject.com/helloworld.txt on null
User-Agent: OkHttp Example

INFO: Received response for https://publicobject.com/helloworld.txt in 1179.7ms
Server: nginx/1.4.6 (Ubuntu)
Content-Type: text/plain
Content-Length: 1759
Connection: keep-alive
```

我看可以看到我们已经重定向了，引文`reponse.request().url()`与`request.url()`不同。两个日志语句打印了两个不同的URL。

## 网络拦截器

注册一个网络拦截器很相似。调用`addNetworkInterceptor()`替代`addInterceptor()`:

```java
OkHttpClient client = new OkHttpClient.Builder()
    .addNetworkInterceptor(new LoggingInterceptor())
    .build();

Request request = new Request.Builder()
    .url("http://www.publicobject.com/helloworld.txt")
    .header("User-Agent", "OkHttp Example")
    .build();

Response response = client.newCall(request).execute();
response.body().close();
```

当我们运行这个代码，拦截器会执行两次。一次是访问[http://www.publicobject.com/helloworld.txt](http://www.publicobject.com/helloworld.txt)的初始请求，另外一个是重定向到[https://publicobject.com/helloworld.txt](https://publicobject.com/helloworld.txt)。

```java
INFO: Sending request http://www.publicobject.com/helloworld.txt on Connection{www.publicobject.com:80, proxy=DIRECT hostAddress=54.187.32.157 cipherSuite=none protocol=http/1.1}
User-Agent: OkHttp Example
Host: www.publicobject.com
Connection: Keep-Alive
Accept-Encoding: gzip

INFO: Received response for http://www.publicobject.com/helloworld.txt in 115.6ms
Server: nginx/1.4.6 (Ubuntu)
Content-Type: text/html
Content-Length: 193
Connection: keep-alive
Location: https://publicobject.com/helloworld.txt

INFO: Sending request https://publicobject.com/helloworld.txt on Connection{publicobject.com:443, proxy=DIRECT hostAddress=54.187.32.157 cipherSuite=TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA protocol=http/1.1}
User-Agent: OkHttp Example
Host: publicobject.com
Connection: Keep-Alive
Accept-Encoding: gzip

INFO: Received response for https://publicobject.com/helloworld.txt in 80.9ms
Server: nginx/1.4.6 (Ubuntu)
Content-Type: text/plain
Content-Length: 1759
Connection: keep-alive
```

网络请求也包含更多数据，例如通过`OkHttp`添加的`Accept-Encoding:gzip`头来通知支持响应压缩。网络拦截器的`Chain`有一个非空`Connection`，可以用来访问IP地址和用来连接网络服务器的TLS配置。

## 选择应用拦截器还是网络拦截器？

每种拦截器chain有相对的优势。

- 应用拦截器
  - 不需要关心像重定向和重试这样的中间响应。
  - 总是调用一次，即使HTTP响应从缓存中获取服务。
  - 监视应用原始意图。不关心OkHttp注入的像If-None-Match头。
  - 允许短路并不调用Chain.proceed()。
  - 允许重试并执行多个Chain.proceed()调用。
- 网络拦截器
  - 可以操作像重定向和重试这样的中间响应。
  - 对于短路网络的缓存响应不会调用。
  - 监视即将要通过网络传输的数据。
  - 访问运输请求的Connection。

> 应用拦截器和网络拦截器的顺序:
>
> ​	应用拦截器会在请求开始前和获得最终响应后开始执行，中间过程会执行网络拦截器
>
> ![image-20201205110641496](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20201205110641496.png)

## 重写请求

拦截器可以添加，移除或替换请求头。如果有请求主体，它们也可以改变。例如，如果你连接一个已知支持请求主体压缩的网络服务器，你可以使用一个应用拦截器来添加请求主体压缩。

```java
/** This interceptor compresses the HTTP request body. Many webservers can't handle this! */
final class GzipRequestInterceptor implements Interceptor {
  @Override public Response intercept(Interceptor.Chain chain) throws IOException {
    Request originalRequest = chain.request();
    if (originalRequest.body() == null || originalRequest.header("Content-Encoding") != null) {
      return chain.proceed(originalRequest);
    }

    Request compressedRequest = originalRequest.newBuilder()
        .header("Content-Encoding", "gzip")
        .method(originalRequest.method(), gzip(originalRequest.body()))
        .build();
    return chain.proceed(compressedRequest);
  }

  private RequestBody gzip(final RequestBody body) {
    return new RequestBody() {
      @Override public MediaType contentType() {
        return body.contentType();
      }

      @Override public long contentLength() {
        return -1; // We don't know the compressed length in advance!
      }

      @Override public void writeTo(BufferedSink sink) throws IOException {
        BufferedSink gzipSink = Okio.buffer(new GzipSink(sink));
        body.writeTo(gzipSink);
        gzipSink.close();
      }
    };
  }
}
```

## 重写响应

对称地，拦截器可以重写响应头并且改变响应主体。**这个通常是比重写请求头更危险的，因为它可能违背网络服务器的期望！**

如果你在一个棘手的环境下并准备处理结果，重写响应头是一个强大的方式来解决问题。例如，你可以修复一个服务器未配置的`Cache-Control`响应头来启用响应缓存：

```java
/** Dangerous interceptor that rewrites the server's cache-control header. */
private static final Interceptor REWRITE_CACHE_CONTROL_INTERCEPTOR = new Interceptor() {
  @Override public Response intercept(Interceptor.Chain chain) throws IOException {
    Response originalResponse = chain.proceed(chain.request());
    return originalResponse.newBuilder()
        .header("Cache-Control", "max-age=60")
        .build();
  }
};
```

通常当在网络服务器上完成相应的修复时，这种方式会更好的工作。

### 监听下载的进度

```java
public class DownloadResponseBody extends ResponseBody {

    private final Response originalResponse;

    private final AtomicLong downloadLength ;

    // 传入一个全局下载下载变量 AtomicLong downloadLength
    public DownloadResponseBody(Response originalResponse, AtomicLong downloadLength){
        this.downloadLength = downloadLength;
        this.originalResponse = originalResponse;
    }

    @Nullable
    @Override
    public MediaType contentType() {
        return originalResponse.body().contentType();
    }

    @Override
    public long contentLength() {
        return originalResponse.body().contentLength();
    }

    /*
    * 监听读取请求，增加下载进度 downloadLength
    */
    @NotNull
    @Override
    public BufferedSource source() {
        return  Okio.buffer(new ForwardingSource(originalResponse.body().source()) {

            @Override
            public long read(@NotNull Buffer sink, long byteCount) throws IOException {
                long bytesRead = super.read(sink, byteCount);
                long bytesCount = bytesRead == -1 ? 0 : bytesRead;
                downloadLength.addAndGet(bytesCount);
                return bytesRead;
            }

        });
    }
}
```

```java
// 重写ResponseBody监听请求
Interceptor interceptor = new Interceptor() {
    @Override
    public Response intercept(Chain chain) throws IOException {
        Response originalResponse = chain.proceed(chain.request());
        return originalResponse.newBuilder()
            .body(new DownloadResponseBody(originalResponse, downloadLength))
            .build();
    }
};
```



