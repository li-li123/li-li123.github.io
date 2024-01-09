# 元素定位技术 

其实 CSS 定位元素的基础依然是 HTML文档中元素的属性，只是通过CSS语法我们可以组合成条件和层次都更加丰富的定位语句。在具体学习复杂的定位之前我们先来学习一下CSS的基本定位语法，如表所示

​                                                 CSS定位语法

| 定位资源  | 语法              | 样例      | 说明                         |
| --------- | ----------------- | --------- | ---------------------------- |
| ID        | #ID               | #kw       | 匹配id = kw的元素            |
| Class     | .Class            | .fly      | 匹配所有class= fly的元素     |
| TagName   | Element           | input     | 匹配所有的input元素          |
| Attribute | [attribute]       | [name]    | 匹配所有具有 name 属性的元素 |
|           | [attribute=value] | [name=su] | 匹配所有 name=su 的元素      |

上面是CSS常用的基本语法，通过这些基础语法就可以组合出更多的定位语句。关于Selenium 支持的 CSS 更多的定位语法可以访问 http:/www.testdoc.org 进行学习。接下来针对前面所列出的几种复杂情况进行CSS定位，

- 获取匹配多个元素中的指定一个

  ```python
  table>tr:nth-chile(1) # 定位table元素下的第1个tr元素
  ```

- 使用更多的元素属性

  ```python
  input[type=text][calue=1]  #定位type为text，value为1的input元素
  ```

- 综合使用不同的属性

  ```python
  input.fly[name=wd] # 定位class为fly，name为wd的input元素
  ```

- 分层定位元素

  ```python
form>table>a[class=dot] # 定位form下的table下的class为dot的a元素
  ```

- 定位特定文本内容的元素。

  ```python
lable:contains('userName')  #  定位包含userName文字的label元素
  ```
  
  
