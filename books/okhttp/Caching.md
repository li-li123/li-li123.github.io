Caching
=======

`OkHttp`实现一个可选的，默认情况下关闭`Cache`。 `OkHttp`旨在遵循`Firefox`/`Chrome`等常见的Web浏览器以及不明确时的服务器行为，来实现RFC正确和实用的缓存行为。

## 基础使用

kotlin

```kotlin
private val client: OkHttpClient = OkHttpClient.Builder()
    .cache(Cache(
        directory = File(application.cacheDir, "http_cache"),
        // $0.05 worth of phone storage in 2020
        maxSize = 50L * 1024L * 1024L // 50 MiB
    ))
    .build()
```

java

```java
OkHttpClient client = new OkHttpClient.Builder()
    .cache(new Cache(new File("./cache"), 50L * 1024L * 1024L))
    .build();
```

## EventListener events

缓存事件可以通过`EventListener API`监听和使用。 典型场景如下:

> `OkHttp`事件请[参阅]()
>
> 添加缓存监听器如下
>
> ```java
> OkHttpClient client = new OkHttpClient.Builder()
>     .cache(new Cache(new File("./cache"), 50L * 1024L * 1024L))
>     .eventListener(new EventListener() {
> 
>         @Override
>         public void cacheMiss(@NotNull Call call) {
>             super.cacheMiss(call);
>         }
> 
>         @Override
>         public void cacheHit(@NotNull Call call, @NotNull okhttp3.Response response) {
>             super.cacheHit(call, response);
>         }
> 
>         @Override
>         public void cacheConditionalHit(@NotNull Call call, @NotNull okhttp3.Response cachedResponse)		{
>             super.cacheConditionalHit(call, cachedResponse);
>         }
>     }).build();
> ```

### 缓存命中

在理想情况下，缓存可以满足请求，而无需对网络进行任何有条件的调用。 这将跳过常规事件，例如DNS，连接到网络以及下载响应正文。

根据`HTTP RFC`的建议，默认情况下，文档的最长使用期限为根据“上次修改时间”提供服务时文档使用期限的10％。 默认有效期不用于包含查询的URI。

- `CallStart`
- **`CacheHit`**
- `CallEnd`

> 以上列表表示事件流，以下列表同上

### 缓存未命中

在高速缓存未命中下，会执行正常的请求事件，但还有一个附加事件显示了高速缓存的存在。 如果尚未从网络中读取，无法缓存或根据响应缓存标头超过其生存期，则通常会出现"缓存未命中"。

- `CallStart`
- `**CacheMiss**`
- `ProxySelectStart`
- `… Standard Events …`
- `CallEnd`

### 条件缓存命中

当缓存标志需要检查缓存结果仍然有效时，会收到早期的`cacheConditionalHit`事件，然后是缓存命中或未命中。 至关重要的是，在缓存命中的情况下，服务器不会发送响应正文。

该响应将具有非`null`的`cacheResponse`和`networkResponse`。 仅当响应代码为`HTTP/1.1` `304 Not Modified`时，才会将`cacheResponse`用作顶级响应。

- `CallStart`
- **`CacheConditionalHit`**
- `ConnectionAcquired`
- `… Standard Events…`
- `ResponseBodyEnd *(0 bytes)`*
- **`CacheHit`**
- `ConnectionReleased`
- `CallEnd`

## Cache directory

**缓存目录必须仅由单个实例拥有。**

> 不能两个okhttpClient使用同一个缓存文件夹

可以在不再需要时删除高速缓存。 但是，这可能会删除旨在保留应用程序重启之间持久性的缓存的目的。

```java
cache.delete()
```

## 清空缓存

可以使用`evictAll`清空整个缓存以临时清除空间。

```java
cache.evictAll()
```

可以使用url迭代器删除单个项目。

```java
val urlIterator = cache.urls()
while (urlIterator.hasNext()) {
    if (urlIterator.next().startsWith("https://www.google.com/")) {
         urlIterator.remove()
    }
}
```

## 故障排除

1. 有效的可缓存响应未缓存

确保您已完全读取响应，因为除非它们被完整读取，取消或停止，否则将不会缓存响应。

## 自定义缓存行为

查看缓存文档  https://square.github.io/okhttp/4.x/okhttp/okhttp3/-cache/