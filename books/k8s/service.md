# 5-Service

## Service的概念

Kubernetes `Service` 定义了这样一种抽象：一个`Pod`的逻辑分组，一种可以访问它们的策略 —— 通常称为微服务。 这一组 `Pod`能够被`Service`访问到，通常是**通过`Label Selector`匹配Pod**

![image-20200930171808383](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20200930171808383.png)

Service能够提供负载均衡的能力，但是在使用上有以下限制：

* 只提供 4 层负载均衡能力，而没有 7 层功能，但有时我们可能需要更多的匹配规则来转发请求，这点上 4 层

  负载均衡是不支持的

> 关于4层与7层负载均衡的区别请参阅[负载均衡总结（四层负载与七层负载的区别）](https://zhuanlan.zhihu.com/p/64777456)

## Service 的类型

Service 在 K8s 中有以下四种类型

* ClusterIp：默认类型，自动分配一个仅 Cluster 内部可以访问的虚拟 IP
* NodePort：在 ClusterIP 基础上为 Service 在每台机器上绑定一个端口，这样就可以通过 : NodePort 来访问该服务
* LoadBalancer：在 NodePort 的基础上，借助 cloud provider 创建一个外部负载均衡器，并将请求转发到: NodePort\(需要外部供应商提供服务\)
* ExternalName：把集群外部的服务引入到集群内部来，在集群内部直接使用。没有任何类型代理被创建，这只有 kubernetes 1.7 或更高版本的 kube-dns 才支持

## Service 的实现方式

![Kubernetes Service](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/Kubernetes%20Service.jpg)

1. 客户端访问访问节点通过`iptables`访问Pod和节点
2. API server 通过监控Kube-proxy来实现服务和端点信息的发现
3. Kube-proxy 可以通过Pod的标签，来判断端点信息是否写入Service 的端点信息和`iptables`中的规则

> **service**创建后，集群中的每个容器都可以通过service名访问指定的服务，原因在于coreDNS，会添加对应的解析记录

## Service 代理模式

### Service 代理模式的更迭

在 Kubernetes 集群中，每个 Node 运行一个 `kube-proxy`进程。`kube-proxy`负责为 `Service`实现了一种VIP\(虚拟IP\)的形式，而不是`ExternalName`的形式。 在 Kubernetes v1.0 版本，代理完全在 userspace。在Kubernetes v1.1 版本，新增了 iptables 代理，但并不是默认的运行模式。从 Kubernetes v1.2 起，默认就是iptables 代理。 在 Kubernetes v1.8.0-beta.0 中，添加了 ipvs 代理。在 Kubernetes 1.14 版本开始默认使用 ipvs 代理

在 Kubernetes v1.0 版本， `Service`是 “4层”（TCP/UDP over IP）概念。 在 Kubernetes v1.1 版本，新增了`Ingress` API（beta 版），用来表示 “7层”（HTTP）服务

> 为什么不是`DNS`进行负载均衡?
>
> 答： DNS会被某些客户端缓存，不能实时更新，从而无法实现负载均衡。

### 代理模式的分类

#### userspace 代理模式

![service-userspace](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/service-userspace.jpg)

`Client Pod`访问`Server Pod`,需要先访问到防火墙，然后访问kube-proxy，最总才可以访问到`Server Pod`。这种模式下，`Kube-proxy`压力会很大。

#### iptables 代理模式

![service-iptables](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/service-iptables.jpg)

`Client Pod`访问`Server Pod`,只需要访问防火墙，就可以访问到`Server Pod`。大大减轻`Kube-proxy`的压力。

#### ipvs 代理模式

这种模式，`kube-proxy`会监视`Kubernetes Service`对象和`Endpoints`，调用`netlink`接口以相应地创建`ipvs`规则并定期与 `Kubernetes Service`对象和`Endpoints`对象同步`ipvs`规则，以确保`ipvs`状态与期望一致。访问服务时，流量将被重定向到其中一个后端 Pod。

与`iptables`类似,`ipvs`于`netfilter`的`hook`功能，但使用哈希表作为底层数据结构并在内核空间中工作。这意味着`ipvs`可以更快地重定向流量，并且在同步代理规则时具有更好的性能。此外,`ipvs`为负载均衡算法提供了更多选项，例如：

* `rr` ：轮询调度
* `lc` ：最小连接数
* `dh` ：目标哈希
* `sh` ：源哈希
* `sed` ：最短期望延迟
* `nq` ： 不排队调度

![service-ipvs](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/service-ipvs.jpg)

> `IPVS`取代防火墙，提升性能和提供多种负载均衡的算法
>
> 查看`IPVS`转发逻辑
>
> ```shell
> # ipvsadm -Ln
> IP Virtual Server version 1.2.1 (size=4096)
> Prot LocalAddress:Port Scheduler Flags
>   -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
> TCP  10.96.0.1:443 rr
>   -> 192.168.135.30:6443          Masq    1      3          0
> TCP  10.96.0.10:53 rr
>   -> 10.244.0.4:53                Masq    1      0          0
>   -> 10.244.0.5:53                Masq    1      0          0
> TCP  10.96.0.10:9153 rr
>   -> 10.244.0.4:9153              Masq    1      0          0
>   -> 10.244.0.5:9153              Masq    1      0          0
> UDP  10.96.0.10:53 rr
>   -> 10.244.0.4:53                Masq    1      0          0
>   -> 10.244.0.5:53                Masq    1      0          0
> ```

## CluseterIP Service

`clusterIP`主要在每个`node`节点使用`iptables`,将发向`clusterIP`对应端口的数据，转发到`kube-proxy`中。然后`kube-proxy`自己内部实现有负载均衡的方法，并可以查询到这个`service`下对应`pod`的地址和端口，进而把数据转发给对应的 pod 的地址和端口。

![service-clusterIP](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/service-clusterIP.jpg)

为了实现图上的功能，主要需要以下几个组件的协同工作：

* `apiserver`用户通过`kubectl`命令向`apiserver`发送创建`service`的命令，`apiserver`接收到请求后将数据存储到`etcd`中
* `kube-proxy kubernetes`的每个节点中都有一个叫做`kube-porxy`的进程，这个进程负责感知`service`，`pod`的变化，并将变化的信息写入本地的`iptables`规则中
* `iptables`使用NAT等技术将`virtualIP`的流量转至`endpoint`中

### 创建`ClusterIp Service`

1. 创建 myapp-deploy.yaml 文件

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deploy
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      release: stabel
  template:
    metadata:
      labels:
        app: myapp
        release: stabel
        env: test
    spec:
      containers:
      - name: myapp
        image: nginx
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 80
```

> `kubectl create -f myapp-deploy.yaml`创建deployment

 结果

```shell
# kubectl get deployment -o wide
NAME           READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES   SELECTOR
myapp-deploy   3/3     3            3           4m40s   myapp        nginx    app=myapp,release=stabel
```

1. 创建Service文件

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: myapp
     namespace: default
   spec:
     type: ClusterIP
     selector:
       app: myapp
       release: stabel
     ports:
     - name: http
       port: 80
       targetPort: 80
   ```

   > 1. `kubectl create -f cluster-service.yaml`创建`Cluster Service`
   > 2. `selector`里面的`label`必须全部匹配，如果匹配不上，`service`依然会创建，只不过`iptables`转发的地址为空

结果

```shell
# kubectl get svc -o wide
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE    SELECTOR
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP   25h    <none>
myapp        ClusterIP   10.110.225.130   <none>        80/TCP    119s   app=myapp,release=stabel
```

### Headless Service

有时不需要或不想要负载均衡，以及单独的 Service IP 。遇到这种情况，可以通过指定`ClusterIP(spec.clusterIP)`的值为 "None"来创建`Headless Service`这类 Service 并不会分配`Cluster IP`,`kubeproxy`不会处理它们，而且平台也不会为它们进行负载均衡和路由。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-headless
  namespace: default
spec:
  clusterIP: "None"
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 80
```

结果：

```shell
$ kubectl get svc  -o wide
NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE     SELECTOR
kubernetes       ClusterIP   10.96.0.1        <none>        443/TCP   26h     <none>
myapp            ClusterIP   10.110.225.130   <none>        80/TCP    33m     app=myapp,release=stabel
myapp-headless   ClusterIP   None             <none>        80/TCP    4m45s   app=myapp
```

如何获取k8s给service分配的实际地址：

原理：所有`Service`创建后都会在`Core DNS`中创建一个解析记录，默认格式是 `Service名称.命名空间名称.当前集群的域名.`

> 默认集群域名为`svc.cluster.local`

具体步骤

1. 获取`CoreDNS`的地址

   ```shell
   # kubectl get pod -n kube-system -o wide
   NAME                                 READY   STATUS    RESTARTS   AGE   IP               NODE       
   coredns-bccdc95cf-6jfzn              1/1     Running   1          26h   10.244.0.4       k8s-master
   coredns-bccdc95cf-fl69q              1/1     Running   1          26h   10.244.0.5       k8s-master
   ```

2. 尝试解析

```shell
dig -t A myapp-headless.default.svc.cluster.local. @10.244.0.4
```

1. 解析结果

   ```shell
   # dig -t A myapp-headless.default.svc.cluster.local. @10.244.0.4

   ; <<>> DiG 9.11.4-P2-RedHat-9.11.4-16.P2.el7_8.6 <<>> -t A myapp-headless.default.svc.cluster.local. .... 不重要的信息
   ;; ANSWER SECTION:

   myapp-headless.default.svc.cluster.local. 30 IN A 10.244.1.3 # 真实IP
   myapp-headless.default.svc.cluster.local. 30 IN A 10.244.1.2
   myapp-headless.default.svc.cluster.local. 30 IN A 10.244.3.2
   ```

## NodePort Service

`NodePort`的原理在于在`node`上开了一个端口，将向该端口的流量导入到`kube-proxy`，然后由`kube-proxy`进一步到给对应的 `pod`。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-nodeport
  namespace: default
spec:
  type: NodePort
  selector:
    app: myapp
    release: stabel
  ports:
  - name: http
    port: 80 # 对外暴露的端口
    targetPort: 80 # Pod内部的端口
    nodePort: 33333 # 指定具体端口, 不指定将随机分配一个
```

> NodePort 指定的端口可能不会生效，原因在于k8s的servcie的端口默认范围在30000-50000，不在这个范围的端口，k8s会随机指定一个新的端口。
>
> 端口范围是`api-server`的启动参数，通过`kubectl -n kube-system describe pod kube-apiserver-k8s-master`可以查看

## LoadBalancer

loadBalancer 和 nodePort 其实是同一种方式。区别在于 loadBalancer 比 nodePort 多了一步，就是可以调用cloud provider 去创建 LB 来向节点导流。

![service-loadblancer](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/service-loadblancer.jpg)

## ExternalName

这种类型的 Service 通过返回 CNAME 和它的值，可以将服务映射到 externalName 字段的内容\( 例如：www.baidu.com \)。ExternalName Service 是 Service 的特例，它没有 selector，也没有定义任何的端口和Endpoint。相反的，对于运行在集群外部的服务，它通过返回该外部服务的别名这种方式来提供服务

```yaml
kind: Service
apiVersion: v1
metadata:
  name: my-service-1
  namespace: default
spec:
  type: ExternalName
  externalName: www.baidu.com
```

当查询主机 my-service.defalut.svc.cluster.local \( SVC\_NAME.NAMESPACE.svc.cluster.local \)时，集群的DNS 服务将返回一个值 my.database.example.com 的 CNAME 记录。访问这个服务的工作方式和其他的相同，唯一不同的是重定向发生在 DNS 层，而且不会进行代理或转发。**相当于，在DNS中加了一条解析记录而已**

查看结果:

```shell
$ dig -t A my-service-1.default.svc.cluster.local. @10.244.0.4
; <<>> DiG 9.11.4-P2-RedHat-9.11.4-16.P2.el7_8.6 <<>> -t A my-service-1.default.svc.cluster.local. @10.244.0.4
;; global options: +cmd
;; Got answer:
;; WARNING: .local is reserved for Multicast DNS
;; You are currently testing what happens when an mDNS query is leaked to DNS
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 45247
;; flags: qr aa rd; QUERY: 1, ANSWER: 4, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;my-service-1.default.svc.cluster.local.        IN A

;; ANSWER SECTION:
my-service-1.default.svc.cluster.local. 5 IN CNAME www.baidu.com.
www.baidu.com.          5       IN      CNAME   www.a.shifen.com.
www.a.shifen.com.       5       IN      A       14.215.177.38
www.a.shifen.com.       5       IN      A       14.215.177.39
```

