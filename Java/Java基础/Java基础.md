---
title: javaSE  
p: java-note/javaSE/javaSE  
date: 2019-10-12 10:32:06  
categories: java  
---

[[toc]]


## 自己相关笔记

<!-- [OnJava8](.\..\Onjava8\OnJava8.md) -->

## java控制台执行  

可以直接编译＋运行  

```cmd  
 java Create.java  
```

## 基础语法

### switch语法结构

1、语句结构
  switch语句从字面上讲，可以称为开关语句，是一种多分支选择结构，一般与case、break、default配合使用，对流程进行控制。
  switch语句的语法格式如下：

```java
switch(表达式){ 
    case 常量表达式1:  语句1;break;
    case 常量表达式2:  语句2;break;
    …… 
    case 常量表达式n:  语句n;break;
    default:  语句n+1;
}
```
switch作为一个开关，当变量表达式的值对应case中的值时，执行case后面的语句后跳出switch语句，如果都不符合则执行default后面的语句后跳出switch语句。
注：**case进入语句后遇到break才会退出**，没有break，会一直运行下去直到整个语句结束。



## 数据类型

### 包装类型

八个基本类型:

- boolean/1
- byte/8
- char/16
- short/16
- int/32
- float/32
- long/64
- double/64

基本类型都有对应的包装类型，基本类型与其对应的包装类型之间的赋值使用自动装箱与拆箱完成。

```java
Integer x = 2;     // 装箱
int y = x;         // 拆箱
```



###  缓存池

new Integer(123) 与 Integer.valueOf(123) 的区别在于:

- new Integer(123) 每次都会新建一个对象
- Integer.valueOf(123) 会使用缓存池中的对象，多次调用会取得同一个对象的引用。

```java
Integer x = new Integer(123);
Integer y = new Integer(123);
System.out.println(x == y);    // false
Integer z = Integer.valueOf(123);
Integer k = Integer.valueOf(123);
System.out.println(z == k);   // true

```

valeOf() 方法的实现比较简单，就是**先判断值是否在缓存池中，如果在的话就直接返回缓存池的内容。**

```java
public static Integer valueOf(int i) {
    if (i >= IntegerCache.low && i <= IntegerCache.high)
        return IntegerCache.cache[i + (-IntegerCache.low)];
    return new Integer(i);
}
```

在 Java 8 中，Integer 缓存池的大小默认为 -128~127。

```java
static final int low = -128;
static final int high;
static final Integer cache[];

static {
    // high value may be configured by property
    int h = 127;
    String integerCacheHighPropValue =
        sun.misc.VM.getSavedProperty("java.lang.Integer.IntegerCache.high");
    if (integerCacheHighPropValue != null) {
        try {
            int i = parseInt(integerCacheHighPropValue);
            i = Math.max(i, 127);
            // Maximum array size is Integer.MAX_VALUE
            h = Math.min(i, Integer.MAX_VALUE - (-low) -1);
        } catch( NumberFormatException nfe) {
            // If the property cannot be parsed into an int, ignore it.
        }
    }
    high = h;

    cache = new Integer[(high - low) + 1];
    int j = low;
    for(int k = 0; k < cache.length; k++)
        cache[k] = new Integer(j++);

    // range [-128, 127] must be interned (JLS7 5.1.7)
    assert IntegerCache.high >= 127;
}

```

编译器会**在缓冲池范围内的基本类型**==自动装箱过程调用 valueOf() 方法==，因此多个 Integer 实例使用自动装箱来创建并且值相同，那么就会引用相同的对象。

```java
Integer m = 123;
Integer n = 123;
System.out.println(m == n); // true
```

基本类型对应的缓冲池如下:

- boolean values true and false
- all byte values
- short values between -128 and 127
- int values between -128 and 127
- char in the range \u0000 to \u007F

在使用这些基本类型对应的包装类型时，就可以直接使用缓冲池中的对象。

如果在缓冲池之外：

```java
Integer m = 323;
Integer n = 323;
System.out.println(m == n); // false
```

### int
主要是有符号整数在计算机中存储采用的补码

在java（任何 32 位字节存储整数的系统）中 -(-2147483648)==(-2147483648)，即

```java
Integer.MIN_VALUE = -Integer.MIN_VALUE
```

参考链接：https://pdai.tech/md/java/basic/java-basic-lan-basic.html



### 浮点数之间的等值判断

**浮点数之间的等值判断，基本数据类型不能用==来比较，包装数据类型不能用equals来判断**。 说明：浮点数采用“尾数+阶码”的编码方式，类似于科学计数法的“有效数字+指数”的表示方式。二进制无法精确表示大部分的十进制小数，具体原理参考《码出高效》。 

####  反例：

  ```java
float a = 1.0F - 0.9F;
float b = 0.9F - 0.8F;
if (a == b) {
    // 预期进入此代码块，执行其它业务逻辑
    // 但事实上a==b的结果为false
}
Float x = Float.valueOf(a);
Float y = Float.valueOf(b);
if (x.equals(y)) {
    // 预期进入此代码块，执行其它业务逻辑
    // 但事实上equals的结果为false
} 
  ```

#### 正例：

(1) 指定一个误差范围，两个浮点数的差值在此范围之内，则认为是相等的。

```java
float a = 1.0F - 0.9F;
float b = 0.9F - 0.8F;
float diff = 1e-6F;
if (Math.abs(a - b) < diff) {
    System.out.println("true");
} 

```

```java
public static boolean equals(double a, double b) {
    float diff = 1e-6F;
    return Math.abs(a - b) < diff;
}
```

(2) 使用BigDecimal来定义值，再进行浮点数的运算操作。

```java
BigDecimal a = new BigDecimal("1.0");
BigDecimal b = new BigDecimal("0.9");
BigDecimal c = new BigDecimal("0.8");
BigDecimal x = a.subtract(b);
BigDecimal y = b.subtract(c);
if (x.compareTo(y) == 0) {
    System.out.println("true");
}
```

来自：java开发手册



## String

###  概览

String 被声明为 final，因此它不可被继承。

**在JDK8中内部使用 char 数组存储数据**，该==数组被声明为 final==，这意味着 value 数组初始化之后就不能再引用其它数组。并且 String 内部没有改变 value 数组的方法，因此**可以保证 String 不可变**。

```java
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence {
    /** The value is used for character storage. */
    private final char value[];
```

### 底层存储的优化

上面说的情况是JDK8及以前版本，到了**JDK9**，String中字符串的存储不再用char数组了，改用byte数组。

```java
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence {

    @Stable
    private final byte[] value;

    private final byte coder;
    
    @Native static final byte LATIN1 = 0;
    @Native static final byte UTF16  = 1;
    
    static final boolean COMPACT_STRINGS;
  
    public String() {
        this.value = "".value;
        this.coder = "".coder;
    }

    @HotSpotIntrinsicCandidate
    public String(String original) {
        this.value = original.value;
        this.coder = original.coder;
        this.hash = original.hash;
    }
    
    // ...
}

```

不仅将char数组改为byte数组，而且新增了一个coder的成员变量。

在程序中，**绝大多数字符串只包含英文字母数字等字符，使用Latin-1编码，一个字符占用一个byte**。如果使用char，一个char要占用两个byte，会占用双倍的内存空间。

但是，如果字符串中使用了中文等超出Latin-1表示范围的字符，使用Latin-1就没办法表示了。这时JDK会使用UTF-16编码，那么**占用的空间和旧版（使用char[]）是一样的。**

coder变量代表编码的格式，目前String支持两种编码格式Latin-1和UTF-16。Latin-1需要用一个字节来存储，而UTF-16需要使用2个字节或者4个字节来存储。

据说这一改进方案是JDK的开发人员用大数据和人工能智能，调研了成千上万的应用程序的heapdump信息后，得出：大部分的String都是以Latin-1字符编码来表示的，只需要一个字节存储就够了，两个字节完全是浪费。

COMPACT_STRINGS属性则是用来控制是否开启String的compact功能。默认情况下是开启的。可以使用-XX:-CompactStrings参数来对此功能进行关闭。

#### 改进的好处

改进的好处是非常明显的，首先如果项目中使用Latin-1字符集居多，内存的占用大幅度减少，同样的硬件配置可以支撑更多的业务。

当内存减少之后，进一步导致减少GC次数，进而减少Stop-The-World的频次，同样会提升系统的性能。

#### 小结

随着JDK的迭代String字符串的内存结构及方法等也在不断地进行演变。这是因为String字符串往往是JVM中占用内存最多的类，通过对它的改造升级，对性能的提升会更加明显。

- https://blog.csdn.net/wo541075754/article/details/114552087

### 不可变的好处

**1. 可以缓存 hash 值**

因为 String 的 hash 值经常被使用，例如 String 用做 HashMap 的 key。不可变的特性可以使得 hash 值也不可变，因此只需要进行一次计算。

**2. String Pool 的需要**

如果一个 String 对象已经被创建过了，那么就会从 String Pool 中取得引用。只有 String 是不可变的，才可能使用 String Pool。

![f76067a5-7d5f-4135-9549-8199c77d8f1c](Java%E5%9F%BA%E7%A1%80/f76067a5-7d5f-4135-9549-8199c77d8f1c.jpg)

String 经常作为参数，String 不可变性可以保证参数不可变。例如在作为网络连接参数的情况下如果 String 是可变的，那么在网络连接过程中，String 被改变，改变 String 对象的那一方以为现在连接的是其它主机，而实际情况却不一定是。

**4. 线程安全**

String 不可变性天生具备线程安全，可以在多个线程中安全地使用。

[Program Creek : Why String is immutable in Java?  (opens new window)](https://www.programcreek.com/2013/04/why-string-is-immutable-in-java/)

### String, StringBuffer and StringBuilder

**1. 可变性**

- String 不可变
- StringBuffer 和 StringBuilder 可变

**2. 线程安全**

- String 不可变，因此是线程安全的
- StringBuilder 不是线程安全的
- StringBuffer 是线程安全的，内部使用 synchronized 进行同步

[StackOverflow : String, StringBuffer, and StringBuilder  (opens new window)](https://stackoverflow.com/questions/2971315/string-stringbuffer-and-stringbuilder)

### String.intern()

使用 String.intern() 可以保证相同内容的字符串变量引用同一的内存对象。

下面示例中，s1 和 s2 采用 new String() 的方式新建了两个不同对象，而 s3 是通过 s1.intern() 方法取得一个对象引用。intern() 首先把 s1 引用的对象放到 String Pool(字符串常量池)中，然后返回这个对象引用。因此 s3 和 s1 引用的是同一个字符串常量池的对象。

```java
String s1 = new String("aaa");
String s2 = new String("aaa");
System.out.println(s1 == s2);           // false
String s3 = s1.intern();
System.out.println(s1.intern() == s3);  // true
```

如果是采用 "bbb" 这种使用双引号的形式创建字符串实例，会自动地将新建的对象放入 String Pool 中。

```java
String s4 = "bbb";
String s5 = "bbb";
System.out.println(s4 == s5);  // true

```

在 Java 7 之前，字符串常量池被放在运行时常量池中，它属于永久代。而在 Java 7，字符串常量池被移到 Native Method 中。这是因为永久代的空间有限，在大量使用字符串的场景下会导致 OutOfMemoryError 错误。

- [StackOverflow : What is String interning?  (opens new window)](https://stackoverflow.com/questions/10578984/what-is-string-interning)
- [深入解析 String#intern  (opens new window)](https://tech.meituan.com/in_depth_understanding_string_intern.html)

## 字符串String  

### 特点  

String内容不可改变  

字符串常量就是String的匿名对象  

所谓的直接赋值实际上就是相当于将一个匿名对象设置了一个名字而已  
	  

String类的匿名对象是由系统自动设置，而不是有用户自己定义的  
String当做参数传递没有改变，是因为新的String通过赋值指向了新的对象，所以对传入的String没有影响  

### 修改类  

StringBuffer  
	  

StringBuffer的内容可以修改  
	  

方法：  
		public StringBuffer reverse()  
		append  
		insert  
		delete  
	线程安全的，都是同步方法  
和String一样都实现了CharSequence接口  
StringBulid  
	是StringBuffer基本一样  
	线程不安全的  

### 两种实例化方式  

直接赋值  
new构造方法  
	  

其内容不会保存在对象池中  
	  

使用new关键字，在堆上开辟一个内存  
	  

手动入池  
		  

public native String intern();  
	  

容易找出空间浪费，不建议使用	  

### 常用函数

| 函数                                                         | 作用                                   |                          |
| ------------------------------------------------------------ | -------------------------------------- | ------------------------ |
| str.trim()                                                   | 除去开头和末尾的空白字符               |                          |
| public static String **join(CharSequence delimiter,         Iterable<? extends CharSequence> elements)** | 给字符数组添加分隔符，并返回一个字符串 | String.join(" ",strList) |
|                                                              |                                        |                          |

### 常见使用

#### 字符串逆置

```java
String reversedStr = new StringBuffer(strs).reverse().toString()
```

#### 使用api统计子串出现次数

```java
import java.util.*;
public class Main{
    /** 
    把他们统一转成小写，然后在判断字符出现的次数
    */
    public static void main(String[] args){
       Scanner scan = new Scanner(System.in);
        //完整的字符串
        String str1 = scan.nextLine().toLowerCase();
        //单个字符
        String str2 = scan.nextLine().toLowerCase();
        //出现的次数 = 完整字符串的长度-单个字符串的长度
        int num = str1.length() - str1.replaceAll(str2,"").length();
        System.out.println(num);
        
    }
}

```



## 枚举enum 
枚举中定义的对象都是当前枚举的类型。
```java
enum  Season{
 
    //提供当前枚举类的多个对象: public static final的
    //每个对象都是Seaon类型
    SPRING("春天","春暖花开"),
    SUMMER("夏天","夏日炎炎"),
    AUTUMN("秋天","秋高气爽"),
    WINTER("冬天","白雪皑皑");
    //声明Season对象的属性priavte final修饰
    private final String seasonName;
    private final String seasonDesc;
 
    //私有化的构造器,并给对象属性赋值
    private Season(String seasonName,String seasonDesc){
        this.seasonName=seasonName;
        this.seasonDesc=seasonDesc;
    }
 
 
 
    //其他诉求:获取枚举类对象的属性
    public String getSeasonName() {
        return seasonName;
    }
 
    public String getSeasonDesc() {
        return seasonDesc;
    }
 
    //4.其他诉灭1:提供toString()
 
    @Override
    public String toString() {
        return "Season{" +
                "seasonName='" + seasonName + '\'' +
                ", seasonDesc='" + seasonDesc + '\'' +
                '}';
    }
}
```



## 常用类  

### 数字类  

### 大数类  

#### 大整数类BigInteger  

String构造方法  
	public BigInteger(String val)  

#### 大浮点数BigDecimal  

构造方法  
	String构造方法  
	double构造方法  
可实现准确的四舍五入操作  
	public BigDecimal divide(BigDecimal divisor, int scale, int roundingMode)  
	除以1实现四舍五入  
		divide(new BigDecimal(1),scale,  
BigDecimal.ROUND_HALF_UP)  
	round(new MathContext(setPrecision, RoundingMode.HALF_UP))  
		MathContext构造方法默认四舍五入  
	setScale(newScale, RoundingMode.HALF_UP)  
		小数位后保留  

### Math类  

 Math类里面提供的方法都是static方法，Math类里面都没有普通方法  
四舍五入round  
	public static long round(double a)  
	如果负数进行四舍五入时，大于-0.5才为-1  

## 集合

### HashMap

Java中的HashMap是一种常用的数据结构，一般用来做数据字典或者Hash查找的容器。

#### 在一个表达式中完成初始化并赋初值的操作


一般我们初始化并赋初值是这样做的：

```java
HashMap<String, Object> map = new HashMap<>();map.put("name", "yanggb");  map.put("name1", "huangq");
```



但是有时候我们会想在一个表达式中完成初始化并赋初值的操作：

```java
HashMap<String, Object> map = new HashMap<>() {    {        put("name", "yanggb");        put("name1", "huangq");    }};
```

这里用了双括号【{{}}】来初始化，使代码简洁易读。第一层括弧实际是**定义了一个匿名内部类 （Anonymous Inner Class）**，第二层括弧实际上是一个**实例初始化块 （Instance Initializer Block）**，这个块在内部匿名类构造时被执行。这种写法的好处很明显，就是一目了然。但是这种写法可能导致这个对象串行化失败的问题。

其一，因为这种方式是匿名内部类的声明方式，所以引用中持有着外部类的引用。所以当串行化这个集合时，外部类也会被不知不觉的串行化，而当外部类没有实现Serialize接口时，就会报错。其二，在上面的例子中，其实是声明了一个继承自HashMap的子类，然而有些串行化方法，例如要通过Gson串行化为json，或者要串行化为xml时，类库中提供的方式，是无法串行化Hashset或者HashMap的子类的，也就导致了串行化失败。解决办法是重新初始化为一个HashMap对象【new HashMap(map);】，这样就可以正常进行初始化了。

另外要注意的是，**这种使用双括号进行初始化的语法在执行效率上要比普通的初始化写法要稍低。**

最后，这个使用**双括号进行初始化的语法同样适用于ArrayList和Set等集合。**

## JDBC  

1、加载数据库驱动  
	E:\app\test\product\11.2.0\dbhome_1\jdbc\lib\ojdbc6.jar  
	  

Oracle驱动类：oracle.jdbc.dirver.OracleDrive  
	连接oracle  
		驱动程序下载oracle自带有  
	  

加载驱动类class.forName("oracle.jdbc.dirver.OracleDrive")  

2、建立数据库连接  
	DriverManager.getConnection(url, user, password)  
	数据库链接地址（URL）  
		oracle  
			jdbc：oracle:连接方式：主机名称：端口号：数据库的SID（Security Identifier）  
			  

连接本机的mldn数据库：  
				jdbc:oracle:thin:@localhost:1521:mldn  
java之中所有的数据库操作类和接口在java.sql  
数据库驱动程序有数据库生成商提供  
JDBC在实现数据库驱动连接对象使用工厂设计设计模式，而DriverManager就是工厂类  
	所以客服端调用连接时，隐藏子类的具体连接实现  

## 正则表达式  

Pattern类  
	获得此类对象必须通过Compile()方法，编译正则表达式  

```java
Pattern p = Pattern.compile("\\d+");
Matcher m = p.matcher(fileName);
```



### Matcher类  

Pattern类获得  

```java
package java.util.regex;
```

| name               | description |      |
| ------------------ | ----------- | ---- |
| public int start() |             |      |
|                    |             |      |
|                    |             |      |



### 字符串的正则运用  

```java
matches()：正则验证  
replaceAll(String regex, String replacement):全部替换  
replaceFirst(String regex, String replacement)：替换首个  
split(String regex) ：全部拆分  
split(String regex, int limit)：部分拆分  
```

#### Pattern,Matcher

**获得表达式中所有的匹配项**

```java
String text = "MyCalendar();\n" +
    "MyCalendar.book(10, 20); // returns true\n" +
    "MyCalendar.book(50, 60); // returns true\n" +
    "MyCalendar.book(10, 40); // returns true\n" +
    "MyCalendar.book(5, 15); // returns false\n" +
    "MyCalendar.book(5, 10); // returns true\n" +
    "MyCalendar.book(25, 55); // returns true\n。";
String rule1 = "\\d+,\\s+\\d+";
Pattern p1 = Pattern.compile(rule1);
Matcher m1 = p1.matcher(text);
String rule2 = "true|false";
Pattern p2 = Pattern.compile(rule2);
Matcher m2 = p2.matcher(text);
while (m1.find()) {
    String group = m1.group(0);
    String group2 = null;
    if (m2.find()) {
        group2 = m2.group(0);
    }
    String[] split = group.split(",");
    System.out.println("匹配结果：" + m1.group(0) + "," + group2);
    System.out.println(myCalendarTwo.book(Integer.parseInt(split[0]), Integer.parseInt(split[1].trim())));

    System.out.println(String.valueOf(myCalendarTwo.book(Integer.parseInt(split[0]), Integer.parseInt(split[1].trim())) ==
                                      Boolean.parseBoolean(group2)).toUpperCase(Locale.ROOT));
}
```



### 正则标记  

都在Pattern类定义  

#### 单个字符（匹配数量1）  

**注意java中转义字符为`'\\'`**

```java
字符：由一个字符组成  
'\\', 转义字符'\'  
'\t'制表符  
'\n' 换行符  
```

#### 字符集（数量1）  

**[],字符集**

[abc]表示字符a、b和c中的任意一个**（或的关系）**  
`[ ^abc]`表示不是abc中任意一个**（^非的关系）**  



**[x-y] x的ascii到y的ascii码之间的值**  

[a-z]所有小写字母**（也可以[e-i])**  

[a-zA-Z]任意字母    

[0-9]任意一位数字  

- 也可以组合使用，如`[A-Z_]`表示大写字母+`_`

#### 简化字符表达式（数量1）  

- `.` :任意一位字符  

- **\w** ,(word): `== [a-zA-Z_0-9]`  	匹配**包括下划线**的任何**单词字符**，注意**也包括数字**

  ```java
  //usage
  Pattern.compile("\\w+\\.");
  ```
  
- \W,匹配任何非单词字符 : = [ ^a-zA-Z_0-9]  


- \W  除了字母、数字、_  [ ^A-z0-9_]  
- `\d`： =[0-9]   (d->digit) 任意的数字
- `\D` : = [ ^0-9]  ，  除了数字
- `\s`:   (s->space) 任意空白字符，如’\t','\n'
- `\S`:  任意非空白字符   
- \b  (b-> boundary)单词边界  
- \B  除了单词边界  

> 小写字母包括，**大写字母取反。** 



边界表达式（不要在java中用，javaScript中用）  
  	^:正则开始  
  	$:正则结束  

#### 数量表达式  

正则`{n}`：表示正则正好出现n次  
		正则`{n,}`：表示正则出现n次及以上  
		正则`{n,m}`：表示正则**出现{n,m}次**  
		正则`？`：==  {0,1}，表示正则可以出现0次或1次  
		正则`*`：== {0,}  表示正则可以出现0次或1次或多次， >= 0
		正则`+`：`=={1,}` 表示正则可以出现1次或1次以上 ，>=1  


#### 逻辑表达式  

	正则1正则2：判断第一个完成以后再判断第二个正则 ,如AB 
	正则1|正则2：两个正则的或  
#### 分组

`(正则)`：**将多个正则作为一组**，可以**为这一组单独设置次数注解**  

### 贪婪模式与非贪婪模式

**正则表达式默认的匹配是贪婪模式**，即总是**尽可能匹配更多的字符串。**
在**正则表达式的后面加 ?则会使用非贪婪模式匹配**，即总是尽可能少的匹配。
直接上个例子，

```java
String str="abcaxc";
Patter p="ab.*c";
```


如果是贪婪模式，上面使用模式p匹配字符串str，结果就是匹配到：abcaxc，匹配到了所有的字符串。

如果是非贪婪模式，上面使用模式p匹配字符串str，结果就是匹配到：abc，只匹配到了部分的字符串。

编程中怎样区分这两种模式？

默认情况下，正则用的都是贪婪模式，**如果要使用非贪婪模式，需要在量词后面直接加上一个问号"?"，**量词包括如下，

(1) {m,n}：m到n个。

(2) *：任意多个。

(3) +：一个到多个。

(4) ?：0或一个。

再上个程序，用贪婪和非贪婪模式找到content中的内容，

```java
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class RegularTest {
  public static void main(String[] arg) {
    String text = "(content:\"hello root\";hello:\"word\";)";
    String rule1 = "content:\".+\"";  // 贪婪模式
    String rule2 = "content:\".+?\""; // 非贪婪模式


    System.out.println("文本：" + text);
    System.out.println("贪婪模式：" + rule1);
    Pattern p1 = Pattern.compile(rule1);
    Matcher m1 = p1.matcher(text);
    while (m1.find()) {
      System.out.println("匹配结果：" + m1.group(0));
    }

 

    System.out.println("非贪婪模式：" + rule2);
    Pattern p2 = Pattern.compile(rule2);
    Matcher m2 = p2.matcher(text);
    while (m2.find()) {
      System.out.println("匹配结果：" + m2.group(0));
    }

  }
}
```

如果是贪婪模式，返回两个字符串，而非贪婪模式，则只返回第一个，

```
文本：(content:"hello root";hello:"word";)
贪婪模式：content:".+"
匹配结果：content:"hello root";hello:"word"
非贪婪模式：content:".+?"
匹配结果：content:"hello root"
```


针对不同场景，我们就可以选择合适的模式。

原文链接：https://blog.csdn.net/bisal/article/details/120714677



## 注解，Annotation  

3个最常用的基础注解  
	声明覆写操作@Override  
		明确告诉编译器覆写，如果没有覆写成功则会报错  
	声明过期操作@desperated  
	压制警告@SupperssWarming  

更多详见：[24 注解,Annotations](./../OnJava8/24Annotations.md)

### 多线程  

实现  
	Thread实现  
	Runnable接口实现，能多继承  
		Thread类有Runnable的构造函数  
	Callable泛型接口实现，能有返回值  
		Thread类没有Callable的构造函数  
		FutureTask类负责接收call方法的返回值（接收Callable构造），实现RunnableFuture接口，RunnableFuture接口实现了Runnable接口、Future接口的get方法（负责接收返回值）  
	需要重写run方法，start开始  
		不用run方法是因为需要判断线程是否重复启动，并且需要不同操作系统提供start0的资源调配方法  
休眠Sleep（Thread）  
	几个线程一起休眠感觉是一起结束（时间长)，当是结束之后还是要抢占资源（时间短）,顺序是不固定的  
优先级  
	优先级越高，越有可能抢占到资源，越有可能执行  
同步synchronized  
	同步代码块  
	同步方法public synchronized 返回值  
等待wait(Object类）  
	notify唤醒  

### 对象克隆  

如果没有实现Cloneable的接口会上抛一个异常  
Cloneable接口  
	没有方法和全局常量  
	此为标识接口，表示一种能力  
需要覆写Object类的clone方法  
	protected native Object clone() throws CloneNotSupportedException;  

## 反射  

“反”通过对象找到类的出处  
java.lang.Class反射的源头  
### 三种实例化方式  
第一种：调用Object类中的getClass()  
	需要对象实例化  
第二种：类.class属性  
	不需要对象实例化，需要import  
	Spring、Hibernate  
第三种：Class提供的forName()方法  
	不需要import导入类，类用String描述  

```java
public static Class<?> forName(String className)  
```

```java
//		 通过Class.forName方式
Class feeClass = null;
try {
    feeClass = Class.forName("pojo.Fee");
} catch (ClassNotFoundException e) {
    e.printStackTrace();
```

### 获取属性

```java
// 获取属性  
Field[] field01 = clazz.getFields(); // 返回属性为public的字段  
Field[] field02 = clazz.getDeclaredFields(); // 返回所有的属性  
Field field03 = clazz.getDeclaredField("id"); // 获取属性为id的字段  
```

#### Field方法:

```java
String name = field.getName();
Class<?> type = field.getType();
```
```java
// 获取对象属性
Fields[] fields = clazz.getDeclaredFields();
for(Field field: fields){
    String name = field.getName();
    field.setAccessible(true); // 私有属性必须设置访问权限
    Object resultValue = field.get(obj); 
    // 这里可以编写你的业务代码
    System.out.println(name + ": " + resultValue);
}
```



### 获取方法

```java
// 获取普通方法  
Method[] Method01 = clazz.getDeclaredMethods(); // 返回public方法 
Method method = clazz.getDeclaredMethod("getId", null); // 返回getId这个方法，如果没有参数，就默认为null   
```

Method使用

```java
method.invoke(obj, new Object[]{});

```

> obj: 调用方法的对象
>
> the object the underlying method is invoked from

```java
Method method = clazz.getMethod(methodName, new Class[]{});
```

> 方法名+参数列表找到指定方法

```java
Object obj = clazz.newInstance();
// 获取对象属性
Fields[] fields = clazz.getDeclaredFields();
for(Field field: fields){
    String fieldName = field.getName();
    String upperChar = fieldName.substring(0,1).toUpperCase();
    String anotherStr = fieldName.substring(1).;
    String methodName = "get" + upperChar + anotherStr;
    Method method = clazz.getMethod(methodName, new Class[]{});
    method.setAccessiable(true);
    Object resultValue = method.invoke(obj, new Object[]{});
    // 这里可以编写你的业务代码
    System.out.println(fieldName + ": " + resultValue);
}
```

反射对象实例化  
	Class类的无参构造方法：public T newInstance()  
	new是耦合的主要元凶，当出现高耦合时大多数时能用反射降低  
		工厂模式  
构造方法调用  
	最好保留无参构造方法，以便构造  

```java
	取得指定构造方法  
		public Constructor<T> getConstructor(Class<?>... parameterTypes)  
			public类型构造方法  
		public Constructor<T> getDeclaredConstructor(Class<?>... parameterTypes)  
			所有构造方法  
	取得一些构造方法    
```



## 函数式编程（Lambda）、流式编程

### 函数式接口

`java.util.function` 包旨在创建一组完整的目标接口，使得我们一般情况下不需再定义自己的接口。这主要是因为基本类型会产生一小部分接口。 如果你了解命名模式，顾名思义就能知道特定接口的作用。

 以下是基本命名准则：

1. 如果**只处理对象而非基本类型**，名称则为 `Function`，`Consumer`，`Predicate` 等。参数类型通过泛型添加。
2. 如果接收的参数是基本类型，则由名称的第一部分表示，如 `LongConsumer`，`DoubleFunction`，`IntPredicate` 等，但基本 `Supplier` 类型例外。
3. 如果返回值为基本类型，则用 `To` 表示，如 `ToLongFunction <T>` 和 `IntToLongFunction`。
4. 如果返回值类型与参数类型一致，则是一个运算符：单个参数使用 `UnaryOperator`，两个参数使用 `BinaryOperator`。
5. 如果接收两个参数且返回值为布尔值，则是一个谓词（Predicate）。
6. 如果接收的两个参数类型不同，则名称中有一个 `Bi`。

下表描述了 `java.util.function` 中的目标类型（包括例外情况）：

| **特征**                                            |                       **函数式方法名**                       |                           **示例**                           |
| :-------------------------------------------------- | :----------------------------------------------------------: | :----------------------------------------------------------: |
| 无参数； <br> 无返回值                              |         **Runnable** <br> (java.lang)  <br>  `run()`         |                         **Runnable**                         |
| 无参数； <br> 返回类型任意                          |         **Supplier** <br> `get()` <br> `getAs类型()`         | **Supplier`<T>`  <br> BooleanSupplier  <br> IntSupplier  <br> LongSupplier  <br> DoubleSupplier** |
| 无参数； <br> 返回类型任意                          |   **Callable** <br> (java.util.concurrent)  <br> `call()`    |                      **Callable`<V>`**                       |
| 1 参数； <br> 无返回值                              |                 **Consumer** <br> `accept()`                 | **`Consumer<T>` <br> IntConsumer <br> LongConsumer <br> DoubleConsumer** |
| 2 参数 **Consumer**                                 |                **BiConsumer** <br> `accept()`                |                    **`BiConsumer<T,U>`**                     |
| 2 参数 **Consumer**； <br> 1 引用； <br> 1 基本类型 |             **Obj类型Consumer** <br> `accept()`              | **`ObjIntConsumer<T>` <br> `ObjLongConsumer<T>` <br> `ObjDoubleConsumer<T>`** |
| 1 参数； <br> 返回类型不同                          | **Function** <br> `apply()` <br> **To类型** 和 **类型To类型** <br> `applyAs类型()` | **Function`<T,R>` <br> IntFunction`<R>` <br> `LongFunction<R>` <br> DoubleFunction`<R>` <br> ToIntFunction`<T>` <br> `ToLongFunction<T>` <br> `ToDoubleFunction<T>` <br> IntToLongFunction <br> IntToDoubleFunction <br> LongToIntFunction <br> LongToDoubleFunction <br> DoubleToIntFunction <br> DoubleToLongFunction** |
| 1 参数； <br> 返回类型相同                          |               **UnaryOperator** <br> `apply()`               | **`UnaryOperator<T>` <br> IntUnaryOperator <br> LongUnaryOperator <br> DoubleUnaryOperator** |
| 2 参数类型相同； <br> 返回类型相同                  |              **BinaryOperator** <br> `apply()`               | **`BinaryOperator<T>` <br> IntBinaryOperator <br> LongBinaryOperator <br> DoubleBinaryOperator** |
| 2 参数类型相同; <br> 返回整型                       |         Comparator <br> (java.util) <br> `compare()`         |                     **`Comparator<T>`**                      |
| 2 参数； <br> 返回布尔型                            |                 **Predicate** <br> `test()`                  | **`Predicate<T>` <br> `BiPredicate<T,U>` <br> IntPredicate <br> LongPredicate <br> DoublePredicate** |
| 参数基本类型； <br> 返回基本类型                    |         **类型To类型Function** <br> `applyAs类型()`          | **IntToLongFunction <br> IntToDoubleFunction <br> LongToIntFunction <br> LongToDoubleFunction <br> DoubleToIntFunction <br> DoubleToLongFunction** |
| 2 参数类型不同                                      |                 **Bi操作** <br> (不同方法名)                 | **`BiFunction<T,U,R>` <br> `BiConsumer<T,U>` <br> `BiPredicate<T,U>` <br> `ToIntBiFunction<T,U>` <br> `ToLongBiFunction<T,U>` <br> `ToDoubleBiFunction<T>`** |

此表仅提供些常规方案。通过上表，你应该或多或少能自行推导出更多行的函数式接口。

可以看出，在创建 `java.util.function` 时，设计者们做出了一些选择。 

例如，为什么没有 `IntComparator`，`LongComparator` 和 `DoubleComparator` 呢？有 `BooleanSupplier` 却没有其他表示 **Boolean** 的接口；有通用的 `BiConsumer` 却没有用于 **int**，**long** 和 **double** 的 `BiConsumers` 变体（我对他们放弃的原因表示同情）。这些选择是疏忽还是有人认为其他组合的使用情况出现得很少（他们是如何得出这个结论的）？

### 流常用处理方法

匹配，遍历中遇到function返回true中断

anyMatch

`anyMatch(Predicate)`：如果流中的任意一个元素根据提供的 **Predicate** 返回 true 时，结果返回为 true。这个操作将会在第一个 true 之后短路；也就是不会在发生 true 之后继续执行计算。



forEach 遍历，全部遍历，不能中断

itearte 自定义序列

根据第一的seed参数应用于第二个function**产生序列**

```java
public static<T> Stream<T> iterate(final T seed, final UnaryOperator<T> f) {
```

> Returns an infinite sequential ordered `Stream` produced by iterative 
> application of a function `f` to an initial element 
> `seed`, producing a `Stream` consisting of 
> `seed`, `f(seed)`, `f(f(seed))`, etc. 

```java
List<String> list = java.util.Arrays.asList("a","b","c");
Stream.iterate(0, i -> i + 1).limit(list.size()).forEach(i -> {
    System.out.println(String.valueOf(i) + list.get(i));
});
```

### 流元素排序

sorted()的默认比较器

```java
Stream<T> sorted();
Stream<T> sorted(Comparator<? super T> comparator);
```

```java
sorted(Comparator.reverseOrder())
```



## 共享设计模式  

	在JVM的底层实际上会存在有一个对象池（不一定只保存String），当String通过直接赋值创建一个String类对象时，会将此匿名对象如此保存，而后若果有新的String通过直接复制并且赋值内容和之前入池的相同，则不会开辟新的堆内存，而是使用之前对象池的引用。  

## 4种代码块  

1、普通代码块  
	代码块写在了方法里面  
	改变变量作用域，能防止重名？（但是什么没有）  
2、构造块  
	代码写在了类里  
	构造块优先于构造块执行，每次构造执行一次（没什么用）  
3、静态代码块  
	非主类  
	主类  
		静态块在主方法前运行  
	为了静态变量的初始化，一个类只执行一次（也没什么用）  
4、同步代码块  
	多线程同步使用  
尽量不要使用代码块



## io流



## transient

*adj.***转瞬即逝的，短暂的；**暂住的，（工作）临时的

***n.*暂住者**，流动人口；（电流、电压、频率的）瞬变

java语言的关键字，[变量](https://baike.baidu.com/item/变量/3956968)[修饰符](https://baike.baidu.com/item/修饰符/4088564)，如果用transient声明一个[实例变量](https://baike.baidu.com/item/实例变量/3386159)，**当对象存储时，它的值不需要维持。换句话来说就是，用transient关键字标记的成员变量不参与序列化过程。**

Java的[serialization](https://baike.baidu.com/item/serialization)提供了一种持久化对象实例的机制。当持久化对象时，可能有一个特殊的对象数据成员，我们不想用serialization机制来保存它。为了在一个特定对象的一个域上关闭serialization，可以在这个域前加上关键字transient。当一个对象被序列化的时候，transient型变量的值不包括在序列化的表示中，然而非transient型的变量是被包括进去的。

## JAVA中的日期类型使用

基本的6种日期类

```java
/**
* 六种时间类型的类
格式的时间三种格式
*/
java.util.Date date = new java.util.Date();//年与日时分秒
//数据库的三种类都继承了java.util.Date，在除了数据库的情况下使用
java.sql.Date sDate = new java.sql.Date(date.getTime());//年月日  
java.sql.Time  sTime = new java.sql.Time(sDate.getTime());//时分秒
java.sql.Timestamp sTimeStamp = new java.sql.Timestamp(sTime.getTime());//年月日时分秒毫秒

//时间格式转换
java.text.SimpleDateFormat dateFormat = new java.text.SimpleDateFormat("yyyy-MM-dd hh:mm:ss");

//日历类是一个抽象基类
java.util.Calendar calender = Calendar.getInstance();//

System.out.println(date);
System.out.println(sDate);
System.out.println(sTime);
System.out.println(sTimeStamp);
System.out.println(calender);

```


输出的日期格式：

```
Thu Mar 28 14:47:18 CST 2019
2019-03-28
14:47:18
2019-03-28 14:47:18.162
java.util.GregorianCalendar[time=1553755638277,areFieldsSet=true,areAllFieldsSet=true,lenient=true,zone=sun.util.calendar.ZoneInfo[id=“Asia/Shanghai”,offset=28800000,dstSavings=0,useDaylight=false,transitions=19,lastRule=null],firstDayOfWeek=1,minimalDaysInFirstWeek=1,ERA=1,YEAR=2019,MONTH=2,WEEK_OF_YEAR=13,WEEK_OF_MONTH=5,DAY_OF_MONTH=28,DAY_OF_YEAR=87,DAY_OF_WEEK=5,DAY_OF_WEEK_IN_MONTH=4,AM_PM=1,HOUR=2,HOUR_OF_DAY=14,MINUTE=47,SECOND=18,MILLISECOND=277,ZONE_OFFSET=28800000,DST_OFFSET=0]
```

由此可以看出几种类的时间格式有差异

| 类名称             | 时间格式         |
| ------------------ | ---------------- |
| java.util.Date     | 年月日时分秒     |
| java.sql.Date      | 年月日           |
| java.sql.Time      | 时分秒           |
| java.sql.Timestamp | 年月日时分秒毫秒 |
| java.util.Calendar | 年月日时分秒毫秒 |


查询源码可知除过Calendar 类外其他的类都是继承java.util.Date类并且屏蔽了相关时间精度，重写了toString()方法。
但是都属于同一父类的继承可以进行相互转换，getTime()方法获取当前时间的秒数还是没有进行重写，获得时间秒数都是一样 （Timestamp除外，Timestamp重写了getTime添加了毫秒数）
	对于基础以上的java.util.Date的继承类来说，都会存在一个问题，那就是对于许多方法都已经废弃掉，**java提供了Calendar 和 SimpleDateFormat 来支持时间日期的更方便操作。**

### Calendar

|                                     |                      |      |
| ----------------------------------- | -------------------- | ---- |
| Calendar.getInstance();             | 返回一个Calendar实例 |      |
| calendar.get(Calendar.DAY_OF_MONTH) | 获取（xx）字段的时间 |      |
|                                     |                      |      |

Java.util.Calendar区别与java.util.Date的几个地方也需要注意一下 ：

- 首先，Calendar增加了毫秒的时间段，通过它可以获取时间点的毫秒值，而java.util.Date只是精确到秒。

- 其次，Calendar过去年的时候是当前年份比如：2010，而Date获取年份的时获取到的是当前年份-1900的一个值（2010-1900=110，因此，你调用getYear后过去的值就是110）。

- Calendar是一个抽象类，之所以能够实例化，是因为此处的Calendar充当了一个类似于工厂的作用，在**getInstance方法中**实例化了Calendar子类GregorianCalendar，并把它返回给用户使用。

- **两个类是可以进行相互转换的**可以使用Calendar类的setTime(Date date)方法可以转换，获取Date队形可以getTime()方法可以转换成Date对象

  ```java
  /** Calendar.class**/
  /**
       * Returns a <code>Date</code> object representing this
       * <code>Calendar</code>'s time value (millisecond offset from the <a
       * href="#Epoch">Epoch</a>").
       *
       * @return a <code>Date</code> representing the time value.
       * @see #setTime(Date)
       * @see #getTimeInMillis()
       */
  public final Date getTime() {
      return new Date(getTimeInMillis());
  }
  
  /**
       * Sets this Calendar's time with the given <code>Date</code>.
       * <p>
       * Note: Calling <code>setTime()</code> with
       * <code>Date(Long.MAX_VALUE)</code> or <code>Date(Long.MIN_VALUE)</code>
       * may yield incorrect field values from <code>get()</code>.
       *
       * @param date the given Date.
       * @see #getTime()
       * @see #setTimeInMillis(long)
       */
  public final void setTime(Date date) {
      setTimeInMillis(date.getTime());
  }
  
  ```

  Calendar和Date可以及逆行转换，也就打通了过时时间类的使用，具体的方法还需要多加练习

  #### Calendar设置日期

  > calendar.set(2022, Calendar.OCTOBER,1);

  ```java
  public static void main(String[] args) {
      SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
  
      Calendar recordStartCalendar = Calendar.getInstance();
      recordStartCalendar.set(2022, Calendar.OCTOBER,1);
      Date recordStartDate = recordStartCalendar.getTime();
      System.out.println(dateFormat.format(recordStartCalendar.getTime()));
  
      //now date
      Date date = new Date();
      Calendar calendar = Calendar.getInstance();
      System.out.println(dateFormat.format(calendar.getTime()));
      System.out.println(recordStartDate.getTime());
      System.out.println(date.getTime());
      long span = date.getTime()  - recordStartDate.getTime();
      System.out.println(span);
      long DayUnit = 24 * 60 * 60 * 1000;
      System.out.println(span / DayUnit);
  
  }
  ```

  

### SimpleDateFormat 日期格式转换

主要使用的是SimpleDateFormat 类的**日期格式转换和日期字符串解析成日期对象**

```java
//时间格式转换
java.text.SimpleDateFormat dateFormat = new java.text.SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
System.out.println("格式转换后：");
//类型转换参数是Date类型，返回值只是 一个字符串
System.out.println(dateFormat.format(date));
System.out.println(dateFormat.format(sDate));
System.out.println(dateFormat.format(sTime));
System.out.println(dateFormat.format(sTimeStamp));
System.out.println(dateFormat.format(calendar.getTime()));


```

格式转换后：

```
2019-03-28 02:47:18
2019-03-28 02:47:18
2019-03-28 02:47:18
2019-03-28 02:47:18
2019-03-28 02:47:18
```



		//时间格式的解析	
		//日期字符转换成日期对象
		//首先进行字符串模式的规定
		java.text.SimpleDateFormat dateFormat1 = new java.text.SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
		//进行字符串的解析,都会解析成Date基类(会产生解析异常)
		java.util.Date date1 = dateFormat1.parse("2020-12-12 12:20:01");
		System.out.println(date1);	
```
Sat Dec 12 00:20:01 CST 2020
```

时间格式的解析，如果时间格式不符合会出现ParseException异常

```java
/**
     * Parses text from the beginning of the given string to produce a date.
     * The method may not use the entire text of the given string.
     * <p>
     * See the {@link #parse(String, ParsePosition)} method for more information
     * on date parsing.
     *
     * @param source A <code>String</code> whose beginning should be parsed.
     * @return A <code>Date</code> parsed from the string.
     * @exception ParseException if the beginning of the specified string
     *            cannot be parsed.
     */
    public Date parse(String source) throws ParseException
    {
        ParsePosition pos = new ParsePosition(0);
        Date result = parse(source, pos);
        if (pos.index == 0)
            throw new ParseException("Unparseable date: \"" + source + "\"" ,
                pos.errorIndex);
        return result;
    }
```


这些时间格式我们应该如何使用
对于现在的日期格式，只要我们几乎都是可以像话转换和借助格式化类行进操作的，具体的到底使用什么类型还是需要看业务需要

```
==针对不同的数据库选用不同的日期类型 ==
```

- Oracle的Date类型，只需要年月日，选择使用java.sql.Date类型
- MS Sqlserver数据库的DateTime类型，需要年月日时分秒，选择java.sql.Timestamp类型

oracle数据库提供的todate()和tochar()函数也可以进行日期格式的转换，所以我们使用的时候最好对日期格式进行格式进行统一转换

相关链接：https://blog.csdn.net/m0_37083940/article/details/88868719

## 相关链接

https://pdai.tech/md/java/basic/java-basic-lan-basic.html