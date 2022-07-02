# git-me

##  git项目流程中常用命令

git克隆远程仓库代码 ：git clone xx (远程仓库地址)
克隆下来之后启动项目，按需求修改问题，完成之后准备提交代码
这时候不能直接提交push的，我们需要先 git add .
然后git commit -m "xx(需求的描述)"
再 git pull 拉取最新代码 看看是否有冲突，有冲突解决冲突合并代码，没有冲突，就可以git push 大功告成等待进一步测试

## git其它一些常用命令

查看本地分支: git branch
查看所有分支: git branch -a
切换到本地xxx分支: git checkout xxx
查看状态: git status
切换到远程xxx分支: git checkout -t origin/xxx
查看commit日志: git log


## 开发时不使用master(保存)分支

1. 开发时添加大型文件，如果在主分支添加，将很难删除其占用的空间，通过合并分支，或者删除分支，很容易办到。

## 添加大型文件请慎重

git commit之后git会保存此时所有文件，如果此时添加了不必要的大型文件，会不必要的增加文件大小。特别是master分支。

[https://git-scm.com/docs/git-checkout]: 

## Git 修改已提交的commit注释

两种情况：
 1.已经将代码push到远程仓库
 2.还没将代码push到远程仓库，还在本地的仓库中

这两种情况下的修改大体相同，只是第一种情况最后会多一步
 下面来说怎么修改

先搞清楚你要修改哪次的提交注释或者哪几次的提交注释

### 修改最后一次注释

如果你只想修改最后一次注释（就是最新的一次提交），那好办：
 `git commit --amend`
 出现有注释的界面（你的注释应该显示在第一行）， 输入`i`进入修改模式，修改好注释后，按`Esc`键 退出编辑模式，输入`:wq`保存并退出。ok，修改完成。
 例如修改时编辑界面的图：

![img](https:////upload-images.jianshu.io/upload_images/10019540-7544f6a6883728d3.png?imageMogr2/auto-orient/strip|imageView2/2/w/671/format/webp)

编辑commit注释.png



### 修改之前的注释

### 修改之前的某次注释

1. 输入：
   `git rebase -i HEAD~2`
   最后的数字2指的是显示到倒数第几次  比如这个输入的2就会显示倒数的两次注释（最上面两行）

   ![img](https:////upload-images.jianshu.io/upload_images/10019540-0db9f307d45630e4.png?imageMogr2/auto-orient/strip|imageView2/2/w/775/format/webp)

   显示倒数两次的commit注释.png

   

2. 你想修改哪条注释 就把哪条注释前面的`pick`换成`edit`。方法就是上面说的编辑方式：`i`---编辑，把`pick`换成`edit`---`Esc`---`:wq`.

3. 然后：（接下来的步骤Terminal会提示）
   `git commit --amend`

4. 修改注释，保存并退出后，输入：
   `git rebase --continue`

   ![img](https:////upload-images.jianshu.io/upload_images/10019540-00d3c9acbce99abe.png?imageMogr2/auto-orient/strip|imageView2/2/w/471/format/webp)

   提示输入的命令.png

   

其实这个原理我的理解就是先版本回退到你想修改的某次版本，然后修改当前的commit注释，然后再回到本地最新的版本

#### 修改之前的某几次注释

修改多次的注释其实步骤和上面的一样，不同点在于：

1. 同上
2. 你可以将**多个**想修改的commit注释前面的`pick`换成`edit`
3. **依次修改**你的注释（顺序是从旧到新），Terminal基本都会提示你接下来的操作，每修改一个注释都要重复上面的3和4步，直到修改完你所选择的所有注释

### 已经将代码push到远程仓库

首先，你把最新的版本从远程仓库先pull下来，修改的方法都如上，最后修改完成后，强制push到远程仓库：
 `git push --force origin master`
 **注：很重要的一点是，你最好保证在你强制push之前没有人提交代码，如果在你push之前有人提交了新的代码到远程仓库，然后你又强制push，那么会被你的强制更新覆盖！！！**

最后，可以检查一下远程的提交记录~~



[参考链接](https://www.jianshu.com/p/098d85a58bf1)

## github

[Github 网页上 更新 Fork别人的 Repository](https://blog.csdn.net/huutu/article/details/51018317)

github查看代码方式：

**github.com改成github1s.com**

/github1s.com/codeOflI/JudgeServer/blob/HEAD/src/main/java/com/yoj/judge_server/aspect/JudgePermitAspect.java

## git cherry-pick 教程

http://www.ruanyifeng.com/blog/2020/04/git-cherry-pick.html

## 使用git stash命令保存和恢复进度

我们有时会遇到这样的情况，正在dev分支开发新功能，做到一半时有人过来反馈一个bug，让马上解决，但是新功能做到了一半你又不想提交，这时就**可以使用git stash命令先把当前进度保存起来**，然后切换到另一个分支去修改bug，修改完提交后，再切回dev分支，使**用git stash pop来恢复之前的进度继续开发新功能**。下面来看一下git stash命令的常见用法

原文链接：https://blog.csdn.net/daguanjia11/article/details/73810577

## git 文件及文件加大小写不识别的解决方案

项目更改了文件名提交到git 仓库结果文件并没有得到跟踪的情况，在你独立开发的时候这个问题是可以被忽略的，但是如果你是，要部署到服务器的时候问题立马就暴露出来了
例子：修改某文件的某个字母 大小写后 git上传到仓库时，并没有跟踪的情况


1.git查看是否忽略了大小写
true:忽略了大小写 fasle:未忽略大小写
```
git config --get core.ignorecase 
```
得到的结果是false 说明我本地已经配置了 区分大小写了，如果 窗口提示为true执行下列代码
```
git config core.ignorecase false 
```
##### 解决方案如下：

1. 用`git`执行下列命令：

```ruby
$ git config core.ignorecase false
```

解释：设置本地`git`环境识别大小写

1. 修改文件夹名称，全部改为小写（F2重命名修改即可），然后`push`到远程仓库。
    这时如我前面的图片所示，仓库上就会有重名的文件(文件夹)了。
2. 删除多余的文件，我这里就是把`Footer`,`Header`,`Menu`等给删掉。
    a).  执行命令，删除远程文件（删除文件夹里面的文件，文件夹也会消失）

```ruby
# 删除Header文件夹下的所有文件
$ git rm --cached src/components/Header -r
# 删除Footer文件夹下的所有文件
$ git rm --cached src/components/Footer -r
# 删除Menu文件夹下的所有文件
$ git rm --cached src/components/Menu -r
```

如果显示如下，说明操作成功：

```bash
rm 'src/components/Menu/Header.js'
rm 'src/components/Menu/Header.less'
...
```

b). 同步，提交到远程仓库

```ruby
# 添加在缓存
$ git add .
# 提交到本地
$ git commit -m'rm files'
# 提交到远程仓库 origin
& git push origin master
```


链接：https://www.jianshu.com/p/420d38913578