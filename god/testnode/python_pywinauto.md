# pywinauto
## 概念
`pywinauto` 是一个用于自动化Python模块，适合Windows系统的软件（GUI)，可以通过`Pywinauto`遍历窗口（对话框）和窗口里的控件，也可以控制鼠标和键盘输入。

## 打开应用软件
```python
# app_path:如果打开应用是系统自带则直接输入exe文件名，否则需要输入exe文件路径
app = Application(backend= 'uia').start(app_path)
print(app.windows)
```
###  backend值的确定
1. `backend`值大致有两种，分别是win32，uia，默认win32
	首先要判断程序是用什么语言写的？在实例化会有区别，主要是判断程序的backend？
（1）Win32 API(backend=“win32”）
（2）MS UI Automation(backend=“uia”）
	
2. 使用工具判断应用程序使用的是那种语言：
	推荐使用spy++和inspect来检查(https://github.com/blackrosezy/gui-inspect-tool)
 将inspect左上角的下拉列表中切换到`UI Automation`,然后鼠标点一下需要测试的程序窗体，inspect就会显示相关信息。inspect中显示了相关的信息，如下图所示，说明backend为`uia`
    如果inspect中显示拒绝访问，说明backend应该是win32
## 连接应用软件
```python
# 连接软件应用
app = Application(backend='uia').connect(title_re= 'data.txt - 记事本')
print(app.windows)

app = Application(backend='uia').connect(handle= 0x00150866)
print(app.windows)

app = Application(backend='uia').connect(process= 35196)
print(app.windows)

```
执行结果：
```python
<bound method Application.windows of <pywinauto.application.Application object at 0x000001E4FF684B50>>
<bound method Application.windows of <pywinauto.application.Application object at 0x000001E482D2F940>>
<bound method Application.windows of <pywinauto.application.Application object at 0x000001E4FF684B50>>
```
