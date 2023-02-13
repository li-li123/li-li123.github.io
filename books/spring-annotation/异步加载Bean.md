### 优化启动时间的思路

当 `Spring` 系统系统足够庞大时, 系统启动时耗时会明显增加, 为了优化启动时间,一般有以下的思路

1.  能够异步初始化的组件,  尽量异步
2. 排除的无关的依赖和垃圾代码
3. 优化业务代码的执行逻辑



### 异步初始化 Bean

Spring 的 生命周期 如下

![](https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-images13150128-bb5c9389cd0acc6c.webp)

这里面最最耗时的就是 `Bean` 的 `init-method` , 例如数据池的链接初始化, 配置文件的拉取与同步

为了优化这一启动时间,  可以采取异步初始化Bean的方式来优化这一逻辑, 具体实现思路如下

1. 自定义 `ApplicationContext` 和 `BeanFactory` 
2. 在 `BeanFacotry` 初始化 `bean` 时, 采用异步执行初始化

-----

自定义 `ApplicationContext`

```java
import org.springframework.boot.context.embedded.AnnotationConfigEmbeddedWebApplicationContext;
import org.springframework.context.support.GenericApplicationContext;
import org.springframework.stereotype.Component;

import java.lang.reflect.Field;

@Component
public class AsyncContext extends AnnotationConfigEmbeddedWebApplicationContext {

    public AsyncContext() throws Exception {
        Field beanFactory = GenericApplicationContext.class.getDeclaredField("beanFactory");
        beanFactory.setAccessible(true);
        // 关键点 替换为自定义的BeanFactory
        beanFactory.set(this, new AsyncInitBeanFactory(this.getBeanFactory()));
    }
}
```

Hack 初始化逻辑, 并异步初始化

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.BeanFactory;
import org.springframework.beans.factory.support.DefaultListableBeanFactory;
import org.springframework.beans.factory.support.RootBeanDefinition;

import javax.validation.constraints.NotNull;
import java.util.Queue;
import java.util.concurrent.Future;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;


@Slf4j
public class AsyncInitBeanFactory extends DefaultListableBeanFactory {

    /**
     * Constructor AsyncInitBeanFactory creates a new AsyncInitBeanFactory instance.
     *
     * @param parentBeanFactory of type BeanFactory
     */
    public AsyncInitBeanFactory(BeanFactory parentBeanFactory) {
        super(parentBeanFactory);
    }

    public final static Queue<Future> futurelist = new LinkedBlockingQueue<>();
    private static final ThreadPoolExecutor exec;

    static {
        int tc = Runtime.getRuntime().availableProcessors() * 4;
        exec = new ThreadPoolExecutor(tc, tc, 1, TimeUnit.MINUTES, new LinkedBlockingQueue<>(300),
                r -> new Thread(r, "async-initor"), new ThreadPoolExecutor.CallerRunsPolicy());
        exec.allowCoreThreadTimeOut(true);
    }


    @Override
    protected void invokeInitMethods(@NotNull final String beanName, final Object bean, final RootBeanDefinition mbd) throws Throwable {
        Runnable init = () -> {
            try {
                super.invokeInitMethods(beanName, bean, mbd);
            } catch (Throwable t) {
                log.error("invokeInitMethods-exp", t);
                throw new RuntimeException(t);
            }
        };
        if (needAsync(beanName, bean, mbd)) {
            futurelist.add(exec.submit(init));
        } else {
            init.run();
        }
    }

    private boolean needAsync(@NotNull final String beanName, final Object bean, 
                              final RootBeanDefinition mbd) {
        // 判断是否需要异步加载
        if (bean instanceof HSFSpringConsumerBean) {
            return true;
        }
        return false;
    }
}
```

### 局限

1. 异步初始化的 `Bean`, 不应当被其他 `Bean` 立刻使用, 否则会出现未知的 Bug

### 扩展阅读

1. [SpringBoot 的 MyBatis 多数据源配置](https://www.cnblogs.com/niumoo/p/14209663.html)

