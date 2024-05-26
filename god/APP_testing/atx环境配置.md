## ATX 环境配置
### adb连接设备
```sh
$ adb devices
```
### 安装uiautomator库
```sh
$ pip install -u uiautomator2
```
### 查看UI层级结构
1. 访问https://github.com/codeskyblue/uiautodev

   ![image-20240526183205104](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20240526183205104.png)

2. 安装uiauto.dev
```sh
$ pip install uiautodev
```
3. 安装完成之后，输入如下命令，会自动打开[uiauto.dev](https://uiauto.devsleep.com/)

https://github.com/codeskyblue/uiautodev

![image-20240526184304016](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20240526184304016.png)
4，该界面可以辅助定位界面的属性和坐标

![image-20240526193958450](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images/image-20240526193958450.png)

### 以测试快手app为例
1. 引入`uiautomator2`包
```python
import uiautomator2 as u2
```


