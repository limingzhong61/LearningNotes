# nvm安装教程

[使用 nvm 管理不同版本的 node 与 npm](https://www.runoob.com/w3cnote/nvm-manager-node-versions.html)

nvm主要用于切换node版本

## 卸载node

安装nvm前最好对以前安装的node进行卸载
在控制面版或者应用列表中卸载nodejs
删除npm的相关文件
例如C:\Users<user>\AppData\Roaming\npm

## 安装注意点：

`nvm install 6.4.0`
試一下這種可不可以，如果不可以~
請打開nvm的安裝路徑，在此路徑找出`settings.txt`文件

安装路径`D:\Users\nicolas\AppData\Roaming\nvm`

打開`settings.txt`文件，在此文件添加此下載包的包來源

```
node_mirror: https://npm.taobao.org/mirrors/node/
npm_mirror: https://npm.taobao.org/mirrors/npm/
```

接下來在執行一次`nvm install 6.4.0`
nvm -v可判断是否安装成功

> 在使用相应的npm -v等指令时，**应该首先使用`nvm use x.x`版本。**

```bash
nvm use x.x
npm -v
...
```



## 下载nvm

进入[GitHub](https://github.com/coreybutler/nvm-windows/releases)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191021152530280.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxODY2Nzc2,size_16,color_FFFFFF,t_70)
下载安装版
打开

# nvm使用（命令）



## 安装

| 命令                           | 作用                |
| ------------------------------ | ------------------- |
| nvm install <version> [<arch>] | 安装多版本 node/npm |
| nvm ls                         | 列出已安装实例      |
| **nvm use** <version>          | 在不同版本间切换    |
|                                |                     |



## 版本 node/npm

使用nvm install <version> [<arch>]命令下载需要的版本。arch参数表示系统位数，默认是64位，如果是32位操作系统，需要执行命令：nvm install 6.9.0 32

```
nvm install 4.2.2
```

nvm 遵守[语义化版本](http://semver.org/lang/zh-CN/)命名规则。例如，你想安装最新的 **4.2** 系列的最新的一个版本的话，可以运行：

```
nvm install 4.2
```

nvm 会寻找 **4.2.x** 中最高的版本来安装。

你可以通过以下命令来**列出远程服务器上所有的可用版本：**

Windows 的话，就是：

```
nvm ls available
```

------

## 在不同版本间切换

每当我们安装了一个新版本 Node 后，全局环境会自动把这个新版本设置为默认。

nvm 提供了 **nvm use** 命令。这个命令的使用方法和 **install** 命令类似。

例如，切换到 **4.2.2**：

```
nvm use 4.2.2
```

切换到最新的 **4.2.x**：

```
nvm use 4.2
```

切换到 iojs：

```
nvm use iojs-v3.2.0
```

切换到最新版：

```
nvm use node
```

每次执行切换的时候，系统都会把 node 的可执行文件链接放到特定版本的文件上。

我们还可以用 nvm 给不同的版本号设置别名：

```
nvm alias awesome-version 4.2.2
```

我们给 **4.2.2** 这个版本号起了一个名字叫做 **awesome-version**，然后我们可以运行：

```
nvm use awesome-version
```

下面这个命令可以取消别名：

```
nvm unalias awesome-version
```

另外，你还可以设置 **default** 这个特殊别名：

```
nvm alias default node
```



