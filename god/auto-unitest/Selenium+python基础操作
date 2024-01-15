# Selenium3+python

## 基础操作
### 控制浏览器窗口大小
```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
time.sleep(60.0)

driver.set_window_size(480,800)
time.sleep(20.0)
driver.quit()
```
### 控制浏览器后退、前进
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
