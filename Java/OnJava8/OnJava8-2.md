---
title: OnJava8-2
date: 2019-10-13 22:19:09
---
[TOC]
 
<!-- Validating Your Code -->

# 第十六章 代码校验

> 你永远不能保证你的代码是正确的，你只能证明它是错的。

<!-- Testing -->

## 测试

> 如果没有测试过，它就是不能工作的。

### 单元测试

这个过程是将集成测试构建到你创建的所有代码中，并在**每次构建系统时运行这些测试**。这样，构建过程不仅能检查语法的错误，同时也能检查语义的错误。

“单元”是指测试一小部分代码 。通常，**每个类都有测试来检查它所有方法的行为。**“系统”测试则是不同的，它检查的是整个程序是否满足要求。

C 风格的语言，尤其是 C++，通常会认为性能比安全更重要。用 Java 编程比 C++（一般认为大概快两倍）快的原因是 Java 的安全性保障：比如垃圾回收以及改良的类型检测等特性。通过将单元测试集成到构建过程中，你扩大了这个安全保障，因而有了更快的开发效率。当发现设计或实现的缺陷时，可以更容易、更大胆地重构你的代码。

### JUnit

[官网](https://junit.org/)

反射和注解得到了极大的改进,增加了对 lambdas 表达式的支持

在 JUnit 最简单的使用中，使用 **@Test** 注解标记表示测试的每个方法。JUnit 将这些方法标识为单独的测试，并一次设置和运行一个测试，采取措施避免测试之间的副作用。

**@BeforeAll** 注解是在任何其他测试操作之前运行一次的方法。 **@AfterAll** 是所有其他测试操作之后只运行一次的方法。两个方法都必须是静态的。

**@BeforeEach**注解是通常用于创建和初始化公共对象的方法，并在每次测试前运行。可以将所有这样的初始化放在测试类的构造函数中，尽管我认为 **@BeforeEach** 更加清晰。JUnit为每个测试创建一个对象，确保测试运行之间没有副作用。然而，所有测试的所有对象都是同时创建的(而不是在测试之前创建对象)，所以使用 **@BeforeEach** 和构造函数之间的唯一区别是 **@BeforeEach** 在测试前直接调用。在大多数情况下，这不是问题，如果你愿意，可以使用构造函数方法。

如果你必须在每次测试后执行清理（如果修改了需要恢复的静态文件，打开文件需要关闭，打开数据库或者网络连接，etc），那就用注解 **@AfterEach**。

JUnit 使用 **@Test** 注解发现这些方法，并将每个方法作为测试运行。在方法内部，你可以执行任何所需的操作并使用 JUnit 断言方法（以"assert"开头）验证测试的正确性（更全面的"assert"说明可以在 Junit 文档里找到）。如果断言失败，将显示导致失败的表达式和值。这通常就足够了，但是你也可以使用每个 JUnit 断言语句的重载版本，它包含一个字符串，以便在断言失败时显示。

断言语句不是必须的；你可以在没有断言的情况下运行测试，**如果没有异常，则认为测试是成功的。**

**只要没有 @Test 注解，JUnit 就不会运行它，也不需要特定的签名。**

JUnit 还包括大量的测试结构，你可以到[官网](junit.org)上学习它们。

```java
// validating/tests/CountedListTest.java
// Simple use of JUnit to test CountedList.
package validating;
import java.util.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
public class CountedListTest {
private CountedList list;
	@BeforeAll
    static void beforeAllMsg() {
        System.out.println(">>> Starting CountedListTest");
    }
    
    @AfterAll
    static void afterAllMsg() {
        System.out.println(">>> Finished CountedListTest");
    }
    
    @BeforeEach
    public void initialize() {
    	list = new CountedList();
    	System.out.println("Set up for " + list.getId());
        for(int i = 0; i < 3; i++)
            list.add(Integer.toString(i));
    }
    
    @AfterEach
    public void cleanup() {
    	System.out.println("Cleaning up " + list.getId());
    }
    
    @Test
    public void insert() {
        System.out.println("Running testInsert()");
        assertEquals(list.size(), 3);
        list.add(1, "Insert");
        assertEquals(list.size(), 4);
        assertEquals(list.get(1), "Insert");
    }
    
    @Test
    public void replace() {
    	System.out.println("Running testReplace()");
    	assertEquals(list.size(), 3);
    	list.set(1, "Replace");
   		assertEquals(list.size(), 3);
    	assertEquals(list.get(1), "Replace");
    }
    	
    // A helper method to simplify the code. As
    // long as it's not annotated with @Test, it will
    // not be automatically executed by JUnit.
    private void compare(List<String> lst, String[] strs) {
        assertArrayEquals(lst.toArray(new String[0]), strs);
    }
}
```

#### 测试覆盖率的幻觉

测试覆盖率，同样也称为代码覆盖率，度量代码的测试百分比。百分比越高，测试的覆盖率越大。这里有很多[方法](https://en.wikipedia.org/wiki/Code_coverage)

计算覆盖率，还有有帮助的文章[Java代码覆盖工具](https://en.wikipedia.org/wiki/Java_Code_Coverage_Tools)。

对于没有知识但处于控制地位的人来说，很容易在没有任何了解的情况下也有概念认为 100% 的测试覆盖是唯一可接受的值。这有一个问题，因为 100% 并不意味着是对测试有效性的良好测量。你可以测试所有需要它的东西，但是只需要 65% 的覆盖率。如果需要 100% 的覆盖，你将浪费大量时间来生成剩余的代码，并且在向项目添加代码时浪费的时间更多。

当分析一个未知的代码库时，测试覆盖率作为一个粗略的度量是有用的。如果覆盖率工具报告的值特别低（比如，少于百分之40），则说明覆盖不够充分。然而，一个非常高的值也同样值得怀疑，这表明对编程领域了解不足的人迫使团队做出了武断的决定。覆盖工具的最佳用途是发现代码库中未测试的部分。但是，不要依赖覆盖率来得到测试质量的任何信息。

<!-- Preconditions -->

## 前置条件

前置条件的概念来自于契约式设计(**Design By Contract, DbC**), 利用断言机制实现。我们从 Java 的断言机制开始来介绍 DBC，最后使用谷歌的 Guava 库作为前置条件。

#### 断言（Assertions）

断言通过验证在程序执行期间满足某些条件，从而增加了程序的健壮性。

如果在方法的内部，则可以使用断言检查参数的有效性。这些是确保程序正确的重要测试，但是**它们不能在编译时被检查，并且它们不属于单元测试的范围。**

#### Java 断言语法

你可以通过其它程序设计架构来模拟断言的效果，因此，在 Java 中包含断言的意义在于它们易于编写。断言语句有两种形式 : 

```java
assert boolean-expression；

assert boolean-expression: information-expression;

```



两者似乎告诉我们 **“我断言这个布尔表达式会产生 true”**， 否则，将抛出 **AssertionError** 异常。

**AssertionError** 是 **Throwable** 的派生类，因此不需要异常说明。

不幸的是，第一种断言形式的异常不会生成包含布尔表达式的任何信息（与大多数其他语言的断言机制相反）。

下面是第一种形式的例子：

```java
// validating/Assert1.java

// Non-informative style of assert
// Must run using -ea flag:
// {java -ea Assert1}
// {ThrowsException}
public class Assert1 {
    public static void main(String[] args) {
        assert false;
    }
}

/* Output:
___[ Error Output ]___
Exception in thread "main" java.lang.AssertionError
at Assert1.main(Assert1.java:9)
*/
```

如果你正常运行程序，没有任何特殊的断言标志，则不会发生任何事情。你需要在运行程序时显式启用断言。一种简单的方法是使用 **-ea** 标志， 它也可以表示为: **-enableassertion**， 这将运行程序并执行任何断言语句。

输出中并没有包含多少有用的信息。另一方面，如果你使用 **information-expression** ， 将生成一条有用的消息作为异常堆栈跟踪的一部分。最有用的 **information-expression** 通常是一串针对程序员的文本：

```java
// validating/Assert2.java
// Assert with an information-expression
// {java Assert2 -ea}
// {ThrowsException}

public class Assert2 {
    public static void main(String[] args) {
    assert false:
    "Here's a message saying what happened";
    }
}
/* Output:
___[ Error Output ]___
Exception in thread "main" java.lang.AssertionError:
Here's a message saying what happened
at Assert2.main(Assert2.java:8)
*/
```

**information-expression** 可以产生任何类型的对象，因此，通常将构造一个包含对象值的更复杂的字符串，它包含失败的断言。

你还可以基于类名或包名打开或关闭断言；也就是说，你可以对整个包启用或禁用断言。实现这一点的详细信息在 JDK 的断言文档中。此特性对于使用断言的大型项目来说很有用当你想打开或关闭某些断言时。但是，日志记录（*Logging*）或者调试（*Debugging*）,可能是捕获这类信息的更好工具。

你还可以通过编程的方式通过链接到类加载器对象（**ClassLoader**）来控制断言。类加载器中有几种方法允许动态启用和禁用断言，其中 **setDefaultAssertionStatus ()** ,它为之后加载的所有类设置断言状态。因此，你可以像下面这样悄悄地开启断言：

```java
// validating/LoaderAssertions.java
// Using the class loader to enable assertions
// {ThrowsException}
public class LoaderAssertions {
public static void main(String[] args) {

	ClassLoader.getSystemClassLoader().
        setDefaultAssertionStatus(true);
		new Loaded().go();
	}
}

class Loaded {
    public void go() {
    assert false: "Loaded.go()";
    }
}
/* Output:
___[ Error Output ]___
Exception in thread "main" java.lang.AssertionError:
Loaded.go()
at Loaded.go(LoaderAssertions.java:15)
at
LoaderAssertions.main(LoaderAssertions.java:9)
*/

```

这消除了在运行程序时在命令行上使用 **-ea** 标志的需要，使用 **-ea** 标志启用断言可能同样简单。当交付独立产品时，可能必须设置一个执行脚本让用户能够启动程序，配置其他启动参数，这么做是有意义的。然而，决定在程序运行时启用断言可以使用下面的 **static** 块来实现这一点，该语句位于系统的主类中：

```java
static {
    boolean assertionsEnabled = false;
    // Note intentional side effect of assignment:
    assert assertionsEnabled = true;
    if(!assertionsEnabled)
        throw new RuntimeException("Assertions disabled");
}

```

如果启用断言，然后执行 **assert** 语句，**assertionsEnabled** 变为 **true** 。断言不会失败，因为分配的返回值是赋值的值。如果不启用断言，**assert** 语句不执行，**assertionsEnabled** 保持false，将导致异常。

#### Guava断言

因为启用 Java 本地断言很麻烦，Guava 团队添加一个始终启用的用来替换断言的 **Verify** 类。他们建议静态导入 **Verify** 方法：

```java
// validating/GuavaAssertions.java
// Assertions that are always enabled.

import com.google.common.base.*;
import static com.google.common.base.Verify.*;
public class GuavaAssertions {
    public static void main(String[] args) {
    	verify(2 + 2 == 4);
    	try {
    		verify(1 + 2 == 4);
   	 	} catch(VerifyException e) {
    		System.out.println(e);
    	}
        
		try {
			verify(1 + 2 == 4, "Bad math");
		} catch(VerifyException e) {
			System.out.println(e.getMessage());
		}
        
		try {
			verify(1 + 2 == 4, "Bad math: %s", "not 4");
		} catch(VerifyException e) {
        	System.out.println(e.getMessage());
        }
        
        String s = "";
        s = verifyNotNull(s);
        s = null;
        try {
            verifyNotNull(s);
        } catch(VerifyException e) {
        	System.out.println(e.getMessage());
        }
        
        try {
        	verifyNotNull(
        		s, "Shouldn't be null: %s", "arg s");
        } catch(VerifyException e) {
        	System.out.println(e.getMessage());
        }
	}
}
/* Output:
com.google.common.base.VerifyException
Bad math
Bad math: not 4
expected a non-null reference
Shouldn't be null: arg s
*/

```

这里有两个方法，使用变量 **verify()** 和 **verifyNotNull()** 来支持有用的错误消息。注意，**verifyNotNull()** 内置的错误消息通常就足够了，而 **verify()** 太一般，没有有用的默认错误消息。

#### 使用断言进行契约式设计

*契约式设计(DbC)*是 Eiffel 语言的发明者 Bertrand Meyer 提出的一个概念，通过确保对象遵循某些规则来帮助创建健壮的程序。这些规则是由正在解决的问题的性质决定的，这超出了编译器可以验证的范围。虽然断言没有直接实现 **DBC**（Eiffel 语言也是如此），但是它们创建了一种非正式的 DbC 编程风格。DbC 假定服务供应者与该服务的消费者或客户之间存在明确指定的契约。在面向对象编程中，服务通常由对象提供，对象的边界 — 供应者和消费者之间的划分 — 是对象类的接口。当客户端调用特定的公共方法时，它们希望该调用具有特定的行为：对象状态改变，以及一个可预测的返回值。

**Meyer** 认为：

1.应该明确指定行为，就好像它是一个契约一样。

2.通过实现某些运行时检查来保证这种行为，他将这些检查称为前置条件、后置条件和不变项。

不管你是否同意，第一条总是对的，在大多数情况下，DbC 确实是一种有用的方法。（我认为，与任何解决方案一样，它的有用性也有界限。但如果你知道这些界限，你就知道什么时候去尝试。）尤其是，设计过程中一个有价值的部分是特定类 DbC 约束的表达式；如果无法指定约束，则你可能对要构建的内容了解得不够。

#### 检查指令

详细研究 DbC 之前，思考最简单使用断言的办法，**Meyer** 称它为检查指令。检查指令说明你确信代码中的某个特定属性此时已经得到满足。检查指令的思想是在代码中表达非明显性的结论，而不仅仅是为了验证测试，也同样为了将来能够满足阅读者而有一个文档。

在化学领域，你也许会用一种纯液体去滴定测量另一种液体，当达到一个特定的点时，液体变蓝了。从两个液体的颜色上并不能明显看出；这是复杂反应的一部分。滴定完成后一个有用的检查指令是能够断定液体变蓝了。

检查指令是对你的代码进行补充，当你可以测试并阐明对象或程序的状态时，应该使用它。

#### 前置条件

前置条件确保客户端(调用此方法的代码)履行其部分契约。这意味着在方法调用开始时几乎总是会检查参数（在你用那个方法做任何操作之前）以此保证它们的调用在方法中是合适的。因为你永远无法知道客户端会传递给你什么，前置条件是确保检查的一个好做法。

#### 后置条件

后置条件测试你在方法中所做的操作的结果。这段代码放在方法调用的末尾，在 **return** 语句之前(如果有的话)。对于长时间、复杂的方法，在返回计算结果之前需要对计算结果进行验证（也就是说，在某些情况下，由于某种原因，你不能总是相信结果)，后置条件很重要，但是任何时候你可以描述方法结果上的约束时，最好将这些约束在代码中表示为后置条件。

#### 不变性

不变性保证了必须在方法调用之间维护的对象的状态。但是，它并不会阻止方法在执行过程中暂时偏离这些保证，它只是在说对象的状态信息应该总是遵守状态规则：

**1**. 在进入该方法时。

**2**.  在离开方法之前。

此外，不变性是构造后对于对象状态的保证。

根据这个描述，一个有效的不变性被定义为一个方法，可能被命名为 **invariant()** ，它在构造之后以及每个方法的开始和结束时调用。方法以如下方式调用：

assert invariant();

这样，如果出于性能原因禁用断言，就不会产生开销。

#### 放松 DbC 检查或非严格的 DbC

尽管 Meyer 强调了前置条件、后置条件和不变性的价值以及在开发过程中使用它们的重要性，他承认在一个产品中包含所有 DbC 代码并不总是实际的。你可以基于对特定位置的代码的信任程度放松 DbC 检查。以下是放松检查的顺序，最安全到最不安全：

**1**. **不变性检查**在每个方法一开始的时候是不能进行的，因为在每个方法结束的时候进行不变性检查能保证一开始的时候对象处于有效状态。也就是说，通常情况下，你可以相信对象的状态不会在方法调用之间发生变化。这是一个非常安全的假设，**你可以只在代码末尾使用不变性检查来编写代码。**

**2**. 接下来**禁用后置条件检查**，当你进行合理的单元测试以验证方法是否返回了适当的值时。因为不变性检查是观察对象的状态，后置条件检查仅在方法期间验证计算结果，因此可能会被丢弃，以便进行单元测试。单元测试不会像运行时后置条件检查那样安全，但是它可能已经足够了，特别是当对自己的代码有信心时。

**3**. 如果你确信方法主体没有把对象改成无效状态，则可以禁用方法调用末尾的不变性检查。可以通过白盒单元测试(通过访问私有字段的单元测试来验证对象状态)来验证这一点。尽管它可能没有调用 **invariant()** 那么稳妥，可以将不变性检查从运行时测试 “迁移” 到构建时测试(通过单元测试)，就像使用后置条件一样。

**4**. 禁用前置条件检查，但除非这是万不得已的情况下。因为这是最不安全、最不明智的选择，因为尽管你知道并且可以控制自己的代码，但是你无法控制客户端可能会传递给方法的参数。然而，某些情况下对性能要求很高，通过分析得到前置条件造成了这个瓶颈，而且你有某种合理的保证客户端不会违反前置条件(比如自己编写客户端的情况下)，那么禁用前置条件检查是可接受的。

你不应该直接删除检查的代码，而只需要禁用检查(添加注释)。这样如果发现错误，就可以轻松地恢复检查以快速发现问题。

#### DbC + 单元测试

下面的例子演示了将契约式设计中的概念与单元测试相结合的有效性。它显示了一个简单的先进先出(FIFO)队列，该队列实现为一个“循环”数组，即以循环方式使用的数组。当到达数组的末尾时，将绕回到开头。

我们可以对这个队列做一些契约定义:

**1**.   前置条件(用于put())：不允许将空元素添加到队列中。

**2**.   前置条件(用于put())：将元素放入完整队列是非法的。

**3**.   前置条件(用于get())：试图从空队列中获取元素是非法的。

**4**.   后置条件用于get())：不能从数组中生成空元素。

**5**.   不变性：包含对象的区域不能包含任何空元素。

**6**.   不变性：不包含对象的区域必须只有空值。

下面是实现这些规则的一种方式，为每个 DbC 元素类型使用显式的方法调用。

首先，我们创建一个专用的 **Exception**：

```java
  // validating/CircularQueueException.java
  package validating;
  public class CircularQueueException extends RuntimeException {
          public CircularQueueException(String why) {
          super(why);
      }
  }

```

它用来报告 **CircularQueue** 中出现的错误：

```java
  // validating/CircularQueue.java
  // Demonstration of Design by Contract (DbC)
  package validating;
  import java.util.*;
  public class CircularQueue {
      private Object[] data;
      private int in = 0, // Next available storage space 
      out = 0; // Next gettable object
               // Has it wrapped around the circular queue?
      private boolean wrapped = false;
      public CircularQueue(int size) {
          data = new Object[size];
          // Must be true after construction:
          assert invariant();
      }
      
      public boolean empty() {
          return !wrapped && in == out;
      }
      
      public boolean full() {
      	  return wrapped && in == out;
      }
      
  	  public boolean isWrapped() { return wrapped; }
      
      public void put(Object item) {
      	  precondition(item != null, "put() null item");
      	  precondition(!full(),
      	  "put() into full CircularQueue");
      	  assert invariant();
      	  data[in++] = item;
      	  if(in >= data.length) {
              in = 0;
              wrapped = true;
      	  }
  		  assert invariant();
  	  }
      
      public Object get() {
      	  precondition(!empty(),
      	  "get() from empty CircularQueue");
      	  assert invariant();
      	  Object returnVal = data[out];
      	  data[out] = null;
      	  out++;
          if(out >= data.length) {
              out = 0;
              wrapped = false;
          }
          assert postcondition(
          returnVal != null,
          "Null item in CircularQueue");
          assert invariant();
          return returnVal;
      }
      
  	  // Design-by-contract support methods:
      private static void precondition(boolean cond, String msg) {
          if(!cond) throw new CircularQueueException(msg);
      }
      
      private static boolean postcondition(boolean cond, String msg) {
          if(!cond) throw new CircularQueueException(msg);
      	  return true;
      }
      
      private boolean invariant() {
          // Guarantee that no null values are in the
          // region of 'data' that holds objects:
          for(int i = out; i != in; i = (i + 1) % data.length)
              if(data[i] == null)
                  throw new CircularQueueException("null in CircularQueue");
                  // Guarantee that only null values are outside the
                  // region of 'data' that holds objects:
          if(full()) return true;
          for(int i = in; i != out; i = (i + 1) % data.length)
               if(data[i] != null)
                   throw new CircularQueueException(
                        "non-null outside of CircularQueue range: " + dump());
          return true;
      }
      
      public String dump() {
          return "in = " + in +
              ", out = " + out +
              ", full() = " + full() +
              ", empty() = " + empty() +
              ", CircularQueue = " + Arrays.asList(data);
      }
  }

```

**in** 计数器指示数组中下一个对象所在的位置。**out** 计数器指示下一个对象来自何处。**wrapped** 的flag表示 **in** 已经“绕着圆圈”走了，现在从后面出来了。当**in**和 **out** 重合时，队列为空(如果包装为 **false** )或满(如果 **wrapped** 为 **true** )。

**put()** 和 **get()** 方法调用 **precondition()** ，**postcondition()**, 和 **invariant**()，这些都是在类中定义的私有方法。前置**precondition()** 和 **postcondition()** 是用来阐明代码的辅助方法。

注意，**precondition()** 返回 **void** , 因为它不与断言一起使用。按照之前所说的，通常你会在代码中保留前置条件。通过将它们封装在 **precondition()**  方法调用中，如果你不得不做出关掉它们的可怕举动，你会有更好的选择。

**postcondition()** 和 **constant()** 都返回一个布尔值，因此可以在 **assert** 语句中使用它们。此外，如果出于性能考虑禁用断言，则根本不存在方法调用。**invariant()** 对对象执行内部有效性检查，如果你在每个方法调用的开始和结束都这样做，这是一个花销巨大的操作，就像 **Meyer** 建议的那样。所以， 用代码清晰地表明是有帮助的，它帮助我调试了实现。此外，如果你对代码实现做任何更改，那么 **invariant()** 将确保你没有破坏代码，将不变性测试从方法调用移到单元测试代码中是相当简单的。如果你的单元测试是足够的，那么你应当对不变性保持一定的信心。

**dump()** 帮助方法返回一个包含所有数据的字符串，而不是直接打印数据。这允许我们用这部分信息做更多事。  

现在我们可以为类创建 JUnit 测试:

```java
  // validating/tests/CircularQueueTest.java
  package validating;
  import org.junit.jupiter.api.*;
  import static org.junit.jupiter.api.Assertions.*;
  public class CircularQueueTest {
      private CircularQueue queue = new CircularQueue(10);
      private int i = 0;
      
      @BeforeEach
      public void initialize() {
          while(i < 5) // Pre-load with some data
              queue.put(Integer.toString(i++));
  	  }
      
      // Support methods:
      private void showFullness() {
          assertTrue(queue.full());
          assertFalse(queue.empty());
          System.out.println(queue.dump());
      }
      
      private void showEmptiness() {
          assertFalse(queue.full());
          assertTrue(queue.empty());
          System.out.println(queue.dump());
      }
      
      @Test
      public void full() {
          System.out.println("testFull");
          System.out.println(queue.dump());
          System.out.println(queue.get());
          System.out.println(queue.get());
          while(!queue.full())
              queue.put(Integer.toString(i++));
              String msg = "";
          try {
          	  queue.put("");
          } catch(CircularQueueException e) {
          	  msg = e.getMessage();
          	  ∂System.out.println(msg);
          }
          assertEquals(msg, "put() into full CircularQueue");
          showFullness();
      }
      
      @Test
      public void empty() {
          System.out.println("testEmpty");
          while(!queue.empty())
      		  System.out.println(queue.get());
      		  String msg = "";
          try {
              queue.get();
          } catch(CircularQueueException e) {
              msg = e.getMessage();
              System.out.println(msg);
          }
          assertEquals(msg, "get() from empty CircularQueue");
          showEmptiness();
      }
      @Test
      public void nullPut() {
          System.out.println("testNullPut");
          String msg = "";
          try {
          	  queue.put(null);
          } catch(CircularQueueException e) {
              msg = e.getMessage();
              System.out.println(msg);
          }
          assertEquals(msg, "put() null item");
      }
      
      @Test
      public void circularity() {
      	  System.out.println("testCircularity");
      	  while(!queue.full())
      		  queue.put(Integer.toString(i++));
      		  showFullness();
      		  assertTrue(queue.isWrapped());
          
          while(!queue.empty())
          	  System.out.println(queue.get());
          	  showEmptiness();
          
          while(!queue.full())
          	  queue.put(Integer.toString(i++));
          	  showFullness();
          
          while(!queue.empty())
          	  System.out.println(queue.get());
          	  showEmptiness();
       }
   }
  /* Output:
  testNullPut
  put() null item
  testCircularity
  in = 0, out = 0, full() = true, empty() = false,
  CircularQueue =
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  0
  1
  2
  3
  4
  5
  6
  7
  8
  9
  in = 0, out = 0, full() = false, empty() = true,
  CircularQueue =
  [null, null, null, null, null, null, null, null, null,
  null]
  in = 0, out = 0, full() = true, empty() = false,
  CircularQueue =
  [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
  10
  11
  12
  13
  14
  15
  16
  17
  18
  19
  in = 0, out = 0, full() = false, empty() = true,
  CircularQueue =
  [null, null, null, null, null, null, null, null, null,
  null]
  testFull
  in = 5, out = 0, full() = false, empty() = false,
  CircularQueue =
  [0, 1, 2, 3, 4, null, null, null, null, null]
  0
  1
  put() into full CircularQueue
  in = 2, out = 2, full() = true, empty() = false,
  CircularQueue =
  [10, 11, 2, 3, 4, 5, 6, 7, 8, 9]
  testEmpty
  0
  1
  2
  3
  4
  get() from empty CircularQueue
  in = 5, out = 5, full() = false, empty() = true,
  CircularQueue =
  [null, null, null, null, null, null, null, null, null,
  null]
  */

```

**initialize()** 添加了一些数据，因此每个测试的 **CircularQueue** 都是部分满的。**showFullness()** 和 **showempty()** 表明 **CircularQueue** 是满的还是空的，这四种测试方法中的每一种都确保了 **CircularQueue** 功能在不同的地方正确运行。

通过将 Dbc 和单元测试结合起来，你不仅可以同时使用这两种方法，还可以有一个迁移路径—你可以将一些 Dbc 测试迁移到单元测试中，而不是简单地禁用它们，这样你仍然有一定程度的测试。

#### 使用Guava前置条件

在非严格的 DbC 中，前置条件是 DbC 中你不想删除的那一部分，因为它可以检查方法参数的有效性。那是你没有办法控制的事情，所以你需要对其检查。因为 Java 在默认情况下禁用断言，所以通常最好使用另外一个始终验证方法参数的库。

谷歌的 Guava 库包含了一组很好的前置条件测试，这些测试不仅易于使用，而且命名也足够好。在这里你可以看到它们的简单用法。库的设计人员建议静态导入前置条件:

```java
// validating/GuavaPreconditions.java
// Demonstrating Guava Preconditions
import java.util.function.*;
import static com.google.common.base.Preconditions.*;
public class GuavaPreconditions {
    static void test(Consumer<String> c, String s) {
        try {
            System.out.println(s);
            c.accept(s);
            System.out.println("Success");
        } catch(Exception e) {
            String type = e.getClass().getSimpleName();
            String msg = e.getMessage();
            System.out.println(type +
            (msg == null ? "" : ": " + msg));
        }
    }
    
    public static void main(String[] args) {
        test(s -> s = checkNotNull(s), "X");
        test(s -> s = checkNotNull(s), null);
        test(s -> s = checkNotNull(s, "s was null"), null);
        test(s -> s = checkNotNull(
        s, "s was null, %s %s", "arg2", "arg3"), null);
        test(s -> checkArgument(s == "Fozzie"), "Fozzie");
        test(s -> checkArgument(s == "Fozzie"), "X");
        test(s -> checkArgument(s == "Fozzie"), null);
        test(s -> checkArgument(
        s == "Fozzie", "Bear Left!"), null);
        test(s -> checkArgument(
        s == "Fozzie", "Bear Left! %s Right!", "Frog"),
        null);
        test(s -> checkState(s.length() > 6), "Mortimer");
        test(s -> checkState(s.length() > 6), "Mort");
        test(s -> checkState(s.length() > 6), null);
        test(s ->
        checkElementIndex(6, s.length()), "Robert");
        test(s ->
        checkElementIndex(6, s.length()), "Bob");
        test(s ->
        checkElementIndex(6, s.length()), null);
        test(s ->
        checkPositionIndex(6, s.length()), "Robert");
        test(s ->
        checkPositionIndex(6, s.length()), "Bob");
        test(s ->
        checkPositionIndex(6, s.length()), null);
        test(s -> checkPositionIndexes(
        0, 6, s.length()), "Hieronymus");
        test(s -> checkPositionIndexes(
        0, 10, s.length()), "Hieronymus");
        test(s -> checkPositionIndexes(
        0, 11, s.length()), "Hieronymus");
        test(s -> checkPositionIndexes(
        -1, 6, s.length()), "Hieronymus");
        test(s -> checkPositionIndexes(
        7, 6, s.length()), "Hieronymus");
        test(s -> checkPositionIndexes(
        0, 6, s.length()), null);
    }
}
/* Output:
X
Success
null
NullPointerException
null
NullPointerException: s was null
null
NullPointerException: s was null, arg2 arg3
Fozzie
Success
X
IllegalArgumentException
null
IllegalArgumentException
null
IllegalArgumentException: Bear Left!
null
IllegalArgumentException: Bear Left! Frog Right!
Mortimer
Success
Mort
IllegalStateException
null
NullPointerException
Robert
IndexOutOfBoundsException: index (6) must be less than
size (6)
Bob
IndexOutOfBoundsException: index (6) must be less than
size (3)
null
NullPointerException
Robert
Success
Bob
IndexOutOfBoundsException: index (6) must not be
greater than size (3)
null
NullPointerException
Hieronymus
Success
Hieronymus
Success
Hieronymus
IndexOutOfBoundsException: end index (11) must not be
greater than size (10)
Hieronymus
IndexOutOfBoundsException: start index (-1) must not be
negative
Hieronymus
IndexOutOfBoundsException: end index (6) must not be	
less than start index (7)
null
NullPointerException
*/

```

虽然 Guava 的前置条件适用于所有类型，但我这里只演示 **字符串（String）** 类型。**test()** 方法需要一个Consumer`<String>`，因此我们可以传递一个 lambda 表达式作为第一个参数，传递给 lambda 表达式的字符串作为第二个参数。它显示字符串，以便在查看输出时确定方向，然后将字符串传递给 lambda 表达式。try 块中的第二个 **println**() 仅在 lambda 表达式成功时才显示; 否则 catch 块将捕获并显示错误信息。注意 **test()** 方法消除了多少重复的代码。

每个前置条件都有三种不同的重载形式：一个什么都没有，一个带有简单字符串消息，以及带有一个字符串和替换值。为了提高效率，只允许 **%s** (字符串类型)替换标记。在上面的例子中，演示了**checkNotNull()** 和 **checkArgument()** 这两种形式。但是它们对于所有前置条件方法都是相同的。注意 **checkNotNull()** 的返回参数， 所以你可以在表达式中内联使用它。下面是如何在构造函数中使用它来防止包含 **Null** 值的对象构造：

```java
/ validating/NonNullConstruction.java
import static com.google.common.base.Preconditions.*;
public class NonNullConstruction {
    private Integer n;
    private String s;
    NonNullConstruction(Integer n, String s) {
        this.n = checkNotNull(n);	
        this.s = checkNotNull(s);
    }
    public static void main(String[] args) {
        NonNullConstruction nnc =
        new NonNullConstruction(3, "Trousers");
    }
}

```

**checkArgument()** 接受布尔表达式来对参数进行更具体的测试， 失败时抛出  **IllegalArgumentException**，**checkState()** 用于测试对象的状态（例如，不变性检查），而不是检查参数，并在失败时抛出 **IllegalStateException** 。

最后三个方法在失败时抛出 **IndexOutOfBoundsException**。**checkElementIndex**() 确保其第一个参数是列表、字符串或数组的有效元素索引，其大小由第二个参数指定。**checkPositionIndex()** 确保它的第一个参数在 0 到第二个参数(包括第二个参数)的范围内。 **checkPositionIndexes()**  检查 **[first_arg, second_arg]** 是一个列表的有效子列表，由第三个参数指定大小的字符串或数组。

所有的 Guava 前置条件对于基本类型和对象都有必要的重载。

<!-- Test-Driven Development -->

## 测试驱动开发

之所以可以有测试驱动开发（TDD）这种开发方式，是因为如果你在设计和编写代码时考虑到了测试，那么你不仅可以写出可测试性更好的代码，而且还可以得到更好的代码设计。 一般情况下这个说法都是正确的。 一旦我想到“我将如何测试我的代码？”，这个想法将使我的代码产生变化，并且往往是从“可测试”转变为“可用”。

纯粹的 TDD 主义者会在实现新功能之前就为其编写测试，这称为测试优先的开发。 我们采用一个简易的示例程序来进行说明，它的功能是反转 **String** 中字符的大小写。 让我们随意添加一些约束：**String** 必须小于或等于30个字符，并且必须只包含字母，空格，逗号和句号(英文)。

此示例与标准 TDD 不同，因为它的作用在于接收 **StringInverter** 的不同实现，以便在我们逐步满足测试的过程中来体现类的演变。 为了满足这个要求，将 **StringInverter** 作为接口：

```java
// validating/StringInverter.java
package validating;

interface StringInverter {
	String invert(String str);
}

```

现在我们通过可以编写测试来表述我们的要求。 以下所述通常不是你编写测试的方式，但由于我们在此处有一个特殊的约束：我们要对 **StringInverter **多个版本的实现进行测试，为此，我们利用了 JUnit5 中最复杂的新功能之一：动态测试生成。 顾名思义，通过它你可以使你所编写的代码在运行时生成测试，而不需要你对每个测试显式编码。 这带来了许多新的可能性，特别是在明确地需要编写一整套测试而令人望而却步的情况下。

JUnit5 提供了几种动态生成测试的方法，但这里使用的方法可能是最复杂的。  **DynamicTest.stream() **方法采用了：

- 对象集合上的迭代器 (versions) ，这个迭代器在不同组的测试中是不同的。 迭代器生成的对象可以是任何类型，但是只能有一种对象生成，因此对于存在多个不同的对象类型时，必须人为地将它们打包成单个类型。
- **Function**，它从迭代器获取对象并生成描述测试的 **String** 。
- **Consumer**，它从迭代器获取对象并包含基于该对象的测试代码。

在此示例中，所有代码将在 **testVersions()**  中进行组合以防止代码重复。 迭代器生成的对象是对 **DynamicTest** 的不同实现，这些对象体现了对接口不同版本的实现：

```java
// validating/tests/DynamicStringInverterTests.java
package validating;
import java.util.*;
import java.util.function.*;
import java.util.stream.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.DynamicTest.*;

class DynamicStringInverterTests {
	// Combine operations to prevent code duplication:
	Stream<DynamicTest> testVersions(String id,
		Function<StringInverter, String> test) {
		List<StringInverter> versions = Arrays.asList(
			new Inverter1(), new Inverter2(),
			new Inverter3(), new Inverter4());
		return DynamicTest.stream(
			versions.iterator(),
			inverter -> inverter.getClass().getSimpleName(),
			inverter -> {
				System.out.println(
					inverter.getClass().getSimpleName() +
						": " + id);
				try {
					if(test.apply(inverter) != "fail")
						System.out.println("Success");
				} catch(Exception | Error e) {
					System.out.println(
						"Exception: " + e.getMessage());
				}
			}
		);
	}
    String isEqual(String lval, String rval) {
		if(lval.equals(rval))
			return "success";
		System.out.println("FAIL: " + lval + " != " + rval);
		return "fail";
	}
    @BeforeAll
	static void startMsg() {
		System.out.println(
			">>> Starting DynamicStringInverterTests <<<");
	}
    @AfterAll
	static void endMsg() {
		System.out.println(
			">>> Finished DynamicStringInverterTests <<<");
	}
	@TestFactory
	Stream<DynamicTest> basicInversion1() {
		String in = "Exit, Pursued by a Bear.";
		String out = "eXIT, pURSUED BY A bEAR.";
		return testVersions(
			"Basic inversion (should succeed)",
			inverter -> isEqual(inverter.invert(in), out)
		);
	}
	@TestFactory
	Stream<DynamicTest> basicInversion2() {
		return testVersions(
			"Basic inversion (should fail)",
			inverter -> isEqual(inverter.invert("X"), "X"));
	}
	@TestFactory
	Stream<DynamicTest> disallowedCharacters() {
		String disallowed = ";-_()*&^%$#@!~`0123456789";
		return testVersions(
			"Disallowed characters",
			inverter -> {
				String result = disallowed.chars()
					.mapToObj(c -> {
						String cc = Character.toString((char)c);
						try {
							inverter.invert(cc);
							return "";
						} catch(RuntimeException e) {
							return cc;
						}
					}).collect(Collectors.joining(""));
				if(result.length() == 0)
					return "success";
				System.out.println("Bad characters: " + result);
				return "fail";
			}
		);
	}
    @TestFactory
	Stream<DynamicTest> allowedCharacters() {
		String lowcase = "abcdefghijklmnopqrstuvwxyz ,.";
		String upcase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ,.";
		return testVersions(
			"Allowed characters (should succeed)",
            inverter -> {
				assertEquals(inverter.invert(lowcase), upcase);
				assertEquals(inverter.invert(upcase), lowcase);
				return "success";
			}
		);
	}
	@TestFactory
	Stream<DynamicTest> lengthNoGreaterThan30() {
		String str = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
		assertTrue(str.length() > 30);
		return testVersions(
			"Length must be less than 31 (throws exception)",
			inverter -> inverter.invert(str)
		);
	}
	@TestFactory
	Stream<DynamicTest> lengthLessThan31() {
		String str = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
		assertTrue(str.length() < 31);
		return testVersions(
			"Length must be less than 31 (should succeed)",
			inverter -> inverter.invert(str)
		);
	}
}
```

在一般的测试中，你可能认为在进行一个结果为失败的测试时应该停止代码构建。 但是在这里，我们只希望系统报告问题，但仍然继续运行，以便你可以看到不同版本的 **StringInverter** 的效果。

每个使用 **@TestFactory** 注释的方法都会生成一个 **DynamicTest** 对象的 **Stream**（通过 **testVersions()** ），每个 JUnit 都像常规的 **@Test** 方法一样执行。

现在测试都已经准备好了，我们就可以开始实现 **StringInverter **了。 我们从一个仅返回其参数的假的实现类开始：

```java
// validating/Inverter1.java
package validating;
public class Inverter1 implements StringInverter {
	public String invert(String str) { return str; }
}

```

接下来我们实现反转操作：

```java
// validating/Inverter2.java
package validating;
import static java.lang.Character.*;
public class Inverter2 implements StringInverter {
	public String invert(String str) {
		String result = "";
		for(int i = 0; i < str.length(); i++) {
			char c = str.charAt(i);
			result += isUpperCase(c) ?
					  toLowerCase(c) :
					  toUpperCase(c);
		}
		return result;
	}
}

```

现在添加代码以确保输入不超过30个字符：

```java
// validating/Inverter3.java
package validating;
import static java.lang.Character.*;
public class Inverter3 implements StringInverter {
	public String invert(String str) {
		if(str.length() > 30)
			throw new RuntimeException("argument too long!");
		String result = "";
		for(int i = 0; i < str.length(); i++) {
			char c = str.charAt(i);
			result += isUpperCase(c) ?
					  toLowerCase(c) :
					  toUpperCase(c);
        }
		return result;
	}
}

```

最后，我们排除了不允许的字符：

```java
// validating/Inverter4.java
package validating;
import static java.lang.Character.*;
public class Inverter4 implements StringInverter {
	static final String ALLOWED =
		"abcdefghijklmnopqrstuvwxyz ,." +
		"ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	public String invert(String str) {
		if(str.length() > 30)
			throw new RuntimeException("argument too long!");
		String result = "";
		for(int i = 0; i < str.length(); i++) {
			char c = str.charAt(i);
			if(ALLOWED.indexOf(c) == -1)
				throw new RuntimeException(c + " Not allowed");
			result += isUpperCase(c) ?
					  toLowerCase(c) :
					  toUpperCase(c);
		}
		return result;
	}
}

```

你将从测试输出中看到，每个版本的 **Inverter** 都几乎能通过所有测试。 当你在进行测试优先的开发时会有相同的体验。

**DynamicStringInverterTests.java** 仅是为了显示 TDD 过程中不同 **StringInverter** 实现的开发。 通常，你只需编写一组如下所示的测试，并修改单个 **StringInverter** 类直到它满足所有测试：

```java
// validating/tests/StringInverterTests.java
package validating;
import java.util.*;
import java.util.stream.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class StringInverterTests {
	StringInverter inverter = new Inverter4();
	@BeforeAll
	static void startMsg() {
		System.out.println(">>> StringInverterTests <<<");
	}
    @Test
	void basicInversion1() {
		String in = "Exit, Pursued by a Bear.";
		String out = "eXIT, pURSUED BY A bEAR.";
		assertEquals(inverter.invert(in), out);
	}
	@Test
	void basicInversion2() {
		expectThrows(Error.class, () -> {
			assertEquals(inverter.invert("X"), "X");
		});
	}
	@Test
	void disallowedCharacters() {
		String disallowed = ";-_()*&^%$#@!~`0123456789";
		String result = disallowed.chars()
			.mapToObj(c -> {
				String cc = Character.toString((char)c);
				try {
					inverter.invert(cc);
					return "";
				} catch(RuntimeException e) {
					return cc;
				}
			}).collect(Collectors.joining(""));
		assertEquals(result, disallowed);
	}
	@Test
	void allowedCharacters() {
		String lowcase = "abcdefghijklmnopqrstuvwxyz ,.";
		String upcase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ,.";
		assertEquals(inverter.invert(lowcase), upcase);
		assertEquals(inverter.invert(upcase), lowcase);
	}
	@Test
	void lengthNoGreaterThan30() {
		String str = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
		assertTrue(str.length() > 30);
		expectThrows(RuntimeException.class, () -> {
			inverter.invert(str);
		});
	}
    @Test
	void lengthLessThan31() {
		String str = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
		assertTrue(str.length() < 31);
		inverter.invert(str);
	}
}

```

你可以通过这种方式进行开发：一开始在测试中建立你期望程序应有的所有特性，然后你就能在实现中一步步添加功能，直到所有测试通过。 完成后，你还可以在将来通过这些测试来得知（或让其他任何人得知）当修复错误或添加功能时，代码是否被破坏了。 TDD的目标是产生更好，更周全的测试，因为在完全实现之后尝试实现完整的测试覆盖通常会产生匆忙或无意义的测试。

### 测试驱动 vs. 测试优先

虽然我自己还没有达到测试优先的意识水平，但我最感兴趣的是来自测试优先中的“测试失败的书签”这一概念。 当你离开你的工作一段时间后，重新回到工作进展中，甚至找到你离开时工作到的地方有时会很有挑战性。 然而，以失败的测试为书签能让你找到之前停止的地方。 这似乎让你能更轻松地暂时离开你的工作，因为不用担心找不到工作进展的位置。

纯粹的测试优先编程的主要问题是它假设你事先了解了你正在解决的问题。 根据我自己的经验，我通常是从实验开始，而只有当我处理问题一段时间后，我对它的理解才会达到能给它编写测试的程度。 当然，偶尔会有一些问题在你开始之前就已经完全定义，但我个人并不常遇到这些问题。 实际上，可能用“*面向测试的开发* ( *Test-Oriented Development* )”这个短语来描述编写测试良好的代码或许更好。

<!-- Logging -->

## 日志

> 日志会给出正在运行的程序的各种信息。

在调试程序中，日志可以是普通状态数据，用于显示程序运行过程（例如，安装程序可能会记录安装过程中采取的步骤，存储文件的目录，程序的启动值等）。

在调试期间，日志也能带来好处。 如果没有日志，你可能会尝试通过插入 **println()** 语句来打印出程序的行为。 但是，一旦你确定程序正常运行，你可能会将 **println()** 语句注释或者删除。 

程序员在日志包可供使用之前，都只能依赖 Java 编译器移除未调用的代码。 如果 **debug** 是一个 **static final boolean **，你就可以这么写：

```java
if(debug) {
	System.out.println("Debug info");
}

```

然后，当 **debug **为 **false **时，编译器将移除大括号内的代码。 

### SLF4J

业内普遍认为标准 Java 发行版本中的日志包 **(java.util.logging)** 的设计相当糟糕。 大多数人会选择其他的替代日志包。**如 *Simple Logging Facade for Java(SLF4J)* ,它为多个日志框架提供了一个封装好的调用方式**，这些日志框架包括 **java.util.logging** ， **logback** 和 **log4j **。 SLF4J 允许用户在部署时插入所需的日志框架。

SLF4J 提供了一个复杂的工具来报告程序的信息，它的效率与前面示例中的技术几乎相同。 对于非常简单的信息日志记录，你可以执行以下操作：

```java
// validating/SLF4JLogging.java
import org.slf4j.*;
public class SLF4JLogging {
	private static Logger log =
		LoggerFactory.getLogger(SLF4JLogging.class);
	public static void main(String[] args) {
		log.info("hello logging");
	}
}
/* Output:
2017-05-09T06:07:53.418
[main] INFO SLF4JLogging - hello logging
*/

```

日志输出中的格式和信息，甚至输出是否正常或“错误”都取决于 SLF4J 所连接的后端程序包是怎样实现的。 在上面的示例中，它连接到的是 **logback** 库（通过本书的 **build.gradle** 文件），并显示为标准输出。

如果我们修改 **build.gradle** 从而使用内置在 JDK 中的日志包作为后端，则输出显示为错误输出，如下所示：

**Aug 16, 2016 5:40:31 PM InfoLogging main**
**INFO: hello logging**

日志系统会检测日志消息处所在的的类名和方法名。 但它不能保证这些名称是正确的，所以不要纠结于其准确性。

### 日志等级

SLF4J 提供了多个等级的日志消息。下面这个例子以“严重性”的递增顺序对它们作出演示：

```java
// validating/SLF4JLevels.java
import org.slf4j.*;
public class SLF4JLevels {
	private static Logger log =
		LoggerFactory.getLogger(SLF4JLevels.class);
	public static void main(String[] args) {
		log.trace("Hello");
		log.debug("Logging");
		log.info("Using");
		log.warn("the SLF4J");
		log.error("Facade");
	}
}
/* Output:
2017-05-09T06:07:52.846
[main] TRACE SLF4JLevels - Hello
2017-05-09T06:07:52.849
[main] DEBUG SLF4JLevels - Logging
2017-05-09T06:07:52.849
[main] INFO SLF4JLevels - Using
2017-05-09T06:07:52.850
[main] WARN SLF4JLevels - the SLF4J
2017-05-09T06:07:52.851
[main] ERROR SLF4JLevels - Facade
*/

```

你可以按等级来查找消息。 级别通常设置在单独的配置文件中，因此你可以重新配置而无需重新编译。 配置文件格式取决于你使用的后端日志包实现。 如 **logback** 使用 XML ：

```xml
<!-- validating/logback.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
	<appender name="STDOUT"
		class="ch.qos.logback.core.ConsoleAppender">
		<encoder>
			<pattern>
%d{yyyy-MM-dd'T'HH:mm:ss.SSS}
[%thread] %-5level %logger - %msg%n
			</pattern>
		</encoder>
	</appender>
	<root level="TRACE">
		<appender-ref ref="STDOUT" />
	</root>
</configuration>

```

你可以尝试将 **<root level =“TRACE"> **行更改为其他级别，然后重新运行该程序查看日志输出的更改情况。 如果你没有写 **logback.xml** 文件，日志系统将采取默认配置。

这只是 SLF4J 最简单的介绍和一般的日志消息，但也足以作为使用日志的基础 - 你可以沿着这个进行更长久的学习和实践。你可以查阅 [SLF4J 文档](http://www.slf4j.org/manual.html)来获得更深入的信息。

<!-- Debugging -->

## 调试

使用调试器，可以展示任何时刻的程序状态，查看变量的值，一步一步运行程序，连接远程运行的程序等等。特别是当你构建较大规模的系统（bug 容易被掩埋）时，熟练使用调试器是值得的。

### 使用 JDB 调试

Java 调试器（JDB）是 JDK 内置的命令行工具。从调试的指令和命令行接口两方面看的话，JDB 至少从概念上是 GNU 调试器（GDB，受 Unix DB 的影响）的继承者。JDB 对于学习调试和执行简单的调试任务来说是有用的，而且知道只要安装了 JDK 就可以使用 JDB 是有帮助的。然而，对于大型项目来说，你可能想要一个图形化的调试器，这在后面会描述。

假设你写了如下程序：

```java
// validating/SimpleDebugging.java
// {ThrowsException}
public class SimpleDebugging {
    private static void foo1() {
        System.out.println("In foo1");
        foo2();
    }
    
    private static void foo2() {
        System.out.println("In foo2");
        foo3();
    }
    
    private static void foo3() {
        System.out.println("In foo3");
        int j = 1;
        j--;
        int i = 5 / j;
    }
    
    public static void main(String[] args) {
        foo1();
    }
}
/* Output
In foo1
In foo2
In foo3
__[Error Output]__
Exception in thread "main"
java.lang.ArithmeticException: /by zero 
at 
SimpleDebugging.foo3(SimpleDebugging.java:17)
at 
SimpleDebugging.foo2(SimpleDebugging.java:11)
at
SimpleDebugging.foo1(SimpleDebugging.java:7)
at
SimpleDebugging.main(SimpleDebugging.java:20)

```

首先看方法 `foo3()`，问题很明显：除数是 0。但是假如这段代码被埋没在大型程序中（像这里的调用序列暗示的那样）而且你不知道从哪儿开始查找问题。结果呢，异常会给出足够的信息让你定位问题。然而，假设事情更加复杂，你必须更加深入程序中来获得比异常提供的更多的信息。

为了运行 JDB，你需要在编译 **SimpleDebugging.java** 时加上 **-g** 标记，从而告诉编译器生成编译信息。然后使用如下命令开始调试程序：

```shell
javac -g .\SimpleDebugging.java

```

**jdb SimpleDebugging**

接着 JDB 就会运行，出现命令行提示。你可以输入 **?** 查看可用的 JDB 命令。

这里展示了如何使用交互式追踪一个问题的调试历程：

```shell
Initializing jdb...

> catch Exception

```

`>` 表明 JDB 在等待输入命令。命令 **catch Exception** 在任何抛出异常的地方设置断点（然而，即使你不显式地设置断点，调试器也会停止— JDB 中好像是默认在异常抛出处设置了异常）。接着命令行会给出如下响应：

**Deferring exception catch Exception.**

**It will be set after the class is loaded.**

继续输入：

**> run**

现在程序将运行到下个断点处，在这个例子中就是异常发生的地方。下面是运行 **run** 命令的结果：

**run SimpleDebugging**

**Set uncaught java.lang.Throwable**

**Set deferred uncaught java.lang.Throwable**

**>**

**VM Started: In foo1**

**In foo2**

**In foo3**

**Exception occurred: java.lang.ArithmeticException**

**(uncaught)"thread=main",**

**SimpleDebugging.foo3(),line=16 bci=15**

**16 int i = 5 / j**

程序运行到第16行时发生异常，但是 JDB 在异常发生时就不复存在。调试器还展示了是哪一行导致了异常。你可以使用 **list** 将导致程序终止的执行点列出来：

**main[1] list**

**12 private static void foo3() {**

**13 System.out.println("In foo3");**

**14 int j = 1;**

**15 j--;**

**16 => int i = 5 / j;**

**17 }**

**18 public static void main(String[] args) {**

**19 foo1();**

**20 }**

**21 }**

**/* Output:**

上述 `=>` 展示了程序将继续运行的执行点。你可以使用命令 **cont**(continue) 继续运行，但是会导致 JDB 在异常发生时退出并打印出栈轨迹信息。

命令 **locals** 能转储所有的局部变量值：

**main[1] locals**

**Method arguments:**

**Local variables:**

**j = 0**

命令 **wherei** 打印进入当前线程的方法栈中的栈帧信息：

**main[1] wherei**

**[1] SimpleDebugging.foo3(SimpleDebugging.java:16), pc =15**

**[2] SimpleDebugging.foo2(SimpleDebugging.java:10), pc = 8**

**[3] SimpleDebugging.foo1(SimpleDebugging.java:6), pc = 8**

**[4] SimpleDebugging.main(SimpleDebugging.java:19), pc = 10**

**wherei** 后的每一行代表一个方法调用和调用返回点（由程序计数器显示数值）。这里的调用序列是 **main()**, **foo1()**, **foo2()** 和 **foo3()**。

因为命令 **list** 展示了执行停止的地方，所以你通常有足够的信息得知发生了什么并修复它。命令 **help** 将会告诉你更多关于 **jdb** 的用法，但是在花更多的时间学习它之前必须明白命令行调试器往往需要花费更多的精力得到结果。使用 **jdb** 学习调试的基础部分，然后转而学习图形界面调试器。

### 图形化调试器

因此，尽管你可能一开始用 JDB 尝试调试，但是你将发现使用图形化调试器能更加高效、更快速地追踪 bug。IBM 的 Eclipse，Oracle 的 NetBeans 和 JetBrains 的 IntelliJ 这些集成开发环境都含有面向  Java 语言的好用的图形化调试器。

<!-- Benchmarking -->

## 基准测试

> 我们应该忘掉微小的效率提升，说的就是这些 97% 的时间做的事：过早的优化是万恶之源。
>
> ​                                                                                                                       —— Donald Knuth

如果你发现自己正在过早优化的滑坡上，你可能浪费了几个月的时间(如果你雄心勃勃的话)。通常，一个简单直接的编码方法就足够好了。如果你进行了不必要的优化，就会使你的代码变得无谓的复杂和难以理解。

基准测试意味着对代码或算法片段进行计时看哪个跑得更快，与下一节的分析和优化截然相反，分析优化是观察整个程序，找到程序中最耗时的部分。

可以简单地对一个代码片段的执行计时吗？在像 C 这样直接的编程语言中，这个方法的确可行。在像 Java 这样拥有复杂的运行时系统的编程语言中，基准测试变得更有挑战性。为了生成可靠的数据，环境设置必须控制诸如 CPU 频率，节能特性，其他运行在相同机器上的进程，优化器选项等等。

### 微基准测试

写一个计时工具类从而比较不同代码块的执行速度是具有吸引力的。看上去这会产生一些有用的数据。比如，这里有一个简单的 **Timer** 类，可以用以下两种方式使用它：

1. 创建一个 **Timer** 对象，执行一些操作然后调用 **Timer** 的 **duration()** 方法产生以毫秒为单位的运行时间。
2. 向静态的 **duration()** 方法中传入 **Runnable**。任何符合 **Runnable** 接口的类都有一个函数式方法 **run()**，该方法没有入参，且没有返回。

```java
// onjava/Timer.java
package onjava;
import static java.util.concurrent.TimeUnit.*;

public class Timer {
    private long start = System.nanoTime();
    
    public long duration() {
        return NANOSECONDS.toMillis(System.nanoTime() - start);
    }
    
    public static long duration(Runnable test) {
        Timer timer = new Timer();
        test.run();
        return timer.duration();
    }
}

```

这是一个很直接的计时方式。难道我们不能只运行一些代码然后看它的运行时长吗？

有许多因素会影响你的结果，即使是生成提示符也会造成计时的混乱。这里举一个看上去天真的例子，它使用了 标准的 Java **Arrays** 库（后面会详细介绍）：

```java
// validating/BadMicroBenchmark.java
// {ExcludeFromTravisCI}
import java.util.*;
import onjava.Timer;

public class BadMicroBenchmark {
    static final int SIZE = 250_000_000;
    
    public static void main(String[] args) {
        try { // For machines with insufficient memory
            long[] la = new long[SIZE];
            System.out.println("setAll: " + Timer.duration(() -> Arrays.setAll(la, n -> n)));
            System.out.println("parallelSetAll: " + Timer.duration(() -> Arrays.parallelSetAll(la, n -> n)));
        } catch (OutOfMemoryError e) {
            System.out.println("Insufficient memory");
            System.exit(0);
        }
    }
    
}
/* Output
setAll: 272
parallelSetAll: 301

```

**main()** 方法的主体包含在 **try** 语句块中，因为一台机器用光内存后会导致构建停止。

对于一个长度为 250,000,000 的 **long** 型（仅仅差一点就会让大部分机器内存溢出）数组，我们比较了 **Arrays.setAll()** 和 **Arrays.parallelSetAll()** 的性能。这个并行的版本会尝试使用多个处理器加快完成任务（尽管我在这一节谈到了一些并行的概念，但是在 [并发编程](./24-Concurrent-Programming.md) 章节我们才会详细讨论这些 ）。然而非并行的版本似乎运行得更快，尽管在不同的机器上结果可能不同。

**BadMicroBenchmark.java** 中的**==每一步操作都是独立的，但是如果你的操作依赖于同一资源，那么并行版本运行的速度会骤降，因为不同的进程会竞争相同的那个资源。==**

```java
// validating/BadMicroBenchmark2.java
// Relying on a common resource

import java.util.*;
import onjava.Timer;

public class BadMicroBenchmark2 {
    static final int SIZE = 5_000_000;
    
    public static void main(String[] args) {
        long[] la = new long[SIZE];
        Random r = new Random();
        System.out.println("parallelSetAll: " + Timer.duration(() -> Arrays.parallelSetAll(la, n -> r.nextLong())));
        System.out.println("setAll: " + Timer.duration(() -> Arrays.setAll(la, n -> r.nextLong())));
        SplittableRandom sr = new SplittableRandom();
        System.out.println("parallelSetAll: " + Timer.duration(() -> Arrays.parallelSetAll(la, n -> sr.nextLong())));
        System.out.println("setAll: " + Timer.duration(() -> Arrays.setAll(la, n -> sr.nextLong())));
    }
}
/* Output
parallelSetAll: 1147
setAll: 174
parallelSetAll: 86
setAll: 39


```

**SplittableRandom** 是为并行算法设计的，它当然看起来比普通的 **Random** 在 **parallelSetAll()** 中运行得更快。 但是看上去还是比非并发的 **setAll()** 运行时间更长，有点难以置信（也许是真的，但我们不能通过一个坏的微基准测试得到这个结论）。

这只考虑了微基准测试的问题。Java 虚拟机 Hotspot 也非常影响性能。如果你在测试前没有通过运行代码给 JVM 预热，那么你就会得到“冷”的结果，不能反映出代码在 JVM 预热之后的运行速度（假如你运行的应用没有在预热的 JVM 上运行，你就可能得不到所预期的性能，甚至可能减缓速度）。

优化器有时可以检测出你创建了没有使用的东西，或者是部分代码的运行结果对程序没有影响。如果它优化掉你的测试，那么你可能得到不好的结果。

一个良好的微基准测试系统能自动地弥补像这样的问题（和很多其他的问题）从而产生合理的结果，但是创建这么一套系统是非常棘手，需要深入的知识。

### JMH 的引入

截止目前为止，唯一能产生像样结果的 Java 微基准测试系统就是 Java Microbenchmarking Harness，简称 JMH。本书的 **build.gradle** 自动引入了 JMH 的设置，所以你可以轻松地使用它。

你可以在命令行编写 JMH 代码并运行它，但是推荐的方式是让 JMH 系统为你运行测试；**build.gradle** 文件已经配置成只需要一条命令就能运行 JMH 测试。

JMH 尝试使基准测试变得尽可能简单。例如，我们将使用 JMH 重新编写 **BadMicroBenchmark.java**。这里只有 **@State** 和 **@Benchmark** 这两个注解是必要的。其余的注解要么是为了产生更多易懂的输出，要么是加快基准测试的运行速度（JMH 基准测试通常需要运行很长时间）：

```java
// validating/jmh/JMH1.java
package validating.jmh;
import java.util.*;
import org.openjdk.jmh.annotations.*;
import java.util.concurrent.TimeUnit;

@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
// Increase these three for more accuracy:
@Warmup(iterations = 5)
@Measurement(iterations = 5)
@Fork(1)
public class JMH1 {
    private long[] la;
    
    @Setup
    public void setup() {
        la = new long[250_000_000];
    }
    
    @Benchmark
    public void setAll() {
        Arrays.setAll(la, n -> n);
    }
    
    public void parallelSetAll() {
        Arrays.parallelSetAll(la, n -> n);
    }
}

```

“forks” 的默认值是 10，意味着每个测试都运行 10 次。为了减少运行时间，这里使用了 **@Fork** 注解来减少这个次数到 1。我还使用了 **@Warmup** 和 **@Measurement** 注解将它们默认的运行次数从 20 减少到 5 次。尽管这降低了整体的准确率，但是结果几乎与使用默认值相同。可以尝试将 **@Warmup**、**@Measurement** 和 **@Fork** 都注释掉然后看使用它们的默认值，结果会有多大显著的差异；一般来说，你应该只能看到长期运行的测试使错误因素减少，而结果没有多大变化。

需要使用显式的 gradle 命令才能运行基准测试（在示例代码的根目录处运行）。这能防止耗时的基准测试运行其他的 **gradlew** 命令：

**gradlew validating:jmh**

这会花费几分钟的时间，取决于你的机器(如果没有注解上的调整，可能需要几个小时)。控制台会显示 **results.txt** 文件的路径，这个文件统计了运行结果。注意，**results.txt** 包含这一章所有 **jmh** 测试的结果：**JMH1.java**，**JMH2.java** 和 **JMH3.java**。

因为输出是绝对时间，所以在不同的机器和操作系统上结果各不相同。重要的因素不是绝对时间，我们真正观察的是一个算法和另一个算法的比较，尤其是哪一个运行得更快，快多少。如果你在自己的机器上运行测试，你将看到不同的结果却有着相同的模式。

我在大量的机器上运行了这些测试，尽管不同的机器上得到的绝对值结果不同，但是相对值保持着合理的稳定性。我只列出了 **results.txt** 中适当的片段并加以编辑使输出更加易懂，而且内容大小适合页面。所有测试中的 **Mode** 都以 **avgt** 展示，代表 “平均时长”。**Cnt**（测试的数目）的值是 200，尽管这里的一个例子中配置的 **Cnt** 值是 5。**Units** 是 **us/op**，是 “Microseconds per operation” 的缩写，因此，这个值越小代表性能越高。

我同样也展示了使用 warmups、measurements 和 forks 默认值的输出。我删除了示例中相应的注解，就是为了获取更加准确的测试结果（这将花费数小时）。结果中数字的模式应该仍然看起来相同，不论你如何运行测试。

下面是 **JMH1.java** 的运行结果：

**Benchmark Score**

**JMH1.setAll 196280.2**

**JMH1.parallelSetAll 195412.9**

即使像 JMH 这么高级的基准测试工具，基准测试的过程也不容易，练习时需要倍加小心。这里测试产生了反直觉的结果：并行的版本 **parallelSetAll()** 花费了与非并行版本的 **setAll()** 相同的时间，两者似乎都运行了相当长的时间。

当创建这个示例时，我假设如果我们要测试数组初始化的话，那么使用非常大的数组是有意义的。所以我选择了尽可能大的数组；如果你实验的话会发现一旦数组的大小超过 2亿5000万，你就开始会得到内存溢出的异常。然而，在这么大的数组上执行大量的操作从而震荡内存系统，产生无法预料的结果是有可能的。不管这个假设是否正确，看上去我们正在测试的并非是我们想测试的内容。

**考虑其他的因素：**

C：客户端执行操作的线程数量

P：并行算法使用的并行数量

N：数组的大小：**10^(2*k)**，通常来说，**k=1..7** 足够来练习不同的缓存占用。

Q：setter 的操作成本

这个 C/P/N/Q 模型在早期 JDK 8 的 Lambda 开发期间付出水面，大多数并行的 Stream 操作(**parallelSetAll()** 也基本相似)都满足这些结论：**N*Q**(主要工作量)对于并发性能尤为重要。并行算法在工作量较少时可能实际运行得更慢。

在一些情况下操作竞争如此激烈使得并行毫无帮助，而不管 **N*Q** 有多大。当 **C** 很大时，**P** 就变得不太相关（内部并行在大量的外部并行面前显得多余）。此外，在一些情况下，并行分解会让相同的 **C** 个客户端运行得比它们顺序运行代码更慢。

基于这些信息，我们重新运行测试，并在这些测试中使用不同大小的数组（改变 **N**）：

```java
// validating/jmh/JMH2.java
package validating.jmh;
import java.util.*;
import org.openjdk.jmh.annotations.*;
import java.util.concurrent.TimeUnit;

@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Warmup(iterations = 5)
@Measurement(iterations = 5)
@Fork(1)
public class JMH2 {

    private long[] la;

    @Param({
            "1",
            "10",
            "100",
            "1000",
            "10000",
            "100000",
            "1000000",
            "10000000",
            "100000000",
            "250000000"
    })
    int size;

    @Setup
    public void setup() {
        la = new long[size];
    }

    @Benchmark
    public void setAll() {
        Arrays.setAll(la, n -> n);
    }

    @Benchmark
    public void parallelSetAll() {
        Arrays.parallelSetAll(la, n -> n);
    }
}


```

**@Param** 会自动地将其自身的值注入到变量中。其自身的值必须是字符串类型，并可以转化为适当的类型，在这个例子中是 **int** 类型。

下面是已经编辑过的结果，包含精确计算出的加速数值：

| JMH2 Benchmark     | Size      | Score %    | Speedup |
| ------------------ | --------- | ---------- | ------- |
| **setAll**         | 1         | 0.001      |         |
| **parallelSetAll** | 1         | 0.036      | 0.028   |
| **setAll**         | 10        | 0.005      |         |
| **parallelSetAll** | 10        | 3.965      | 0.001   |
| **setAll**         | 100       | 0.031      |         |
| **parallelSetAll** | 100       | 3.145      | 0.010   |
| **setAll**         | 1000      | 0.302      |         |
| **parallelSetAll** | 1000      | 3.285      | 0.092   |
| **setAll**         | 10000     | 3.152      |         |
| **parallelSetAll** | 10000     | 9.669      | 0.326   |
| **setAll**         | 100000    | 34.971     |         |
| **parallelSetAll** | 100000    | 20.153     | 1.735   |
| **setAll**         | 1000000   | 420.581    |         |
| **parallelSetAll** | 1000000   | 165.388    | 2.543   |
| **setAll**         | 10000000  | 8160.054   |         |
| **parallelSetAll** | 10000000  | 7610.190   | 1.072   |
| **setAll**         | 100000000 | 79128.752  |         |
| **parallelSetAll** | 100000000 | 76734.671  | 1.031   |
| **setAll**         | 250000000 | 199552.121 |         |
| **parallelSetAll** | 250000000 | 191791.927 | 1.040   |

可以看到当数组大小达到 10 万左右时，**parallelSetAll()** 开始反超，而后趋于与非并行的运行速度相同。即使它运行速度上胜了，看起来也不足以证明由于并行的存在而使速度变快。

**setAll()/parallelSetAll()** 中工作的计算量起很大影响吗？在前面的例子中，我们所做的只有对数组的赋值操作，这可能是最简单的任务。所以即使 **N** 值变大，**N*Q** 也仍然没有达到巨大，所以看起来像是我们没有为并行提供足够的机会（JMH 提供了一种模拟变量 Q 的途径；如果想了解更多的话，可搜索 **Blackhole.consumeCPU**）。

我们通过使方法 **f()** 中的任务变得更加复杂，从而产生更多的并行机会：

```java
// validating/jmh/JMH3.java
package validating.jmh;
import java.util.*;
import org.openjdk.jmh.annotations.*;
import java.util.concurrent.TimeUnit;

@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Warmup(iterations = 5)
@Measurement(iterations = 5)
@Fork(1)
public class JMH3 {
    private long[] la;

    @Param({
            "1",
            "10",
            "100",
            "1000",
            "10000",
            "100000",
            "1000000",
            "10000000",
            "100000000",
            "250000000"
    })
    int size;

    @Setup
    public void setup() {
        la = new long[size];
    }

    public static long f(long x) {
        long quadratic = 42 * x * x + 19 * x + 47;
        return Long.divideUnsigned(quadratic, x + 1);
    }

    @Benchmark
    public void setAll() {
        Arrays.setAll(la, n -> f(n));
    }

    @Benchmark
    public void parallelSetAll() {
        Arrays.parallelSetAll(la, n -> f(n));
    }
}

```

**f()** 方法提供了更加复杂且耗时的操作。现在除了简单的给数组赋值外，**setAll()** 和 **parallelSetAll()** 都有更多的工作去做，这肯定会影响结果。

| JMH2 Benchmark     | Size      | Score %     | Speedup |
| ------------------ | --------- | ----------- | ------- |
| **setAll**         | 1         | 0.012       |         |
| **parallelSetAll** | 1         | 0.047       | 0.255   |
| **setAll**         | 10        | 0.107       |         |
| **parallelSetAll** | 10        | 3.894       | 0.027   |
| **setAll**         | 100       | 0.990       |         |
| **parallelSetAll** | 100       | 3.708       | 0.267   |
| **setAll**         | 1000      | 133.814     |         |
| **parallelSetAll** | 1000      | 11.747      | 11.391  |
| **setAll**         | 10000     | 97.954      |         |
| **parallelSetAll** | 10000     | 37.259      | 2.629   |
| **setAll**         | 100000    | 988.475     |         |
| **parallelSetAll** | 100000    | 276.264     | 3.578   |
| **setAll**         | 1000000   | 9203.103    |         |
| **parallelSetAll** | 1000000   | 2826.974    | 3.255   |
| **setAll**         | 10000000  | 92144.951   |         |
| **parallelSetAll** | 10000000  | 28126.202   | 3.276   |
| **setAll**         | 100000000 | 921701.863  |         |
| **parallelSetAll** | 100000000 | 266750.543  | 3.455   |
| **setAll**         | 250000000 | 2299127.273 |         |
| **parallelSetAll** | 250000000 | 538173.425  | 4.272   |

可以看到当数组的大小达到 1000 左右时，**parallelSetAll()** 的运行速度反超了 **setAll()**。==看来 **parallelSetAll()** 严重依赖数组中计算的复杂度。==这正是基准测试的价值所在，因为我们已经得到了关于 **setAll()** 和 **parallelSetAll()** 间微妙的信息，知道在何时使用它们。

这显然不是从阅读 Javadocs 就能得到的。

大多数时候，JMH 的简单应用会产生好的结果（正如你将在本书后面例子中所见），但是我们从这里知道，你不能一直假定 JMH 会产生好的结果。 JMH 网站上的范例可以帮助你开始。

<!-- Profiling and Optimizing -->

## 剖析和优化

有时你必须检测程序运行时间花在哪儿，从而看是否可以优化那一块的性能。剖析器可以找到这些导致程序慢的地方，因而你可以找到最轻松，最明显的方式加快程序运行速度。

剖析器收集的信息能显示程序哪一部分消耗内存，哪个方法最耗时。一些剖析器甚至能关闭垃圾回收，从而帮助限定内存分配的模式。

剖析器还可以帮助检测程序中的线程死锁。注意剖析和基准测试的区别。剖析关注的是已经运行在真实数据上的整个程序，而**基准测试关注的是程序中隔离的片段，通常是去优化算法。**

安装 Java 开发工具包（JDK）时会顺带安装一个虚拟的剖析器，叫做 ==**VisualVM**。==它会被自动安装在与 **javac** 相同的目录下，你的执行路径应该已经包含该目录。启动 VisualVM 的控制台命令是：

**> jvisualvm**

运行该命令后会弹出一个窗口，其中包括一些指向帮助信息的链接。

### 优化准则

- 避免为了性能牺牲代码的可读性。
- 不要独立地看待性能。衡量与带来的收益相比所需投入的工作量。
- 程序的大小很重要。性能优化通常只对运行了长时间的大型项目有价值。性能通常不是小项目的关注点。
- 运行起来程序比一心钻研它的性能具有更高的优先级。一旦你已经有了可工作的程序，如有必要的话，你可以使用剖析器提高它的效率。只有当性能是关键因素时，才需要在设计/开发阶段考虑性能。
- 不要猜测瓶颈发生在哪。运行剖析器，让剖析器告诉你。
- 无论何时有可能的话，**显式地设置实例为 null 表明你不再用它。这对垃圾收集器来说是个有用的暗示。**
- ==**static final** 修饰的变量会被 JVM 优化从而提高程序的运行速度。==因而程序中的常量应该声明 **static final**。

<!-- Style Checking -->

## 风格检测

当你在一个团队中工作时(包括尤其是开源项目)，让每个人遵循相同的代码风格是非常有帮助的。这样阅读项目的代码时，不会因为风格的不同产生思维上的中断。然而，如果你习惯了某种不同的代码风格，那么记住项目中所有的风格准则对你来说可能是困难的。幸运的是，存在可以指出你代码中不符合风格准则的工具。

一个流行的风格检测器是 **Checkstyle**。查看本书 [示例代码](https://github.com/BruceEckel/OnJava8-Examples) 中的 **gradle.build** 和 **checkstyle.xml** 文件中配置代码风格的方式。checkstyle.xml 是一个常用检测的集合，其中一些检测被注释掉了以允许使用本书中的代码风格。

运行所有风格检测的命令是：

**gradlew checkstyleMain**

一些文件仍然产生了风格检测警告，通常是因为这些例子展示了你在生产代码中不会使用的样例。

你还可以针对一个具体的章节运行代码检测。例如，下面命令会运行 [Annotations](./23-Annotations.md) 章节的风格检测：

**gradlew annotations:checkstyleMain**

<!-- Static Error Analysis -->

## 静态错误分析

尽管 Java 的静态类型检测可以发现基本的语法错误，其他的分析工具可以发现躲避 **javac** 检测的更加复杂的bug。一个这样的工具叫做 **Findbugs**。本书 [示例代码](https://github.com/BruceEckel/OnJava8-Examples) 中的 **build.gradle** 文件包含了 Findbugs 的配置，所以你可以输入如下命令：

**gradlew findbugsMain**

这会为每一章生成一个名为 **main.html** 的报告，报告中会说明代码中潜在的问题。Gradle 命令的输出会告诉你每个报告在何处。

当你查看报告时，你将会看到很多 false positive 的情况，即代码没问题却报告了问题。我在一些文件中展示了不要做一些事的代码确实是正确的。

当我最初看到本书的 Findbugs 报告时，我发现了一些不是技术错误的地方，但能使我改善代码。如果你正在寻找 bug，那么在调试之前运行 Findbugs 是值得的，因为这将可能节省你数小时的时间找到问题。

<!-- Code Reviews -->

## 代码重审

单元测试能找到明显重要的 bug 类型，风格检测和 Findbugs 能自动执行代码重审，从而发现额外的问题。最终你走到了必须人为参与进来的地步。代码重审是一个或一群人的一段代码被另一个或一群人阅读和评估的众多方式之一。这最初看起来会使人不安，而且需要情感信任，但它的目的肯定不是羞辱任何人。它的目标是找到程序中的错误，代码重审是最成功的能做到这点的途径之一。可惜的是，它们也经常被认为是“过于昂贵的”（有时这会成为程序员避免代码被重审时感到尴尬的借口）。

代码重审可以作为结对编程的一部分，作为代码签入过程的一部分（另一个程序员自动安排上审查新代码的任务）或使用群组预排的方式，即每个人阅读代码并讨论之。后一种方式对于分享知识和营造代码文化是极其有益的。

<!-- Pair Programming -->

## 结对编程

结对编程是指两个程序员一起编程的实践活动。通常来说，一个人“驱动”（敲击键盘，输入代码），另一人（观察者或指引者）重审和分析代码，同时也要思考策略。这产生了一种实时的代码重审。通常程序员会定期地互换角色。

结对编程有很多好处，但最显著的是分享知识和防止阻塞。最佳传递信息的方式之一就是一起解决问题，我已经在很多次研讨会使用了结对编程，都取得了很好的效果（同时，研讨会上的众人可以通过这种方式互相了解对方）。而且两个人一起工作时，可以更容易地推进开发的进展，而只有一个程序员的话，可能被轻易地卡住。结对编程的程序员通常可以从工作中感到更高的满足感。有时很难向管理人员们推行结对编程，因为他们可能觉得两个程序员解决同一个问题的效率比他们分开解决不同问题的效率低。尽管短期内是这样，但是结对编程能带来更高的代码质量；除了结对编程的其他益处，如果你眼光长远的话，这会产生更高的生产力。

维基百科上这篇 [结对编程的文章](https://en.wikipedia.org/wiki/Pair_programming) 可以作为你深入了解结对编程的开始。

<!-- Refactoring -->

## 重构

技术负债是指迭代发展的软件中为了应急而生的丑陋解决方案从而导致设计难以理解，代码难以阅读的部分。特别是当你必须修改和增加新特性的时候，这会造成麻烦。

**重构可以矫正技术负债。重构的关键是它能改善代码设计，结构和可读性（因而减少代码负债），但是它不能改变代码的行为。**

很难向管理人员推行重构：“我们将投入很多工作不是增加新的特性，当我们完成时，外界无感知变化。但是相信我们，事情会变得更加美好”。不幸的是，管理人员意识到重构的价值时都为时已晚了：当他们提出增加新的特性时，你不得不告诉他们做不到，因为代码基底已经埋藏了太多的问题，试图增加新特性可能会使软件崩溃，即使你能想出怎么做。

### 重构基石

在开始重构代码之前，你需要有以下三个系统的支撑：

1. **测试**（通常，JUnit 测试作为最小的根基），因此你能确保重构不会改变代码的行为。
2. **自动构建**，因而你能轻松地构建代码，运行所有的测试。通过这种方式做些小修改并确保修改不会破坏任何事物是毫不费力的。本书使用的是 Gradle 构建系统，你可以在 [代码示例](https://github.com/BruceEckel/OnJava8-Examples) 的 **build.gradle** 文件中查看示例。
3. **版本控制**，以便你能回退到可工作的代码版本，能够一直记录重构的每一步。

本书的代码托管在 [Github](https://github.com/BruceEckel/OnJava8-Examples) 上，使用的是 **git** 版本控制系统。

没有这三个系统的支持，重构几乎是不可能的。确实，没有这些系统，起初维护和增加代码是一个巨大的挑战。令人意外的是，有很多成功的公司竟然在没有这三个系统的情况下在相当长的时间里勉强过得去。然而，对于这样的公司来说，在他们遇到严重的问题之前，这只是个时间问题。

维基百科上的 [重构文章](https://en.wikipedia.org/wiki/Code_refactoring) 提供了更多的细节。

<!-- Continuous Integration -->

## 持续集成

在软件开发的早期，人们只能一次处理一步，所以他们坚信他们总是在经历快乐之旅，每个开发阶段无缝进入下一个。这种错觉经常被称为软件开发中的“瀑布流模型”。很多人告诉我瀑布流是他们的选择方法，好像这是一个选择工具，而不仅是一厢情愿。

在这片童话的土地上，每一步都按照指定的预计时间准时完美结束，然后下一步开始。当最后一步结束时，所有的部件都可以无缝地滑在一起，瞧，一个装载产品诞生了！

当然，现实中没有事能按计划或预计时间运作。相信它应该，然后当它不能时更加相信，只会使整件事变得更糟。否认证据不会产生好的结果。

除此之外，产品本身经常也不是对客户有价值的事物。有时一大堆的特性完全是浪费时间，因为创造出这些特性需求的人不是客户而是其他人。

因为受流水工作线的思路影响，所以每个开发阶段都有自己的团队。上游团队的延期传递到下游团队，当到了需要进行测试和集成的时候，这些团队被指望赶上预期时间，当他们必然做不到时，就认为他们是“差劲的团队成员”。不可能的时间安排和负相关的结合产生了自实现的预期：只有最绝望的开发者才会乐意做这些工作。

另外，商学院培养出的管理人员仍然被训练成只在已有的流程上做一些改动——这些流程都是基于工业时代制造业的想法上。注重培养创造力而不是墨守成规的商学院仍然很稀有。终于一些编程领域的人们再也忍受不了这种情况并开始进行实验。最初一些实验叫做“极限编程”，因为它们与工业时代的思想完全不同。随着实验展示的结果，这些思想开始看起来像是常识。这些实验逐渐形成了如今显而易见的观点——尽管非常小——即把生产可运作的产品交到客户手中，询问他们 (A) 是否想要它 (B) 是否喜欢它工作的方式 (C) 还希望有什么其他有用的功能特性。然后这些信息反馈给开发，从而继续产出一个新版本。版本不断迭代，项目最终演变成为客户带来真正价值的事物。

这完全颠倒了瀑布流开发的方式。你停止假设你要处理产品测试和把部署"作为最后一步"这类的事情。相反，每件事从开始到结束必须都在进行——即使一开始产品几乎没有任何特性。这么做对于在开发周期的早期发现更多问题有巨大的益处。此外，不是做大量宏大超前的计划和花费时间金钱在许多无用的特性上，而是一直都能从顾客那得到反馈。当客户不再需要其他特性时，你就完成了。这节省了大量的时间和金钱，并提高了顾客的满意度。

**有许多不同的想法导向这种方式，但是目前首要的术语叫持续集成（CI）。**CI 与导向 CI 的想法之间的不同之处在于 CI 是一种独特的机械式的过程，过程中涵盖了这些想法；它是一种定义好的做事方式。事实上，它定义得如此明确以至于整个过程是自动化的。

当前 CI 技术的高峰是持续集成服务器。这是一台独立的机器或虚拟机，通常是由第三方公司托管的完全独立的服务。这些公司通常免费提供基本服务，如果你需要额外的特性如更多的处理器或内存或者专门的工具或系统，你需要付费。CI 服务器起初是完全空白状态，即只是可用的操作系统的最小配置。这很重要因为你可能之前在你的开发机器上安装过一些程序，却没有在你的构建和部署系统中包含它。正如重构一样，持续集成需要分布式版本管理，自动构建和自动测试系统作为基础。通常来说，CI 服务器会绑定到你的版本控制仓库上。当 CI 服务器发现仓库中有改变时，就会拉取最新版本的代码，并按照 CI 脚本中的过程处理。这包括安装所有必要的工具和类库（记住，CI 服务器起初只有一个干净、基本的操作系统），所以如果过程中出现任何问题，你都可以发现它们。接着它会执行脚本中定义的构建和测试操作；通常脚本中使用的命令与人们在安装和测试中使用的命令完全相同。如果执行成功或失败，CI 服务器会有许多种方式汇报给你，包括在你的代码仓库上显示一个简单的标记。

使用持续集成，每次你合进仓库时，这些改变都会被从头到尾验证。通过这种方式，一旦出现问题你能立即发现。甚至当你准备交付一个产品的新版本时，都不会有延迟或其他必要的额外步骤（在任何时刻都可以交付叫做持续交付）。

本书的示例代码都是在 Travis-CI(基于 Linux 的系统) 和 AppVeyor(Windows) 上自动测试的。你可以在 [Gihub仓库](https://github.com/BruceEckel/OnJava8-Examples) 上的 Readme 看到通过/失败的标记。

<!-- Summary -->

## 本章小结

"它在我的机器上正常工作了。" "我们不会运载你的机器！"

代码校验不是单一的过程或技术。**每种方法只能发现特定类型的 bug，作为程序员的你在开发过程中会明白每个额外的技术都能增加代码的可靠性和鲁棒性。校验不仅能在开发过程中，还能在为应用添加新功能的整个项目期间帮你发现更多的错误。**现代化开发意味着比仅仅编写代码更多的内容，每种你在开发过程中融入的测试技术—— 包括而且尤其是你创建的能适应特定应用的自定义工具——都会带来更好、更快和更加愉悦的开发过程，同时也能为客户提供更高的价值和满意度体验。



<!-- Strings -->

# 第十八章 字符串

> 字符串操作毫无疑问是计算机程序设计中最常见的行为之一。

在 Java 大展拳脚的 Web 系统中更是如此。

<!-- Immutable Strings -->

## 字符串的不可变

==`String` 对象是不可变的==。查看 JDK 文档你就会发现，`String` 类中每一个看起来会修改 `String` 值的**方法，实际上都是创建了一个全新的 `String` 对象**，以包含修改后的字符串内容。而最初的 `String` 对象则丝毫未动。

看看下面的代码：

```java
// strings/Immutable.java
public class Immutable { 
    public static String upcase(String s) { 
        return s.toUpperCase(); 
    } 
    public static void main(String[] args) { 
        String q = "howdy";
        System.out.println(q); // howdy 
        String qq = upcase(q); 
        System.out.println(qq); // HOWDY 
        System.out.println(q); // howdy 
    } 
} 
/* Output: 
howdy
HOWDY 
howdy
*/ 
```

当把 `q` 传递给 `upcase()` 方法时，实际传递的是引用的一个拷贝。其实，每当把 String 对象作为方法的参数时，都会复制一份引用，而该引用所指向的对象其实一直待在单一的物理位置上，从未动过。

回到 `upcase()` 的定义，传入其中的引用有了名字 `s`，只有 `upcase()` 运行的时候，局部引用 `s` 才存在。一旦 `upcase()` 运行结束，`s` 就消失了。当然了，`upcase()` 的返回值，其实是最终结果的引用。这足以说明，`upcase()` 返回的引用已经指向了一个新的对象，而 `q` 仍然在原来的位置。

`String` 的这种行为正是我们想要的。例如：

```java
String s = "asdf";
String x = Immutable.upcase(s);
```

难道你真的希望 `upcase()` 方法改变其参数吗？对于一个方法而言，参数是为该方法提供信息的，而不是想让该方法改变自己的。在阅读这段代码时，读者自然会有这样的感觉。这一点很重要，正是有了这种保障，才使得代码易于编写和阅读。

<!-- Overloading + vs. StringBuilder -->

## `+` 的重载与 `StringBuilder`

`String` 对象是不可变的，你可以给一个 `String` 对象添加任意多的别名。**因为 `String` 是只读的**，所以**指向它的任何引用都不可能修改它的值**，因此，也就不会影响到其他引用。

不可变性会带来一定的效率问题。为 `String` 对象重载的 `+` 操作符就是一个例子。重载的意思是，一个操作符在用于特定的类时，被赋予了特殊的意义（**用于 `String` 的 `+` 与 `+=` 是 Java 中仅有的两个重载过的操作符**，Java 不允许程序员重载任何其他的操作符 [^1]）。

操作符 `+` 可以用来连接 `String`：

```java
// strings/Concatenation.java

public class Concatenation {
    public static void main(String[] args) { 
        String mango = "mango"; 
        String s = "abc" + mango + "def" + 47; 
        System.out.println(s);
    } 
}
/* Output:
abcmangodef47 
*/
```

可以想象一下，这段代码是这样工作的：`String` 可能有一个 `append()` 方法，它会生成一个新的 `String` 对象，以包含“abc”与 `mango` 连接后的字符串。该对象会再创建另一个新的 `String` 对象，然后与“def”相连，生成另一个新的对象，依此类推。

这种方式当然是可行的，但是为了生成最终的 `String` 对象，会产生一大堆需要垃圾回收的中间对象。我猜想，Java 设计者一开始就是这么做的（这也是软件设计中的一个教训：除非你用代码将系统实现，并让它运行起来，否则你无法真正了解它会有什么问题），然后他们发现其性能相当糟糕。

想看看以上代码到底是如何工作的吗？**可以用 JDK 自带的 `javap` 工具来反编译以上代码。**命令如下：

```java
javap -c Concatenation
```

**这里的 `-c` 标志表示将生成 JVM 字节码。**我们剔除不感兴趣的部分，然后做细微的修改，于是有了以下的字节码：

```x86asm
public static void main(java.lang.String[]); 
 Code:
  Stack=2, Locals=3, Args_size=1
  0: ldc #2; //String mango 
  2: astore_1 
  3: new #3; //class StringBuilder 
  6: dup 
  7: invokespecial #4; //StringBuilder."<init>":() 
  10: ldc #5; //String abc 
  12: invokevirtual #6; //StringBuilder.append:(String) 
  15: aload_1 
  16: invokevirtual #6; //StringBuilder.append:(String) 
  19: ldc #7; //String def 
  21: invokevirtual #6; //StringBuilder.append:(String) 
  24: bipush 47 
  26: invokevirtual #8; //StringBuilder.append:(I) 
  29: invokevirtual #9; //StringBuilder.toString:() 
  32: astore_2 
  33: getstatic #10; //Field System.out:PrintStream;
  36: aload_2 
  37: invokevirtual #11; //PrintStream.println:(String) 
  40: return
```

如果你有汇编语言的经验，以上代码应该很眼熟(其中的 `dup` 和 `invokevirtual` 语句相当于Java虚拟机上的汇编语句。即使你完全不了解汇编语言也无需担心)。**需要重点注意的是：编译器自动引入了 `java.lang.StringBuilder` 类。虽然源代码中并没有使用 `StringBuilder` 类，但是编译器却自作主张地使用了它，就因为它更高效。**

在这里，编译器创建了一个 `StringBuilder` 对象，用于构建最终的 `String`，并对每个字符串调用了一次 `append()` 方法，共计 4 次。最后调用 `toString()` 生成结果，并存为 `s` (使用的命令为 `astore_2`)。

现在，也许你会觉得可以随意使用 `String` 对象，反正编译器会自动为你做性能优化。可是在这之前，让我们更深入地看看编译器能为我们优化到什么程度。下面的例子采用两种方式生成一个 `String`：方法一使用了多个 `String` 对象；方法二在代码中使用了 `StringBuilder`。

```java
// strings/WhitherStringBuilder.java

public class WhitherStringBuilder { 
    public String implicit(String[] fields) { 
        String result = ""; 
        for(String field : fields) { 
            result += field;
        }
        return result; 
    }
    public String explicit(String[] fields) { 
        StringBuilder result = new StringBuilder(); 
        for(String field : fields) { 
            result.append(field); 
        } 
        return result.toString(); 
    }
}
```

现在运行 `javap -c WitherStringBuilder`，可以看到两种不同方法（我已经去掉不相关的细节）对应的字节码。首先是 `implicit()` 方法：

```x86asm
public java.lang.String implicit(java.lang.String[]); 
0: ldc #2 // String 
2: astore_2
3: aload_1 
4: astore_3 
5: aload_3 
6: arraylength 
7: istore 4 
9: iconst_0 
10: istore 5 
12: iload 5 
14: iload 4 
16: if_icmpge 51 
19: aload_3 
20: iload 5 
22: aaload 
23: astore 6 
25: new #3 // StringBuilder 
28: dup 
29: invokespecial #4 // StringBuilder."<init>"
32: aload_2 
33: invokevirtual #5 // StringBuilder.append:(String) 
36: aload 6 
38: invokevirtual #5 // StringBuilder.append:(String;) 
41: invokevirtual #6 // StringBuilder.toString:() 
44: astore_2 
45: iinc 5, 1 
48: goto 12 
51: aload_2 
52: areturn
```

注意从第 16 行到第 48 行构成了一个循环体。第 16 行：对堆栈中的操作数进行“大于或等于的整数比较运算”，循环结束时跳转到第 51 行。第 48 行：重新回到循环体的起始位置（第 12 行）。**注意：`StringBuilder` 是在循环内构造的，这意味着每进行一次循环，会创建一个新的 `StringBuilder` 对象。**

下面是 `explicit()` 方法对应的字节码：

```x86asm
public java.lang.String explicit(java.lang.String[]); 
0: new #3 // StringBuilder 
3: dup
4: invokespecial #4 // StringBuilder."<init>" 
7: astore_2 
8: aload_1 
9: astore_3 
10: aload_3 
11: arraylength 
12: istore 4 
14: iconst_0 
15: istore 5 
17: iload 5 
19: iload 4 
21: if_icmpge 43 
24: aload_3 
25: iload 5 
27: aaload 
28: astore 6 
30: aload_2 
31: aload 6 
33: invokevirtual #5 // StringBuilder.append:(String) 
36: pop
37: iinc 5, 1 
40: goto 17 
43: aload_2 
44: invokevirtual #6 // StringBuilder.toString:() 
47: areturn
```

可以看到，不仅循环部分的代码更简短、更简单，而且**它只生成了一个 `StringBuilder` 对象。显式地创建 `StringBuilder` 还允许你预先为其指定大小。如果你已经知道最终字符串的大概长度，那预先指定 `StringBuilder` 的大小可以避免频繁地重新分配缓冲。**

因此，当你为一个类编写 `toString()` 方法时，如果字符串操作比较简单，那就可以信赖编译器，它会为你合理地构造最终的字符串结果。但是，如果**你要在 `toString()` 方法中使用循环，且可能有性能问题**，那么最好自己创建一个 `StringBuilder` 对象，用它来构建最终结果。请参考以下示例：

```java
// strings/UsingStringBuilder.java 

import java.util.*; 
import java.util.stream.*; 
public class UsingStringBuilder { 
    public static String string1() { 
        Random rand = new Random(47);
        StringBuilder result = new StringBuilder("["); 
        for(int i = 0; i < 25; i++) { 
            result.append(rand.nextInt(100)); 
            result.append(", "); 
        } 
        result.delete(result.length()-2, result.length()); 
        result.append("]");
        return result.toString(); 
    } 
    public static String string2() { 
        String result = new Random(47)
            .ints(25, 0, 100)
            .mapToObj(Integer::toString)
            .collect(Collectors.joining(", "));
        return "[" + result + "]"; 
    } 
    public static void main(String[] args) { 
        System.out.println(string1()); 
        System.out.println(string2()); 
    }
} 
/* Output: 
[58, 55, 93, 61, 61, 29, 68, 0, 22, 7, 88, 28, 51, 89, 
9, 78, 98, 61, 20, 58, 16, 40, 11, 22, 4] 
[58, 55, 93, 61, 61, 29, 68, 0, 22, 7, 88, 28, 51, 89,
9, 78, 98, 61, 20, 58, 16, 40, 11, 22, 4] 
*/ 
```

在方法 `string1()` 中，最终结果是用 `append()` 语句拼接起来的。如果你想走捷径，例如：`append(a + ": " + c)`，编译器就会掉入陷阱，从而为你另外创建一个 `StringBuilder` 对象处理括号内的字符串操作。如果拿不准该用哪种方式，随时可以用 `javap` 来分析你的程序。

`StringBuilder` 提供了丰富而全面的方法，包括 `insert()`、`replace()`、`substring()`，甚至还有`reverse()`，但是最常用的还是 `append()` 和 `toString()`。还有 `delete()`，上面的例子中我们用它删除最后一个逗号和空格，以便添加右括号。

`string2()` 使用了 `Stream`，这样代码更加简洁美观。可以证明，`Collectors.joining()` 内部也是使用的 `StringBuilder`，这种写法不会影响性能！

`StringBuilder `是 Java SE5 引入的，在这之前用的是 `StringBuffer`。后者是线程安全的（参见[并发编程](./24-Concurrent-Programming.md)），因此开销也会大些。使用 `StringBuilder` 进行字符串操作更快一点。

<!-- Unintended Recursion -->

## 意外递归

如果你真的**想要打印对象的内存地址，应该调用 `Object.toString()` 方法，这才是负责此任务的方法。所以，不要使用 `this`，而是应该调用 `super.toString()` 方法。**

Java 中的每个类从根本上都是继承自 `Object`，标准集合类也是如此，它们都有 `toString()` 方法，并且覆盖了该方法，使得它生成的 `String` 结果能够表达集合自身，以及集合包含的对象。例如 `ArrayList.toString()`，它会遍历 `ArrayList` 中包含的所有对象，调用每个元素上的 `toString()` 方法：

```java
// strings/ArrayListDisplay.java 
import java.util.*;
import java.util.stream.*; 
import generics.coffee.*;
public class ArrayListDisplay { 
    public static void main(String[] args) {
        List<Coffee> coffees = 
            Stream.generate(new CoffeeSupplier())
                .limit(10)
                .collect(Collectors.toList()); 
        System.out.println(coffees); 
    } 
}
/* Output: 
[Americano 0, Latte 1, Americano 2, Mocha 3, Mocha 4, 
Breve 5, Americano 6, Latte 7, Cappuccino 8, Cappuccino 9] 
*/ 

```

如果你希望 `toString()` 打印出类的内存地址，也许你会考虑使用 `this` 关键字：

```java
// strings/InfiniteRecursion.java 
// Accidental recursion 
// {ThrowsException} 
// {VisuallyInspectOutput} Throws very long exception
import java.util.*;
import java.util.stream.*;

public class InfiniteRecursion { 
    @Override 
    public String toString() { 
        return " InfiniteRecursion address: " + this + "\n"
    } 
    public static void main(String[] args) { 
        Stream.generate(InfiniteRecursion::new) 
            .limit(10) 
            .forEach(System.out::println); 
    } 
} 

```

当你创建了 `InfiniteRecursion` 对象，并将其打印出来的时候，你会得到一串很长的异常信息。如果你将该 `InfiniteRecursion` 对象存入一个 `ArrayList` 中，然后打印该 `ArrayList`，同样也会抛出异常。其实，当运行到如下代码时：

```java
"InfiniteRecursion address: " + this 

```

这里发生了自动类型转换，由 `InfiniteRecursion` 类型转换为 `String` 类型。因为编译器发现一个 `String` 对象后面跟着一个 “+”，而 “+” 后面的对象不是 `String`，于是编译器试着将 `this` 转换成一个 `String`。它怎么转换呢？正是通过调用 `this` 上的 `toString()` 方法，于是就发生了递归调用。

<!-- Operations on Strings -->

## 字符串操作

以下是 `String` 对象具备的一些基本方法。重载的方法归纳在同一行中：

| 方法                                   | 参数，重载版本                                               | 作用                                                         |
| -------- | -------------------------------------- | ------------------------------------------------------------ |
| 构造方法                               | 默认版本，`String`，`StringBuilder`，<br/>`StringBuffer`，`char`数组，`byte`数组 | 创建`String`对象                                             |
| `length()`                             |                                                              | `String`中字符的个数                                         |
| `charAt()`                             | `int`索引                                                    | 获取`String`中索引位置上的`char`                             |
| `getChars()`，<br/>`getBytes()`       | 待复制部分的开始和结束索引，复制的目标数组<br/>，目标数组的开始索引 | 复制`char`或`byte`到一个目标数组中                           |
| `toCharArray()`                        |                                                              | 生成一个`char[]`，包含`String`中的所有字符                   |
| `equals()`，<br/>`equalsIgnoreCase()`  | 与之进行比较的`String`                                       | 比较两个`String`的内容是否相同。如果相同，结果为`true`       |
| `compareTo()`<br/>，`compareToIgnoreCase()` | 与之进行比较的`String`                                       | 按词典顺序比较`String`的内容，比较结果为负数、零或正数。注意，大小写不等价 |
| `contains()`                           | 要搜索的`CharSequence`                                       | 如果该`String`对象包含参数的内容，则返回`true`               |
| `contentEquals()`                      | 与之进行比较的`CharSequence`或`StringBuffer`                 | 如果该`String`对象与参数的内容完全一致，则返回`true`         |
| `isEmpty()`                            |                                                              | 返回`boolean`结果，以表明`String`对象的长度是否为0           |
| `regionMatches()`                      | 该`String`的索引偏移量，另一个`String`及<br/>其索引偏移量，要比较的长度。重载版本增加<br/>了“忽略大小写”功能 | 返回`boolean`结果，以表明所比较区域是否相等                  |
| `startsWith()`                         | 可能的起始`String`。重载版本在参数中增加<br/>了偏移量        | 返回`boolean`结果，以表明该`String`是否以传入参数开始        |
| `endsWith()`                           | 该`String`可能的后缀`String`                                 | 返回`boolean`结果，以表明此参数是否是该字符串的后缀          |
| `indexOf()`<br/>，`lastIndexOf()`      | 重载版本包括：`char`，`char`与起始索引，`String`，`String`与起始索引 | 如果该`String`并不包含此参数，就返回-1；否则返回此参数在`String`中的起始索引。`lastIndexOf`()是从后往前搜索 |
| `matches()`                            | 一个正则表达式                                               | 返回`boolean`结果，以表明该`String`和给出的正则表达式是否匹配 |
| `split()`                              | 一个正则表达式。可选参数为需要拆分的最大数量                 | 按照正则表达式拆分`String`，返回一个结果数组                 |
| `join()`（Java8引入的）                | 分隔符，待拼字符序列。用分隔符将字符序列<br/>拼接成一个新的`String` | 用分隔符拼接字符片段，产生一个新的`String`                   |
| `substring()`<br/>（即`subSequence()`） | 重载版本：起始索引；起始索引+终止索引                        | 返回一个新的`String`对象，以包含参数指定的子串               |
| `concat()`                             | 要连接的`String`                                             | 返回一个新的`String`对象，内容为原始`String`连接上参数`String` |
| `replace()`                            | 要替换的字符，用来进行替换的新字符。<br/>也可以用一个`CharSequence`替换<br/>另一个`CharSequence` | 返回替换字符后的新`String`对象。如果没有替换发生，则返回原始的`String`对象 |
| `replaceFirst()`                       | 要替换的正则表达式，用来进行替换的`String`                   | 返回替换首个目标字符串后的`String`对象                       |
| `replaceAll()`                         | 要替换的正则表达式，用来进行替换的`String`                   | 返回替换所有目标字符串后的`String`对象                       |
| `toLowerCase()`，<br/>`toUpperCase()`  |                                                              | 将字符的大小写改变后，返回一个新的`String`对象。如果没有任何改变，则返回原始的`String`对象 |
| `trim()`                               |                                                              | 将`String`两端的空白符删除后，返回一个新的`String`对象。如果没有任何改变，则返回原始的`String`对象 |
| `valueOf()`<br/>（`static`）           | 重载版本：`Object`；`char[]`；`char[]`，<br/>偏移量，与字符个数；`boolean`；`char`<br/>；`int`；`long`；`float`；`double` | 返回一个表示参数内容的`String`                               |
| `intern()`                             |                                                              | 为每个唯一的字符序列生成一个且仅生成一个`String`引用         |
| `format()`                             | 要格式化的字符串，要替换到格式化字符串的参数                 | 返回格式化结果`String`                                       |

从这个表可以看出，当需要改变字符串的内容时，`String` 类的方法都会返回一个新的 `String` 对象。同时，如果内容不改变，`String` 方法只是返回原始对象的一个引用而已。这可以节约存储空间以及避免额外的开销。

本章稍后还将介绍正则表达式在 `String` 方法中的应用。

<!-- Formatting Output -->

## 格式化输出

在长久的等待之后，Java SE5 终于推出了 C 语言中 `printf()` 风格的格式化输出这一功能。这不仅使得控制输出的代码更加简单，同时也给与Java开发者对于输出格式与排列更强大的控制能力。

### `printf()`

C 语言的 `printf()` 并不像 Java 那样连接字符串，它使用一个简单的格式化字符串，加上要插入其中的值，然后将其格式化输出。 `printf()` 并不使用重载的 `+` 操作符（C语言没有重载）来连接引号内的字符串或字符串变量，而是使用特殊的占位符来表示数据将来的位置。而且它还将插入格式化字符串的参数，以逗号分隔，排成一行。例如：

```c
System.out.printf("Row 1: [%d %f]%n", x, y);
```

这一行代码在运行的时候，首先将 `x` 的值插入到 `%d_` 的位置，然后将 `y` 的值插入到 `%f` 的位置。这些占位符叫做*格式修饰符*，它们不仅指明了插入数据的位置，同时还指明了将会插入什么类型的变量，以及如何格式化。在这个例子中 **`%d` 表示 `x` 是一个整数，`%f` 表示 `y` 是一个浮点数**（`float` 或者 `double`）。

### `System.out.format()`

Java SE5 引入了 `format()` 方法，可用于 `PrintStream` 或者 `PrintWriter` 对象（你可以在 [附录:流式 I/O](./Appendix-IO-Streams.md) 了解更多内容），其中也包括 `System.out` 对象。`format()` 方法模仿了 C 语言的 `printf()`。如果你比较怀旧的话，也可以使用 `printf()`。以下是一个简单的示例：

```java
// strings/SimpleFormat.java 

public class SimpleFormat {   
    public static void main(String[] args) {     
        int x = 5;     
        double y = 5.332542;     
        // The old way: 
        System.out.println("Row 1: [" + x + " " + y + "]");     
        // The new way:     
        System.out.format("Row 1: [%d %f]%n", x, y);     
        // or     
        System.out.printf("Row 1: [%d %f]%n", x, y);   
    } 
} 
/* Output: 
Row 1: [5 5.332542] 
Row 1: [5 5.332542] 
Row 1: [5 5.332542] 
*/

```

可以看到，**`format()` 和  `printf()` 是等价的**，它们只需要一个简单的格式化字符串，加上一串参数即可，每个参数对应一个格式修饰符。

`String` 类也有一个 `static format()` 方法，可以格式化字符串。

### `Formatter` 类

**在 Java 中，所有的格式化功能都是由 `java.util.Formatter` 类处理的**。可以将 `Formatter` 看做一个翻译器，它将你的格式化字符串与数据翻译成需要的结果。当你创建一个 `Formatter` 对象时，需要向其构造器传递一些信息，告诉它最终的结果将向哪里输出：

```java
// strings/Turtle.java 
import java.io.*;
import java.util.*;

public class Turtle {   
    private String name;   
    private Formatter f;  
    public Turtle(String name, Formatter f) {
        this.name = name;     
        this.f = f;   
    }   
    public void move(int x, int y) {     
        f.format("%s The Turtle is at (%d,%d)%n",       
            name, x, y);   
    }
    public static void main(String[] args) {    
        PrintStream outAlias = System.out;     
        Turtle tommy = new Turtle("Tommy",
            new Formatter(System.out));     
        Turtle terry = new Turtle("Terry",       
            new Formatter(outAlias));     
        tommy.move(0,0);     
        terry.move(4,8);     
        tommy.move(3,4);     
        terry.move(2,5);     
        tommy.move(3,3);     
        terry.move(3,3);   
    } 
} 
/* Output: 
Tommy The Turtle is at (0,0) 
Terry The Turtle is at (4,8) 
Tommy The Turtle is at (3,4) 
Terry The Turtle is at (2,5) 
Tommy The Turtle is at (3,3) 
Terry The Turtle is at (3,3) 
*/

```

**格式化修饰符 `%s` 表明这里需要 `String` 参数。**

所有的 `tommy` 都将输出到 `System.out`，而所有的 `terry` 则都输出到 `System.out` 的一个别名中。`Formatter` 的重载构造器支持输出到多个路径，不过最常用的还是 `PrintStream()`（如上例）、`OutputStream` 和 `File`。你可以在 [附录:流式 I/O](././Appendix-IO-Streams.md) 中了解更多信息。

### 格式化修饰符

在插入数据时，如果想要优化空格与对齐，你需要更精细复杂的格式修饰符。以下是其通用语法：

```java
%[argument_index$][flags][width][.precision]conversion 
```

最常见的应用是控制一个字段的最小长度，这可以通过指定 *width* 来实现。`Formatter `对象通过在必要时添加空格，来确保一个字段至少达到设定长度。默认情况下，数据是右对齐的，不过可以通过使用 `-` 标志来改变对齐方向。

与 *width* 相对的是 *precision*，用于指定最大长度。*width* 可以应用于各种类型的数据转换，并且其行为方式都一样。*precision* 则不然，当应用于不同类型的数据转换时，*precision* 的意义也不同。在将 *precision* 应用于 `String` 时，它表示打印 `string` 时输出字符的最大数量。而在将 *precision* 应用于浮点数时，它表示小数部分要显示出来的位数（默认是 6 位小数），如果小数位数过多则舍入，太少则在尾部补零。由于整数没有小数部分，所以 *precision* 无法应用于整数，如果你对整数应用 *precision*，则会触发异常。

下面的程序应用格式修饰符来打印一个购物收据。这是 *Builder* 设计模式的一个简单实现，即先创建一个初始对象，然后逐渐添加新东西，最后调用 `build()` 方法完成构建：

```java
// strings/ReceiptBuilder.java 
import java.util.*; 

public class ReceiptBuilder {   
    private double total = 0;   
    private Formatter f =     
        new Formatter(new StringBuilder());   
    public ReceiptBuilder() {     
        f.format(       
          "%-15s %5s %10s%n", "Item", "Qty", "Price");     
        f.format(       
          "%-15s %5s %10s%n", "----", "---", "-----");   
        }   
    public void add(String name, int qty, double price) {     
        f.format("%-15.15s %5d %10.2f%n", name, qty, price);     
        total += price * qty;   
    }  
    public String build() {     
        f.format("%-15s %5s %10.2f%n", "Tax", "",       
          total * 0.06);     
        f.format("%-15s %5s %10s%n", "", "", "-----");     
        f.format("%-15s %5s %10.2f%n", "Total", "",       
          total * 1.06);     
        return f.toString();   
    }   
    public static void main(String[] args) {     
        ReceiptBuilder receiptBuilder =       
          new ReceiptBuilder();     
        receiptBuilder.add("Jack's Magic Beans", 4, 4.25);     
        receiptBuilder.add("Princess Peas", 3, 5.1);     
        receiptBuilder.add(       
          "Three Bears Porridge", 1, 14.29);     
        System.out.println(receiptBuilder.build());   
    } 
} 
/* Output: 
Item              Qty      Price 
----              ---      ----- 
Jack's Magic Be     4       4.25 
Princess Peas       3       5.10 
Three Bears Por     1      14.29 
Tax                         2.80 
                           ----- 
Total                      49.39 
*/ 

```

通过传入一个 `StringBuilder` 对象到 `Formatter` 的构造器，我们指定了一个容器来构建目标 `String`。你也可以通过不同的构造器参数，把结果输出到标准输出，甚至是一个文件里。

正如你所见，通过相当简洁的语法，`Formatter ` 提供了对空格与对齐的强大控制能力。在该程序中，为了恰当地控制间隔，格式化字符串被重复利用了多遍。

### `Formatter` 转换

下面的表格展示了最常用的类型转换：

| 类型 | 含义               |
| :--: | :----------------- |
| `d`  | 整型（十进制）     |
| `c`  | Unicode字符        |
| `b`  | Boolean值          |
| `s`  | String             |
| `f`  | 浮点数（十进制）   |
| `e`  | 浮点数（科学计数） |
| `x`  | 整型（十六进制）   |
| `h`  | 散列码（十六进制） |
| `%`  | 字面值“%”          |

下面的程序演示了这些转换是如何工作的：

```java
// strings/Conversion.java 
import java.math.*;
import java.util.*; 

public class Conversion {   
    public static void main(String[] args) {     
        Formatter f = new Formatter(System.out); 

        char u = 'a';     
        System.out.println("u = 'a'");     
        f.format("s: %s%n", u);     
        // f.format("d: %d%n", u);     
        f.format("c: %c%n", u);     
        f.format("b: %b%n", u);     
        // f.format("f: %f%n", u);     
        // f.format("e: %e%n", u);     
        // f.format("x: %x%n", u);     
        f.format("h: %h%n", u); 

        int v = 121;     
        System.out.println("v = 121");    
        f.format("d: %d%n", v);     
        f.format("c: %c%n", v);     
        f.format("b: %b%n", v);     
        f.format("s: %s%n", v);     
        // f.format("f: %f%n", v);     
        // f.format("e: %e%n", v);     
        f.format("x: %x%n", v);     
        f.format("h: %h%n", v); 

        BigInteger w = new BigInteger("50000000000000");     
        System.out.println(       
          "w = new BigInteger(\"50000000000000\")");     
        f.format("d: %d%n", w);     
        // f.format("c: %c%n", w);     
        f.format("b: %b%n", w);     
        f.format("s: %s%n", w);     
        // f.format("f: %f%n", w);     
        // f.format("e: %e%n", w);     
        f.format("x: %x%n", w);     
        f.format("h: %h%n", w); 

        double x = 179.543;     
        System.out.println("x = 179.543");     
        // f.format("d: %d%n", x);     
        // f.format("c: %c%n", x);     
        f.format("b: %b%n", x);     
        f.format("s: %s%n", x);     
        f.format("f: %f%n", x);     
        f.format("e: %e%n", x);     
        // f.format("x: %x%n", x);     
        f.format("h: %h%n", x); 

        Conversion y = new Conversion();     
        System.out.println("y = new Conversion()"); 

        // f.format("d: %d%n", y);     
        // f.format("c: %c%n", y);     
        f.format("b: %b%n", y);     
        f.format("s: %s%n", y);     
        // f.format("f: %f%n", y);     
        // f.format("e: %e%n", y);     
        // f.format("x: %x%n", y);     
        f.format("h: %h%n", y); 

        boolean z = false;     
        System.out.println("z = false");     
        // f.format("d: %d%n", z);     
        // f.format("c: %c%n", z);     
        f.format("b: %b%n", z);     
        f.format("s: %s%n", z);     
        // f.format("f: %f%n", z);     
        // f.format("e: %e%n", z);     
        // f.format("x: %x%n", z);     
        f.format("h: %h%n", z);   
    } 
} 
```

被注释的代码表示，针对相应类型的变量，这些转换是无效的。如果执行这些转换，则会触发异常。

注意，程序中的每个变量都用到了 `b` 转换。虽然它对各种类型都是合法的，但其行为却不一定与你想象的一致。**对于 `boolean` 基本类型或 `Boolean` 对象，其转换结果是对应的 `true` 或 `false`。但是，==对其他类型的参数，只要该参数不为 `null`，其转换结果永远都是 `true`。==即使是数字 0，转换结果依然为 `true`，而这**在其他语言中（包括C），往往转换为 `false`。所以，将 `b` 应用于非布尔类型的对象时请格外小心。

还有许多不常用的类型转换与格式修饰符选项，你可以在 JDK 文档中的 `Formatter` 类部分找到它们。

### `String.format()`

Java SE5 也参考了 C 中的 `sprintf()` 方法，以生成格式化的 `String` 对象。`String.format()` 是一个 `static` 方法，它接受与 `Formatter.format()` 方法一样的参数，但返回一个 `String` 对象。**当你只需使用一次 `format()` 方法的时候，`String.format()` 用起来很方便。**例如：

```java
// strings/DatabaseException.java 

public class DatabaseException extends Exception {   
    public DatabaseException(int transactionID,     
      int queryID, String message) {     
      super(String.format("(t%d, q%d) %s", transactionID,         
        queryID, message));   
    }   
    public static void main(String[] args) {     
      try {       
        throw new DatabaseException(3, 7, "Write failed");     
      } catch(Exception e) {       
        System.out.println(e);     
      }   
    } 
} 
/* 
Output: 
DatabaseException: (t3, q7) Write failed 
*/

```

其实在 `String.format()` 内部，它也是创建了一个 `Formatter` 对象，然后将你传入的参数转给 `Formatter`。不过，与其自己做这些事情，不如使用便捷的 `String.format()` 方法，何况这样的代码更清晰易读。

#### 一个十六进制转储（dump）工具

在第二个例子中，我们把二进制文件转换为十六进制格式。下面的小工具使用了 `String.format()` 方法，以可读的十六进制格式将字节数组打印出来：

```java
// strings/Hex.java 
// {java onjava.Hex} 
package onjava;
import java.io.*; 
import java.nio.file.*; 

public class Hex {   
    public static String format(byte[] data) {     
        StringBuilder result = new StringBuilder();     
        int n = 0;     
        for(byte b : data) {       
            if(n % 16 == 0)         
                result.append(String.format("%05X: ", n));       
            result.append(String.format("%02X ", b));       
            n++;       
            if(n % 16 == 0) result.append("\n");     
        }     
        result.append("\n");     
        return result.toString();   
    }   
    public static void main(String[] args) throws Exception {  
        if(args.length == 0)       
            // Test by displaying this class file:       
            System.out.println(format(         
                Files.readAllBytes(Paths.get(           
                  "build/classes/main/onjava/Hex.class"))));     
        else       
            System.out.println(format(         
                Files.readAllBytes(Paths.get(args[0]))));   
    } 
} 
/* Output: (First 6 Lines) 
00000: CA FE BA BE 00 00 00 34 00 61 0A 00 05 00 31 07 
00010: 00 32 0A 00 02 00 31 08 00 33 07 00 34 0A 00 35 
00020: 00 36 0A 00 0F 00 37 0A 00 02 00 38 08 00 39 0A 
00030: 00 3A 00 3B 08 00 3C 0A 00 02 00 3D 09 00 3E 00 
00040: 3F 08 00 40 07 00 41 0A 00 42 00 43 0A 00 44 00 
00050: 45 0A 00 14 00 46 0A 00 47 00 48 07 00 49 01 00
                  ... 
*/
```

为了打开及读入二进制文件，我们用到了另一个工具 `Files.readAllBytes()`，这已经在 [Files章节](./17-Files.md) 介绍过了。这里的 `readAllBytes()` 方法将整个文件以 `byte` 数组的形式返回。

<!-- Regular Expressions -->

## 正则表达式

注：特殊字符，如`+`,要写成`\\+`

`+`,`\`,`.`,`(`,

**在正则表达式中，用括号将表达式进行分组，用竖线 ` | ` 表示或操作。**

很久之前，*正则表达式*就已经整合到标准 Unix 工具集之中，例如 sed、awk 和程序语言之中了，如 Python 和Perl（有些人认为正是正则表达式促成了 Perl 的成功）。

正则表达式是一种强大而灵活的文本处理工具。使用正则表达式，我们能够以编程的方式，构造复杂的文本模式，并对输入 `String` 进行搜索。一旦找到了匹配这些模式的部分，你就能随心所欲地对它们进行处理。初学正则表达式时，其语法是一个难点，但它确实是一种简洁、动态的语言。正则表达式提供了一种完全通用的方式，能够解决各种 `String` 处理相关的问题：匹配、选择、编辑以及验证。

### 基础

一般来说，正则表达式就是以某种方式来描述字符串，因此你可以说：“如果一个字符串含有这些东西，那么它就是我正在找的东西。”例如，要找一个数字，它可能有一个负号在最前面，那你就写一个负号加上一个问号，就像这样：

```java
-?
```

要描述一个整数，你可以说它有一位或多位阿拉伯数字。在正则表达式中，用 `\d` 表示一位数字。如果在其他语言中使用过正则表达式，那你可能就能发现 Java 对反斜线 \ 的不同处理方式。在其他语言中，`\\` 表示“我想要在正则表达式中插入一个普通的（字面上的）反斜线，请不要给它任何特殊的意义。”而在Java中**，`\\` 的意思是“我要插入一个正则表达式的反斜线**，所以其后的字符具有特殊的意义。”例如，如果你想表示一位数字，那么正则表达式应该是 `\\d`。**如果你想插入一个普通的反斜线，应该这样写 `\\\`。**不过换行符和制表符之类的东西只需要使用单反斜线：`\n\t`。 [^2]

要表示“一个或多个之前的表达式”，应该使用 `+`。所以，如果要表示“可能有一个负号，后面跟着一位或多位数字”，可以这样：

```java
-?\\d+ 
```

应用正则表达式最简单的途径，就是利用 `String` 类内建的功能。例如，你可以检查一个 `String` 是否匹配如上所述的正则表达式：

```java
// strings/IntegerMatch.java 

public class IntegerMatch {  
    public static void main(String[] args) {     
        System.out.println("-1234".matches("-?\\d+"));    
        System.out.println("5678".matches("-?\\d+"));     
        System.out.println("+911".matches("-?\\d+"));     
        System.out.println("+911".matches("(-|\\+)?\\d+"));   
    }
}
/* Output: 
true 
true 
false 
true 
*/ 
```

前两个字符串都满足对应的正则表达式，匹配成功。第三个字符串以 `+` 开头，这也是一个合法的符号，但与对应的正则表达式却不匹配。因此，我们的正则表达式应该描述为：“可能以一个加号或减号开头”。**==在正则表达式中，用括号将表达式进行分组，用竖线 ` | ` 表示或操作==**。也就是：

```java
(-|\\+)? 
```

这个正则表达式表示字符串的起始字符可能是一个 `-` 或 `+`，**或者二者都没有（因为后面跟着 `?` 修饰符）**。因为字符 `+` 在正则表达式中有特殊的意义，所以必须使用 `\\` 将其转义，使之成为表达式中的一个普通字符。

**`String`类还自带了一个非常有用的正则表达式工具——`split()` 方法**，其功能是“将字符串从正则表达式匹配的地方切开。”

```java
// strings/Splitting.java import java.util.*; 

public class Splitting {
    public static String knights =   
      "Then, when you have found the shrubbery, " +
      "you must cut down the mightiest tree in the " +
      "forest...with... a herring!";
    public static void split(String regex) {
        System.out.println(
          Arrays.toString(knights.split(regex)));
        }
    public static void main(String[] args) {
        split(" "); // Doesn't have to contain regex chars
        split("\\W+"); // Non-word characters
        split("n\\W+"); // 'n' followed by non-words
    }
}
/* Output:
[Then,, when, you, have, found, the, shrubbery,, you,
must, cut, down, the, mightiest, tree, in, the,
forest...with..., a, herring!]
[Then, when, you, have, found, the, shrubbery, you,
must, cut, down, the, mightiest, tree, in, the, forest,
with, a, herring]
[The, whe, you have found the shrubbery, you must cut
dow, the mightiest tree i, the forest...with... a
herring!]
*/
```

首先看第一个语句，注意这里用的是普通的字符作为正则表达式，其中并不包含任何特殊字符。因此第一个 `split()` 只是按空格来划分字符串。

第二个和第三个 `split()` 都用到了 **`\\W`，它的意思是一个非单词字符（如果 W 小写，`\\w`，则表示一个单词字符）**。通过第二个例子可以看到，它将标点字符删除了。第三个 `split()` 表示“字母 `n` 后面跟着一个或多个非单词字符。”可以看到，在原始字符串中，与正则表达式匹配的部分，在最终结果中都不存在了。

`String.split()` 还有一个重载的版本，它允许你限制字符串分割的次数。

用正则表达式进行替换操作时，你可以只替换第一处匹配，也可以替换所有的匹配：

```java
// strings/Replacing.java 

public class Replacing {
    static String s = Splitting.knights;   
    public static void main(String[] args) {
        System.out.println(
          s.replaceFirst("f\\w+", "located"));
        System.out.println(       
          s.replaceAll("shrubbery|tree|herring","banana"));   
    } 
}
/* Output: 
Then, when you have located the shrubbery, you must cut 
down the mightiest tree in the forest...with... a 
herring! 
Then, when you have found the banana, you must cut down
the mightiest banana in the forest...with... a banana! 
*/

```

第一个表达式要匹配的是，以字母 `f` 开头，后面跟一个或多个字母（注意这里的 `w` 是小写的）。并且只替换掉第一个匹配的部分，所以 “found” 被替换成 “located”。

第二个表达式要匹配的是三个单词中的任意一个，因为它们以竖线分割表示“或”，并且替换所有匹配的部分。

稍后你会看到，`String` 之外的正则表达式还有更强大的替换工具，例如，可以通过方法调用执行替换。而且，如果正则表达式不是只使用一次的话，非 `String` 对象的正则表达式明显具备更佳的性能。

### String 类的正则方法

| name           | useage |
| -------------- | ------ |
| matches        |        |
| split()        |        |
| replaceFirst() |        |
| replaceAll     |        |
|                |        |

### 创建正则表达式

我们首先从正则表达式可能存在的构造集中选取一个很有用的子集，以此开始学习正则表达式。正则表达式的完整构造子列表，请参考JDK文档 `java.util.regex` 包中的 `Pattern`类。

| 表达式   | 含义                                |
| :------- | :---------------------------------- |
| `B`      | 指定字符`B`                         |
| `\xhh`   | 十六进制值为`0xhh`的字符            |
| `\uhhhh` | 十六进制表现为`0xhhhh`的Unicode字符 |
| `\t`     | 制表符Tab                           |
| `\n`     | 换行符                              |
| `\r`     | 回车                                |
| `\f`     | 换页                                |
| `\e`     | 转义（Escape）                      |

当你学会了使用字符类（character classes）之后，正则表达式的威力才能真正显现出来。以下是一些创建字符类的典型方式，以及一些预定义的类：

| 表达式         | 含义                                                         |
| :------------- | :----------------------------------------------------------- |
| `.`            | 任意字符                                                     |
| `[abc]`        | 包含`a`、`b`或`c`的任何字符（和`a|b|c`作用相同）             |
| `[^abc]`       | 除`a`、`b`和`c`之外的任何字符**（否定）**                    |
| `[a-zA-Z]`     | 从`a`到`z`或从`A`到`Z`的任何字符（范围）                     |
| `[abc[hij]]`   | `a`、`b`、`c`、`h`、`i`、`j`中的任意字符（与`a|b|c|h|i|j`作用相同）（合并） |
| `[a-z&&[hij]]` | 任意`h`、`i`或`j`（交）                                      |
| `\s`           | 空白符（空格、tab、换行、换页、回车）                        |
| `\S`           | 非空白符（`[^\s]`）                                          |
| `\d`           | 数字（`[0-9]`）                                              |
| `\D`           | 非数字（`[^0-9]`）                                           |
| `\w`           | 词字符（`[a-zA-Z_0-9]`）                                     |
| `\W`           | 非词字符（`[^\w]`）                                          |

这里只列出了部分常用的表达式，你应该将JDK文档中 `java.util.regex.Pattern` 那一页加入浏览器书签中，以便在需要的时候方便查询。

| 逻辑操作符 | 含义                                                         |
| :--------: | :----------------------------------------------------------- |
|    `XY`    | `Y`跟在`X`后面                                               |
|   `X|Y`    | `X`或`Y`                                                     |
|   `(X)`    | 捕获组（capturing group）。可以在表达式中用`\i`引用第i个捕获组 |

下面是不同的边界匹配符：

| 边界匹配符 | 含义             |
| :--------: | :--------------- |
|    `^`     | 一行的开始       |
|    `$`     | 一行的结束       |
|    `\b`    | 词的边界         |
|    `\B`    | 非词的边界       |
|    `\G`    | 前一个匹配的结束 |

作为演示，下面的每一个正则表达式都能成功匹配字符序列“Rudolph”：

```java
// strings/Rudolph.java 

public class Rudolph {   
    public static void main(String[] args) {     
        for(String pattern : new String[]{       
          "Rudolph",       
          "[rR]udolph",       
          "[rR][aeiou][a-z]ol.*",       
          "R.*" })       
        System.out.println("Rudolph".matches(pattern));   
    } 
} 
/* Output: 
true 
true 
true 
true 
*/

```

我们的目的并不是编写最难理解的正则表达式，而是尽量编写能够完成任务的、最简单以及最必要的正则表达式。一旦真正开始使用正则表达式了，你就会发现，在编写新的表达式之前，你通常会参考代码中已经用到的正则表达式。

### 量词

```java
正则?：表示正则可以出现0次或1次 {0,1}  
正则+：表示正则可以出现1次或1次以上 >=1 {1,}  
正则*：表示正则可以出现0次或1次或多次 >= 0 {0,}  
正则{n}：表示正则正好出现n次  
正则{n,}：表示正则出现n次及以上  
正则{n,m}：表示正则出现{n,m}次 
```
量词描述了一个模式捕获输入文本的方式：

- **贪婪型**：
  量词总是贪婪的，除非有其他的选项被设置。贪婪表达式会为所有可能的模式发现尽可能多的匹配。导致此问题的一个典型理由就是假定我们的模式仅能匹配第一个可能的字符组，如果它是贪婪的，那么它就会继续往下匹配。
- **勉强型**：
  用问号来指定，这个量词匹配**满足模式所需的最少字符数。**因此也被称作懒惰的、最少匹配的、非贪婪的或不贪婪的。
- **占有型**：
  目前，这种类型的量词只有在 Java 语言中才可用（在其他语言中不可用），并且也更高级，因此我们大概不会立刻用到它。当正则表达式被应用于 `String` 时，它会产生相当多的状态，以便在匹配失败时可以回溯。而“占有的”量词并不保存这些中间状态，因此**它们可以防止回溯。**它们常常用于防止正则表达式失控，因此可以使正则表达式执行起来更高效。

| 贪婪型   | 勉强型    | 占有型    | 如何匹配                    |
| -------- | --------- | --------- | --------------------------- |
| `X?`     | `X??`     | `X?+`     | 一个或零个`X`               |
| `X*`     | `X*?`     | `X*+`     | 零个或多个`X`               |
| `X+`     | `X+?`     | `X++`     | 一个或多个`X`               |
| `X{n}`   | `X{n}?`   | `X{n}+`   | 恰好`n`次`X`                |
| `X{n,}`  | `X{n,}?`  | `X{n,}+`  | 至少`n`次`X`                |
| `X{n,m}` | `X{n,m}?` | `X{n,m}+` | `X`至少`n`次，但不超过`m`次 |

应该非常清楚地意识到，**表达式 `X` 通常必须要用圆括号括起来**，以便它能够按照我们期望的效果去执行。例如：

```java
abc+
```

看起来它似乎应该匹配1个或多个`abc`序列，如果我们把它应用于输入字符串`abcabcabc`，则实际上会获得3个匹配。然而，这个表达式实际上表示的是：匹配`ab`，后面跟随1个或多个`c`。要表明匹配1个或多个完整的字符串`abc`，我们必须这样表示：

```java
(abc)+
```

你会发现，在使用正则表达式时很容易混淆，因为它是一种在 Java 之上的新语言。

### `CharSequence`

接口 `CharSequence` 从 `CharBuffer`、`String`、`StringBuffer`、`StringBuilder` 类中抽象出了字符序列的一般化定义：

```java
interface CharSequence {   
    char charAt(int i);   
    int length();
    CharSequence subSequence(int start, int end);
    String toString(); 
}
```

因此，这些类都实现了该接口。**多数正则表达式操作都接受 `CharSequence` 类型参数。**

### `Pattern` 和 `Matcher`

**==注意：==**获得的matcher的group()对象需要使用find()，即使是使用group(1)

```java
String fileName = "input10.txt";
System.out.println(fileName);
Pattern p = Pattern.compile("\\d+");
Matcher m = p.matcher(fileName);
Pattern p = Pattern.compile(arg);       
Matcher m = p.matcher(args[0]);       
while(m.find()) {         
    System.out.println(           
        "Match \"" + m.group() + "\" at positions " +           
        m.start() + "-" + (m.end() - 1));       
} 
```

```java
String fileName = "input10.txt";
        System.out.println(fileName);
        Pattern p = Pattern.compile("input(\\d+).txt");
        Matcher m = p.matcher(fileName);
        if (m.find())
            System.out.print(m.group(1) + " ");
```

通常，比起功能有限的 `String` 类，我们更愿意构造功能强大的正则表达式对象。只需导入 `java.util.regex`包，然后**用 `static Pattern.compile()` 方法来编译你的正则表达式**即可。它会根据你的 `String` 类型的正则表达式生成一个 `Pattern` 对象。接下来，把你想要检索的**字符串传入 `Pattern` 对象的 `matcher()` 方法。**`matcher()` 方法会生成一个 `Matcher` 对象，它有很多功能可用（可以参考 `java.util.regext.Matcher` 的 JDK 文档）。例如，它的 `replaceAll()` 方法能将所有匹配的部分都替换成你传入的参数。

作为第一个示例，下面的类可以用来测试正则表达式，看看它们能否匹配一个输入字符串。第一个控制台参数是将要用来搜索匹配的输入字符串，后面的一个或多个参数都是正则表达式，它们将被用来在输入的第一个字符串中查找匹配。在Unix/Linux上，命令行中的正则表达式必须用引号括起来。这个程序在测试正则表达式时很有用，特别是当你想验证它们是否具备你所期待的匹配功能的时候。[^3]

```java
// strings/TestRegularExpression.java 
// Simple regular expression demonstration 
// {java TestRegularExpression 
// abcabcabcdefabc "abc+" "(abc)+" } 
import java.util.regex.*; 

public class TestRegularExpression {
    public static void main(String[] args) {     
        if(args.length < 2) {     
            System.out.println(       
              "Usage:\njava TestRegularExpression " +         
              "characterSequence regularExpression+");      
            System.exit(0);    
        }
        System.out.println("Input: \"" + args[0] + "\"");     
        for(String arg : args) {       
            System.out.println(         
              "Regular expression: \"" + arg + "\"");       
            Pattern p = Pattern.compile(arg);       
            Matcher m = p.matcher(args[0]);       
            while(m.find()) {         
                System.out.println(           
                  "Match \"" + m.group() + "\" at positions " +           
                m.start() + "-" + (m.end() - 1));       
            }     
        }  
    }
}
/* Output: 
Input: "abcabcabcdefabc" 
Regular expression: "abcabcabcdefabc" 
Match "abcabcabcdefabc" at positions 0-14 
Regular expression: "abc+" 
Match "abc" at positions 0-2 
Match "abc" at positions 3-5 
Match "abc" at positions 6-8 
Match "abc" at positions 12-14 
Regular expression: "(abc)+"
Match "abcabcabc" at positions 0-8 
Match "abc" at positions 12-14 
*/
```

还可以在控制台参数中加入`“(abc){2,}”`，看看执行结果。

#### Pattern

```java
Matcher	matcher(CharSequence input)	
Creates a matcher that will match the given input against this pattern.
static boolean	matches(String regex, CharSequence input)	
Compiles the given regular expression and attempts to match the given input against it.
String[]	split(CharSequence input)	
Splits the given input sequence around matches of this pattern.
String[]	split(CharSequence input, int limit)	
Splits the given input sequence around matches of this pattern.
```

**`Pattern` 对象表示编译后的正则表达式。**从这个例子可以看到，我们使用已编译的 `Pattern` 对象上的 `matcher()` 方法，加上一个输入字符串，从而共同构造了一个 `Matcher` 对象。同时，`Pattern` 类还提供了一个`static`方法：

```java
static boolean matches(String regex, CharSequence input)
```

该方法用以检查 `regex` 是否匹配整个 `CharSequence` 类型的 `input` 参数。编译后的 `Pattern` 对象还提供了 `split()` 方法，它从匹配了 `regex` 的地方分割输入字符串，返回分割后的子字符串 `String` 数组。

通过调用 `Pattern.matcher()` 方法，并传入一个字符串参数，我们得到了一个 `Matcher` 对象。使用 `Matcher` 上的方法，我们将能够判断各种不同类型的匹配是否成功：

| funcition               | useage                                                       |
| ----------------------- | ------------------------------------------------------------ |
| boolean matches()       | `matches()` 方法用来判断整个输入字符串是否匹配正则表达式模式 |
| boolean lookingAt()     | `lookingAt()` 则用来判断该字符串（不必是整个字符串）的**起始部分**是否能够匹配模式。 |
| boolean find()          |                                                              |
| boolean find(int start) | @param start the index to start searching for a match        |

### `find()`

`Matcher.find()` 方法可用来在 `CharSequence` 中查找多个匹配。例如：

```java
// strings/Finding.java 
import java.util.regex.*; 

public class Finding {   
    public static void main(String[] args) {     
        Matcher m = Pattern.compile("\\w+")       
          .matcher(         
            "Evening is full of the linnet's wings");     
        while(m.find())       
            System.out.print(m.group() + " ");   
        System.out.println();     
        int i = 0;     
        while(m.find(i)) {       
            System.out.print(m.group() + " ");       
            i++;     
        }   
    }
}
/* Output: 
Evening is full of the linnet s wings
Evening vening ening ning ing ng g is is s full full 
ull ll l of of f the the he e linnet linnet innet nnet 
net et t s s wings wings ings ngs gs s 
*/
```

模式 `\\w+` 将字符串划分为词。`find()` 方法像迭代器那样向前遍历输入字符串。**而第二个重载的 `find()` 接收一个整型参数，该整数表示字符串中字符的位置，并以其作为搜索的起点。**从结果可以看出，后一个版本的 `find()` 方法能够根据其参数的值，不断重新设定搜索的起始位置。

### 组（Groups）

组是用括号划分的正则表达式，可以根据组的编号来引用某个组。**组号为 0 表示整个表达式**，组号 1 表示被第一对括号括起来的组，以此类推。因此，下面这个表达式，

```java
A(B(C))D
```

中有三个组：组 0 是 `ABCD`，组 1 是 `BC`，组 2 是 `C`。

`Matcher` 对象提供了一系列方法，用以获取与组相关的信息：

- `public int groupCount()` 返回该匹配器的模式中的分组数目，**组 0 不包括在内。**
- `public String group()` 返回前一次匹配操作（例如 `find()`）的第 0 组（整个匹配）。
- `public String group(int i)` 返回前一次匹配操作期间指定的组号，如果匹配成功，但是指定的组没有匹配输入字符串的任何部分，则将返回 `null`。
- `public int start(int group)` 返回在前一次匹配操作中寻找到的组的起始索引。
- `public int end(int group)` 返回在前一次匹配操作中寻找到的组的最后一个字符索引加一的值。

下面是正则表达式组的例子：

```java
// strings/Groups.java
import java.util.regex.*; 

public class Groups {   
    public static final String POEM =     
      "Twas brillig, and the slithy toves\n" +     
      "Did gyre and gimble in the wabe.\n" +     
      "All mimsy were the borogoves,\n" +     
      "And the mome raths outgrabe.\n\n" +     
      "Beware the Jabberwock, my son,\n" +     
      "The jaws that bite, the claws that catch.\n" +     
      "Beware the Jubjub bird, and shun\n" +     
      "The frumious Bandersnatch.";   
    public static void main(String[] args) {     
        Matcher m = Pattern.compile(
          "(?m)(\\S+)\\s+((\\S+)\\s+(\\S+))$")       
          .matcher(POEM);     
        while(m.find()) {       
            for(int j = 0; j <= m.groupCount(); j++)         
                System.out.print("[" + m.group(j) + "]");       
            System.out.println();     
        }   
    } 
}
/* Output: 
[the slithy toves][the][slithy toves][slithy][toves] 
[in the wabe.][in][the wabe.][the][wabe.] 
[were the borogoves,][were][the 
borogoves,][the][borogoves,] 
[mome raths outgrabe.][mome][raths 
outgrabe.][raths][outgrabe.] 
[Jabberwock, my son,][Jabberwock,][my son,][my][son,] 
[claws that catch.][claws][that catch.][that][catch.] 
[bird, and shun][bird,][and shun][and][shun] 
[The frumious Bandersnatch.][The][frumious 
Bandersnatch.][frumious][Bandersnatch.] 
*/
```

这首诗来自于 Lewis Carroll 所写的 *Through the Looking Glass* 中的 “Jabberwocky”。可以看到这个正则表达式模式有许多圆括号分组，由任意数目的非空白符（`\\S+`）及随后的任意数目的空白符（`\\s+`）所组成。目的是捕获每行的最后3个词，每行最后以 `\$` 结束。不过，在正常情况下是将 `\$` 与整个输入序列的末端相匹配。所以我们一定要显式地告知正则表达式注意输入序列中的换行符。**这可以由序列开头的==模式标记 `(?m)` 来完成==（模式标记马上就会介绍）。**

### `start()` 和 `end()`

在匹配操作成功之后，**`start()` 返回先前匹配的起始位置的索引，而 `end()` 返回所匹配的最后字符的索引加一的值。**匹配操作失败之后（或先于一个正在进行的匹配操作去尝试）调用 `start()` 或 `end()` 将会产生 `IllegalStateException`。下面的示例还同时展示了 `matches()` 和 `lookingAt()` 的用法 [^4]：

```java
// strings/StartEnd.java 
import java.util.regex.*; 

public class StartEnd {
    public static String input =
      "As long as there is injustice, whenever a\n" +     
      "Targathian baby cries out, wherever a distress\n" +     
      "signal sounds among the stars " +     
      "... We'll be there.\n"+     
      "This fine ship, and this fine crew ...\n" +     
      "Never give up! Never surrender!";   
    private static class Display {
        private boolean regexPrinted = false;     
        private String regex;
        Display(String regex) { this.regex = regex; }     
    
        void display(String message) {       
            if(!regexPrinted) {         
                System.out.println(regex);         
                regexPrinted = true;       
            }       
            System.out.println(message);     
        }   
    }   
  
    static void examine(String s, String regex) {     
        Display d = new Display(regex);     
        Pattern p = Pattern.compile(regex);     
        Matcher m = p.matcher(s);     
        while(m.find())       
            d.display("find() '" + m.group() +         
              "' start = "+ m.start() + " end = " + m.end());     
            if(m.lookingAt()) // No reset() necessary       
                d.display("lookingAt() start = "         
                  + m.start() + " end = " + m.end());     
        if(m.matches()) // No reset() necessary       
            d.display("matches() start = "         
              + m.start() + " end = " + m.end());   
    }
    
    public static void main(String[] args) {     
        for(String in : input.split("\n")) {       
            System.out.println("input : " + in);       
            for(String regex : new String[]{"\\w*ere\\w*",         
              "\\w*ever", "T\\w+", "Never.*?!"})         
                examine(in, regex);     
        }   
    } 
} 
/* Output: 
input : As long as there is injustice, whenever a 
\w*ere\w* 
find() 'there' start = 11 end = 16 
\w*ever 
find() 'whenever' start = 31 end = 39 
input : Targathian baby cries out, wherever a distress 
\w*ere\w* 
find() 'wherever' start = 27 end = 35 
\w*ever 
find() 'wherever' start = 27 end = 35 
T\w+ find() 'Targathian' start = 0 end = 10 
lookingAt() start = 0 end = 10 
input : signal sounds among the stars ... We'll be 
there. 
\w*ere\w* 
find() 'there' start = 43 end = 48 
input : This fine ship, and this fine crew ... 
T\w+ find() 'This' start = 0 end = 4
lookingAt() start = 0 end = 4 
input : Never give up! Never surrender! 
\w*ever 
find() 'Never' start = 0 end = 5 
find() 'Never' start = 15 end = 20 
lookingAt() start = 0 end = 5 
Never.*?! 
find() 'Never give up!' start = 0 end = 14 
find() 'Never surrender!' start = 15 end = 31 
lookingAt() start = 0 end = 14 
matches() start = 0 end = 31 
*/ 
```

注意，`find()` 可以在输入的任意位置定位正则表达式，而 `lookingAt()` 和 `matches()` 只有在正则表达式与输入的最开始处就开始匹配时才会成功。`matches()` 只有在整个输入都匹配正则表达式时才会成功，而 `lookingAt()` [^5] 只要输入的第一部分匹配就会成功。

### `Pattern` 标记

`Pattern` 类的 `compile()` 方法还有另一个版本，它接受一个标记参数，以调整匹配行为：

```java
Pattern Pattern.compile(String regex, int flag)
```

其中的 `flag` 来自以下 `Pattern` 类中的常量

| 编译标记                       | 效果                                                         |
| ------------------------------ | ------------------------------------------------------------ |
| `Pattern.CANON_EQ`             | 当且仅当两个字符的完全规范分解相匹配时，才认为它们是匹配的。例如，如果我们指定这个标记，表达式`\u003F`就会匹配字符串`?`。默认情况下，匹配不考虑规范的等价性 |
| `Pattern.CASE_INSENSITIVE(?i)` | 默认情况下，大小写不敏感的匹配假定只有US-ASCII字符集中的字符才能进行。这个标记允许模式匹配不考虑大小写（大写或小写）。**通过指定`UNICODE_CASE`标记及结合此标记。基于Unicode的大小写不敏感的匹配就可以开启了** |
| `Pattern.COMMENTS(?x)`         | 在这种模式下，空格符将被忽略掉，并且以`#`开始直到行末的注释也会被忽略掉。通过嵌入的标记表达式也可以开启Unix的行模式 |
| `Pattern.DOTALL(?s)`           | 在dotall模式下，表达式`.`匹配所有字符，包括行终止符。**默认情况下，`.`不会匹配行终止符** |
| `Pattern.MULTILINE(?m)`        | **在多行模式下，表达式`^`和`$`分别匹配一行的开始和结束。**`^`还匹配输入字符串的开始，而`$`还匹配输入字符串的结尾。**默认情况下，这些表达式仅匹配输入的完整字符串的开始和结束** |
| `Pattern.UNICODE_CASE(?u)`     | 当指定这个标记，并且开启`CASE_INSENSITIVE`时，大小写不敏感的匹配将按照与Unicode标准相一致的方式进行。**默认情况下，大小写不敏感的匹配假定只能在US-ASCII字符集中的字符才能进行** |
| `Pattern.UNIX_LINES(?d)`       | 在这种模式下，在`.`、`^`和`$`的行为中，只识别行终止符`\n`    |

在这些标记中，`Pattern.CASE_INSENSITIVE`、`Pattern.MULTILINE` 以及 `Pattern.COMMENTS`（对声明或文档有用）特别有用。请注意，你可以直接在正则表达式中使用其中的大多数标记，只需要将上表中括号括起来的字符插入到正则表达式中，你希望它起作用的位置即可。

你还**可以通过“或”(`|`)操作符组合多个标记的功能：**

```java
// strings/ReFlags.java 
import java.util.regex.*; 

public class ReFlags {   
    public static void main(String[] args) {     
        Pattern p =  Pattern.compile("^java",       
          Pattern.CASE_INSENSITIVE | Pattern.MULTILINE);     
        Matcher m = p.matcher(       
          "java has regex\nJava has regex\n" +       
          "JAVA has pretty good regular expressions\n" +       
          "Regular expressions are in Java");     
        while(m.find())       
            System.out.println(m.group());   
    } 
}
/* Output: 
java 
Java 
JAVA 
*/
```

在这个例子中，我们创建了一个模式，它将匹配所有以“java”、“Java”和“JAVA”等开头的行，并且是在设置了多行标记的状态下，对每一行（从字符序列的第一个字符开始，至每一个行终止符）都进行匹配。注意，`group()` 方法只返回已匹配的部分。

### `split()`

`split()`方法将输入 `String` 断开成 `String` 对象数组，断开边界由正则表达式确定：

```java
String[] split(CharSequence input) 
String[] split(CharSequence input, int limit)
```

这是一个快速而方便的方法，可以按照通用边界断开输入文本：

```java
// strings/SplitDemo.java 
import java.util.regex.*; 
import java.util.*; 

public class SplitDemo {  
    public static void main(String[] args) {     
        String input =       
          "This!!unusual use!!of exclamation!!points";     
        System.out.println(Arrays.toString(       
        Pattern.compile("!!").split(input)));     
        // Only do the first three:     
        System.out.println(Arrays.toString(       
        Pattern.compile("!!").split(input, 3)));   
    }
}
/* Output: 
[This, unusual use, of exclamation, points] 
[This, unusual use, of exclamation!!points]
*/

```

第二种形式的 `split()` 方法可以限制将输入分割成字符串的数量。

### 替换操作

正则表达式在进行文本替换时特别方便，它提供了许多方法：

- `replaceFirst(String replacement)` 以参数字符串 `replacement` 替换掉第一个匹配成功的部分。
- `replaceAll(String replacement)` 以参数字符串 `replacement` 替换所有匹配成功的部分。
- `appendReplacement(StringBuffer sbuf, String replacement)` 执行渐进式的替换，而不是像 `replaceFirst()` 和 `replaceAll()` 那样只替换第一个匹配或全部匹配。这是一个非常重要的方法。它允许你调用其他方法来生成或处理 `replacement`（`replaceFirst()` 和 `replaceAll()` 则只能使用一个固定的字符串），使你能够以编程的方式将目标分割成组，从而具备更强大的替换功能。
- `appendTail(StringBuffer sbuf)` 在执行了一次或多次 `appendReplacement()` 之后，调用此方法可以将输入字符串余下的部分复制到 `sbuf` 中。

下面的程序演示了如何使用这些替换方法。开头部分注释掉的文本，就是正则表达式要处理的输入字符串：

```java
// strings/TheReplacements.java 
import java.util.regex.*; 
import java.nio.file.*; 
import java.util.stream.*;

/*! Here's a block of text to use as input to 
    the regular expression matcher. Note that we 
    first extract the block of text by looking for 
    the special delimiters, then process the     
    extracted block. !*/

public class TheReplacements {   
    public static void main(String[] args) throws Exception {     
        String s = Files.lines(       
          Paths.get("TheReplacements.java"))       
          .collect(Collectors.joining("\n"));     
        // Match specially commented block of text above:     
        Matcher mInput = Pattern.compile(       
          "/\\*!(.*)!\\*/", Pattern.DOTALL).matcher(s);     
        if(mInput.find())       
            s = mInput.group(1); // Captured by parentheses     
        // Replace two or more spaces with a single space:     
        s = s.replaceAll(" {2,}", " ");     
        // Replace 1+ spaces at the beginning of each     
        // line with no spaces. Must enable MULTILINE mode:     
        s = s.replaceAll("(?m)^ +", "");     
        System.out.println(s);     
        s = s.replaceFirst("[aeiou]", "(VOWEL1)");     
        StringBuffer sbuf = new StringBuffer();     
        Pattern p = Pattern.compile("[aeiou]");     
        Matcher m = p.matcher(s);     
        // Process the find information as you     
        // perform the replacements:     
        while(m.find())      
            m.appendReplacement(sbuf, m.group().toUpperCase());     
        // Put in the remainder of the text:     
        m.appendTail(sbuf);     
        System.out.println(sbuf);
    } 
}
/* Output: 
Here's a block of text to use as input to 
the regular expression matcher. Note that we 
first extract the block of text by looking for 
the special delimiters, then process the 
extracted block. 
H(VOWEL1)rE's A blOck Of tExt tO UsE As InpUt tO 
thE rEgUlAr ExprEssIOn mAtchEr. NOtE thAt wE 
fIrst ExtrAct thE blOck Of tExt by lOOkIng fOr 
thE spEcIAl dElImItErs, thEn prOcEss thE 
ExtrActEd blOck. 
*/

```

此处使用上一章介绍过的 [`Files`](./17-Files.md) 类打开并读入文件。`Files.lines()` 返回一个 `Stream` 对象，包含读入的所有行，`Collectors.joining()` 在每一行的结尾追加参数字符序列，最终拼接成一个 `String` 对象。

`mInput` 匹配 `/*!` 和 `！*/` 之间的所有文字（注意分组的括号）。接下来，将存在两个或两个以上空格的地方，缩减为一个空格，并且删除每行开头部分的所有空格（为了使每一行都达到这个效果，而不仅仅是删除文本开头部分的空格，这里特意开启了多行模式）。这两个替换操作所使用的的 `replaceAll()` 是 `String` 对象自带的方法，在这里，使用此方法更方便。注意，因为这两个替换操作都只使用了一次 `replaceAll()`，所以，与其编译为 `Pattern`，不如直接使用 `String` 的 `replaceAll()` 方法，而且开销也更小些。

`replaceFirst()` 只对找到的第一个匹配进行替换。此外，`replaceFirst()` 和 `replaceAll()` 方法用来替换的只是普通字符串，所以，如果想对这些替换字符串进行某些特殊处理，这两个方法时无法胜任的。如果你想要那么做，就应该**使用 `appendReplacement()` 方法**。**该方法允许你在执行替换的过程中，操作用来替换的字符串。**在这个例子中，先构造了 `sbuf` 用来保存最终结果，然后用 `group()` 选择一个组，并对其进行处理，将正则表达式找到的元音字母替换成大些字母。一般情况下，你应该遍历执行所有的替换操作，然后再调用 `appendTail()` 方法，但是，如果你想模拟 `replaceFirst()`（或替换n次）的行为，那就只需要执行一次替换，然后调用 `appendTail()` 方法，将剩余未处理的部分存入 `sbuf` 即可。

同时**，`appendReplacement()` 方法还允许你通过 `\$g` 直接找到匹配的某个组，这里的 `g` 就是组号。**然而，它只能应付一些简单的处理，无法实现类似前面这个例子中的功能。

### `reset()`

```java
Matcher	reset()	 Resets this matcher.
Matcher	reset(CharSequence input)	    Resets this matcher with a new input sequence.
```

使用创建Matcher的Pattern重新匹配reset中传入的String

通过 `reset()` 方法，可以将现有的 `Matcher` 对象应用于一个新的字符序列：

```java
// strings/Resetting.java 
import java.util.regex.*; 

public class Resetting {   
    public static void main(String[] args) throws Exception {     
        Matcher m = Pattern.compile("[frb][aiu][gx]")       
          .matcher("fix the rug with bags");     
        while(m.find())       
            System.out.print(m.group() + " ");     
        System.out.println();     
        m.reset("fix the rig with rags");     
        while(m.find())       
            System.out.print(m.group() + " ");   
    } 
} 
/* Output: 
fix rug bag 
fix rig rag 
*/
```

使用不带参数的 `reset()` 方法，**可以将 `Matcher` 对象重新设置到当前字符序列的起始位置。**

### 正则表达式与 Java I/O

到目前为止，我们看到的例子都是将正则表达式用于静态的字符串。下面的例子将向你演示，如何应用正则表达式在一个文件中进行搜索匹配操作。`JGrep.java` 的灵感源自于 Unix 上的 *grep*。它有两个参数：文件名以及要匹配的正则表达式。输出的是每行有匹配的部分以及匹配部分在行中的位置。

```java
// strings/JGrep.java 
// A very simple version of the "grep" program 
// {java JGrep 
// WhitherStringBuilder.java 'return|for|String'} 
import java.util.regex.*; 
import java.nio.file.*; 
import java.util.stream.*;

public class JGrep {  
    public static void main(String[] args) throws Exception {    
        if(args.length < 2) {      
            System.out.println(        
              "Usage: java JGrep file regex");      
            System.exit(0);   
        }    
        Pattern p = Pattern.compile(args[1]);    
        // Iterate through the lines of the input file:    
        int index = 0;    
        Matcher m = p.matcher("");    
        for(String line: Files.readAllLines(Paths.get(args[0]))) {      
            m.reset(line);      
            while(m.find())        
                System.out.println(index++ + ": " +          
                  m.group() + ": " + m.start());    
        }  
    } 
} 
/* Output: 
0: for: 4 
1: for: 4 
*/

```

`Files.readAllLines()` 返回一个 `List<String>` 对象，这意味着可以用 *for-in* 进行遍历。虽然可以在 `for` 循环内部创建一个新的 `Matcher` 对象，但是，在循环体外创建一个空的 `Matcher` 对象，然后用 `reset()` 方法每次为 `Matcher` 加载一行输入，这种处理会有一定的性能优化。最后用 `find()` 搜索结果。

这里读入的测试参数是 `JGrep.java` 文件，然后搜索以 `[Ssct]` 开头的单词。

如果想要更深入地学习正则表达式，你可以阅读 Jeffrey E. F. Friedl 的《精通正则表达式（第2版）》。网络上也有很多正则表达式的介绍，你还可以从 Perl 和 Python 等其他语言的文档中找到有用的信息。

<!-- Scanning Input -->

## 扫描输入

到目前为止，从文件或标准输入读取数据还是一件相当痛苦的事情。一般的解决办法就是读入一行文本，对其进行分词，然后使用 `Integer`、`Double` 等类的各种解析方法来解析数据：

```java
// strings/SimpleRead.java 
import java.io.*;

public class SimpleRead {  
    public static BufferedReader input =    
      new BufferedReader(new StringReader(    
        "Sir Robin of Camelot\n22 1.61803"));  
    public static void main(String[] args) {    
        try {      
            System.out.println("What is your name?");      
            String name = input.readLine();      
            System.out.println(name);      
            System.out.println("How old are you? " +        
              "What is your favorite double?");      
            System.out.println("(input: <age> <double>)");      
            String numbers = input.readLine();      
            System.out.println(numbers);      
            String[] numArray = numbers.split(" ");      
            int age = Integer.parseInt(numArray[0]);      
            double favorite = Double.parseDouble(numArray[1]);      
            System.out.format("Hi %s.%n", name);      
            System.out.format("In 5 years you will be %d.%n", age + 5);      
            System.out.format("My favorite double is %f.", favorite / 2);    
        } catch(IOException e) {      
            System.err.println("I/O exception");    
        }  
    } 
}
/* Output: 
What is your name? 
Sir Robin of Camelot 
How old are you? What is your favorite double? 
(input: <age> <double>) 
22 1.61803
Hi Sir Robin of Camelot. 
In 5 years you will be 27. 
My favorite double is 0.809015. 
*/

```

`input` 字段使用的类来自 `java.io`，[附录:流式 I/O](./Appendix-IO-Streams.md) 详细介绍了相关内容。`StringReader` 将 `String` 转化为可读的流对象，然后用这个对象来构造 `BufferedReader` 对象，因为我们要使用 `BufferedReader` 的 `readLine()` 方法。最终，我们可以使用 `input` 对象一次读取一行文本，就像从控制台读入标准输入一样。

`readLine()` 方法将一行输入转为 `String` 对象。如果每一行数据正好对应一个输入值，那这个方法也还可行。但是，如果两个输入值在同一行中，事情就不好办了，我们必须分解这个行，才能分别解析所需的输入值。在这个例子中，分解的操作发生在创建 `numArray`时。

终于，Java SE5 新增了 `Scanner` 类，它可以大大减轻扫描输入的工作负担：

```java
// strings/BetterRead.java 
import java.util.*; 

public class BetterRead {
  public static void main(String[] args) {
    Scanner stdin = new Scanner(SimpleRead.input);
    System.out.println("What is your name?");
    String name = stdin.nextLine();
    System.out.println(name);
    System.out.println(
      "How old are you? What is your favorite double?");
    System.out.println("(input: <age> <double>)");
    int age = stdin.nextInt();
    double favorite = stdin.nextDouble();
    System.out.println(age);
    System.out.println(favorite);
    System.out.format("Hi %s.%n", name);
    System.out.format("In 5 years you will be %d.%n",
      age + 5);
    System.out.format("My favorite double is %f.",
      favorite / 2);
  }
}
/* Output: 
What is your name? 
Sir Robin of Camelot 
How old are you? What is your favorite double? 
(input: <age> <double>) 
22 
1.61803 
Hi Sir Robin of Camelot. 
In 5 years you will be 27. 
My favorite double is 0.809015. 
*/

```

**`Scanner` 的构造器可以接收任意类型的输入对象，包括 `File`、`InputStream`、`String` 或者像此例中的`Readable` 实现类。**`Readable` 是 Java SE5 中新加入的一个接口，表示“具有 `read()` 方法的某种东西”。上一个例子中的 `BufferedReader` 也归于这一类。

有了 `Scanner`，所有的输入、分词、以及解析的操作都隐藏在不同类型的 `next` 方法中。普通的 `next()` 方法返回下一个 `String`。所有的基本类型（除 `char` 之外）都有对应的 `next` 方法，包括 `BigDecimal` 和 `BigInteger`。所有的 next 方法，只有在找到一个完整的分词之后才会返回。**`Scanner` 还有相应的 `hasNext` 方法，用以判断下一个输入分词是否是所需的类型，如果是则返回 `true`。**

在 `BetterRead.java` 中没有用 `try` 区块捕获`IOException`。**因为，`Scanner` 有一个假设，在输入结束时会抛出 `IOException`，所以 `Scanner` 会把 `IOException` 吞掉。**不过，通过 `ioException()` 方法，你可以找到最近发生的异常，因此，你可以在必要时检查它。

### `Scanner` 分隔符

默认情况下，`Scanner` 根据空白字符对输入进行分词，但是你可以用正则表达式指定自己所需的分隔符：

```java
// strings/ScannerDelimiter.java 
import java.util.*;
public class ScannerDelimiter {  
    public static void main(String[] args) {    
        Scanner scanner = new Scanner("12, 42, 78, 99, 42");    
        scanner.useDelimiter("\\s*,\\s*");    
        while(scanner.hasNextInt())    
            System.out.println(scanner.nextInt());  
    } 
}
/* Output: 
12 
42 
78 
99 
42 
*/

```

这个例子使用逗号（包括逗号前后任意的空白字符）作为分隔符，同样的技术也可以用来读取逗号分隔的文件。我们可以用 `useDelimiter()` 来设置分隔符，同时，还有一个 `delimiter()` 方法，用来返回当前正在作为分隔符使用的 `Pattern` 对象。

### 用正则表达式扫描

除了能够扫描基本类型之外，你还可以使用自定义的正则表达式进行扫描，这在扫描复杂数据时非常有用。下面的例子将扫描一个防火墙日志文件中的威胁数据：

```java
// strings/ThreatAnalyzer.java 
import java.util.regex.*; 
import java.util.*;
public class ThreatAnalyzer { 
    static String threatData =    
      "58.27.82.161@08/10/2015\n" +   
      "204.45.234.40@08/11/2015\n" +    
      "58.27.82.161@08/11/2015\n" +    
      "58.27.82.161@08/12/2015\n" +    
      "58.27.82.161@08/12/2015\n" +
      "[Next log section with different data format]";  
    public static void main(String[] args) { 
        Scanner scanner = new Scanner(threatData);    
        String pattern = "(\\d+[.]\\d+[.]\\d+[.]\\d+)@" +      
            "(\\d{2}/\\d{2}/\\d{4})";    
        while(scanner.hasNext(pattern)) {      
            scanner.next(pattern);      
            MatchResult match = scanner.match();      
            String ip = match.group(1);      
            String date = match.group(2);      
            System.out.format(        
                "Threat on %s from %s%n", date,ip);    
        }  
    } 
} 
/* Output: 
Threat on 08/10/2015 from 58.27.82.161 
Threat on 08/11/2015 from 204.45.234.40 
Threat on 08/11/2015 from 58.27.82.161 
Threat on 08/12/2015 from 58.27.82.161 
Threat on 08/12/2015 from 58.27.82.161 
*/  
```

当 `next()` 方法配合指定的正则表达式使用时，将找到下一个匹配该模式的输入部分，调用 `match()` 方法就可以获得匹配的结果。如上所示，它的工作方式与之前看到的正则表达式匹配相似。

在配合正则表达式使用扫描时，有一点需要注意：它仅仅针对下一个输入分词进行匹配，如果**你的正则表达式中含有分隔符，那永远不可能匹配成功。**

<!-- StringTokenizer -->

## StringTokenizer类

在 Java 引入正则表达式（J2SE1.4）和 `Scanner` 类（Java SE5）之前，分割字符串的唯一方法是使用 `StringTokenizer` 来分词。不过，现在有了正则表达式和 `Scanner`，我们可以使用更加简单、更加简洁的方式来完成同样的工作了。下面的例子中，我们将 `StringTokenizer` 与另外两种技术简单地做了一个比较：

```java
// strings/ReplacingStringTokenizer.java 
import java.util.*; 

public class ReplacingStringTokenizer {   
    public static void main(String[] args) {     
        String input =       
          "But I'm not dead yet! I feel happy!";     
        StringTokenizer stoke = new StringTokenizer(input);     
        while(stoke.hasMoreElements())       
            System.out.print(stoke.nextToken() + " ");     
        System.out.println(); 
        System.out.println(Arrays.toString(input.split(" ")));     
        Scanner scanner = new Scanner(input);     
        while(scanner.hasNext())       
            System.out.print(scanner.next() + " ");   
    }
} 
/* Output: 
But I'm not dead yet! I feel happy! 
[But, I'm, not, dead, yet!, I, feel, happy!] 
But I'm not dead yet! I feel happy! 
*/
```

使用正则表达式或 `Scanner` 对象，我们能够以更加复杂的模式来分割一个字符串，而这对于 `StringTokenizer` 来说就很困难了。**基本上，我们可以放心地说，`StringTokenizer` 已经可以废弃不用了。**

<!-- Summary -->

## 本章小结

过去，Java 对于字符串操作的技术相当不完善。不过随着近几个版本的升级，我们可以看到，Java 已经从其他语言中吸取了许多成熟的经验。到目前为止，它对字符串操作的支持已经很完善了。不过，有时你还要在细节上注意效率问题，例如恰当地使用 `StringBuilder` 等。

[^1]: C++允许编程人员任意重载操作符。这通常是很复杂的过程（参见Prentice Hall于2000年编写的《Thinking in C++（第2版）》第10章），因此Java设计者认为这是很糟糕的功能，不应该纳入到Java中。起始重载操作符并没有糟糕到只能自己去重载的地步，但具有讽刺意味的是，与C++相比，在Java中使用操作符重载要容易得多。这一点可以在Python(参见[www.Python.org](http://www.python.org))和C#中看到，它们都有垃圾回收机制，操作符重载也简单易懂。
[^4]: input来自于[Galaxy Quest](https://en.wikipedia.org/wiki/Galaxy_Quest)中Taggart司令的一篇演讲。
[^5]: 我不知道他们是如何想出这个方法名的，或者它到底指的什么。这只是代码审查很重要的原因之一。

