## selenium之鼠标键盘操作(ACtionChains)

ActionChains模拟鼠标操作的常用方法。使用click()方法可以进行鼠标的单击操作，但是鼠标操作还包括：双击、右击、悬停、鼠标拖动等功能，所以，ActionChains类提供了鼠标的常用方法：

### 1. 执行原理

调用ActionChains的方法时，不会立即执行，而是将所有的操作，按照顺序存放在一个队列中，调用perform()方法时，队列中的事件才会依次执行。

### 2. ActionChains基本用法

1. 链式写法

```python
ActionChains(driver).move_to_element(element).click(element).perform()
```

2. 分布写法

```python
actions = ActionChains(driver)
actions.mover_to_element(element)
actions.click(element)
actions.perform()
```

### 3. 基本用法

- 生成一个动作：action = ActionChains(driver)
- 动作添加method1 action.method1
- 动作添加method2 action.method2
- 调用perform()方法执行，(action.perform())

### 4. 常用方法介绍

- click(on_element=None)：单击鼠标左键
- click_and_hold(on_element=None)：点击鼠标左键不松开
- context_click(on_element=None)：点击鼠标右键
- double_click(on_element=None)：双击鼠标左键
- drag_and_drop(source, target)：拖拽某个元素到目标位置后松开
- drag_and_drop_by_offset(source, xoffset, yoffset)：推拽到某个坐标后松开
- key_down(value, element=None)：按下键盘上的某个键
- key_up(value, element=None)：松开键盘上的某个键
- move_by_offset(xoffset, yoffset)：鼠标从当前位置移动到某个坐标
- move_to_element(to_element)：鼠标移动到某个元素
- move_to_element_with_offset(to_element, xoffset, yoffset)：鼠标移动到距离某个元素（左上角坐标）多少距离的位置
- pause(seconds)：暂停
- perform()：执行链中的所有动作
- release(on_element=None)：在某个元素位置松开鼠标左键，如果传入参数，则移动到该元素后抬起鼠标，如果没有传入元素则执行鼠标抬起操作
- send_keys(*keys_to_send)：发送某个键到当前焦点的元素
- send_keys_to_element(element,*kets_to_send)：发送某个键到指定元素

### 5. 实操测试
```python
from selenium.webdriver import ActionChains
action = ActionChains(self.driver)
find_text = self.driver.find_element('id', user_login_id)
time.sleep(2.0)
find_pws = self.driver.find_element('id', pwd_login_id)
time.sleep(2.0)
fine_slide = self.driver.find_element('class name',slide_xpath)
find_submit = self.driver.find_element('xpath',submit_xpath)
action.click(find_text).send_keys(login_name).click(find_pws).send_keys(login_password).click(fine_slide).click_and_hold(fine_slide).move_by_offset(288,2).release().perform()
```
#### 1. 点击操作

#### 2. 鼠标移动操作

#### 3. 
