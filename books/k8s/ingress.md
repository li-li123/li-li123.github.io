# 6-nginx-Ingress

## Ingress-Nginx 运行逻辑

![service-Ingress-1](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/service-Ingress-1.jpg)

客户端通过一个或多个域名访问到服务器，服务器中的`Nginx`反向代理到`k8s`内部的Service。

> `Nginx`通过`NodePort`部署到`k8s`,底层逻辑在于，`k8s`会自动管理`nginx`的配置文件来实现路由的转发，而不用手动管理。

### `k8s`管理`Nginx`

![service-Ingress-2](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/service-Ingress-2.jpg)

1. `APIServer`监听协程，如果出现更新事件
2. `NginxController`会监听更新事件，把事件写入同步队列
3. 同步协程会定时从同步队列中，读取事件，更新`Nginx`中的配置文件
4. 如果 一些事件不需要等待，会直接被同步进程读取

参考资料:

> * [Ingress-Nginx github 地址](https://github.com/kubernetes/ingress-nginx)
> * [Ingress-Nginx 官方网站](https://kubernetes.github.io/ingress-nginx)

## 部署

1. 安装`nginx-controller`

```shell
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.35.0/deploy/static/provider/cloud/deploy.yaml
```

> v.15.1版本，最高支持到v0.35.0的ingress-nginx
> **`Warning: extensions/v1beta1 Ingress is deprecated in v1.14+, unavailable in v1.22+; use networking.k8s.io/v1 Ingress`**

1. 查看安装结果

   ```shell
   $kubectl get pod -n ingress-nginx
   NAME                                        READY   STATUS      RESTARTS   AGE
   ingress-nginx-controller-854d6b8b6b-n5vxl   1/1     Running     0          4m51s
   $kubectl get svc -n ingress-nginx
   NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                 
   ingress-nginx-controller             NodePort    10.102.183.75    <none>    80:32152/TCP,443:32375/TCP 
   ingress-nginx-controller-admission   ClusterIP   10.106.141.229   <none>    443/TCP
   ```

   > `ingress-nginx-controller`暴露的端口将在下面一节用到

## Ingress HTTP 代理访问

资源文件

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-dm
spec:
  replicas: 2
  selector:
    matchLabels:
      name: nginx
  template:
    metadata:
      labels:
        name: nginx
    spec:
      containers:
      - name: nginx
        image: wangyanglinux/myapp:v1
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc
spec:
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  selector:
    name: nginx
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
spec:
  rules:
  - host: www.abc.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```

测试

```shell
$curl www.abc.com:32152 # 查看svc可以获取开放的端口
Hello MyApp | Version: v1 | <a href="hostname.html">Pod Name</a>
```

架构图

![image-20201012194657638](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20201012194657638.png)

## Ingress HTTPS 代理访问

### 创建证书，以及cert存储方式

```shell
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=nginxsvc/O=nginxsvc"
kubectl create secret tls tls-secret --key tls.key --cert tls.crt
```

### 资源文件

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test-https
spec:
  tls:
    - hosts:
      - foo.bar.com
      secretName: tls-secret
  rules:
  - host: foo.bar.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```

测试

```yaml
$curl -k https://foo.bar.com:32375 # 查看svc可以获取开放的端口
```

## Nginx 进行 BasicAuth

### 生成密钥

```yaml
yum -y install httpd # 安装httpd是为了生成密钥文件，后续的操作不需要httpd
htpasswd -c auth foo
kubectl create secret generic basic-auth --from-file=auth
```

### 资源文件

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-with-auth
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required - foo'
spec:
  rules:
  - host: foo2.bar.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```

> 更多信息参考[官方教程](https://kubernetes.github.io/ingress-nginx/examples/auth/basic/)

## Nginx 进行自定义配置

| 名称 | 描述 | 值 |
| :--- | :--- | :--- |
| `nginx.ingress.kubernetes.io/rewrite-target` | 必须重定向流量的目标URI | 字符串 |
| `nginx.ingress.kubernetes.io/ssl-redirect` | 指示位置部分是否仅可访问SSL（当Ingress包含证书时默认为True） | 布尔 |
| `nginx.ingress.kubernetes.io/forcessl-redirect` | 即使Ingress未启用TLS，也强制重定向到HTTPS | 布尔 |
| `nginx.ingress.kubernetes.io/app-root` | 定义Controller必须重定向的应用程序根，如果它在'/'上下文中 | 字符串 |
| `nginx.ingress.kubernetes.io/use-regex` | 指示Ingress上定义的路径是否使用正则表达式 | 布尔 |
|  |  |  |

## 指定跳转

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: http://foo.bar.com:31795/hostname.html
spec:
  rules:
  - host: foo10.bar.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```

> 访问 [http://foo10.bar.com](http://foo10.bar.com) 都将被重定向至 [http://foo.bar.com:31795/hostname.html](http://foo.bar.com:31795/hostname.html)

