# 元素定位大全
## 8中基本元素定位
1. ID定位
```python
driver.find_element_by_id("id属性值")
```
2. name定位
```python
driver.find_element_by_name("name属性值")
```
3. class_name定位
```python
driver.find_element_by_class_name("class属性值")
```
4. tag_name定位
```python
driver.find_element_by_tag_name("标签")
```
5. link_text定位

精准定位
```python
driver.find_element_by_link_text("文本内容")
```
6. partial_link_text定位

模糊定位
```python
driver.find_element_by_partial_link_text("d文本链接部分链接")
```
7. Xpath定位

- Xpath定位的两种方式：绝对路径定位(绝对路径跨度大，稳定性差)、相对路径定位
 - 相对路径定位属性定位语法://标签名[@属性名=属性值]
 ```python
driver.find_element_by_partial_by_xpath("路径")
```
