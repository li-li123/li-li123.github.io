Spring AOP
------

## 使用方法

AOP指在程序运行期间动态的将某段代码切入到指定方法指定位置进行运行的编程方式；
1. 导入aop模块；Spring AOP：(spring-aspects)
2. 定义一个业务逻辑类（MathCalculator), 在业务逻辑运行的时候将日志进行打印（方法之前、方法运行结束、方法出现异常，xxx）
3. 定义一个日志切面类（LogAspects）：切面类里面的方法需要动态感知MathCalculator.div运行到哪里然后执行；
    通知方法：
    - 前置通知(@Before)：logStart：在目标方法(div)运行之前运行
    - 后置通知(@After)：logEnd：在目标方法(div)运行结束之后运行（无论方法正常结束还是异常结束）
    - 返回通知(@AfterReturning)：logReturn：在目标方法(div)正常返回之后运行
    - 异常通知(@AfterThrowing)：logException：在目标方法(div)出现异常以后运行
    - 环绕通知(@Around)：动态代理，手动推进目标方法运行（joinPoint.procced()）
4. 给切面类的目标方法标注何时何地运行（通知注解）；
5. 将切面类和业务逻辑类（目标方法所在类）都加入到容器中;
6. 必须告诉Spring哪个类是切面类(给切面类上加一个注解：@Aspect)
7. 给配置类中加 @EnableAspectJAutoProxy 【开启基于注解的aop模式】
	
	> 在Spring中很多的 @EnableXXX;
	

具体aop语言参考[aop官方文档](https://docs.spring.io/spring/docs/current/spring-framework-reference/core.html#aop-api)
共三步：

   1. 将业务逻辑组件和切面类都加入到容器中；告诉Spring哪个是切面类（@Aspect）

   2. 在切面类上的每一个通知方法上标注通知注解，告诉Spring何时何地运行（切入点表达式）

  	3. 开启基于注解的aop模式；@EnableAspectJAutoProxy


例：
```java
public class MathCalculator {
	
	public int div(int i,int j){
		System.out.println("MathCalculator...div...");
		return i/j;	
	}
}
```

```java
// @Aspect： 告诉Spring当前类是一个切面类
@Aspect
public class LogAspects {
    
//抽取公共的切入点表达式, 返回值名字类型都无所谓
//1、本类引用
//2、其他的切面引用
@Pointcut("execution(public int com.atguigu.aop.MathCalculator.*(..))")
public void pointCut(){};

//@Before在目标方法之前切入；切入点表达式（指定在哪个方法切入）
//@Before("execution(public int com.atguigu.aop.MathCalculator.*(..))")
@Before("pointCut()")
public void logStart(JoinPoint joinPoint){
	Object[] args = joinPoint.getArgs();
	System.out.println(""+joinPoint.getSignature().getName()+
                       "运行。。。@Before:参数列表是：{"+Arrays.asList(args)+"}");
}

@After("com.atguigu.aop.LogAspects.pointCut()")
public void logEnd(JoinPoint joinPoint){
	System.out.println(""+joinPoint.getSignature().getName()+
                       "结束。。。@After");
}

//JoinPoint一定要出现在参数表的第一位
@AfterReturning(value="pointCut()",returning="result")
public void logReturn(JoinPoint joinPoint,Object result){
	System.out.println(""+joinPoint.getSignature().getName()+
                       "正常返回。。。@AfterReturning:运行结果：{"+result+"}");
}

@AfterThrowing(value="pointCut()",throwing="exception")
public void logException(JoinPoint joinPoint,Exception exception){
	System.out.println(""+joinPoint.getSignature().getName()+
                       "异常。。。异常信息：{"+exception+"}");
}
}
```
```java
@EnableAspectJAutoProxy // 开启切面编程
@Configuration
public class MainConfigOfAOP {
	 
	//业务逻辑类加入容器中
	@Bean
	public MathCalculator calculator(){
		return new MathCalculator();
	}
    
	//切面类加入到容器中
	@Bean
	public LogAspects logAspects(){
		return new LogAspects();
	}
}
```

  ## 基于注解的 Spring AOP 日志 记录

日志注解，切面会对该注解标识的方法进行日志记录

```java
@Documented
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface LogOperation {

    /**
     * 操作名
     */
    String operationName() default "unknown";

    /**
     * 是否忽略结果
     */
    boolean ignoreOutput() default true;

    /**
     * 敏感参数
     * 日志会记录操作参数。 如果有敏感参数(例如密码等)，请忽略该参数
     */
    String[] sensitiveParams() default {};

    /**
     * 目标类型：CONTROLLER：controller日志, SERVICE：service日志, DAO：dao日志, METHOD：普通方法日志
     */
    OperationType operationType();

}
```

日志类别，用于日志分类

```java
@Documented
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface LogTag {
    String value() default "unknown";
}
```

AOP类

```java
@Slf4j
@Aspect
@Component
public class LogAspect {

    @Value("${syslog.select:false}")
    private boolean logSelect;

    @Autowired
    SysLogService sysLogService;
	
    // 生命切点
    @Pointcut("@annotation(com.bdilab.iot.annotation.LogOperation)")
    public void logPoint() {}

    @AfterReturning(value = "logPoint()", returning = "result")
    public void afterReturn(JoinPoint jp,  Object result) {
        if(needLog(jp)) {
            SysLog sysLog = buildLog(jp, result, null);
            sysLogService.saveLog(sysLog);
        }
    }

    @AfterThrowing(value = "logPoint()", throwing = "ex")
    public void afterReturn(JoinPoint jp,  Throwable ex) {
        if(needLog(jp)){
            SysLog sysLog = buildLog(jp, null, ex);
            sysLogService.saveLog(sysLog);
        }

    }

    private SysLog buildLog(JoinPoint joinPoint, Object result, Throwable ex){

        ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes(); // 获取当前请求中的Request
        assert attributes != null;
        HttpServletRequest request = attributes.getRequest();

        MethodSignature signature = (MethodSignature) joinPoint.getSignature(); // 获取当前执行方法的反射类

        LogOperation logOperation = signature.getMethod().getAnnotation(LogOperation.class);

        LogTag logTag = joinPoint.getTarget().getClass().getAnnotation(LogTag.class);

        String ip = IpUtils.getRemoteAddr(request);

        User user = (User) request.getAttribute(Constants.CURRENT_USER);

        if(user == null){
            user = new User();
            user.setId(-1L);
            user.setUsername("匿名用户");
        }

        String userAgent = request.getHeader("User-Agent");
        userAgent = StringUtils.isEmpty(userAgent)?"未知客户端":userAgent;

        String input = handleInput(joinPoint.getArgs(), Arrays.asList(logOperation.sensitiveParams()));

        String output = handleOutput(result, logOperation.ignoreOutput());

        String ex_msg = handleException(ex);

        String operationName = String.format("%s:%s", logTag == null?"unknown":logTag.value(), logOperation.operationName());

        return SysLog.builder().userId(user.getId())
                .username(user.getUsername())
                .ip(ip).userAgent(userAgent)
                .input(input).output(output)
                .exMsg(ex_msg).operationName(operationName)
                .operationType(logOperation.operationType())
                .build();
    }

    /**
     * 处理输入参数
     *
     * @param args 入参
     * @param sensitiveParams 敏感参数关键字
     * @return 特殊处理都的入参
     */
    private String handleInput(Object[] args, List<String> sensitiveParams)  {

        Map<String, Object> argMap = Maps.newTreeMap();

        ObjectMapper om = new ObjectMapper();
        if (!ObjectUtils.isEmpty(args)) {
            for (int i = 0; i < args.length; i++) {
                if(filterArgs(args[i]))
                    continue;
                if (args[i] != null && !ObjectUtils.isEmpty(sensitiveParams)) {
                    try {
                        JsonNode  root = om.readTree(om.writeValueAsString(args[i]));
                        handleSensitiveParams(root, sensitiveParams);
                        argMap.put("arg" + (i + 1), root);
                    } catch (IOException e) {
                        argMap.put("arg" + (i + 1), "[exception]");
                    }
                } else {
                    argMap.put("arg" + (i + 1), args[i]);
                }
            }
        }
        try{
            return om.writeValueAsString(argMap);
        }catch (JsonProcessingException e){
            return "{parse args exception}";
        }

    }

    /**
     * 处理敏感参数
     *
     * @param root jackson节点
     * @param params 敏感参数名列表
     */
    private void handleSensitiveParams(JsonNode  root, List<String> params) {


        if (root.isObject()) {

            Iterator<Map.Entry<String, JsonNode>> rootIt = root.fields();
            while (rootIt.hasNext()) {
                Map.Entry<String, JsonNode> node = rootIt.next();
                if (params.contains(node.getKey())) {
                    node.setValue(new TextNode("[hidden]"));
                } else {
                    JsonNode tmpNode = node.getValue();
                    if (tmpNode.isObject()) {
                        handleSensitiveParams(tmpNode, params);
                    } else if (tmpNode.isArray()) {
                        for (JsonNode jsonNode : tmpNode) {
                            handleSensitiveParams(jsonNode, params);
                        }
                    }
                }
            }
        } else if (root.isArray()) {

            for (JsonNode jsonNode : root) {
                handleSensitiveParams(jsonNode, params);
            }

        }
    }

    /**
     * 过滤常用的Controller输入参数
     * @param args
     * @return
     */
    private boolean filterArgs(Object args){
        if(args == null)
            return true;
        return args instanceof User || args instanceof MultipartFile || args instanceof HttpServletRequest ||
                args instanceof ServletResponse || args instanceof BindingResult;
    }

    /**
     * 处理异常信息
     *
     * @param ex 异常对象
     * @return 处理后的异常信息
     */
    private String handleException(Throwable ex) {
        return ex == null ? null : ex.toString();
    }

    /**
     * 处理输出结果
     *
     * @param result 源输出结果
     * @param ignore 是否忽略结果
     * @return 处理后的输出结果
     */
    private String handleOutput(Object result, boolean ignore) {

        return (ignore || result == null) ? null : JSON.toJSONString(result);
    }

    /**
     * 判断是否需要记录查询日志
     */
    private boolean needLog(JoinPoint joinPoint){
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        LogOperation logOperation = signature.getMethod().getAnnotation(LogOperation.class);
        if(logOperation == null)
            return false;
        if(logOperation.operationType() == OperationType.SELECT){
            return logSelect;
        }
        return true;
    }


}
```

主启动类

```java

@EnableAspectJAutoProxy // 开启基于ASPJ的AOP织入模式
public class IotApplication {

    public static void main(String[] args) {
        SpringApplication.run(IotApplication.class, args);

    }
}
```

使用示例

```java

@LogTag("用户管理")
@RequestMapping(value = Constants.BASE_API_PATH + "/user")
public class UserController {

	@PostMapping("")
    @LogOperation(operationName = "添加用户", sensitiveParams = {"password"},operationType = OperationType.INSERT)
    public ResponseEntity addUser(){
        return ResponseEntity.ok();
    }
            

}    
```



  