# ConcurrentHashMap1.8 - 扩容详解

## **简介**

​    **ConcurrenHashMap 在扩容过程中主要使用 sizeCtl 和 transferIndex 这两个属性来协调多线程之间的并发操作，并且在扩容过程中大部分数据依旧可以做到访问不阻塞，具体是如何实现的，请继续 。**

说明：该源码来自于 jdk_1.8.0_162 版本 。

***特别说明：不想看源码可直接跳到后面直接看图解 。***

## ConcurrentHashMap扩容简洁概述



- ConcurrenHashMap 在扩容过程中主要使用 **扩容控制标志位sizeCtl 和 transferIndex表示原Node数组中0到transferIndex-1的需要进行迁移** 这两个属性来协调多线程之间的并发操作，并且在扩容过程中大部分数据依旧可以做到访问不阻塞
- sizeCtl是ConcurrenHashMap 在扩容过程中的控制标志位
- ransferIndex表示原Node数组中0到transferIndex-1的需要迁移 

**put过程（触发扩容的情况之一）：**

- put键值对后，将ConcurrentHashMap中key，value键值对的计数器baseCount通过CAS加一

  - put()方法->putVa()方法-> addCount()方法

- 如果baseCount大于扩容的阈值sizeCtl，则进行扩容

  - 如果sizeCtl > 0 则sizeCtl表示扩容的阈值，表示当前线程是首次触发扩容的线程：如果是首个触发扩容的线程，则将通过CAS修改sizeCtl为**首个扩容线程所设置的特定值，后面扩容时会根据线程是否为这个值来确定是否为最后一个线程**
  - **如果sizeCtl < 0 , 如果不是首个触发扩容的线程，就通过CAS将sizeCtl加1**

  - transfer()方法

**扩容过程,transfer() 方法**：

- **首先计算单个线程处理桶的个数stride**：根据cpu核心数计算单个线程处理桶的数量stride，最少为一个线程处理16个

- **是否需要初始化nextTab数组**：如果新Node数组nextTab为null，则当前线程是首次触发扩容的线程：
  - 为**新Node数组nextTab申请长度为原Node数组的两倍大小的数组**。
  - 将 transferIndex赋值为原Node数组tab的大小，用于计算nextIndex的值
  
- 将**原数组中transferIndex前stride个步长[transferIndex-stride,transferIndex-1]的元素迁移到新的Node数组中**,并在迁移的过程前**通过CAS将transferIndex减去stride的步长**，**便于后序的线程获取自己应该迁移原Node数组的stride步长区间中的元素**。

- **每次迁移完成原Node数组的一个桶时**，将**一个新建的占位对象赋值给原Node数组，这个占位Node对象hash值为-1**，表示该原Node数组中该位置正在进行迁移，

  该占位对象主要有两个用途：

  - put操作时，**用于标识数组该位置的桶已经迁移完毕，处于扩容中的状态**。**其他线程在put时，如果发现Node数组中首节点 hash值为-1，则可以加入到ConcurrentHashMap的扩容过程中**
  - 2、作为一个转发的作用，**扩容期间如果遇到查询操作get，遇到转发节点，会把该查询操作转发到新的数组上去，不会阻塞查询操作**。

- **每当一个线程迁移完后，就将sizeCtl减一，如果sizeCtl减到特定值之后**，就表示当前线程是最后一个线程，则表示ConcurrenHashMap 扩容结束

- 扩容结束后：将新的Node数组nextTable赋值个table，并**将sizeCtl的值修改为扩容后的阈值**



## 一、sizeCtl 属性在各个阶段的作用

(1)、新建而未初始化时

```java
int cap = ((initialCapacity >= (MAXIMUM_CAPACITY >>> 1)) ? MAXIMUM_CAPACITY : tableSizeFor(initialCapacity + (initialCapacity >>> 1) + 1));
this.sizeCtl = cap;
```


作用：**sizeCtl 用于记录初始容量大小**，**仅用于记录集合在实际创建时应该使用的大小的作用** 。

 

(2)、初始化过程中

```java
U.compareAndSwapInt(this, SIZECTL, sc, -1)
```


作用：**将 sizeCtl 值设置为 -1 表示集合正在初始化中**，**其他线程发现该值为 -1 时会让出CPU资源以便初始化操作尽快完成 。**

 

(3)、初始化完成后

```java
Node<K,V>[] nt = (Node<K,V>[])new Node<?,?>[n];
table = tab = nt;
sc = n - (n >>> 2);
sizeCtl = sc;
```


作用：**sizeCtl 用于记录当前集合的负载容量值，也就是触发集合扩容的极限值** 。

 

(4)、正在扩容时

```java
//第一条扩容线程设置的某个特定基数
U.compareAndSwapInt(this, SIZECTL, sc, (rs << RESIZE_STAMP_SHIFT) + 2)
//后续线程加入扩容大军时每次加 1
U.compareAndSwapInt(this, SIZECTL, sc, sc + 1)
//线程扩容完毕退出扩容操作时每次减 1
U.compareAndSwapInt(this, SIZECTL, sc = sizeCtl, sc - 1)
```


作用：**sizeCtl 用于记录当前扩容的并发线程数情况**，此时 sizeCtl 的值为：((rs << RESIZE_STAMP_SHIFT) + 2) + (正在扩容的线程数) ，并且该状态下 sizeCtl < 0 。

 

## 二、什么时候触发扩容？

- put键值对后，通过addCount将ConcurrentHashMap中key，value键值对的计数器baseCount通过CAS加一

sizeCtl扩容标志

- 如果是首个触发扩容的线程，则将通过CAS修改sizeCtl为**首个扩容线程所设置的特定值，后面扩容时会根据线程是否为这个值来确定是否为最后一个线程**
- 如果不是首个触发扩容的线程，就通过CAS将sizeCtl加1

```java
//新增元素时，也就是在调用 putVal 方法后，为了通用，增加了个 check 入参，用于指定是否可能会出现扩容的情况
//check >= 0 即为可能出现扩容的情况，例如 putVal方法中的调用
private final void addCount(long x, int check){
    ... ...
    if (check >= 0) {
        Node<K,V>[] tab, nt; int n, sc;
        //检查当前集合元素个数 s 是否达到扩容阈值 sizeCtl ，扩容时 sizeCtl 为负数，依旧成立，同时还得满足数组非空且数组长度不能大于允许的数组最大长度这两个条件才能继续
        //这个 while 循环除了判断是否达到阈值从而进行扩容操作之外还有一个作用就是当一条线程完成自己的迁移任务后，如果集合还在扩容，则会继续循环，继续加入扩容大军，申请后面的迁移任务
        while (s >= (long)(sc = sizeCtl) && (tab = table) != null && (n = tab.length) < MAXIMUM_CAPACITY) {
            int rs = resizeStamp(n);
            // sc < 0 说明集合正在扩容当中
            if (sc < 0) {
                //判断扩容是否结束或者并发扩容线程数是否已达最大值，如果是的话直接结束while循环
                if ((sc >>> RESIZE_STAMP_SHIFT) != rs || sc == rs + 1 || sc == rs + MAX_RESIZERS || (nt = nextTable) == null || transferIndex <= 0)
                    break;
                //扩容还未结束，并且允许扩容线程加入，此时加入扩容大军中
                if (U.compareAndSwapInt(this, SIZECTL, sc, sc + 1))
                    transfer(tab, nt);
            }
            //如果集合还未处于扩容状态中，则进入扩容方法，并首先初始化 nextTab 数组，也就是新数组
            //(rs << RESIZE_STAMP_SHIFT) + 2 为首个扩容线程所设置的特定值，后面扩容时会根据线程是否为这个值来确定是否为最后一个线程
            else if (U.compareAndSwapInt(this, SIZECTL, sc, (rs << RESIZE_STAMP_SHIFT) + 2))
                transfer(tab, null);
            s = sumCount();
        }
    }
}
```

```java
//扩容状态下其他线程对集合进行插入、修改、删除、合并、compute等操作时遇到 ForwardingNode 节点会调用该帮助扩容方法 (ForwardingNode 后面介绍)
final Node<K,V>[] helpTransfer(Node<K,V>[] tab, Node<K,V> f) {
    Node<K,V>[] nextTab; int sc;
    if (tab != null && (f instanceof ForwardingNode) && (nextTab = ((ForwardingNode<K,V>)f).nextTable) != null) {
        int rs = resizeStamp(tab.length);
        //此处的 while 循环是上面 addCount 方法的简版，可以参考上面的注释
        while (nextTab == nextTable && table == tab && (sc = sizeCtl) < 0) {
            if ((sc >>> RESIZE_STAMP_SHIFT) != rs || sc == rs + 1 ||
                sc == rs + MAX_RESIZERS || transferIndex <= 0)
                break;
            if (U.compareAndSwapInt(this, SIZECTL, sc, sc + 1)) {
                transfer(tab, nextTab);
                break;
            }
        }
        return nextTab;
    }
    return table;
}
```

```java
//putAll批量插入或者插入节点后发现链表长度达到8个或以上，但数组长度为64以下时触发的扩容会调用到这个方法
private final void tryPresize(int size) {
    int c = (size >= (MAXIMUM_CAPACITY >>> 1)) ? MAXIMUM_CAPACITY : tableSizeFor(size + (size >>> 1) + 1);
    int sc;
    //如果不满足条件，也就是 sizeCtl < 0 ，说明有其他线程正在扩容当中，这里也就不需要自己去扩容了，结束该方法
    while ((sc = sizeCtl) >= 0) {
        Node<K,V>[] tab = table; int n;
        //如果数组初始化则进行初始化，这个选项主要是为批量插入操作方法 putAll 提供的
        if (tab == null || (n = tab.length) == 0) {
            n = (sc > c) ? sc : c;
            //初始化时将 sizeCtl 设置为 -1 ，保证单线程初始化
            if (U.compareAndSwapInt(this, SIZECTL, sc, -1)) {
                try {
                    if (table == tab) {
                        @SuppressWarnings("unchecked")
                        Node<K,V>[] nt = (Node<K,V>[])new Node<?,?>[n];
                        table = nt;
                        sc = n - (n >>> 2);
                    }
                } finally {
                    //初始化完成后 sizeCtl 用于记录当前集合的负载容量值，也就是触发集合扩容的阈值
                    sizeCtl = sc;
                }
            }
        }
        else if (c <= sc || n >= MAXIMUM_CAPACITY)
            break;
        //插入节点后发现链表长度达到8个或以上，但数组长度为64以下时触发的扩容会进入到下面这个 else if 分支
        else if (tab == table) {
            int rs = resizeStamp(n);
            //下面的内容基本跟上面 addCount 方法的 while 循环内部一致，可以参考上面的注释
            if (sc < 0) {
                Node<K,V>[] nt;
                if ((sc >>> RESIZE_STAMP_SHIFT) != rs || sc == rs + 1 || sc == rs + MAX_RESIZERS || (nt = nextTable) == null || transferIndex <= 0)
                    break;
                if (U.compareAndSwapInt(this, SIZECTL, sc, sc + 1))
                    transfer(tab, nt);
            }
            else if (U.compareAndSwapInt(this, SIZECTL, sc, (rs << RESIZE_STAMP_SHIFT) + 2))
                transfer(tab, null);
        }
    }
}
```

说明：总的来说

(1) 在**调用 addCount 方法增加集合元素计数后**发现**当前集合元素个数到达扩容阈值时就会触发扩容** 。

(2) **扩容状态下**其他线程对**集合进行插入、修改、删除、合并、compute 等操作时遇到 ForwardingNode 节点会触发扩容 。**

(3) putAll 批量插入或者插入节点后发现存在链表长度达到 8 个或以上，但数组长度为 64 以下时会触发扩容  。

注意：**桶上链表长度达到 8 个或者以上，并且数组长度为 64 以下时只会触发扩容而不会将链表转为红黑树** 。

## CocurrentHashMap相关属性

CocurrentHashMap相关属性

```java
/* ---------------- Fields -------------- */

/**
     * The array of bins. Lazily initialized upon first insertion.
     * Size is always a power of two. Accessed directly by iterators.
     */
transient volatile Node<K,V>[] table;

/**
* The next table to use; non-null only while resizing.
*/
private transient volatile Node<K,V>[] nextTable;
/**
     * Base counter value, used mainly when there is no contention,
     * but also as a fallback during table initialization
     * races. Updated via CAS.
     */
private transient volatile long baseCount;
/**	Node数组table初始化和resize控件。当为负数时，Node数组table正在初始化或者resize
	-1是正在初始化，-(1 + 正在进行数组迁移的线程数)；否则，当table为null时，
	将保留创建时使用的初始表大小，或者保留默认值为0。
	table初始化后，表示Node数组table需要扩容的阈值。
* Table initialization and resizing control.  When negative, the
* table is being initialized or resized: -1 for initialization,
* else -(1 + the number of active resizing threads).  Otherwise,
* when table is null, holds the initial table size to use upon
* creation, or 0 for default. 
*/
private transient volatile int sizeCtl;

/**	调整大小时要分割的下一个表索引(+1)。
* The next table index (plus one) to split while resizing.
*/
private transient volatile int transferIndex;

static final int MOVED     = -1; // hash for forwarding nodes
ForwardingNode<K,V> fwd = new ForwardingNode<K,V>(nextTab);
//java.util.concurrent.ConcurrentHashMap.ForwardingNode
ForwardingNode(Node<K,V>[] tab) {
    super(MOVED, null, null, null);
    this.nextTable = tab;
}
```



## 三、扩容代码详解

transfer() 方法

- **计算单个线程处理桶的个数**：根据cpu核心数计算单个线程处理桶的数量stride，最少为一个线程处理16个

- **是否需要初始化nextTab数组**：有一个nextTab数组，如果为null，则初始化nextTab数组为原Node数组长度的两倍

- 将 transferIndex记为原Node数组tab的大小，用于计算nextIndex的值

- 新建一个占位对象，该占位对象的 hash 值为 -1 该占位对象存在时表示集合正在扩容状态，key、value、next 属性均为 null ，nextTable 属性指向扩容后的数组

  该占位对象主要有两个用途：

  - 1、占位作用，**用于标识数组该位置的桶已经迁移完毕，处于扩容中的状态**。
  - 2、作为一个转发的作用，**扩容期间如果遇到查询操作，遇到转发节点，会把该查询操作转发到新的数组上去，不会阻塞查询操作**。

- 通过CAS比较nextIndex是否和transferIndex相等，如果相等则是第一次计算nextIndex，i=nextIndex-1，i为当前线程迁移原Node数组的位置下标

- 通过迁移下标判断

  - 如果下标i < 0 || i >= 原Node数组tab的大小n || i +原Node数组tab的大小n >= nextn : 表示线程迁移当前原Node数组下标i的位置元素成功
    - 将需要迁移的数组个数sizeCtl通过CAS减一，如果将sizeCtl减至特定的值后，就表示当前线程是最后的线程，则进行Node数组扩容收尾工作，即将新的Node数组赋值给原Node数组的引用，并将扩容状态标志位sizeCtl修改为扩容的阈值
  - **遇到原Node数组下标i的位置为空**，则直接放置一个占位对象，以便查询操作的转发和标识当前处于扩容状态

```java
//调用该扩容方法的地方有：
//java.util.concurrent.ConcurrentHashMap#addCount        向集合中插入新数据后更新容量计数时发现到达扩容阈值而触发的扩容
//java.util.concurrent.ConcurrentHashMap#helpTransfer    扩容状态下其他线程对集合进行插入、修改、删除、合并、compute 等操作时遇到 ForwardingNode 节点时触发的扩容
//java.util.concurrent.ConcurrentHashMap#tryPresize      putAll批量插入或者插入后发现链表长度达到8个或以上，但数组长度为64以下时触发的扩容
private final void transfer(Node<K,V>[] tab, Node<K,V>[] nextTab) {
    int n = tab.length, stride;
    //计算每条线程处理的桶个数，每条线程处理的桶数量一样，如果CPU为单核，则使用一条线程处理所有桶
    //每条线程至少处理16个桶，如果计算出来的结果少于16，则一条线程处理16个桶
    if ((stride = (NCPU > 1) ? (n >>> 3) / NCPU : n) < MIN_TRANSFER_STRIDE)
        stride = MIN_TRANSFER_STRIDE; // subdivide range
    if (nextTab == null) {            // 初始化新数组(原数组长度的2倍)
        try {
            @SuppressWarnings("unchecked")
            Node<K,V>[] nt = (Node<K,V>[])new Node<?,?>[n << 1];
            nextTab = nt;
        } catch (Throwable ex) {      // try to cope with OOME
            sizeCtl = Integer.MAX_VALUE;
            return;
        }
        nextTable = nextTab;
        //将 transferIndex记为原Node数组tab的大小，用于计算nextIndex的值
        transferIndex = n;
    }
    int nextn = nextTab.length;
    //新建一个占位对象，该占位对象的 hash 值为 -1 该占位对象存在时表示集合正在扩容状态，key、value、next 属性均为 null ，nextTable 属性指向扩容后的数组
    //该占位对象主要有两个用途：
    //   1、占位作用，用于标识数组该位置的桶已经迁移完毕，处于扩容中的状态。
    //   2、作为一个转发的作用，扩容期间如果遇到查询操作，遇到转发节点，会把该查询操作转发到新的数组上去，不会阻塞查询操作。
    ForwardingNode<K,V> fwd = new ForwardingNode<K,V>(nextTab);
    //该标识用于控制是否继续处理下一个桶，为 true 则表示已经处理完当前桶，可以继续迁移下一个桶的数据
    boolean advance = true;
    //该标识用于控制扩容何时结束，该标识还有一个用途是最后一个扩容线程会负责重新检查一遍数组查看是否有遗漏的桶
    boolean finishing = false; // to ensure sweep before committing nextTab
    //这个循环用于处理一个 stride 长度的任务，i 后面会被赋值为该 stride 内最大的下标，而 bound 后面会被赋值为该 stride 内最小的下标
    //通过循环不断减小 i 的值，从右往左依次迁移桶上面的数据，直到 i 小于 bound 时结束该次长度为 stride 的迁移任务
    //结束这次的任务后会通过外层 addCount、helpTransfer、tryPresize 方法的 while 循环达到继续领取其他任务的效果
    for (int i = 0, bound = 0;;) {
        Node<K,V> f; int fh;
        while (advance) {
            int nextIndex, nextBound;
            //每处理完一个hash桶就将 bound 进行减 1 操作
            if (--i >= bound || finishing)
                advance = false;
            else if ((nextIndex = transferIndex) <= 0) {
                //transferIndex <= 0 说明数组的hash桶已被线程分配完毕，没有了待分配的hash桶，将 i 设置为 -1 ，后面的代码根据这个数值退出当前线的扩容操作
                i = -1;
                advance = false;
            }
            //只有首次进入for循环才会进入这个判断里面去，设置 bound 和 i 的值，也就是领取到的迁移任务的数组区间
            // TRANSFERINDEX 是transferIndex 在内存中地址的偏离
            else if (U.compareAndSwapInt(this, TRANSFERINDEX, nextIndex, nextBound = (nextIndex > stride ? nextIndex - stride : 0))) {
                bound = nextBound;
                i = nextIndex - 1;
                advance = false;
            }
        }
        if (i < 0 || i >= n || i + n >= nextn) {
            int sc;
            //扩容结束后做后续工作，将 nextTable 设置为 null，表示扩容已结束，将 table 指向新数组，sizeCtl 设置为扩容阈值
            if (finishing) {
                nextTable = null;
                table = nextTab;
                sizeCtl = (n << 1) - (n >>> 1);
                return;
            }
            //每当一条线程扩容结束就会更新一次 sizeCtl 的值，进行减 1 操作
            if (U.compareAndSwapInt(this, SIZECTL, sc = sizeCtl, sc - 1)) {
                //(sc - 2) != resizeStamp(n) << RESIZE_STAMP_SHIFT 成立，说明该线程不是扩容大军里面的最后一条线程，直接return回到上层while循环
                if ((sc - 2) != resizeStamp(n) << RESIZE_STAMP_SHIFT)
                    return;
                //(sc - 2) == resizeStamp(n) << RESIZE_STAMP_SHIFT 说明这条线程是最后一条扩容线程
                //之所以能用这个来判断是否是最后一条线程，因为第一条扩容线程进行了如下操作：
                //    U.compareAndSwapInt(this, SIZECTL, sc, (rs << RESIZE_STAMP_SHIFT) + 2)
                //除了修改结束标识之外，还得设置 i = n; 以便重新检查一遍数组，防止有遗漏未成功迁移的桶
                finishing = advance = true;
                i = n; // recheck before commit
            }
        }
        else if ((f = tabAt(tab, i)) == null)
            //遇到数组上空的位置直接放置一个占位对象，以便查询操作的转发和标识当前处于扩容状态
            advance = casTabAt(tab, i, null, fwd);
        else if ((fh = f.hash) == MOVED)
            //数组上遇到hash值为MOVED，也就是 -1 的位置，说明该位置已经被其他线程迁移过了，将 advance 设置为 true ，以便继续往下一个桶检查并进行迁移操作
            advance = true; // already processed
        else {
            synchronized (f) {
                if (tabAt(tab, i) == f) {
                    Node<K,V> ln, hn;
                    //该节点为链表结构
                    if (fh >= 0) {
                        int runBit = fh & n;
                        Node<K,V> lastRun = f;
                        //遍历整条链表，找出 lastRun 节点
                        for (Node<K,V> p = f.next; p != null; p = p.next) {
                            int b = p.hash & n;
                            if (b != runBit) {
                                runBit = b;
                                lastRun = p;
                            }
                        }
                        //根据 lastRun 节点的高位标识(0 或 1)，首先将 lastRun设置为 ln 或者 hn 链的末尾部分节点，后续的节点使用头插法拼接
                        if (runBit == 0) {
                            ln = lastRun;
                            hn = null;
                        }
                        else {
                            hn = lastRun;
                            ln = null;
                        }
                        //使用高位和低位两条链表进行迁移，使用头插法拼接链表
                        for (Node<K,V> p = f; p != lastRun; p = p.next) {
                            int ph = p.hash; K pk = p.key; V pv = p.val;
                            if ((ph & n) == 0)
                                ln = new Node<K,V>(ph, pk, pv, ln);
                            else
                                hn = new Node<K,V>(ph, pk, pv, hn);
                        }
                        //setTabAt方法调用的是 Unsafe 类的 putObjectVolatile 方法
                        //使用 volatile 方式的 putObjectVolatile 方法，能够将数据直接更新回主内存，并使得其他线程工作内存的对应变量失效，达到各线程数据及时同步的效果
                        //使用 volatile 的方式将 ln 链设置到新数组下标为 i 的位置上
                        setTabAt(nextTab, i, ln);
                        //使用 volatile 的方式将 hn 链设置到新数组下标为 i + n(n为原数组长度) 的位置上
                        setTabAt(nextTab, i + n, hn);
                        //迁移完成后使用 volatile 的方式将占位对象设置到该 hash 桶上，该占位对象的用途是标识该hash桶已被处理过，以及查询请求的转发作用
                        setTabAt(tab, i, fwd);
                        //advance 设置为 true 表示当前 hash 桶已处理完，可以继续处理下一个 hash 桶
                        advance = true;
                    }
                    //该节点为红黑树结构
                    else if (f instanceof TreeBin) {
                        TreeBin<K,V> t = (TreeBin<K,V>)f;
                        //lo 为低位链表头结点，loTail 为低位链表尾结点，hi 和 hiTail 为高位链表头尾结点
                        TreeNode<K,V> lo = null, loTail = null;
                        TreeNode<K,V> hi = null, hiTail = null;
                        int lc = 0, hc = 0;
                        //同样也是使用高位和低位两条链表进行迁移
                        //使用for循环以链表方式遍历整棵红黑树，使用尾插法拼接 ln 和 hn 链表
                        for (Node<K,V> e = t.first; e != null; e = e.next) {
                            int h = e.hash;
                            //这里面形成的是以 TreeNode 为节点的链表
                            TreeNode<K,V> p = new TreeNode<K,V>
                                (h, e.key, e.val, null, null);
                            if ((h & n) == 0) {
                                if ((p.prev = loTail) == null)
                                    lo = p;
                                else
                                    loTail.next = p;
                                loTail = p;
                                ++lc;
                            }
                            else {
                                if ((p.prev = hiTail) == null)
                                    hi = p;
                                else
                                    hiTail.next = p;
                                hiTail = p;
                                ++hc;
                            }
                        }
                        //形成中间链表后会先判断是否需要转换为红黑树：
                        //1、如果符合条件则直接将 TreeNode 链表转为红黑树，再设置到新数组中去
                        //2、如果不符合条件则将 TreeNode 转换为普通的 Node 节点，再将该普通链表设置到新数组中去
                        //(hc != 0) ? new TreeBin<K,V>(lo) : t 这行代码的用意在于，如果原来的红黑树没有被拆分成两份，那么迁移后它依旧是红黑树，可以直接使用原来的 TreeBin 对象
                        ln = (lc <= UNTREEIFY_THRESHOLD) ? untreeify(lo) :
                        (hc != 0) ? new TreeBin<K,V>(lo) : t;
                        hn = (hc <= UNTREEIFY_THRESHOLD) ? untreeify(hi) :
                        (lc != 0) ? new TreeBin<K,V>(hi) : t;
                        //setTabAt方法调用的是 Unsafe 类的 putObjectVolatile 方法
                        //使用 volatile 方式的 putObjectVolatile 方法，能够将数据直接更新回主内存，并使得其他线程工作内存的对应变量失效，达到各线程数据及时同步的效果
                        //使用 volatile 的方式将 ln 链设置到新数组下标为 i 的位置上
                        setTabAt(nextTab, i, ln);
                        //使用 volatile 的方式将 hn 链设置到新数组下标为 i + n(n为原数组长度) 的位置上
                        setTabAt(nextTab, i + n, hn);
                        //迁移完成后使用 volatile 的方式将占位对象设置到该 hash 桶上，该占位对象的用途是标识该hash桶已被处理过，以及查询请求的转发作用
                        setTabAt(tab, i, fwd);
                        //advance 设置为 true 表示当前 hash 桶已处理完，可以继续处理下一个 hash 桶
                        advance = true;
                    }
                }
            }
        }
    }
}
```

 

## 四、扩容过程图解

### 触发扩容的操作

![img](img/img_ConcurrentHashMap1.8%20-%20%E6%89%A9%E5%AE%B9%E8%AF%A6%E8%A7%A3/20190510092825539.png)

总结一下：

(1) 元素个数达到扩容阈值。

(2) 调用 putAll 方法，但目前容量不足以存放所有元素时。

(3) 某条链表长度达到8，但数组长度却小于64时。

 

 

### CPU核数与迁移任务hash桶数量分配的关系

![img](img/img_ConcurrentHashMap1.8%20-%20%E6%89%A9%E5%AE%B9%E8%AF%A6%E8%A7%A3/20190510093016265.png)

 

 

### 单线程下线程的任务分配与迁移操作

![img](img/img_ConcurrentHashMap1.8%20-%20%E6%89%A9%E5%AE%B9%E8%AF%A6%E8%A7%A3/20190510093338545.png)

 

 

 

### 多线程如何分配任务？

![img](img/img_ConcurrentHashMap1.8%20-%20%E6%89%A9%E5%AE%B9%E8%AF%A6%E8%A7%A3/20190510093435247.png)

 

 

 

### 普通链表如何迁移？

![img](img/img_ConcurrentHashMap1.8%20-%20%E6%89%A9%E5%AE%B9%E8%AF%A6%E8%A7%A3/20190510093520878.png)



 

 

### 什么是 lastRun 节点？

![img](img/img_ConcurrentHashMap1.8%20-%20%E6%89%A9%E5%AE%B9%E8%AF%A6%E8%A7%A3/20190510093610941.png)







 

 

 

### 红黑树如何迁移？

![img](img/img_ConcurrentHashMap1.8%20-%20%E6%89%A9%E5%AE%B9%E8%AF%A6%E8%A7%A3/20190510093656144.png)

 

 

 

### hash桶迁移中以及迁移后如何处理存取请求？2

![img](img/img_ConcurrentHashMap1.8%20-%20%E6%89%A9%E5%AE%B9%E8%AF%A6%E8%A7%A3/20190602184408984.png)

 

 

 

### 多线程迁移任务完成后的操作

![img](img/img_ConcurrentHashMap1.8%20-%20%E6%89%A9%E5%AE%B9%E8%AF%A6%E8%A7%A3/20190510093843462.png)



 

 

## 扩展问题：

1、为什么HashMap的容量会小于数组长度？

答：HashMap是为了通过hash值计算出index，从而最快速的访问 。如果容量大于数组很多的话再加上散列算法不是非常优秀的情况下**很容易出现链表过长的情况**，虽然现在出现了红黑树，但是速度依旧不如直接定位到某个数组位置直接获取元素的速度快，所以最理想的情况是数组的每个位置放入一个元素，这样定位最快，从而访问也最快，集合容量小于数组长度的原因在于尽量去分散元素的分布，相当于是拉长了分布的范围，尽量减少集中到一起的概率，从而提高访问的速度，同时，负载因子只要小于 1 ，就不存在容量等于数组长度的情况 。

 

2、扩容期间在未迁移到的hash桶插入数据会发生什么？

答：**只要插入的位置扩容线程还未迁移到，就可以插入，当迁移到该插入的位置时**，就会阻塞等待插入操作完成再继续迁移 。

 

3、正在迁移的hash桶遇到 get 操作会发生什么？

答：在**扩容过程期间形成的 hn 和 ln链 是使用的类似于复制引用的方式**，也就是说 **ln 和 hn 链是复制出来的，而非原来的链表迁移过去的**，所以**原来 hash 桶上的链表并没有受到影响**，因此**从迁移开始到迁移结束这段时间都是可以正常访问原数组 hash 桶上面的链表**，**迁移结束后放置上fwd，往后的访问请求就直接转发到扩容后的数组去了** 。

 

4、如果 lastRun 节点正好在一条全部都为高位或者全部都为低位的链表上，会不会形成死循环？

答：在数组长度为64之前会导致一直扩容，但是到了64或者以上后就会转换为红黑树，因此不会一直死循环 。

 

5、扩容后 ln 和 hn 链不用经过 hash 取模运算，分别被直接放置在新数组的 i 和 n + i 的位置上，那么如何保证这种方式依旧可以用过 h & (n - 1) 正确算出 hash 桶的位置？

答：如果 fh & n-1 = i ，那么扩容之后的 hash 计算方法应该是 fh & 2n-1 。 因为 n 是 2 的幂次方数，所以 如果 n=16， n-1 就是 1111(二进制)， 那么 2n-1 就是 11111 (二进制) 。 其实 **fh & 2n-1 和 fh & n-1 的值区别就在于多出来的那个 1 => fh & (10000) 这个就是两个 hash 的区别所在** 。而 10000 就是 n 。所以说 如果 fh 的第五 bit 不是 1 的话 fh & n = 0 => fh & 2n-1 == fh & n-1 = i 。 如果第5位是 1 的话 。fh & n = n => fh & 2n-1 = i+n 。

 

6、我们都知道，并发情况下，各线程中的数据可能不是最新的，那为什么 get 方法不需要加锁？

答：**get操作全程不需要加锁是因为Node的成员val是用volatile修饰的 。**

 

7、ConcurrentHashMap 的数组上插入节点的操作是否为原子操作，为什么要使用 CAS 的方式？ 

答：待解决 。

 

8、扩容完成后为什么要再检查一遍？

答：为了避免遗漏hash桶，至于为什么会遗漏hash桶，有待后续补充 。

 

特别说明：如有错误欢迎指出，对于目前待解决的后面第  7 、8 两个问题，如有大佬知道还望不吝啬指教，共同交流 。

## Reference

原文链接：https://blog.csdn.net/ZOKEKAI/article/details/90051567