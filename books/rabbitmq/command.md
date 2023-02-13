## 常用管理
### 启动

```shell
rabbitmqctl start_app
```

### 关闭

```shell
rabbitmqctl stop_app
```

### 节点状态

```shell
rabbitmqctl status
```

### 移除全部数据

要在stop_app之后使用

```shell
rabbitmqctl reset
```

### 加入集群

```shell
join_cluster --ram <clusternode>
```

### 改变该节点在集群的存储模式

```shell
rabbitmqctl change_cluster_node_type disc|ram
```

### 忘记节点(删除节点)

```shell
rabbitmqlctl forget_cluster_node <nodename> --offline(可选,表示本地没有节点，离线方式操作集群)
```

### 修改节点名称

```shell
rabbitmqctl rename_cluster_node oldnode1 newnode1 .....
```

### 启用管理插件

```shell
rabbitmq-plugins enbale rabbitmq_management
```

### 查看插件

```shell
rabbitmq-plugins list
```

## 用户操作

### 列出所有用户

```shell
rabbitmqctl list_users
```

### 添加用户

```shell
rabbitmqctl add_user username passwd
```

### 删除用户

```shell
rabbitmqctl delete_user username
```

### 修改密码

```shell
rabbitmqctl add_user username passwd
```

### 设置角色

```shell
rabbitmqctl set_user_tags {username} {tag ...}
# 管理员 角色 administrator
```

### 权限设置

```shell
rabbitmqctl set_permissions [-pvhostpath] {user} {conf} {write} {read}
Vhostpath：虚拟主机，表示该用户可以访问那台虚拟主机；
user：用户名。
Conf：一个正则表达式match哪些配置资源能够被该用户访问。
Write：一个正则表达式match哪些配置资源能够被该用户设置。
Read：一个正则表达式match哪些配置资源能够被该用户访问。
```

### 清除用户所有权限

```shell
rabbitmqctl clear_permissions -p vhostpath <username>
```

### 列出用户权限

```shell
rabbitmqctl list_user_permissions <username>
```

## 虚拟主机命令

### 创建虚拟主机

```shell
rabbitmqctl add_vhost /ning
```

### 列出全部虚拟主机

```shell
rabbitmqctl list_vhosts
```

### 列出虚拟主机权限

```shell
rabbitmqctl list_permissions -p /ning
```

### 删除虚拟主机

```shell
rabbitmqctl delete_vhost /ning
```

## 队列

### 查看所有队列

```shell
 rabbitmqctl list_queues
```

### 清除队列消息

```shell
rabbitmqctl -p vhostpath purge_queue <queue>
```

## 交换机

### 列出全部交换机

```shell
rabbitmqctl list_exchanges
```