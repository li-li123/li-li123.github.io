##  下载镜像

```shell
docker pull rabbitmq:3.6.15-management
```

带--management 标签的镜像是带网页控制台的镜像

## 启动单台实例

```shell
docker run -d --hostname rabbit --name myrabbit -p 15672:15672 -p 5672:5672 rabbitmq:3.6.15-management
```

参数说明

* -d 后台运行
* --hostname  设置hostname
* --name 容器名称
* -p 映射端口

## 启动集群

步骤一：安装RabbitMQ；

步骤二：加入RabbitMQ节点到集群；

### 步骤一

1. 安装RabbitMQ

```shell
docker run -d --hostname rabbit1 --name myrabbit1 -p 15672:15672 -p 5672:5672 -e RABBITMQ_ERLANG_COOKIE='rabbitcookie' rabbitmq:3.6.15-management
```

```shell
docker run -d --hostname rabbit2 --name myrabbit2 -p 5673:5672 --link myrabbit1:rabbit1 -e RABBITMQ_ERLANG_COOKIE='rabbitcookie' rabbitmq:3.6.15-management
```

```shell
docker run -d --hostname rabbit3 --name myrabbit3 -p 5674:5672 --link myrabbit1:rabbit1 --link myrabbit2:rabbit2 -e RABBITMQ_ERLANG_COOKIE='rabbitcookie' rabbitmq:3.6.15-management
```

参数说明

* --link 是在主机中添加一个通往另一个容器的路由
* Erlang Cookie值必须相同，也就是RABBITMQ_ERLANG_COOKIE参数的值必须相同，原因见下文“配置相同Erlang Cookie”部分

### 步骤二

设置节点1

```shell
$ docker exec -it myrabbit1 bash
$ rabbitmqctl stop_app
$ rabbitmqctl reset
$ rabbitmqctl start_app
# 退出容器
crtl+P+Q
```

设置节点2

```shell
$ docker exec -it myrabbit2 bash
$ rabbitmqctl stop_app
$ rabbitmqctl reset
$ rabbitmqctl join_cluster --ram rabbit@rabbit1
$ rabbitmqctl start_app

# 退出容器
crtl+P+Q
```

参数说明

* --ram 是设定为内存节点，忽略次参数默认为磁盘节点。

设置节点3

```shell
$ docker exec -it myrabbit3 bash
$ rabbitmqctl stop_app
$ rabbitmqctl reset
$ rabbitmqctl join_cluster --ram rabbit@rabbit1
$ rabbitmqctl start_app

# 退出容器
crtl+P+Q
```

设置好之后，使用http://物理机ip:15672 进行访问了，默认账号密码是guest/guest，效果如下图：

![image-20200416202439826](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20200416202439826.png?x-oss-process=style/default)
### 启用高可用镜像模式

```shell
rabbitmqctl set_policy ha-all "^" '{"ha-mode":"all"}'
```

参数意思为：

* ha-all：为策略名称。

* ^：为匹配符，只有一个^代表匹配所有，^zlh为匹配名称为zlh的exchanges或者queue。

* ha-mode：为匹配类型，他分为3种模式：all-所有（所有的queue），exctly-部分（需配置ha-params参数，此参数为int类型比如3，众多集群中的随机3台机器），nodes-指定（需配置ha-params参数，此参数为数组类型比如["3rabbit@F","rabbit@G"]这样指定为F与G这2台机器。）。

### 高可用配置

1. docker镜像

   ```shell
   docker pull haproxy
   ```

2.  设置配置文件

   ```text
   global
           daemon
           # nbproc 1
           # pidfile /var/run/haproxy.pid
           # 工作目录
           chroot /usr/local/etc/haproxy
   
   defaults
           log 127.0.0.1 local0 err #[err warning info debug]
           mode tcp                #默认的模式mode { tcp|http|health }，tcp是4层，http是7层，health只会返回OK
           option tcplog
           option dontlognull
           retries 3                #两次连接失败就认为是服务器不可用，也可以通过后面设置
           option redispatch        #当serverId对应的服务器挂掉后，强制定向到其他健康的服务器
           option abortonclose      #当服务器负载很高的时候，自动结束掉当前队列处理比较久的链接
           maxconn 4096             #默认的最大连接数
           timeout connect 5000ms   #连接超时
           timeout client 30000ms   #客户端超时
           timeout server 30000ms   #服务器超时
           #timeout check 2000      #=心跳检测超时
   
   
   ######## 监控界面配置 #################
   listen status
           # 监控界面访问信息
           bind 0.0.0.0:8100
           mode http
           stats enable
           # URI相对地址
           stats uri /rabbitmq-stats
           # 统计报告格式
           stats realm Global\ statistics
           # 登录账户信息
           stats refresh 5s
   # 集群设置
   listen rabbitmq_cluster
           bind 0.0.0.0:5672
           mode tcp
           balance roundrobin
           server myrabbit1 myrabbit1:5672 check inter 5000 rise 2 fall 2
           server myrabbit2 myrabbit2:5672 check inter 5000 rise 2 fall 2
           server myrabbit3 myrabbit3:5672 check inter 5000 rise 2 fall 2
   ```

3.  启动 Haproxy

```shell
docker run -d --name haproxy1 -p 80:80 -p 443:443 -p 2222:2222 --link myrabbit1:rabbit1 --link myrabbit2:rabbit2 --link myrabbit3:rabbit3 -p 9090:9090 --restart=always -v /usr/local/etc/haproxy:/usr/local/etc/haproxy haproxy
```



## 附录

### 镜像中的RabbitMQ地址

```shell
/usr/lib/rabbitmq
```

### 为什么要配置相同的erlang cookie？

```text
因为RabbitMQ是用Erlang实现的，Erlang Cookie相当于不同节点之间相互通讯的秘钥，Erlang节点通过交换Erlang Cookie获得认证。
```

### Erlang Cookie的位置

```text
默认在 /var/lib/rabbitmq
```

### 用户设置

```shell
新建用户：rabbitmqctl add_user username passwd
删除用户：rabbitmqctl delete_user username
改密码: rabbimqctl change_password {username} {newpassword}
设置用户角色：rabbitmqctl set_user_tags {username} {tag ...}

rabbitmqctl set_permissions -p / username ".*" ".*" ".*"  //添加权限
```

### 权限说明

```shell
rabbitmqctl set_permissions [-pvhostpath] {user} {conf} {write} {read}
Vhostpath：虚拟主机，表示该用户可以访问那台虚拟主机；
user：用户名。
Conf：一个正则表达式match哪些配置资源能够被该用户访问。
Write：一个正则表达式match哪些配置资源能够被该用户设置。
Read：一个正则表达式match哪些配置资源能够被该用户访问。
```

### 虚拟主机

```shell
# 创建一个虚拟主机
rabbitmqctl add_vhost vhost_name
# 删除一个虚拟主机
rabbitmqctl delete_vhost vhost_name
```

### 添加超级用户

```shell
rabbitmqctl add_user username passwd  //添加用户，后面两个参数分别是用户名和密码
rabbitmqctl set_permissions -p / username ".*" ".*" ".*"  //添加权限
rabbitmqctl set_user_tags username administrator  //修改用户角色,将用户设为管理员
```