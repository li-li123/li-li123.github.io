
## selenium的基础操作
### 1. 打开浏览器，访问谷歌首页
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
    def WebDriverChrom(self, chrom_path, web_path):
    '''
        :param chrom_path: chrome浏览器路径
        :param web_path: 访问网站地址
        :return: None
        '''
        self.option = Options()
        self.option.binary_location = chrom_path
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.maximize_window()
        self.driver.get(web_path)
```
### 2. 控制浏览器窗口大小
```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
time.sleep(60.0)
driver.set_window_size(480,800)
time.sleep(20.0)
driver.quit()
```
### 3. 定位文本框，处理文本框
1. 输入文本：
send_keys()
```python
time.sleep(5.0)
self.find_text = self.driver.find_element('name', 'wd')
time.sleep(5.0)
self.find_text.send_keys('百度')
time.sleep(1.0)
```
2. 清空文本

```python
self.find_text.clear()
```
### 4. 模拟键盘的操作
1. 导入keys的Keys方法：
```python
from selenium.webdriver.common.keys import Keys
```
2. 键入空格
```python
self.find_text.send_keys(Keys.SPACE*5)
```
### 5. 模拟鼠标的操作
1. 点击左键、右键
· 左键
```python
find_submit = self.driver.find_element('id','su')
find_submit.click()
self.driver.save_screenshot('result1.png')
```
2. 右键
```python

```
3. 
### 5. 截屏
1. 截取固定元素
```python
from selenium import webdriver
self.find_text.screenshot('err.png')
```
2. 全屏截图
```python
self.driver.save_screenshot('result.png')
```
3. 截取指定位置的图片
- 首先浏览器全屏情况下进行全屏截图pic1
- 然后找到元素通过使用`location`确定元素上、下、左、右的位置
- 最后在pic1的基础上结合元素上、下、左、右的位置，截取出相应的元素
```python
from PIL import Image
# 全屏截图
self.driver.save_screenshot('result.png')
 self.find_text.send_keys('ba第几哦')
        print('获取元素的坐标')
        # 计算元素上下左右的位置
        top = self.find_text.location['y']
        print(top)
        bottom =self.find_text.location['y']+self.find_text.size['height']
        print(bottom)
        left = self.find_text.location['x']
        right = left+self.find_text.size['width']
        print(top,bottom,left,right)
        pic_im= Image.open('result.png')
        pic_im = pic_im.crop((left, top, right, bottom))
        pic_im.show()
        pic_im.save('result1.png')
```
4. 图片拼接
```python
    def join_png(self,png1,png2,size=0,output = 'result.png'):
        '''
        :param png1:图片1
        :param png2: 图片2
        :param size: 两个图片重叠的距离
        :param output: 输出的图片文件
        :return:
        '''
        img1,img2 = Image.open(png1),Image.open(png2)
        size1,size2 = img1.size,img2.size # 获取两张图片的大小
        print(size1,size2)
        joint = Image.new('RGB', (size1[0],size1[1]+size2[1]-size)) #创建一个空白图片
        # 设置两张图片要放置的初始位置
        loc1, loc2=(0,0),(0,size1[1]-size)
        joint.paste(img1,loc1)
        joint.paste(img2,loc2)
        joint.save(output)
```
5. 滚动截图
```python
from selenium import webdriver
from PIL import Image

from selenium.webdriver.chrome.options import Options

option = Options()
option.binary_location =  r'D:\zml\chrome-win64\chrome.exe'
driver = webdriver.Chrome(options=option)
driver.maximize_window()
driver.get('https://www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%E7%83%AD%E6%90%9C&sa=ire_dl_gh_logo_texing&rsv_dl=igh_logo_pcs')
driver.save_screenshot('result.png')

def join_images(png1, png2, size=0, output='result.png'):
    """
    图片拼接
    :param png1: 图片1
    :param png2: 图片2
    :param size: 两个图片重叠的距离
    :param output: 输出的图片文件
    :return:
    """
    # 图片拼接
    img1, img2 = Image.open(png1), Image.open(png2)
    size1, size2 = img1.size, img2.size  # 获取两张图片的大小
    joint = Image.new('RGB', (size1[0], size1[1]+size2[1]-size))    # 创建一个空白图片
    # 设置两张图片要放置的初始位置
    loc1, loc2 = (0, 0), (0, size1[1] - size)
    # 分别放置图片
    joint.paste(img1, loc1)
    joint.paste(img2, loc2)
    # 保存结果
    joint.save(output)


JS = {
    '滚动到页尾': "window.scroll({top:document.body.clientHeight,left:0,behavior:'auto'});",
    '滚动到': "window.scroll({top:%d,left:0,behavior:'auto'});",
}
# 获取body大小
body_h = int(driver.find_element('xpath', '//body').size.get('height'))
# 计算当前页面截图的高度
# （使用driver.get_window_size()也可以获取高度，但有误差，推荐使用图片高度计算）
current_h = Image.open('result.png').size[1]
image_list = ['result.png']  # 储存截取到的图片路径

for i in range(1, int(body_h/current_h)):
    # 1. 滚动到指定锚点
    driver.execute_script(JS['滚动到'] % (current_h * i))
    # 2. 截图
    driver.save_screenshot(f'test_{i}.png')
    join_images('result.png', f'test_{i}.png')
# 处理最后一张图
driver.execute_script(JS['滚动到页尾'])
driver.save_screenshot('test_end.png')
# 拼接图片
join_images('result.png', 'test_end.png', size=current_h-int(body_h % current_h))

```
### 3. 控制浏览器后退、前进
```python
import time
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
time.sleep(60.0)

#访问百度首页
first_url = 'https://www.baidu.com'
print('now access  %s',first_url)
driver.get(first_url)

#访问问问也
second_utl = "https://wenku.baidu.com/?fr=bdpcindex&_wkts_=1705321401173"
print("now access %s",second_utl)
#返回到百度首页
print("back to %s",first_url)
driver.back()

#前进到新闻页
driver.forward()

driver.quit()


```
