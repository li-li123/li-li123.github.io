# 12-prometheus

## 项目地址

Prometheus github 地址：[https://github.com/coreos/kube-prometheus](https://github.com/coreos/kube-prometheus)

## 组件说明

1. MetricServer：是kubernetes集群资源使用情况的聚合器，收集数据给kubernetes集群内使用，如kubectl,hpa,scheduler等
2. PrometheusOperator：是一个系统监测和警报工具箱，用来存储监控数据。
3. NodeExporter：用于各node的关键度量指标状态数据。 
4. KubeStateMetrics：收集kubernetes集群内资源对象数据，制定告警规则。 
5. Prometheus：采用pull方式收集apiserver，scheduler，controller-manager，kubelet组件数据，通过http协议传输。
6. Grafana：是可视化数据统计和监控平台

## 下载代码

```shell
git clone https://github.com/coreos/kube-prometheus.git
```

```shell
cd ./kube-prometheus/manifests/
```

## 修改配置

修改`grafana-service.yaml` 文件，使用 nodepode 方式访问 grafana：

```shell
apiVersion: v1
kind: Service
metadata:
  labels:
    app: grafana
  name: grafana
  namespace: monitoring
spec:
  type: NodePort # 添加内容
  ports:
  - name: http
    port: 3000
    targetPort: http
    nodePort: 30100 # 添加内容
  selector:
    app: grafana
  type: NodePort
```

修改`prometheus-service.yaml`，改为 nodeport

```shell
apiVersion: v1
kind: Service
metadata:
  labels:
    prometheus: k8s
  name: prometheus-k8s
  namespace: monitoring
spec:
  type: NodePort # 添加
  ports:
  - name: web
    port: 9090
    targetPort: web
    nodePort: 30200 # 添加
  selector:
    app: prometheus
    prometheus: k8s
  sessionAffinity: ClientIP
```

修改 `alertmanager-service.yaml`，改为 nodepode

```shell
apiVersion: v1
kind: Service
metadata:
  labels:
    alertmanager: main
  name: alertmanager-main
  namespace: monitoring
spec:
  type: NodePort # 添加
  ports:
  - name: web
    port: 9093
    targetPort: web
    nodePort: 30300 # 添加
  selector:
    alertmanager: main
    app: alertmanager
  sessionAffinity: ClientIP
```

## 创建

```shell
kubectl create -f manifests/
```

