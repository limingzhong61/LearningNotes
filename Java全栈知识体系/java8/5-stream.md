---
sidebar: heading
title: Stream
category: Java
tag:
  - Java8
head:
  - - meta
    - name: keywords
      content: java stream,java流操作
  - - meta
    - name: description
      content: 高质量的Java基础常见知识点和面试题总结，让天下没有难背的八股文！
---

# Stream

使用 `java.util.Stream` 对一个包含一个或多个元素的集合做各种操作，原集合不变，返回新集合。只能对实现了 `java.util.Collection` 接口的类做流的操作。`Map` 不支持 `Stream` 流。`Stream` 流支持同步执行，也支持并发执行。

## Filter 过滤

Filter` 的入参是一个 `Predicate，用于筛选出我们需要的集合元素。原集合不变。filter 会过滤掉不符合特定条件的，下面的代码会过滤掉`nameList`中不以nicolas开头的字符串。

```java
/**
 * @description:
 * @author: 
 * @time: 2021-09-06 00:05
 */
public class StreamTest {
    public static void main(String[] args) {
        List<String> nameList = new ArrayList<>();
        nameList.add("nicolas1");
        nameList.add("nicolas2");
        nameList.add("aaa");
        nameList.add("bbb");

        nameList
                .stream()
                .filter((s) -> s.startsWith("nicolas"))
                .forEach(System.out::println);
    }
    /**
     * output
     * nicolas1
     * nicolas2
     */
}
```

## Sorted 排序

自然排序，不改变原集合，返回排序后的集合。

```java
/**
 * @description:
 * @author: 
 * @time: 2021-09-06 00:05
 */
public class StreamTest1 {
    public static void main(String[] args) {
        List<String> nameList = new ArrayList<>();
        nameList.add("nicolas3");
        nameList.add("nicolas1");
        nameList.add("nicolas2");
        nameList.add("aaa");
        nameList.add("bbb");

        nameList
                .stream()
                .filter((s) -> s.startsWith("nicolas"))
                .sorted()
                .forEach(System.out::println);
    }
    /**
     * output
     * nicolas1
     * nicolas2
     * nicolas3
     */
}
```

逆序排序：

```java
nameList
    .stream()
    .sorted(Comparator.reverseOrder());
```

对元素某个字段排序：

```java
list.stream().sorted(Comparator.comparing(Student::getAge).reversed());
list.stream().sorted(Comparator.comparing(Student::getAge));
```

## Map 转换

将每个字符串转为大写。

```java
/**
 * @description:
 * @author: 
 * @time: 2021-09-06 00:05
 */
public class StreamTest2 {
    public static void main(String[] args) {
        List<String> nameList = new ArrayList<>();
        nameList.add("aaa");
        nameList.add("bbb");

        nameList
                .stream()
                .map(String::toUpperCase)
                .forEach(System.out::println);
    }
    /**
     * output
     * AAA
     * BBB
     */
}
```

## Match 匹配

验证 nameList 中的字符串是否有以`nicolas`开头的。

```java
/**
 * @description:
 * @author: 
 * @time: 2021-09-06 00:05
 */
public class StreamTest3 {
    public static void main(String[] args) {
        List<String> nameList = new ArrayList<>();
        nameList.add("nicolas1");
        nameList.add("nicolas2");

        boolean startWithDabin =
                nameList
                    .stream()
                    .map(String::toUpperCase)
                    .anyMatch((s) -> s.startsWith("nicolas"));

        System.out.println(startWithDabin);
    }
    /**
     * output
     * true
     */
}
```

## Count 计数

统计 `stream` 流中的元素总数，返回值是 `long` 类型。

```java
/**
 * @description:
 * @author: 
 * @time: 2021-09-06 00:05
 */
public class StreamTest4 {
    public static void main(String[] args) {
        List<String> nameList = new ArrayList<>();
        nameList.add("nicolas1");
        nameList.add("nicolas2");
        nameList.add("aaa");

        long count =
                nameList
                    .stream()
                    .map(String::toUpperCase)
                    .filter((s) -> s.startsWith("nicolas"))
                    .count();

        System.out.println(count);
    }
    /**
     * output
     * 2
     */
}
```

## Reduce

类似拼接。可以实现将 `list` 归约成一个值。它的返回类型是 `Optional` 类型。

```java
/**
 * @description:
 * @author: 
 * @time: 2021-09-06 00:22
 */
public class StreamTest5 {
    public static void main(String[] args) {
        List<String> nameList = new ArrayList<>();
        nameList.add("nicolas1");
        nameList.add("nicolas2");

        Optional<String> reduced =
                nameList
                        .stream()
                        .sorted()
                        .reduce((s1, s2) -> s1 + "#" + s2);

        reduced.ifPresent(System.out::println);
    }
    /**
     * output
     * nicolas1#nicolas2
     */
}
```


## flatMap

flatMap 用于将多个Stream连接成一个Stream。

下面的例子，把几个小的list转换到一个大的list。

```java
/**
 * @description: 把几个小的list转换到一个大的list。
 * @author: 
 * @time: 2021-09-06 00:28
 */
public class StreamTest6 {
    public static void main(String[] args) {
        List<String> team1 = Arrays.asList("nicolas1", "nicolas2", "nicolas3");
        List<String> team2 = Arrays.asList("nicolas4", "nicolas5");

        List<List<String>> players = new ArrayList<>();
        players.add(team1);
        players.add(team2);

        List<String> flatMapList = players.stream()
                .flatMap(pList -> pList.stream())
                .collect(Collectors.toList());

        System.out.println(flatMapList);
    }
    /**
     * output
     * [nicolas1, nicolas2, nicolas3, nicolas4, nicolas5]
     */
}
```
下面的例子中，将words数组中的元素按照字符拆分，然后对字符去重。

```java
/**
 * @description:
 * @author: 
 * @time: 2021-09-06 00:35
 */
public class StreamTest7 {
    public static void main(String[] args) {
        List<String> words = new ArrayList<String>();
        words.add("nicolas最强");
        words.add("nicolas666");

        //将words数组中的元素按照字符拆分，然后对字符去重
        List<String> stringList = words.stream()
                .flatMap(word -> Arrays.stream(word.split("")))
                .distinct()
                .collect(Collectors.toList());
        stringList.forEach(e -> System.out.print(e + ", "));
    }
    /**
     * output
     * , , 最, 强, 6,
     */
}
```

## collect

```java
<R, A> R collect(Collector<? super T, A, R> collector);
```

收集为某个集合类型

- Collectors.toSet()

```java
Set<Integer> set1 = IntStream.of(nums1).boxed().collect(Collectors.toSet());
```



# JavaGuide

## Stream

java 新增了 `java.util.stream` 包，它和之前的流大同小异。之前接触最多的是资源流，比如`java.io.FileInputStream`，通过流把文件从一个地方输入到另一个地方，它只是内容搬运工，对文件内容不做任何*CRUD*。

`Stream`依然不存储数据，不同的是它可以检索(Retrieve)和逻辑处理集合数据、包括筛选、排序、统计、计数等。可以想象成是 Sql 语句。

它的源数据可以是 `Collection`、`Array` 等。由于它的方法参数都是函数式接口类型，所以一般和 Lambda 配合使用。

### [#](#流类型) 流类型

1. stream 串行流
2. parallelStream 并行流，可多线程执行

### [#](#常用方法) 常用方法

接下来我们看`java.util.stream.Stream`常用方法



```java
/**
* 返回一个串行流
*/
default Stream<E> stream()

/**
* 返回一个并行流
*/
default Stream<E> parallelStream()

/**
* 返回T的流
*/
public static<T> Stream<T> of(T t)

/**
* 返回其元素是指定值的顺序流。
*/
public static<T> Stream<T> of(T... values) {
    return Arrays.stream(values);
}


/**
* 过滤，返回由与给定predicate匹配的该流的元素组成的流
*/
Stream<T> filter(Predicate<? super T> predicate);

/**
* 此流的所有元素是否与提供的predicate匹配。
*/
boolean allMatch(Predicate<? super T> predicate)

/**
* 此流任意元素是否有与提供的predicate匹配。
*/
boolean anyMatch(Predicate<? super T> predicate);

/**
* 返回一个 Stream的构建器。
*/
public static<T> Builder<T> builder();

/**
* 使用 Collector对此流的元素进行归纳
*/
<R, A> R collect(Collector<? super T, A, R> collector);

/**
 * 返回此流中的元素数。
*/
long count();

/**
* 返回由该流的不同元素（根据 Object.equals(Object) ）组成的流。
*/
Stream<T> distinct();

/**
 * 遍历
*/
void forEach(Consumer<? super T> action);

/**
* 用于获取指定数量的流，截短长度不能超过 maxSize 。
*/
Stream<T> limit(long maxSize);

/**
* 用于映射每个元素到对应的结果
*/
<R> Stream<R> map(Function<? super T, ? extends R> mapper);

/**
* 根据提供的 Comparator进行排序。
*/
Stream<T> sorted(Comparator<? super T> comparator);

/**
* 在丢弃流的第一个 n元素后，返回由该流的 n元素组成的流。
*/
Stream<T> skip(long n);

/**
* 返回一个包含此流的元素的数组。
*/
Object[] toArray();

/**
* 使用提供的 generator函数返回一个包含此流的元素的数组，以分配返回的数组，以及分区执行或调整大小可能需要的任何其他数组。
*/
<A> A[] toArray(IntFunction<A[]> generator);

/**
* 合并流
*/
public static <T> Stream<T> concat(Stream<? extends T> a, Stream<? extends T> b)
```

### [#](#实战) 实战

本文列出 `Stream` 具有代表性的方法之使用，更多的使用方法还是要看 Api。



```java
@Test
public void test() {
  List<String> strings = Arrays.asList("abc", "def", "gkh", "abc");
    //返回符合条件的stream
    Stream<String> stringStream = strings.stream().filter(s -> "abc".equals(s));
    //计算流符合条件的流的数量
    long count = stringStream.count();

    //forEach遍历->打印元素
    strings.stream().forEach(System.out::println);

    //limit 获取到1个元素的stream
    Stream<String> limit = strings.stream().limit(1);
    //toArray 比如我们想看这个limitStream里面是什么，比如转换成String[],比如循环
    String[] array = limit.toArray(String[]::new);

    //map 对每个元素进行操作返回新流
    Stream<String> map = strings.stream().map(s -> s + "22");

    //sorted 排序并打印
    strings.stream().sorted().forEach(System.out::println);

    //Collectors collect 把abc放入容器中
    List<String> collect = strings.stream().filter(string -> "abc".equals(string)).collect(Collectors.toList());
    //把list转为string，各元素用，号隔开
    String mergedString = strings.stream().filter(string -> !string.isEmpty()).collect(Collectors.joining(","));

    //对数组的统计，比如用
    List<Integer> number = Arrays.asList(1, 2, 5, 4);

    IntSummaryStatistics statistics = number.stream().mapToInt((x) -> x).summaryStatistics();
    System.out.println("列表中最大的数 : "+statistics.getMax());
    System.out.println("列表中最小的数 : "+statistics.getMin());
    System.out.println("平均数 : "+statistics.getAverage());
    System.out.println("所有数之和 : "+statistics.getSum());

    //concat 合并流
    List<String> strings2 = Arrays.asList("xyz", "jqx");
    Stream.concat(strings2.stream(),strings.stream()).count();

    //注意 一个Stream只能操作一次，不能断开，否则会报错。
    Stream stream = strings.stream();
    //第一次使用
    stream.limit(2);
    //第二次使用
    stream.forEach(System.out::println);
    //报错 java.lang.IllegalStateException: stream has already been operated upon or closed

    //但是可以这样, 连续使用
    stream.limit(2).forEach(System.out::println);
}
```

### [#](#延迟执行) 延迟执行

在执行返回 `Stream` 的方法时，并不立刻执行，而是等返回一个非 `Stream` 的方法后才执行。因为拿到 `Stream` 并不能直接用，而是需要处理成一个常规类型。这里的 `Stream` 可以想象成是二进制流（2 个完全不一样的东东），拿到也看不懂。

我们下面分解一下 `filter` 方法。



```java
@Test
public void laziness(){
  List<String> strings = Arrays.asList("abc", "def", "gkh", "abc");
  Stream<Integer> stream = strings.stream().filter(new Predicate() {
      @Override
      public boolean test(Object o) {
        System.out.println("Predicate.test 执行");
        return true;
        }
      });

   System.out.println("count 执行");
   stream.count();
}
/*-------执行结果--------*/
count 执行
Predicate.test 执行
Predicate.test 执行
Predicate.test 执行
Predicate.test 执行
```

按执行顺序应该是先打印 4 次「`Predicate.test` 执行」，再打印「`count` 执行」。实际结果恰恰相反。说明 filter 中的方法并没有立刻执行，而是等调用`count()`方法后才执行。

上面都是串行 `Stream` 的实例。并行 `parallelStream` 在使用方法上和串行一样。主要区别是 `parallelStream` 可多线程执行，是基于 ForkJoin 框架实现的，有时间大家可以了解一下 `ForkJoin` 框架和 `ForkJoinPool`。这里可以简单的理解它是通过线程池来实现的，这样就会涉及到线程安全，线程消耗等问题。下面我们通过代码来体验一下并行流的多线程执行。



```java
@Test
public void parallelStreamTest(){
   List<Integer> numbers = Arrays.asList(1, 2, 5, 4);
   numbers.parallelStream() .forEach(num->System.out.println(Thread.currentThread().getName()+">>"+num));
}
//执行结果
main>>5
ForkJoinPool.commonPool-worker-2>>4
ForkJoinPool.commonPool-worker-11>>1
ForkJoinPool.commonPool-worker-9>>2
```

从结果中我们看到，for-each 用到的是多线程。

### [#](#小结) 小结

从源码和实例中我们可以总结出一些 stream 的特点

1. 通过简单的链式编程，使得它可以方便地对遍历处理后的数据进行再处理。
2. 方法参数都是函数式接口类型
3. 一个 Stream 只能操作一次，操作完就关闭了，继续使用这个 stream 会报错。
4. Stream 不保存数据，不改变数据源

------

著作权归Guide所有 原文链接：https://javaguide.cn/java/new-features/java8-common-new-features.html#lambda-%E5%AE%9E%E6%88%98

# 具体使用

## int数组转String数组



```java
String[] x= IntStream.of(new int[]{1, 2, 3}).boxed().map(Object::toString).toArray(String[]::new);
```

技巧： **先collect收集为List，然后转为数组。**

```java
String[] x= IntStream.of(new int[]{1, 2, 3}).boxed().map(i -> i.toString()).collect(Collectors.toList()).toArray(new String[0]);
```

## set 转为list

```java
set.stream().toList();
```

## int数组转为set

```java
Set<Integer> set1 = IntStream.of(nums1).boxed().collect(Collectors.toSet());
```

