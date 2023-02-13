---
description: 安装k8s
---

## 系统初始化

### 升级系统内核为 4.44

CentOS 7.x 系统自带的 3.10.x 内核存在一些 Bugs，导致运行的 Docker、Kubernetes 不稳定，例如： rpm -Uvh [http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm](http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm)

```shell
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
# 安装完成后检查 /boot/grub2/grub.cfg 中对应内核 menuentry 中是否包含 initrd16 配置，如果没有，再安装一次！
yum --enablerepo=elrepo-ke# 系统初始化

## 升级系统内核为 4.44

CentOS 7.x 系统自带的 3.10.x 内核存在一些 Bugs，导致运行的 Docker、Kubernetes 不稳定，例如： rpm -Uvh
http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm

​```shell
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
# 安装完成后检查 /boot/grub2/grub.cfg 中对应内核 menuentry 中是否包含 initrd16 配置，如果没有，再安装一次！
yum --enablerepo=elrepo-kernel install -y kernel-lt
# 设置开机从新内核启动
grub2-set-default 'CentOS Linux (4.4.189-1.el7.elrepo.x86_64) 7 (Core)'
```

### 安装依赖

```shell
yum install -y conntrack ntpdate ntp ipvsadm ipset jq iptables curl sysstat libseccomp wget vim net-tools git
```

### 设置防火墙未iptables 并设置空规则

```shell
systemctl stop firewalld && systemctl disable firewalld 

yum -y install iptables-services && systemctl start iptables && systemctl enable iptables && iptables -F && service iptables save
```

### 关闭SELINUX和虚拟内存

```shell
swapoff -a && sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab # 关闭虚拟内存， k8s认为pod运行在虚拟内存中，性能会损失很多
setenforce 0 && sed -i 's/^SELINUX=.*/SELINX=disabled/' /etc/selinux/config
```

### 调整内核参数，对于 K8S

```shell
cat > kubernetes.conf <<EOF
net.bridge.bridge-nf-call-iptables=1 # 开启网桥转发
net.bridge.bridge-nf-call-ip6tables=1 # 开启转发
net.ipv4.ip_forward=1
net.ipv4.tcp_tw_recycle=0
vm.swappiness=0 # 禁止使用 swap 空间，只有当系统 OOM 时才允许使用它
vm.overcommit_memory=1 # 不检查物理内存是否够用
vm.panic_on_oom=0 # 开启 OOM
fs.inotify.max_user_instances=8192
fs.inotify.max_user_watches=1048576
fs.file-max=52706963
fs.nr_open=52706963
net.ipv6.conf.all.disable_ipv6=1 # 关闭ipv6
net.netfilter.nf_conntrack_max=2310720
EOF
```

```shell
cp kubernetes.conf /etc/sysctl.d/kubernetes.conf # 内核为3.x时会报某个目录不存在，所以需要升级内核
sysctl -p /etc/sysctl.d/kubernetes.conf
```

### 调整系统时区

```shell
# 设置系统时区为 中国/上海
timedatectl set-timezone Asia/Shanghai
# 将当前的 UTC 时间写入硬件时钟
timedatectl set-local-rtc 0
# 重启依赖于系统时间的服务
systemctl restart rsyslog
systemctl restart crond
```

### 关闭系统不需要服务

```shell
systemctl stop postfix && systemctl disable postfix
```

### 设置 rsyslogd 和 systemd journald

```shell
mkdir /var/log/journal # 持久化保存日志的目录
mkdir /etc/systemd/journald.conf.d
cat > /etc/systemd/journald.conf.d/99-prophet.conf <<EOF
[Journal]
# 持久化保存到磁盘
Storage=persistent
# 压缩历史日志
Compress=yes
SyncIntervalSec=5m
RateLimitInterval=30s
RateLimitBurst=1000
# 最大占用空间 10G
SystemMaxUse=10G
# 单日志文件最大 200M
SystemMaxFileSize=200M
# 日志保存时间 2 周
MaxRetentionSec=2week
# 不将日志转发到 syslog  ！！重要！！
ForwardToSyslog=no
EOF

systemctl restart systemd-journald
```

## Kubeadm 部署安装

### kube-proxy开启ipvs的前置条件

```shell
modprobe br_netfilter
cat > /etc/sysconfig/modules/ipvs.modules <<EOF
#!/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4
EOF
chmod 755 /etc/sysconfig/modules/ipvs.modules && bash /etc/sysconfig/modules/ipvs.modules && lsmod | grep -e ip_vs -e nf_conntrack_ipv4
```

### 安装 Docker 软件

```shell
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager \
--add-repo \
http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum update -y && yum install -y docker-ce
## 创建 /etc/docker 目录
mkdir /etc/docker
# 配置 daemon.
# 设置日志方便日后收集
cat > /etc/docker/daemon.json <<EOF
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "log-driver": "json-file", 
    "log-opts": {
        "max-size": "100m"
    },
    "registry-mirrors": ["https://eec8k1sz.mirror.aliyuncs.com"]
}
EOF
mkdir -p /etc/systemd/system/docker.service.d
# 重启docker服务
systemctl daemon-reload && systemctl restart docker && systemctl enable docker
```

### 添加阿里云YUM软件源

```shell
cat > /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```

```shell
# 导入gpgkey文件
wget https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
rpm --import yum-key.gpg
wget https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
rpm --import rpm-package-key.gpg
```

### 安装kubeadm，kubelet和kubectl

```shell
yum install -y kubelet-1.15.1 kubeadm-1.15.1 kubectl-1.15.1
systemctl enable kubelet
```

### 修改主节点配置文件

```shell
kubeadm config print init-defaults > kubeadm-config.yaml

vi kubeadm-config.yaml
```

修改后的文件

```yaml
apiVersion: kubeadm.k8s.io/v1beta2
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 192.168.195.131 # 修改成master地址
  bindPort: 6443
nodeRegistration:
  criSocket: /var/run/dockershim.sock
  name: k8s-master
  taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
---
apiServer:
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta2
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns:
  type: CoreDNS
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: registry.aliyuncs.com/google_containers # 使用阿里云镜像
kind: ClusterConfiguration
kubernetesVersion: v1.15.1 # 更正版本
networking:
  dnsDomain: cluster.local
  podSubnet: "10.244.0.0/16" # 添加pod网段，使其支持flannel插件
  serviceSubnet: 10.96.0.0/12
# 添加以下内容 把调度方式设置为IPVS模式 
--- 
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
featureGates:
        SupportIPVSProxyMode: true
mode: ipvs
scheduler: {}
```

### 初始化主节点

```shell
# 使用阿里云镜像，进行初始化
kubeadm init --config=kubeadm-config.yaml --experimental-upload-certs | tee kubeadm-init.log
```

### 部署网络

```shell
# 一键安装
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

### Node加入集群

```shell
# 每个node上运行masterlog里面输出的加入命令
kubeadm join 192.168.1.80:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:74983294c0fbd977dc002f96a19dbd271340a1de9ab9a1f95c55ba1522d83073

# 查看节点启动情况
kubectl get pod -n kube-system -o wide -w
```

### 重置节点

```shell
kubeadm reset
```

## kubectl 常用命令

```shell
# 获取pod
kubectl get pod -n kube-system -w  -o wide
-n 获取指定namespace中的pod
-w 刷新
-o wide 详细信息
--show-labels 查看标签

# 删除pod
kubectl delete pod nginx-deployment-8859878f8-crzrs 

# 给pod打标签
kubectl label pod frontend-9b2wx a=b

# pod重写标签
kubectl label pod frontend-9b2wx a=b --overwrite=True

# 删除全部pod
kubectl delete pod --all

# 描述Pod
kubectl describe pod my-app


# 删除 rs
kubectl delete rs
--all 全部

# 创建deployment
kubectl run nginx-deployment --image=nginx --port=80 --replicas=1
--image 镜像
--port pod 端口
--replicas 副本数

# 扩容deployment
kubectl scale --replicas=3 deployment/nginx-deployment


# 创建svc
kubectl expose deployment nginx-deployment --port=30000 --target-port=80
expose deployment [deployment 名称]   
--port 释放端口      
--target--port pod端口

# 获取svc
kubectl get svc
-w 刷新

# 修改svc配置
kubectl edit svc nginx-deployment

# 获取configMap
kubectl get configmaps special-config -o yaml

# 获取pv
kubectl get pv

# 常用的debug容器
kubectl run -i --tty --rm debug --image=busybox --restart=Never -- sh

# 查看日志
kubectl log my-app -c text
-c 指定具体的容器
```

rnel install -y kernel-lt


