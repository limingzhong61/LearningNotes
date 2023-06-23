# Ubuntu



### Ubuntu的介绍Ubuntu

Python：开发平台Ubuntu

（友帮拓、优般图、乌班图）是一个以桌面应用为主的开源GNU/Linux操作系统，Ubuntu是基于GNU/Linux，支持x86、amd64（即x64）和ppc架构，由全球化的专业开发团队（CanonicalLtd）打造的。

专业的Python开发者一般会选择Ubuntu这款Linux系统作为生产平台.

温馨提示：Ubuntu和Centos都是基于GNU/Linux内核的，因此基本使用和Centos是几乎一样的，它们的各种指令可以通用，同学们在学习和使用Ubuntu的过程中，会发现各种操作指令在前面学习CentOS都使用过。只是界面和预安装的软件有所差别。

Ubuntu下载地址：http://cn.ubuntu.com/download/

## Ubuntu的安装

用户名 lee

密码 123456

用户：root

密码 123456

https://blog.csdn.net/qq_43377653/article/details/126877889

### VMware安装Ubuntu后网络连接失败解决办法

https://blog.csdn.net/CHYabc123456hh/article/details/112890125

**方法3解决**

### ubuntu ssh

https://blog.csdn.net/DCJwwh/article/details/128520453

#### ubuntu ssh root

**ubuntu在终端root用户及密码可以正常登陆,但是用ssh登陆,系统却总是提示密码不对**

原因：

​    [ubuntu](https://so.csdn.net/so/search?q=ubuntu&spm=1001.2101.3001.7020)系统的SSH 默认root权限禁用密码登录

解决方法：

vi /etc/ssh/sshd_config
将PermitRootLogin项改为yes
service sshd restart 重启sshd服务即可



### Ubuntu22.04使用笔记本电脑安装摄像头步骤

http://www.taodudu.cc/news/show-3248144.html

```
Job for vmware-tools.service failed because the control process exited eith err or code.

unable to start services for vmware tools
```





18.2.1安装的步骤

18.2.2设置Ubuntu支持中文

默认安装的ubuntu中只有英文语言，因此是不能显示汉字的。要正确显示汉字，需要安装中文语言包。安装中文支持步骤

1.单击左侧图标栏打开SystemSettings（系统设置）菜单，点击打开LanguageSupport（语言支持）选项卡。

2.**点击Install/RemoveLanguages**，在弹出的选项卡中下拉找到**Chinese(Simplified)**，即中文简体，在后面的选项框中打勾。然后点击ApplyChanges提交，系统会自动联网下载中文语言包。（保证ubuntu是联网的）。

3.这时“汉语（中国）”在最后一位因为当前第一位是”English”，所以默认显示都是英文。我们如果希望默认显示用中文，则应该将“汉语（中国）”设置为第一位。设置方法是拖动，鼠标单击“汉语（中国）”，当底色变化（表示选中了）后，按住鼠标左键不松手，**向上拖动放置到第一位。**

4.设置后不会即刻生效，需要下一次登录时才会生效。

**==如果中文包下载时间过长，可以给ubuntu换源（阿里源）；==**

### Ubuntu的root用户 

#### 18.3.1介绍

安装ubuntu成功后，**都是普通用户权限**，并没有最高root权限，如果需要使用root权限的时候，通常都会在命令前面加上sudo。

有的时候感觉很麻烦。我们一般使用su命令来直接切换到root用户的，但是**如果没有给root设置初始密码，就会抛出su:Authentication failure这样的问题。**所以，我们只要给root用户设置一个初始密码就好了。

###  给root用户设置密码并使用

https://blog.csdn.net/WHEgqing/article/details/129379047

1)输入sudo passwd命令，输入一般用户密码并设定root用户密码。

2)设定root密码成功后，输入su命令，并输入刚才设定的root密码，就可以切换成root了。提示符$代表一般用户，提示符#代表root用户。3)输入exit命令，退出root并返回一般用户4)以后就可以使用root用户了

```shell
nicolas@ubuntu:~$ sudo passwd
[sudo] nicolas 的密码： 
对不起，请重试。
[sudo] nicolas 的密码： 
对不起，请重试。
[sudo] nicolas 的密码： 
输入新的 UNIX 密码： 
重新输入新的 UNIX 密码： 
passwd：已成功更新密码
```

### Ubuntu vi命令键盘错乱问题解决

刚装好[Ubuntu](https://so.csdn.net/so/search?q=Ubuntu&spm=1001.2101.3001.7020)系统，使用 vi 命令发现键盘是错乱的，输入任何值都会换行，我们可以通过安装 vim 命令解决，命令如下：

```bash
sudo apt install vim
```

安装完成后，再使用 vim 命令打开文件，发现问题解决。





18.4Ubuntu下开发Python

18.4.1说明安装好Ubuntu后，默认就已经安装好Python的开发环境[Python2.7和Python3.5]

```shell
nicolas@ubuntu:~$ python
Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
nicolas@ubuntu:~$ python3
Python 3.5.2 (default, Nov 17 2016, 17:05:23) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
```

18.4.2在Ubuntu下开发一个Python程序

1)vim hello.py[编写hello.py]

提示：如果Ubuntu没有vim我们可以根据提示信息安装一个vim

```shell
sudo apt install vim
```

## apt软件管理和远程登录

### apt介绍

apt是Advanced Packaging Tool的简称，是一款安装包管理工具。在Ubuntu下，我们可以使用apt命令可用于软件包的安装、删除、清理等，类似于Windows中的软件管理工具。

unbuntu软件管理的原理示意图：

![1566129158215](Ubuntu/1566129158215.png)

19.2Ubuntu软件操作的相关命令

sudo apt-get update更新源

```shell
sudo apt-get install package安装包
```

```shell
sudo apt-get remove package删除包

sudo apt-cache search  package搜索软件包

sudo apt-cache show package 获取包的相关信息，如说明、大小、版本等sudo apt-get install package -- reinstall重新安装包

sudo apt-get -finstall修复安装

sudo apt-get remove package --purge删除包，包括配置文件等

sudo apt-get build -deppackage安装相关的编译环境

```

#### 更新已安装的包

系统最开始使用时尝试更新

```shell
sudo apt-get upgrade 
```

```shell
sudo apt-get dist-upgrade升级系统
```



```shell
sudo apt-cache depends package了解使用该包依赖那些包

sudo apt-cache rdepends package查看该包被哪些包依赖

sudo apt-get source package下载该包的源代码

```



### 更新Ubuntu软件下载地址

19.3.1原理示意图

![1566129449920](Ubuntu/1566129449920.png)

19.3.2寻找国内镜像源

https://mirrors.tuna.tsinghua.edu.cn/

所谓的镜像源：可以理解为提供下载软件的地方，比如Android手机上可以下载软件的安卓市场；iOS手机上可以下载软件的AppStore

19.3.3 备份Ubuntu默认的源地址

```shell
nicolas@ubuntu:/etc/apt$ sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup #拷贝
root@ubuntu:/etc/apt## echo '' > sources.list #清空
root@ubuntu:/etc/apt## vim sources.list #拷贝清华镜像
root@ubuntu:/etc/apt## exit
exit
nicolas@ubuntu:~$ sudo apt-get update #更新ubuntu软件列表
```

### 使用ssh远程登录Ubuntu

19.5.1ssh介绍

SSH为SecureShell的缩写，由IETF的网络工作小组（NetworkWorkingGroup）所制定；SSH为建立在应用层和传输层基础上的安全协议。

SSH是目前较可靠，专为远程登录会话和其他网络服务提供安全性的协议。常用于远程登录，以及用户之间进行资料拷贝。几乎所有UNIX平台—包括HP-UX、Linux、AIX、Solaris、DigitalUNIX、Irix，以及其他平台，都可运行SSH。

使用SSH服务，需要安装相应的服务器和客户端。客户端和服务器的关系：如果，A机器想被B机器远程控制，那么，A机器需要安装SSH服务器，B机器需要安装SSH客户端。和CentOS不一样，Ubuntu默认没有安装SSHD服务，因此，我们不能进行远程登录。

### 使用ssh远程登录Ubuntu

19.6.1安装SSH和启用

```shell
nicolas@ubuntu:~$ sudo apt-get install openssh-server
```

执行上面指令后，在当前这台Linux上就安装了SSH服务端和客户端。

```shell
nicolas@ubuntu:~$ service sshd restart
```

执行上面的指令，就启动了sshd服务。会监听端口22

```shell
nicolas@ubuntu:~$ netstat -anp | more
（并非所有进程都能被检测到，所有非本用户的进程信息将不会显示，如果想看到所有信息，则必须切换到 root 用户）
激活Internet连接 (服务器和已建立连接的)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       
PID/Program name
tcp        0      0 127.0.1.1:53            0.0.0.0:*               LISTEN      
-               
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      
-               
tcp6       0      0 :::22                   :::*                    LISTEN      
-               
udp        0      0 0.0.0.0:631             0.0.0.0:*                           
-               
udp        0      0 0.0.0.0:36829           0.0.0.0:*                           
-               
udp        0      0 127.0.1.1:53            0.0.0.0:*                           
-               
udp        0      0 0.0.0.0:68              0.0.0.0:*                           
-               
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           
-               
udp6       0      0 :::50035                :::*                                
-               
udp6       0      0 :::5353                 :::*                                
-               
--更多--

```

19.6.2在Windows使用XShell5/XFTP5登录Ubuntu

前面我们已经安装了XShell5，直接使用即可。

注意：使用atguigu用户登录，需要的时候再su-切换成root用户

19.6.3从linux系统客户机远程登陆linux

系统服务机首先，我们需要在linux的系统客户机也要安装openssh-server

•基本语法：ssh 用户名@IP

例如：sshatguigu@192.168.188.131使用ssh访问，如访问出现错误。可查看是否有该文件～/.ssh/known_ssh尝试删除该文件解决。

•登出登出命令：exit或者logout

## 安装软件

### 安装C++编译器

打开终端输入sudo apt-get install build-essential 安装gcc和一些库函数。提供C/C++的编译环境

 

注意编译c++程序要用g++

### 安装JDK

https://blog.csdn.net/weixin_38924500/article/details/106215048

