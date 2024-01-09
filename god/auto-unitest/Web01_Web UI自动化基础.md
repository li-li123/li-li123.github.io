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
#### 1. DOM树是一种结构，树是有DOM元素和属性节点组成的，DOM的本质是把Hhtml结构化成js可识别的树模型，有了树模型，就有了层级结构。层级结构值的是元素和元素之间的关系父子、兄弟。
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

#### 2. DOM节点

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

#### 3. 获取元素节点：

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
2. 根据name获取
语法规范:document.getElementByName(name名称)	//返回的是一个数组
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
3. 根据className获取
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
4. 根据tagName获取
语法规范：document.getElementsByTagName(标签名称)//返回的是一个数组
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
5. 根据选择器获取
语法规范：document.querySelector()
返回一个dom节点对象，没有返回Nulldocument.querySelectorALL()  //返回的是一个数组，没有返回空数组 
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
#### 4. 获取元素节点相关的其他节点
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

#### 5. 创建节点
   语法格式:
1，生成节点的方法:
	document.createElement ("div");
2，插入节点：
	父元素.appendChild(新节点)； //在父元素的子节点后面插入新节点
3，在指定位置插入新的节点
	父元素.inSertBefore(新节点；谁的前面） //将新节点插入指定元素前面
4，删除元素节点:
	父元素.removerChild();

#### 6. 设置/修改DOM元素内容
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
2. 元素.innerText属性
注意：将文本内同添加/更新到任意标签位置；
文本中包含的标签会被解析
代码示例：
```html
<div>
	粉红色的回忆
</div>
<script>
	//获取标签(元素
		let box = document.querySelector('div')
	//修改标签（元素)内容 box是对象 innerHTML是属性
	// 语法格式: 对象.属性 = 值
	box.innerHTML = '<strong>我很棒<strong>'
	II innerHTML可以识别标签
</script>
```
4. 综合案例

```javascript
代码示例：
<i㎎ src=″./image/1.jpg" alt="″>
	<script>
	// 获取图片元素
	let pic = document.querySelector('i㎎')
	// 修改元素属性src
	pic.src = './image/2.jpg'
	pic.title='我的最爱
</script>

```
/I 随机抽取的名字显示到指定的标签内部
抽中的选手是: <span>≮span>

```javascript
//随机抽取的名字显示到指定的标签内部
抽中的选手是:<span></span>
<script>
    /I 获取元素
    let box = document.querySelector('span')
    //得到随机数
    function getRandom(min, max){
    return Math.floor(Math.random() * (max ﹣ min ﹢ 1))﹢min
    }
    // 声明一个数组
    let arr = [´张云'，`黄总'，`卢布，，`马超’，`刘恩，，`冠宇’，´张飞´]
    //生成一个随机数作为数组的索引号
    let random = getRandom(Θ, arr.length - 1)
    // 写入标签内部
    box.innerHTML = arr[random]
    //删除已经点到名字的同学名字
    arr.splice(random, 1)
</script>

```

#### 7. 设置/修改DOM元素内容
1. 设置/修改元素常用属性
注意：
还可以通过js设置/修改标签元素属性，比如通过src更换图片
常见的属性比如：href、title、src等
语法格式：对象、属性 = 值
```javascript
    <i㎎ src=″∴/image/1.jpg″ alt=″″>
    <script>
    // 获取图片元素
    let pic = document.querySelector('i㎎')
    // 修改元素属性 src
    pic.src = './image/2.jpg'
    pic.title = ´我的最爱´
≮/script>
```
2. 设置/修改元素样式属性
注意：
还可以通过JS设置/修改标签元素的样式属性：
比如通过轮播图小圆点自动更换颜色样式：
点击按银可以滚动图片，这是移动的图片的位置1eft等。
① 通过style属性操作CSS
语法格式：对象.style.样式属性 = 值
```javascript
<div>≮/div>
<script>
    获取元素
    let box = document.querySelector('div')
    //改变背景颜色 样式 style
    box.style.backgroundcolor = 'hotpink'
    II 改变盒子宽度
    box.style.width = '2øøpx'
<script>

```
② 操作类名（className）操作CSS
语法格式: 对象.style.样式属性 = 值
注意:
修改样式通过style属性引出:
如果属性有﹣连接符，需要转换为小驼峰命名法；
赋值的时候，需要的时候不要忘记加SS单位。
代码实例：
```javascript
<head>
	<style>
		div {
		width: 1øpx;
		height: 10px;
		background-color: pink;
		}
		.active {
		width: 100px;
		height: 10øpx;
		back㎏round-color: skyblue;
		}
	</style>
	</head>
	
<body>
	<div></div>
	<script>
		let box = document.querySelector('div')
		box.className = 'active'
	</script>
</body>
```
③ 通过classList操作类控制CSS
语法：
追加一个类：元素.classList.add('类名'）
删除一个类:元素.classList.remove(´类名')
切换一个类:元素.classList.toggle('类名'）
注意：
为了解决className容易覆盖以前的类名，我们可以通过classList方式追加和删除类名。
代码示例：
```javascript
<html>
	<head><head>
	<body>
		<div>
		粉红色的回忆
		</div>
			<script>
				// 获取元素
				let box = document.querySelector('div')
				// add是个方法 添加 追加
				box.classList.add('active')
				// remove()移除 类
				box.classList.remove('one')
				// 切换类 有就删除 没有就添加
				box.classList.toggle('one')
			</script>
	</body>
</html>
```
#### 8. 设置/修改表单元素属性
语法格式:
获取: DOM对象.属性名
设置：DOM对象.属性名=新值
代码示例：
````javascript
<input type="text" value=“请输入你的密码:”>
<script>
    // 获取元素
    let input = document.querySelector('input')
    // 修改属性值
    input.value = ´小米手机´
    // 设置属性值
    input.type = 'password'
≮/script>
````
表单属性中添加就有效果，移除就没有效果，一律使用布尔值表示。
如果为true代表添加了该属性，如果是false代表移除了该属性。
比如: disabled, checked, selected。
代码示例：
````javascript
<body>
    <button disabled>确定</button>
    <input type=″text" value=”请输入文字: ">
    <input type="checkbox" class="agree">
    <script>
    // 获取元素
    let btn = document.querySelector('button')
    // 让按钮启用
    btn.disabled = false
    // 勾选复选框
    let checkbox = document.querySelector('.agree')
    checkbox.checked = true
    </script>
</body>
````

