## Vscode——python环境输出中文乱码的一种解决方法

https://blog.csdn.net/Williamcsj/article/details/121940871

## pip‘ 不是内部或外部命令，也不是可运行的程序或批处理文件

添加环境变量:

**pip 所在的文件夹（pip.exe在python的安装目录里的Scripts里面）**

C:\Users\Lenovo\AppData\Local\Programs\Python\Python39\Scripts

```
C:\Users\Lenovo>pip -V
pip 21.2.3 from C:\Users\Lenovo\AppData\Local\Programs\Python\Python39\lib\site-packages\pip (python 3.9)
```

# 使用

# python获取当前时间

**python 如何获取当前系统的时间**

**1、导入包**

```
import datetime
```



**2、获取当前的时间**

```
curr_time = datetime.datetime.now()　　# 2019-07-06 14:55:56.873893 <class 'datetime.datetime'>
curr_time.year　　# 2019 <class 'int'>
curr_time.month　　# 7 <class 'int'>
curr_time.day　　# 6 <class 'int'>
curr_time.hour　　# 14 <class 'int'>
curr_time.minute　　# 55 <class 'int'>
curr_time.second　　# 56 <class 'int'>
curr_time.date()　　# 2019-07-06 <class 'datetime.date'>
```



**3、格式化**

通过datetime.datetime.now()，我们获取到的时间格式为：2019-07-06 14:55:56.873893，类型：<class 'datetime.datetime'>

我们可以使用strftime()转换成我们想要的格式。处理之后的返回的值为2019-07-06、07/06等目标形式，类型为str

```
time_str = curr_time.strftime("%Y-%m-%d")　　# 2019-07-06
time_str = curr_time.strftime("%m/%d")　　# 07/06
```

**4、类型转换**

时间一般通过：时间对象，时间字符串，时间戳表示

通过[datetime](https://www.py.cn/jishu/jichu/20899.html)获取到的时间变量，类型为：datetime，那么datetime与str类型如何互相转换呢？

```
datetime-->str
time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')　　# 2019-07-06 15:50:12
str-->datetime
time_str = '2019-07-06 15:59:58'
curr_time = datetime.datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
```

# pycharm导入python项目

选择New environment 或者 Existing environment都可以，路径选择本地配置的python.exe路径即可；

New Environment:
New Environment部分是选择新建项目所依赖的python库，第一个选项会在项目中简历一个venv（virtualenv）目录，这里存放一个虚拟的python环境。这里所有的类库依赖都可以直接脱离系统安装的python独立运行。 

Existing Interpreter:
Existing Interpreter关联已经存在的python解释器，如果不想在项目中出现venv这个虚拟解释器就可以选择本地安装的python环境。 
**通常选择Existing Interpreter即可**

## python定义类似常量

const.py

```python
class PROBLEM:
    MEMORY_LIMIT = "memory_limit"
    TIME_LIMIT = "time_limit"
    DESCRIPTION = 'description'
    SAMPLE_INPUT = "sample_input"
    SAMPLE_OUTPUT = "sample_output"
    FORMAT_INPUT = "format_input"
    FORMAT_OUTPUT = "format_output"
    HINT = "hint"
    STATE = "state"
```

使用：

```python
from const import *
print(PROBLEM.DESCRIPTION)
```

# `__init__.py`文件

init.py 文件的作用是将文件夹变为一个[Python](https://edu.csdn.net/course/detail/26755)模块,Python 中的每个模块的包中，都有__init__.py 文件.

######### 批量引入

init.py 文件的作用是将文件夹变为一个Python模块,Python 中的每个模块的包中，都有__init__.py 文件。

通常__init__.py 文件为空，但是我们还可以为它增加其他的功能。我们在导入一个包时，实际上是导入了它的__init__.py文件。这样我们可以在__init__.py文件中批量导入我们所需要的模块，而不再需要一个一个的导入。

### package

### __init__.py

import re
import urllib
import sys
import os

### a.py

import package
print(package.re, package.urllib, package.sys, package.os)
init.py中还有一个重要的变量，all, 它用来将模块全部导入

### __init__.py

__all__ = ['os', 'sys', 're', 'urllib']

### a.py

from package import *
可以被import语句导入的对象是以下类型：
模块文件（.py文件）
C或C++扩展（已编译为共享库或DLL文件）
包（包含多个模块）
内建模块（使用C编写并已链接到Python解释器中）
当导入模块时，解释器按照sys.path列表中的目录顺序来查找导入文件。

import sys

> > > print(sys.path)

### Linux:

['', '/usr/local/lib/python3.4',
'/usr/local/lib/python3.4/plat-sunos5',
'/usr/local/lib/python3.4/lib-tk',
'/usr/local/lib/python3.4/lib-dynload',
'/usr/local/lib/python3.4/site-packages']
其中list第一个元素空字符串代表当前目录。

关于.pyc 文件 与 .pyo 文件
py文件的汇编,只有在import语句执行时进行，当.py文件第一次被导入时，它会被汇编为字节代码，并将字节码写入同名的.pyc文件中。后来每次导入操作都会直接执行.pyc 文件（当.py文件的修改时间发生改变，这样会生成新的.pyc文件），在解释器使用-O选项时，将使用同名的.pyo文件，这个文件去掉了断言（assert）、断行号以及其他调试信息，体积更小，运行更快。（使用-OO选项，生成的.pyo文件会忽略文档信息）

导入模块

模块通常为单独的.py文件，可以用import直接引用，可以作为模块的文件类型有.py、.pyo、.pyc、.pyd、.so、.dll

## **对象调用类中的变量和方法**

　　__init__方法是一个特殊的方法,只要类名+() 产生一个对象,自动执行类中的__init__方法,并把类的地址传给方法里的第一个参数,约定把第一个参数定为'self', 再给对象封装相应的属性.

(1) __dict__ 查询对象中的所有的内容

(2)  万能的点： **.**

```python
class Person:
    mind = '有思想'
    belif = '有信仰'
    animal = '高级动物'
    def __init__(self, name,age,hobby):
        self.name = name
        self.age = age
        self.hobby = hobby
        print(name,age,hobby)
    def work(self):
        print('会工作')
        return self
    def money(self):
        print('会消费')
        print(self)
```

## 私有方法

**如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线__**
**在Python中，实例的变量名如果以__开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问**

## 函数传递问题

python不允许程序员选择采用传值还是传引用。python参数传递采用的肯定是**“传对象引用”**的方式。这种方式相当于传值和传引用的一种综合。

- 如果函数收到的是一个不可变对象（数字、字符或元组）的引用，就不能直接修改原始对象--相当于通过**‘值传递’**来传递对象。
- 如果函数收到的是一个可变对象（字典、列表）的引用，就能修改对象的原始值--相当于**‘传引用’**来传递对象。

# Python生成exe文件

为了让没有安装Python的人也能使用我们编写的.py文件，我们需要将编写好的Python程序生成.exe文件。

## 第一步 下载pyinstaller

pyinstaller插件是Python自带的插件，用于为我们写好的代码进行打包，最终自动合成.exe文件。

在Pycharm界面的最下面，你可以看到Terminal，选择这个选项，这就是一个终端界面。

在此界面写输入指令： **`pip install pyinstaller`** 对pyinstaller进行下载。

```
pip install pyinstaller
```



## 第二步 使用pyinstaller

在终端里输入的指令为： 

```
pyinstaller -w -F XXX.py
```

但是对于初学者来说，这里要解释的东西很多：

-w：表示希望在生成的.exe程序运行过程中，不要出现cmd黑框（就是图中的黑框）（注意：小写！）

-F：表示希望将所有的程序全部打包在一起，生成的只有一个.exe文件，这样的文件集成度高，但是运行速度慢；如果不写-F，生成的还有一堆.dll文件，这样的程序里文件很多，但是运行速度比较快，这也是我们平时使用的程序的样式（如图）（注意：大写！）