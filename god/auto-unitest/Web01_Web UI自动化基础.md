# 01 Web UI自动化基础
## 1.1 HTML与DOM简介
1. HTML 超文本标记语言，是网页制作与Web开发所使用的语言。他不是编程语言，而是标记；
2. DOM是浏览器创建的对象，是W3C组织推荐的处理可扩展语言的标准编程接口。是浏览器在解析HTML页面的过程中生成的一个内部对象。在OM对象中吧页面（或文档）的对象都组织在一个树状结构中，器树状结构中的每一个对象都是与源HTML中的节点一一对应的。
3. 浏览器最终在渲染和显示页面内容的时候正是基于DOM对象的内容而来的，并且DOM对象一旦被修改浏览器将会重新渲染页面内容。而另一方面DOM本身就是一个可编程的接口，即我们可以通过编程的方法调用它。简而言之，我们可以通过编程来动态改变页面显示的效果。
4. 大部分基于Web的自动化测试工具都是通过操作DOM来控制浏览器行为的；而我们在进行自动化测试脚本开发的时候，其中一个重要的知识点就是如何定位DOM中的元素；在定位到元素之后自动化工具就可以对其DOM节点进行相关操作，来实现自动化测试Web页面效果。
### 什么是DOM
### DOM
### DOM含义
 文档对象模型（Document Obiect Model，简称DOM），是W3C组织推荐的处理可扩展置表语言的标准编程接口、它是一种与平台和语言无关的应用程序接口（API），可以动态的访问程序和脚本，更新其内容、结构和www文档的风格（HTML和XML文档是通过说明部分定义的）。文档可以进一步被处理，处理的结果可以加入到当前的页面。DOM是一种基于树的API文档，它要求在处理过程中整个文档都表示在存储器中。另外一种简单的API是基于时间的SAX，它是用于处理很大的XML文档，由于大，所以不合适全部放在存储其中处理。
### DOM树
1. DOM树是一种结构，树是有DOM元素和属性节点组成的，DOM的本质是把Hhtml结构化成js可识别的树模型，有了树模型，就有了层级结构。层级结构值的是元素和元素之间的关系父子、兄弟。
  总结：
 ```html
<html>
	<head>
		<meta charset = 'utf-8'>
		<title>标题</title>
	</head>
	<body>
		<a href = '#'>我的连接</a>
		<h1>我的链接</h1>
	</body>
</html>
  ```
[图片】https://blog.csdn.net/Wanan_J/article/details/128736903?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522170470195616800226553094%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=170470195616800226553094&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-2-128736903-null-null.142^v99^control&utm_term=DOM&spm=1018.2226.3001.4187

2. DOM节点

   ① 文档节点：Docunent整个文档
   ② 元素节点：Element html元素
   ③ 文本节点：Text文本
   ④ 注释节点：Comment注释
   ⑥ 属性节点：Sttr属性
   节点对象属性：
   标记、标记属性、标记内子标记对象或文本子对象等DOM节点对象都具有nodeTypr节点类型、nodeName节点名称和nodeValue节点值三个通用属性。
注意：
① 文本区域标记texttaree 的文本节点应使用vvalue属性，若用nodeValue属性很容易出错。
② 可以通过直接赋值为任意节点对象添加任意类型的属性。

| 节点类型                      | nodevalue | nodeType | nodeName   |
| ----------------------------- | --------- | -------- | ---------- |
| 稳点根节点：Document 整个文档 | null      | 9        | #document  |
| 元素节点：Element html元素    | null      | 1        | 大写标签名 |
| 文本节点：Text                | 文本内容  | 3        | #text      |
| 注释节点：Comment 注释        |           | 8        |            |
| 属性节点：Attr属性            | 属性值    | 2        | 属性名     |

3. 获取元素节点：

   i. 根据id获取
  语法规范: document.getElementById(id名);   //返回的是一个节点对象   注意:获取指定的id，获取的元素是唯一的
代码示例：
   ```html
   <body>
   	<botton id ='btn'>按钮</boy=tton>
   	<script>
          bet btn = document.getElementById('bit');
   	  console.log(btn)
   	</script>
   </body>   
   ```
    ii. 根据name获取        语法规范:document.getElementByName(name名称)	//返回的是一个数组
注意：
  (1)这个方法不论获取几个元素都是为数组的形式
  (2)如果页面没有这个元素，则返回的是空的伪数组
```html
<body>
    <botton name = 'btn'>按钮</botton>
    <scrip>
        let btn = document.getElementByName('btn')
        console.log(btn)
    </scrip>
</body>
```
   iii. 根据className获取
语法规范：document.getElementByClassName（class名称）   返回的是一个数组
代码示例：
```html
<body>
    <botton name = 'btn'>按钮</botton>
    <scrip>
        let btn = document.getElementsByClassName('btn')
        console.log(btn)
    </scrip>
</body>
```
   iiii. 根据tagName获取	语法规范：document.getElementsByTagName(标签名称)//返回的是一个数组
代码示例：
```html
<body>
    <botton name = 'btn'>按钮</botton>
    <scrip>
        let btn = document.getElementsTagName(button)
        console.log(btn)
    </scrip>
</body>
```
   iiiii. 根据选择器获取
	语法规范：document.querySelector()   返回一个dom节点对象，没有返回Nulldocument.querySelectorALL()  //返回的是一个数组，没有返回空数组 
代码示例：
```html
<body>
    <ul>
    	<li>1</li>
    	<li>2</li>
    	<li>3</li>
    </ul>
    <scrip>
        let li= document.querySelectorALL('ul li')
        console.log(li)
    </scrip>
</body>
```
4. 获取元素节点相关的其他节点
   1. 获取上一个节点
   语法格式：
	previousSibling:返回档期那节点的上一个节点
	previousElementSibling:返回当前节点的上一个元素节点
   ```html
   <body>
    <ul class ='list'>
    	<li>1</li>
    	<li>2</li>
    	<li>3</li>
    </ul>
    <scrip>
        // js获取元素
	let list = document.querySelector('.list');
	//返回当前节点的上一个节点
	console.log(list.previoussibling);
	返回当前节点的上一个元素节点
	console.log(list.children[1].previousElementSibling);
    </scrip>
</body>
   ```
   2. 获取下一个节点
     语法格式：
     nextSibling:返回当前的节点下一个节点
     nextElementSibling:返回当煎节点的下一个元素节点
```html
<body>
    <ul class ='list'>
    	<li>1</li>
    	<li>2</li>
    	<li>3</li>
    </ul>
    <scrip>
        // js获取元素
	let list = document.querySelector('.list');
	//返回当前节点的下一个节点
	console.log(list.nextsibling);
	//返回当前节点的下一个元素节点
	console.log(list.children 1].nextElementsibling);
    </scrip>
</body>
```
   3. 获取子节点的方法
      语法格式：
        childNodes:返回当前节点的所有子节点
	children:返回当前节点的所有元素子节点
	firstChild:返回当前节点的第一个子节点
	lastChild:返回当前节点的最后一个子节点
	firstElementChild:返回当前节点的第一个元素子节点
	lastElementChild:返回当前节点的最后一个元素子节点
 ```html
 <body>
    <ul class ='list'>
    	<li>1</li>
    	<li>2</li>
    	<li>3</li>
    </ul>
    <scrip>
        // js获取元素
	let list = document.querySelector('.list');
	//返回当前节点的所有子节点
	console.log(list.childNodes);
	//返回当前节点的所有元素子节点
	console.log(list.children);
	//返回当前节点的第一个子节点
	console.log(list.firstChild);
	//返回当前节点的最后一个子节点
	console.log(list.lastChild);
	//返回当前节点的第一个元素子节点
	console.log(list.firstElementChild);
	//返回当前节点的最后一个元素子节点
	console.log(list.lastElementChild);
    </scrip>
</body>
 ```
   4. 获取父节点方法
   语法格式： parentNode:返回当前节点的父节点；
```html
 <body>
    <ul class ='list'>
    	<li>1</li>
    	<li>2</li>
    	<li>3</li>
    </ul>
    <scrip>
        // js获取元素
	let list = document.querySelector('.list');
	//返回当前节点的父节点
	console.log(list.children[1].parentNode);
    </scrip>
</body>
```
5. 创建节点
语法格式:
  1，生成节点的方法:
	document.createElement ("div");
  2，插入节点：
	父元素.appendChild(新节点)； //在父元素的子节点后面插入新节点
  3，在指定位置插入新的节点
	父元素.inSertBefore(新节点；谁的前面） //将新节点插入指定元素前面
  4，删除元素节点:
	父元素.removerChild();

6. 设置/修改DOM元素内容
   1. document.write()方法
      注意：
	只能将文本内容追加到</body>前面的位置；
	文本中包含的标签会被解析。
代码示例：
 ```javascript
	//永远都只是追加操作，而且只能在位置<body>前
	<script>
	document.write('hello world');
	document.write('<h3>你好，世界！<h3>');
	<script>
  ```
   3. 元素.
8. 
6. 
