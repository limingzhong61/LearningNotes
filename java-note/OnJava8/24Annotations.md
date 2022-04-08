

# 24 注解,Annotations

注解（也被称为**元数据**,**本质就是一种保存在java代码中数据**）为我们在**代码中添加信息提供了一种形式化的方式**，使我们可以在稍后的某个时刻更容易的使用这些数据。

## 24.1.2 元注解

Java 语言中目前有5 种标准注解（前面介绍过），以及**5 种元注解。元注解用于注解其他的注解**
注解解释

- **@Target** 表示注解可以用于哪些地方。可能的ElementType 参数包括：
  CONSTRUCTOR：构造器的声明
  
- - **FIELD**：字段声明（包括enum 实例）
  - **LOCAL_VARIABLE**：局部变量声明
  - METHOD：方法声明
  - PACKAGE：包声明
  - PARAMETER：参数声明
  
  - **TYPE**：类、接口（包括注解类型）或者enum 声明
  
  ```java
    @Target(ElementType.TYPE) // Applies to classes only
  ```
  
  >  如果想要将注解**应用于所有的ElementType，那么可以省去@Target 注解**，但是这并不常
  > 见。
  
- **@Retention** 表示**注解信息保存的时长**（保存周期）。可选的RetentionPolicy 参数包括：
  
  - SOURCE：注解将被编译器丢弃，这意味着**注解不会再存留在编译后的代码**，这在编译时
    处理注解是没有必要的，它只是指出，在这里，**javac 是唯一有机会处理该注解的代理。**
  - CLASS：注解在class 文件中可用，但是会被VM 丢弃。
  - RUNTIME：VM 将在运行期也保留注解，因此可以通过反射机制读取注解的信
    息。
  
- @Documented 将此注解保存在Javadoc 中

- @Inherited 允许子类继承父类的注解

- @Repeatable 允许一个注解可以被使用一次或者多次（Java 8）。
    大多数时候，程序员定义自己的注解，并编写自己的处理器来处理他们。
    24.2 编

getAnnotation() 方法返回指定类型的注解对象

```java
UseCase uc = m.getAnnotation(UseCase.class);
```

# 24.2 编写注解处理器

在Java 8，在使用多个注解的时候，你可以重复使用同一个注解。@Repeatable

## 24.2.5 注解不支持继承

你不能**使用extends 关键字来继承@interfaces。**

## 24.4 基于注解的单元测试

单元测试是对类中**每个方法**提供一个或者多个测试的一种事件，其目的是为了有规律的**测试一个类中每个部分是否具备正确的行为**。在Java 中，最著名的单元测试工具就是JUnit。

## 更复杂的处理器（粗略看过）

## ==基于注解的单元测试（粗略看过）==



