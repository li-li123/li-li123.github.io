## ubuntu 更换阿里云镜像

```dockerfile
FROM ubuntu:20.04
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g'

```

## socket 转 http

```dockerfile
FROM shinobit/privoxy
RUN echo -e "forward-socks5t   /   ssr:1080 . " >> /etc/privoxy/config
EXPOSE 8118
CMD ["/usr/sbin/privoxy", "--no-daemon", "/etc/privoxy/config"]
```

## Java

```dockerfile
FROM openjdk:8-alpine
ENV TZ Asia/Shanghai
ENV LANG "en_US.UTF-8"
RUN set -eux; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; \
    echo $TZ > /etc/timezone
RUN mkdir -p /var/books
ENV BOOK_PATH /var/books/
VOLUME ["/var/books"]
COPY target/books-0.0.1-SNAPSHOT.jar /app.jar

EXPOSE 8909
CMD ["java", "-version"]
ENTRYPOINT ["java", "-Dfile.encoding=UTF-8", "-jar", "/app.jar"]

```