## selenium的环境配置
### 安装第三方库selenium
1. 安装语法
```sh
$ pip install selenium
```
2. 验证是否安装成功
能够成功引用说明selenium安装成功
```python
from selenium import webdriver
from web_loggin.config import *
from selenium.webdriver.chrome.options import Options

def chromdrive(self):
    option = Options()
    option.binary_location = chrom_path
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    driver.get(web_path)
```
### 配置驱动，以Chrome浏览器为例
1. 下载`Chrome`驱动及其相应的Chrome浏览器：https://googlechromelabs.github.io/chrome-for-testing/
2. 将驱动器中文件移动到python路径下
3. 电脑中已经安装Chrome不想删除，且与驱动版本不匹配，在编写脚本时配置好与驱动相应的浏览器路径即可：
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def WebDriverChrom(self, chrom_path, web_path):
	self.option = Options()
    self.option.binary_location = chrom_path
    self.driver = webdriver.Chrome(options=self.option)
    self.driver.maximize_window()
    self.driver.get(web_path)
```

