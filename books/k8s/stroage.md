# 7-存储

## 存储类型

| 类型 | 作用 |
| :--- | :--- |
| `configMap`cu | 存储配置文件 |
| `Secret` | 存储密钥 |
| `volume` | 对Pod提供共享存储卷 |
| `Persistent Volume` | 持久化存储 |

## configMap

`ConfigMap`功能在`Kubernetes1.2`版本中引入，许多应用程序会从配置文件、命令行参数或环境变量中读取配置信息。`ConfigMap API`给我们提供了向容器中注入配置信息的机制,`ConfigMap`可以被用来保存单个属性，也可以用来保存整个配置文件或者`JSON`二进制大对象。**类似于配置中心的作用**

> **`configMaps`的信息存储在`etcd`中**

### configMap 的创建

#### 使用文件或目录创建

```shell
$tree /root/storage/config/
/root/storage/config/
├── game.properties
└── ui.properties

$cat /root/storage/config/ui.properties
color.good=purple
color.bad=yellow
allow.textmode=true
how.nice.to.look=fairlyNice

$ cat /root/storage/config/game.properties
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30

$kubectl create configmap game-config --from-file=/root/storage/config
```

> `--from-file`可以指定单个文件，或者目录。当指定在目录下的所有文件都会被用在`ConfigMap`里面创建一个键值对，键的名字就是文件名，值就是文件的内容。

#### 使用字面值创建

> 使用文字值创建，利用`--from-literal`参数传递配置信息，该参数可以使用多次，格式如下

```shell
$ kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
```

#### 使用资源清单创建

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config
  namespace: default
data:
  log_level: INFO
```

> kubectl create -f env.yaml

### 查看configMaps

```shell
# 获取configmap
$ kubectl get configmaps 
$ kubectl get cm


# 获取指定configMap的详细信息
$ kubectl get configmaps game-config -o yaml
$ kubectl describe cm game-config
```

### 删除configMap

```shell
 $ kubectl delete configmap special-config
```

### Pod 中使用 ConfigMap

#### 使用 ConfigMap 来替代环境变量

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config
  namespace: default
data:
  log_level: INFO
---
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
  - name: test-container
    image: nginx:latest
    imagePullPolicy: IfNotPresent
    command: [ "/bin/sh", "-c", "env" ]
    env:
    - name: SPECIAL_LEVEL_KEY
      valueFrom:
        configMapKeyRef:
          name: special-config
          key: special.how
    - name: SPECIAL_TYPE_KEY
      valueFrom:
        configMapKeyRef:
          name: special-config
          key: special.type
    envFrom:
    - configMapRef:
        name: env-config
  restartPolicy: Never
```

> kubectl create -f 资源文件名 创建pod

查看结果

```shell
$ kubectl logs dapi-test-pod
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT=tcp://10.96.0.1:443
HOSTNAME=dapi-test-pod
HOME=/root
PKG_RELEASE=1~buster
SPECIAL_TYPE_KEY=charm
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
NGINX_VERSION=1.19.3
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KUBERNETES_PORT_443_TCP_PORT=443
NJS_VERSION=0.4.4
KUBERNETES_PORT_443_TCP_PROTO=tcp
SPECIAL_LEVEL_KEY=very
log_level=INFO
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_SERVICE_HOST=10.96.0.1
PWD=/
```

#### 用`ConfigMap`设置命令行参数

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
---
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
  - name: test-container
    image: nginx:latest
    imagePullPolicy: IfNotPresent
    command: [ "/bin/sh", "-c", "echo $(SPECIAL_LEVEL_KEY) $(SPECIAL_TYPE_KEY)" ]
    env:
    - name: SPECIAL_LEVEL_KEY
      valueFrom:
        configMapKeyRef:
          name: special-config
          key: special.how
    - name: SPECIAL_TYPE_KEY
      valueFrom:
        configMapKeyRef:
          name: special-config
          key: special.type
  restartPolicy: Never
```

查看结果

```shell
# kubectl logs pod/dapi-test-pod
very charm
```

#### 通过数据卷插件使用ConfigMap

```shell
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
---
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
  - name: test-container
    image: nginx:latest
    imagePullPolicy: IfNotPresent
    command: [ "/bin/sh", "-c", "ls /etc/config && cat /etc/config/special.how && cat    /etc/config/special.type" ]
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: special-config  
  restartPolicy: Never
```

> **在数据卷里面使用这个 ConfigMap，有不同的选项。最基本的就是将文件填入数据卷，在这个文件中,键就是文件名，键值就是文件内容**

查看结果

```shell
# kubectl logs pod/dapi-test-pod
special.how
special.type
verycharm
```

### configMap 热更新

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: log-config
  namespace: default
data:
  log_level: INFO
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: my-nginx
spec:
  replicas: 1
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: nginx:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
      volumes:
      - name: config-volume
        configMap:
          name: log-config
```

查看数据

```shell
$ kubectl exec `kubectl get pods -l run=my-nginx -o=name|cut -d "/" -f2` cat  /etc/config/log_level
INFO
```

> `kubectl get pods -l run=my-nginx -o=name|cut -d "/" -f2`是为了获取pod的名称

修改 ConfigMap

```shell
$ kubectl edit configmap log-config
```

修改 log\_level 的值为 DEBUG **等待大概 10 秒钟时间**，再次查看环境变量的值

```shell
$ kubectl exec `kubectl get pods -l run=my-nginx -o=name|cut -d "/" -f2` cat /etc/config/log_level
DEBUG
```

ConfigMap 更新后滚动更新 Pod **更新 ConfigMap 目前并不会触发相关 Pod 的滚动更新，可以通过修改 pod annotations 的方式强制触发滚动更新**

```shell
$kubectl patch deployment my-nginx --patch '{"spec": {"template": {"metadata": {"annotations":
{"version/config": "20190411" }}}}}'
```

这个例子里我们在 `.spec.template.metadata.annotations`中添加`version/config`，每次通过修改`version/config`来触发滚动更新

**!!!!!注意**

* **使用该 ConfigMap 挂载的 Env 不会同步更新**
* **使用该 ConfigMap 挂载的 Volume 中的数据需要一段时间（实测大概10秒）才能同步更新**

## Secret

### Secret 存在的意义

`Secret`解决了密码、`token`、密钥等敏感数据的配置问题，而不需要把这些敏感数据暴露到镜像或者`Pod Spec`中。`Secret`可以以 `Volume`或者环境变量的方式使用

Secret 有三种类型：

* Service Account ：用来访问 Kubernetes API，由 Kubernetes 自动创建，并且会自动挂载到 Pod 的`/run/secrets/kubernetes.io/serviceaccount`目录中
* Opaque ：base64编码格式的Secret，用来存储密码、密钥等
* kubernetes.io/dockerconfigjson ：用来存储私有 docker registry 的认证信息

### Service Account

Service Account 用来访问 Kubernetes API，由 Kubernetes 自动创建,并且会自动挂载到Pod`/run/secrets/kubernetes.io/serviceaccount`目录中

```shell
$ kubectl get pods -n kube-system
kube-flannel-ds-56jc9

$ kubectl exec -n kube-system kube-flannel-ds-56jc9 ls /run/secrets/kubernetes.io/serviceaccount
ca.crt
namespace
token
```

### Opaque Secret

Opaque 类型的数据是一个 map 类型，要求 value 是 base64 编码格式：

```shell
$ echo -n "admin" | base64
YWRtaW4=
$ echo -n "1f2d1e2e67df" | base64
MWYyZDFlMmU2N2Rm
```

secrets.yaml

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  password: MWYyZDFlMmU2N2Rm
  username: YWRtaW4=
```

#### 将 Secret 挂载到 Volume 中

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: seret-test
  name: seret-test
spec:
  volumes:
  - name: secrets
    secret:
      secretName: mysecret
  containers:
  - image: nginx:latest
    name: db
    volumeMounts:
    - name: secrets
      mountPath: "/etc/secret"
      readOnly: true
```

> k8s 会自动解码secret中的数据

查看结果

```shell
$ kubectl exec seret-test  cat /etc/secret/username
admin
```

#### 将 Secret 导出到环境变量中

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: pod-deployment
spec:
  replicas: 2
  template:
      metadata:
        labels:
          app: pod-deployment
      spec:
        containers:
        - name: pod-1
          image: nginx:latest
          imagePullPolicy: IfNotPresent
          command: ["/bin/sh", "-c", "env"]
          ports:
          - containerPort: 80
          env:
          - name: TEST_USER
            valueFrom:
              secretKeyRef:
                name: mysecret
                key: username
          - name: TEST_PASSWORD
            valueFrom:
              secretKeyRef:
                name: mysecret
                key: password
```

查看结果

```shell
$ kubectl logs pod-deployment-7f865f64d7-p99r2
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_SERVICE_PORT=443
HOSTNAME=pod-deployment-7f865f64d7-p99r2
HOME=/root
TEST_PASSWORD=1f2d1e2e67df
PKG_RELEASE=1~buster
TEST_USER=admin
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
NGINX_VERSION=1.19.3
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KUBERNETES_PORT_443_TCP_PORT=443
NJS_VERSION=0.4.4
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_SERVICE_HOST=10.96.0.1
PWD=/
```

### kubernetes.io/dockerconfigjson

使用 Kuberctl 创建 docker registry 认证的 secret

```shell
$kubectl create secret docker-registry myregistrykey --docker-server=DOCKER_REGISTRY_SERVER --docker-username=DOCKER_USER --docker-password=DOCKER_PASSWORD --docker-email=DOCKER_EMAIL
```

在创建 Pod 的时候，通过 imagePullSecrets 来引用刚创建的 `myregistrykey`

```shell
apiVersion: v1
kind: Pod
metadata:
  name: foo
spec:
    containers:
    - name: foo
      image: roc/awangyang:v1
    imagePullSecrets:
      - name: myregistrykey
```

## Volume

容器磁盘上的文件的生命周期是短暂的，这就使得在容器中运行重要应用时会出现一些问题。首先，当容器崩溃时，kubelet 会重启它，但是容器中的文件将丢失——容器以干净的状态（镜像最初的状态）重新启动。其次，在`Pod`中同时运行多个容器时，这些容器之间通常需要共享文件。Kubernetes 中的 Volume 抽象就很好的解决了这些问题

### 背景

Kubernetes 中的卷有明确的寿命 —— 与封装它的 Pod 相同。所以，卷的生命比 Pod 中的所有容器都长，当这个容器重启时数据仍然得以保存。当然，当 Pod 不再存在时，卷也将不复存在。也许更重要的是，Kubernetes支持多种类型的卷，Pod 可以同时使用任意数量的卷

### 卷的类型

Kubernetes 支持以下类型的卷：

* `awsElasticBlockStore` `azureDisk` `azureFile` `cephfs` `csi` `downwardAPI` `emptyDir`
* `fc` `flocker` `gcePersistentDisk` `gitRepo` `glusterfs` `hostPath` `iscsi` `local` `nfs`
* `persistentVolumeClaim` `projected` `portworxVolume` `quobyte` `rbd` `scaleIO` `secret`
* `storageos` `vsphereVolume`

### emptyDir

当 Pod 被分配给节点时，首先创建`emptyDir`卷，并且只要该 Pod 在该节点上运行，该卷就会存在。正如卷的名字所述，它最初是空的。Pod 中的容器可以读取和写入`emptyDir`卷中的相同文件，尽管该卷可以挂载到每个容器中的相同或不同路径上。当出于任何原因从节点中删除 Pod 时，`emptyDir`中的数据将被永久删除

`emptyDir`的用法有：

* 暂存空间，例如用于基于磁盘的合并排序
* 用作长时间计算崩溃恢复时的检查点
* Web服务器容器提供数据时，保存内容管理器容器提取的文件

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}
```

### hostPath

`hostPath`卷将主机节点的文件系统中的文件或目录挂载到集群中

`hostPath`的用途如下：

* 运行需要访问 Docker 内部的容器；使用 /var/lib/docker 的 hostPath
* 在容器中运行 cAdvisor；使用 `/dev/cgroups` 的 `hostPath`
* 允许 pod 指定给定的 hostPath 是否应该在 pod 运行之前存在，是否应该创建，以及它应该以什么形式存在

除了所需的`path`属性之外，用户还可以为`hostPath`卷指定`type`

| 值 | 行为 |
| :--- | :--- |
|  | 空字符串（默认）用于向后兼容，这意味着在挂载 hostPath 卷之前不会执行任何检查。 |
| `DirectoryOrCreate` | 如果在给定的路径上没有任何东西存在，那么将根据需要在那里创建一个空目录，权限设置为 0755，与 Kubelet 具有相同的组和所有权。 |
| `Directory` | 给定的路径下必须存在目录 |
| `FileOrCreate` | 如果在给定的路径上没有任何东西存在，那么会根据需要创建一个空文件，权限设置为 0644，与 Kubelet 具有相同的组和所有权。 |
| `File` | 给定的路径下必须存在文件 |
| `Socket` | 给定的路径下必须存在 UNIX 套接字 |
| `CharDevice` | 给定的路径下必须存在字符设备 |
| `BlockDevice` | 给定的路径下必须存在块设备 |
|  |  |

使用这种卷类型是请注意，因为：

* 由于每个节点上的文件都不同，具有相同配置（例如从 podTemplate 创建的）的 pod 在不同节点上的行为可能会有所不同
* 当 Kubernetes 按照计划添加资源感知调度时，将无法考虑 hostPath 使用的资源
* 在底层主机上创建的文件或目录只能由 root 写入。您需要在特权容器中以 root 身份运行进程，或修改主机上的文件权限以便写入 hostPath 卷

```shell
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      # directory location on host
      path: /data
      # this field is optional
      type: Directory
```

## PV

### 概念

#### `PersistentVolume`\(PV\)

是由管理员设置的存储，它是群集的一部分。就像节点是集群中的资源一样，PV 也是集群中的资源。 PV 是Volume 之类的卷插件，但具有独立于使用 PV 的 Pod 的生命周期。此 API 对象包含存储实现的细节，即 NFS，iSCSI 或特定于云供应商的存储系统

#### `PersistentVolumeClaim`\(PVC\)

是用户存储的请求。它与 Pod 相似。Pod 消耗节点资源，PVC 消耗 PV 资源。Pod 可以请求特定级别的资源（CPU 和内存）。声明可以请求特定的大小和访问模式（例如，可以以读/写一次或 只读多次模式挂载）

#### 静态 pv

集群管理员创建一些 PV。它们带有可供群集用户使用的实际存储的细节。它们存在于 Kubernetes API 中，可用于消费

#### 动态PV

当管理员创建的静态 PV 都不匹配用户的`PersistentVolumeClaim`时，集群可能会尝试动态地为 PVC 创建卷。此配置基于 `StorageClasses`：PVC 必须请求 \[存储类\]，并且管理员必须创建并配置该类才能进行动态创建。声明该类为 "" 可以有效地禁用其动态配置 要启用基于存储级别的动态存储配置，集群管理员需要启用 API server 上的`DefaultStorageClass`\[准入控制器\]。例如，通过确保 DefaultStorageClass 位于 API server 组件的 --admission-control 标志，使用逗号分隔的有序值列表中，可以完成此操作

#### 绑定

`master`中的控制环路监视新的 PVC，寻找匹配的 PV（如果可能），并将它们绑定在一起。如果为新的 PVC 动态调配 PV，则该环路将始终将该 PV 绑定到 PVC。否则，用户总会得到他们所请求的存储，但是容量可能超出要求的数量。一旦 PV 和 PVC 绑定后， PersistentVolumeClaim 绑定是排他性的，不管它们是如何绑定的。 PVC 跟PV 绑定是**一对一的映射**

### 持久化卷声明的保护

PVC 保护的目的是确保由 pod 正在使用的 PVC 不会从系统中移除，因为如果被移除的话可能会导致数据丢失当启用PVC 保护 alpha 功能时，如果用户删除了一个 pod 正在使用的 PVC，则该 PVC 不会被立即删除。PVC 的删除将被推迟，直到 PVC 不再被任何 pod 使用

### 持久化卷类型

`PersistentVolume`类型以插件形式实现。Kubernetes 目前支持以下插件类型：

* `GCEPersistentDisk` `AWSElasticBlockStore` `AzureFile` `AzureDisk` `FC (Fibre Channel)`
* `FlexVolume` `Flocker` `NFS` `iSCSI` `RBD` `(Ceph Block Device)` `CephFS`
* `Cinder(OpenStack block storage)` `Glusterfs` `VsphereVolume` `Quobyte` `Volumes`
* `HostPath` `VMware` `Photon` `Portworx` `Volumes` `ScaleIO` `Volumes` `StorageOS`

#### 示例

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0003
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: slow
  mountOptions:
  - hard
  - nfsvers=4.1
  nfs:
    path: /tmp
    server: 172.17.0.2
```

### PV访问模式

`PersistentVolume`可以以资源提供者支持的任何方式挂载到主机上。如下表所示，供应商具有不同的功能，每个PV 的访问模式都将被设置为该卷支持的特定模式。例如，NFS 可以支持多个读/写客户端，但特定的 NFS PV 可能以只读方式导出到服务器上。每个 PV 都有一套自己的用来描述特定功能的访问模式

* ReadWriteOnce——该卷可以被单个节点以读/写模式挂载
* ReadOnlyMany——该卷可以被多个节点以只读模式挂载
* ReadWriteMany——该卷可以被多个节点以读/写模式挂载

在命令行中，访问模式缩写为：

* RWO - ReadWriteOnce
* ROX - ReadOnlyMany
* RWX - ReadWriteMany

![image-20201016103237691](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20201016103237691.png)

### 回收策略

* Retain（保留）——手动回收
* Recycle（回收）——基本擦除（ rm -rf /thevolume/\* ）
* Delete（删除）——关联的存储资产（例如 AWS EBS、GCE PD、Azure Disk 和 OpenStack Cinder 卷）将被删除

当前，只有 NFS 和 HostPath 支持回收策略。AWS EBS、GCE PD、Azure Disk 和 Cinder 卷支持删除策略

> 现在NFS已经无法实现回收策略

### 状态

卷可以处于以下的某种状态：

* Available（可用）——一块空闲资源还没有被任何声明绑定
* Bound（已绑定）——卷已经被声明绑定
* Released（已释放）——声明被删除，但是资源还未被集群重新声明
* Failed（失败）——该卷的自动回收失败

命令行会显示绑定到 PV 的 PVC 的名称

### 示例

#### 安装NFS服务器

```shell
yum install -y nfs-common nfs-utils rpcbind
mkdir mkdir /nfs
chmod 666 /nfs
chown nfsnobody /nfsdata
# 输入配置文件
echo '/nfs *(rw,no_root_squash,no_all_squash,sync)' > /etc/exports
# 启动服务
systemctl start rpcbind
systemctl start nfs
```

#### 客户端挂载目录

```shell
# 查看共享目录
showmount -e NFSIP

# 挂载目录
mount -t nfs NFSIP:NFS路径 本地路径

# 停止挂载
umount 本地路径
```

#### 部署 PV

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv1
spec:
  capacity:
    storage: 5Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /nfs
    server: k8s-node-1
```

#### 创建服务并使用PVC

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "nginx"
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: k8s.gcr.io/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "nfs"
      resources:
        requests:
          storage: 1Gi
```

> `StatefulSet`必须先建立一个`headless Service`

### StatefulSet

* 匹配 Pod name \( 网络标识 \) 的模式为：$\(statefulset名称\)-$\(序号\)，比如上面的示例：web-0，web-1，web-2
* StatefulSet 为每个 Pod 副本创建了一个 DNS 域名，这个域名的格式为：`$(podname).(headless servername)`，也就意味着服务间是通过Pod域名来通信而非 Pod IP，因为当Pod所在Node发生故障时， Pod 会被飘移到其它 Node 上，Pod IP 会发生变化，但是 Pod 域名不会有变化

> 示例表示为 `web-0.nginx`, `web-1.nginx`, `web-2.nginx`,
>
> 在k8s集群中每个容器都可以访问的域名包括：
>
> * Service名
> * StatefulSet为每个 Pod 副本创建了一个 DNS 域名

* `StatefulSet`使用`Headless`服务来控制Pod的域名,这个域名的FQDN 为：`$(servicename).$(namespace).svc.cluster.local`，其中，`cluster.local` 指的是集群的域名根据 volumeClaimTemplates，为每个 Pod 创建一个 pvc，pvc 的命名规则匹配模式：`(volumeClaimTemplates.name)-(pod_name)`，比如上面的 volumeMounts.name=www， Podname=web-\[0-2\]，因此创建出来的 PVC 是 `www-web-0`、`www-web-1`、www-web-2
* 删除 Pod 不会删除其 pvc，手动删除 pvc 将自动释放 pv

Statefulset的启停顺序：

* 有序部署：部署StatefulSet时，如果有多个Pod副本，它们会被顺序地创建（从0到N-1）并且，在下一个Pod运行之前所有之前的Pod必须都是Running和Ready状态。
* 有序删除：当Pod被删除时，它们被终止的顺序是从N-1到0。
* 有序扩展：当对Pod执行扩展操作时，与部署一样，它前面的Pod必须都处于Running和Ready状态。

StatefulSet使用场景：

* 稳定的持久化存储，即Pod重新调度后还是能访问到相同的持久化数据，基于 PVC 来实现。
* 稳定的网络标识符，即 Pod 重新调度后其 PodName 和 HostName 不变。
* 有序部署，有序扩展，基于 init containers 来实现。
* 有序收缩。

### Mysql 单点 on K8S\(如何生成本地文件PV\)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
  labels:
    app: mysql
spec:
  type: NodePort
  selector:
      app: mysql
  ports:
  - protocol : TCP
    nodePort: 30306
    port: 3306
    targetPort: 3306 
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  storageClassName:  standard # 持久卷存储类型，它需要与持久卷申请的类型相匹配
  local:
    path: /root/database/mysql # 宿主机的目录
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
                - k8s-node-2 # Node的名字
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
  labels:
    app: mysql
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: "standard"
  resources:
    requests:
      storage: 1Gi #持久卷的容量是 1 GB
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-deployment
spec:
  selector:
    matchLabels:
      app: mysql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - image: mysql:5.7
          name: mysql-con
          imagePullPolicy: Never
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: root
            - name: MYSQL_USER
              value: dbuser
            - name: MYSQL_PASSWORD
              value: dbuser
          args: ["--default-authentication-plugin=mysql_native_password"]
          ports:
            - containerPort: 3306
              name: mysql
          volumeMounts: # 挂载Pod上的卷到容器
            - name: mysql-persistent-storage # Pod上卷的名字，与“volumes”名字匹配
              mountPath: /var/lib/mysql # 挂载的Pod的目录
      volumes:   # 挂载持久卷到Pod
        - name: mysql-persistent-storage # 持久卷名字， 与“volumMounts”名字匹配
          persistentVolumeClaim: 
            claimName: mysql-pv-claim  # 持久卷申请名字
```

