# Map - LinkedHashSet&Map源码解析

> 本文主要对Map - LinkedHashSet&Map 源码解析。

- Map - LinkedHashSet&Map源码解析
  - [总体介绍](#总体介绍)
  - 方法剖析
    - [get()](#get)
    - [put()](#put)
    - [remove()](#remove)
  - [LinkedHashSet](#linkedhashset)
  - [LinkedHashMap经典用法](#linkedhashmap经典用法)

https://blog.csdn.net/qq_40050586/article/details/105851970

##  总体介绍

一句话总结，**LinkedHashMap就是HashMap中将其node维护成了一个双向链表entry**。只要搞懂了HashMap就可以很容易搞懂LinkedHashMap。

LinkedHashMap的有序可以按两种顺序排列，一种是按照插入的顺序，一种是按照**读取**的顺序（这个题目的示例就是告诉我们要按照读取的顺序进行排序），而其内部是靠 **建立一个双向链表** 来维护这个顺序的，在每次插入、删除后，都会调用一个函数来进行 **双向链表的维护** ，准确的来说，是有三个函数来做这件事，这三个函数都统称为 **回调函数** ，这三个函数分别是：

- **void afterNodeAccess(Node<K,V> p) { }**
  其作用就是在访问元素之后，将该元素放到双向链表的尾巴处(所以这个函数只有在按照读取的顺序的时候才会执行)，之所以提这个，是建议大家去看看，如何优美的实现在双向链表中将指定元素放入链尾！

- **void afterNodeRemoval(Node<K,V> p) { }**
  其作用就是在删除元素之后，将元素从双向链表中删除，还是非常建议大家去看看这个函数的，很优美的方式在双向链表中删除节点！

- **void afterNodeInsertion(boolean evict) { }**
  这个才是我们题目中会用到的，在插入新元素之后，需要回调函数判断是否需要移除一直不用的某些元素！

  

如果你已看过前面关于*HashSet*和*HashMap*，以及*TreeSet*和*TreeMap*的讲解，一定能够想到本文将要讲解的*LinkedHashSet*和*LinkedHashMap*其实也是一回事。*LinkedHashSet*和*LinkedHashMap*在Java里也有着相同的实现，前者仅仅是对后者做了一层包装，也就是说**LinkedHashSet里面有一个LinkedHashMap(适配器模式)**。因此本文将重点分析*LinkedHashMap*。

*LinkedHashMap*实现了*Map*接口，即允许放入`key`为`null`的元素，也允许插入`value`为`null`的元素。从名字上可以看出该容器是*linked list*和*HashMap*的混合体，也就是说它同时满足*HashMap*和*linked list*的某些特性。**可将*LinkedHashMap*看作采用*linked list*增强的*HashMap*。**

![LinkedHashMap_base.png](img_Map%20-%20LinkedHashSet&Map%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/LinkedHashMap_base.png)

```java
public class LinkedHashMap<K,V> extends HashMap<K,V> implements Map<K,V> {
/**
* LinkedHashMap中的Entry直接继承自HashMap中的Node。并且增加了双向的指针
*/
static class Entry<K,V> extends HashMap.Node<K,V> {
    Entry<K,V> before, after;
    Entry(int hash, K key, V value, Node<K,V> next) {
        super(hash, key, value, next);
    }
}
```

事实上*LinkedHashMap*是*HashMap*的直接子类，**二者唯一的区别是*LinkedHashMap*在*HashMap*的基础上，采用双向链表(doubly-linked list)的形式将所有`entry`连接起来，这样是为保证元素的迭代顺序跟插入顺序相同**。上图给出了*LinkedHashMap*的结构图，主体部分跟*HashMap*完全一样，多了`header`指向双向链表的头部(是一个哑元)，**该双向链表的迭代顺序就是`entry`的插入顺序**。

除了可以保迭代历顺序，这种结构还有一个好处 : **迭代*LinkedHashMap*时不需要像*HashMap*那样遍历整个`table`，而只需要直接遍历`header`指向的双向链表即可**，也就是说*LinkedHashMap*的迭代时间就只跟`entry`的个数相关，而跟`table`的大小无关。

有两个参数可以影响*LinkedHashMap*的性能: 初始容量(inital capacity)和负载系数(load factor)。初始容量指定了初始`table`的大小，负载系数用来指定自动扩容的临界值。当`entry`的数量超过`capacity*load_factor`时，容器将自动扩容并重新哈希。对于插入元素较多的场景，将初始容量设大可以减少重新哈希的次数。

将对象放入到*LinkedHashMap*或*LinkedHashSet*中时，有两个方法需要特别关心: `hashCode()`和`equals()`。**`hashCode()`方法决定了对象会被放到哪个`bucket`里，当多个对象的哈希值冲突时，`equals()`方法决定了这些对象是否是“同一个对象”**。所以，如果要将自定义的对象放入到`LinkedHashMap`或`LinkedHashSet`中，需要@Override `hashCode()`和`equals()`方法。

通过如下方式可以得到一个跟源*Map* **迭代顺序**一样的*LinkedHashMap*:

```Java
void foo(Map m) {
    Map copy = new LinkedHashMap(m);
    ...
}
```

出于性能原因**，*LinkedHashMap*是非同步的(not synchronized)**，如果需要在多线程环境使用，需要程序员手动同步；或者通过如下方式将*LinkedHashMap*包装成(wrapped)同步的:

```java
Map m = Collections.synchronizedMap(new LinkedHashMap(...));
```

## 主要元素

```java
/**
* 头指针，指向第一个node
*/
transient LinkedHashMap.Entry<K,V> head;
/**
* 尾指针，指向最后一个node
*/
transient LinkedHashMap.Entry<K,V> tail;

/**
* 一个条件变量，它控制了是否在get操作后需要将新的get的节点重新放到链表的尾部
* LinkedHashMap可以维持了插入的顺序，但是这个顺序不是不变的，可以被get操作打乱。
*
* @serial
*/
final boolean accessOrder;
```
其他的元素就是直接继承HashMap中的。

## 构造函数

```java
  /**
     * Constructs an empty insertion-ordered <tt>LinkedHashMap</tt> instance
     * with the specified initial capacity and load factor.
     *
     * @param  initialCapacity the initial capacity
     * @param  loadFactor      the load factor
     * @throws IllegalArgumentException if the initial capacity is negative
     *         or the load factor is nonpositive
     */
    public LinkedHashMap(int initialCapacity, float loadFactor) {
        super(initialCapacity, loadFactor);
        accessOrder = false;
    }

    /**
     * 构造一个空的，按插入序（accessOrder = false）的LinkedHashMap，使用默认初始大小和负载因子0.75
     *
     * @param  initialCapacity the initial capacity
     * @throws IllegalArgumentException if the initial capacity is negative
     */
    public LinkedHashMap(int initialCapacity) {
        super(initialCapacity);
        accessOrder = false;
    }

    /**
     * 默认构造函数也是关闭了get改变顺序，使用插入序。
     */
    public LinkedHashMap() {
        super();
        accessOrder = false;
    }

    /**
     * Constructs an insertion-ordered <tt>LinkedHashMap</tt> instance with
     * the same mappings as the specified map.  The <tt>LinkedHashMap</tt>
     * instance is created with a default load factor (0.75) and an initial
     * capacity sufficient to hold the mappings in the specified map.
     *
     * @param  m the map whose mappings are to be placed in this map
     * @throws NullPointerException if the specified map is null
     */
    public LinkedHashMap(Map<? extends K, ? extends V> m) {
        super();
        accessOrder = false;
        putMapEntries(m, false);
    }

    /**
     * 这个构造方法指定了accessOrder
     *
     * @param  initialCapacity the initial capacity
     * @param  loadFactor      the load factor
     * @param  accessOrder     the ordering mode - <tt>true</tt> for
     *         access-order, <tt>false</tt> for insertion-order
     * @throws IllegalArgumentException if the initial capacity is negative
     *         or the load factor is nonpositive
     */
    public LinkedHashMap(int initialCapacity,
                         float loadFactor,
                         boolean accessOrder) {
        super(initialCapacity, loadFactor);
        this.accessOrder = accessOrder;
    }

```
注意，**构造函数如果不明确传入accessOrder的话，默认都是按插入序的。**

## 维护链表的操作

维护链表主要使用三个方法。

afterNodeRemoval，afterNodeInsertion，afterNodeAccess。这三个方法的主要作用是，在删除，插入，获取节点之后，对链表进行维护。简单来说，这三个方法中执行双向链表的操作：

### afterNodeRemoval

顾名思义，在节点remove操作后进行调用：

```java
//在节点删除后，维护链表，传入删除的节点
void afterNodeRemoval(Node<K,V> e) { // unlink
    //p指向待删除元素，b执行前驱，a执行后驱
    LinkedHashMap.Entry<K,V> p =
        (LinkedHashMap.Entry<K,V>)e, b = p.before, a = p.after;
    //这里执行双向链表删除p节点操作，很简单。
    p.before = p.after = null;
    if (b == null)
        head = a;
    else
        b.after = a;
    if (a == null)
        tail = b;
    else
        a.before = b;
}
```
```java
void afterNodeRemoval(Node<K,V> e) { // 优美的一笔，学习一波如何在双向链表中删除节点
    LinkedHashMap.Entry<K,V> p =
        (LinkedHashMap.Entry<K,V>)e, b = p.before, a = p.after;
    // 将 p 节点的前驱后后继引用置空
    p.before = p.after = null;
    // b 为 null，表明 p 是头节点
    if (b == null)
        head = a;
    else
        b.after = a;
    // a 为 null，表明 p 是尾节点
    if (a == null)
        tail = b;
    else
        a.before = b;
}
```



### afterNodeAccess

```java
//在节点被访问后根据accessOrder判断是否需要调整链表顺序
void afterNodeAccess(Node<K,V> e) { // move node to last
    LinkedHashMap.Entry<K,V> last;
    //如果accessOrder为false，什么都不做
    if (accessOrder && (last = tail) != e) {
        //p指向待删除元素，b执行前驱，a执行后驱
        LinkedHashMap.Entry<K,V> p =
            (LinkedHashMap.Entry<K,V>)e, b = p.before, a = p.after;
        //这里执行双向链表删除操作
        p.after = null;
        if (b == null)
            head = a;
        else
            b.after = a;
        if (a != null)
            a.before = b;
        else
            last = b;
        //这里执行将p放到尾部
        if (last == null)
            head = p;
        else {
            p.before = last;
            last.after = p;
        }
        tail = p;
        //保证并发读安全。
        ++modCount;
    }
}

```

来自lc的详细注释

```java
//标准的如何在双向链表中将指定元素放入队尾
// LinkedHashMap 中覆写
//访问元素之后的回调方法

/**
 * 1. 使用 get 方法会访问到节点, 从而触发调用这个方法
 * 2. 使用 put 方法插入节点, 如果 key 存在, 也算要访问节点, 从而触发该方法
 * 3. 只有 accessOrder 是 true 才会调用该方法
 * 4. 这个方法会把访问到的最后节点重新插入到双向链表结尾
 */
void afterNodeAccess(Node<K,V> e) { // move node to last
    // 用 last 表示插入 e 前的尾节点
    // 插入 e 后 e 是尾节点, 所以也是表示 e 的前一个节点
    LinkedHashMap.Entry<K,V> last;
    //如果是访问序，且当前节点并不是尾节点
    //将该节点置为双向链表的尾部
    if (accessOrder && (last = tail) != e) {
        // p: 当前节点
        // b: 前一个节点
        // a: 后一个节点
        // 结构为: b <=> p <=> a
        LinkedHashMap.Entry<K,V> p =
            (LinkedHashMap.Entry<K,V>)e, b = p.before, a = p.after;
        // 结构变成: b <=> p <- a
        p.after = null;

        // 如果当前节点 p 本身是头节点, 那么头结点要改成 a
        if (b == null)
            head = a;
        // 如果 p 不是头尾节点, 把前后节点连接, 变成: b -> a
        else
            b.after = a;

        // a 非空, 和 b 连接, 变成: b <- a
        if (a != null)
            a.before = b;
        // 如果 a 为空, 说明 p 是尾节点, b 就是它的前一个节点, 符合 last 的定义
      	// 这个 else 没有意义，因为最开头if已经确保了p不是尾结点了，自然after不会是null
        else
            last = b;

        // 如果这是空链表, p 改成头结点
        if (last == null)
            head = p;
        // 否则把 p 插入到链表尾部
        else {
            p.before = last;
            last.after = p;
        }
        tail = p;
        ++modCount;
    }
}
```



### afterNodeInsertion

这是一个很奇葩的方法，虽然名字是在插入之后进行的维护链表的操作，但是默认实际上这个什么都没做，看代码：

```java
void afterNodeInsertion(boolean evict) { // possibly remove eldest
    LinkedHashMap.Entry<K,V> first;
    //removeEldestEntry(first)默认返回false，所以afterNodeInsertion这个方法其实并不会执行
    if (evict && (first = head) != null && removeEldestEntry(first)) {
        K key = first.key;
        removeNode(hash(key), key, null, false, true);
    }
}

protected boolean removeEldestEntry(Map.Entry<K,V> eldest) {
    return false;
}
```

为什么不执行也可以呢，这个要到put操作的时候就能看出来了。

那么removeEldestEntry这个方法有什么用呢，看名字可以知道是删除最久远的节点，也就是head节点，这个方法实际是给我们自己扩展的。默认是没有用的，接下来实现LRU的代码中将可以看到它的作用。

```java
// 在插入一个新元素之后，如果是按插入顺序排序，即调用newNode()中的linkNodeLast()完成
// 如果是按照读取顺序排序，即调用afterNodeAccess()完成
// 那么这个方法是干嘛的呢，这个就是著名的 LRU 算法啦
// 在插入完成之后，需要回调函数判断是否需要移除某些元素！
// LinkedHashMap 函数部分源码

/**
 * 插入新节点才会触发该方法，因为只有插入新节点才需要内存
 * 根据 HashMap 的 putVal 方法, evict 一直是 true
 * removeEldestEntry 方法表示移除规则, 在 LinkedHashMap 里一直返回 false
 * 所以在 LinkedHashMap 里这个方法相当于什么都不做
 */
void afterNodeInsertion(boolean evict) { // possibly remove eldest
    LinkedHashMap.Entry<K,V> first;
    // 根据条件判断是否移除最近最少被访问的节点
    if (evict && (first = head) != null && removeEldestEntry(first)) {
        K key = first.key;
        removeNode(hash(key), key, null, false, true);
    }
}

// 移除最近最少被访问条件之一，通过覆盖此方法可实现不同策略的缓存
// LinkedHashMap是默认返回false的，我们可以继承LinkedHashMap然后复写该方法即可
// 例如 LeetCode 第 146 题就是采用该种方法，直接 return size() > capacity;
protected boolean removeEldestEntry(Map.Entry<K,V> eldest) {
    return false;
}
```



##  方法剖析

###  get()

`get(Object key)`方法根据指定的`key`值返回对应的`value`。该方法跟`HashMap.get()`方法的流程几乎完全一样，读者可自行[参考前文在新窗口打开](https://github.com/CarpenterLee/JCFInternals/blob/master/markdown/6-HashSet and HashMap.md#get)，这里不再赘述。 

```java
public V get(Object key) {
    Node<K,V> e;
    // getNode()方法是LinkedHashMap继承的HashMap的方法，而HashMap的get()方法也调用的getNode方法
    if ((e = getNode(hash(key), key)) == null)
        return null;
    if (accessOrder)
        afterNodeAccess(e);
    return e.value;
}
```

###  put()

`put(K key, V value)`方法是将指定的`key, value`对添加到`map`里。

LinkedHashMap没有重写HashMap的put方法，所以执行put操作的时候，还是**使用的是HashMap的put方法**。那么这样如何保证链表的逻辑呢？原因就是HashMap的putVal方法中**实际调用了维护链表的方法**，下面是关键代码：HashMap的putVal()方法

> 1. 如果key结点元素不存在：**LinkedHashMap 重写了 newNode 方法**，在创建节点的时候就维护了链表了
> 2. 如果key结点元素存在： 添加了**LinkedHashMap 重写的afterNodeAccess(e)来更新顺序**（在HashMap中是一个空方法）

```java
//HashMap#putVal(…)
//默认的传入的evict是true
final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
               boolean evict) {
    HashMap.Node<K,V>[] tab; HashMap.Node<K,V> p; int n, i;
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    if ((p = tab[i = (n - 1) & hash]) == null)
        //  LinkedHashMap 重写了 newNode 方法，在创建节点的时候就维护了链表了
        tab[i] = newNode(hash, key, value, null);
    else {
        HashMap.Node<K,V> e; K k;
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;
        else if (p instanceof HashMap.TreeNode)
            e = ((HashMap.TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        else {
            for (int binCount = 0; ; ++binCount) {
                if ((e = p.next) == null) {
                    //  LinkedHashMap 重写了 newNode 方法，在创建节点的时候就维护了链表了
                    p.next = newNode(hash, key, value, null);
                    if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                        treeifyBin(tab, hash);
                    break;
                }
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    break;
                p = e;
            }
        }
        if (e != null) { // existing mapping for key
            //如果e不为null，此时的e指向的就是在map中的那个插入点，所以这个时候来赋值。
            V oldValue = e.value;
            // onlyIfAbsent入口参数，为true，则不更新value（前面已说明）。
            //这个地方的主要作用主要控制如果map中已经有那个key了，是否需要需要更新值
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            //这里其实是插入成功后执行的，获得的效果就是将e放到了链表结尾。
            //所以afterNodeInsertion方法就算什么都不做也可以。
            //但是如果accessOrder为false，那么我们新插入的节点，都不会进入链表了
            // 在HashMap中是一个空方法
            afterNodeAccess(e);
            return oldValue;
        }
    }
    //fast-fail机制的实现，为了保证并发读安全。
    ++modCount;
    //容器中的键值对数自增，如果大于了阈值，开始扩容
    if (++size > threshold)
        resize();
    afterNodeInsertion(evict);
    return null;
}

//LinkedHashMap.Entry
Node<K,V> newNode(int hash, K key, V value, Node<K,V> e) {
    LinkedHashMap.Entry<K,V> p =
        new LinkedHashMap.Entry<K,V>(hash, key, value, e);
    linkNodeLast(p);
    return p;
}
//LinkedHashMap.linkNodeLast
// link at the end of list
private void linkNodeLast(LinkedHashMap.Entry<K,V> p) {
    LinkedHashMap.Entry<K,V> last = tail;
    tail = p;
    if (last == null)
        head = p;
    else {
        p.before = last;
        last.after = p;
    }
}

// Callbacks to allow LinkedHashMap post-actions
void afterNodeAccess(Node<K,V> p) { }
```



```java
//LinkedListHashMap
Node<K,V> newNode(int hash, K key, V value, Node<K,V> e) {
    LinkedHashMap.Entry<K,V> p =
        new LinkedHashMap.Entry<K,V>(hash, key, value, e);
    linkNodeLast(p);
    return p;
}
```


在put方法中，HashMap会在合适的位置使用 afterNodeAccess(e)，和afterNodeInsertion(evict);方法。因为在HashMap中也定义了这三个函数，但是都是为空函数，在LInkedHashMap中只是重写了这3个方法。我们在使用map.put(key,value)的时候，实际调用HashMap#putVal(key,value)方法，然后再调用afterNodeAccess方法，那么这个时候调用的会是子类的afterNodeAccess方法吗？

这个就要涉及到多态的知识了，可以从虚拟机方面去解释：在虚拟机加载类的解析过程中，对方法调用有两种分派方式，静态分派对应重载，动态分派对应重写。这里对应的就是动态分派。动态分配是在运行时发生的，它对于方法是按照实际类型来首先寻找的。找不到再往父类走。这里的实际类型其实值new 后面跟着的类。所以这里不用担心会调用到父类的方法。

afterNodeInsertion方法不是没有用，而是留给扩展用的，下面会展示。

还有一点，put操作中使用afterNodeAccess来将新插入的节点放到尾部。但是这个方法要受到accessOrder的控制，如果accessOrder为false（默认就为false）那么新插入的节点应该就不能插入到链表中了。这样设计有什么特殊的意义吗

### Remove

HashMap#removeNode(…)
和put操作一样，也是直接使用HashMap的方法来完成的：

```java
final Node<K,V> removeNode(int hash, Object key, Object value,
                           boolean matchValue, boolean movable) {
    Node<K,V>[] tab; Node<K,V> p; int n, index;
    //判断table是否为空，该key对应的桶是否为空
    if ((tab = table) != null && (n = tab.length) > 0 &&
        (p = tab[index = (n - 1) & hash]) != null) {
        Node<K,V> node = null, e; K k; V v;
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            node = p;
        else if ((e = p.next) != null) {
            if (p instanceof TreeNode)
                node = ((TreeNode<K,V>)p).getTreeNode(hash, key);
            else {
                do {
                    if (e.hash == hash &&
                        ((k = e.key) == key ||
                         (key != null && key.equals(k)))) {
                        node = e;
                        break;
                    }
                    p = e;
                } while ((e = e.next) != null);
            }
        }
        //到这里了其实node就已经指向了要删除的节点了
        //matchValue的作用是指现在是否需要值匹配。因为可能没有传入value，所以判断一下
        if (node != null && (!matchValue || (v = node.value) == value ||
                             (value != null && value.equals(v)))) {
            if (node instanceof TreeNode)
                ((TreeNode<K,V>)node).removeTreeNode(this, tab, movable);
            else if (node == p)
                tab[index] = node.next;
            else
                p.next = node.next;
            ++modCount;
            --size;
            //调用维护链表的操作
            afterNodeRemoval(node);
            return node;
        }
    }
    return null;
}
```



##  LinkedHashSet

LinkedHashSet继承了HashSet，而HashSet里面有LinkedHashMap，对*LinkedHashSet*的函数调用都会转换成合适的*LinkedHashMap*方法，因此*LinkedHashSet*的实现非常简单，这里不再赘述。

```Java
public class LinkedHashSet<E>
    extends HashSet<E>
    implements Set<E>, Cloneable, java.io.Serializable {
    ......
    // LinkedHashSet继承了HashSet，而HashSet里面有LinkedHashMap
    public LinkedHashSet(int initialCapacity, float loadFactor) {
        //调用HashSet的构造方法
        super(initialCapacity, loadFactor, true);
    }
	......
}
//HashSet
HashSet(int initialCapacity, float loadFactor, boolean dummy) {
    map = new LinkedHashMap<>(initialCapacity, loadFactor);
}
```



## LinkedHashMap用作实现LRU

LRU，即最近最少使用。LRU中保存的数据如果满了，那么就会将最近最少使用的数据删除。

LinkedHashMap通过使accessOrder为true，可以满足这种特性。代码如下：

 [leetcode-146. LRU缓存机制](https://leetcode-cn.com/problems/lru-cache/)

```java
class LRUCache extends LinkedHashMap<Integer, Integer>{
        private int capacity;

        public LRUCache(int capacity) {
            //accessOrder为true
            super(capacity, 0.75F, true);
            this.capacity = capacity;
        }

        public int get(int key) {
            return super.getOrDefault(key, -1);
        }

        public void put(int key, int value) {
            super.put(key, value);
        }

        @Override
        protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
            return size() > capacity;
        }
    }
```

这里重写了removeEldestEntry方法，然后removeEldestEntry方法在afterNodeInsertion中被调用，如果这个方法返回真，那么就会删除head指向的节点。根据每次get的节点都会放到尾部的特性，所以head指向的节点就是最久没有使用到的节点，所以可以删除。由于我们每次put完（HashMap#putVal()）都会调用这个afterNodeInsertion方法，所以可以上面的设计可以使put过后如果size超了，将删除最久没有使用的一个节点，从而腾出空间给新的节点。

## 参考链接

- https://blog.csdn.net/qq_40050586/article/details/105851970
- https://leetcode.cn/problems/lru-cache/solution/yuan-yu-linkedhashmapyuan-ma-by-jeromememory/
- https://pdai.tech/md/java/collection/java-map-LinkedHashMap&LinkedHashSet.html

------

