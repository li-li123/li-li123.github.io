# Xpath基本语法和CSS选择器语法
 ##  Xpatch基本语法

 ###  一、常用的路径表达式：

| 表达式   | 描述                             | 实例     |
| -------- | -------------------------------- | -------- |
| nodename | nodename节点的所有子节点         | //div    |
| /        | 从节点选取                       | /div     |
| //       | 选取所有的节点，不考虑他们的位置 | //div    |
| .        | 选取当前节点                     |          |
| ..       | 选取当前节点的父节点             | //@class |
| @        | 选取属性                         |          |

###  举例元素标签为artical标签

| 语法         | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| artical      | 选取所有的artical元素的子节点                                |
| /artical     | 选取根元素artical                                            |
| ./artical    | 选取当前元素下的artical                                      |
| ../artical   | 选取父元素下的artical                                        |
| artical/a    | 选取所有属于artical的子元素a元素                             |
| //div        | 选取所有div子元素，无论div在任何地方                         |
| artical//div | 选取所有属于artical的div元素，无论div元素在artical的任何位置 |
| //@class     | 选取所有名为class的属性的                                    |
| a/@href      | 选取a标签的href属性                                          |
| a/text()     | 选取a标签下的文本                                            |
| string(.)    | 解析出当前节点下所有文字                                     |
| string(..)   | 解析出父节点下所有文字                                       |

###  二.、谓语

谓语被嵌入在括号内，用于查找某个特定的节点活包含某个制定的值的节点

| 语法                        | 说明                                        |      |
| --------------------------- | ------------------------------------------- | ---- |
| /artical/div[1]             | 选取所有属于artical子元素的第一个div元素    |      |
| /artical/div[last()]        | 选取所有属于artical子元素的最后一个div元素  |      |
| /artical/div[last()-1]      | 选取所有属于artical子元素的倒数第2个div元素 |      |
| /artical/div[poosition()<3] | 选取所有属于artical子元素 的钱2个div元素    |      |
| //div[@class]               | 选取所有拥有属性为class的div节点            |      |
| //div[@class = 'main']      | 选取所有div下class属性为main的div节点       |      |
| //div[price>3.5]            | 选取所有div下元素值price大于3.5的节点       |      |

###  三、通配符

Xpath通过通配符来选取位置的XML元素

| 表达式    | 结果                            |
| --------- | ------------------------------- |
| //*       | 选取所有元素                    |
| //div/*   | 选取所有属于div元素的所有子节点 |
| //div[@*] | 选取所欲呆属性的元素            |

四、曲多个路径

使用”|“运算符可以选取多个路径

| 表达式                   | 结果                               |
| ------------------------ | ---------------------------------- |
| //div \| //table         | 选取文档中所有的div和tablel节点    |
| //div \| //div/p         | 选取所有div元素的a和p元素          |
| artical/div/pl \| //span | 选取所有diiv下的pl和文档中所有span |

#### 五、Xpath轴

轴可以定义相对于当前节点的节点集

| 轴名称            | 表达式                 | 描述                                        |
| ----------------- | ---------------------- | ------------------------------------------- |
| ancestor          | ./ancestor::*          | 选取当前节点的所有鲜卑节点（父、祖）        |
| ancestor-or-self  | ./ancestor-or-self::*  | 选取当前节点的所有西安备节点以及节点本身    |
| descendant        | ./descendant""*        | 返回当前节点的所有后代节点（子节点、孙节点) |
| child             | /child::*              | 返回当前接待你的所有子节点                  |
| parent            | ./parent               | 返回当前节点的所有子节点                    |
| following         | ./following::*         | 选取文档中当前节点结束标签后的所有节点      |
| following-sibling | ./following-sibling::* | 选取当前节点之后的兄弟节点                  |
| preceding         | /preceding::*          | 选取文档中当前节点开始标签钱的所有节点      |
| preceding         | /preceding-sibling::*  | 选取当前节点之前的兄弟节点                  |
| self              | ./self::*              | 选取当前节点                                |
| attribute         | ./attribute::*         | 选取当前节点的所有属性                      |

#### 六、功能函数

使用功能函数能够更好的进行模糊搜索


| 函数 | 用法 | 解释 |
| ---- | ---- | ---- |
|starts-with|//div[starts-with(@id," ma”)]|选取id值以ma开头的div节点|
|contains|//div[contains(@id," ma” )]|选取所有id值包含ma的div节点|
|	and|//div[contains(@id," ma” ) and contains(@id," in”)]|选取id值包含ma和in的div节点 |
|text()|//div[contains(text(),” ma”)]|选取节点文本包含ma的div节点 |
注意事项：
1)按照审查元素的写法不一定正确，要按照网页源码的才行
2)浏览器有自带的复制xpath功能，firefox下载firebug插件
3)xpath有c的速度，所以按照[@class=""]准确性较高


### CCS选择器语法
|语法|说明|
|----|----|
|*|选择所有节点|
|#container|选择id为container|
|.container|选择所有class包含container的节点|
|div,p|选择所有div元素和所有p元素|
|li a|选取所有li下所有a节点|
|ul+p|选取ul后面的第一个ul子元素|
|div#container>ul|选取id为container的div的第一个ul子元素|
|ul~p|选取与ul相邻的所有p元素|
|a[title]|选取所有属性有title属性的a元素|
|a[href=”http://baidu.com“]|选取所有herf属性为http://baidu.com的a元素|
|a[href*=”baidu”]|选取所有href属性值中包含baidu的a元素|
|a[href^=”http”]|选取所有href属性值中以http开头的a元素|
|a[href$=”.jpg”]|选取所有href属性值中以.jpg结尾的a元素|
|input[type=radio]:checked|选择选中的radio的元素|
|div:not(#container)|选取所有id为非container 的div属性|
|li:nth-child(3)|选取第三个li元素|
|li:nth-child(2n)|选取第偶数个li元素|
|a::attr(href)|选取a标签的href属性|
|a::text|选取a标签下的文本|

关于更多CSS语法，可以查看
