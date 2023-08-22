# Map - HashSet & HashMap 源码解析

> 本文主要对Map - HashSet & HashMap进行源码解析。

- Map - HashSet & HashMap 源码解析
  - Java7 HashMap
    - [概述](#概述)
    - [get()](#get)
    - [put()](#put)
    - [remove()](#remove)
  - Java8 HashMap
    - [put 过程分析](#put-过程分析)
    - [数组扩容](#数组扩容)
    - [get 过程分析](#get-过程分析)
  - [HashSet](#hashset)

##  Java7 HashMap

###  概述

之所以把HashSet和HashSet放在一起讲解，是因为二者在Java里有着相同的实现，前者仅仅是对后者做了一层包装，也就是说HashSet里面有一个HashSet(适配器模式)。因此本文将重点分析HashSet。

HashSet实现了HashSet接口，即允许放入`key`为`null`的元素，也允许插入`value`为`null`的元素；除该类未实现同步外，其余跟`Hashtable`大致相同；跟HashSet不同，该容器不保证元素顺序，根据需要该容器可能会对元素重新哈希，元素的顺序也会被重新打散，因此不同时间迭代同一个HashSet的顺序可能会不同。 根据对冲突的处理方式不同，哈希表有两种实现方式，一种开放地址方式(Open addressing)，另一种是冲突链表方式(Separate chaining with linked lists)。

**Java7 HashMap、HashSet。**

![HashMap_base](img_Map%20-%20HashSet%20&%20HashMap%20%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/HashMap_base.png)从上图容易看出，如果选择合适的哈希函数，`put()`和`get()`方法可以在常数时间内完成。但在对HashSet进行迭代时，需要遍历整个table以及后面跟的冲突链表。因此对于迭代比较频繁的场景，不宜将HashSet的初始大小设的过大。

HashMap的性能: 初始容量(inital capacity)和负载系数(load factor)**。初始容量指定了初始`table`的大小，负载系数用来指定自动扩容的临界值。当`entry`的数量超过`capacity*load_factor`时，容器将自动扩容并重新哈希。对于插入元素较多的场景，将初始容量设大可以减少重新哈希的次数。

将对象放入到HashSet或HashSet中时，有两个方法需要特别关心: `hashCode()`和`equals()`。**`hashCode()`方法决定了对象会被放到哪个`bucket`里，当多个对象的哈希值冲突时，`equals()`方法决定了这些对象是否是“同一个对象”**。所以，如果要将自定义的对象放入到`HashMap`或`HashSet`中，需要**@Override** `hashCode()`和`equals()`方法。

###  get()

`get(Object key)`方法根据指定的`key`值返回对应的`value`，该方法调用了`getEntry(Object key)`得到相应的`entry`，然后返回`entry.getValue()`。因此`getEntry()`是算法的核心。 算法思想是首先通过`hash()`函数得到对应`bucket`的下标，然后依次遍历冲突链表，通过`key.equals(k)`方法来判断是否是要找的那个`entry`。

![HashMap_getEntry](img_Map%20-%20HashSet%20&%20HashMap%20%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/HashMap_getEntry.png)上图中`hash(k)&(table.length-1)`等价于`hash(k)%table.length`，原因是HashSet要求`table.length`必须是2的指数，因此`table.length-1`就是二进制低位全是1，跟`hash(k)`相与会将哈希值的高位全抹掉，剩下的就是余数了。

```Java
//getEntry()方法
final Entry<K,V> getEntry(Object key) {
	......
	int hash = (key == null) ? 0 : hash(key);
    for (Entry<K,V> e = table[hash&(table.length-1)];//得到冲突链表
         e != null; e = e.next) {//依次遍历冲突链表中的每个entry
        Object k;
        //依据equals()方法判断是否相等
        if (e.hash == hash &&
            ((k = e.key) == key || (key != null && key.equals(k))))
            return e;
    }
    return null;
}
```

###  put()

`put(K key, V value)`方法是将指定的`key, value`对添加到`map`里。该方法首先会对`map`做一次查找，看是否包含该元组，如果已经包含则直接返回，查找过程类似于`getEntry()`方法；如果没有找到，则会通过`addEntry(int hash, K key, V value, int bucketIndex)`方法插入新的`entry`，插入方式为HashMap。

![HashMap_addEntry](img_Map%20-%20HashSet%20&%20HashMap%20%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/HashMap_addEntry.png)



```Java
//addEntry()
void addEntry(int hash, K key, V value, int bucketIndex) {
    if ((size >= threshold) && (null != table[bucketIndex])) {
        resize(2 * table.length);//自动扩容，并重新哈希
        hash = (null != key) ? hash(key) : 0;
        bucketIndex = hash & (table.length-1);//hash%table.length
    }
    //在冲突链表头部插入新的entry
    Entry<K,V> e = table[bucketIndex];
    table[bucketIndex] = new Entry<>(hash, key, value, e);
    size++;
}
```

###  remove()

`remove(Object key)`的作用是删除`key`值对应的`entry`，该方法的具体逻辑是在`removeEntryForKey(Object key)`里实现的。`removeEntryForKey()`方法会首先找到`key`值对应的`entry`，然后删除该`entry`(修改链表的相应引用)。查找过程跟`getEntry()`过程类似。

![HashMap_removeEntryForKey](img_Map%20-%20HashSet%20&%20HashMap%20%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/HashMap_removeEntryForKey.png)

```Java
//removeEntryForKey()
final Entry<K,V> removeEntryForKey(Object key) {
	......
	int hash = (key == null) ? 0 : hash(key);
    int i = indexFor(hash, table.length);//hash&(table.length-1)
    Entry<K,V> prev = table[i];//得到冲突链表
    Entry<K,V> e = prev;
    while (e != null) {//遍历冲突链表
        Entry<K,V> next = e.next;
        Object k;
        if (e.hash == hash &&
            ((k = e.key) == key || (key != null && key.equals(k)))) {//找到要删除的entry
            modCount++; size--;
            if (prev == e) table[i] = next;//删除的是冲突链表的第一个entry
            else prev.next = next;
            return e;
        }
        prev = e; e = next;
    }
    return e;
}
```

#  Java8 HashMap

Java8 对 HashMap 进行了一些修改，最大的不同就是利用了红黑树，所以其由 **数组+链表+红黑树** 组成。

根据 Java7 HashMap 的介绍，我们知道，查找的时候，根据 hash 值我们能够快速定位到数组的具体下标，但是之后的话，需要顺着链表一个个比较下去才能找到我们需要的，时间复杂度取决于链表的长度，为 O(n)。

为了降低这部分的开销，在 Java8 中，当链表中的元素达到了 8 个时，会将链表转换为红黑树，在这些位置进行查找的时候可以降低时间复杂度为 O(logN)。

来一张图简单示意一下吧：

![img](img_Map%20-%20HashSet%20&%20HashMap%20%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/java-collection-hashmap8.png)注意，上图是示意图，主要是描述结构，不会达到这个状态的，因为这么多数据的时候早就扩容了。

下面，我们还是用代码来介绍吧，个人感觉，Java8 的源码可读性要差一些，不过精简一些。

Java7 中使用 Entry 来代表每个 HashMap 中的数据节点，Java8 中使用 Node，基本没有区别，都是 key，value，hash 和 next 这四个属性，不过，Node 只能用于链表的情况，红黑树的情况需要使用 TreeNode。

我们根据数组元素中，第一个节点数据类型是 Node 还是 TreeNode 来判断该位置下是链表还是红黑树的。

> 这里需要注意的是，如果链表大小超过阈值（TREEIFY_THRESHOLD, 8），图中的链表就会被改造为树形结构。如果链表长度超过阈值( TREEIFY THRESHOLD==8)，就把链表转成红黑树，链表长度低于6，就把红黑树转回链表。
>
> JDK版本	实现方式	节点数>=8	节点数<=6
> 1.8以前	数组+单向链表	数组+单向链表	数组+单向链表
> 1.8以后	数组+单向链表+红黑树	数组+红黑树	数组+单向链表

## 主要元素

```java
//这两个是限定值 当节点数大于8时会转为红黑树存储
static final int TREEIFY_THRESHOLD = 8;
//当节点数小于6时会转为单向链表存储
static final int UNTREEIFY_THRESHOLD = 6;
//红黑树最小长度为 64
static final int MIN_TREEIFY_CAPACITY = 64;
//HashMap容量初始大小
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16
//HashMap容量极限
static final int MAXIMUM_CAPACITY = 1 << 30;
//负载因子默认大小
static final float DEFAULT_LOAD_FACTOR = 0.75f; // aka 3/4
//Node是Map.Entry接口的实现类
//在此存储数据的Node数组容量是2次幂
//每一个Node本质都是一个单向链表结点
transient Node<K,V>[] table;
//HashMap大小,它代表HashMap保存的键值对的多少
transient int size;
//HashMap被改变的次数
transient int modCount;
//下一次HashMap扩容的大小
int threshold;
//存储负载因子的常量
final float loadFactor;
//默认的构造函数
public HashMap() {
    this.loadFactor = DEFAULT_LOAD_FACTOR; // all other fields defaulted
}
//指定容量大小
public HashMap(int initialCapacity) {
    this(initialCapacity, DEFAULT_LOAD_FACTOR);
}
//指定容量大小和负载因子大小
public HashMap(int initialCapacity, float loadFactor) {
    //指定的容量大小不可以小于0,否则将抛出IllegalArgumentException异常
    if (initialCapacity < 0)
        throw new IllegalArgumentException("Illegal initial capacity: " +
                                           initialCapacity);
    //判定指定的容量大小是否大于HashMap的容量极限
    if (initialCapacity > MAXIMUM_CAPACITY)
        initialCapacity = MAXIMUM_CAPACITY;
    //指定的负载因子不可以小于0或为Null，若判定成立则抛出IllegalArgumentException异常
    if (loadFactor <= 0 || Float.isNaN(loadFactor))
        throw new IllegalArgumentException("Illegal load factor: " +
                                           loadFactor);

    this.loadFactor = loadFactor;
    // 设置“HashMap阈值”，当HashMap中存储数据的数量达到threshold时，就需要将HashMap的容量加倍。
    //tableSizeFor用于查找到大于给定数值的最近2次幂值，比如给定18就是32。给定33就是64。
    this.threshold = tableSizeFor(initialCapacity);
}
//传入一个Map集合,将Map集合中元素Map.Entry全部添加进HashMap实例中
public HashMap(Map<? extends K, ? extends V> m) {
    this.loadFactor = DEFAULT_LOAD_FACTOR;
    //此构造方法主要实现了Map.putAll()
    putMapEntries(m, false);
}

/**
     * Returns a power of two size for the given target capacity.
     */
static final int tableSizeFor(int cap) {
    int n = cap - 1;
    n |= n >>> 1;
    n |= n >>> 2;
    n |= n >>> 4;
    n |= n >>> 8;
    n |= n >>> 16;
    return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
}
```

## 构造方法

```java

/* ---------------- Public operations -------------- */

/**
     * Constructs an empty {@code HashMap} with the specified initial
     * capacity and load factor.
     *
     * @param  initialCapacity the initial capacity
     * @param  loadFactor      the load factor
     * @throws IllegalArgumentException if the initial capacity is negative
     *         or the load factor is nonpositive
     */
public HashMap(int initialCapacity, float loadFactor) {
    if (initialCapacity < 0)
        throw new IllegalArgumentException("Illegal initial capacity: " +
                                           initialCapacity);
    if (initialCapacity > MAXIMUM_CAPACITY)
        initialCapacity = MAXIMUM_CAPACITY;
    if (loadFactor <= 0 || Float.isNaN(loadFactor))
        throw new IllegalArgumentException("Illegal load factor: " +
                                           loadFactor);
    this.loadFactor = loadFactor;
    this.threshold = tableSizeFor(initialCapacity);
}

/**
     * Constructs an empty {@code HashMap} with the specified initial
     * capacity and the default load factor (0.75).
     *
     * @param  initialCapacity the initial capacity.
     */
// 初始化后，第一次 put 的时候;使用该构造方法会计算阈值threshold
public HashMap(int initialCapacity) {
    this(initialCapacity, DEFAULT_LOAD_FACTOR);
}

/**
     * Constructs an empty {@code HashMap} with the default initial capacity
     * (16) and the default load factor (0.75).
     */
public HashMap() {
    this.loadFactor = DEFAULT_LOAD_FACTOR; // all other fields defaulted
}
```



##  put 过程分析

>  TREEIFY_THRESHOLD 为 8，所以，**如果新插入的值是链表中的第 8 个会触发下面的 treeifyBin，也就是将链表转换为红黑树**

注意： 在使用key之前，对key进行了hash()的操作

```java
public V put(K key, V value) {
    return putVal(hash(key), key, value, false, true);
}

// 第四个参数 onlyIfAbsent 如果是 true，那么只有在不存在该 key 时才会进行 put 操作
// 第五个参数 evict 我们这里不关心
final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
               boolean evict) {
    Node<K,V>[] tab; Node<K,V> p; int n, i;
    // 第一次 put 值的时候，会触发下面的 resize()，类似 java7 的第一次 put 也要初始化数组长度
    // 第一次 resize 和后续的扩容有些不一样，因为这次是数组从 null 初始化到默认的 16 或自定义的初始容量
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    // 找到具体的数组下标，如果此位置没有值，那么直接初始化一下 Node 并放置在这个位置就可以了
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);

    else {// 数组该位置有数据
        Node<K,V> e; K k;
        // 首先，判断该位置的第一个数据和我们要插入的数据，key 是不是"相等"，如果是，取出这个节点
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;
        // 如果该节点是代表红黑树的节点，调用红黑树的插值方法，本文不展开说红黑树
        else if (p instanceof TreeNode)
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        else {
            // 到这里，说明数组该位置上是一个链表
            for (int binCount = 0; ; ++binCount) {
                // 插入到链表的最后面(Java7 是插入到链表的最前面)
                if ((e = p.next) == null) {
                    p.next = newNode(hash, key, value, null);
                    // TREEIFY_THRESHOLD 为 8，所以，如果新插入的值是链表中的第 8 个
                    // 会触发下面的 treeifyBin，也就是将链表转换为红黑树
                    if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                        treeifyBin(tab, hash);
                    break;
                }
                // 如果在该链表中找到了"相等"的 key(== 或 equals)
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    // 此时 break，那么 e 为链表中[与要插入的新值的 key "相等"]的 node
                    break;
                p = e;
            }
        }
        // e!=null 说明存在旧值的key与要插入的key"相等"
        // 对于我们分析的put操作，下面这个 if 其实就是进行 "值覆盖"，然后返回旧值
        if (e != null) {
            V oldValue = e.value;
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            afterNodeAccess(e);
            return oldValue;
        }
    }
    ++modCount;
    // 如果 HashMap 由于新插入这个值导致 size 已经超过了阈值，需要进行扩容
    if (++size > threshold)
        resize();
    afterNodeInsertion(evict);
    return null;
}
```

和 Java7 稍微有点不一样的地方就是，Java7 是先扩容后插入新值的，Java8 先插值再扩容，不过这个不重要。

##  数组扩容

resize() 方法用于初始化数组或数组扩容，**每次扩容后，容量为原来的 2 倍，并进行数据迁移。**

### 补充：HashMap 的数组长度为什么是 2 的幂次方

为了能让 HashMap 存取高效，尽量较少碰撞，也就是要尽量把数据分配均匀。我们上面也讲到了过了，Hash 值的范围值-2147483648 到 2147483647，前后加起来大概 40 亿的映射空间，只要哈希函数映射得比较均匀松散，一般应用是很难出现碰撞的。但问题是一个 40 亿长度的数组，内存是放不下的。所以这个散列值是不能直接拿来用的。用之前还要先做对数组的长度取模运算，得到的余数才能用来要存放的位置也就是对应的数组下标。这个**数组下标的计算方法是“ `(n - 1) & hash`”**。（n 代表数组长度）。这也就解释了 HashMap 的长度为什么是 2 的幂次方。

**这个算法应该如何设计呢？**

我们首先可能会想到采用%取余的操作来实现。但是，重点来了：**“取余(%)操作中如果除数是 2 的幂次则等价于与其除数减一的与(&)操作（也就是说 hash%length==hash&(length-1)的前提是 length 是 2 的 n 次方；）。”** 并且 **采用二进制位操作 &，相对于%能够提高运算效率，这就解释了 HashMap 的长度为什么是 2 的幂次方。**

```java
//重新设置table大小/扩容 并返回扩容的Node数组即HashMap的最新数据
final Node<K,V>[] resize() {
    Node<K,V>[] oldTab = table;//table赋予oldTab作为扩充前的table数据
    int oldCap = (oldTab == null) ? 0 : oldTab.length;
    int oldThr = threshold;
    int newCap, newThr = 0;
    if (oldCap > 0) { // 对应数组扩容
        //判定数组是否已达到极限大小，若判定成功将不再扩容，直接将老表返回
        if (oldCap >= MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return oldTab;
        }
        //若新表大小(oldCap*2)小于数组极限大小 并且 老表大于等于数组初始化大小
        // 将数组大小扩大一倍
        else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                 oldCap >= DEFAULT_INITIAL_CAPACITY)
            //旧数组大小oldThr 经二进制运算向左位移1个位置 即 oldThr*2当作新数组的大小
            // 将阈值扩大一倍
            newThr = oldThr << 1; // double threshold
    }
    else if (oldThr > 0) // 对应使用 new HashMap(int initialCapacity) 初始化后，第一次 put 的时候;使用该构造方法会计算阈值threshold
        newCap = oldThr; //将oldThr赋予控制新表大小的newCap
    else {// 对应使用 new HashMap() 初始化后，第一次 put 的时候
        newCap = DEFAULT_INITIAL_CAPACITY;
        newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
    }
	//若新表的下表下一次扩容大小为0
    if (newThr == 0) {
        float ft = (float)newCap * loadFactor;
        newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                  (int)ft : Integer.MAX_VALUE);
    }
    threshold = newThr;//扩容阈值，下次扩容的大小

    // 用新的数组大小初始化新的数组
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab; // 如果是初始化数组，到这里就结束了，返回 newTab 即可

    if (oldTab != null) {//若oldTab中有值需要通过循环将oldTab中的值保存到新表中
        // 开始遍历原数组，进行数据迁移。
        for (int j = 0; j < oldCap; ++j) {
            Node<K,V> e;
            if ((e = oldTab[j]) != null) {//获取老表中第j个元素 赋予e	
                oldTab[j] = null;//并将老表中的元素数据置Null
                // 如果该数组位置上只有单个元素，那就简单了，简单迁移这个元素就可以了
                if (e.next == null)
                    newTab[e.hash & (newCap - 1)] = e;//将e直接存于新表的指定位置
                // 如果是红黑树，具体我们就不展开了
                else if (e instanceof TreeNode)
                    ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                else { 
                    // 这块是处理链表的情况，
                    // 需要将此链表拆成两个链表，放到新的数组中，并且保留原来的先后顺序
                    // loHead、loTail 对应一条链表，hiHead、hiTail 对应另一条链表，代码还是比较简单的
                    Node<K,V> loHead = null, loTail = null;//存储与旧索引的相同的节点
                    Node<K,V> hiHead = null, hiTail = null; //存储与新索引相同的节点
                    Node<K,V> next;
                    do {
                        next = e.next;
                        if ((e.hash & oldCap) == 0) {
                            if (loTail == null)
                                loHead = e;
                            else
                                loTail.next = e;
                            loTail = e;
                        }
                        else {
                            if (hiTail == null)
                                hiHead = e;
                            else
                                hiTail.next = e;
                            hiTail = e;
                        }
                    } while ((e = next) != null);
                     //通过判定将旧数据和新数据存储到新表指定的位置
                    if (loTail != null) {
                        loTail.next = null;
                        // 第一条链表
                        newTab[j] = loHead;
                    }
                    if (hiTail != null) {
                        hiTail.next = null;
                        // 第二条链表的新的位置是 j + oldCap，这个很好理解
                        newTab[j + oldCap] = hiHead;
                    }
                }
            }
        }
    }
    //返回新表
    return newTab;
}
```

详细过程解释：

1.判定数组是否已达到极限大小，若判定成功将不再扩容，直接将老表返回

2.若新表大小(oldCap2)小于数组极限大小&老表大于等于数组初始化大小 判定成功则 旧数组大小oldThr 经二进制运算向左位移1个位置 即 oldThr2当作新数组的大小

2.1. 若[2]的判定不成功，则继续判定 oldThr （代表 老表的下一次扩容量）大于0，若判定成功 则将oldThr赋给newCap作为新表的容量

2.2 若 [2] 和[2.1]判定都失败,则走默认赋值 代表 表为初次创建

3.确定下一次表的扩容量, 将新表赋予当前表

4.通过for循环将老表中德值存入扩容后的新表中

4.1 获取旧表中指定索引下的Node对象 赋予e 并将旧表中的索引位置数据置空

4.2 若e的下面没有其他节点则将e直接赋到新表中的索引位置

4.3 若e的类型为TreeNode红黑树类型

 4.3.1 分割树，将新表和旧表分割成两个树，并判断索引处节点的长度是否需要转换成红黑树放入新表存储

 4.3.2 通过Do循环 不断获取新旧索引的节点

 4.3.3 通过判定将旧数据和新数据存储到新表指定的位置

门限值等于（负载因子）x（容量），如果构建 HashMap 的时候没有指定它们，那么就是依据相应的默认常量值。

门限通常是以倍数进行调整 （newThr = oldThr << 1），我前面提到，根据 putVal 中的逻辑，当元素个数超过门限大小时，则调整 Map 大小。

扩容后，需要将老的数组中的元素重新放置到新的数组，这是扩容的一个主要开销来源。

##  get 过程分析

相对于 put 来说，get 真的太简单了。

1. 计算 key 的 hash 值，**根据 hash 值找到对应数组下标**: hash & (length-1)
1. 判断数组该位置处的元素是否刚好就是我们要找的，如果不是，走第三步
1. 判断该元素类型是否是 TreeNode，如果是，用红黑树的方法取数据，如果不是，走第四步
1. 遍历链表，直到找到相等(==或equals)的 key

```java
public V get(Object key) {
    Node<K,V> e;
    return (e = getNode(hash(key), key)) == null ? null : e.value;
}
final Node<K,V> getNode(int hash, Object key) {
    Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    if ((tab = table) != null && (n = tab.length) > 0 &&
        (first = tab[(n - 1) & hash]) != null) {
        // 判断第一个节点是不是就是需要的
        if (first.hash == hash && // always check first node
            ((k = first.key) == key || (key != null && key.equals(k))))
            return first;
        if ((e = first.next) != null) {
            // 判断是否是红黑树
            if (first instanceof TreeNode)
                return ((TreeNode<K,V>)first).getTreeNode(hash, key);

            // 链表遍历
            do {
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    return e;
            } while ((e = e.next) != null);
        }
    }
    return null;
}
```

##  HashSet

前面已经说过**HashSet是对HashSet的简单包装，对HashSet的函数调用都会转换成合适的HashSet方法**，因此HashSet的实现非常简单，只有不到300行代码。这里不再赘述。

```Java
//HashSet是对HashMap的简单包装
public class HashSet<E>
{
	......
	private transient HashMap<E,Object> map;//HashSet里面有一个HashMap
    // Dummy value to associate with an Object in the backing Map
    private static final Object PRESENT = new Object();
    public HashSet() {
        map = new HashMap<>();
    }
    ......
    public boolean add(E e) {//简单的方法转换
        return map.put(e, PRESENT)==null;
    }
    ......
}
```

## 参考链接

 原文链接：https://pdai.tech/md/java/collection/java-map-HashMap&HashSet.html

------

# will

阅读整合：

https://blog.csdn.net/xadasss/article/details/116793267