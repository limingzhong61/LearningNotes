# 文件处理

## 文件的理解

**文件是数据的抽象和集合**

- 文件是存储在辅助存储器上的数据序列
- 文件是数据存储的一种形式
- 文件展现形态：文本文件和二进制文件 

**文本文件 vs. 二进制文件**

- 文件文件和二进制文件只是文件的展示方式
- 本质上，所有文件都是二进制形式存储
- 形式上， 所有文件采用两种方式展示 

### 文本文件 

- 由单一特定编码组成的文件，如UTF-8编码
- 由于存在编码，也被看成是存储着的长字符串
- 适用于例如： .txt文件、 .py文件等 

### 二进制文件 

- 直接由比特0和1组成， 没有统一字符编码
- 一般存在二进制0和1的组织结构，即文件格式
- 适用于例如： .png文件、 .avi文件等 

### 文本文件vs二进制文件

**f.txt文件保存：“中国是一个伟大的国家！”；**

#### 文本形式打开文件

```python
#tf = open("f.txt", mode="rt",encoding='UTF-8') 能指定编码
tf = open("f.txt", "rt",encoding='UTF-8')
print(tf.readline())
tf.close()

============= RESTART: E:/Codes/Python/new/file.py ====================
中国是一个伟大的国家！
>>> 
```

#### 二进制形式打开文件

```python
tf = open("f.txt", mode="rb")
#tf = open("f.txt", "rb")
print(tf.readline())
tf.close()

====== RESTART: E:/Codes/Python/new/file.py ====================
b'\xe4\xb8\xad\xe5\x9b\xbd\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe4\xbc\x9f\xe5\xa4\xa7\xe7\x9a\x84\xe5\x9b\xbd\xe5\xae\xb6\xef\xbc\x81'
>>> 
```

## 文件的使用

![1567820024993](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/%E6%96%87%E4%BB%B6%E7%9A%84%E6%89%93%E5%BC%80%E5%85%B3%E9%97%AD.png)

文件的打开

```python
<变量名(文件句柄)> = open(<文件名|文件路径和名称>, <打开模式 |文本 or 二进制|读 or 写 >)
```

文件路径和名称
源文件同目录可省路径

```
"D:/PYE/f.txt"
"D:\\PYE\\f.txt" "f.txt"
"./PYE/f.txt" 
```

## 打开模式 

文本文件：存储的是普通“字符"文本，默认为unicode字符集，可以使用记本事程序打开
二进制文件：把数据内容用“字节"”进行存储，无法用记事本打开，必须使用专用的软件打开，举例：mp3音频文件，jpg图片.doc文档等

**文本形式、只读模式、默认值**

| 文件的打开模式 | 描述                                                         |
| -------------- | ------------------------------------------------------------ |
| 'r'            | 只读模式，默认值，文件的指针将会放在文件的开头，如果文件不存在，返回FileNotFoundError |
| 'w'            | 覆盖写（只写）模式，文件不存在则创建，存在则完全覆盖，文件的指针在文件的开头 |
| 'a'            | 追加写模式，文件不存在则创建,，文件指针在 文件开头;文件存在则在文件最后追加内容,文件指针在原文件末尾 |
| 'b'            | 二进制文件模式                                               |
| 't'            | 文本文件模式，默认值                                         |
| '+'            | 不能单独使用，与r/w/x/a一同使用，在原功能基础上增加同时读写功能，如a+ |
| 'x'            | 创建写模式，文件不存在则创建，存在则返回FileExistsError      |



```python
f = open("f.txt")
f = open("f.txt", "rt")
f = open("f.txt", "w")
f = open("f.txt", "a+")
f = open("f.txt", "x")
f = open("f.txt", "b")
f = open("f.txt", "wb")
- 文本形式、只读模式、默认值
- 文本形式、只读模式、同默认值
- 文本形式、覆盖写模式
- 文本形式、追加写模式+ 读文件
- 文本形式、创建写模式
- 二进制形式、只读模式
- 二进制形式、覆盖写模式
```

```python
#文本形式打开文件
tf = open("f.txt", "rt")
print(tf.readline())
tf.close()
#二进制形式打开文件
bf = open("f.txt", "rb")
print(bf.readline())
bf.close()
```



## 文件内容的读取 

| 操作方法               | 描述                                                         |
| ---------------------- | ------------------------------------------------------------ |
| <f>.read(size=-1)      | 读入全部内容，如果给出参数，读入前size长度 >>>s = f.read(2) 中国 |
| <f>.readline(size=-1)  | 读入一行内容，如果给出参数，读入该行前size长度 >>>s = f.readline() 中国是一个伟大的国家！ |
| <f>.readlines(hint=-1) | 读入文件所有行，以每行为元素形成列表 如果给出参数，读入前hint行 >>>s = f.readlines() ['中国是一个伟大的国家！ '] |

### **文件的逐行操作** 

逐行遍历文件：方法一

- **一次读入，分行处理**

```python
fname = input("请输入要打开的文件名称:")
fo = open(fname,"r")
for line in fo.readlines():
	print(line)
fo.close()
```

逐行遍历文件：方法二

- **分行读入，逐行处理**

```python
fname = input("请输入要打开的文件名称:")
fo = open(fname,"r")
for line in fo:
	print(line)
fo.close()
```

## 数据的文件写入 

| 操作方法              | 描述                                                         |
| --------------------- | ------------------------------------------------------------ |
| <f>.write(s)          | 向文件写入一个字符串或字节流 >>>f.write("中国是一个伟大的国家!") |
| <f>.writelines(lines) | 将一个元素全为字符串的列表写入文件 >>>ls = ["中国", "法国", "美国"] >>>f.writelines(ls) 中国法国美国 |
| <f>.seek(offset)      | 改变当前文件操作指针的位置， offset含义如下： 0 – 文件开头； 1 – 当前位置； 2 – 文件结尾 >>>f.seek(0) #回到文件开头 |

**数据的文件写入** 

- 写入一个字符串列表(没有任何输出)

```python
fo = open("output.txt","w+")
ls = ["中国", "法国", "美国"]
fo.writelines(ls)
for line in fo:
 print(line)
fo.close()
```

- 写入一个字符串列表

```python
fo = open("output.txt","w+")
ls = ["中国", "法国", "美国"]
fo.writelines(ls)
fo.seek(0)
for line in fo:
 print(line)
fo.close()
```

## with open



**文件使用完毕后必须关闭，因为文件对象会占用操作系统的资源，并且操作系统同一时间能打开的文件数量也是有限的**：

```
f.close()
```

由于文件读写时都有可能产生`IOError`，一旦出错，后面的`f.close()`就不会调用。所以，为了保证无论是否出错都能正确地关闭文件，我们可以使用`try ... finally`来实现：

```python
try:
    f = open('/path/to/file', 'r')
    print(f.read())
finally:
    if f:
        f.close()
```

但是每次都这么写实在太繁琐，所以，Python引入了`with`语句来自动帮我们调用`close()`方法：

```python
with open('/path/to/file', 'r') as f:
    print(f.read())
```

这和前面的`try ... finally`是一样的，但是代码更佳简洁，并且不必调用`f.close()`方法。

## 遍历文件夹下的所有文件

```python
for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            print(os.path.join(root, f))

        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))
```

## 删除文件

os.remove() 方法用于删除指定路径的文件。**如果指定的路径是一个目录，将抛出OSError**。

在Unix, Windows中有效

### 语法

**remove()**方法语法格式如下：

```
`os.remove(path)`
```

### 参数

- **path** -- 要移除的文件路径

### 返回值

该方法没有返回值

## 修改文件内容3种方法（替换文件内容）

## 一、修改原文件方式

```python
def alter(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)
 
alter("file1", "09876", "python")
```

https://blog.csdn.net/u012206617/article/details/121673782

# 文件的读写操作

文件的读写俗称“IO操作”

文件的读写操作流程

<img src="python/image-20220526143736596-1654138202739.png" alt="image-20220526143736596" style="zoom:50%;" />

<img src="python/image-20220526143748382-1654138202739.png" alt="image-20220526143748382" style="zoom:33%;" />

## open()语法规则

open()创建文件对象

![image-20220526144035058](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/image-20220526144035058-1654138202739.png)



## 文件对象的常用方法

![image-20220526144706581](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/image-20220526144706581-1654138202740.png)

# with语句（上下文管理器）

wth语句可以自动管理上下文资源，不论什么原因跳出wth块都能确保文件正确的关闭，以此来释放资源

![image-20220526144908120](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/image-20220526144908120-1654138202740.png)

# 目录操作--os模块

os模块是Python内置的与**操作系统功能和文件系统相关的模块**，该模块中的语句的执行结果通常与操作系统有关，在不同的操作系统上运行，得到的结果可能不一样
		os模块与os.path模块用于对目录或文件进行操作

## os模块的常用函数

```python
import os
os.system('notedpad.exe')
#直接调用可执行文件
os.startfile('可执行文件的位置')
```

| 返回值    | 函数                               | 说明                           |
| --------- | ---------------------------------- | ------------------------------ |
|           | getcwd()                           | 返回当前的工作目录             |
| list[str] | listdir (path)                     | 返回指定路径下的文件和目录信息 |
|           | mkdir (path[, mode])               | 创建目录                       |
|           | makedirs (path1/path2... [, mode]) | 创建多级目录                   |
|           | os.chdir(path)                     | 将path设置为当前工作目录       |

## os.path模块操作目录相关函数

| 函数                  | 说明                                                         |
| --------------------- | ------------------------------------------------------------ |
| abspath (path)        | 用于获取文件或目录的绝对路径                                 |
| os.path.exists (path) | 用于判断文件或目录是否存在，如果存在返回True,<br/>否则返回False |
| join (path, name)     | 将目录与目录或者文件名拼接起来                               |
| splitext ()           | 分离文件名和扩展名                                           |
| basename (path)       | 从一个目录中提取文件名                                       |
| dirname (path)        | 从一个路径中提取文件路径，不包括文件名                       |
| isdir (path)          | 用于判断是否为路径                                           |
|                       |                                                              |



```
"""Utility functions for copying and archiving files and directory trees.

XXX The functions here don't copy the resource fork or other metadata on Mac.

"""
```



# os模块的补充——shutil模块

## 本文大纲

os模块是Python标准库中一个重要的模块，里面提供了对目录和文件的一般常用操作。而Python另外一个标准库——shutil库，它作为os模块的补充，提供了复制、移动、删除、压缩、解压等操作，这些 os 模块中一般是没有提供的。但是需要注意的是：shutil 模块对压缩包的处理是调用 ZipFile 和 TarFile这两个模块来进行的。

![在这里插入图片描述](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/2020081717024675.png)

## 知识串讲

本文所使用的素材，都是基于以下2个文件夹，其中一个文件夹为空。

![在这里插入图片描述](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/20200817122825398.png)

### 1）模块导入



```
import shutil
```

### 2）复制文件

函数：shutil.copy(src,dst)
含义：复制文件；
参数：src表示源文件，dst表示目标文件夹；
注意：当移动到一个不存在的“目标文件夹”，系统会将这个不存在的“目标文件夹”识别为新的文件夹，而不会报错；

```java
# 1.将a表的“data.txt”移动到b表
src = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_a\data.txt"
dst = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_b"

shutil.copy(src,dst)
------------------------------------------------------------
# 2.将a表的“data.txt”移动到b表，并重新命名为“new_data.txt”
src = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_a\data.txt"
dst = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_b\new_data.txt"

shutil.copy(src,dst)
------------------------------------------------------------
# 3.将a表的“data.txt”移动到“不存在”的文件夹
src = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_a\data.txt"
dst = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_c"

shutil.copy(src,dst)
"""
注意：对于情况3，系统会默认将“test_shutil_c”识别为文件名，而不是按照我们认为的，移动到一个新的不存在的文件夹。
"""

```

结果如下：

### 3）复制文件夹

函数：shutil.copytree(src,dst)
含义：**复制文件夹；**
参数：src表示源文件夹，dst表示目标文件夹；
注意：这里**只能是移动到一个空文件夹，而不能是包含其他文件的非空文件夹**，否则会报错PermissionError；
① 如果目标文件夹中存在其他文件，会报错；

```python
# 将a文件夹移动到b文件夹，由于前面的操作，此时b文件夹中已经有其他文件
src = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_a"
dst = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_b"

shutil.copytree(src,dst)
```

结果如下：

```
Traceback (most recent call last):
  File "D:\Codes\Python\python-util\java_all_str.py", line 211, in <module>
    shutil.copytree(source_dir, target_dir)
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python39\lib\shutil.py", line 565, in copytree
    return _copytree(entries=entries, src=src, dst=dst, symlinks=symlinks,
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python39\lib\shutil.py", line 466, in _copytree
    os.makedirs(dst, exist_ok=dirs_exist_ok)
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python39\lib\os.py", line 225, in makedirs
    mkdir(name, mode)
FileExistsError: [WinError 183] 当文件已存在时，无法创建该文件。: 'D:/Codes/Python/python-util/java_all_str'

Process finished with e
xit code 1

```

② 如果指定任意一个目标文件夹，则会自动创建；

```
# c文件夹原本是不存在的，我们使用了下方的代码，会自动创建该文件夹
src = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_a"
dst = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_c"

shutil.copytree(src,dst)
```

结果如下：

![在这里插入图片描述](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/20200817161935610.png)

### 4）移动文件或文件夹

函数：shutil.move(src,dst)
含义：移动文件/文件夹；
– 参数：src表示源文件/文件夹，dst表示目标文件夹；
注意：文件/文件夹一旦被移动了，原来位置的文件/文件夹就没了。目标文件夹不存在时，会报错；

```
# c文件夹原本是不存在的，我们使用了下方的代码，会自动创建该文件夹
src = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_a"
dst = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_c"

shutil.copytree(src,dst)

```

结果如下：

![在这里插入图片描述](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/20200817161935610.png)

注意：移动文件夹操作类似，我这里就不赘述了，自行下去学习。

### 5）删除文件夹

#### send2trash删除（推荐）

shutil.rmtree删除后不能找回来，可以用 **send2trash第三方模块中的 send2trash. send2trash(path)删除，这个模块删除的东西可以放到回收站，需要时再还原**

```python
target_dir = 'D:/Codes/Python/python-util/java_all_str'
if path.exists(target_dir):
    send2trash.send2tr
```

#### **shutil删除文件不可以恢复**，删除文件夹(慎用)

函数：shutil.rmtree(src)
含义：删除文件夹；
参数：src表示源文件夹；
注意：区别这里和os模块中remove()、rmdir()的用法，remove()方法只能删除某个文件，mdir()只能删除某个空文件夹。但是**shutil模块中的rmtree()可以递归彻底删除非空文件夹；**

```
# 将c文件夹彻底删除
src = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_c"
shutil.rmtree(src)
```

结果如下：

![在这里插入图片描述](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/2020081716500280.png)

### 6）创建和解压压缩包

zipobj.write()：创建一个压缩包；
zipobj.namelist()：读取压缩包中的文件信息；
zipobj.extract()：将压缩包中的单个文件，解压出来；
zipobj.extractall()：将压缩包中所有文件，解压出来；
shutil 模块对压缩包的处理是调用 ZipFile 和 TarFile这两个模块来进行的，因此需要导入这两个模块；
注意：这里所说的压缩包，指的是“.zip”格式的压缩包；
① 创建一个压缩包

```
import zipfile
import os
file_list = os.listdir(os.getcwd())
# 将上述所有文件，进行打包，使用“w”
with zipfile.ZipFile(r"我创建的压缩包.zip", "w") as zipobj:
    for file in file_list:
        zipobj.write(file)

```

结果如下：

![在这里插入图片描述](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/2020081717211632.png)

② 读取压缩包中的文件信息

```
import zipfile

with zipfile.ZipFile("我创建的压缩包.zip", "r") as zipobj:
    print(zipobj.namelist())

```

结果如下：

![在这里插入图片描述](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/20200817173909169.png)

③ 将压缩包中的单个文件，解压出来
注意：目标文件夹不存在，会自动创建；

```
import zipfile
# 将压缩包中的“test.ipynb”文件，单独解压到a文件夹下
dst = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_a"
with zipfile.ZipFile("我创建的压缩包.zip", "r") as zipobj:
    zipobj.extract("test.ipynb",dst)

```

结果如下：

![在这里插入图片描述](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/20200817174345911.png)

④ 将压缩包中所有文件，解压出来；
注意：目标文件夹不存在，会自动创建；

```
import zipfile
# 将压缩包中的所有文件，解压到d文件夹下
dst = r"C:\Users\limingzhong\Desktop\publish\os模块\test_shutil_d"
with zipfile.ZipFile("我创建的压缩包.zip", "r") as zipobj:
    zipobj.extractall(dst)

```

结果如下：

![在这里插入图片描述](img_Python-%E6%96%87%E4%BB%B6%E7%9B%AE%E5%BD%95%E6%93%8D%E4%BD%9C/20200817175442891.png)


原文链接：https://blog.csdn.net/weixin_41261833/article/details/108050152