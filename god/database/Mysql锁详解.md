## 事务隔离级别的实现方式

### LBCC

传统的隔离级别是基于锁实现的，这种方式叫做 **基于锁的并发控制（Lock-Based Concurrent Control，简写 LBCC）**。通过对读写操作加不同的锁，以及对释放锁的时机进行不同的控制，就可以实现四种隔离级别。传统的锁有两种：读操作通常加共享锁（Share locks，S锁，又叫读锁），写操作加排它锁（Exclusive locks，X锁，又叫写锁）；加了共享锁的记录，其他事务也可以读，但不能写；加了排它锁的记录，其他事务既不能读，也不能写。另外，对于锁的粒度，又分为行锁和表锁，行锁只锁某行记录，对其他行的操作不受影响，表锁会锁住整张表，所有对这个表的操作都受影响。

### MVCC

虽然数据库的四种隔离级别通过 LBCC 技术都可以实现，但是它最大的问题是它只实现了并发的读读，对于并发的读写还是冲突的，写时不能读，读时不能写，当读写操作都很频繁时，数据库的并发性将大大降低，针对这种场景，MVCC 技术应运而生。MVCC 的全称叫做**Multi-Version Concurrent Control（多版本并发控制）**，InnoDb 会为每一行记录增加几个隐含的“辅助字段”，（实际上是 3 个字段：一个隐式的 ID 字段，一个事务 ID，还有一个回滚指针），事务在写一条记录时会将其拷贝一份生成这条记录的一个原始拷贝，写操作同样还是会对原记录加锁，但是读操作会读取未加锁的新记录，这就保证了读写并行。要注意的是，生成的新版本其实就是**undo log**，它也是实现事务回滚的关键技术。

> `InnoDB` 采用的是 MVCC 的实现方式

## MySQL InnoDB 锁介绍



<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210301113422200.png" alt="image-20210301113422200"  /></center>

<center><font size='3'>锁的模式</font></center>

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210301113754438.png" alt="image-20210301113754438"  /></center>

<center><font size='3'>锁的算法</font></center>

### 锁分类

#### 共享锁(行锁)

共享锁( `Shared Locks` )又名读锁，对某一资源加共享锁，自身可以读该资源，其他人也可以读该资源（也可以再继续加共享锁，即共享锁可以多个共存）， 但无法修改。要想修改就必须等所有共享锁都释放完之后才能进行

> 行锁的意思在于: 锁定指定行, 而不是锁定整个表

加锁

```sql
select * from table lock in share mode;
```

释放锁

```sql
commit; rollback;
```

#### 排它锁(行锁)

排他锁( `Exclusive Locks` ), 对某一资源加排他锁,自身可以进行增删改查,其他人无法进行任何操作.  <span style="color: red">注意: 排他锁不能与其他锁并存</span>

加锁

1. 自动: 增删改操作默认会加排它锁
2. 手动: `select * from user where id=1 for update;`

释放锁

```sql
commit; rollback;
```

#### 意向锁(表锁)

* 意向共享锁( `Intention Shared Locks` ) : 表示事务准备给数据行加入共享锁之前-数据行加共享锁的前提是获取此表的共享锁( IS 锁 ) 

* 意向排它锁 ( `Intention Exclusive Locks` ): 表示事务给数据行加入排他锁之前-数据行加锁的前提是获取此表的排他锁( IX锁 ) 

> **意向锁均是表锁,无法手动创建**

### 锁的区间

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/image-20210301150436936.png" alt="image-20210301150436936" style="zoom: 80%;" /></center>

> 例如上图: 表中有 1, 5, 9, 11 四条数据



### 加锁原则



```sql

CREATE TABLE `t` (
  `id` int(11) NOT NULL,
  `c` int(11) DEFAULT NULL,
  `d` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c` (`c`)
) ENGINE=InnoDB;

insert into t values(0,0,0),(5,5,5),
(10,10,10),(15,15,15),(20,20,20),(25,25,25);
```

| id   | c    | d    |
| ---- | ---- | ---- |
| 0    | 0    | 0    |
| 5    | 5    | 5    |
| 10   | 10   | 10   |
| 15   | 15   | 15   |
| 20   | 20   | 20   |
| 25   | 25   | 25   |

总原则如下

* 原则 1：加锁的基本单位是 next-key lock。

* > 这就话的意思是: 进行加锁是, 取条件中的每一个变量的 `next-key lock` , 然后进行加锁区间计算 

* 原则 2：查找过程中访问到的对象才会加锁。

> 这就话的意思是: 如果查询中覆盖索引, 只对该索引加锁, 不对主键索引加锁.<br/>
>
> 有一个例外, 如果使用 `select ... for update` 语句上锁时, MySQL 会认为该语句之后会对主键的数据进行修改, 从而也对主键进行加锁.   

* 优化 1：索引上的等值查询，给唯一索引加锁的时候，next-key lock 退化为行锁。
* 优化 2：索引上的等值查询，向右遍历时且最后一个值不满足等值条件的时候，next-key lock 退化为间隙锁。
* 一个 bug：唯一索引上的范围查询会访问到不满足条件的第一个值为止。

#### 等值查询

-----

<center>唯一索引</center>

* 值存在: 退化为行锁
* 值不存在: 计算该值所处的 `next-key lock` 区间, 把区间改成开区间就是加锁范围

-----

<center>非唯一索引</center>

* 值存在:  值所处的 `next-key lock` 区间 + 下一个 `next-key lock` 的开区间
* 值不存在: 计算该值所处的 `next-key lock` 区间, 把区间改成开区间就是加锁范围

-----

#### 范围查询

**范围查询时唯一索引和非唯一索引的结论是一致的**, 如果查询条件中包含等值查询, 拆分为等值查询,  范围查询(开区间) 等几个查询条件, 然后把各个查询条件的加锁区间的并集就是加锁区间.

以下只讨论开区间查询条件,例如 `select * from t where c < 2 and  c < 5` . 如果查询区间落在1个 `next-key lock` 的范围内, 这个 `next-key` 区间就是加锁区间, 如果落在了多个 `next-key lock` 范围内, 就把这几个区间的求并集, 就是最终的加锁区间

#### 唯一索引范围锁 bug

<center><img src="https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/b105f8c4633e8d3a84e6422b1b1a316d.png" alt="b105f8c4633e8d3a84e6422b1b1a316d"  /></center>

session A 是一个范围查询，按照原则 1 的话，应该是索引 id 上只加 (10,15]这个 next-key lock，并且因为 id 是唯一键，所以循环判断到 id=15 这一行就应该停止了。

但是实现上，InnoDB 会往前扫描到第一个不满足条件的行为止，也就是 id=20。而且由于这是个范围扫描，因此索引 id 上的 (15,20]这个 next-key lock 也会被锁上。

所以你看到了，session B 要更新 id=20 这一行，是会被锁住的。同样地，session C 要插入 id=16 的一行，也会被锁住。

照理说，这里锁住 id=20 这一行的行为，其实是没有必要的。因为扫描到 id=15，就可以确定不用往后再找了。但实现上还是这么做了，因此我认为这是个 bug。

> 以下是 《MySQL实战45讲》作者的原话
>
> 我也曾找社区的专家讨论过，官方 bug 系统上也有提到，但是并未被 verified。所以，认为这是 bug 这个事儿，也只能算我的一家之言，如果你有其他见解的话，也欢迎你提出来。



