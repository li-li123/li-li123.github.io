Events
-----
> 当监听器监听开始事件时，监听器会在开始动作前执行。当监听器监听结束事件时，监听器会在动作结束后执行

通过事件，您可以捕获应用程序的HTTP调用中的指标。 事件可用用来监视：

* 应用程序发出的`HTTP`调用的大小和频率。 如果您发送了过多请求，或者您的请求过大，那么您应该知道这一点！
* 这些请求在基础网络上的性能。 如果网络的性能不足，则需要改善网络或减少使用。

## 事件监听器

可以重写`EventListener`的子类，来监听感兴趣的事件。在没有重定向或重试的成功HTTP调用中，此流程描述了事件的顺序。

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/events-1.png" alt="events-1" style="zoom: 50%;" />

这是一个示例事件侦听器，可显示带有时间戳的每个事件。[源码地址](https://github.com/square/okhttp/blob/master/samples/guide/src/main/java/okhttp3/recipes/PrintEventsNonConcurrent.java)

```java
class PrintingEventListener extends EventListener {
  private long callStartNanos;

  private void printEvent(String name) {
    long nowNanos = System.nanoTime();
    if (name.equals("callStart")) {
      callStartNanos = nowNanos;
    }
    long elapsedNanos = nowNanos - callStartNanos;
    System.out.printf("%.3f %s%n", elapsedNanos / 1000000000d, name);
  }

  @Override public void callStart(Call call) {
    printEvent("callStart");
  }

  @Override public void callEnd(Call call) {
    printEvent("callEnd");
  }

  @Override public void dnsStart(Call call, String domainName) {
    printEvent("dnsStart");
  }

  @Override public void dnsEnd(Call call, String domainName, List<InetAddress> inetAddressList) {
    printEvent("dnsEnd");
  }

  ...
}
```

发起了两个请求

```java
Request request = new Request.Builder()
    .url("https://publicobject.com/helloworld.txt")
    .build();

System.out.println("REQUEST 1 (new connection)");
try (Response response = client.newCall(request).execute()) {
  // Consume and discard the response body.
  response.body().source().readByteString();
}

System.out.println("REQUEST 2 (pooled connection)");
try (Response response = client.newCall(request).execute()) {
  // Consume and discard the response body.
  response.body().source().readByteString();
}
```

监听器打印相应事件

```text
REQUEST 1 (new connection)
0.000 callStart
0.028 proxySelectStart
0.028 proxySelectEnd
0.028 dnsStart
0.072 dnsEnd
0.080 connectStart
0.283 secureConnectStart
0.798 secureConnectEnd
0.798 connectEnd
0.799 connectionAcquired
0.801 requestHeadersStart
0.802 requestHeadersEnd
1.007 responseHeadersStart
1.008 responseHeadersEnd
1.012 responseBodyStart
1.012 responseBodyEnd
1.013 connectionReleased
1.013 callEnd
REQUEST 2 (pooled connection)
0.000 callStart
0.009 connectionAcquired  // 没有发起连接
0.009 requestHeadersStart
0.009 requestHeadersEnd
0.209 responseHeadersStart
0.210 responseHeadersEnd
0.210 responseBodyStart
0.210 responseBodyEnd
0.211 connectionReleased
0.211 callEnd
```

**请注意，第二个请求并没有不触发连接事件**。 它重用了第一个请求后的连接，从而显着提高了性能。

## 监听器工厂

在前面的示例中，我们使用了一个名为`callStartNanos`的字段来跟踪每个事件的经过时间。 这很方便，但是如果同时执行多个调用，它将不起作用。 为了适应这种情况，请使用`Factory`为每个`Call`创建一个新的`EventListener`实例。 这允许每个侦听器保持特定于呼叫的状态。

该示例工厂为每个请求创建唯一的ID，并使用该ID区分日志消息中的请求。[源码地址](https://github.com/square/okhttp/blob/master/samples/guide/src/main/java/okhttp3/recipes/PrintEvents.java)

```java
class PrintingEventListener extends EventListener {
  public static final Factory FACTORY = new Factory() {
    final AtomicLong nextCallId = new AtomicLong(1L);

    @Override public EventListener create(Call call) {
      long callId = nextCallId.getAndIncrement();
      System.out.printf("%04d %s%n", callId, call.request().url());
      return new PrintingEventListener(callId, System.nanoTime());
    }
  };

  final long callId;
  final long callStartNanos;

  public PrintingEventListener(long callId, long callStartNanos) {
    this.callId = callId;
    this.callStartNanos = callStartNanos;
  }

  private void printEvent(String name) {
    long elapsedNanos = System.nanoTime() - callStartNanos;
    System.out.printf("%04d %.3f %s%n", callId, elapsedNanos / 1000000000d, name);
  }

  @Override public void callStart(Call call) {
    printEvent("callStart");
  }

  @Override public void callEnd(Call call) {
    printEvent("callEnd");
  }

  ...
}
```

我们可以使用此监听器来监听对并发的HTTP请求：

```java
Request washingtonPostRequest = new Request.Builder()
    .url("https://www.washingtonpost.com/")
    .build();
client.newCall(washingtonPostRequest).enqueue(new Callback() {
  ...
});

Request newYorkTimesRequest = new Request.Builder()
    .url("https://www.nytimes.com/")
    .build();
client.newCall(newYorkTimesRequest).enqueue(new Callback() {
  ...
});
```

在家用WiFi上进行的比赛显示，《时代》(0002）比《邮报》(0001)的完成时间稍早：

```text
0001 https://www.washingtonpost.com/
0001 0.002 callStart
0002 https://www.nytimes.com/
0002 0.000 callStart
0001 0.015 proxySelectStart
0002 0.011 proxySelectStart
0001 0.015 proxySelectEnd
0002 0.011 proxySelectEnd
0002 0.026 connectStart
0001 0.030 connectStart
0002 0.099 secureConnectStart
0002 0.337 secureConnectEnd
0002 0.362 connectEnd
0002 0.363 connectionAcquired
0002 0.366 requestHeadersStart
0002 0.372 requestHeadersEnd
0002 0.446 responseHeadersStart
0002 0.448 responseHeadersEnd
0002 0.460 responseBodyStart
0002 0.545 responseBodyEnd
0002 0.545 connectionReleased
0002 0.545 callEnd
0001 5.102 secureConnectStart
0001 5.272 secureConnectEnd
0001 5.273 connectEnd
0001 5.275 connectionAcquired
0001 5.276 requestHeadersStart
0001 5.276 requestHeadersEnd
0001 14.386 responseHeadersStart
0001 14.387 responseHeadersEnd
0001 14.388 responseBodyStart
0001 14.496 responseBodyEnd
0001 14.496 connectionReleased
0001 14.497 callEnd
```

EventListener.Factory还可以将指标限制为一部分调用。 这是随机抽取10％的指标：

```java
class MetricsEventListener extends EventListener {
  private static final Factory FACTORY = new Factory() {
    @Override public EventListener create(Call call) {
      if (Math.random() < 0.10) {
        return new MetricsEventListener(call);
      } else {
        return EventListener.NONE;
      }
    }
  };

  ...
}
```

## 失败事件流

当操作失败时，将调用失败方法。 这是`connectFailed()`，用于在建立与服务器的连接时失败，而在HTTP调用永久失败时，则是`callFailed()`。 发生故障时，`start`事件可能没有相应的`end`事件。

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/event2.png" alt="event2" style="zoom: 50%;" />

## Events with Retries and Follow-Ups

`OkHttp`具有弹性，可以自动从某些连接故障中恢复。 在这种情况下，`connectFailed()`事件不是最终事件，也不是`callFailed()`之后的事件。 尝试重试时，事件侦听器将收到多个相同类型的事件。

单个HTTP调用可能需要发出后续请求，以处理身份验证质询，重定向和HTTP层超时。 在这种情况下，可能会尝试多个连接，请求和响应。这也是当跟踪是单个请求时可能触发相同类型的多个事件的另一个原因。

<img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/events3.png" alt="events3" style="zoom: 50%;" />

## 可用性

在`OkHttp 3.11`中，事件可以作为公共API使用。 将来的版本可能会引入新的事件类型； 您将需要覆盖相应的方法来处理它们。