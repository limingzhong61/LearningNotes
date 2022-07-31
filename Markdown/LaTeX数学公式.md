# LaTeX数学公式

**在Markdown文档中是能使用LaTeX数学公式的**

Typora是支持的。

[LaTex官方文档](https://www.latex-project.org/help/documentation/)感觉写的不好

$ 表示行内公式： 

质能守恒方程可以用一个很简洁的方程式 $E=mc^2$ 来表达。

`$$` 表示整行公式：

$$ \sum_{i=1}^n a_i=0 $$

$$f(x_1,x_x,\ldots,x_n) = x_1^2 + x_2^2 + \cdots + x_n^2 $$

$$ \sum^{j-1}_{k=0}{\widehat{\gamma}_{kj} z_k}$$

访问 [MathJax](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference) 参考更多使用方法。

## 常用的数学符号

### 希腊字母

#### 1、小写希腊字母

下面的都要上面这个案例一样才有用。两边只写了一个\$的可以插在文本中，而两边写两个连续的$则会单独占一行，并且会居中而且还要大一些。

##### 2、大写希腊字母

 大写希腊字母只需要将小写希腊字母的**第一个英文字母大写即可**。但是需要注意的是，有些小写希腊字母的大写可以直接通过键盘输入，也就是说和英文大写是相同的。

| 希腊字母           | 英语             | 希腊字母           | 英语             |
| ------------------ | ---------------- | ------------------ | ---------------- |
| α                  | \alpha           | $\nu$              | \nu              |
| β                  | \beta            | $\Xi$$\xi$         | \Xi\|\xi         |
| $\Gamma$γ          | \Gamma\|\gamma   | $o$                | \o               |
| $\Delta$δ          | \Delta\|\delta   | $\Pi\pi$           | \Pi\pi           |
| $\Epsilon\epsilon$ | \epsilon         | $\rho$             | \rho             |
| $\Zeta\zeta$       | \zeta            | $\Sigma$$\sigma$   | \Sigma\sigma     |
| η                  | \eta             | $\tau$             | \tau             |
| $\Theta\theta$     | \Theta\theta     | $\Upsilon\upsilon$ | \Upsilon\upsilon |
| ι                  | \iota            | $\Phi$$\phi$       | \Phi\phi         |
| κ                  | \kappa           | $\chi$             | \chi             |
| $\Lambda$λ         | \Lambda\|\lambda | $\Psi\psi$         | \Psi\psi         |
| μ                  | \mu              | $\Omega$$\omega$   | \Omega\omega     |

### 运算符

 对于加减除，对应键盘上便可打出来，但是对于乘法，键盘上没有这个符号，所以我们应该输入 \times 来显示一个 $\times $号。

  普通字符在数学公式中含义一样，除了 # $ % & ~ _ ^ \ { } 若要在数学环境中表示这些符号# $ % & _ { }，需要分别表示为# $ % & _ { }，即在个字符前加上\ 。

### 集合符号

### 集合符号

一些特殊的集合符号，使用 \mathbb 命令：

 

| 集合符号             | 编码                    |
| -------------------- | ----------------------- |
| $实数集合\mathbb{R}$ | \mathbb{R} 或 \mathbb R |
| $\mathbb{z}$         | \mathbb{z}              |
| $\mathbb{N}$         | \mathbb{N}              |

集合关系符号

| 符号           | 英语   |
| -------------- | ------ |
| 属于$\in$      | \in    |
| 不属于$\notin$ | \notin |
|                |        |

### LaTeX 中的特殊符号

[参考博文](https://blog.csdn.net/chen134225/article/details/78793622)



## 格式

### 简单格式

##### 1、上下标

 上标：表示 $ f(x) = x^ 2 $

```latex
`$ f(x) = x^ 2 $` 或者 `$ f(x) = {x}^ {2} $` 均可
```

 下标：表示 $ f(x) = x_2 $

```latex
$ f(x) = x_2 $ 或者 $ f(x) = {x}_{2} $ 均可
```

 上下标可以级联：$ f(x) = x_1^2 + {x}_{2}^{2} $

```latex
$ f(x) = x_1^2 + {x}_{2}^{2} $
```

##### 2、加粗和倾斜

 加粗：$ f(x) = \textbf{x}^2 $ 均可表示

```latex
$ f(x) = \textbf{x}^2 $
```

 文本：$ f(x) = x^2 \mbox{abcd} $ 均可表示

```latex
$ f(x) = x^2 \mbox{abcd} $
```

 倾斜：$ f(x) = x^2 \mbox{\emph{abcd} defg} $

```latex
$ f(x) = x^2 \mbox{\emph{abcd} defg} $
```

##### 3、分数

```latex
$ f(x,y) = \frac{x^2}{y^3} $
```

$ f(x,y) = \frac{x^2}{y^3} $

##### 4、开根号

```latex
$ f(x,y) = \sqrt[n]{{x^2}{y^3}} $
```

```
$ f(x,y) = \sqrt[n]{{x^2}{y^3}} $
```

##### 5、省略号

```latex
$ f(x_1, x_2, \ldots, x_n) = x_1 + x_2 + \cdots + x_n $
```

$ f(x_1, x_2, \ldots, x_n) = x_1 + x_2 + \cdots + x_n $



##### 6、括号和分隔符

 公式高度比较低的话直接从键盘输入括号即可，但是对于公式高度比较高的情形，需要特殊的运算。

```latex
$ {f}'(x) = (\frac{df}{dx}) $
```

$ {f}'(x) = (\frac{df}{dx}) $

```latex
$ {f}'(x) = \left( \frac{df}{dx} \right) $
```

$$ {f}'(x) = \left( \frac{df}{dx} \right) $$
可以看出，通过将 **\left( 和 \right) 结合使用**，可以将括号大小随着其内容变化。[ ] 和 { } 同理。

```latex
$ {f}'(0) =  \left. \frac{df}{dx} \right|_{x=0} $
```

$ {f}'(0) =  \left. \frac{df}{dx} \right|_{x=0} $

### 字母上面加符号

加^号 $\hat{a},\widehat{A}$

```latex
$\hat{a},\widehat{A}$
```

加横线 输入 \overline

加波浪线 输入 \widetilde

加一个点 \dot{要加点的字母}

加两个点\ddot{要加点的字母}

加箭头 输入\vec

 ![img](LaTeX%E6%95%B0%E5%AD%A6%E5%85%AC%E5%BC%8F/20160927145319800.png) 

### LaTeX 换行

https://blog.csdn.net/DUTwangtaiyu/article/details/114281954

#### 方法一：输入 **`\\`**

![在这里插入图片描述](LaTeX%E6%95%B0%E5%AD%A6%E5%85%AC%E5%BC%8F/20210302115338816.png)

结果即只进行单纯换行，并无缩进
![在这里插入图片描述](LaTeX%E6%95%B0%E5%AD%A6%E5%85%AC%E5%BC%8F/20210302115440326.png)

## 三、矩阵和行列式

```latex
$ A=\left[ \begin{matrix}
   a & b  \\
   c & d  \\
\end{matrix} \right] $
```

$ A=\left[ \begin{matrix}
   a & b  \\
   c & d  \\
\end{matrix} \right] $



```latex
$ \chi (\lambda)=\left| \begin{matrix}
   \lambda - a & -b  \\
   -c & \lambda - d  \\
\end{matrix} \right| $
```

$ \chi (\lambda)=\left| \begin{matrix}
   \lambda - a & -b  \\
   -c & \lambda - d  \\
\end{matrix} \right| $

### 四、求和与连乘

```latex
$ \sum_{k=1}^n k^2 = \frac{1}{2} n (n+1) $
12
```

$ \sum_{k=1}^n k^2 = \frac{1}{2} n (n+1) $

```latex
$ \prod_{k=1}^n k = n! $
```

$ \prod_{k=1}^n k = n! $

### 五、导数、极限、积分

##### 1、导数

 导数的表示用一对花括号将被导函数括起来，然后加上一个英文的引号即可。

```latex
$ {f}'(x) = x^2 + x $
```

$ {f}'(x) = x^2 + x $

##### 2、极限

```latex
$ \lim_{x \to 0} \frac{3x^2 +7x^3}{x^2 +5x^4} = 3 $
```

$$ \lim_{x \to 0} \frac{3x^2 +7x^3}{x^2 +5x^4} = 3 $$

##### 3、积分

integral： 积分

 积分中，需要注意的是，在多重积分内 dx 和 dy 之间 使用一个斜杠加一个逗号 , 来增大稍许间距。同样，在两个积分号之间使用一个斜杠加一个感叹号 ! 来减小稍许间距。使之更美观。

```latex
$ \int_a^b f(x)\,dx $
```

$ \int_a^b f(x)\,dx $

```latex
$ \int_0^{+\infty} x^n e^{-x} \,dx = n! $
```

$ \int_0^{+\infty} x^n e^{-x} \,dx = n! $

```latex
$ \int_{x^2 + y^2 \leq R^2} f(x,y)\,dx\,dy = 
\int_{\theta=0}^{2\pi} \int_{r=0}^R 
f(r\cos\theta,r\sin\theta) r\,dr\,d\theta $
```

$ \int_{x^2 + y^2 \leq R^2} f(x,y)\,dx\,dy = 
\int_{\theta=0}^{2\pi} \int_{r=0}^R 
f(r\cos\theta,r\sin\theta) r\,dr\,d\theta $

```latex
$ \int \!\!\! \int_D f(x,y)\,dx\,dy
\int \int_D f(x,y)\,dx\,dy $
```

$ \int \!\!\! \int_D f(x,y)\,dx\,dy
\int \int_D f(x,y)\,dx\,dy $
 在加入了 ! 之后，距离的改变还是很明显的。

```latex
$ i\hbar\frac{\partial \psi}{\partial {t}} = \frac{-\hbar^2}{2m} 
\left( \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + 
\frac{\partial^2}{\partial z^2} \right) \psi + V \psi $
```

$ i\hbar\frac{\partial \psi}{\partial {t}} = \frac{-\hbar^2}{2m} 
\left( \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + 
\frac{\partial^2}{\partial z^2} \right) \psi + V \psi $

```latex
$ \frac{d}{dt} \int \!\!\! \int \!\!\! \int_{\textbf{R}^3} \left
| \psi(\mathbf{r},t) \right|^2\,dx\,dy\,dz = 0 $
```

$$ \frac{d}{dt} \int \!\!\! \int \!\!\! \int_{\textbf{R}^3} \left
| \psi(\mathbf{r},t) \right|^2\,dx\,dy\,dz = 0 $$

------

附：

##### 关于如何在Word中插入LaTeX公式：

链接：[撒哈拉之心23的博文](https://blog.csdn.net/huilingwu/article/details/52425402)
该种方法若公式显示不完整，需调整段落行距为最小值：[百度链接](https://jingyan.baidu.com/article/656db9182f26d0e380249c44.html)

[参考博文](https://blog.csdn.net/weixin_42373330/article/details/89785443)

### 用其他软件编写

使用word写LaTex公式，能直接选择相应结构。如果自己实在不会写，**可以用word写成公式，然后转成LaTex编码格式。**

![image-20211121212108892](LaTeX%E6%95%B0%E5%AD%A6%E5%85%AC%E5%BC%8F/image-20211121212108892.png)

## 

## latex求和符号上下标

https://blog.csdn.net/weixin_39655362/article/details/110806154

一般在手写的时候通常都是用左边这种格式，也是我们一般认为的“标准格式”。而我们有时也会看到一些书上或者论文里出现右边这种格式，这种格式我们称为text style，也就是普通文本的样式。

<img src="LaTeX%E6%95%B0%E5%AD%A6%E5%85%AC%E5%BC%8F/9684f378f58f823f0af5a212d6ab5a09.png" alt="9684f378f58f823f0af5a212d6ab5a09.png" style="zoom: 33%;" />

在[latex](https://so.csdn.net/so/search?q=latex&spm=1001.2101.3001.7020)中，通常是会自动将行内公式（或者也叫内联公式）写成textstyle，这样主要是为了让公式上下更加紧凑，在文字间显示时既能保持公式大小，也不至于顶出行。而在行间公式里则默认标准格式，这种写法更加接近手写体，显得开阔、大方。

<img src="LaTeX%E6%95%B0%E5%AD%A6%E5%85%AC%E5%BC%8F/b984bf4380f82ef607999b4a2f44744f.png" alt="b984bf4380f82ef607999b4a2f44744f.png" style="zoom: 33%;" />

那不同的格式怎么打出来呢？

不过要注意的是，**textstyle命令要写在运算符的前面**，**而limits命令要写在运算符的后面**。这样就可以不受行内还是行间的限制，任何时候都可以打出我们想要的上下标了

### textstyle

```latex
$$\textstyle \int_a^b f(x)\,dx$$
```


$$
\textstyle \int_a^b f(x)\,dx
$$


### 默认模式

```latex
$$\int_a^b f(x)\,dx$$
```


$$
\int_a^b f(x)\,dx
$$

### limits

code:

```latex
\int\limits_a^b f(x)dx
```

結果


$$
\int\limits_a^b f(x)dx
$$

但是注意，这种打法只对**运算符**有效，字母的上下标样式是不能这样改的

## 字母上下标overset和underset

正确的做法是**使用overset和underset**

```latex
\overset{123}{a}
```

$$
\overset{123}{a}
$$
### 下标

```latex
\underset{abc}{x}
```

$$
\underset{abc}{x}
$$









用这两个命令其实也可以编辑运算符的上下标位置，但这就完全没有必要了。关于符号摆放位置我们在后续的教程里再单独讲一讲

![289ba1b92a778823f6b5f2fd4cbf89e0.gif](LaTeX%E6%95%B0%E5%AD%A6%E5%85%AC%E5%BC%8F/289ba1b92a778823f6b5f2fd4cbf89e0.gif)





