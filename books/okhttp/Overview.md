OkHttp
========

> 本文档翻译自[官方文档](https://square.github.io/okhttp)版本(4.9.0)

Http是现代应用程序的交换数据、媒体资源常用的网络交互方式。有效的执行HTTP请求可以使您更快的加载以及节省带宽。



`OkHttp`是一个在默认情况就很高效的HTTP客户端：

* 支持`HTTP/2`(对同一个主机的请求，复用同一个`socket`)
* 当`HTTP/2`不可用时，`OkHttp`会使用连接池技术减少请求延时
* 使用`GZIP`压缩技术缩小了下载大小
* 使用缓存技术，避免重复的网络请求

当网络出现问题时，`OkHttp`会坚持不懈的从常见的连接问题中静默恢复。如果您的服务中具有多个IP地址，则在第一次连接失败时，`OkHttp`将尝试使用备用地址。这种特性对于托管在`IPV4+IPV6`和冗余数据中心的服务是必须的。OkHttp支持现代TLS功能(`TLS 1.3`,`ALPN`,证书固定)。可以配置指定的加密协议，获得广泛的连接性。

`OkHttp`提供易用的API,它的`request`和`response`设计成支持流式编程和不变性。支持同步阻塞调用和异步调用。

## Usage

```xml
<dependency>
  <groupId>com.squareup.okhttp3</groupId>
  <artifactId>okhttp</artifactId>
  <version>4.9.0</version>
</dependency>
```

## 发送GET请求

该程序访问一个URL并将结果打印成字符串 [源代码](https://raw.github.com/square/okhttp/master/samples/guide/src/main/java/okhttp3/guide/GetExample.java)

```java
OkHttpClient client = new OkHttpClient();

String run(String url) throws IOException {
  Request request = new Request.Builder()
      .url(url)
      .build();

  try (Response response = client.newCall(request).execute()) {
    return response.body().string();
  }
}
```

## 发送POST请求

该程序使用POST发送数据到服务器。[源代码](https://raw.github.com/square/okhttp/master/samples/guide/src/main/java/okhttp3/guide/PostExample.java)

```java
public static final MediaType JSON
    = MediaType.get("application/json; charset=utf-8");

OkHttpClient client = new OkHttpClient();

String post(String url, String json) throws IOException {
  RequestBody body = RequestBody.create(json, JSON);
  Request request = new Request.Builder()
      .url(url)
      .post(body)
      .build();
  try (Response response = client.newCall(request).execute()) {
    return response.body().string();
  }
}
```

> 更多例子参阅 [OkHttp示例 ](https://book.ironblog.cn/#/books/okhttp/Recipes)

## 使用要求

OkHttp可在`Android 5.0+`(API级别21+)和`Java 8+`上运行。

OkHttp依靠`Okio`获得高性能的`I/O`和`Kotlin`标准库。 两者都是具有强大的向后兼容性的小型库。

**我们强烈建议您保持`OkHttp`为最新**。 与自动更新Web浏览器一样，保持HTTPS客户端的最新状态是防范潜在安全问题的重要防御措施。 我们跟踪动态TLS生态系统并调整OkHttp以改善连接性和安全性。

`OkHttp`使用平台的内置TLS实现。 在Java平台上，OkHttp还支持`Conscrypt`, 它将`BoringSSL`与Java集成在一起。 如果`OkHttp`是第一个安全提供程序，它将使用`Conscrypt`：

```java
Security.insertProviderAt(Conscrypt.newProvider(), 1);
```

`OkHttp 3.12.x`分支支持`Android 2.3+`(API级别9+)和Java 7+。 这些平台不支持`TLS 1.2`，因此不应使用。但是由于升级困难，我们将在2021年12月31日之前将关键补丁程序移植到3.12.x分支。

## 发行版本

具体查看[OkHttp 发行历史](https://square.github.io/okhttp/changelog/)

## MockWebServer

OkHttp提供用于测试`HTTP`，`HTTPS`和`HTTP/2`客户端的库。

```java
testImplementation("com.squareup.okhttp3:mockwebserver:4.9.0")
```

## License

```text
Copyright 2019 Square, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```



