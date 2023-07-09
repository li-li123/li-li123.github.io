## 自动化优点

1. 时间和效率：自动化可以最大化利用时间，有效缩短测试周期，从而使软件更快地推向市场。
2. 精确性和一致性: 认为测试有较大的误差型，不一定能够每次都把每个测试点覆盖完全，但自动化测试能够准确地重复相同的操作，并记录每一步的结果，降低了疏忽和误差的可能性。
3. 更广泛的测试范围: 自动化测试能够覆盖更多的测试场景，例如高负载或压力测试，这是手动测试难以办到的。
4. 可重复：自动化测试用例可以在任何时间重复执行，特别是在代码修改或增加新功能后。
5. 提高团队的生产力：当测试通过自动化来完成，测试人员就可以把更多的时间和精力集中在复杂的测试场景和新功能的测试上。
6. 提供可靠的测试报告：根据自动化测试的结果，能产生详细的测试报告

## 自动化缺点

1.初期投入大，优化、调试需要投入，对测试人员的技术要求高

2.自动化测试测试点比较固定，主要考虑的是功能性问题，可能会忽视用户体验相关的问题。（一般在测试周期内测试人员会针对特性进行发散测试）

3.非功能性测试难以实现： 某些类型的测试，如用户界面的一致性、易用性、可访问性等非功能性测试（在实际测试够成中，想这类问题取决于自动化对桌面定位的方式，比如web测试，主流方式是通过Selenium定位元素，相对来说对用户界面依赖性不大，所以在用户界面功能性方面需要特别注意，如果是通过对软件在桌面显示位置进行定位，一般对用户界面的依赖性比较大，所以不需要过分关注。

## Web网页自动化测试

### 什么是Selenium，Selenium的功能是什么

Selenium 是一款十分流行的开源自动化测试框架，主要用于 web 应用程序的自动化测试。

以下是 Selenium 的一些主要功能：

1. 跨浏览器支持：Selenium 支持所有主流的 web 浏览器，如 Chrome、Firefox、Safari、Edge 等，使得你可以在多种浏览器环境下执行你的测试脚本。
2. 多编程语言支持: Selenium 提供了一系列驱动程序，支持多种编程语言，包括 Java、Python、C#、Ruby、JavaScript等。
3. 各种操作支持：Selenium WebDriver 可以模拟用户的各种操作，如点击按钮、输入文本、操作滑块、拖拽元素、选择下拉菜单等。
4. 截图功能：Selenium 可以截取 web 应用的屏幕截图，用于捕捉测试过程中的问题和错误。
5. 集成支持：Selenium 能够与许多测试工具和框架配合使用，如测试管理工具TestNG，持续集成工具Jenkins等。
6. 支持异步测试：适用于 AJAX 和大量 JavaScript 的 web 应用。
7. 支持分布式测试：可以在不同的环境和机器上并行处理多个测试。
8. 开源社区：Selenium 由一个活跃的开源社区维护，有很多的学习资源、教程和解决方案。

通过使用 Selenium，开发者和测试者可以编写出强大的自动化测试脚本，提升测试效率，保障软件产品的质量。

### 安装Selenium IDE

1.进入Selenium网站：https://www.selenium.dev/downloads/

![image-20230709180431880](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20230709180431880.png)

2.根据不同的浏览器选择所要安装的Selenium IDE

## Selenium的使用

### Selenium对Web的定位方法分为哪几类

8类：ID定位、name定位、Class Name定位、Tag Name定位、Link Text定位、partial Link定位、CSS Selector定位、Xpath定位

1. 通过ID定位：这是最直接也是最常用的定位方式，只要元素的id是唯一的。

2. 通过Name定位：对于有Name属性的元素可以使用Name定位。

3. 通过Class Name定位：对于有Class属性的元素可以使用Class Name定位。

4. 通过Tag Name定位：可以通过标签名进行定位，通常用于查找一组或多个具有相同标签名称的元素。

5. 通过Link Text定位：对于链接（`<a>`标签），可以直接通过链接的文本进行定位。

6. 通过Partial Link Text定位：对于文本过长的链接，可以通过链接的部分文本进行定位。

7. 通过CSS Selector定位：可以使用CSS选择器定位元素，这是一种非常强大而灵活的定位方式。

8. 通过XPath定位：XPath 是一种在 XML 文档中查找信息的语言，可以用来在 HTML 中定位元素。这也是一种非常强大的定位方式，尤其是在其他方式难以定位元素的情况下。

   ### Selenium引用的库

   ```python
   import time
   from selenium import webdriver
   from selenium.webdriver import ActionChains
   from selenium.webdriver.common.by import By
   from auto_config import *
   ```

### Selenium实例化浏览器

```python
# 实例化Edge浏览器
driver = webdriver.Edge()
#实例化火狐浏览器
driver1 = webdriver.Firefox()
#实例化谷歌浏览器
driver2 = webdriver.Chrome()
```

### Selenium打开相应的网站页面

```python
# 打开网站页面
taobao_url = "https:\\login.taobao.com\\member\\" \
             "login.jhtml?spm=a21bo.jianhua.754894437.1.5af92a89jZkEEn&f=top&redirect" \
             "URL=https%3A%2F%2Fwww.taobao.com%2F"
driver.get(taobao_url)
```

### Selenium元素定位方法

```
# ID定位方法
element = driver.find_element(By.ID, "fm-login-id")
element.send_keys("18292811977")
```

