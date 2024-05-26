## 手机Android测试
### 安装abd
1. 下载adb
    在Android 官网下载
    https://developer.android.com/tools/releases/platform-tools?hl=zh-cn

  ![image-20240526173823431](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20240526173823431.png)
2. 安装adb完成，配置环境变量

   ![image-20240526194728351](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20240526194728351.png)


3. 验证adb
```sh
$ adb version
```
### 手机进入开发者模式
1. Android手机进入方法：[设置]>[关于手机] 连续点击版本号，直至提醒进入了开发者模式
2. 进入[系统]>[高级选项] >[开发者选项]
3. 开启之后，打开USB调试授权
### adb命令调测手机
1. 启动adb服务
```sh
adb start-server
```
1. 获取当前设备连接
```sh
 adb devices
```
1. 唤醒手机
```sh
adb shell input keyevent 26
```
1. adb命令安装apk
```sh
$ adb install '安装软件在电脑中的路径'
```
1. 卸载apk
```sh
adb -unstall [-k] <应用包名>
```
[-k]:参数可选，表示卸载应用但保留数据和缓存目录；
1. 清除应用数据和缓存
``` sh
$ adb ahell pm clear 包名
```
1. 耗电量信息
```sh
$ adb shell dumpsysy 包名
```
1. CPU使用率信息
```sh
adb shell dumpsys cpuinfo
```
1. 日志获取
```sh
$ adb shell am logcat>路径
```
将所有的日志信息全部写入指定文件中，其中>表示覆盖，>>表示追加
如果需要筛选日志，如果筛选警告以上级别的日志
```sh
$ adb shell am logcat *W>文件保存路径
```
日志主要有以下几个级别：
V-verbose: 所有的信息全部输出，其日志级别是最低的
D-debug：（调试日志信息）
I-info：一般日志信息
W-warning：警告信息
E-error：错误信息

