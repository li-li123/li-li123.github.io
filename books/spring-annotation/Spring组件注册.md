# Spring组件注册

 给容器中注册组件可以通过以下几种方式

1. 包扫描+组件标注注解（`@Controller`/`@Service`/`@Repository`/`@Component`）[自己写的类]
2. `@Bean`[导入的第三方包里面的组件]
3. `@Import`[快速给容器中导入一个组件]
	*  `@Import`(要导入到容器中的组件)；容器中就会自动注册这个组件，id默认是全类名
	*  `ImportSelector`:返回需要导入的组件的全类名数组；
	*  `ImportBeanDefinitionRegistrar`:手动注册bean到容器中
4. 使用Spring提供的`FactoryBean`(工厂Bean);
	* 默认获取到的是工厂bean调用`getObject`创建的对象
	* 要获取工厂Bean本身，我们需要给id前面加一个`&colorFactoryBean`

组件注册高级用法

* 可以通过@Conditional控制组件注册 
* 可以通过@Scope控制Bean的生命周期
* 可以通过@Layz控制Bean进行懒加载(容器启动不创建对象,第一次使用(获取)Bean创建对象，并初始化)

## @ComponentScan 组件扫描

### 源代码

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
@Repeatable(ComponentScans.class)
public @interface ComponentScan {

    // 指定要扫描的包
    @AliasFor("basePackages")
    String[] value() default {};

    // 指定要扫描的包
    @AliasFor("value")
    String[] basePackages() default {};

    Class<?>[] basePackageClasses() default {};

    Class<? extends BeanNameGenerator> nameGenerator() default BeanNameGenerator.class;

    Class<? extends ScopeMetadataResolver> scopeResolver() default AnnotationScopeMetadataResolver.class;

    ScopedProxyMode scopedProxy() default ScopedProxyMode.DEFAULT;

    String resourcePattern() default ClassPathScanningCandidateComponentProvider.DEFAULT_RESOURCE_PATTERN;

    // 默认扫描规则，如果不关闭则会自动加载spring默认组件(@Controller/@Service/@Repository/@Component)
    boolean useDefaultFilters() default true;
    
	// 指定扫描的时候只需要包含哪些组件, 如果不关闭默认扫描规则，还会加载Spring默认组件(@Controller/@Service/@Repository/@Component)
    Filter[] includeFilters() default {};
    
    // 指定扫描的时候按照什么规则排除那些组件
    Filter[] excludeFilters() default {};

    boolean lazyInit() default false;

    @Retention(RetentionPolicy.RUNTIME)
    @Target({})
    @interface Filter {

        FilterType type() default FilterType.ANNOTATION;

        @AliasFor("classes")
        Class<?>[] value() default {};

        @AliasFor("value")
        Class<?>[] classes() default {};

        String[] pattern() default {};

    }

}

```

### 常用属性

#### value/basePackages

指定要扫描的包

#### useDefaultFilters

默认扫描规则，如果不关闭则会自动加载spring默认组件(@Controller/@Service/@Repository/@Component)

#### includeFilters

指定扫描的时候只需要包含哪些组件, 如果不关闭默认扫描规则，还会加载Spring默认组件(@Controller/@Service/@Repository/@Component)

#### excludeFilters

指定扫描的时候按照什么规则排除那些组件

#### @Filter 组件过滤器 

使用示例

```java
@ComponentScan(value="org.ning",includeFilters = { // 指定扫描的时候只需要包含哪些组件, 如果不关闭默认扫描规则，还会加载Spring默认组件
						@Filter(type=FilterType.ANNOTATION,classes={Controller.class}),
                		@ComponentScan.Filter(type=FilterType.CUSTOM, classes={MyTypeFilter.class})
                },useDefaultFilters = false)
@Configuration
class MainConfig{
    
}
```

Filter 类别

* FilterType.ANNOTATION：按照注解
* FilterType.ASSIGNABLE_TYPE：按照给定的类型；
* FilterType.ASPECTJ：使用ASPECTJ表达式
* FilterType.REGEX：使用正则指定
* FilterType.CUSTOM：使用自定义规则

自定义Filter

```java
import org.springframework.core.io.Resource;
import org.springframework.core.type.AnnotationMetadata;
import org.springframework.core.type.ClassMetadata;
import org.springframework.core.type.classreading.MetadataReader;
import org.springframework.core.type.classreading.MetadataReaderFactory;
import org.springframework.core.type.filter.TypeFilter;

import java.io.IOException;

public class MyTypeFilter implements TypeFilter {

    /**
     * metadataReader：读取到的当前正在扫描的类的信息
     * metadataReaderFactory:可以获取到其他任何类信息的
     */
    public boolean match(MetadataReader metadataReader, MetadataReaderFactory metadataReaderFactory) throws IOException {
        //获取当前类注解的信息
        AnnotationMetadata annotationMetadata = metadataReader.getAnnotationMetadata();
        //获取当前正在扫描的类的类信息
        ClassMetadata classMetadata = metadataReader.getClassMetadata();
        //获取当前类资源（类的路径）
        Resource resource = metadataReader.getResource();

        String classname = classMetadata.getClassName();

        System.out.println("--->"+classname);
        return !classname.toLowerCase().contains("test");

    }
}
```

## @ComponentScans

@ComponentScans可以包含多个扫描规则，代码示例如下

```java
@ComponentScans(
        value = {
                @ComponentScan(value="org.ning",includeFilters = {
/*						@Filter(type=FilterType.ANNOTATION,classes={Controller.class}),
						@Filter(type=FilterType.ASSIGNABLE_TYPE,classes={BookService.class}),*/
                        @ComponentScan.Filter(type=FilterType.CUSTOM,classes={MyTypeFilter.class})
                },useDefaultFilters = false),
            @ComponentScan(value="org.ning",includeFilters = {
						@Filter(type=FilterType.ANNOTATION,classes={Controller.class})
                },useDefaultFilters = false),
            
        }
)
```

## @Bean

可以通过Spring任意组件中使用@Bean注册组件

### 源代码

```java
@Target({ElementType.METHOD, ElementType.ANNOTATION_TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Bean {

    // 注册Bean的ID
	@AliasFor("name")
	String[] value() default {};

	// 注册Bean的ID
	@AliasFor("value")
	String[] name() default {};

	Autowire autowire() default Autowire.NO;

    // 初始化方法，不常用， 可以使用InitializingBean, DisposableBean接口控制Bean的生命周期，默认值是"" ，表示没有init方法被调用
	String initMethod() default "";

	//  销毁方法
	String destroyMethod() default AbstractBeanDefinition.INFER_METHOD;

}
```

### 使用示例

```java
@Configuration
public class MainConfig {

    // id默认为方法名,也可指定id
    @Bean("person")
    public Person person(){
        return new Person("李四", 18) ;
    }

}
```

## @Import

	@Import[快速给容器中导入一个组件
	
		1. @Import(要导入到容器中的组件)；容器中就会自动注册这个组件，id默认是全类名。**可以导入配置类，Spring会自动处理配置类中注册的组件。**
  		2. ImportSelector:返回需要导入的组件的全类名数组；
                		3. ImportBeanDefinitionRegistrar:手动注册bean到容器中

### 源代码

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Import {

	//可以导入 Configuration, ImportSelector, ImportBeanDefinitionRegistrar或常规组件类进口
	Class<?>[] value();

}
```

### ImportSelector

当一个类实现`ImportSelector`接口，并且通过Import导入。Spring 会提取`selectImports()`返回的全类名，并注册到spring 容器中

```java
import org.springframework.context.annotation.ImportSelector;
import org.springframework.core.type.AnnotationMetadata;

public class MyImportSelector implements ImportSelector {


    //返回值，就是到导入到容器中的组件全类名
    //AnnotationMetadata:当前标注@Import注解的类的所有注解信息
    public String[] selectImports(AnnotationMetadata importingClassMetadata) {


        return new String[]{"org.ning.bean.Blue"};
    }
}
```

### ImportBeanDefinitionRegistrar

当一个类实现`ImportBeanDefinitionRegistrar`接口，并且通过Import导入。Spring 会自动执行`registerBeanDefinitions()`方法，用户可以根据实际情况注册组件

```java
import org.ning.bean.RainBow;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.beans.factory.support.BeanDefinitionRegistry;
import org.springframework.beans.factory.support.RootBeanDefinition;
import org.springframework.context.annotation.ImportBeanDefinitionRegistrar;
import org.springframework.core.type.AnnotationMetadata;

public class MyImportBeanRegister implements ImportBeanDefinitionRegistrar {


    /**
     * AnnotationMetadata：当前类的注解信息
     * BeanDefinitionRegistry:BeanDefinition注册类；
     * 		把所有需要添加到容器中的bean；调用
     * 		BeanDefinitionRegistry.registerBeanDefinition手工注册进来
     */

    public void registerBeanDefinitions(AnnotationMetadata importingClassMetadata, BeanDefinitionRegistry registry) {
        boolean definition = registry.containsBeanDefinition("org.ning.bean.Blue");
        boolean definition2 = registry.containsBeanDefinition("org.ning.bean.Red");

        if(definition&&definition2){
            //指定Bean定义信息；（Bean的类型，Bean。。。）
            BeanDefinition definition1 = new RootBeanDefinition(RainBow.class);
            //注册一个Bean，指定bean名
            registry.registerBeanDefinition("org.ning.RainBow",definition1);
        }
    }
}
```

### 使用示例

```java
public class Color {

    private int i =0;

    public Color() {
    }

    public Color(int i) {
        this.i = i;
    }
}
```

```java
public class ImportBean {

    @Bean
    public HelloBean helloBean(){
        return new HelloBean();
    }

    public static class HelloBean{

    }

}
```

```java
public class MyImportSelector implements ImportSelector {


    //返回值，就是到导入到容器中的组件全类名
    //AnnotationMetadata:当前标注@Import注解的类的所有注解信息
    public String[] selectImports(AnnotationMetadata importingClassMetadata) {


        return new String[]{"org.ning.bean.Blue"};
    }
}
```

```java
public class MyImportBeanRegister implements ImportBeanDefinitionRegistrar {


    /**
     * AnnotationMetadata：当前类的注解信息
     * BeanDefinitionRegistry:BeanDefinition注册类；
     * 		把所有需要添加到容器中的bean；调用
     * 		BeanDefinitionRegistry.registerBeanDefinition手工注册进来
     */

    public void registerBeanDefinitions(AnnotationMetadata importingClassMetadata, BeanDefinitionRegistry registry) {
        boolean definition = registry.containsBeanDefinition("org.ning.bean.Blue");
        boolean definition2 = registry.containsBeanDefinition("org.ning.bean.Red");

        if(definition&&definition2){
            //指定Bean定义信息；（Bean的类型，Bean。。。）
            BeanDefinition definition1 = new RootBeanDefinition(RainBow.class);
            //注册一个Bean，指定bean名
            registry.registerBeanDefinition("org.ning.RainBow",definition1);
        }
    }
}
```

```java
@Configuration
@Import({Color.class, ImportBean.class,MyImportSelector.class, MyImportBeanRegister.class} )
public class MainConfig {

}
```

## FactoryBean<T> 自定义注册Bean

使用Spring提供的 FactoryBean（工厂)

1.  默认获取到的是工厂bean调用getObject创建的对象

 2. 要获取工厂Bean本身，我们需要给id前面加一个& （例如"&colorFactoryBean")Bean）

### 使用示例

```java
import org.springframework.beans.factory.FactoryBean;

public class ColorFactoryBean implements FactoryBean<Color> {

    //返回一个Color对象，这个对象会添加到容器中
    @Override
    public Color getObject() throws Exception {
        // TODO Auto-generated method stub
        System.out.println("ColorFactoryBean...getObject...");
        return new Color(10086);
    }

    @Override
    public Class<?> getObjectType() {
        return Color.class;
    }

    //是单例？
    //true：这个bean是单实例，在容器中保存一份
    //false：多实例，每次获取都会创建一个新的bean；
    @Override
    public boolean isSingleton() {
        // TODO Auto-generated method stub
        return false;
    }

}

```

```java
@Configuration
public class MainConfig {

    @Bean
    public ColorFactoryBean customColor(){
        return new ColorFactoryBean();
    }
}

```

### 测试程序

```java
@Test
public void testImport(){
    AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfig.class);
    Color color = (Color) applicationContext.getBean("customColor");
    // 获取BeanFactory本身对象
    ColorFactoryBean factoryBean = (ColorFactoryBean)applicationContext.getBean("&customColor");
}
```

##  高级特性

### @Conditional 条件加载

* 修饰类时,满足当前条件，这个类中配置的所有bean注册才能生效；
* 修饰Bean时,满足当前条件，这个bean注册才能生效；

#### 使用示例

```java
public class LinuxCondition implements Condition {

    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {

        //1、能获取到ioc使用的beanfactory
        ConfigurableListableBeanFactory beanFactory = context.getBeanFactory();
        //2、获取类加载器
        ClassLoader classLoader = context.getClassLoader();
        //3、获取当前环境信息
        Environment environment = context.getEnvironment();
        //4、获取到bean定义的注册类
        BeanDefinitionRegistry registry = context.getRegistry();

        String property = environment.getProperty("os.name");

        //可以判断容器中的bean注册情况，也可以给容器中注册bean
        boolean definition = registry.containsBeanDefinition("person");

        return !context.getEnvironment().getProperty("os.name").toLowerCase().contains("windows");
    }
}
```

```java
@Configuration
@Conditional(WindowsCondition.class)
public class MainConfig2 {

    @Bean("bill")
    @Conditional(WindowsCondition.class)
    public Person person01(){
        return new Person("Bill Gates", 62);
    }

    @Conditional(LinuxCondition.class)
    @Bean("linus")
    public Person person02(){
        return new Person("Linus", 48);
    }


}
```

### Scope 设置 Bean 作用域

默认是Bean单实例的
可选作用域    

* prototype：多实例的：ioc容器启动并不会去调用方法创建对象放在容器中。每次获取的时候才会调用方法创建对象；
* singleton：单实例的（默认值）：ioc容器启动会调用方法创建对象放到ioc容器中。以后每次获取就是直接从容器（map.get()）中拿，
* request：同一次请求创建一个实例
* session：同一个session创建一个实例

#### 使用示例

```java
@Configuration
public class MainConfig2 {

    @Scope("prototype")
    @Bean("person")
    public Person person(){
        return new Person("张三", 14);
    }

}
```

### **@Layz** 懒加载

用于控制单实例bean，单实例bean默认在容器启动的时候创建对象。当设置懒加载后，容器启动不创建对象。第一次使用(获取)Bean创建对象，同时完成初始化。

#### 使用示例

```java
@Configuration
public class MainConfig2 {

    @Scope("prototype")
    @Bean("person")
    @Lazy
    public Person person(){
        return new Person("张三", 14);
    }

}
```