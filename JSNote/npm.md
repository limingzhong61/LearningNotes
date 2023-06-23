# NPM 使用介绍

NPM是随同NodeJS一起安装的包管理工具，能解决NodeJS代码部署上的很多问题，常见的使用场景有以下几种：

- 允许用户从NPM服务器下载别人编写的第三方包到本地使用。
- 允许用户从NPM服务器下载并安装别人编写的命令行程序到本地使用。
- 允许用户将自己编写的包或命令行程序上传到NPM服务器供别人使用。

由于新版的nodejs已经集成了npm，所以之前npm也一并安装好了。同样可以通过输入 **"npm -v"** 来测试是否成功安装。命令如下，出现版本提示表示安装成功:

```使用 npm 命令安装模块
$ npm -v
2.3.0
```

## 使用 npm 命令安装模块

npm 安装 Node.js 模块语法格式如下：

```
$ npm install <Module Name>
```

以下实例，我们使用 npm 命令安装常用的 Node.js web框架模块 **express**:

```
$ npm install express
```

安装好之后，express 包就放在了工程目录下的 node_modules 目录中，因此在代码中只需要通过 **require('express')** 的方式就好，无需指定第三方包路径。

```
var express = require('express');
```

## 全局安装与本地安装

npm 的包安装分为本地安装（local）、全局安装（global）两种，从敲的命令行来看，差别只是有没有-g而已，比如

```
npm install express          # 本地安装
npm install express -g   # 全局安装
```

如果出现以下错误：

```
npm err! Error: connect ECONNREFUSED 127.0.0.1:8087 
```

解决办法为：

```
$ npm config set proxy null
```

### 本地安装

- \1. 将安装包放在 ./node_modules 下（运行 npm 命令时所在的目录），如果没有 node_modules 目录，会在当前执行 npm 命令的目录下生成 node_modules 目录。
- \2. 可以通过 require() 来引入本地安装的包。

### 全局安装

- \1. 将安装包放在 /usr/local 下或者你 node 的安装目录。
- \2. 可以直接在命令行里使用。

如果你希望具备两者功能，则需要在两个地方安装它或使用 **npm link**。

接下来我们使用全局方式安装 express

```
$ npm install express -g
```

安装过程输出如下内容，第一行输出了模块的版本号及安装位置。

```
express@4.13.3 node_modules/express
├── escape-html@1.0.2
├── range-parser@1.0.2
├── merge-descriptors@1.0.0
├── array-flatten@1.1.1
├── cookie@0.1.3
├── utils-merge@1.0.0
├── parseurl@1.3.0
├── cookie-signature@1.0.6
├── methods@1.1.1
├── fresh@0.3.0
├── vary@1.0.1
├── path-to-regexp@0.1.7
├── content-type@1.0.1
├── etag@1.7.0
├── serve-static@1.10.0
├── content-disposition@0.5.0
├── depd@1.0.1
├── qs@4.0.0
├── finalhandler@0.4.0 (unpipe@1.0.0)
├── on-finished@2.3.0 (ee-first@1.1.1)
├── proxy-addr@1.0.8 (forwarded@0.1.0, ipaddr.js@1.0.1)
├── debug@2.2.0 (ms@0.7.1)
├── type-is@1.6.8 (media-typer@0.3.0, mime-types@2.1.6)
├── accepts@1.2.12 (negotiator@0.5.3, mime-types@2.1.6)
└── send@0.13.0 (destroy@1.0.3, statuses@1.2.1, ms@0.7.1, mime@1.3.4, http-errors@1.3.1)
```

### 查看安装信息

你可以使用以下命令来查看所有全局安装的模块：

```
npm list -g
```



```

├─┬ cnpm@4.3.2
│ ├── auto-correct@1.0.0
│ ├── bagpipe@0.3.5
│ ├── colors@1.1.2
│ ├─┬ commander@2.9.0
│ │ └── graceful-readlink@1.0.1
│ ├─┬ cross-spawn@0.2.9
│ │ └── lru-cache@2.7.3
……
```

如果要查看某个模块的版本号，可以使用命令如下：

```
$ npm list grunt

projectName@projectVersion /path/to/project/folder
└── grunt@0.4.1
```

# npm安装实在太慢怎么办

## 设置npm registry更改镜像

将npm registry更改为淘宝镜像，快的飞起！
1.临时使用
[npm --registry https://registry.npm.taobao.org install express](https://www.jianshu.com/p/94d084ce6834)
2.持久使用

```bash
npm config set registry https://registry.npm.taobao.org
```

使用mac需要权限的话，前面需要加sudo，然后输入密码。
配置后可通过下面方式来验证是否成功：

```bash
npm config get registry
```

3.通过cnpm使用

```bash
npm install -g cnpm --registry=https://registry.npm.taobao.org
```



# 查看,修改npm全局安装目录

查看npm 安装路径 , 终端执行 npm config get prefix

1、打开Node.js Command prompt，执行npm config ls

2、修改prefix的值：npm config set prefix *

3、npm help +命令,查看详情

# npm 安装

参数

- --save：将保存配置信息到pacjage.json。默认为dependencies节点中。

  ```bash
  npm install echarts --save
  ```

# 







# nrm安装与配置

1.nrm

nrm(npm registry manager )是npm的镜像源管理工具，有时候国外资源太慢，使用这个就可以快速地在 npm 源间切换

2.安装nrm

在命令行执行命令，npm install -g nrm，全局安装nrm。

```
npm install -g nrm
```

3.使用

执行命令nrm ls查看可选的源。

> nrm ls                                                                  
>
> *npm ---- https://registry.npmjs.org/
>
> cnpm --- http://r.cnpmjs.org/
>
> taobao - http://registry.npm.taobao.org/
>
> eu ----- http://registry.npmjs.eu/
>
> au ----- http://registry.npmjs.org.au/
>
> sl ----- http://npm.strongloop.com/
>
> nj ----- https://registry.nodejitsu.com/

其中，带*的是当前使用的源，上面的输出表明当前源是官方源。

5.切换

如果要切换到taobao源，执行命令:

```
nrm use taobao
```

## 6.增加

你可以增加定制的源，特别适用于添加企业内部的私有源，执行命令 `nrm add <registry> <url>`，其中reigstry为源名，url为源的路径。

```
nrm add registry http://registry.npm.frp.trmap.cn/
nrm add taobao https://registry.npm.taobao.org/
```

## 7.删除

执行命令nrm del <registry>删除对应的源。

```
nrm del taobao
```

8.测试速度

你还可以通过 nrm test 测试相应源的响应时间。

```bash
nrm test npm          
```

​                                                     

------

9 报错

最近安装好npm时候，再安装nrm 后，

nrm ls 报错internal/validators.js:124 throw new ERR_INVALID_ARG_TYPE(name, ‘string‘, value)

![img](https:////upload-images.jianshu.io/upload_images/13658013-77f1903a7650cff6.png?imageMogr2/auto-orient/strip|imageView2/2/w/784/format/webp)

报错

解决方法

1、首先检查node.js是否安装成功，输入 node -v 若可查看版本号，如图所示即安装成功；

若不一致则重新安装node.js。

node.js官方下载地址：[https://nodejs.org/en/download/](https://links.jianshu.com/go?to=https%3A%2F%2Fnodejs.org%2Fen%2Fdownload%2F)

2.查看npm是否安装成功，如下图成功，反之则重新安装

npm -v

3、报错截图中可见 cli.js文件中 第17行报错，

![img](https:////upload-images.jianshu.io/upload_images/13658013-4b06b0dfcac36348.png?imageMogr2/auto-orient/strip|imageView2/2/w/720/format/webp)

17行

按路径找到该文件：

![img](https:////upload-images.jianshu.io/upload_images/13658013-12c4af98d98ac1cd.png?imageMogr2/auto-orient/strip|imageView2/2/w/655/format/webp)

报错截图中可见 cli.js文件

打开文件找到报错的第17行，注掉原17行改为如图：

//const NRMRC = path.join(process.env.HOME, '.nrmrc');(注掉)

const NRMRC = path.join(process.env[(process.platform == 'win32') ? 'USERPROFILE' : 'HOME'], '.nrmrc');

再管理员模式运行cmd，输入nrm ls ：

![img](https:////upload-images.jianshu.io/upload_images/13658013-47b13f8ae6971f9e.png?imageMogr2/auto-orient/strip|imageView2/2/w/396/format/webp)

好了

> 链接：https://www.jianshu.com/p/94d084ce6834

# Other



## node 16.14 npm ERR! Unexpected token '.'

I had a similar issue when using `npm init` and `npm install`. I downgrade my node version to 16.13.2 (recommended for most users) and it works.