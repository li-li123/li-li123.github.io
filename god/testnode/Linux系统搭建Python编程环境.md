# 搭建Python编程环境
## 1. Linux系统安装Python编程环境

Linux系统中默认安装python

## 1. 检查Python版本
1. 打开终端窗口（快捷键——Ctrl+Alt+T)

   ```php
   $python
   ```

2. 关闭终端窗口（快捷键——Ctrl+D/ext())
3. 要是检查系统是否安装Python3
```php
$python3
```
## 2. 安装文本编辑器
Geany 是一款简单的文本编辑器
原因：	
	1. 易安装
	2. 能够直接运行几乎所有的程序
	3. 使用不同的颜色来显示代码，以突出代码语法
	4. 在终端窗口中运行代码
```php
$sudo aot-get install geany
```
## 3. 运行Hello World程序
1. 启动Geany
2. 按Windows键并在系统中搜索Geany，找到Geany后，双击启动它；
3. 将Gany拖拽到任务栏或桌面上，已创建一个快捷方式。
4. 创建一个存储存储项目文件夹，并将其命名。命名规则（小写，且下划线表示空格）
5. 选择Geany 选择菜单File→Save As将python文件保存到文件夹中，扩展名为".py"
```python
print（"Hello Python world!")
```
### 注意
如果系统中安装了多个Python版本，需要对Geany进行配置
配置方法： 菜单Build(生成)>Set Build Commands(设置生成命令)；将看到文字Compile (编译)和Excute(执行)，旁边有个命令，默认情况下，这两个命令都是python，要让Geany使用命令python3
### 终端执行python3
```python
python3 -m py_compile "%f"
```
必须完全按照上面的代码显示的那样输出这个命令，确保空格和大小写完全相同
```python
python3 "%f"
```
