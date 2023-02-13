## Spring Bean生命周期

bean的生命周期： bean创建---初始化----销毁的过程
容器管理bean的生命周期；
我们可以自定义初始化和销毁方法；容器在bean进行到当前生命周期的时候来调用我们自定义的初始化和销毁方法
构造（对象创建）
 - 单实例：在容器启动的时候创建对象
 - 多实例：在每次获取的时候创建对象

自定义方法

1. 指定初始化和销毁方法；
	* 通过@Bean指定init-method和destroy-method

2. 通过让Bean实现
   - InitializingBean（定义初始化逻辑），
   - DisposableBean（定义销毁逻辑）;

3. 可以使用JSR250；
   -  @PostConstruct：在bean创建完成并且属性赋值完成后(即自动注入等动作完成后)，来执行初始化方法
   -  @PreDestroy：在容器销毁bean之前通知我们进行清理工作
4. BeanPostProcessor【interface】：bean的后置处理器；在bean初始化前后进行一些处理工作
	- postProcessBeforeInitialization:在初始化之前工作
    - postProcessAfterInitialization:在初始化之后工作

Spring底层对 BeanPostProcessor 的使用；
bean赋值，注入其他组件，@Autowired，生命周期注解功能，@Async,xxx BeanPostProcessor



```java
@ComponentScan("org.ning.bean")
@Configuration
public class MainConfigOfLifeCycle {

    @Bean(initMethod = "init", destroyMethod = "destroy")
    public Car car(){
        return new Car();
    }

    @Bean
    public Cat cat(){
        return new Cat();
    }

    @Bean
    public Dog dog(){
        return new Dog();
    }
}
```



### @Bean 指定init-method和destroy-method

```java

@Configuration
public class MainConfigOfLifeCycle {

    @Bean(initMethod = "init", destroyMethod = "destroy")
    public Car car(){
        return new Car();
    }
}
```

### Bean实现 (InitializingBean|DisposableBean)

```java
public class Cat implements InitializingBean, DisposableBean {

    public Cat(){
        System.out.println("cat constroctor");
    }
	
    // 销毁
    @Override
    public void destroy() throws Exception {
        System.out.println("cat Destroy ");
    }

    // 初始化
    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("Cat init");
    }
}
```

### JSR250 控制

```java
@Component
public class Dog {


    public Dog(){
        System.out.println("dog constructor..");
    }
	
    // 初始化
    @PostConstruct
    public void init(){
        System.out.println("dog ... @PostConstruct");
    }

    // 销毁
    @PreDestroy
    public void destroy(){
        System.out.println("dog ...@PreDestroy");
    }
}
```

### BeanPostProcessor 进行生命周期控制

![](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images13150128-bb5c9389cd0acc6c.webp)


spring内部会遍历得到容器中所有的BeanPostProcessor；挨个执行beforeInitialization，一但返回null，跳出for循环，不会执行后面的BeanPostProcessor.postProcessorsBeforeInitialization

Spring底层对 BeanPostProcessor 的使用：
 - bean赋值，注入其他组件

 - @Autowired，生命周期注解功能

 - @Async

 - xxx BeanPostProcessor

 - 等

**BeanPostProcessor原理**

```java
// populateBean(beanName, mbd, instanceWrapper);给bean进行属性赋值
initializeBean{
	applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
	invokeInitMethods(beanName, wrappedBean, mbd);执行自定义初始化
 	applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
}
```
#### 使用BeanPostProcessor进行动态代理

动态代理类

```java
package org.ning.beanPostProcessor;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.util.Date;


public class LogHandler implements InvocationHandler {
    Object target;  // 被代理的对象，实际的方法执行者

    public LogHandler(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        before();
        Object result = method.invoke(target, args);  // 调用 target 的 method 方法
        after();
        return result;  // 返回方法的执行结果
    }
    // 调用invoke方法之前执行
    private void before() {
        System.out.println(String.format("log start time [%s] ", new Date()));
    }
    // 调用invoke方法之后执行
    private void after() {
        System.out.println(String.format("log end time [%s] ", new Date()));
    }

    static public  <T> T bind(Class<T> clazz, Object object){
        Class<?>[]  interfaces = object.getClass().getInterfaces();
        for(Class item:interfaces){
            if (clazz == item){
                ClassLoader classLoader = object.getClass().getClassLoader();
                InvocationHandler logHandler = new LogHandler(object);
                return (T) Proxy.newProxyInstance(classLoader, interfaces, logHandler);
            }
        }
        return null;
    }
}
```

要代理的接口

```java
package org.ning.beanPostProcessor;

public interface UserService {
     void select();
     void update();
}
```

接口实现类

```java
package org.ning.beanPostProcessor;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {

    public void select() {
        System.out.println("UserDao select selectById");
    }
    public void update() {
        System.out.println("UserDao update update");
    }
}
```

后置处理器

```java
package org.ning.beanPostProcessor;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.stereotype.Component;


 /**
 * 后置处理器：初始化前后进行处理工作 AOP原理就是注入BeanPostProcessor，来拦截方法，注入AOP
 * 将后置处理器加入到容器中
 * 2020-02-26 14:18
 */
@Component
public class MyBeanPostProcessor implements BeanPostProcessor {

    // bean初始化方法调用前被调用
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {

        System.out.println("postProcessBeforeInitialization..."+beanName);
        // 此时bean已经创建，但是没有完成初始化方法。(所有Autowired已经注入完成)
        if(beanName.equals("userServiceImpl")){
            ((UserService)bean).select();
        }
        return bean;
    }

    // bean初始化方法调用后被调用
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {

        System.out.println("postProcessAfterInitialization..."+beanName);
        if(bean instanceof UserService){
            // 完成动态代理
            bean = LogHandler.bind(UserService.class, bean);
        }
        return bean;
    }
}
```

主配置类

```java
@ComponentScan("org.ning.beanPostProcessor")
@Configuration
public class MainConfigOfBeanPostProcessor {

}
```

测试代码

```java
public class IOCTest_BeanPostProcesser {

    @Test
    public void test01(){
        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(MainConfigOfBeanPostProcessor.class);
        printBeans(context);
        UserService userService = context.getBean(UserService.class);
        userService.select();
        userService.update();
    }

    private void printBeans(ApplicationContext context){
        String[] definitionNames = context.getBeanDefinitionNames();
        for(String item:definitionNames){
            System.out.println(item);
        }
    }

}
```



## 属性赋值

### @Value 赋值

```java
@ToString
public class Person {

    //使用@Value赋值；
    //1、基本数值
    //2、可以写SpEL； #{}
    //3、可以写${}；取出配置文件【properties】中的值（在运行环境变量里面的值）

    @Value("张三")
    private String name;

    @Value("#{20-12}" )
    private Integer age;

    public Person(){

    }

    public Person(String name, Integer age){
        this.name = name;
        this.age = age;
    }

}
```

### @PropertySource 赋值

@PropertySource使用后,会在运行环境中注册一个键值对。

```java
@Configuration
@PropertySource(value={"classpath:/person.properties"})
public class MainConfigOfPropertyValues {

    @Bean
    public Person person(){
        return new Person();
    }

}
```

```java
package org.ning.bean;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.beans.factory.annotation.Value;

/**
 * @author NingWang
 * 2020-02-24 13:23
 */

@ToString
public class Person {

    //使用@Value赋值；
    //1、基本数值
    //2、可以写SpEL； #{}
    //3、可以写${}；取出配置文件【properties】中的值（在运行环境变量里面的值）
    @Value("张三")
    private String name;

    @Value("#{20-12}" )
    private Integer age;

    @Value("${person.nickName}")
    private String nicName;
    public Person(){

    }

    public Person(String name, Integer age){
        this.name = name;
        this.age = age;
    }



}
```
person.properties
```shell
person.nickName=\u5C0F\u674E\u56DB
```
测试类
```java
public class IOCTest_PropertyValue {


    @Test
    public void test01(){
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfigOfPropertyValues.class);

        System.out.println("容器创建完成");
        System.out.println(applicationContext.getEnvironment().getProperty("person.nickName"));
        printBeans(applicationContext);
        Person person = (Person)applicationContext.getBean("person");
        System.out.println(person);
    }

    private void printBeans(ApplicationContext context){
        String[] definitionNames = context.getBeanDefinitionNames();
        for(String item:definitionNames){
            System.out.println(item);
        }
    }
}
```

## 自动装配


Spring利用依赖注入（DI），完成对**IOC**容器中中各个组件的依赖关系赋值



### @Autowired 自动注入
自动注入规则

* 默认优先按照类型去容器中找对应的组件:applicationContext.getBean(BookDao.class)找到就赋值
* 如果找到多个相同类型的组件，再将属性的名称作为组件的id去容器中查找。例如
```java
	@Service
public class BookService {
	
	/*
	*如果BookDao存在多个Bean,就使用applicationContext.getBean("bookDao2")去查找
	*
	*/
    @Autowired
    private BookDao bookDao2;

    public void print(){
        System.out.println(bookDao);
    }
}
```
* @Qualifier("bookDao")：使用@Qualifier指定需要装配的组件的id，而不是使用属性名

  ```java
  @Service
  public class BookService {
  	
  	@Qualifier("bookDao")
  	@Autowired
  	private BookDao bookDao;
  	
  	public void print(){
  		System.out.println(bookDao);
  	}
  }
  
  ```

  

* 自动装配默认一定要将属性赋值好，没有就会报错，可以使用@Autowired(required=false)，避免注入错误

  ```java
  @Service
  public class BookService {
  	
  	@Autowired(required=false)
  	private BookDao bookDao;
  	
  	public void print(){
  		System.out.println(bookDao);
  	}
  }
  ```

  

* @Primary：让Spring进行自动装配的时候，默认使用首选的bean，也可以继续使用@Qualifier指定需要装配的bean的名字

   ```java
  @Configuration
  public class MainConfigOfAutowired {
  
      @Primary
      @Bean("bookDao2")
      public BookDao bookDao(){
          return new BookDao();
      }
  
  }
  
  ```

**Autowired**会自动注入容器中的**Bean**

```java
@Service
public class BookService {

    @Autowired
    private BookDao bookDao;

    
}
```

### @Resource 注入


可以和@Autowired一样实现自动装配功能；默认是按照组件名称进行装配的； 没有能支持@Primary功能没有支持@Autowired（reqiured=false）;

```java
@Service
public class BookService {
	
    
    @Resource 
    private BookDao bookDao2;

    public void print(){
        System.out.println(bookDao);
    }
}
```

### @Inject

需要导入javax.inject的包，和Autowired的功能一样。没有required=false的功能；
```java
@Service
public class BookService {
	
    @Inject 
    private BookDao bookDao2;

    public void print(){
        System.out.println(bookDao);
    }
}
```

### @Autowired 其他特性

@Autowired:构造器，参数，方法，属性；都是从容器中获取参数组件的值
* [标注在方法位置]：@Bean+方法参数；参数从容器中获取;默认不写@Autowired效果是一样的；都能自动装配

  ```java
  @Configuration
  @ComponentScan({"org.ning.dao","org.ning.service", "org.ning.bean", "org.ning.controller"})
  public class MainConfigOfAutowired {
  
      @Primary
      @Bean("bookDao2")
      public BookDao bookDao(){
          return new BookDao();
      }
  
      @Bean
      //@Autowired 可以省略
      public Color color(Car car){
          Color color = new Color();
          return color;
      }
  
  }
  ```

  

* [标在构造器上]：如果组件**只有一个有参构造器**，这个有参构造器的@Autowired可以**省略**，参数位置的组件还是可以自动从容器中获取

* [放在参数位置]


```java
//默认加在ioc容器中的组件，容器启动会调用无参构造器创建对象，再进行初始化赋值等操作
@Component
public class Boss {
	
	@Autowired 
	private Car car;
	
	//构造器要用的组件，都是从容器中获取
	public Boss(Car car){
		this.car = car;
		System.out.println("Boss...有参构造器");
	}

	public Car getCar() {
		return car;
	}

	//标注在方法，Spring容器创建当前对象，就会调用方法，完成赋值；
	//方法使用的参数，自定义类型的值从ioc容器中获取
	@Autowired 
	public void setCar(Car car) {
		this.car = car;
	}


}
```

### Spring注入底层的对象(XXXXAwre)
1. 自定义组件想要使用Spring容器底层的一些组件（ApplicationContext，BeanFactory，xxx), 自定义组件只需实现xxxAware；在创建对象的时候，会调用接口规定的方法注入相关组件；Aware，把Spring底层一些组件注入到自定义的Bean中
   	xxxAware：功能使用xxxProcessor
      		内部会自动注入 (ApplicationContextAware==》ApplicationContextAwareProcessor)
2. 也可直接使用**@Autowired** 

```java
public class Red implements ApplicationContextAware,BeanNameAware,EmbeddedValueResolverAware {
	
	private ApplicationContext applicationContext;

	@Override
	public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
		System.out.println("传入的ioc："+applicationContext);
		this.applicationContext = applicationContext;
	}

	@Override
	public void setBeanName(String name) {
		System.out.println("当前bean的名字："+name);
	}

	@Override
	public void setEmbeddedValueResolver(StringValueResolver resolver) {
        // 解析字符串的解析器
		String resolveStringValue = resolver.resolveStringValue("你好 ${os.name} 我是 #{20*18}");
		System.out.println("解析的字符串："+resolveStringValue);
	}

}
```

### Profile 注入

Profile：
	Spring为我们提供的可以根据当前环境，动态的激活和切换一系列组件的功能。
@Profile：指定组件在哪个环境的情况下才能被注册到容器中，不指定，任何环境下都能注册这个组件
* 加了环境标识的bean，只有这个环境被激活的时候才能注册到容器中。默认是default环境
* 写在配置类上，只有是指定的环境的时候，整个配置类里面的所有配置才能开始生效
* 没有标注环境标识的bean在，任何环境下都是加载的

```java
@PropertySource("classpath:/dbconfig.properties")
@Configuration
public class MainConfigOfProfile implements EmbeddedValueResolverAware{
	
	@Value("${db.user}")
	private String user;
	
	private StringValueResolver valueResolver;
	
	private String  driverClass;
	
	
	@Bean
	public Yellow yellow(){
		return new Yellow();
	}
	
	@Profile("test")
	@Bean("testDataSource")
	public DataSource dataSourceTest(@Value("${db.password}")String pwd) throws Exception{
		ComboPooledDataSource dataSource = new ComboPooledDataSource();
		dataSource.setUser(user);
		dataSource.setPassword(pwd);
		dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/test");
		dataSource.setDriverClass(driverClass);
		return dataSource;
	}
	
	
	@Profile("dev")
	@Bean("devDataSource")
	public DataSource dataSourceDev(@Value("${db.password}")String pwd) throws Exception{
		ComboPooledDataSource dataSource = new ComboPooledDataSource();
		dataSource.setUser(user);
		dataSource.setPassword(pwd);
		dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/ssm_crud");
		dataSource.setDriverClass(driverClass);
		return dataSource;
	}
	
	@Profile("prod")
	@Bean("prodDataSource")
	public DataSource dataSourceProd(@Value("${db.password}")String pwd) throws Exception{
		ComboPooledDataSource dataSource = new ComboPooledDataSource();
		dataSource.setUser(user);
		dataSource.setPassword(pwd);
		dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/scw_0515");
		
		dataSource.setDriverClass(driverClass);
		return dataSource;
	}

	@Override
	public void setEmbeddedValueResolver(StringValueResolver resolver) {
		// TODO Auto-generated method stub
		this.valueResolver = resolver;
		driverClass = valueResolver.resolveStringValue("${db.driverClass}");
	}

}
```


dbconfig.properties


```shell
db.user=root
db.password=123456
db.driverClass=com.mysql.jdbc.Driver
```

#### 激活方法

1. VM参数  -Dspring.profiles.active=test

2. 代码激活

   ```java
   AnnotationConfigApplicationContext applicationContext = 
   				new AnnotationConfigApplicationContext();
   //1、创建一个applicationContext
   //2、设置需要激活的环境
   applicationContext.getEnvironment().setActiveProfiles("dev");
   //3、注册主配置类
   applicationContext.register(MainConfigOfProfile.class);
   //4、启动刷新容器
   applicationContext.refresh();
   ```