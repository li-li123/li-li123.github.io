示例
-----

我们写了一些方法来示例如果使用`OkHttp`来解决常见问题。通读它们了解它们是如何一起工作的。**你可以随意地进行复制、粘贴，这就是它们存在的目的。**

## 同步Get

下载一个文件，打印它的头，并将其响应主体以字符串形式打印。

作用在响应主体上的`string()`方法对于小文档来说是方便和高效的。但是如果响应主体比较大(大于1MB)，避免使用`string()`，因为它会加载整个文档到内存中。**在这种情况下，优先使用`stream`来处理主体。**

```java
private final OkHttpClient client = new OkHttpClient();

public void run() throws Exception {
    Request request = new Request.Builder()
        .url("https://publicobject.com/helloworld.txt")
        .build();

    try (Response response = client.newCall(request).execute()) {
        if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

        Headers responseHeaders = response.headers();
        for (int i = 0; i < responseHeaders.size(); i++) {
            System.out.println(responseHeaders.name(i) + ": " + responseHeaders.value(i));
        }

        System.out.println(response.body().string());
    }
}
```

## 生成复杂的Get请求

```java
public String getString(String url, Map<String, String> params, Map<String, String> headers) throws IOException {
    
    // 生成基础URL
    HttpUrl.Builder builder = null;
    try{
        builder = Objects.requireNonNull(HttpUrl.parse(url)).newBuilder();
    }catch (NullPointerException e){
        return null;
    }

    // 添加参数
    if(params!=null){
        params.forEach(builder::addQueryParameter);
    }
    
    // 添加 Header
    Request.Builder requestBuilder = new Request.Builder();
    requestBuilder.url(builder.toString());
    if(headers!=null){
        headers.forEach(requestBuilder::addHeader);
    }

    // 调用请求
    OkHttpClient client = OkhttpClientFactory.getInstance();
    try(Response response = client.newCall(requestBuilder.build()).execute()){
        if (response.body() == null){
            return null;
        }

        return response.body().string();
    }
}
```

## 异步Get请求

在一个工作线程下载一个文件，当响应可读时获取回调。这个回调将在响应头准备好时执行。读取响应主体可能仍然阻塞。`OkHttp`当前没有提供异步`API`来局部地接收响应主体

```java
 private final OkHttpClient client = new OkHttpClient();

public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://publicobject.com/helloworld.txt")
        .build();

    client.newCall(request).enqueue(new Callback() {
        @Override public void onFailure(Call call, IOException e) {
            e.printStackTrace();
        }

        @Override public void onResponse(Call call, Response response) throws IOException {
            try (ResponseBody responseBody = response.body()) {
                if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

                Headers responseHeaders = response.headers();
                for (int i = 0, size = responseHeaders.size(); i < size; i++) {
                    System.out.println(responseHeaders.name(i) + ": " + responseHeaders.value(i));
                }

                System.out.println(responseBody.string());
            }
        }
    });
}
```

## 访问Header

典型的HTTP头工作起来像一个`Map< String, String >`，每一个字段有一个值或没有值。但是有一些头允许多个值，像`Guava`的`Multimap`。对于一个HTTP响应来应用多个`Vary`头是合法的并且常见的。`OkHttp`的`API`试图兼容这些情况。

当写请求头时，使用`header(name, value)`的方式来设置唯一出现的键值。如果已有值，会在新值添加前移除已有值。使用`addHeader(name, value)`来添加一个头而不移除已经存在的头。

当读取一个响应头时，使用`header(name)`来返回最后一次出现的键值对。通常这是唯一出现的键值对。**如果不存在值，`header(name)`会返回null**。使用`headers(name)`来用一个list读取一个字段的所有值。

使用支持按索引访问的Headers类来访问所有的头。

```java
private final OkHttpClient client = new OkHttpClient();

public void run() throws Exception {
    Request request = new Request.Builder()
        .url("https://api.github.com/repos/square/okhttp/issues")
        .header("User-Agent", "OkHttp Headers.java")
        .addHeader("Accept", "application/json; q=0.5")
        .addHeader("Accept", "application/vnd.github.v3+json")
        .build();

    try (Response response = client.newCall(request).execute()) {
        if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

        System.out.println("Server: " + response.header("Server"));
        System.out.println("Date: " + response.header("Date"));
        System.out.println("Vary: " + response.headers("Vary"));
    }
}
```

## 上传字符串

使用`HTTP` `POST`来发送请求主体到服务器。这个例子上传了一个`markdown`文档到一个用HTML渲染`markdown`的服务器中。因为整个请求主体同时存在内存中，避免使用这个API上传大的文档(大于1MB)。

```java
  public static final MediaType MEDIA_TYPE_MARKDOWN
      = MediaType.parse("text/x-markdown; charset=utf-8");

  private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    String postBody = ""
        + "Releases\n"
        + "--------\n"
        + "\n"
        + " * _1.0_ May 6, 2013\n"
        + " * _1.1_ June 15, 2013\n"
        + " * _1.2_ August 11, 2013\n";

    Request request = new Request.Builder()
        .url("https://api.github.com/markdown/raw")
        .post(RequestBody.create(MEDIA_TYPE_MARKDOWN, postBody))
        .build();

    try (Response response = client.newCall(request).execute()) {
      if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

      System.out.println(response.body().string());
    }
  }
```

## 上传流

这里以`stream`的形式上传请求主体。请求主体的内容如它写入的进行生成。这个示例`stream`直接放入到了`Okio`缓存`sink`中。你的程序可能需要一个`OutputStream`，你可以从`BufferedSink.outputStream()`中获取。

```java
  public static final MediaType MEDIA_TYPE_MARKDOWN
      = MediaType.parse("text/x-markdown; charset=utf-8");

  private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    RequestBody requestBody = new RequestBody() {
      @Override public MediaType contentType() {
        return MEDIA_TYPE_MARKDOWN;
      }

      @Override public void writeTo(BufferedSink sink) throws IOException {
        sink.writeUtf8("Numbers\n");
        sink.writeUtf8("-------\n");
        for (int i = 2; i <= 997; i++) {
          sink.writeUtf8(String.format(" * %s = %s\n", i, factor(i)));
        }
      }

      private String factor(int n) {
        for (int i = 2; i < n; i++) {
          int x = n / i;
          if (x * i == n) return factor(x) + " × " + i;
        }
        return Integer.toString(n);
      }
    };

    Request request = new Request.Builder()
        .url("https://api.github.com/markdown/raw")
        .post(requestBody)
        .build();

    try (Response response = client.newCall(request).execute()) {
      if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

      System.out.println(response.body().string());
    }
  }
```

## 上传文件

使用文件作为请求主体很容易

```java
public static final MediaType MEDIA_TYPE_MARKDOWN
    = MediaType.parse("text/x-markdown; charset=utf-8");

private final OkHttpClient client = new OkHttpClient();

public void run() throws Exception {
    File file = new File("README.md");

    Request request = new Request.Builder()
        .url("https://api.github.com/markdown/raw")
        .post(RequestBody.create(MEDIA_TYPE_MARKDOWN, file))
        .build();

    try (Response response = client.newCall(request).execute()) {
        if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

        System.out.println(response.body().string());
    }
}
```

## 上传表格参数

使用`FormBody.Builder`来构建一个工作起来像`HTML< form >`标签的请求主体。键值对会使用一个兼容`HTML form`的URL编码进行编码

```java
private final OkHttpClient client = new OkHttpClient();

public void run() throws Exception {
    RequestBody formBody = new FormBody.Builder()
        .add("search", "Jurassic Park")
        .build();
    Request request = new Request.Builder()
        .url("https://en.wikipedia.org/w/index.php")
        .post(formBody)
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    System.out.println(response.body().string());
}
```

## 上传多部分请求

> 表单上传文件

`MultipartBody.Builder`可以构造复杂的请求主体与HTML文件上传表单兼容。`multipart`请求主体的每部分本身就是一个请求主体，可以定义它自己的头。如果存在自己的头，那么这些头应该描述部分主体，例如它的`Content-Disposition`。`Content-Length`和`Content-Type`会在其可用时自动添加。

```java
private static final String IMGUR_CLIENT_ID = "...";
  private static final MediaType MEDIA_TYPE_PNG = MediaType.parse("image/png");

  private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    // Use the imgur image upload API as documented at https://api.imgur.com/endpoints/image
    RequestBody requestBody = new MultipartBody.Builder()
        .setType(MultipartBody.FORM)
        .addFormDataPart("title", "Square Logo")
        .addFormDataPart("image", "logo-square.png",
            RequestBody.create(MEDIA_TYPE_PNG, new File("website/static/logo-square.png")))
        .build();

    Request request = new Request.Builder()
        .header("Authorization", "Client-ID " + IMGUR_CLIENT_ID)
        .url("https://api.imgur.com/3/image")
        .post(requestBody)
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    System.out.println(response.body().string());
  }
```



## 使用Moshi 解析Json响应

[Moshi](https://github.com/square/moshi) 是用于在JSON和Java对象之间进行转换的便捷API。 在这里，我们使用它来解码来自`GitHub API`的JSON响应。

请注意，`ResponseBody.charStream()`使用`Content-Type`响应标头来选择在解码响应正文时要使用的字符集。 如果未指定字符集，则默认为`UTF-8`。

```java
private final OkHttpClient client = new OkHttpClient();
private final Moshi moshi = new Moshi.Builder().build();
private final JsonAdapter<Gist> gistJsonAdapter = moshi.adapter(Gist.class);

public void run() throws Exception {
    Request request = new Request.Builder()
        .url("https://api.github.com/gists/c2a7c39532239ff261be")
        .build();
    try (Response response = client.newCall(request).execute()) {
        if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

        Gist gist = gistJsonAdapter.fromJson(response.body().source());

        for (Map.Entry<String, GistFile> entry : gist.files.entrySet()) {
            System.out.println(entry.getKey());
            System.out.println(entry.getValue().content);
        }
    }
}

static class Gist {
    Map<String, GistFile> files;
}

static class GistFile {
    String content;
}
```

## 响应缓存

要缓存响应，你需要一个进行读取和写入的缓存目录，以及一个缓存大小的限制。缓存目录应该是私有的，且不被信任的应用不能够读取它的内容。

让多个缓存同时访问相同的混存目录是错误的。大多数应用应该只调用一次`new OkHttpClient()`，配置它们的缓存，并在所有地方使用相同的实例。否则两个缓存实例会相互进行干涉，腐朽响应缓存，有可能造成你的程序崩溃。

响应缓存使用HTTP头进行所有配置。你可以添加像`Cache-Control:max-stale=3600`这样的请求头并且`OkHttp`的缓存会尊重它们。你的服务器使用自己的响应头像`Cache-Control:max-age=9600`来配置响应缓存多久。这里有缓存头来强制一个缓存响应，强制一个网络响应，强制使用一个条件的GET来验证网络响应。

```java
private final OkHttpClient client;

public CacheResponse(File cacheDirectory) throws Exception {
    int cacheSize = 10 * 1024 * 1024; // 10 MiB
    Cache cache = new Cache(cacheDirectory, cacheSize);

    client = new OkHttpClient.Builder()
        .cache(cache)
        .build();
}

public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://publicobject.com/helloworld.txt")
        .build();

    String response1Body;
    try (Response response1 = client.newCall(request).execute()) {
        if (!response1.isSuccessful()) throw new IOException("Unexpected code " + response1);

        response1Body = response1.body().string();
        System.out.println("Response 1 response:          " + response1);
        System.out.println("Response 1 cache response:    " + response1.cacheResponse());
        System.out.println("Response 1 network response:  " + response1.networkResponse());
    }

    String response2Body;
    try (Response response2 = client.newCall(request).execute()) {
        if (!response2.isSuccessful()) throw new IOException("Unexpected code " + response2);

        response2Body = response2.body().string();
        System.out.println("Response 2 response:          " + response2);
        System.out.println("Response 2 cache response:    " + response2.cacheResponse());
        System.out.println("Response 2 network response:  " + response2.networkResponse());
    }

    System.out.println("Response 2 equals Response 1? " + response1Body.equals(response2Body));
}
```

使用`CacheControl.FORCE_NETWORK`来阻止响应使用缓存。使用`CacheContril.FORCE_CACHE`来阻止使用网络。注意：如果你使用`FORCE_CACHE`且响应需要网络，`OkHttp`会返回一个`504 Unsatisfiable Request`响应。

## 取消调用

使用`Call.cancel()`来立即停止一个正在进行的调用。如果一个线程正在写请求或读响应，它会接收到一个`IOException`。当一个调用不再需要时，使用这个来节省网络，例如当用户从应用离开。同步和异步调用都可以取消。

```java
private final ScheduledExecutorService executor = Executors.newScheduledThreadPool(1);
private final OkHttpClient client = new OkHttpClient();

public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://httpbin.org/delay/2") // This URL is served with a 2 second delay.
        .build();

    final long startNanos = System.nanoTime();
    final Call call = client.newCall(request);

    // Schedule a job to cancel the call in 1 second.
    executor.schedule(new Runnable() {
        @Override public void run() {
            System.out.printf("%.2f Canceling call.%n", (System.nanoTime() - startNanos) / 1e9f);
            call.cancel();
            System.out.printf("%.2f Canceled call.%n", (System.nanoTime() - startNanos) / 1e9f);
        }
    }, 1, TimeUnit.SECONDS);

    System.out.printf("%.2f Executing call.%n", (System.nanoTime() - startNanos) / 1e9f);
    try (Response response = call.execute()) {
        System.out.printf("%.2f Call was expected to fail, but completed: %s%n",
                          (System.nanoTime() - startNanos) / 1e9f, response);
    } catch (IOException e) {
        System.out.printf("%.2f Call failed as expected: %s%n",
                          (System.nanoTime() - startNanos) / 1e9f, e);
    }
}
```

## 超时

使用超时来使调用在当另一端没有到达时失败。网络部分可能是由于连接问题，服务器可用性问题或者其他。`OkHttp`支持连接、读取和写入超时。

```java
private final OkHttpClient client;

public ConfigureTimeouts() throws Exception {
    client = new OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .writeTimeout(10, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build();
}

public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://httpbin.org/delay/2") // This URL is served with a 2 second delay.
        .build();

    try (Response response = client.newCall(request).execute()) {
        System.out.println("Response completed: " + response);
    }
}
```

## 单独配置调用

所有`HTTP client`配置都存在`OkHttpClient`中，包括代理设置，超时和缓存。当你需要改变一个单独`call`的配置时，调用`OkHttpClient.newBuilder()`。这个会返回一个`builder`，与原始的`client`共享下共同的连接池，调度器和配置。在下面的例子中，我们让一个请求有`500ms`的超时而另一个有`3000ms`的超时。

```java
private final OkHttpClient client = new OkHttpClient();

public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://httpbin.org/delay/1") // This URL is served with a 1 second delay.
        .build();

    try {
        // Copy to customize OkHttp for this request.
        OkHttpClient copy = client.newBuilder()
            .readTimeout(500, TimeUnit.MILLISECONDS)
            .build();

        Response response = copy.newCall(request).execute();
        System.out.println("Response 1 succeeded: " + response);
    } catch (IOException e) {
        System.out.println("Response 1 failed: " + e);
    }

    try {
        // Copy to customize OkHttp for this request.
        OkHttpClient copy = client.newBuilder()
            .readTimeout(3000, TimeUnit.MILLISECONDS)
            .build();

        Response response = copy.newCall(request).execute();
        System.out.println("Response 2 succeeded: " + response);
    } catch (IOException e) {
        System.out.println("Response 2 failed: " + e);
    }
}
```

## 处理认证

`OkHttp`会自动重试未认证请求。当一个响应为`401 Not Authorized`时，会要求`Authenticator`来应用证书。`Authenticator`的实现应该构建一个包含缺失证书的新请求。如果没有证书可用，返回null来跳过重试。

使用`Response.challenges()`来获取所有认证挑战的模式和领域。当完成一个`Basic`挑战时，使用`Credentials.basic(username，password)`来编码请求头。

```java
private final OkHttpClient client;

public Authenticate() {
    client = new OkHttpClient.Builder()
        .authenticator(new Authenticator() {
            @Override public Request authenticate(Route route, Response response) throws IOException {
                if (response.request().header("Authorization") != null) {
                    return null; // Give up, we've already attempted to authenticate.
                }

                System.out.println("Authenticating for response: " + response);
                System.out.println("Challenges: " + response.challenges());
                String credential = Credentials.basic("jesse", "password1");
                return response.request().newBuilder()
                    .header("Authorization", credential)
                    .build();
            }
        })
        .build();
}

public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://publicobject.com/secrets/hellosecret.txt")
        .build();

    try (Response response = client.newCall(request).execute()) {
        if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

        System.out.println(response.body().string());
    }
}
```

为了避免当认证无法工作时过多的尝试，你可以返回`null`来放弃。例如，当这些明确的证书已经尝试过了，你可能想跳过。

```java
if (credential.equals(response.request().header("Authorization"))) {
    return null; // If we already failed with these credentials, don't retry.
}
```

你可能也想在达到应用定义的尝试限制次数时跳过尝试：

```java
if (respondseCount(response) >= 3) {
    return null; // If we've failed 3 times, give up.
}
```

上面的代码依赖这个`responseCount()`方法：

```java
private int responseCount(Response response) {
    int result = 1;
    while ((response = response.priorResponse()) != null) {
        result++;
    }
    return result;
}
```

> `response.priorResponse()` 是`OkHttp`库中存储前置响应的数据结构



## 操作cookies

`Okhttp` 提供存储和获取 `cookie` 的接口, 实现这一接口, 就可以保存连接的状态等. 下面展示的是 基于内存的 **线程不安全 `cookie` 管理器**

```java
public class CookieManager implements CookieJar {

    private final Map<String, List<Cookie>> cookieStore = new ConcurrentHashMap<>();
    @Override
    public void saveFromResponse(HttpUrl httpUrl, List<Cookie> cookies) {
        cookieStore.put(httpUrl.host(),cookies);
    }

    @NotNull
    @Override
    public List<Cookie> loadForRequest(HttpUrl httpUrl) {
        List<Cookie> cookies = cookieStore.get(httpUrl.host());
        return cookies != null ? cookies : new ArrayList<Cookie>();
    }

    public void addCookie(URI uri, Cookie cookie){
        List<Cookie> cookieList = cookieStore.get(uri.getHost())!=null ? 			cookieStore.get(uri.getHost()):new LinkedList<Cookie>();
        cookieList.add(cookie);
        cookieStore.put(uri.getHost(),cookieList);
    }
}
```

使用方法如下

```java
OkHttpClient httpClient = new OkHttpClient.Builder()
            .cookieJar(new CookieManager())
            .build();
```



