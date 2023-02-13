## 快速开始

Maven 依赖

```xml
<!-- https://mvnrepository.com/artifact/org.apache.zookeeper/zookeeper -->
<dependency>
    <groupId>org.apache.zookeeper</groupId>
    <artifactId>zookeeper</artifactId>
    <version>3.6.3</version>
</dependency>

<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-log4j12</artifactId>
    <version>1.7.2</version>
</dependency>
```

日志配置(可选)

```properties
log4j.rootLogger=DEBUG,console

# 控制台(console)
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.Threshold=DEBUG
log4j.appender.console.ImmediateFlush=true
log4j.appender.console.Target=System.err
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=[%-5p] %d(%r) [%t] %l: %m %x %n
```

> log4j.properties

## 会话的连接与恢复

创建 ZK 连接所需类为 `org.apache.zookeeper.ZooKeeper`, 其中主构造函数如下

```java
    public ZooKeeper(
        String connectString, // 连接地址
        int sessionTimeout, // 会话过期时间
        Watcher watcher, // 连接成功后, 自动触发的 watcher
        long sessionId, // 断线恢复需要的 sessionID
        byte[] sessionPasswd, // 断线恢复需要的 sessionPassword
        boolean canBeReadOnly) throws IOException { // 以只读模式启动
        this(
            connectString,
            sessionTimeout,
            watcher,
            sessionId,
            sessionPasswd,
            canBeReadOnly,
            createDefaultHostProvider(connectString));
    }
```



创建连接

```java
public class ConnectZookeeper {
    
    private static final String zkServerPath = 
        "192.168.1.148:2181,192.168.1.148:2182,192.168.1.148:2183";
    public static final Integer timeOut = 5000; // 单位毫秒
    
    public static void main(String[] args) throws Exception {
        
        ZooKeeper zk = new ZooKeeper(zkServerPath, timeOut, new Watcher() {
            @Override
            public void process(WatchedEvent watchedEvent) {
                System.out.println("连接成功");
                System.out.println(watchedEvent);
            }
        });
        
        Thread.sleep(5000);
        System.out.println("连接状态: "+zk.getState());
    }

}
```



断线重连

```java
public class ConnectZookeeper {

    private static final String zkServerPath = 
        "192.168.1.148:2181,192.168.1.148:2182,192.168.1.148:2183";
    public static final Integer timeOut = 5000; // 单位毫秒
    
    public static void main(String[] args) throws Exception {
        ZooKeeper zk = new ZooKeeper(zkServerPath, timeOut, new Watcher() {
            @Override
            public void process(WatchedEvent watchedEvent) {
                System.out.println("连接成功");
                System.out.println(watchedEvent);
            }
        });
        Thread.sleep(10000);
        System.out.println("连接状态: "+zk.getState());
        long  sessionID = zk.getSessionId();
        byte[] sessionPassword = zk.getSessionPasswd();
        zk.close();

        System.out.println("开始会话重连");
        zk = new ZooKeeper(zkServerPath, timeOut, new Watcher() {
            @Override
            public void process(WatchedEvent event) {
                System.out.println("连接成功");
                System.out.println(event);
            }
        }, sessionID, sessionPassword);
        Thread.sleep(10000);
        System.out.println("连接状态: "+zk.getState());
        
    }

}
```



## 节点的增删改查

### 添加和删除

```java
public class ZKNodeOperator implements Watcher {

    private ZooKeeper zooKeeper = null;

    private static final String zkServerPath =
        "192.168.1.148:2181,192.168.1.148:2182,192.168.1.148:2183";
    public static final Integer timeOut = 5000; // 单位毫秒

    public ZKNodeOperator(){
        try {
            zooKeeper = new ZooKeeper(zkServerPath, timeOut, new Watcher() {
                @Override
                public void process(WatchedEvent event) {
                    System.out.println("连接成功");
                }
            });
        }catch (IOException e){
            e.printStackTrace();
            if(zooKeeper!=null){
                try {
                    zooKeeper.close();
                }catch (InterruptedException e1){
                    e1.printStackTrace();
                }
            }
        }
    }

    /**
     * 创建 zk节点
     * @param path 路径
     * @param data 数据
     * @param acls 权限
     */
    public void createZKNode(String path, byte[] data, List<ACL> acls){
          String res = "";

        try {
            /**
             * 同步或者异步创建节点，都不支持子节点的递归创建，异步有一个callback函数
             * 参数：
             * path：创建的路径
             * data：存储的数据的byte[]
             * acl：控制权限策略
             * 			Ids.OPEN_ACL_UNSAFE --> world:anyone:cdrwa
             * 			CREATOR_ALL_ACL --> auth:user:password:cdrwa
             * createMode：节点类型, 是一个枚举
             * 			PERSISTENT：持久节点
             * 			PERSISTENT_SEQUENTIAL：持久顺序节点
             * 			EPHEMERAL：临时节点
             * 			EPHEMERAL_SEQUENTIAL：临时顺序节点
             */
            res = zooKeeper.create(path, data, acls, CreateMode.PERSISTENT); // 同步方法
            
//           异步方法
//			String ctx = "{'create':'success'}";
//			zookeeper.create(path, data, acls, CreateMode.PERSISTENT, new CreateCallBack(), ctx); 
            System.out.println("创建节点：\t" + res + "\t成功...");

        } catch (Exception e) {
            e.printStackTrace();
        }

    }



    @Override
    public void process(WatchedEvent event) {

    }

    public static void main(String[] args) throws Exception{
        ZKNodeOperator zkServer = new ZKNodeOperator();

        while (zkServer.getZooKeeper().getState() == ZooKeeper.States.CONNECTING){
            Thread.sleep(1000);
        }


        // 创建节点
        zkServer.createZKNode("/testnode", "testnode".getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE);
        Thread.sleep(2000);

        /*
         * 参数：
         * path：节点路径
         * data：数据
         * version：数据状态
         */
        // 修改数据
		Stat status  = zkServer.getZooKeeper().setData("/testnode", "xyz".getBytes(), 2);
		System.out.println(status.getVersion());

        /*
         * 参数：
         * path：节点路径
         * version：数据状态
         */
        zkServer.createZKNode("/test-delete-node", "123".getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE);
        zkServer.getZooKeeper().delete("/test-delete-node", 2); // 同步删除
        
        String ctx = "{'delete':'success'}";
        zkServer.getZooKeeper().delete("/test-delete-node", 0, new AsyncCallback.VoidCallback() {
            @Override
            public void processResult(int rc, String path, Object ctx) {

            }
        }, ctx); // 异步删除
        
        Thread.sleep(2000);

    }

    public ZooKeeper getZooKeeper() {
        return zooKeeper;
    }
}
```

<hr></hr>

### 查询

1. 获取节点数据

```java

/**
 * 
 * @Description: zookeeper 获取节点数据的demo演示
 */
public class ZKGetNodeData implements Watcher {

	private ZooKeeper zookeeper = null;
	
	public static final String zkServerPath = "192.168.1.110:2181";
	public static final Integer timeout = 5000;
	private static Stat stat = new Stat();
	
	public ZKGetNodeData() {}
	
	public ZKGetNodeData(String connectString) {
		try {
			zookeeper = new ZooKeeper(connectString, timeout, new ZKGetNodeData());
		} catch (IOException e) {
			e.printStackTrace();
			if (zookeeper != null) {
				try {
					zookeeper.close();
				} catch (InterruptedException e1) {
					e1.printStackTrace();
				}
			}
		}
	}
	
	private static CountDownLatch countDown = new CountDownLatch(1);
	
	public static void main(String[] args) throws Exception {
	
		ZKGetNodeData zkServer = new ZKGetNodeData(zkServerPath);
		
		/**
		 * 参数：
		 * path：节点路径
		 * watch：true或者false，注册一个watch事件
		 * stat：状态
		 */
		byte[] resByte = zkServer.getZookeeper().getData("/imooc", true, stat);
		String result = new String(resByte);
		System.out.println("当前值:" + result);
		countDown.await();
	}
	
	@Override
	public void process(WatchedEvent event) {
		try {
			if(event.getType() == EventType.NodeDataChanged){
				ZKGetNodeData zkServer = new ZKGetNodeData(zkServerPath);
				byte[] resByte = zkServer.getZookeeper().getData("/imooc", false, stat);
				String result = new String(resByte);
				System.out.println("更改后的值:" + result);
				System.out.println("版本号变化dversion：" + stat.getVersion());
				countDown.countDown();
			} else if(event.getType() == EventType.NodeCreated) {
				
			} else if(event.getType() == EventType.NodeChildrenChanged) {
				
			} else if(event.getType() == EventType.NodeDeleted) {
				
			} 
		} catch (KeeperException e) { 
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	public ZooKeeper getZookeeper() {
		return zookeeper;
	}
	public void setZookeeper(ZooKeeper zookeeper) {
		this.zookeeper = zookeeper;
	}
}
```

-----

2. 获取子节点数据

```java

/**
 * @Description: zookeeper 获取子节点数据的demo演示
 */
public class ZKGetChildrenList implements Watcher {

	private ZooKeeper zookeeper = null;
	
	public static final String zkServerPath = "192.168.1.110:2181";
	public static final Integer timeout = 5000;
	
	public ZKGetChildrenList() {}
	
	public ZKGetChildrenList(String connectString) {
		try {
			zookeeper = new ZooKeeper(connectString, timeout, new ZKGetChildrenList());
		} catch (IOException e) {
			e.printStackTrace();
			if (zookeeper != null) {
				try {
					zookeeper.close();
				} catch (InterruptedException e1) {
					e1.printStackTrace();
				}
			}
		}
	}
	
	private static CountDownLatch countDown = new CountDownLatch(1);
	
	public static void main(String[] args) throws Exception {
	
		ZKGetChildrenList zkServer = new ZKGetChildrenList(zkServerPath);
		
		/**
		 * 参数：
		 * path：父节点路径
		 * watch：true或者false，注册一个watch事件
		 */
//		List<String> strChildList = zkServer.getZookeeper().getChildren("/imooc", true);
//		for (String s : strChildList) {
//			System.out.println(s);
//		}
		
		// 异步调用
		String ctx = "{'callback':'ChildrenCallback'}";
//		zkServer.getZookeeper().getChildren("/imooc", true, new ChildrenCallBack(), ctx);
		zkServer.getZookeeper().getChildren("/imooc", true, new Children2CallBack(), ctx);
		
		countDown.await();
	}
	
	@Override
	public void process(WatchedEvent event) {
		try {
			if(event.getType()==EventType.NodeChildrenChanged){
				System.out.println("NodeChildrenChanged");
				ZKGetChildrenList zkServer = new ZKGetChildrenList(zkServerPath);
				List<String> strChildList = zkServer.getZookeeper().getChildren(event.getPath(), false);
				for (String s : strChildList) {
					System.out.println(s);
				}
				countDown.countDown();
			} else if(event.getType() == EventType.NodeCreated) {
				System.out.println("NodeCreated");
			} else if(event.getType() == EventType.NodeDataChanged) {
				System.out.println("NodeDataChanged");
			} else if(event.getType() == EventType.NodeDeleted) {
				System.out.println("NodeDeleted");
			} 
		} catch (KeeperException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	public ZooKeeper getZookeeper() {
		return zookeeper;
	}
	public void setZookeeper(ZooKeeper zookeeper) {
		this.zookeeper = zookeeper;
	}
	
}
```

```java
public class ChildrenCallBack implements ChildrenCallback {

	@Override
	public void processResult(int rc, String path, Object ctx, List<String> children) {
		for (String s : children) {
			System.out.println(s);
		}
		System.out.println("ChildrenCallback:" + path);
		System.out.println((String)ctx);	
	}
}

public class Children2CallBack implements Children2Callback {

	@Override
	public void processResult(int rc, String path, Object ctx, List<String> children, Stat stat) {
		for (String s : children) {
			System.out.println(s);
		}
		System.out.println("ChildrenCallback:" + path);
		System.out.println((String)ctx);	
		System.out.println(stat.toString());
	}
}
```

### 判断节点是否存在

```java
/**
 * @Description: zookeeper 判断阶段是否存在demo
 */
public class ZKNodeExist implements Watcher {

	private ZooKeeper zookeeper = null;
	
	public static final String zkServerPath = "192.168.1.110:2181";
	public static final Integer timeout = 5000;
	
	public ZKNodeExist() {}
	
	public ZKNodeExist(String connectString) {
		try {
			zookeeper = new ZooKeeper(connectString, timeout, new ZKNodeExist());
		} catch (IOException e) {
			e.printStackTrace();
			if (zookeeper != null) {
				try {
					zookeeper.close();
				} catch (InterruptedException e1) {
					e1.printStackTrace();
				}
			}
		}
	}
	private static CountDownLatch countDown = new CountDownLatch(1);
	
	public static void main(String[] args) throws Exception {
	
		ZKNodeExist zkServer = new ZKNodeExist(zkServerPath);
		/**
		 * 参数：
		 * path：节点路径
		 * watch：watch
		 */
		Stat stat = zkServer.getZookeeper().exists("/imooc-fake", true);
		if (stat != null) {
			System.out.println("查询的节点版本为dataVersion：" + stat.getVersion());
		} else {
			System.out.println("该节点不存在...");
		}
		countDown.await();
	}
	
	@Override
	public void process(WatchedEvent event) {
		if (event.getType() == EventType.NodeCreated) {
			System.out.println("节点创建");
			countDown.countDown();
		} else if (event.getType() == EventType.NodeDataChanged) {
			System.out.println("节点数据改变");
			countDown.countDown();
		} else if (event.getType() == EventType.NodeDeleted) {
			System.out.println("节点删除");
			countDown.countDown();
		}
	}
	
	public ZooKeeper getZookeeper() {
		return zookeeper;
	}
	public void setZookeeper(ZooKeeper zookeeper) {
		this.zookeeper = zookeeper;
	}
}
```



## ACL 的相关操作



```java
/**
 * 
 * @Description: zookeeper 操作节点acl演示
 */
public class ZKNodeAcl implements Watcher {

	private ZooKeeper zookeeper = null;
	
	public static final String zkServerPath = "192.168.1.110:2181";
	public static final Integer timeout = 5000;
	
	public ZKNodeAcl() {}
	
	public ZKNodeAcl(String connectString) {
		try {
			zookeeper = new ZooKeeper(connectString, timeout, new ZKNodeAcl());
		} catch (IOException e) {
			e.printStackTrace();
			if (zookeeper != null) {
				try {
					zookeeper.close();
				} catch (InterruptedException e1) {
					e1.printStackTrace();
				}
			}
		}
	}
	
	public void createZKNode(String path, byte[] data, List<ACL> acls) {
		
		String result = "";
		try {
			/**
			 * 同步或者异步创建节点，都不支持子节点的递归创建，异步有一个callback函数
			 * 参数：
			 * path：创建的路径
			 * data：存储的数据的byte[]
			 * acl：控制权限策略
			 * 			Ids.OPEN_ACL_UNSAFE --> world:anyone:cdrwa
			 * 			CREATOR_ALL_ACL --> auth:user:password:cdrwa
			 * createMode：节点类型, 是一个枚举
			 * 			PERSISTENT：持久节点
			 * 			PERSISTENT_SEQUENTIAL：持久顺序节点
			 * 			EPHEMERAL：临时节点
			 * 			EPHEMERAL_SEQUENTIAL：临时顺序节点
			 */
			result = zookeeper.create(path, data, acls, CreateMode.PERSISTENT);
			System.out.println("创建节点：\t" + result + "\t成功...");
		} catch (KeeperException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		} 
	}
	
	public static void main(String[] args) throws Exception {
	
		ZKNodeAcl zkServer = new ZKNodeAcl(zkServerPath);
		
		/**
		 * ======================  创建node start  ======================  
		 */
		// acl 任何人都可以访问
//		zkServer.createZKNode("/aclimooc", "test".getBytes(), Ids.OPEN_ACL_UNSAFE);
		
		// 自定义用户认证访问
//		List<ACL> acls = new ArrayList<ACL>();
//		Id imooc1 = new Id("digest", AclUtils.getDigestUserPwd("imooc1:123456"));
//		Id imooc2 = new Id("digest", AclUtils.getDigestUserPwd("imooc2:123456"));
//		acls.add(new ACL(Perms.ALL, imooc1));
//		acls.add(new ACL(Perms.READ, imooc2));
//		acls.add(new ACL(Perms.DELETE | Perms.CREATE, imooc2));
//		zkServer.createZKNode("/aclimooc/testdigest", "testdigest".getBytes(), acls);
		
		// 注册过的用户必须通过addAuthInfo才能操作节点，参考命令行 addauth
//		zkServer.getZookeeper().addAuthInfo("digest", "imooc1:123456".getBytes());
//		zkServer.createZKNode("/aclimooc/testdigest/childtest", 
//        "childtest".getBytes(), Ids.CREATOR_ALL_ACL);
//		Stat stat = new Stat();
//		byte[] data = zkServer.getZookeeper().getData("/aclimooc/testdigest", false, stat);
//		System.out.println(new String(data));
//		zkServer.getZookeeper().setData("/aclimooc/testdigest", "now".getBytes(), 1);
		
		// ip方式的acl
//		List<ACL> aclsIP = new ArrayList<ACL>();
//		Id ipId1 = new Id("ip", "192.168.1.6");
//		aclsIP.add(new ACL(Perms.ALL, ipId1));
//		zkServer.createZKNode("/aclimooc/iptest6", "iptest".getBytes(), aclsIP);

		// 验证ip是否有权限
		zkServer.getZookeeper().setData("/aclimooc/iptest6", "now".getBytes(), 1);
		Stat stat = new Stat();
		byte[] data = zkServer.getZookeeper().getData("/aclimooc/iptest6", false, stat);
		System.out.println(new String(data));
		System.out.println(stat.getVersion());
	}

	public ZooKeeper getZookeeper() {
		return zookeeper;
	}
	public void setZookeeper(ZooKeeper zookeeper) {
		this.zookeeper = zookeeper;
	}
	@Override
	public void process(WatchedEvent event) {		
	}
}

```

