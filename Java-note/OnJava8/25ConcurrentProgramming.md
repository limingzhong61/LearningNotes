# 25并发编程,Concurrent Programming

[并发编程](https://github.com/LingCoder/OnJava8/blob/master/docs/book/24-Concurrent-Programming.md)

对于更多凌乱，低级别的细节，请参阅附录：[并发底层原理](https://github.com/LingCoder/OnJava8/blob/master/docs/book/Appendix-Low-Level-Concurrency.md)

## 概念

> 要进一步深入这个领域，你还**必须阅读Brian Goetz等人的Java Concurrency in Practice。**

> 另一个有价值的资源是 Bill Venner 的 **Inside the Java Virtual Machine**，它详细描述了 JVM 的最内部工作方式，包括线程。





# 25.1 术语问题

- 并发是关于正确有效地控制对共享资源的访问。
- 并行是使用额外的资源来更快地产生结果。

这是另一种解释：

_并发_

**同时完成多个任务。在开始处理其他任务之前，当前任务不需要完成。并发解决了阻塞发生的问题。**当任务无法进一步执行，直到外部环境发生变化时才会继续执行。最常见的例子是I/O，其中任务必须等待一些input（在这种情况下会被阻止）。**这个问题产生在I/O密集型。**

_并行_

**同时在多个地方完成多个任务。**这**解决了所谓的计算密集型问题**，如果将程序分成多个部分并在不同的处理器上编辑不同的部分，程序可以运行得更快。

> **并发性是一系列性能技术，专注于减少等待**

**在Java中，并发是非常棘手和困难的，所以绝对不要使用它，除非你有一个重大的性能问题**

## 并发的新定义

几十年来，我一直在努力解决各种形式的并发问题，其中一个最大的挑战是简洁的定义它。我将其定义为：

> 并发性是一系列**专注于减少等待的性能技术**

这实际上是一个相当复杂的表述，所以我将其分解：

- 这是一个集合：包含许多不同的方法来解决这个问题。因为技术差异很大，这是使定义并发性如此具有挑战性的问题之一。
- 这些是性能技术：就是这样。并发的关键点在于让你的程序运行得更快。在 Java 中，并发是非常棘手和困难的，所以绝对不要使用它，除非你有一个重大的性能问题 - 即使这样，使用最简单的方法产生你需要的性能，因为并发很快变得难以管理。
- “减少等待”部分很重要而且微妙。无论（例如）你的程序运行在多少个处理器上，你只能在等待发生时产生效益。如果你发起 I/O 请求并立即获得结果，没有延迟，因此无需改进。如果你在多个处理器上运行多个任务，并且每个处理器都以满容量运行，并且没有任务需要等待其他任务，那么尝试提高吞吐量是没有意义的。并发的唯一机会是程序的某些部分被迫等待。等待会以多种形式出现 - 这解释了为什么存在多种不同的并发方法。

值得强调的是，这个定义的有效性取决于“等待”这个词。如果没有什么可以等待，那就没有机会去加速。如果有什么东西在等待，那么就会有很多方法可以加快速度，这取决于多种因素，包括系统运行的配置，你要解决的问题类型以及其他许多问题。

问题在于，我们来描述这种**现象的任何模型最终都是抽象泄露的（leaky abstraction)。**

以下是其中一个泄露：在理想的世界中，每次克隆自己时，也会复制一个物理处理器来运行克隆搜索者。这当然是不现实的——实际上，你的机器上一般只有 4 个或 8 个处理器核心（编写本文时的典型情况）。或许你拥有更多的处理器，但仍有很多情况下只有一个单核处理器。在关于抽象的讨论中，分配物理处理器核心这本身就是抽象的泄露，甚至也可以支配你的决策。

让我们在科幻电影中改变一些东西。现在当每个克隆搜索者最终到达一扇门时，他们必须敲门并等到有人开门。如果每个搜索者都有一个处理器核心，这没有问题——只是空闲等待直到有人开门。但是如果我们只有 8 个处理器核心却有几千个搜索者，我们不希望处理器仅仅因为某个搜索者恰好在等待回答中被锁住而闲置下来。相反，我们希望将处理器应用于可以真正执行工作的搜索者身上，因此需要将处理器从一个任务切换到另一个任务的机制。

**许多模型能够有效地隐藏处理器的数量**，允许你假装有很多个处理器。但在某些情况下，当你必须明确知道处理器数量以便于工作的时候，这些模型就会失效。

最大的影响之一取决于是**使用单核处理器还是多核处理器**。如果你只有单核处理器，那么任务切换的成本也由该核心承担，将并发技术应用于你的系统会使它运行得更慢。

这可能会让你以为，在单核处理器的情况下，编写并发代码是没有意义的。然而，有些情况下，**并发模型会产生更简单的代码**，光是为了这个目的就值得舍弃一些性能。

在克隆体敲门等待的情况下，即使单核处理器系统也能从并发中受益，因为它可以从等待（阻塞）的任务切换到准备运行的任务。但是如果所有任务都可以一直运行那么切换的成本反而会使任务变慢，在这种情况下，并发只在如果你有多个处理器的情况下有意义。

假设你正在尝试破解某种密码，在同一时间内参与破解的线程越多，你越快得到答案的可能性就越大。每个线程都能持续使用你所分配的处理器时间，在这种情况下（CPU 密集型问题），你代码中的**线程数应该和你拥有的处理器的核心数保持一致。**

在接听电话的客户服务部门，你只有一定数量的员工，但是你的部门可能会收到很多电话。这些员工（处理器）一次只能接听一个电话直到打完，此时其它打来的电话必须排队等待。

在“鞋匠和精灵”的童话故事中，鞋匠有很多工作要做，当他睡着时，出现了一群精灵来为他制作鞋子。这里的工作是分布式的，但即使使用大量的物理处理器，在制造鞋子的某些部件时也会产生限制——例如，如果鞋底的制作时间最长，这就限制了鞋子的制作速度，这也会改变你设计解决方案的方式。

因此，**你要解决的问题驱动了方案的设计**。将一个问题分解成“独立运行”的子任务，这是一种美好的抽象，然后就是实际发生的现实：物**理现实不断干扰和动摇这个抽象。**

这只是问题的一部分：考虑一个制作蛋糕的工厂。我们以某种方式把制作蛋糕的任务分给了工人们，现在是时候让工人把蛋糕放在盒子里了。那里有一个准备存放蛋糕的盒子。但是在一个工人把蛋糕放进盒子之前，另一个工人就冲过去，把蛋糕放进盒子里，砰！这两个蛋糕撞到一起砸坏了。这是常见的**“共享内存”问题，会产生所谓的竞态条件（race condition）**，其结果取决于哪个工人能先把蛋糕放进盒子里（通常**使用锁机制来解决问题**，因此一个工作人员可以**先抓住一个盒子并防止蛋糕被砸烂**）。

当“同时”执行的任务相互干扰时，就会出现问题。这可能以一种微妙而偶然的方式发生，因此可以说**并发是“可以论证的确定性，但实际上是不确定性的”**。也就是说，假设你很小心地编写并发程序，而且通过了代码检查可以正确运行。然而实际上，我们编写的并发程序大部分情况下都能正常运行，但是在一些特定情况下会失败。这些情况可能永远不会发生，或者在你在测试期间几乎很难发现它们。实际上，**编写测试代码通常无法为并发程序生成故障条件**。由此产生的失败只会偶尔发生，因此它们以客户投诉的形式出现。这是**学习并发中最强有力的论点之一：如果你忽略它，你可能会受伤。**

因此，并发似乎充满了危险，如果这让你有点害怕，这可能是一件好事。尽管 Java 8 在并发性方面做出了很大改进，但仍然没有像**编译时验证 (compile-time verification) 或受检查的异常 (checked exceptions) 那样的安全网来告诉你何时出现错误**。关于并发，你只能依靠自己**，只有知识渊博、保持怀疑和积极进取的人，才能用 Java 编写可靠的并发代码。**

<!-- Concurrency is for Speed -->

## 并发为速度而生

在听说并发编程的问题之后，你可能会想知道它是否值得这么麻烦。答案**是“不，除非你的程序运行速度不够快。”**并且在决定用它之前你会想要仔细思考。不要随便跳进并发编程的悲痛之中。如果有一种方法可以在更快的机器上运行你的程序，或者如果你可以对其进行分析并发现瓶颈并在该位置替换更快的算法，那么请执行此操作。**只有在显然没有其他选择时才开始使用并发，然后仅在必要的地方去使用它。**

速度问题一开始听起来很简单：如果你想要一个程序运行得更快，将其分解为多个部分，并在单独的处理器上运行每个部分。随着我们提高时钟速度的能力耗尽（至少对传统芯片而言），速度的提高是出现在多核处理器的形式而不是更快的芯片。为了使程序运行得更快，你必须学会利用那些额外的处理器（译者注：处理器一般代表 CPU 的一个逻辑核心），这是并发所带来的好处之一。

对于多处理器机器，可以在这些处理器之间分配多个任务，这可以显著提高吞吐量。强大的多处理器 Web 服务器通常就是这种情况，它可以在程序中为 CPU 分配大量用户请求，每个请求分配一个线程。

但是，并发通常可以提高在单处理器上运行的程序的性能。这听起来有点违反直觉。如果你仔细想想，由于上下文切换的成本增加（从一个任务切换到另一个任务），在单个处理器上运行的并发程序实际上应该比程序的所有部分顺序运行具有更多的开销。从表面上看，将程序的所有部分作为单个任务运行，并且节省上下文切换的成本，这样看似乎更划算。

使这个**问题变得有些不同的是阻塞**。如果程序中的某个任务由于程序控制之外的某种情况而无法继续（通常是 I/O），我们就称该任务或线程已阻塞（在我们的科幻故事中，就是克隆人已经敲门并等待它打开）。如果没有并发，整个程序就会停下来，直到外部条件发生变化。但是，如果使用并发编写程序，则当一个任务被阻塞时，程序中的其他任务可以继续执行，因此整个程序得以继续运行。事实上，从性能的角度来看，**如果没有任务会阻塞，那么在单处理器机器上使用并发是没有意义的。**

单处理器系统中性能改进的一个常见例子是**事件驱动编程**，特别是用户界面编程。考虑一个程序执行一些耗时操作，最终忽略用户输入导致无响应。如果你有一个“退出”按钮，你不想在你编写的每段代码中都检查它的状态（轮询）。这会产生笨拙的代码，也无法保证程序员不会忘了检查。没有并发，生成可响应用户界面的唯一方法是让所有任务都定期检查用户输入。通过**创建单独的线程以执行用户输入的响应，能够让程序保证一定程度的响应能力。**

**实现并发的一种简单方式**是**使用操作系统级别的进程**。与线程不同，进程是**在其自己的地址空间中运行的独立程序**。进程的优势在于，因为操作系统通常将一个进程与另一个进程隔离，因此它们**不会相互干扰**，这使得进程编程相对容易。相比之下，**线程之间会共享内存和 I/O 等资源**，因此编写多线程程序最基本的困难，在于协调不同线程驱动的任务之间对这些资源的使用，以免这些资源同时被多个任务访问。

<!-- 文献引用未加，因为暂时没看到很好的解决办法 -->
有些人甚至提倡将进程作为唯一合理的并发实现方式[^1]，但遗憾的是，通常**存在数量和开销方面的限制**，从而阻止了进程在并发范围内的适用性（最终你会习惯标准的并发限制，“这种方法适用于一些情况但不适用于其他情况”）

一些编程语言**旨在将并发任务彼此隔离**。这些通常被称为**_函数式语言_，**其中每个函数调用**不产生副作用（不会干扰到其它函数）**，所以**可以作为独立的任务来驱动**。Erlang 就是这样一种语言，它包括一个任务与另一个任务进行通信的安全机制。如果发现程序的某一部分必须大量使用并发，并且在尝试构建该部分时遇到了过多的问题，那么可以考虑使用这些**专用的并发语言创建程序的这个部分**。
<!-- 文献标记 -->
Java 采用了更传统的方法[^2]，即在顺序语言之上添加对线程的支持而不是在多任务操作系统中分叉外部进程，**线程**是在表示**执行程序的单个进程内创建任务。**

并发会带来各种成本，包括复杂性成本，但可以被程序设计、资源平衡和用户便利性方面的改进所抵消。通常，并发性使你能够创建更低耦合的设计；另一方面，你必须特别关注那些使用了并发操作的代码。

<!-- The Four Maxims of Java Concurrency -->

## Java 并发的四句格言

在经历了多年 Java 并发的实践之后，我总结了以下四个格言：

>1.**不要用它（避免使用并发）**
>
>2.没有什么是真的，一切可能都有问题
>
>3.仅仅是它能运行，并不意味着它没有问题
>
>4.**你必须理解它（逃不掉并发）**

这些格言专门针对 Java 的并发设计问题，尽管它们也可以适用于其他一些语言。但是，确实存在旨在防止这些问题的语言。

### 1.不要用它

（而且不要自己去实现它）

避免陷入并发所带来的玄奥问题的最简单方法就是不要用它。尽管尝试一些简单的东西可能很诱人，也似乎足够安全，但是陷阱却是无穷且微妙的。如果你能避免使用它，你的生活将会轻松得多。

**使用并发唯一的正当理由是速度**。如果你的程序运行速度不够快——这里要小心，因为仅仅想让它运行得更快不是正当理由——应该**首先用一个分析器（参见代码校验章中分析和优化）来发现你是否可以执行其他一些优化。**

如果你被迫使用并发，请采取最简单，最安全的方法来解决问题。**使用知名的库并尽可能少地自己编写代码。**对于并发，就没有“太简单了”——自作聪明是你的敌人。

### 2.没有什么是真的，一切可能都有问题

不使用并发编程，你已经预料到你的世界具有确定的顺序和一致性。对于变量赋值这样简单的操作，很明显它应该总是能够正常工作。

在并发领域，有些事情可能是真的而有些事情却不是，以至于你必须假设没有什么是真的。你必须质疑一切。即使将变量设置为某个值也可能不会按预期的方式工作，事情从这里开始迅速恶化。我已经熟悉了这样一种感觉：我认为应该明显奏效的东西，实际上却行不通。

在非并发编程中你可以忽略的各种事情，在并发下突然变得很重要。例如，你必须了解处理器缓存以及保持本地缓存与主内存一致的问题，你必须理解对象构造的深层复杂性，这样你的构造函数就不会意外地暴露数据，以致于被其它线程更改。这样的例子不胜枚举。

虽然这些主题过于复杂，无法在本章中给你提供专业知识（同样，请参见 Java Concurrency in Practice），但你必须了解它们。

### 3.仅仅是它能运行，并不意味着它没有问题

我们很容易编写出一个看似正常实则有问题的并发程序，而且问题只有在极少的情况下才会显现出来——在程序部署后不可避免地会成为用户问题（投诉）。

- 你**不能验证出并发程序是正确的**，你只能（有时）验证出它是不正确的。
- 大多数情况下你甚至没办法验证：如果它出问题了，你可能无法检测到它。
- 你通常无法编写有用的测试，因此你必须依靠代码检查和对并发的深入了解来发现错误。
- 即使是有效的程序也只能在其设计参数下工作。当超出这些设计参数时，大多数并发程序会以某种方式失败。

在其他 Java 主题中，我们养成了决定论的观念。一切都按照语言的承诺的（或暗示的）发生，这是令人欣慰的也是人们所期待的——毕竟，编程语言的意义就是让机器做我们想要它做的事情。从确定性编程的世界进入**并发编程领域**，我们遇到了一种称为 [邓宁-克鲁格效应](https://en.wikipedia.org/wiki/Dunning%E2%80%93Kruger_effect) 的认知偏差，可以概括**为“无知者无畏**”，意思是：**“相对不熟练的人拥有着虚幻的优越感，错误地评估他们的能力远高于实际。**

我自己的经验是，无论你是多么确定你的代码是_线程安全_的，它都可能是有问题的。你可以很容易地了解所有的问题，然后几个月或几年后你会发现一些概念，让你意识到你编写的大多数代码实际上都容易受到并发 bug 的影响。当某些代码不正确时，编译器不会告诉你。为了使它正确，在研究代码时，必须将并发性的所有问题都放在前脑中。

在 Java 的所有非并发领域，“没有明显的 bug 而且没有编译报错“似乎意味着一切都好。但对于并发，它没有任何意义。**在这种情况你最糟糕的表现就是“自信”。**

### 4.你必须理解它

在格言 1-3 之后，你可能会对并发性感到害怕，并且认为，“到目前为止，我已经避免了它，也许我可以继续避免它。

这是一种理性的反应。你可能知道其他更好地被设计用于构建并发程序的编程语言——甚至是在 JVM 上运行的语言（从而提供与 Java 的轻松通信），例如 Clojure 或 Scala。为什么不用这些语言来编写并发部分，然后用Java来做其他的事情呢?

唉，你不能轻易逃脱：

- 即使**你从未显示地创建一个线程，你使用的框架也可能**——例如，Swing 图形用户界面（GUI）库，或者像 **Timer** 类（计时器）那样简单的东西。
- 最糟糕的是：当你创建组件时，必须假设这些组件可能会在多线程环境中重用。即使你的解决方案是放弃并声明你的组件是“非线程安全的”，你仍然必须充分了解这样一个语句的重要性及其含义。

人们有时会认为并发对于介绍语言的书来说太高级了，因此不适合放在其中。他们认为并发是一个独立的主题，并且对于少数出现在日常的程序设计中的情况（例如图形用户界面），可以用特殊的惯用法来处理。如果你可以回避，为什么还要介绍这么复杂的主题呢？

唉，如果是这样就好了。遗憾的是，对于线程何时出现在 Java 程序中，这不是你能决定的。仅仅是你自己没有启动线程，并不代表你就可以回避编写使用线程的代码。例如，Web 系统是最常见的 Java 应用之一，**本质上是多线程的 Web 服务器**，通常包含多个处理器，而并行是利用这些处理器的理想方式。尽管这样的系统看起来很简单，但你必须理解并发才能正确地编写它。

Java 是一种多线程语言，不管你有没有意识到并发问题，它就在那里。因此，有很多使用并发的 Java 程序，要么只是偶然运行，要么大部分时间都在运行，并且会因为未被发现的并发缺陷而时不时地神秘崩溃。有时这种崩溃是相对温和的，但有时它意味着丢失有价值的数据，如果你没有意识到并发问题，你最终可能会把问题归咎于其他地方而不是你的代码中。如果将程序移动到多处理器系统中，这些类型的问题还会被暴露或放大。基本上，**了解并发可以使你意识到明显正确的程序也可能会表现出错误的行为。**

<!-- The Brutal Truth -->

## 残酷的真相

当人类开始烹饪他们的食物时，他们大大减少了他们的身体分解和消化食物所需的能量。烹饪创造了一个“外化的胃”，从而释放出能量去发展其他的能力。火的使用促成了文明。

我们现在通过计算机和网络技术创造了一个“外化大脑”，开始了第二次基本转变。虽然我们只是触及表面，但已经引发了其他转变，例如设计生物机制的能力，并且已经看到文化演变的显著加速（过去，人们通过旅游进行文化交流，但现在他们开始在互联网上做这件事）。这些转变的影响和好处已经超出了科幻作家预测它们的能力（他们在预测文化和个人变化，甚至技术转变的次要影响方面都特别困难）。

有了这种根本性的人类变化，看到许多破坏和失败的实验并不令人惊讶。实际上，进化依赖于无数的实验，其中大多数都失败了。这些实验是向前发展的必要条件。

Java 是在充满自信，热情和睿智的氛围中创建的。在发明一种编程语言时，很容易感觉语言的初始可塑性会持续存在一样，你可以把某些东西拿出来，如果不能解决问题，那么就修复它。编程语言以这种方式是独一无二的 - 它们经历了类似水的改变：气态，液态和最终的固态。在气态阶段，灵活性似乎是无限的，并且很容易认为它总是那样。一旦人们开始使用你的语言，变化就会变得更加严重，环境变得更加粘稠。语言设计的过程本身就是一门艺术。

紧迫感来自互联网的最初兴起。它似乎是一场比赛，第一个通过起跑线的人将“获胜”（事实上，Java，JavaScript 和 PHP 等语言的流行程度可以证明这一点）。唉，通过匆忙设计语言而产生的认知负荷和技术债务最终会赶上我们。

[Turing completeness](https://en.wikipedia.org/wiki/Turing_completeness) 是不足够的;语言需要更多的东西：它们必须能够创造性地表达，而不是用不必要的东西来衡量我们。解放我们的心理能力只是为了扭转并再次陷入困境，这是毫无意义的。我承认，尽管存在这些问题，我们已经完成了令人惊奇的事情，但我也知道如果没有这些问题我们能做得更多。

热情使原始 Java 设计师加入了一些似乎有必要的特性。信心（以及气态的初始语言）让他们认为任何问题随后都可以解决。在时间轴的某个地方，有人认为任何加入 Java 的东西是固定的和永久性的 -他们非常有信心，并相信第一个决定永远是正确的，因此我们看到 Java 的体系中充斥着糟糕的决策。其中一些决定最终没有什么后果;例如，你可以告诉人们不要使用 Vector，但只能在语言中继续保留它以便对之前版本的支持。

线程包含在 Java 1.0 中。当然，对 java 来说支持并发是一个很基本的设计决定，该特性影响了这个语言的各个角落，我们很难想象以后在以后的版本添加它。公平地说，当时并不清楚基本的并发性是多少。像 C 这样的其他语言能够将线程视为一个附加功能，因此 Java 设计师也纷纷效仿，包括一个 Thread 类和必要的 JVM 支持（这比你想象的要复杂得多）。

C 语言是面向过程语言，这限制了它的野心。这些限制使附加线程库合理。当采用原始模型并将其粘贴到复杂语言中时，Java 的大规模扩展迅速暴露了基本问题。在 Thread 类中的许多方法的弃用以及后续的高级库浪潮中，这种情况变得明显，这些库试图提供更好的并发抽象。

不幸的是，为了在更高级别的语言中获得并发性，所有语言功能都会受到影响，包括最基本的功能，例如标识符代表可变值。在简化并发编程中，所有函数和方法中为了**保持事物不变和防止副作用**都要做出巨大的改变（这些是纯函数式编程语言的基础），但当时对于主流语言的创建者来说似乎是奇怪的想法。最初的 Java 设计师要么没有意识到这些选择，要么认为它们太不同了，并且会劝退许多潜在的语言使用者。我们可以慷慨地说，语言设计社区当时根本没有足够的经验来理解调整在线程库中的影响。

Java 实验告诉我们，结果是悄然灾难性的。程序员很容易陷入认为 Java 线程并不那么困难的陷阱。表面上看起来正常工作的程序实际上充满了微妙的并发 bug。

为了获得正确的并发性，语言功能必须从头开始设计并考虑并发性。木已成舟；Java 将不再是**为并发而设计的语言**，而**只是一种允许并发的语言。**

尽管有这些基本的不可修复的缺陷，但令人印象深刻的是它已经走了这么远。Java 的后续版本添加了库，以便在使用并发时提升抽象级别。事实上，我根本不会想到有可能在 Java 8 中进行改进：并行流和 **CompletableFutures**  - 这是惊人的史诗般的变化，我会惊奇地重复的查看它[^3]。

这些改进非常有用，我们将在本章重点介绍并行流和 **CompletableFutures** 。虽然它们可以大大简化你对并发和后续代码的思考方式，但基本问题仍然存在：由于 Java 的原始设计，代码的所有部分仍然很脆弱，你仍然必须理解这些复杂和微妙的问题。Java 中的线程绝不是简单或安全的;那种经历必须降级为另一种更新的语言。

<!-- The Rest of the Chapter -->

## 本章其余部分

这是我们将在本章的其余部分介绍的内容。请记住，本章的重点是**使用最新的高级 Java 并发结构。**相比于旧的替代品，使用这些会使你的生活更加轻松。但是，你仍会在遗留代码中遇到一些低级工具。有时，你可能会被迫自己使用其中的一些。附录：[并发底层原理 ](./Appendix-Low-Level-Concurrency.md) 包含一些更原始的 Java 并发元素的介绍。

- **Parallel Streams（并行流）**
  到目前为止，我已经强调了 Java 8 Streams 提供的改进语法。现在该语法（作为一个粉丝，我希望）会使你感到舒适，你可以获得额外的好处：你可以通过简单地将 parallel() 添加到表达式来并行化流。这是一种简单，强大，坦率地说是利用多处理器的惊人方式

添加 parallel() 来提高速度似乎是微不足道的，但是，唉，它就像你刚刚在[残酷的真相 ](#The-Brutal-Truth) 中学到的那样简单。我将演示并解释一些盲目添加 parallel() 到 Stream 表达式的缺陷。

- 创建和运行任务
  任务是一段**可以独立运行的代码**。为了解释创建和运行任务的一些基础知识，本节介绍了一种比并行流或 CompletableFutures 更简单的机制：Executor。执行者管理一些低级 Thread 对象（Java 中最原始的并发形式）。你创建一个任务，然后将其交给 Executor 去运行。

有多种类型的 Executor 用于不同的目的。在这里，我们将展示规范形式，代表创建和运行任务的最简单和最佳方法。

- 终止长时间运行的任务
  任务独立运行，因此需要一种机制来关闭它们。典型的方法使用了一个标志，这引入了共享内存的问题，我们将使用 Java 的“Atomic”库来回避它。
- Completable Futures
  当你将衣服带到干洗店时，他们会给你一张收据。你继续完成其他任务，当你的衣服洗干净时你可以把它取走。收据是你与干洗店在后台执行的任务的连接。这是 **Java 5 中引入的 Future 的方法**。(好像是异步回调)

Future 比以前的方法更方便，但你仍然必须出现并用收据取出干洗，如果任务没有完成你还需要等待。对于一系列操作，Futures 并没有真正帮助那么多。

Java 8 CompletableFuture 是一个更好的解决方案：它允许你将操作链接在一起，因此你不必将代码写入接口排序操作。有了 CompletableFuture 完美的结合，就可以更容易地做出“采购原料，组合成分，烹饪食物，提供食物，收拾餐具，储存餐具”等一系列链式操作。

- 死锁
  某些任务必须去**等待 - 阻塞**来获得其他任务的结果。被阻止的任务有可能等待另一个被阻止的任务，另一个被阻止的任务也在等待其他任务，等等。如果被阻止的任务链循环到第一个，没有人可以取得任何进展，你就会陷入死锁。

如果在运行程序时没有立即出现死锁，则会出现最大的问题。你的系统可能容易出现死锁，并且只会在某些条件下死锁。程序可能在某个平台上（例如在你的开发机器）运行正常，但是当你将其部署到不同的硬件时会开始死锁。

死锁通常源于细微的编程错误;一系列无辜的决定，最终意外地创建了一个依赖循环。本节包含一个经典示例，演示了死锁的特性。

* 努力，复杂，成本

我们将通过模拟创建披萨的过程完成本章，首先使用并行流实现它，然后是 CompletableFutures。这不仅仅是两种方法的比较，更重要的是探索你应该投入多少工作来使你的程序变得更快。

## 并行流

Java 8 流的一个显著优点是，在某些情况下，它们可以很容易地并行化。这来自库的仔细设计，特别是流使用内部迭代的方式 - 也就是说，**它们控制着自己的迭代器**。特别是，他们使用一种特殊的迭代器，称为 Spliterator，它被限制为易于自动分割。我们只需要念 `.parallel()` 就会产生魔法般的结果，流中的所有内容都作为一组并行任务运行。**如果你的代码是使用 Streams 编写的，那么并行化以提高速度似乎是一种琐事**

**线程安全的 AtomicInteger  类**



```java
// concurrent/ParallelStreamPuzzle3.java
// {VisuallyInspectOutput}
import java.util.*;
import java.util.stream.*;
public class ParallelStreamPuzzle3 {
    public static void main(String[] args) {
    List<Integer> x = IntStream.range(0, 30)
        .peek(e -> System.out.println(e + ": " +Thread.currentThread()
        .getName()))
        .limit(10)
        .parallel()
        .boxed()
        .collect(Collectors.toList());
        System.out.println(x);
    }
}
```

，我添加了一个对 **peek()**  的调用，这是一个**主要用于调试的流函数**：它从流中提取一个值并执行**某些操作但不影响从流向下传递的元素**。

看到 **boxed()**  的添加，它接受 **int** 流并将其转换为 **Integer** 流。



记住这句格言：“**首先使它工作，然后使它更快地工作**。”

它更快吗？一个更好的问题是：什么时候开始有意义？当然不是这么小的一套；上下文切换的代价远远超过并行性的任何加速。很难想象什么时候用并行生成一个简单的数字序列会有意义。如果**你要生成的东西需要很高的成本，它可能有意义 - 但这都是猜测**。只有通过测试我们才能知道用并行是否有效。记住这句格言：“首先使它工作，然后使它更快地工作 - 只有当你必须这样做时。”将 **parallel()**  和 **limit()**  结合使用仅供专家操作（把话说在前面，我不认为自己是这里的专家）。

- 并行流只看起来很容易

实际上，在许多情况下，并行流确实可以毫不费力地更快地产生结果。但正如你所见，仅仅将 **parallel()**  加到你的 Stream 操作上并不一定是安全的事情。在使用 **parallel()**  之前，你必须了解**并行性如何帮助或损害你的操作**。一个基本认知错误就是认为使用并行性总是一个好主意。事实上并不是。Stream 意味着你不需要重写所有代码便可以并行运行它。但是流的出现并不意味着你可以不用理解并行的原理以及不用考虑并行是否真的有助于实现你的目标。



## 创建和运行任务

如果无法通过并行流实现并发，则必须创建并运行自己的任务。稍后你将看到运行任务的理想 Java 8 方法是 CompletableFuture，但我们将使用更基本的工具介绍概念。

Java 并发的历史始于非常原始和有问题的机制，并且充满了各种尝试的改进。这些主要归入附录：[低级并发 (Appendix: Low-Level Concurrency)](./Appendix-Low-Level-Concurrency.md)。在这里，我们将展示一个规范形式，表示创建和运行任务的最简单，最好的方法。与并发中的所有内容一样，存在各种变体，但这些变体要么降级到该附录，要么超出本书的范围。

- Tasks and Executors

**在 Java 的早期版本中**，你通过直接**创建自己的 Thread 对象来使用线程**，甚至将它们子类化以创建你自己的特定“任务线程”对象。你手动调用了构造函数并自己启动了线程。

创建所有这些线程的开销变得非常重要，**现在不鼓励采用手动操作方法**。**在 Java 5 中，添加了类来为你处理线程池**。你可以将任务创建为单独的类型，然后将其交给 ExecutorService 以运行该任务，而不是为每种不同类型的任务创建新的 Thread 子类型。ExecutorService 为你管理线程，并且**在运行任务后重新循环线程而不是丢弃线程**。

首先，我们将创建一个几乎不执行任务的任务。它“sleep”（暂停执行）100 毫秒，显示其标识符和正在执行任务的线程的名称，然后完成：

```java
// concurrent/NapTask.java
import onjava.Nap;
public class NapTask implements Runnable {
    final int id;
    public NapTask(int id) {
        this.id = id;
        }
    @Override
    public void run() {
        new Nap(0.1);// Seconds
        System.out.println(this + " "+
            Thread.currentThread().getName());
        }
    @Override
    public String toString() {
        return"NapTask[" + id + "]";
    }
}
```

这只是一个 **Runnable** ：一个包含 **run()**  方法的类。它没有包含实际运行任务的机制。我们使用 **Nap** 类中的“sleep”：

```java
// onjava/Nap.java
package onjava;
import java.util.concurrent.*;
public class Nap {
    public Nap(double t) { // Seconds
        try {
            TimeUnit.MILLISECONDS.sleep((int)(1000 * t));
        } catch(InterruptedException e){
            throw new RuntimeException(e);
        }
    }
    public Nap(double t, String msg) {
        this(t);
        System.out.println(msg);
    }
}
```

为了消除异常处理的视觉干扰，这被定义为实用程序。第二个构造函数在超时时显示一条消息

为了消除异常处理的视觉干扰，这被定义为实用程序。第二个构造函数在超时时显示一条消息

对 **TimeUnit.MILLISECONDS.sleep()**  的调用**获取“当前线程”并在参数中将其置于休眠状态**，这意味着**该线程被挂起**。这并不意味着底层处理器停止。操作系统将其切换到其他任务，例如在你的计算机上运行另一个窗口。OS 任务管理器定期检查 **sleep()**  是否超时。当它执行时，线程被“唤醒”并给予更多处理时间。

你可以看到 **sleep()**  抛出一个受检的 **InterruptedException** ;这是原始 Java 设计中的一个工件，它通过突然断开它们来终止任务。因为它往往会产生不稳定的状态，所以后来不鼓励终止。但是，我们必须在需要或仍然发生终止的情况下捕获异常。

要执行任务，我们将从**最简单的方法--SingleThreadExecutor 开始:**

```java
//concurrent/SingleThreadExecutor.java
import java.util.concurrent.*;
import java.util.stream.*;
import onjava.*;
public class SingleThreadExecutor {
    public static void main(String[] args) {
        ExecutorService exec =
            Executors.newSingleThreadExecutor();
        IntStream.range(0, 10)
            .mapToObj(NapTask::new)
            .forEach(exec::execute);
        System.out.println("All tasks submitted");
        exec.shutdown();
        while(!exec.isTerminated()) {
            System.out.println(
            Thread.currentThread().getName()+
            " awaiting termination");
            new Nap(0.1);
        }
    }
}
```

输出结果：

```
All tasks submitted
main awaiting termination
main awaiting termination
NapTask[0] pool-1-thread-1
main awaiting termination
NapTask[1] pool-1-thread-1
main awaiting termination
NapTask[2] pool-1-thread-1
main awaiting termination
NapTask[3] pool-1-thread-1
main awaiting termination
NapTask[4] pool-1-thread-1
main awaiting termination
NapTask[5] pool-1-thread-1
main awaiting termination
NapTask[6] pool-1-thread-1
main awaiting termination
NapTask[7] pool-1-thread-1
main awaiting termination
NapTask[8] pool-1-thread-1
main awaiting termination
NapTask[9] pool-1-thread-1
```

首先请注意，没有 **SingleThreadExecutor** 类。**newSingleThreadExecutor()**  是 **Executors**  中的一个工厂方法，它创建特定类型的 **ExecutorService** [^4]

我创建了十个 NapTasks 并将它们提交给 ExecutorService，这意味着它们开始自己运行。然而，在此期间，main() 继续做事。当我**运行exec.shutdown() 时**，它告诉 **ExecutorService 完成已经提交的任务，但不接受任何新任务**。此时，这些任务仍然在运行，因此我们必须等到它们在退出 main() 之前完成。这是**通过检查 exec.isTerminated() 来实现的，这在所有任务完成后变为 true。**

请注意，main() 中线程的名称是 main，并且只有一个其他线程 pool-1-thread-1。此外，交错输出显示两个线程确实同时运行。

如果你**只是调用 exec.shutdown()，程序将完成所有任务**。也就是说，不需要 **while(!exec.isTerminated())** 。

```java
// concurrent/SingleThreadExecutor2.java
import java.util.concurrent.*;
import java.util.stream.*;
public class SingleThreadExecutor2 {
    public static void main(String[] args)throws InterruptedException {
        ExecutorService exec
        =Executors.newSingleThreadExecutor();
        IntStream.range(0, 10)
            .mapToObj(NapTask::new)
            .forEach(exec::execute);
        exec.shutdown();
    }
}
```

输出结果：

```
NapTask[0] pool-1-thread-1
NapTask[1] pool-1-thread-1
NapTask[2] pool-1-thread-1
NapTask[3] pool-1-thread-1
NapTask[4] pool-1-thread-1
NapTask[5] pool-1-thread-1
NapTask[6] pool-1-thread-1
NapTask[7] pool-1-thread-1
NapTask[8] pool-1-thread-1
NapTask[9] pool-1-thread-1
```

一旦你调用了 exec.shutdown()，**尝试提交新任务将抛出 RejectedExecutionException**。

```java
// concurrent/MoreTasksAfterShutdown.java
import java.util.concurrent.*;
public class MoreTasksAfterShutdown {
    public static void main(String[] args) {
        ExecutorService exec
        =Executors.newSingleThreadExecutor();
        exec.execute(newNapTask(1));
        exec.shutdown();
        try {
            exec.execute(newNapTask(99));
        } catch(RejectedExecutionException e) {
            System.out.println(e);
        }
    }
}
```

输出结果：

```
java.util.concurrent.RejectedExecutionException: TaskNapTask[99] rejected from java.util.concurrent.ThreadPoolExecutor@4e25154f[Shutting down, pool size = 1,active threads = 1, queued tasks = 0, completed tasks =0]NapTask[1] pool-1-thread-1
```

**exec.shutdown()**  的替代方法是 **exec.shutdownNow()**  ，它除了不接受新任务外，还会**尝试通过中断任务来停止任何当前正在运行的任务**。同样，**中断是错误的，容易出错并且不鼓励。**

- **

  - 使用更多线程

  使用线程的重点是（几乎总是）更快地完成任务，那么我们**==为什么要限制自己使用 SingleThreadExecutor==** 呢？查看执行 **Executors** 的 Javadoc，你将看到更多选项。例如 CachedThreadPool：

  ```java
  // concurrent/CachedThreadPool.java
  import java.util.concurrent.*;
  import java.util.stream.*;
  public class CachedThreadPool {
      public static void main(String[] args) {
          ExecutorService exec
          =Executors.newCachedThreadPool();
          IntStream.range(0, 10)
          .mapToObj(NapTask::new)
          .forEach(exec::execute);
          exec.shutdown();
      }
  }
  ```

  输出结果：

  ```
  NapTask[7] pool-1-thread-8
  NapTask[4] pool-1-thread-5
  NapTask[1] pool-1-thread-2
  NapTask[3] pool-1-thread-4
  NapTask[0] pool-1-thread-1
  NapTask[8] pool-1-thread-9
  NapTask[2] pool-1-thread-3
  NapTask[9] pool-1-thread-10
  NapTask[6] pool-1-thread-7
  NapTask[5] pool-1-thread-6
  ```

  **当你运行这个程序时，你会发现它完成得更快**。这是有道理的，每个任务都有自己的线程，所以它们都并行运行，而不是**使用相同的线程来顺序运行每个任务**。这似乎没毛病，**很难理解为什么有人会使用 SingleThreadExecutor。**

要理解这个问题，我们需要一个更复杂的任务：

```java
// concurrent/InterferingTask.java
public class InterferingTask implements Runnable {
    final int id;
    private static Integer val = 0;
    public InterferingTask(int id) {
        this.id = id;
    }
    @Override
    public void run() {
        for(int i = 0; i < 100; i++)
        val++;
    System.out.println(id + " "+
        Thread.currentThread().getName() + " " + val);
    }
}

```

每个任务增加 val 一百次。这似乎很简单。让我们用 CachedThreadPool 尝试一下：

```java
// concurrent/CachedThreadPool2.java
import java.util.concurrent.*;
import java.util.stream.*;
public class CachedThreadPool2 {
    public static void main(String[] args) {
    ExecutorService exec
    =Executors.newCachedThreadPool();
    IntStream.range(0, 10)
    .mapToObj(InterferingTask::new)
    .forEach(exec::execute);
    exec.shutdown();
    }
}
```

输出结果：

```
0 pool-1-thread-1 200
1 pool-1-thread-2 200
4 pool-1-thread-5 300
5 pool-1-thread-6 400
8 pool-1-thread-9 500
9 pool-1-thread-10 600
2 pool-1-thread-3 700
7 pool-1-thread-8 800
3 pool-1-thread-4 900
6 pool-1-thread-7 1000
```

输出不是我们所期望的，并且从一次运行到下一次运行会有所不同。问题是所有的任务都试图写入 val 的单个实例，并且他们正在踩着彼此的脚趾。**我们称这样的类是线程不安全的**。让我们看看 SingleThreadExecutor 会发生什么：

```java
// concurrent/SingleThreadExecutor3.java
import java.util.concurrent.*;
import java.util.stream.*;
public class SingleThreadExecutor3 {
    public static void main(String[] args)throws InterruptedException {
        ExecutorService exec
        =Executors.newSingleThreadExecutor();
        IntStream.range(0, 10)
        .mapToObj(InterferingTask::new)
        .forEach(exec::execute);
        exec.shutdown();
    }
}
```

输出结果：

```
0 pool-1-thread-1 100
1 pool-1-thread-1 200
2 pool-1-thread-1 300
3 pool-1-thread-1 400
4 pool-1-thread-1 500
5 pool-1-thread-1 600
6 pool-1-thread-1 700
7 pool-1-thread-1 800
8 pool-1-thread-1 900
9 pool-1-thread-1 1000
```

现在我们每次都得到一致的结果，尽管 **InterferingTask** 缺乏线程安全性。这是 SingleThreadExecutor 的主要好处 - **因为它一次运行一个任务，这些任务不会相互干扰，因此强加了线程安全性**。这种现象称为**线程封闭**，因为**在单线程上运行任务限制了它们的影响**。**线程封闭限制了加速，但可以节省很多困难的调试和重写。**

- 产生结果

因为 **InterferingTask** 是一个 **Runnable** ，**它没有返回值，因此只能使用副作用产生结果** - **操纵缓冲值而不是返回结果**。副作用是并发编程中的主要问题之一，因为我们看到了 **CachedThreadPool2.java** 。**InterferingTask** 中的 **val** 被称为**可变共享状态**，这就是问题所在：多个任务同时修改同一个变量会产生竞争。结果取决于首先在终点线上执行哪个任务，并修改变量（以及其他可能性的各种变化）。

**==避免竞争条件的最好方法是避免可变的共享状态==**。我们可以称之为**==自私的孩子原则：什么都不分享==**。

使用 **InterferingTask** ，最好==**删除副作用并返回任务结果**==。为此，我们创建 **Callable** 而不是 **Runnable** ：

```java
// concurrent/CountingTask.java
import java.util.concurrent.*;
public class CountingTask implements Callable<Integer> {
    final int id;
    public CountingTask(int id) { this.id = id; }
    @Override
    public Integer call() {
    Integer val = 0;
    for(int i = 0; i < 100; i++)
        val++;
    System.out.println(id + " " +
        Thread.currentThread().getName() + " " + val);
    return val;
    }
}

```

**call() 完全独立于所有其他 CountingTasks 生成其结果**，这意味着没有可变的共享状态

**ExecutorService** 允许你使用 **invokeAll()** 启动集合中的每个 Callable：

```java
// concurrent/CachedThreadPool3.java
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;
public class CachedThreadPool3 {
    public static Integer extractResult(Future<Integer> f) {
        try {
            return f.get();
        } catch(Exception e) {
            throw new RuntimeException(e);
        }
    }
    public static void main(String[] args)throws InterruptedException {
        ExecutorService exec =
        Executors.newCachedThreadPool();
        List<CountingTask> tasks =
        IntStream.range(0, 10)
            .mapToObj(CountingTask::new)
            .collect(Collectors.toList());
        List<Future<Integer>> futures =
            exec.invokeAll(tasks);
        Integer sum = futures.stream()
            .map(CachedThreadPool3::extractResult)
            .reduce(0, Integer::sum);
        System.out.println("sum = " + sum);
        exec.shutdown();
    }
}
```

输出结果：

```
1 pool-1-thread-2 100
0 pool-1-thread-1 100
4 pool-1-thread-5 100
5 pool-1-thread-6 100
8 pool-1-thread-9 100
9 pool-1-thread-10 100
2 pool-1-thread-3 100
3 pool-1-thread-4 100
6 pool-1-thread-7 100
7 pool-1-thread-8 100
sum = 1000

```

**只有在所有任务完成后**，**invokeAll()** 才会返回一个 **Future** 列表，每个任务一个 **Future** 。**Future** 是 Java 5 中引入的机制，**允许你提交任务而无需等待它完成**。在这里，我们使用 **ExecutorService.submit()** :

```java
// concurrent/Futures.java
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;
public class Futures {
    public static void main(String[] args)throws InterruptedException, ExecutionException {
    ExecutorService exec
        =Executors.newSingleThreadExecutor();
    Future<Integer> f =
        exec.submit(newCountingTask(99));
    System.out.println(f.get()); // [1]
    exec.shutdown();
    }
}
```

输出结果：

```
99 pool-1-thread-1 100
100
```

- [1] 当你的任务在尚未完成的 **Future** 上调用 **get()** 时，**调用会阻塞（等待）直到结果可用。**

但这意味着，在 **CachedThreadPool3.java** 中，**Future** 似乎是多余的，因为 **invokeAll()** 甚至在所有任务完成之前都不会返回。但是，**这里的 Future 并不用于延迟结果，而是用于捕获任何可能发生的异常。**

还要注意在 **CachedThreadPool3.java.get()** 中抛出异常，因此 **extractResult()** 在 Stream 中执行此提取。

因为当你调用 **get()** 时，**Future** 会阻塞，所以它**只能解决等待任务完成才暴露问题**。最终，**Futures** 被认为是一种无效的解决方案，==**现在不鼓励，我们推荐 Java 8 的 CompletableFuture**== ，这将在本章后面探讨。当然，你仍会在遗留库中遇到 Futures。

我们可以使用并行 Stream 以更简单，更优雅的方式解决这个问题:



```java
// concurrent/CountingStream.java
// {VisuallyInspectOutput}
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;
public class CountingStream {
    public static void main(String[] args) {
        System.out.println(
            IntStream.range(0, 10)
                .parallel()
                .mapToObj(CountingTask::new)
                .map(ct -> ct.call())
                .reduce(0, Integer::sum));
    }
}
```

输出结果：

```
1 ForkJoinPool.commonPool-worker-3 100
8 ForkJoinPool.commonPool-worker-2 100
0 ForkJoinPool.commonPool-worker-6 100
2 ForkJoinPool.commonPool-worker-1 100
4 ForkJoinPool.commonPool-worker-5 100
9 ForkJoinPool.commonPool-worker-7 100
6 main 100
7 ForkJoinPool.commonPool-worker-4 100
5 ForkJoinPool.commonPool-worker-2 100
3 ForkJoinPool.commonPool-worker-3 100
1000
```

这不仅更容易理解，而且我们需要做的就是将 `parallel()` 插入到其他顺序操作中，然后一切都在同时运行。

- **Lambda 和方法引用作为任务**

在 **java8**  有了 **lambdas**  和方法引用，你不需要受限于只能使用  **Runnable**  和 **Callable**  。因为 java8 的 **lambdas**  和方法引用**可以通过匹配方法签名来使用（即，它支持结构一致性）**，所以我们可以将非 **Runnable**  或 **Callable**  的参数传递给 `ExecutorService` : 

```java
// concurrent/LambdasAndMethodReferences.java
import java.util.concurrent.*;
class NotRunnable {
    public void go() {
        System.out.println("NotRunnable");
    }
}
class NotCallable {
    public Integer get() {
        System.out.println("NotCallable");
        return 1;
    }
}
public class LambdasAndMethodReferences {
    public static void main(String[] args)throws InterruptedException {
    ExecutorService exec =
        Executors.newCachedThreadPool();
    exec.submit(() -> System.out.println("Lambda1"));
    exec.submit(new NotRunnable()::go);
    exec.submit(() -> {
        System.out.println("Lambda2");
        return 1;
    });
    exec.submit(new NotCallable()::get);
    exec.shutdown();
    }
}
```

输出结果：

```
Lambda1
NotCallable
NotRunnable
Lambda2

```

这里，前两个 **submit()** 调用可以改为调用 **execute()** 。所有 **submit()** 调用都返回 **Futures** ，你可以在后两次调用的情况下提取结果。

<!-- Terminating Long-Running Tasks -->

## 终止耗时任务

并发程序**通常使用长时间运行的任务**。可调用任务在完成时返回值;虽然这给它一个有限的寿命，但仍然可能很长。可运行的任务有时被设置为永远运行的后台进程。你经常需要一种方法在正常完成之前停止 **Runnable** 和 **Callable** 任务，例如当你关闭程序时。

最初的 Java 设计提供了中断运行任务的机制（为了向后兼容，仍然存在）;中断机制包括阻塞问题。中断任务既乱又复杂，因为你必须了解可能发生中断的所有可能状态，以及可能导致的数据丢失。**使用中断被视为反对模式**，但我们仍然被迫接受。

InterruptedException，因为设计的向后兼容性残留。

任务终止的最佳方法是**设置任务周期性检查的标志**。然后**任务可以通过自己的 shutdown 进程并正常终止**。不是在任务中随机关闭线程，而是**要求任务在到达了一个较好时自行终止**。这总是产生比中断更好的结果，以及更容易理解的更合理的代码。

以这种方式终止任务听起来很简单：设置任务可以看到的 **boolean**  flag。编写任务，以便定期检查标志并执行正常终止。这实际上就是你所做的，但是有一个复杂的问题：我们的旧克星，共同的可变状态。如果该标志可以被另一个任务操纵，则存在碰撞可能性。

在研究 Java 文献时，你会发现很多解决这个问题的方法，经常使用 **volatile** 关键字。我们将使用更简单的技术并避免所有易变的参数，这些都在[附录：低级并发 ](./Appendix-Low-Level-Concurrency.md) 中有所涉及。

==**Java 5 引入了 Atomic 类，它提供了一组可以使用的类型，而不必担心并发问题**==。我们将添加 **AtomicBoolean** 标志，告诉任务清理自己并退出。



```java
// concurrent/QuittableTask.java
import java.util.concurrent.atomic.AtomicBoolean;import onjava.Nap;
public class QuittableTask implements Runnable {
    final int id;
    public QuittableTask(int id) {
        this.id = id;
    }
    private AtomicBoolean running =
        new AtomicBoolean(true);
    public void quit() {
        running.set(false);
    }
    @Override
    public void run() {
        while(running.get())         // [1]
            new Nap(0.1);
        System.out.print(id + " ");  // [2]
    }
}

```

虽然多个任务可以在同一个实例上成功调用 **quit()** ，但是 **AtomicBoolean** 可以防止多个任务同时实际修改 **running** ，从而使 **quit()** 方法成为线程安全的。

- [1]:只要运行标志为 true，此任务的 run() 方法将继续。

- [2]: 显示仅在任务退出时发生。

需要 **running AtomicBoolean** 证明编写 Java program 并发时最基本的困难之一是，如果 **running** 是一个普通的布尔值，你可能无法在执行程序中看到问题。实际上，在这个例子中，你可能永远不会有任何问题 - 但是代码仍然是不安全的。编写表明该问题的测试可能很困难或不可能。因此，你没有任何反馈来告诉你已经做错了。通常，你**编写线程安全代码的唯一方法就是通过了解事情可能出错的所有细微之处**。

作为测试，我们将启动很多 QuittableTasks 然后关闭它们。尝试使用较大的 COUNT 值



```java
// concurrent/QuittingTasks.java
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import onjava.Nap;
public class QuittingTasks {
    public static final int COUNT = 150;
    public static void main(String[] args) {
    	ExecutorService es =
   	 	Executors.newCachedThreadPool();
    	List<QuittableTask> tasks =
   		 IntStream.range(1, COUNT)
            .mapToObj(QuittableTask::new)
            .peek(qt -> es.execute(qt))
            .collect(Collectors.toList());
    	new Nap(1);
    	tasks.forEach(QuittableTask::quit);    
        es.shutdown();
    }
}
```

输出结果：

```
24 27 31 8 11 7 19 12 16 4 23 3 28 32 15 20 63 60 68 6764 39 47 52 51 55 40 43 48 59 44 56 36 35 71 72 83 10396 92 88 99 100 87 91 79 75 84 76 115 108 112 104 107111 95 80 147 120 127 119 123 144 143 116 132 124 128
136 131 135 139 148 140 2 126 6 5 1 18 129 17 14 13 2122 9 10 30 33 58 37 125 26 34 133 145 78 137 141 138 6274 142 86 65 73 146 70 42 149 121 110 134 105 82 117106 113 122 45 114 118 38 50 29 90 101 89 57 53 94 4161 66 130 69 77 81 85 93 25 102 54 109 98 49 46 97
```

我使用 **peek()** 将 **QuittableTasks** 传递给 **ExecutorService** ，然后将这些任务收集到 **List.main()** 中，只要任何任务仍在运行，就会阻止程序退出。即使为每个任务按顺序调用 quit() 方法，任务也不会按照它们创建的顺序关闭。**独立运行的任务不会确定性地响应信号。**

## CompletableFuture 类

作为介绍，这里是使用 CompletableFutures 在 QuittingTasks.java 中：

```java
// concurrent/QuittingCompletable.java
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import onjava.Nap;
public class QuittingCompletable {
    public static void main(String[] args) {
    List<QuittableTask> tasks =
        IntStream.range(1, QuittingTasks.COUNT)
            .mapToObj(QuittableTask::new)
            .collect(Collectors.toList());
        List<CompletableFuture<Void>> cfutures =
        tasks.stream()
            .map(CompletableFuture::runAsync)
            .collect(Collectors.toList());
        new Nap(1);
        tasks.forEach(QuittableTask::quit);
        cfutures.forEach(CompletableFuture::join);
    }
}
```

输出结果：

```
7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 2526 27 28 29 30 31 32 33 34 6 35 4 38 39 40 41 42 43 4445 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 6263 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 8081 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 9899 100 101 102 103 104 105 106 107 108 109 110 111 1121 113 114 116 117 118 119 120 121 122 123 124 125 126127 128 129 130 131 132 133 134 135 136 137 138 139 140141 142 143 144 145 146 147 148 149 5 115 37 36 2 3
```

任务是一个 `List<QuittableTask>`，就像在 `QuittingTasks.java` 中一样，但是在这个例子中，没有 `peek()` 将每个 `QuittableTask` 提交给 `ExecutorService`。相反，在创建 `cfutures` 期间，每个任务都交给 `CompletableFuture::runAsync`。这执行 `VerifyTask.run()` 并返回 `CompletableFuture<Void>` 。因为 `run()` 不返回任何内容，所以**在这种情况下我只使用 `CompletableFuture` 调用 `join()` 来等待它完成**。

在本例中需要注意的重要一点是，运行任务不需要使用 `ExecutorService`。而是**直接交给 `CompletableFuture` 管理** (不过你可以向它提供自己定义的 `ExectorService`)。您也不需要调用 `shutdown()`;事实上，除非你像我在**这里所做的那样显式地调用 `join()`，否则程序将尽快退出，而不必等待任务完成**。

这个例子只是一个起点。你很快就会看到 `ComplempleFuture` 能够做得更多。

### 基本用法

这是一个带有静态方法 **work()** 的类，它对该类的对象执行某些工作：

```java
// concurrent/Machina.java
import onjava.Nap;
public class Machina {
    public enum State {
        START, ONE, TWO, THREE, END;
        State step() {
            if(equals(END))
            return END;
          return values()[ordinal() + 1];
        }
    }
    private State state = State.START;
    private final int id;
    public Machina(int id) {
        this.id = id;
    }
    public static Machina work(Machina m) {
        if(!m.state.equals(State.END)){
            new Nap(0.1);
            m.state = m.state.step();
        }
        System.out.println(m);
        return m;
    }
    @Override
    public String toString() {
        return"Machina" + id + ": " + (state.equals(State.END)? "complete" : state);
    }
}

```

这是一个有限状态机，一个微不足道的机器，因为它没有分支......它只是从头到尾遍历一条路径。**work()** 方法将机器从一个状态移动到下一个状态，并且需要 100 毫秒才能完成“工作”。

**CompletableFuture** 可以被用来做的一件事是, 使用 **completedFuture()** 将它感兴趣的对象进行包装。

```java
// concurrent/CompletedMachina.java
import java.util.concurrent.*;
public class CompletedMachina {
    public static void main(String[] args) {
        CompletableFuture<Machina> cf =
        CompletableFuture.completedFuture(
            new Machina(0));
        try {
            Machina m = cf.get();  // Doesn't block
        } catch(InterruptedException |
            ExecutionException e) {
        throw new RuntimeException(e);
        }
    }
}
```

**completedFuture()** 创建一个“已经完成”的 **CompletableFuture** 。对这样一个未来做的唯一有用的事情是 **get()** 里面的对象，所以这看起来似乎没有用。注意 **CompletableFuture** 被输入到它包含的对象。这个很重要。

通常，**get()** 在等待结果时阻塞调用线程。此块可以通过 **InterruptedException** 或 **ExecutionException** 中断。在这种情况下，阻止永远不会发生，因为 **CompletableFuture** 已经完成，所以结果立即可用。

当我们将 **handle()** 包装在 **CompletableFuture** 中时，发现我们可以在 **CompletableFuture** 上添加操作来处理所包含的对象，使得事情变得更加有趣：

```java
// concurrent/CompletableApply.java
import java.util.concurrent.*;
public class CompletableApply {
    public static void main(String[] args) {
        CompletableFuture<Machina> cf =
        CompletableFuture.completedFuture(
            new Machina(0));
        CompletableFuture<Machina> cf2 =
            cf.thenApply(Machina::work);
        CompletableFuture<Machina> cf3 =
            cf2.thenApply(Machina::work);
        CompletableFuture<Machina> cf4 =
            cf3.thenApply(Machina::work);
        CompletableFuture<Machina> cf5 =
            cf4.thenApply(Machina::work);
    }
}
```

**输出结果**：

```
Machina0: ONE
Machina0: TWO
Machina0: THREE
Machina0: complete
```

`thenApply()` 应用**一个接收输入并产生输出的函数**。在本例中，`work()` 函数产生的类型与它所接收的类型相同 （`Machina`），因此每个 `CompletableFuture`添加的操作的返回类型都为 `Machina`，但是 (类似于流中的 `map()` ) 函数也可以返回不同的类型，这将体现在返回类型上。

你可以在此处看到有关 **CompletableFutures** 的重要信息：它们会在你**执行操作时自动解包并重新包装它们所携带的对象。**这使得编写和理解代码变得更加简单， 而不会在陷入在麻烦的细节中。

我们可以消除中间变量并将操作链接在一起，就像我们使用 Streams 一样：

```java
// concurrent/CompletableApplyChained.javaimport java.util.concurrent.*;
import onjava.Timer;
public class CompletableApplyChained {
    public static void main(String[] args) {
        Timer timer = new Timer();
        CompletableFuture<Machina> cf =
        CompletableFuture.completedFuture(
            new Machina(0))
                  .thenApply(Machina::work)
                  .thenApply(Machina::work)
                  .thenApply(Machina::work)
                  .thenApply(Machina::work);
        System.out.println(timer.duration());
    }
}
```

输出结果：

```
Machina0: ONE
Machina0: TWO
Machina0: THREE
Machina0: complete
514
```

这里我们还添加了一个 `Timer`，它的功能在每一步都显性地增加 100ms 等待时间之外，还将 `CompletableFuture` 内部 `thenApply` 带来的额外开销给体现出来了。 
**CompletableFutures**  的一个重要好处是它们**鼓励使用私有子类原则（不共享任何东西）**。默认情况下，使用 **thenApply()**  来应用一个不对外通信的函数 - 它只需要一个参数并返回一个结果。这是函数式编程的基础，并且它在并发特性方面非常有效[^5]。并行流和 `ComplempleFutures` 旨在支持这些原则。**只要你不决定共享数据（共享非常容易导致意外发生）你就可以编写出相对安全的并发程序。**

回调 `thenApply()` 一旦开始一个操作，在完成所有任务之前，不会完成 **CompletableFuture**  的构建。虽然这有时很有用，但是开始所有任务通常更有价值，这样就可以运行继续前进并执行其他操作。我们可通过`thenApplyAsync()` 来实现此目的：

```java
// concurrent/CompletableApplyAsync.java
import java.util.concurrent.*;
import onjava.*;
public class CompletableApplyAsync {
    public static void main(String[] args) {
        Timer timer = new Timer();
        CompletableFuture<Machina> cf =
            CompletableFuture.completedFuture(
                new Machina(0))
                .thenApplyAsync(Machina::work)
                .thenApplyAsync(Machina::work)
                .thenApplyAsync(Machina::work)
                .thenApplyAsync(Machina::work);
            System.out.println(timer.duration());
            System.out.println(cf.join());
            System.out.println(timer.duration());
    }
}
```

输出结果：

```
116
Machina0: ONE
Machina0: TWO
Machina0:THREE
Machina0: complete
Machina0: complete
552
```

**==同步调用==** (我们通常使用的那种) 意味着：**“当你完成工作时，才返回”**，而**异步调用**以意味着： **“立刻返回并继续后续工作”**。 正如你所看到的，`cf` 的创建现在发生的更快。每次调用 `thenApplyAsync()` 都会立刻返回，因此可以进行下一次调用，整个调用链路完成速度比以前快得多。

事实上，如果没有回调 `cf.join()` 方法，**程序会在完成其工作之前退出**。而 `cf.join()` 直到 **cf 操作完成之前，阻止 `main()` 进程结束。**我们还可以看出本示例大部分时间消耗在 `cf.join()` 这。

这种“立即返回”的异步能力需要 `CompletableFuture` 库进行一些秘密（`client` 无感）工作。特别是，**它将你需要的操作链存储为一组回调**。当操作的第一个链路（后台操作）完成并返回时，第二个链路（后台操作）必须获取生成的 `Machina` 并开始工作，以此类推！ 但这种异步机制**没有我们可以通过程序调用栈控制的普通函数调用序列，它的调用链路顺序会丢失，因此它使用一个函数地址来存储的回调来解决这个问题。**

幸运的是，这就是你需要了解的有关回调的全部信息。程序员将这种人为制造的混乱称为 callback hell（回调地狱）。**通过异步调用，`CompletableFuture` 帮你管理所有回调。** 除非你知道你系统中的一些特定逻辑会导致某些改变，或许你更想使用异步调用来实现程序。

- 其他操作

当你查看`CompletableFuture`的 `Javadoc` 时，你会看到它有很多方法，但这个方法的大部分来自不同操作的变体。例如，有 `thenApply()`，`thenApplyAsync()` 和第二种形式的 `thenApplyAsync()`，它们使用 `Executor` 来运行任务 (在本书中，我们忽略了 `Executor` 选项)。

下面的示例展示了所有"基本"操作，这些操作既不涉及组合两个 `CompletableFuture`，也不涉及异常 (我们将在后面介绍)。首先，为了提供简洁性和方便性，我们应该重用以下两个实用程序:

```java
package onjava;
import java.util.concurrent.*;

public class CompletableUtilities {
  // Get and show value stored in a CF:
  public static void showr(CompletableFuture<?> c) {
    try {
      System.out.println(c.get());
    } catch(InterruptedException
            | ExecutionException e) {
      throw new RuntimeException(e);
    }
  }
  // For CF operations that have no value:
  public static void voidr(CompletableFuture<Void> c) {
    try {
      c.get(); // Returns void
    } catch(InterruptedException
            | ExecutionException e) {
      throw new RuntimeException(e);
    }
  }
}
```

`showr()` 在 `CompletableFuture<Integer>` 上调用 `get()`，并显示结果，`try/catch` 两个可能会出现的异常。

`voidr()` 是 `CompletableFuture<Void>` 的 `showr()` 版本，也就是说，`CompletableFutures` 只为任务完成或失败时显示信息。

为简单起见，下面的 `CompletableFutures` 只包装整数。`cfi()` 是一个便利的方法，它把一个整数包装在一个完整的 `CompletableFuture<Integer>` :

```java
// concurrent/CompletableOperations.java
import java.util.concurrent.*;
import static onjava.CompletableUtilities.*;

public class CompletableOperations {
    static CompletableFuture<Integer> cfi(int i) {
        return CompletableFuture.completedFuture(
                        Integer.valueOf(i));
    }

    public static void main(String[] args) {
        showr(cfi(1)); // Basic test
        voidr(cfi(2).runAsync(() ->
                System.out.println("runAsync")));
        voidr(cfi(3).thenRunAsync(() ->
                System.out.println("thenRunAsync")));
        voidr(CompletableFuture.runAsync(() ->
                System.out.println("runAsync is static")));
        showr(CompletableFuture.supplyAsync(() -> 99));
        voidr(cfi(4).thenAcceptAsync(i ->
                System.out.println("thenAcceptAsync: " + i)));
        showr(cfi(5).thenApplyAsync(i -> i + 42));
        showr(cfi(6).thenComposeAsync(i -> cfi(i + 99)));
        CompletableFuture<Integer> c = cfi(7);
        c.obtrudeValue(111);
        showr(c);
        showr(cfi(8).toCompletableFuture());
        c = new CompletableFuture<>();
        c.complete(9);
        showr(c);
        c = new CompletableFuture<>();
        c.cancel(true);
        System.out.println("cancelled: " +
                c.isCancelled());
        System.out.println("completed exceptionally: " +
                c.isCompletedExceptionally());
        System.out.println("done: " + c.isDone());
        System.out.println(c);
        c = new CompletableFuture<>();
        System.out.println(c.getNow(777));
        c = new CompletableFuture<>();
        c.thenApplyAsync(i -> i + 42)
                .thenApplyAsync(i -> i * 12);
        System.out.println("dependents: " +
                c.getNumberOfDependents());
        c.thenApplyAsync(i -> i / 2);
        System.out.println("dependents: " +
                c.getNumberOfDependents());
    }
}
```

**输出结果** ：

```
1
runAsync
thenRunAsync
runAsync is static
99
thenAcceptAsync: 4
47
105
111
8
9
cancelled: true
completed exceptionally: true
done: true
java.util.concurrent.CompletableFuture@6d311334[Complet ed exceptionally]
777
dependents: 1
dependents: 2
```

- `main()` 包含一系列可由其 `int` 值引用的测试。
  - `cfi(1)` 演示了 `showr()` 正常工作。
  - `cfi(2)` 是调用 `runAsync()` 的示例。由于 `Runnable` 不产生返回值，因此使用了返回 `CompletableFuture <Void>` 的`voidr()` 方法。
  - 注意使用 `cfi(3)`,`thenRunAsync()` 效果似乎与 上例 `cfi(2)` 使用的 `runAsync()`相同，差异在后续的测试中体现：
    - `runAsync()` 是一个 **`static` 方法**，所以你通常不会像`cfi(2)`一样调用它。相反你可以在 `QuittingCompletable.java` 中使用它。
    - 后续测试中表明 `supplyAsync()` 也是静态方法，区别在于**它需要一个 `Supplier`** 而不是`Runnable`, 并产生一个`CompletableFuture<Integer>` 而不是 `CompletableFuture<Void>`。
  - `then` 系列方法将对现有的 `CompletableFuture<Integer>` 进一步操作。
    - 与 `thenRunAsync()` 不同，`cfi(4)`，`cfi(5)` 和`cfi(6)` "then" 方法的参数是未包装的 `Integer`。
    - 通过使用 `voidr()`方法可以看到: 
      - `AcceptAsync()`接收了一个 `Consumer`，因此不会产生结果。
      - `thenApplyAsync()` 接收一个`Function`, 并生成一个结果（该结果的类型可以不同于其输入类型）。
      - `thenComposeAsync()` 与 `thenApplyAsync()`非常相似，唯一区别在于其 `Function` 必须产生已经包装在`CompletableFuture`中的结果。
  - `cfi(7)` 示例演示了 `obtrudeValue()`，它强制将值作为结果。
  - `cfi(8)` 使用 `toCompletableFuture()` 从 `CompletionStage` 生成一个`CompletableFuture`。
  - `c.complete(9)` 显示了如何通过给它一个结果来完成一个`task`（`future`）（与 `obtrudeValue()` 相对，后者可能会迫使其结果替换该结果）。
  - 如果你调用 `CompletableFuture`中的 `cancel()`方法，如果已经完成此任务，则正常结束。 如果尚未完成，则使用 `CancellationException` 完成此 `CompletableFuture`。
  - 如果任务（`future`）完成，则 **getNow()** 方法返回`CompletableFuture`的完成值，否则返回`getNow()`的替换参数。
  - 最后，我们看一下依赖 (`dependents`) 的概念。如果我们将两个`thenApplyAsync()`调用链路到`CompletableFuture`上，则依赖项的数量不会增加，保持为 1。但是，如果我们另外将另一个`thenApplyAsync()`直接附加到`c`，则现在有两个依赖项：两个一起的链路和另一个单独附加的链路。
    - 这表明你可以使用一个`CompletionStage`，当它完成时，可以根据其结果派生多个新任务。

### 结合 CompletableFuture

第二种类型的 `CompletableFuture` 方法采用两种 `CompletableFuture` 并以各异方式将它们组合在一起。就像两个人在比赛一样, 一个`CompletableFuture`通常比另一个更早地到达终点。这些方法允许你以不同的方式处理结果。
为了测试这一点，我们将创建一个任务，它有一个我们可以控制的定义了完成任务所需要的时间量的参数。 
CompletableFuture 先完成:

```java
// concurrent/Workable.java
import java.util.concurrent.*;
import onjava.Nap;

public class Workable {
    String id;
    final double duration;

    public Workable(String id, double duration) {
        this.id = id;
        this.duration = duration;
    }

    @Override
    public String toString() {
        return "Workable[" + id + "]";
    }

    public static Workable work(Workable tt) {
        new Nap(tt.duration); // Seconds
        tt.id = tt.id + "W";
        System.out.println(tt);
        return tt;
    }

    public static CompletableFuture<Workable> make(String id, double duration) {
        return CompletableFuture
                .completedFuture(
                        new Workable(id, duration)
                )
                .thenApplyAsync(Workable::work);
    }
}
```

在 `make()`中，`work()`方法应用于`CompletableFuture`。`work()`需要一定的时间才能完成，然后它将字母 W 附加到 id 上，表示工作已经完成。

现在我们可以创建多个竞争的 `CompletableFuture`，并使用 `CompletableFuture` 库中的各种方法来进行操作:

```java
// concurrent/DualCompletableOperations.java
import java.util.concurrent.*;
import static onjava.CompletableUtilities.*;

public class DualCompletableOperations {
    static CompletableFuture<Workable> cfA, cfB;

    static void init() {
        cfA = Workable.make("A", 0.15);
        cfB = Workable.make("B", 0.10); // Always wins
    }

    static void join() {
        cfA.join();
        cfB.join();
        System.out.println("*****************");
    }

    public static void main(String[] args) {
        init();
        voidr(cfA.runAfterEitherAsync(cfB, () ->
                System.out.println("runAfterEither")));
        join();

        init();
        voidr(cfA.runAfterBothAsync(cfB, () ->
                System.out.println("runAfterBoth")));
        join();

        init();
        showr(cfA.applyToEitherAsync(cfB, w -> {
            System.out.println("applyToEither: " + w);
            return w;
        }));
        join();

        init();
        voidr(cfA.acceptEitherAsync(cfB, w -> {
            System.out.println("acceptEither: " + w);
        }));
        join();

        init();
        voidr(cfA.thenAcceptBothAsync(cfB, (w1, w2) -> {
            System.out.println("thenAcceptBoth: "
                    + w1 + ", " + w2);
        }));
        join();

        init();
        showr(cfA.thenCombineAsync(cfB, (w1, w2) -> {
            System.out.println("thenCombine: "
                    + w1 + ", " + w2);
            return w1;
        }));
        join();

        init();
        CompletableFuture<Workable>
                cfC = Workable.make("C", 0.08),
                cfD = Workable.make("D", 0.09);
        CompletableFuture.anyOf(cfA, cfB, cfC, cfD)
                .thenRunAsync(() ->
                        System.out.println("anyOf"));
        join();

        init();
        cfC = Workable.make("C", 0.08);
        cfD = Workable.make("D", 0.09);
        CompletableFuture.allOf(cfA, cfB, cfC, cfD)
                .thenRunAsync(() ->
                        System.out.println("allOf"));
        join();
    }
}
```

**输出结果**：

```
Workable[BW]
runAfterEither
Workable[AW]
*****************
Workable[BW]
Workable[AW]
runAfterBoth
*****************
Workable[BW]
applyToEither: Workable[BW]
Workable[BW]
Workable[AW]
*****************
Workable[BW]
acceptEither: Workable[BW]
Workable[AW]
*****************
Workable[BW]
Workable[AW]
thenAcceptBoth: Workable[AW], Workable[BW]
****************
 Workable[BW]
 Workable[AW]
 thenCombine: Workable[AW], Workable[BW]
 Workable[AW]
 *****************
 Workable[CW]
 anyOf
 Workable[DW]
 Workable[BW]
 Workable[AW]
 *****************
 Workable[CW]
 Workable[DW]
 Workable[BW]
 Workable[AW]
 *****************
 allOf
```

- 为了方便访问， 将 `cfA` 和 `cfB` 定义为 `static`的。 
  - `init()`方法用于 `A`, `B` 初始化这两个变量，因为 `B` 总是给出比`A`较短的延迟，所以总是 `win` 的一方。
  - `join()` 是在两个方法上调用 `join()` 并显示边框的另一个便利方法。
- 所有这些 “`dual`” 方法都以一个 `CompletableFuture` 作为调用该方法的对象，第二个 `CompletableFuture` 作为第一个参数，然后是要执行的操作。
- 通过使用 `showr()` 和 `voidr()` 可以看到，“`run`”和“`accept`”是终端操作，而“`apply`”和“`combine`”则生成新的 `payload-bearing` (承载负载) 的 `CompletableFuture`。
- 方法的名称不言自明，你可以通过查看输出来验证这一点。一个特别有趣的方法是 `combineAsync()`，它等待两个 `CompletableFuture` 完成，然后将它们都交给一个 `BiFunction`，这个 `BiFunction` 可以将结果加入到最终的 `CompletableFuture` 的有效负载中。


### 模拟

作为使用 `CompletableFuture` 将一系列操作组合的示例，让我们模拟一下制作蛋糕的过程。在第一阶段，我们准备并将原料混合成面糊:

```java
// concurrent/Batter.java
import java.util.concurrent.*;
import onjava.Nap;

public class Batter {
    static class Eggs {
    }

    static class Milk {
    }

    static class Sugar {
    }

    static class Flour {
    }

    static <T> T prepare(T ingredient) {
        new Nap(0.1);
        return ingredient;
    }

    static <T> CompletableFuture<T> prep(T ingredient) {
        return CompletableFuture
                .completedFuture(ingredient)
                .thenApplyAsync(Batter::prepare);
    }

    public static CompletableFuture<Batter> mix() {
        CompletableFuture<Eggs> eggs = prep(new Eggs());
        CompletableFuture<Milk> milk = prep(new Milk());
        CompletableFuture<Sugar> sugar = prep(new Sugar());
        CompletableFuture<Flour> flour = prep(new Flour());
        CompletableFuture
                .allOf(eggs, milk, sugar, flour)
                .join();
        new Nap(0.1); // Mixing time
        return CompletableFuture.completedFuture(new Batter());
    }
}
```

每种原料都需要一些时间来准备。`allOf()` 等待所有的配料都准备好，然后使用更多些的时间将其混合成面糊。接下来，我们把单批面糊放入四个平底锅中烘烤。产品作为 `CompletableFutures`  流返回：

```java
// concurrent/Baked.java

import java.util.concurrent.*;
import java.util.stream.*;
import onjava.Nap;

public class Baked {
    static class Pan {
    }

    static Pan pan(Batter b) {
        new Nap(0.1);
        return new Pan();
    }

    static Baked heat(Pan p) {
        new Nap(0.1);
        return new Baked();
    }

    static CompletableFuture<Baked> bake(CompletableFuture<Batter> cfb) {
        return cfb
                .thenApplyAsync(Baked::pan)
                .thenApplyAsync(Baked::heat);
    }

    public static Stream<CompletableFuture<Baked>> batch() {
        CompletableFuture<Batter> batter = Batter.mix();
        return Stream.of(
                bake(batter),
                bake(batter),
                bake(batter),
                bake(batter)
        );
    }
}
```

最后，我们制作了一批糖，并用它对蛋糕进行糖化：

```java
// concurrent/FrostedCake.java

import java.util.concurrent.*;
import java.util.stream.*;
import onjava.Nap;

final class Frosting {
    private Frosting() {
    }

    static CompletableFuture<Frosting> make() {
        new Nap(0.1);
        return CompletableFuture
                .completedFuture(new Frosting());
    }
}

public class FrostedCake {
    public FrostedCake(Baked baked, Frosting frosting) {
        new Nap(0.1);
    }

    @Override
    public String toString() {
        return "FrostedCake";
    }

    public static void main(String[] args) {
        Baked.batch().forEach(
                baked -> baked
                        .thenCombineAsync(Frosting.make(),
                                (cake, frosting) ->
                                        new FrostedCake(cake, frosting))
                        .thenAcceptAsync(System.out::println)
                        .join());
    }
}
```

一旦你习惯了这种背后的想法, `CompletableFuture` 它们相对易于使用。

### 异常

与 `CompletableFuture` 在处理链中包装对象的方式相同，它也会缓冲异常。这些在处理时调用者是无感的，但仅当你尝试提取结果时才会被告知。为了说明它们是如何工作的，我们首先创建一个类，它在特定的条件下抛出一个异常:

```java
// concurrent/Breakable.java
import java.util.concurrent.*;
public class Breakable {
    String id;
    private int failcount;

    public Breakable(String id, int failcount) {
        this.id = id;
        this.failcount = failcount;
    }

    @Override
    public String toString() {
        return "Breakable_" + id + " [" + failcount + "]";
    }

    public static Breakable work(Breakable b) {
        if (--b.failcount == 0) {
            System.out.println(
                    "Throwing Exception for " + b.id + ""
            );
            throw new RuntimeException(
                    "Breakable_" + b.id + " failed"
            );
        }
        System.out.println(b);
        return b;
    }
}
```

当`failcount` > 0，且每次将对象传递给 `work()` 方法时， `failcount - 1` 。当`failcount - 1 = 0` 时，`work()` 将抛出一个异常。如果传给 `work()` 的 `failcount = 0` ，`work()` 永远不会抛出异常。

注意，异常信息此示例中被抛出（ `RuntimeException` )

在下面示例  `test()` 方法中，`work()` 多次应用于 `Breakable`，因此如果 `failcount` 在范围内，就会抛出异常。然而，在测试`A`到`E`中，你可以从输出中看到抛出了异常，但它们从未出现:

```java
// concurrent/CompletableExceptions.java
import java.util.concurrent.*;
public class CompletableExceptions {
    static CompletableFuture<Breakable> test(String id, int failcount) {
        return CompletableFuture.completedFuture(
                new Breakable(id, failcount))
                .thenApply(Breakable::work)
                .thenApply(Breakable::work)
                .thenApply(Breakable::work)
                .thenApply(Breakable::work);
    }

    public static void main(String[] args) {
        // Exceptions don't appear ...
        test("A", 1);
        test("B", 2);
        test("C", 3);
        test("D", 4);
        test("E", 5);
        // ... until you try to fetch the value:
        try {
            test("F", 2).get(); // or join()
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        // Test for exceptions:
        System.out.println(
                test("G", 2).isCompletedExceptionally()
        );
        // Counts as "done":
        System.out.println(test("H", 2).isDone());
        // Force an exception:
        CompletableFuture<Integer> cfi =
                new CompletableFuture<>();
        System.out.println("done? " + cfi.isDone());
        cfi.completeExceptionally(
                new RuntimeException("forced"));
        try {
            cfi.get();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
```

输出结果：

```
Throwing Exception for A
Breakable_B [1]
Throwing Exception for B
Breakable_C [2]
Breakable_C [1]
Throwing Exception for C
Breakable_D [3]
Breakable_D [2]
Breakable_D [1]
Throwing Exception for D
Breakable_E [4]
Breakable_E [3]
Breakable_E [2]
Breakable_E [1]
Breakable_F [1]
Throwing Exception for F
java.lang.RuntimeException: Breakable_F failed
Breakable_G [1]
Throwing Exception for G
true
Breakable_H [1]
Throwing Exception for H
true
done? false
java.lang.RuntimeException: forced
```

测试 `A` 到 `E` 运行到抛出异常，然后…并没有将抛出的异常暴露给调用方。只有在测试 F 中调用 `get()` 时，我们才会看到抛出的异常。
测试 `G` 表明，你可以首先检查在处理期间是否抛出异常，而不抛出该异常。然而，test `H` 告诉我们，**不管异常是否成功，它仍然被视为已“完成”。**
代码的最后一部分展示了**如何将异常插入到 `CompletableFuture` 中，而不管是否存在任何失败**。
在连接或获取结果时，我们使用 `CompletableFuture` 提供的更复杂的机制来自动响应异常，而不是使用粗糙的 `try-catch`。
你可以使用与我们看到的所有 `CompletableFuture`  相同的表单来完成此操作:在链中插入一个  `CompletableFuture` 调用。有三个选项 `exceptionally()`，`handle()`， `whenComplete()`:

```java
// concurrent/CatchCompletableExceptions.java
import java.util.concurrent.*;
public class CatchCompletableExceptions {
    static void handleException(int failcount) {
        // Call the Function only if there's an
        // exception, must produce same type as came in:
        CompletableExceptions
                .test("exceptionally", failcount)
                .exceptionally((ex) -> { // Function
                    if (ex == null)
                        System.out.println("I don't get it yet");
                    return new Breakable(ex.getMessage(), 0);
                })
                .thenAccept(str ->
                        System.out.println("result: " + str));

        // Create a new result (recover):
        CompletableExceptions
                .test("handle", failcount)
                .handle((result, fail) -> { // BiFunction
                    if (fail != null)
                        return "Failure recovery object";
                    else
                        return result + " is good";
                })
                .thenAccept(str ->
                        System.out.println("result: " + str));

        // Do something but pass the same result through:
        CompletableExceptions
                .test("whenComplete", failcount)
                .whenComplete((result, fail) -> { // BiConsumer
                    if (fail != null)
                        System.out.println("It failed");
                    else
                        System.out.println(result + " OK");
                })
                .thenAccept(r ->
                        System.out.println("result: " + r));
    }

    public static void main(String[] args) {
        System.out.println("**** Failure Mode ****");
        handleException(2);
        System.out.println("**** Success Mode ****");
        handleException(0);
    }
}
```

输出结果：

```
**** Failure Mode ****
Breakable_exceptionally [1]
Throwing Exception for exceptionally
result: Breakable_java.lang.RuntimeException:
Breakable_exceptionally failed [0]
Breakable_handle [1]
Throwing Exception for handle
result: Failure recovery object
Breakable_whenComplete [1]
Throwing Exception for whenComplete
It failed
**** Success Mode ****
Breakable_exceptionally [-1]
Breakable_exceptionally [-2]
Breakable_exceptionally [-3]
Breakable_exceptionally [-4]
result: Breakable_exceptionally [-4]
Breakable_handle [-1]
Breakable_handle [-2]
Breakable_handle [-3]
Breakable_handle [-4]
result: Breakable_handle [-4] is good
Breakable_whenComplete [-1]
Breakable_whenComplete [-2]
Breakable_whenComplete [-3]
Breakable_whenComplete [-4]
Breakable_whenComplete [-4] OK
result: Breakable_whenComplete [-4]
```

- `exceptionally()`  参数**仅在出现异常时才运行**。`exceptionally()`  局限性在于，该函数只能返回输入类型相同的值。

- `exceptionally()` 通过将一个好的对象插入到流中来恢复到一个可行的状态。

- `handle()` 一致被**调用来查看是否发生异常**（必须检查 fail 是否为 true）。
  - 但是 `handle()` 可以生成任何新类型，所以它允许执行处理，而不是像使用 `exceptionally()`那样简单地恢复。

  - `whenComplete()` 类似于 handle()，同样必须测试它是否失败，但是参数是一个消费者，并且不修改传递给它的结果对象。


### 流异常（Stream Exception）

通过修改 **CompletableExceptions.java** ，看看 **CompletableFuture** 异常与流异常有何不同：

```java
// concurrent/StreamExceptions.java
import java.util.concurrent.*;
import java.util.stream.*;
public class StreamExceptions {
    
    static Stream<Breakable> test(String id, int failcount) {
        return Stream.of(new Breakable(id, failcount))
                .map(Breakable::work)
                .map(Breakable::work)
                .map(Breakable::work)
                .map(Breakable::work);
    }

    public static void main(String[] args) {
        // No operations are even applied ...
        test("A", 1);
        test("B", 2);
        Stream<Breakable> c = test("C", 3);
        test("D", 4);
        test("E", 5);
        // ... until there's a terminal operation:
        System.out.println("Entering try");
        try {
            c.forEach(System.out::println);   // [1]
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
```

输出结果：

```
Entering try
Breakable_C [2]
Breakable_C [1]
Throwing Exception for C
Breakable_C failed
```

使用 `CompletableFuture`，我们可以看到测试 A 到 E 的进展，但是使用流，在你应用一个终端操作之前（e.g. `forEach()`），什么都不会暴露给 Client 

`CompletableFuture` 执行工作并捕获任何异常供以后检索。比较这两者并不容易，因为 `Stream` 在没有终端操作的情况下根本不做任何事情——**但是流绝对不会存储它的异常。**

### 检查性异常

`CompletableFuture` 和 `parallel Stream` 都不支持包含检查性异常的操作。相反，你必须在调用操作时处理检查到的异常，这会产生不太优雅的代码：

```java
// concurrent/ThrowsChecked.java
import java.util.stream.*;
import java.util.concurrent.*;

public class ThrowsChecked {
    class Checked extends Exception {}

    static ThrowsChecked nochecked(ThrowsChecked tc) {
        return tc;
    }

    static ThrowsChecked withchecked(ThrowsChecked tc) throws Checked {
        return tc;
    }

    static void testStream() {
        Stream.of(new ThrowsChecked())
                .map(ThrowsChecked::nochecked)
                // .map(ThrowsChecked::withchecked); // [1]
                .map(
                        tc -> {
                            try {
                                return withchecked(tc);
                            } catch (Checked e) {
                                throw new RuntimeException(e);
                            }
                        });
    }

    static void testCompletableFuture() {
        CompletableFuture
                .completedFuture(new ThrowsChecked())
                .thenApply(ThrowsChecked::nochecked)
                // .thenApply(ThrowsChecked::withchecked); // [2]
                .thenApply(
                        tc -> {
                            try {
                                return withchecked(tc);
                            } catch (Checked e) {
                                throw new RuntimeException(e);
                            }
                        });
    }
}
```

如果你试图像使用 `nochecked()` 那样使用` withchecked()` 的方法引用，编译器会在 `[1]` 和 `[2]` 中报错。相反，你必须写出 lambda 表达式 (或者编写一个不会抛出异常的包装器方法)。

## 死锁

由于任务可以被阻塞，因此一个任务有可能卡在等待另一个任务上，而后者又在等待别的任务，这样一直下去，知道这个链条上的任务又在等待第一个任务释放锁。这得到了一个任务之间**相互等待的连续循环， 没有哪个线程能继续， 这称之为死锁**[^6]
如果你运行一个程序，而它马上就死锁了， 你可以立即跟踪下去。真正的问题在于，程序看起来工作良好， 但是具有潜在的死锁危险。这时， 死锁可能发生，而事先却没有任何征兆， 所以 `bug` 会潜伏在你的程序例，直到客户发现它出乎意料的发生（以一种几乎肯定是很难重现的方式发生）。因此在编写并发程序的时候，**进行仔细的程序设计以防止死锁是关键部分。**
埃德斯·迪克斯特拉（`Essger Dijkstra`）发明的“哲学家进餐"问题是经典的死锁例证。基本描述指定了五位哲学家（此处显示的示例允许任何数目）。这些哲学家将花部分时间思考，花部分时间就餐。他们在思考的时候并不需要任何共享资源；但是他们使用的餐具数量有限。在最初的问题描述中，餐具是叉子，需要两个叉子才能从桌子中间的碗里取出意大利面。常见的版本是使用筷子， 显然，每个哲学家都需要两根筷子才能吃饭。
引入了一个困难：作为哲学家，他们的钱很少，所以他们只能买五根筷子（更一般地讲，筷子的数量与哲学家相同）。他们围在桌子周围，每人之间放一根筷子。 当一个哲学家要就餐时，该哲学家必须同时持有左边和右边的筷子。如果任一侧的哲学家都在使用所需的筷子，则我们的哲学家必须等待，直到可得到必须的筷子。

**StickHolder**  类通过将单根筷子保持在大小为 1 的 **BlockingQueue** 中来管理它。**BlockingQueue** 是一个**设计用于在并发程序中安全使用的集合**，如果你调用 take() 并且队列为空，则它将阻塞（等待）。将新元素放入队列后，将释放该块并返回该值：

```java
// concurrent/StickHolder.java
import java.util.concurrent.*;
public class StickHolder {
    private static class Chopstick {
    }

    private Chopstick stick = new Chopstick();
    private BlockingQueue<Chopstick> holder =
            new ArrayBlockingQueue<>(1);

    public StickHolder() {
        putDown();
    }

    public void pickUp() {
        try {
            holder.take(); // Blocks if unavailable
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    public void putDown() {
        try {
            holder.put(stick);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
```

为简单起见，`Chopstick`(`static`) 实际上不是由 `StickHolder` 生产的，而是在其类中保持私有的。

如果您调用了`pickUp()`，而 `stick` 不可用，那么`pickUp()`将阻塞该 `stick`，直到另一个哲学家调用`putDown()` 将 `stick` 返回。 

注意，该类中的**所有线程安全都是通过 `BlockingQueue` 实现的。**

每个哲学家都是一项任务，他们试图把筷子分别 `pickUp()` 在左手和右手上，这样筷子才能吃东西，然后通过 `putDown()` 放下 `stick`。

```java
// concurrent/Philosopher.java
public class Philosopher implements Runnable {
    private final int seat;
    private final StickHolder left, right;

    public Philosopher(int seat, StickHolder left, StickHolder right) {
        this.seat = seat;
        this.left = left;
        this.right = right;
    }

    @Override
    public String toString() {
        return "P" + seat;
    }

    @Override
    public void run() {
        while (true) {
            // System.out.println("Thinking");   // [1]
            right.pickUp();
            left.pickUp();
            System.out.println(this + " eating");
            right.putDown();
            left.putDown();
        }
    }
}
```

没有两个哲学家可以同时成功调用 take() 同一只筷子。另外，如果一个哲学家已经拿过筷子，那么下一个试图拿起同一根筷子的哲学家将阻塞，等待其被释放。

结果是一个看似无辜的程序陷入了死锁。我在这里使用数组而不是集合，只是因为这种语法更简洁：

```java
// concurrent/DiningPhilosophers.java
// Hidden deadlock
// {ExcludeFromGradle} Gradle has trouble
import java.util.*;
import java.util.concurrent.*;
import onjava.Nap;

public class DiningPhilosophers {
    private StickHolder[] sticks;
    private Philosopher[] philosophers;

    public DiningPhilosophers(int n) {
        sticks = new StickHolder[n];
        Arrays.setAll(sticks, i -> new StickHolder());
        philosophers = new Philosopher[n];
        Arrays.setAll(philosophers, i ->
                new Philosopher(i,
                        sticks[i], sticks[(i + 1) % n]));    // [1]
        // Fix by reversing stick order for this one:
        // philosophers[1] =                     // [2]
        //   new Philosopher(0, sticks[0], sticks[1]);
        Arrays.stream(philosophers)
                .forEach(CompletableFuture::runAsync); // [3]
    }

    public static void main(String[] args) {
        // Returns right away:
        new DiningPhilosophers(5);               // [4]
        // Keeps main() from exiting:
        new Nap(3, "Shutdown");
    }
}
```

- 当你停止查看输出时，该程序将死锁。但是，根据你的计算机配置，你可能不会看到死锁。看来这取决于计算机上的内核数[^7]。两个核心不会产生死锁，但两核以上却很容易产生死锁。
- 此行为使该示例更好地说明了死锁，因为你可能正在具有 2 核的计算机上编写程序（如果确实是导致问题的原因），并且确信该程序可以正常工作，只能启动它将其安装在另一台计算机上时出现死锁。请注意，不能因为你没或不容易看到死锁，这并不意味着此程序不会在 2 核机器上发生死锁。 该程序仍然有死锁倾向，只是很少发生——可以说是最糟糕的情况，因为问题不容易出现。
- 在 `DiningPhilosophers` 的构造方法中，每个哲学家都获得一个左右筷子的引用。除最后一个哲学家外，都是通过把哲学家放在下一双空闲筷子之间来初始化： 
  - 最后一位哲学家得到了第 0 根筷子作为他的右筷子，所以圆桌就完成。
  - 那是因为最后一位哲学家正坐在第一个哲学家的旁边，而且他们俩都共用零筷子。[1] 显示了以 n 为模数选择的右筷子，将最后一个哲学家绕到第一个哲学家的旁边。
- 现在，所有哲学家都可以尝试吃饭，每个哲学家都在旁边等待哲学家放下筷子。
  - 为了让每个哲学家在[3] 上运行，**调用 `runAsync()`，**这意味着 DiningPhilosophers 的构造函数立即返回到[4]。
  - 如果没有任何东西阻止 `main()` 完成，程序就会退出，不会做太多事情。
  - `Nap` 对象阻止 `main()` 退出，然后在三秒后强制退出 (假设/可能是) 死锁程序。
  - 在给定的配置中，哲学家几乎不花时间思考。因此，他们在吃东西的时候都争着用筷子，而且往往很快就会陷入僵局。你可以改变这个:

1. 通过增加[4] 的值来添加更多哲学家。

2. 在 Philosopher.java 中取消注释行[1]。

任一种方法都会减少死锁的可能性，这表明编写并发程序并认为它是安全的危险，因为它似乎“在我的机器上运行正常”。你可以轻松地说服自己该程序没有死锁，即使它不是。这个示例相当有趣，因为它演示了看起来可以正确运行，但实际上会可能发生死锁的程序。

要修正死锁问题，你必须明白，**当以下四个条件同时满足时，就会发生死锁：**

1) 互斥条件。任务使用的资源中**至少有一个不能共享的**。 这里，一根筷子一次就只能被一个哲学家使用。
2) 至少有一个任务它**必须持有一个资源且正在等待获取一个被当前别的任务持有的资源**。也就是说，要发生死锁，哲学家必须拿着一根筷子并且等待另一根。
3) **资源不能被任务抢占**， 任务必须把资源释放当作普通事件。哲学家很有礼貌，他们不会从其它哲学家那里抢筷子。
4) 必须有**循环等待**， 这时，一个任务等待其它任务所持有的资源， 后者又在等待另一个任务所持有的资源， 这样一直下去，知道有一个任务在等待第一个任务所持有的资源， 使得大家都被锁住。 在 `DiningPhilosophers.java` 中， 因为每个哲学家都试图先得到右边的 筷子, 然后得到左边的 筷子, 所以发生了循环等待。

因为必须满足所有条件才能导致死锁，所以要阻止死锁的话，**只需要破坏其中一个即可**。在此程序中，防止死锁的一种简单方法是打破第四个条件。之所以会发生这种情况，是因为每个哲学家都尝试按照特定的顺序拾起自己的筷子：先右后左。因此，每个哲学家都有可能在等待左手的同时握住右手的筷子，从而导致循环等待状态。但是，如果其中一位哲学家尝试首先拿起左筷子，则该哲学家决不会阻止紧邻右方的哲学家拿起筷子，从而排除了循环等待。

在 **DiningPhilosophers.java** 中，取消注释[1] 和其后的一行。这将原来的哲学家[1] 替换为筷子颠倒的哲学家。通过确保第二位哲学家拾起并在右手之前放下左筷子，我们消除了死锁的可能性。
这只是解决问题的一种方法。你也可以通过防止其他情况之一来解决它。
**没有语言支持可以帮助防止死锁；你有责任通过精心设计来避免这种情况。**对于试图调试死锁程序的人来说，这些都不是安慰。当然，**避免并发问题的最简单，最好的方法是永远不要共享资源-不幸的是，这并不总是可能的。**

## 构造方法非线程安全

当你在脑子里想象一个对象构造的过程，你会很容易认为这个过程是线程安全的。毕竟，在对象初始化完成前对外不可见，所以又怎会对此产生争议呢？确实，[Java 语言规范 ](https://docs.oracle.com/javase/specs/jls/se8/html/jls-8.html#jls-8.8.3) (JLS) 自信满满地陈述道：“*没必要使构造器的线程同步，因为它会锁定正在构造的对象，直到构造器完成初始化后才对其他线程可见。*”

不幸的是，对象的构造过程如其他操作一样，也会**受到共享内存并发问题的影响**，只是作用机制可能更微妙罢了。

设想下使用一个 **static**  字段为每个对象自动创建唯一标识符的过程。为了测试其不同的实现过程，我们从一个接口开始。代码示例：

```java
//concurrent/HasID.java
public interface HasID {
    int getID();
}
```

然后 **StaticIDField**  类显式地实现该接口。代码示例：

```java
// concurrent/StaticIDField.java
public class StaticIDField implements HasID {
    private static int counter = 0;
    private int id = counter++;
    public int getID() { return id; }
}
```

如你所想，该类是个简单无害的类，它甚至都没一个显式的构造器来引发问题。当我们运行多个用于创建此类对象的线程时，究竟会发生什么？为了搞清楚这点，我们做了以下测试。代码示例：

```java
// concurrent/IDChecker.java
import java.util.*;
import java.util.function.*;
import java.util.stream.*;
import java.util.concurrent.*;
import com.google.common.collect.Sets;
public class IDChecker {
    public static final int SIZE = 100_000;

    static class MakeObjects implements
        Supplier<List<Integer>> {
        private Supplier<HasID> gen;

        MakeObjects(Supplier<HasID> gen) {
            this.gen = gen;
        }

        @Override public List<Integer> get() {
            return Stream.generate(gen)
            .limit(SIZE)
            .map(HasID::getID)
            .collect(Collectors.toList());
        }
    }

    public static void test(Supplier<HasID> gen) {
        CompletableFuture<List<Integer>>
        groupA = CompletableFuture.supplyAsync(new
            MakeObjects(gen)),
        groupB = CompletableFuture.supplyAsync(new
            MakeObjects(gen));

        groupA.thenAcceptBoth(groupB, (a, b) -> {
            System.out.println(
                Sets.intersection(
                Sets.newHashSet(a),
                Sets.newHashSet(b)).size());
            }).join();
    }
}
```

**MakeObjects**  类是一个生产者类，包含一个能够产生 List\<Integer> 类型的列表对象的 `get()` 方法。通过从每个 `HasID` 对象提取 `ID` 并放入列表中来生成这个列表对象，而 `test()` 方法则创建了两个并行的 **CompletableFuture**  对象，用于运行 **MakeObjects**  生产者类，然后获取运行结果。

使用 Guava 库中的 Sets.`intersection()` 方法，计算出这两个返回的 List\<Integer> 对象中有多少相同的 `ID`（使用谷歌 Guava 库里的方法比使用官方的 `retainAll()` 方法速度快得多）。

现在我们可以测试上面的 **StaticIDField**  类了。代码示例：

```java
// concurrent/TestStaticIDField.java
public class TestStaticIDField {

    public static void main(String[] args) {
        IDChecker.test(StaticIDField::new);
    }
}
```

输出结果：

```
    13287
```

结果中出现了很多重复项。很显然，纯静态 `int` 用于构造过程并不是线程安全的。让我们使用 **AtomicInteger**  来使其变为线程安全的。代码示例：

```java
// concurrent/GuardedIDField.java
import java.util.concurrent.atomic.*;
public class GuardedIDField implements HasID {  
    private static AtomicInteger counter = new
        AtomicInteger();

    private int id = counter.getAndIncrement();

    public int getID() { return id; }

    public static void main(String[] args) {                IDChecker.test(GuardedIDField::new);
    }
}
```

输出结果：

```
0
```

==**构造器有一种更微妙的状态共享方式：通过构造器参数：**==

```java
// concurrent/SharedConstructorArgument.java
import java.util.concurrent.atomic.*;
interface SharedArg{
    int get();
}

class Unsafe implements SharedArg{
    private int i = 0;

    public int get(){
        return i++;
    }
}

class Safe implements SharedArg{
    private static AtomicInteger counter = new AtomicInteger();

    public int get(){
        return counter.getAndIncrement();
    }
}

class SharedUser implements HasID{
    private final int id;

    SharedUser(SharedArg sa){
        id = sa.get();
    }

    @Override
    public int getID(){
        return id;
    }
}

public class SharedConstructorArgument{
    public static void main(String[] args){
        Unsafe unsafe = new Unsafe();
        IDChecker.test(() -> new SharedUser(unsafe));

        Safe safe = new Safe();
        IDChecker.test(() -> new SharedUser(safe));
    }
}
```

输出结果：

```
24838
0
```

在这里，**SharedUser**  构造器实际上共享了相同的参数。即使 **SharedUser**  以完全无害且合理的方式使用其自己的参数，其构造器的调用方式也会引起冲突。**SharedUser**  甚至不知道它是以这种方式调用的，更不必说控制它了。

**同步构造器并不被 java 语言所支持**，但是通过**==使用同步语块来创建你自己的同步构造器是可能的==**（请参阅附录：[并发底层原理 ](./Appendix-Low-Level-Concurrency.md)，来进一步了解同步关键字—— `synchronized`）。尽管 JLS（java 语言规范）这样陈述道：“……它会锁定正在构造的对象”，但这并不是真的——构造器实际上只是一个静态方法，因此**同步构造器实际上会锁定该类的 Class 对象**。我们可以通过**创建自己的静态对象并锁定它，来达到与同步构造器相同的效果**：

```java
// concurrent/SynchronizedConstructor.java

import java.util.concurrent.atomic.*;

class SyncConstructor implements HasID{
    private final int id;
    private static Object constructorLock =
        new Object();

    SyncConstructor(SharedArg sa){
        synchronized (constructorLock){
            id = sa.get();
        }
    }

    @Override
    public int getID(){
        return id;
    }
}

public class SynchronizedConstructor{
    public static void main(String[] args){
        Unsafe unsafe = new Unsafe();
        IDChecker.test(() -> new SyncConstructor(unsafe));
    }
}
```

输出结果：

0

**Unsafe** 类的共享使用现在就变得安全了。另一种方法是==**将构造器设为私有（因此可以防止继承），并提供一个静态 Factory 方法来生成新对象**==：

```java
// concurrent/SynchronizedFactory.java
import java.util.concurrent.atomic.*;

final class SyncFactory implements HasID{
    private final int id;

    private SyncFactory(SharedArg sa){
        id = sa.get();
    }

    @Override
    public int getID(){
        return id;
    }

    public static synchronized SyncFactory factory(SharedArg sa){
        return new SyncFactory(sa);
    }
}

public class SynchronizedFactory{
    public static void main(String[] args){
        Unsafe unsafe = new Unsafe();
        IDChecker.test(() -> SyncFactory.factory(unsafe));
    }
}
```

输出结果：

```
 0
```

通过同步静态工厂方法，可以在构造过程中锁定 **Class**  对象。

这些示例充分表明了在并发 Java 程序中检测和管理共享状态有多困难。**即使你采取“不共享任何内容”的策略，也很容易产生意外的共享事件。**

## 复杂性和代价

假设你正在做披萨，我们把从整个流程的当前步骤到下一个步骤所需的工作量，在这里一一表示为枚举变量的一部分：

```java
// concurrent/Pizza.java import java.util.function.*;

import onjava.Nap;
public class Pizza{
    public enum Step{
        DOUGH(4), ROLLED(1), SAUCED(1), CHEESED(2),
        TOPPED(5), BAKED(2), SLICED(1), BOXED(0);
        int effort;// Needed to get to the next step 

        Step(int effort){
            this.effort = effort;
        }

        Step forward(){
            if (equals(BOXED)) return BOXED;
            new Nap(effort * 0.1);
            return values()[ordinal() + 1];
        }
    }

    private Step step = Step.DOUGH;
    private final int id;

    public Pizza(int id){
        this.id = id;
    }

    public Pizza next(){
        step = step.forward();
        System.out.println("Pizza " + id + ": " + step);
        return this;
    }

    public Pizza next(Step previousStep){
        if (!step.equals(previousStep))
            throw new IllegalStateException("Expected " +
                      previousStep + " but found " + step);
        return next();
    }

    public Pizza roll(){
        return next(Step.DOUGH);
    }

    public Pizza sauce(){
        return next(Step.ROLLED);
    }

    public Pizza cheese(){
        return next(Step.SAUCED);
    }

    public Pizza toppings(){
        return next(Step.CHEESED);
    }

    public Pizza bake(){
        return next(Step.TOPPED);
    }

    public Pizza slice(){
        return next(Step.BAKED);
    }

    public Pizza box(){
        return next(Step.SLICED);
    }

    public boolean complete(){
        return step.equals(Step.BOXED);
    }

    @Override
    public String toString(){
        return "Pizza" + id + ": " + (step.equals(Step.BOXED) ? "complete" : step);
    }
}
```

这只算得上是一个平凡的状态机，就像 **Machina** 类一样。 

制作一个披萨，当披萨饼最终被放在盒子中时，就算完成最终任务了。 如果一个人在做一个披萨饼，那么所有步骤都是线性进行的，即一个接一个地进行：

```java
// concurrent/OnePizza.java 

import onjava.Timer;

public class OnePizza{
    public static void main(String[] args){
        Pizza za = new Pizza(0);
        System.out.println(Timer.duration(() -> {
            while (!za.complete()) za.next();
        }));
    }
}
```

输出结果：

```
Pizza 0: ROLLED 
Pizza 0: SAUCED 
Pizza 0: CHEESED 
Pizza 0: TOPPED 
Pizza 0: BAKED 
Pizza 0: SLICED 
Pizza 0: BOXED 
	1622 
```

时间以毫秒为单位，加总所有步骤的工作量，会得出与我们的期望值相符的数字。 如果你以这种方式制作了五个披萨，那么你会认为它花费的时间是原来的五倍。 但是，如果这还不够快怎么办？ 我们可以从尝试并行流方法开始：

```java
// concurrent/PizzaStreams.java
// import java.util.*; import java.util.stream.*;

import onjava.Timer;

public class PizzaStreams{
    static final int QUANTITY = 5;

    public static void main(String[] args){
        Timer timer = new Timer();
        IntStream.range(0, QUANTITY)
            .mapToObj(Pizza::new)
            .parallel()//[1]
        	.forEach(za -> { while(!za.complete()) za.next(); }); 			System.out.println(timer.duration());
    }
}
```

输出结果：

```
Pizza 2: ROLLED
Pizza 0: ROLLED
Pizza 1: ROLLED
Pizza 4: ROLLED
Pizza 3:ROLLED
Pizza 2:SAUCED
Pizza 1:SAUCED
Pizza 0:SAUCED
Pizza 4:SAUCED
Pizza 3:SAUCED
Pizza 2:CHEESED
Pizza 1:CHEESED
Pizza 0:CHEESED
Pizza 4:CHEESED
Pizza 3:CHEESED
Pizza 2:TOPPED
Pizza 1:TOPPED
Pizza 0:TOPPED
Pizza 4:TOPPED
Pizza 3:TOPPED
Pizza 2:BAKED
Pizza 1:BAKED
Pizza 0:BAKED
Pizza 4:BAKED
Pizza 3:BAKED
Pizza 2:SLICED
Pizza 1:SLICED
Pizza 0:SLICED
Pizza 4:SLICED
Pizza 3:SLICED
Pizza 2:BOXED
Pizza 1:BOXED
Pizza 0:BOXED
Pizza 4:BOXED
Pizza 3:BOXED
1739
```

现在，我们制作五个披萨的时间与制作单个披萨的时间就差不多了。 尝试删除标记为[1] 的行后，你会发现它花费的时间是原来的五倍。 你还可以尝试将 **QUANTITY** 更改为 4、8、10、16 和 17，看看会有什么不同，并猜猜看为什么会这样。

**PizzaStreams**  类产生的每个并行流在它的`forEach()`内完成所有工作，如果我们将其各个步骤用映射的方式一步一步处理，情况会有所不同吗？

```java
// concurrent/PizzaParallelSteps.java 

import java.util.*;
import java.util.stream.*;
import onjava.Timer;

public class PizzaParallelSteps{
    static final int QUANTITY = 5;

    public static void main(String[] args){
        Timer timer = new Timer();
        IntStream.range(0, QUANTITY)
            .mapToObj(Pizza::new)
            .parallel()
            .map(Pizza::roll)
            .map(Pizza::sauce)
            .map(Pizza::cheese)
            .map(Pizza::toppings)
            .map(Pizza::bake)
            .map(Pizza::slice)
            .map(Pizza::box)
            .forEach(za -> System.out.println(za));
        System.out.println(timer.duration());
    }
} 
```

输出结果：

```
Pizza 2: ROLLED 
Pizza 0: ROLLED 
Pizza 1: ROLLED 
Pizza 4: ROLLED 
Pizza 3: ROLLED 
Pizza 1: SAUCED 
Pizza 0: SAUCED 
Pizza 2: SAUCED 
Pizza 3: SAUCED 
Pizza 4: SAUCED 
Pizza 1: CHEESED 
Pizza 0: CHEESED 
Pizza 2: CHEESED 
Pizza 3: CHEESED 
Pizza 4: CHEESED 
Pizza 0: TOPPED 
Pizza 2: TOPPED
Pizza 1: TOPPED 
Pizza 3: TOPPED 
Pizza 4: TOPPED 
Pizza 1: BAKED 
Pizza 2: BAKED 
Pizza 0: BAKED 
Pizza 4: BAKED 
Pizza 3: BAKED 
Pizza 0: SLICED 
Pizza 2: SLICED 
Pizza 1: SLICED 
Pizza 3: SLICED 
Pizza 4: SLICED 
Pizza 1: BOXED 
Pizza1: complete 
Pizza 2: BOXED 
Pizza 0: BOXED 
Pizza2: complete 
Pizza0: complete 
Pizza 3: BOXED
Pizza 4: BOXED 
Pizza4: complete 
Pizza3: complete 
1738 
```

答案是“否”，事后看来这并不奇怪，因为每个披萨都需要按顺序执行步骤。因此，没法通过分步执行操作来进一步提高速度，就像上文的 `PizzaParallelSteps.java` 里面展示的一样。

我们可以使用 **CompletableFutures**  重写这个例子：

```java
// concurrent/CompletablePizza.java 

import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;
import onjava.Timer;

public class CompletablePizza{
    static final int QUANTITY = 5;

    public static CompletableFuture<Pizza> makeCF(Pizza za){
        return CompletableFuture
                .completedFuture(za)
            .thenApplyAsync(Pizza::roll)
            .thenApplyAsync(Pizza::sauce)
            .thenApplyAsync(Pizza::cheese)
            .thenApplyAsync(Pizza::toppings)
            .thenApplyAsync(Pizza::bake)
            .thenApplyAsync(Pizza::slice)
            .thenApplyAsync(Pizza::box);
    }

    public static void show(CompletableFuture<Pizza> cf){
        try{
            System.out.println(cf.get());
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args){
        Timer timer = new Timer();
        List<CompletableFuture<Pizza>> pizzas =
                IntStream.range(0, QUANTITY)
            .mapToObj(Pizza::new)
            .map(CompletablePizza::makeCF)
            .collect(Collectors.toList());
        System.out.println(timer.duration());
        pizzas.forEach(CompletablePizza::show);
        System.out.println(timer.duration());
    }
}
```

输出结果：

```
169 
Pizza 0: ROLLED 
Pizza 1: ROLLED 
Pizza 2: ROLLED 
Pizza 4: ROLLED 
Pizza 3: ROLLED 
Pizza 1: SAUCED 
Pizza 0: SAUCED 
Pizza 2: SAUCED 
Pizza 4: SAUCED
Pizza 3: SAUCED 
Pizza 0: CHEESED 
Pizza 4: CHEESED 
Pizza 1: CHEESED 
Pizza 2: CHEESED 
Pizza 3: CHEESED 
Pizza 0: TOPPED 
Pizza 4: TOPPED 
Pizza 1: TOPPED 
Pizza 2: TOPPED 
Pizza 3: TOPPED 
Pizza 0: BAKED 
Pizza 4: BAKED 
Pizza 1: BAKED 
Pizza 3: BAKED 
Pizza 2: BAKED 
Pizza 0: SLICED 
Pizza 4: SLICED 
Pizza 1: SLICED 
Pizza 3: SLICED
Pizza 2: SLICED 
Pizza 4: BOXED 
Pizza 0: BOXED 
Pizza0: complete 
Pizza 1: BOXED 
Pizza1: complete 
Pizza 3: BOXED 
Pizza 2: BOXED 
Pizza2: complete 
Pizza3: complete 
Pizza4: complete 
1797 
```

并行流和 **CompletableFutures**  是 **Java 并发工具箱中最先进发达的技术**。 你应该始终首先选择其中之一。 当一个问题很容易并行处理时，或者说，**很容易把数据分解成相同的、易于处理的各个部分时，使用并行流方法处理最为合适**（而如果你决定不借助它而由自己完成，你就必须撸起袖子，深入研究 **Spliterator** 的文档）。

而当工作的各个部分内容各不相同时，使用 **CompletableFutures**  是最好的选择。比起面向数据，**CompletableFutures**  更像是面向任务的。

对于披萨问题，结果似乎也没有什么不同。实际上，**并行流方法看起来更简洁，仅出于这个原因，我认为并行流作为解决问题的首次尝试方法更具吸引力。**

由于制作披萨总需要一定的时间，无论你使用哪种并发方法，你能做到的最好情况，是在制作一个披萨的相同时间内制作 n 个披萨。 在这里当然很容易看出来，但是当你处理更复杂的问题时，你就可能忘记这一点。 通常，在项目开始时进行粗略的计算，就能很快弄清楚最大可能的并行吞吐量，这可以防止你因为采取无用的加快运行速度的举措而忙得团团转。

使用 **CompletableFutures**  或许可以轻易地带来重大收益，但是在尝试更进一步时需要倍加小心，因为额外增加的成本和工作量会非常容易远远超出你之前拼命挤出的那一点点收益。

## 本章小结

需要并发的唯一理由是“等待太多”。这也可以包括用户界面的响应速度，但是由于 Java 用于构建用户界面时并不高效，因此[^8] 这仅仅意味着“你的程序运行速度还不够快”。

如果并发很容易，则没有理由拒绝并发。 正因为并发实际上很难，所以你应该仔细考虑是否值得为此付出努力，并考虑你能否以其他方式提升速度。

例如，迁移到更快的硬件（这可能比消耗程序员的时间要便宜得多）或者将程序分解成多个部分，然后在不同的机器上运行这些部分。

奥卡姆剃刀是一个经常被误解的原则。 我看过至少一部电影，他们将其定义为”最简单的解决方案是正确的解决方案“，就好像这是某种毋庸置疑的法律。实际上，这是一个准则：**面对多种方法时，请先尝试需要最少假设的方法。** 在编程世界中，这已演变为**“尝试可能可行的最简单的方法”。**当你了解了特定工具的知识时——就像你现在了解了有关并发性的知识一样，你可能会很想使用它，或者提前规定你的解决方案必须能够“速度飞快”，从而来证明从一开始就进行并发设计是合理的。但是，我们的奥卡姆剃刀编程版本表示你应该首先尝试最简单的方法（这种方法开发起来也更便宜），然后看看它是否足够好。

由于我出身于底层学术背景（物理学和计算机工程），所以我很容易想到所有小轮子转动的成本。**我确定使用最简单的方法不够快的场景出现的次数已经数不过来了，但是尝试后却发现它实际上绰绰有余。**

### 缺点

并发编程的主要缺点是：

1. 在线程等待共享资源时会降低速度。 

2. 线程管理产生**额外 CPU 开销。**

3. 糟糕的设计决策**带来无法弥补的复杂性。**

4. 诸如饥饿，竞速，死锁和活锁（多线程各自处理单个任务而整体却无法完成）之类的问题。

5. **跨平台的不一致。** 通过一些示例，我发现了某些计算机上很快出现的竞争状况，而在其他计算机上却没有。 如果你在后者上开发程序，则在分发程序时可能会感到非常惊讶。

另外，并发的应用是一门艺术。 Java 旨在允许你创建尽可能多的所需要的对象来解决问题——至少在理论上是这样。[^9] 但是，线程不是典型的对象：**每个线程都有其自己的执行环境，包括堆栈和其他必要的元素，使其比普通对象大得多**。 在大多数环境中，只能在内存用光之前创建数千个 **Thread** 对象。通常，你只需要几个线程即可解决问题，因此一般来说创建线程没有什么限制，但是对于某些设计而言，它会成为一种约束，可能迫使你使用完全不同的方案。

### 共享内存陷阱

并发性的主要困难之一是因为可能有**多个任务共享一个资源（例如对象中的内存）**，并且**你必须确保多个任务不会同时读取和更改该资源。**

我花了多年的时间研究并发。 我了解到你永远无法相信使用共享内存并发的程序可以正常工作。 你可以轻易发现它是错误的，但永远无法证明它是正确的。 这是众所周知的并发原则之一。[^10]

我遇到了许多人，他们对编写正确的线程程序的能力充满信心。 我偶尔开始认为我也可以做好。 对于一个特定的程序，我最初是在只有单个 CPU 的机器上编写的。 那时我能够说服自己该程序是正确的，因为我以为我对 Java 工具很了解。 而且在我的单 CPU 计算机上也没有失败。而到了具有多个 CPU 的计算机，程序出现问题不能运行后，我感到很惊讶，但这还只是众多问题中的一个而已。 这不是 Java 的错； “写一次，到处运行”，在单核与多核计算机间无法扩展到并发编程领域。这是并发编程的基本问题。 实际上你可以在单 CPU 机器上发现一些并发问题，但是在多线程实际上真的在并行运行的多 CPU 机器上，就会出现一些其他问题。

再举一个例子，哲学家就餐的问题可以很容易地进行调整，因此几乎不会产生死锁，这会给你一种一切都棒极了的印象。当涉及到共享内存并发编程时，你永远不应该对自己的编程能力变得过于自信。

### This Albatross is Big

如果你对 Java 并发感到不知所措，那说明你身处在一家出色的公司里。你可以访问 **Thread** 类的[Javadoc](https://docs.oracle.com/javase/8/docs/api/java/lang/Thread.html) 页面， 看一下哪些方法现在是 **Deprecated** （废弃的）。这些是 Java 语言设计者犯过错的地方，因为他们在设计语言时对并发性了解不足。

事实证明，在 Java 的后续版本中添加的许多库解决方案都是无效的，甚至是无用的。 幸运的是，Java 8 中的并行 **Streams** 和 **CompletableFutures** 都非常有价值。但是当你使用旧代码时，仍然会遇到旧的解决方案。

在本书的其他地方，我谈到了 Java 的一个基本问题：每个失败的实验都永远嵌入在语言或库中。 Java 并发强调了这个问题。尽管有不少错误，但错误并不是那么多，因为有很多不同的尝试方法来解决问题。 好的方面是，这些尝试产生了更好，更简单的设计。 不利之处在于，在找到好的方法之前，你很容易迷失于旧的设计中。

### 其他类库

本章重点介绍了相对安全易用的并行工具流和 **CompletableFutures** ，并且仅涉及 Java 标准库中一些更细粒度的工具。 为避免你不知所措，我没有介绍你可能实际在实践中使用的某些库。我们使用了==几个 **Atomic** （原子）类，==**ConcurrentLinkedDeque** ，**ExecutorService** 和 **ArrayBlockingQueue** 。附录：[并发底层原理 ](./Appendix-Low-Level-Concurrency.md) 涵盖了其他一些内容，但是你还想探索 **java.util.concurrent** 的 Javadocs。 但是要小心，因为某些库组件已被新的更好的组件所取代。

### 考虑为并发设计的语言

通常，请谨慎地使用并发。 如果需要使用它，请尝试使用最现代的方法：并行流或 **CompletableFutures** 。 这些==功能旨在（假设你**不尝试共享内存**）使你摆脱麻烦（在 Java 的世界范围内）。==

如果你的并发问题变得比高级 Java 构造所支持的问题更大且更复杂，请考虑使用专为并发设计的语言，仅在需要并发的程序部分中使用这种语言是有可能的。 在撰写本文时，JVM 上最纯粹的功能语言是 Clojure（Lisp 的一种版本）和 Frege（Haskell 的一种实现）。这些使你可以在其中编写应用程序的并发部分语言，并通过 JVM 轻松地与你的主要 Java 代码进行交互。 或者，你可以选择更复杂的方法，即通过外部功能接口（FFI）将 JVM 之外的语言与另一种为并发设计的语言进行通信。[^11]

你很容易被一种语言绑定，**迫使自己尝试使用该语言来做所有事情。** 一个常见的示例是构建 HTML / JavaScript 用户界面。 这些工具确实很难使用，令人讨厌，并且有许多库允许你通过使用自己喜欢的语言编写代码来生成这些工具（例如，**Scala.js** 允许你在 Scala 中完成代码）。

心理上的便利是一个合理的考虑因素。 但是，我希望我在本章（以及附录：[并发底层原理 ](./Appendix-Low-Level-Concurrency.md)）中已经表明 Java 并发是一个你可能无法逃离很深的洞。 与 Java 语言的任何其他部分相比，在视觉上检查代码同时记住所有陷阱所需要的的知识要困难得多。

无论使用特定的语言、库使得并发看起来多么简单，都要将其视为一种妖术，因为总是有东西会在你最不期望出现的时候咬你。

### 拓展阅读

《Java Concurrency in Practice》，出自 Brian Goetz，Tim Peierls， Joshua Bloch，Joseph Bowbeer，David Holmes 和 Doug Lea (Addison Wesley，2006 年)——这些基本上就是 Java 并发世界中的名人名单了《Java Concurrency in Practice》第二版，出自 Doug Lea (Addison-Wesley，2000 年)。尽管这本书出版时间远远早于 Java 5 发布，但 Doug 的大部分工作都写入了 **java.util.concurrent** 库。因此，这本书对于全面理解并发问题至关重要。 它超越了 Java，讨论了跨语言和技术的并发编程。 尽管它在某些地方可能很钝，但值得多次重读（最好是在两个月之间进行消化）。 道格（Doug）是世界上为数不多的真正了解并发编程的人之一，因此这是值得的。

[^1]: 例如,Eric-Raymond 在“Unix 编程艺术”（Addison-Wesley，2004）中提出了一个很好的案例。
[^2]: 可以说，试图将并发性用于后续语言是一种注定要失败的方法，但你必须得出自己的结论
[^3]: 有人谈论在 Java——10 中围绕泛型做一些类似的基本改进，这将是非常令人难以置信的。
[^4]: 这是一种有趣的，虽然不一致的方法。通常，我们期望在公共接口上使用显式类表示不同的行为
[^5]: 不，永远不会有纯粹的功能性 Java。我们所能期望的最好的是一种在 JVM 上运行的全新语言。
[^6]: 当两个任务能够更改其状态以使它们不会被阻止但它们从未取得任何有用的进展时，你也可以使用活动锁。
[^7]: 而不是超线程；通常每个内核有两个超线程，并且在询问内核数量时，本书所使用的 Java 版本会报告超线程的数量。超线程产生了更快的上下文切换，但是只有实际的内核才真的工作，而不是超线程。 ↩
[^8]: 库就在那里用于调用，而语言本身就被设计用于此目的，但实际上它很少发生，以至于可以说”没有“。↩
[^9]: 举例来说，如果没有 Flyweight 设计模式，在工程中创建数百万个对象用于有限元分析可能在 Java 中不可行。↩
[^10]: 在科学中，虽然从来没有一种理论被证实过，但是一种理论必须是可证伪的才有意义。而对于并发性，我们大部分时间甚至都无法得到这种可证伪性。↩
[^11]: 尽管 **Go** 语言显示了 FFI 的前景，但在撰写本文时，它并未提供跨所有平台的解决方案。

<!-- 分页 -->

































<!-- Appendix: Low-Level Concurrency -->

# 附录:并发底层原理

> 尽管不建议你自己编写底层 Java 并发代码，但是这样通常有助于了解它是如何工作的。

[并发编程](./24-Concurrent-Programming.md) 章节中介绍了一些用于高级并发的概念，包括为 Java 并发编程而最新提出的，更安全的概念（ parallel Streams 和 CompletableFutures  ）。本附录则介绍在 Java 中底层并发概念，因此在阅读本篇时，你能有所了解掌握这些代码。你还会将进一步了解并发的普遍问题。

在 Java 的早期版本中, 底层并发概念是并发编程的重要组成部分。我们会着眼于围绕这些技巧的复杂性以及为何你应该避免它们而谈。 “并发编程” 章节展示最新的 Java 版本(尤其是 Java 8)所提供的改进技巧，这些技巧使得并发的使用，如果本来不容易使用，也会变得更容易些。

<!-- What is a Thread? -->

## 什么是线程？

并发将程序划分成独立分离运行的任务。每个任务都由一个 *执行线程* 来驱动，我们通常将其简称为 *线程* 。而一个 *线程* 就是操作系统**进程中单一顺序的控制流**。因此，单个进程可以有多个并发执行的任务，但是你的程序使得每个任务都好像有自己的处理器一样。此线程模型为编程带来了便利，它简化了在单一程序中处理变戏法般的多任务过程。操作系统则从处理器上分配时间片到你程序的所有线程中。

Java 并发的==核心机制是 **Thread** 类==，在该语言最初版本中， **Thread （线程）** 是由程序员直接创建和管理的。随着语言的发展以及人们发现了更好的一些方法，中间层机制 - 特别是 **Executor** 框架  - 被添加进来，以消除自己管理线程时候的心理负担（及错误）。 最终，甚至发展出比 **Executor** 更好的机制，如 [并发编程](./24-Concurrent-Programming.md) 一章所示。

**Thread（线程）** 是将任务关联到处理器的软件概念。虽然创建和使用 **Thread**  类看起来与任何其他类都很相似，但实际上它们是非常不同的。当你创建一个 **Thread** 时，JVM 将**分配一大块内存到专为线程保留的特殊区域上**，用于提供运行任务时所需的一切，包括：

* 程序计数器，指明要执行的下一个 JVM 字节码指令。
* 用于支持 Java 代码执行的栈，包含有关此线程已到达当时执行位置所调用方法的信息。它也包含每个正在执行的方法的所有局部变量(包括原语和堆对象的引用)。**每个线程的栈通常在 64K 到 1M 之间** [^1] 。
* 第二个则用于 native code（本机方法代码）执行的栈
* *thread-local variables* （线程本地变量）的存储区域
* 用于控制线程的状态管理变量

包括 `main()` 在内的所有代码都会在某个线程内运行。 每当调用一个方法时，当前程序计数器被推到该线程的栈上，然后栈指针向下移动以足够来创建一个栈帧，其栈帧里存储该方法的所有局部变量，参数和返回值。所有基本类型变量都直接在栈上，虽然方法中创建（或方法中使用）对象的任何引用都位于栈帧中，但对象本身存于堆中。这仅且只有一个堆，被程序中所有线程所共享。

除此以外，线程必须绑定到操作系统，这样它就可以在某个时候连接到处理器。这是作为线程构建过程的一部分为你管理的。Java 使用底层操作系统中的机制来管理线程的执行。

### 最佳线程数

如果你查看第 24 章 [并发编程](./24-Concurrent-Programming.md) 中使用 *CachedThreadPool* 的用例，你会发现 **ExecutorService** 为每个我们提交的任务分配一个线程。然而，并行流（**parallel Stream**）在 [**CountingStream.java** ](https://github.com/BruceEckel/OnJava8-Examples/blob/master/concurrent/CountingStream.java
) 中只分配了 8 个线程（id 中 1-7 为工作线程，8 为  `main()` 方法的主线程，它巧妙地将其用作额外的并行流）。如果你尝试提高 `range()` 方法中的上限值，你会看到没有创建额外的线程。这是为什么？

我们可以**查出当前机器上处理器的数量**：

```Java
// lowlevel/NumberOfProcessors.java

public class NumberOfProcessors {
  public static void main(String[] args) {
    System.out.println(
    Runtime.getRuntime().availableProcessors());
  }
}
/* Output:
8
*/
```

在我的机器上（使用英特尔酷睿i7），我有四个内核，每个内核呈现两个*超线程*（指一种硬件技巧，能在单个处理器上产生非常快速的上下文切换，在某些情况下可以使内核看起来**像运行两个硬件线程**）。虽然这是 “最近” 计算机上的常见配置(在撰写本文时)，但你可能会看到不同的结果，包括 **CountingStream.java ** 中同等数量的默认线程。

你的操作系统可能有办法来查出关于处理器的更多信息，例如，在Windows 10上，按下 “开始” 键，输入 “任务管理器” 和 Enter 键。点击 “详细信息” 。选择 “性能” 标签,你将会看到各种各样的关于你的硬件信息,包括“内核” 和 “逻辑处理器” 。

事实证明，==**“通用”线程的最佳数量**==就算是**可用处理器的数量**(对于特定的问题可能不是这样)。这原因来自在Java线程之间切换上下文的代价：存储被挂起线程的当前状态，并检索另一个线程的当前状态，以便从它进入挂起的位置继续执行。对于 8 个处理器和 8 个（计算密集型）Java线程，JVM 在运行这8个任务时从不需要切换上下文。对于比处理器数量少的任务，分配更多线程没有帮助。

定义了 “逻辑处理器” 数量的 Intel 超线程，但并没有增加计算能力 - 该特性在硬件级别维护额外的线程上下文，从而加快了上下文切换，这有助于提高用户界面的响应能力。对于计算密集型任务，请考虑将线程数量与物理内核(而不是超线程)的数量匹配。尽管Java认为每个超线程都是一个处理器，但这似乎是由于 Intel 对超线程的过度营销造成的错误。尽管如此**，为了简化编程，我只允许 JVM 决定默认的线程数**。 你将需要试验你的产品应用。 这并不意味着将线程数与处理器数相匹配就适用于所有问题; 相反，它主要用于计算密集型解决方案。

### 我可以创建多少个线程？

Thread（线程）对象的最大部分是用于执行方法的 Java 堆栈。查看 Thread （线程）对象的大小因操作系统而异。该程序通过**创建 Thread 对象来测试它，直到 JVM 内存不足为止：**

```java
// lowlevel/ThreadSize.java
// {ExcludeFromGradle} Takes a long time or hangs
import java.util.concurrent.*;
import onjava.Nap;

public class ThreadSize {
  static class Dummy extends Thread {
    @Override
    public void run() { new Nap(1); }
  }
  public static void main(String[] args) {
    ExecutorService exec =
      Executors.newCachedThreadPool();
    int count = 0;
    try {
      while(true) {
        exec.execute(new Dummy());
        count++;
      }
    } catch(Error e) {
      System.out.println(
      e.getClass().getSimpleName() + ": " + count);
      System.exit(0);
    } finally {
      exec.shutdown();
    }
  }
}
```

只要你不断递交任务，**CachedThreadPool** 就会继续创建线程。将 **Dummy** 对象递交到 `execute()` 方法以开始任务，如果线程池无可用线程，则分配一个新线程。执行的暂停方法 `pause()` 运行时间必须足够长，使任务不会开始即完成(从而为新任务释放现有线程)。只要任务不断进入而没有完成，**CachedThreadPool** 最终就会耗尽内存。

我并不总是能够在我尝试的每台机器上造成内存不足的错误。在一台机器上，我看到这样的结果:

```shell
> java ThreadSize
OutOfMemoryError: 2816
```

我们可以使用 **-Xss** 标记减少每个线程栈分配的内存大小。允许的最小线程栈大小是 64k:

```shell
>java -Xss64K ThreadSize
OutOfMemoryError: 4952
```

如果我们将线程栈大小增加到 2M ，我们就可以分配更少的线程。

```shell
>java -Xss2M ThreadSize
OutOfMemoryError: 722
```

**Windows 操作系统默认栈大小是 320K**，我们可以通过验证它给出的数字与我们完全不设置栈大小时的数字是大致相同:

```shell
>java -Xss320K ThreadSize
OutOfMemoryError: 2816
```

你还可以使用 **-Xmx** 标志增加 JVM 的最大内存分配:

```shell
>java -Xss64K -Xmx5M ThreadSize
OutOfMemoryError: 5703
```

请注意的是操作系统还可能对允许的线程数施加限制。

因此**，“我可以拥有多少线程”这一问题的答案是“几千个”**。但是，如果你发现自己分配了数千个线程，那么你可能需要重新考虑你的做法; **恰当的问题是“我需要多少线程？”**

### The WorkStealingPool (工作窃取线程池)

这是一个 **ExecutorService** ，它使用所有可用的(由JVM报告) 处理器自动创建线程池。

```java
// lowlevel/WorkStealingPool.java
import java.util.stream.*;
import java.util.concurrent.*;

class ShowThread implements Runnable {
  @Override
  public void run() {
    System.out.println(
    Thread.currentThread().getName());
  }
}

public class WorkStealingPool {
  public static void main(String[] args)
    throws InterruptedException {
    System.out.println(
      Runtime.getRuntime().availableProcessors());
    ExecutorService exec =
      Executors.newWorkStealingPool();
    IntStream.range(0, 10)
      .mapToObj(n -> new ShowThread())
      .forEach(exec::execute);
    exec.awaitTermination(1, TimeUnit.SECONDS);
  }
}
/* Output:
8
ForkJoinPool-1-worker-2
ForkJoinPool-1-worker-1
ForkJoinPool-1-worker-2
ForkJoinPool-1-worker-3
ForkJoinPool-1-worker-2
ForkJoinPool-1-worker-1
ForkJoinPool-1-worker-3
ForkJoinPool-1-worker-1
ForkJoinPool-1-worker-4
ForkJoinPool-1-worker-2
*/
```

工作窃取算法允许已经耗尽输入队列中的工作项的线程从其他队列“窃取”工作项。目标是在处理器之间分配工作项，从而最大限度地利用所有可用的处理器来完成计算密集型任务。这项算法**也用于 Java 的fork/join 框架。**

<!-- Catching Exceptions -->

## 异常捕获

这可能会让你感到惊讶：

```java
// lowlevel/SwallowedException.java
import java.util.concurrent.*;

public class SwallowedException {
  public static void main(String[] args)
    throws InterruptedException {
    ExecutorService exec =
      Executors.newSingleThreadExecutor();
    exec.submit(() -> {
      throw new RuntimeException();
    });
    exec.shutdown();
  }
}
```

这个程序什么也不输出（然而，如果你用 **execute** 方法替换 `submit()` 方法，你就将会看到异常抛出。这**说明在线程中抛出异常是很棘手的**，需要特别注意的事情。

你无法捕获到从线程逃逸的异常。一旦异常越过了任务的 `run()` 方法，它就会传递至控制台，除非你采取特殊步骤来捕获此类错误异常。

下面是一个抛出异常的代码，该异常会传递到它的 `run()` 方法之外，而 `main()` 方法会显示运行它时会发生什么：

```java
// lowlevel/ExceptionThread.java
// {ThrowsException}
import java.util.concurrent.*;

public class ExceptionThread implements Runnable {
  @Override
  public void run() {
    throw new RuntimeException();
  }
  public static void main(String[] args) {
    ExecutorService es =
      Executors.newCachedThreadPool();
    es.execute(new ExceptionThread());
    es.shutdown();
  }
}
/* Output:
___[ Error Output ]___
Exception in thread "pool-1-thread-1"
java.lang.RuntimeException
        at ExceptionThread.run(ExceptionThread.java:8)
        at java.util.concurrent.ThreadPoolExecutor.runW
orker(ThreadPoolExecutor.java:1142)
        at java.util.concurrent.ThreadPoolExecutor$Work
er.run(ThreadPoolExecutor.java:617)
        at java.lang.Thread.run(Thread.java:745)
*/
```

输出是(经过调整一些限定符以适应阅读)：

```
Exception in thread "pool-1-thread-1" RuntimeException
  at ExceptionThread.run(ExceptionThread.java:9)
  at ThreadPoolExecutor.runWorker(...)
  at ThreadPoolExecutor$Worker.run(...)
  at java.lang.Thread.run(Thread.java:745)
```

即使在 `main()` 方法体内包裹 **try-catch** 代码块来捕获异常也不成功：

```java
// lowlevel/NaiveExceptionHandling.java
// {ThrowsException}
import java.util.concurrent.*;

public class NaiveExceptionHandling {
  public static void main(String[] args) {
    ExecutorService es =
      Executors.newCachedThreadPool();
    try {
      es.execute(new ExceptionThread());
    } catch(RuntimeException ue) {
      // This statement will NOT execute!
      System.out.println("Exception was handled!");
    } finally {
      es.shutdown();
    }
  }
}
/* Output:
___[ Error Output ]___
Exception in thread "pool-1-thread-1"
java.lang.RuntimeException
        at ExceptionThread.run(ExceptionThread.java:8)
        at java.util.concurrent.ThreadPoolExecutor.runW
orker(ThreadPoolExecutor.java:1142)
        at java.util.concurrent.ThreadPoolExecutor$Work
er.run(ThreadPoolExecutor.java:617)
        at java.lang.Thread.run(Thread.java:745)
*/
```

这会产生与前一个示例相同的结果:未捕获异常。

为解决这个问题，需要改变 **Executor** （执行器）生成线程的方式。 ==**Thread.UncaughtExceptionHandler 是一个添加给每个 Thread 对象，用于进行异常处理的接口。**==

当该线程即将死于未捕获的异常时，将自动调用 `Thread.UncaughtExceptionHandler.uncaughtException()`
 方法。为了调用该方法，我们创建一个新的 **ThreadFactory** 类型来让 **Thread.UncaughtExceptionHandler** 对象附加到每个它所新创建的 **Thread**（线程）对象上。我们赋值该工厂对象给 **Executors** 对象的 方法，让它的方法来生成新的 **ExecutorService** 对象：

```java
// lowlevel/CaptureUncaughtException.java
import java.util.concurrent.*;

class ExceptionThread2 implements Runnable {
  @Override
  public void run() {
    Thread t = Thread.currentThread();
    System.out.println("run() by " + t.getName());
    System.out.println(
      "eh = " + t.getUncaughtExceptionHandler());
    throw new RuntimeException();
  }
}

class MyUncaughtExceptionHandler implements
Thread.UncaughtExceptionHandler {
  @Override
  public void uncaughtException(Thread t, Throwable e) {
    System.out.println("caught " + e);
  }
}

class HandlerThreadFactory implements ThreadFactory {
  @Override
  public Thread newThread(Runnable r) {
    System.out.println(this + " creating new Thread");
    Thread t = new Thread(r);
    System.out.println("created " + t);
    t.setUncaughtExceptionHandler(
      new MyUncaughtExceptionHandler());
    System.out.println(
      "eh = " + t.getUncaughtExceptionHandler());
    return t;
  }
}

public class CaptureUncaughtException {
  public static void main(String[] args) {
    ExecutorService exec =
      Executors.newCachedThreadPool(
        new HandlerThreadFactory());
    exec.execute(new ExceptionThread2());
    exec.shutdown();
  }
}
/* Output:
HandlerThreadFactory@4e25154f creating new Thread
created Thread[Thread-0,5,main]
eh = MyUncaughtExceptionHandler@70dea4e
run() by Thread-0
eh = MyUncaughtExceptionHandler@70dea4e
caught java.lang.RuntimeException
*/
```

额外会在代码中添加跟踪机制，用来验证工厂对象创建的线程是否获得新 **UncaughtExceptionHandler** 。现在未捕获的异常由 **uncaughtException** 方法捕获。

上面的示例根据具体情况来设置处理器。如果你知道你将要**在代码中处处使用相同的异常处理器**，那么**更简单的方式是在 Thread 类中设置一个 static（静态） 字段**，并将这个**处理器设置为默认的未捕获异常处理器：**

```java
// lowlevel/SettingDefaultHandler.java
import java.util.concurrent.*;

public class SettingDefaultHandler {
  public static void main(String[] args) {
    Thread.setDefaultUncaughtExceptionHandler(
      new MyUncaughtExceptionHandler());
    ExecutorService es =
      Executors.newCachedThreadPool();
    es.execute(new ExceptionThread());
    es.shutdown();
  }
}
/* Output:
caught java.lang.RuntimeException
*/
```

只有在每个线程**没有设置异常处理器时候，默认处理器才会被调用**。系统会检查线程专有的版本，如果没有，则检查是否**线程组中有专有的 `uncaughtException()` 方法**；如果都没有，就会调用 **defaultUncaughtExceptionHandler** 方法。

可以将此方法与 **CompletableFuture** 的改进方法进行比较。

<!-- Sharing Resources -->

## 资源共享

你可以将单线程程序看作一个孤独的实体，在你的问题空间中移动并同一时间只做一件事。因为只有一个实体，你永远不会想到两个实体试图同时使用相同资源的问题：问题犹如两个人试图同时停放在同一个空间，同时走过一扇门，甚至同时说话。

通过并发，事情不再孤单，但现在两个或更多任务可能会相互干扰。如果你不阻止这种冲突，你将有两个任务同时尝试访问同一个银行帐户，打印到同一个打印机，调整同一个阀门，等等。

### 资源竞争

当你启动一个任务来执行某些工作时，可以通过两种不同的方式捕获该工作的结果:**通过副作用或通过返回值。**

从编程方式上看，**副作用似乎更容易**:你只需使用结果来操作环境中的某些东西。例如，你的任务可能会执行一些计算，然后直接将其结果写入集合。

伴随**这种方式的问题是集合通常是共享资源**。当运行多个任务时，任何任务都可能同时读写 *共享资源* 。这揭示了 *资源竞争* 问题，这是处理任务时的主要陷阱之一。

在单线程系统中，你不需要考虑资源竞争，因为你永远不可能同时做多件事。当你有多个任务时，你就必须始终防止资源竞争。

解决此问题的的一种方法是使用能够应对资源竞争的集合，如果多个任务同时尝试对此类集合进行写入，那么此类集合可以应付该问题。在 Java 并发库中，你将发现许多尝试解决资源竞争问题的类；在本附录中，你将看到其中的一些，但覆盖范围并不全面。

请思考以下的示例，其中一个任务负责生成偶数，其他任务则负责消费这些数字。在这里，消费者任务的唯一工作就是检查偶数的有效性。

我们将定义消费者任务 **EvenChecker** 类，以便在后续示例中可复用。为了将 **EvenChecker** 与我们的各种实验生成器类解耦，我们首先创建名为 **IntGenerator** 的抽象类，它包含 **EvenChecker** 必须知道的最低必要方法：它包含 `next()` 方法，以及可以取消它执行生成的方法。

```java
// lowlevel/IntGenerator.java
import java.util.concurrent.atomic.AtomicBoolean;

public abstract class IntGenerator {
  private AtomicBoolean canceled =
    new AtomicBoolean();
  public abstract int next();
  public void cancel() { canceled.set(true); }
  public boolean isCanceled() {
    return canceled.get();
  }
}
```

`cancel()` 方法改变 **AtomicBoolean** 类型的 **canceled** 标志位的状态， 而 `isCanceled()` 方法则告诉标志位是否设置。因为 **canceled** 标志位是 **AtomicBoolean** 类型，由于它是原子性的，这意味着分配和值返回等简单操作发生时没有中断的可能性，因此你无法在这些简单操作中看到该字段处于中间状态。你将在本附录的后面部分了解有关原子性和 **Atomic** 类的更多信息

任何 **IntGenerator** 都可以使用下面的 **EvenChecker** 类进行测试:

```java
// lowlevel/EvenChecker.java
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import onjava.TimedAbort;

public class EvenChecker implements Runnable {
  private IntGenerator generator;
  private final int id;
  public EvenChecker(IntGenerator generator, int id) {
    this.generator = generator;
    this.id = id;
  }
  @Override
  public void run() {
    while(!generator.isCanceled()) {
      int val = generator.next();
      if(val % 2 != 0) {
        System.out.println(val + " not even!");
        generator.cancel(); // Cancels all EvenCheckers
      }
    }
  }
  // Test any IntGenerator:
  public static void test(IntGenerator gp, int count) {
    List<CompletableFuture<Void>> checkers =
      IntStream.range(0, count)
        .mapToObj(i -> new EvenChecker(gp, i))
        .map(CompletableFuture::runAsync)
        .collect(Collectors.toList());
    checkers.forEach(CompletableFuture::join);
  }
  // Default value for count:
  public static void test(IntGenerator gp) {
    new TimedAbort(4, "No odd numbers discovered");
    test(gp, 10);
  }
}
```

`test()` 方法开启了许多访问同一个 **IntGenerator** 的 **EvenChecker**。**EvenChecker** 任务们会不断读取和测试与其关联的 **IntGenerator** 对象中的生成值。如果 **IntGenerator** 导致失败，`test()` 方法会报告并返回。

依赖于 **IntGenerator** 对象的所有 **EvenChecker** 任务都会检查它是否已被取消。如果 `generator.isCanceled()` 返回值为 true ，则 `run()` 方法返回。 任何 **EvenChecker** 任务都可以在 **IntGenerator** 上调用 `cancel()` ，这会导致使用该 **IntGenerator** 的其他所有 **EvenChecker** 正常关闭。

在本设计中，共享公共资源（ **IntGenerator** ）的任务会监视该资源的终止信号。这消除所谓的竞争条件，其中两个或更多的任务竞争响应某个条件并因此冲突或不一致结果的情况。

你必须仔细考虑并防止并发系统失败的所有可能途径。例如，一个任务不能依赖于另一个任务，因为任务关闭的顺序无法得到保证。这里，通过使任务依赖于非任务对象，我们可以消除潜在的竞争条件。

一般来说，我们假设 `test()` 方法最终失败，因为各个 **EvenChecker** 的任务在 **IntGenerator** 处于 “不恰当的” 状态时，仍能够访问其中的信息。但是，直到 **IntGenerator** 完成许多循环之前，它可能无法检测到问题，具体取决于操作系统的详细信息和其他实现细节。为确保本书的自动构建不会卡住，我们使用 **TimedAbort** 类，在此处定义：

```java
// onjava/TimedAbort.java
// Terminate a program after t seconds
package onjava;
import java.util.concurrent.*;

public class TimedAbort {
  private volatile boolean restart = true;
  public TimedAbort(double t, String msg) {
    CompletableFuture.runAsync(() -> {
      try {
        while(restart) {
          restart = false;
          TimeUnit.MILLISECONDS
            .sleep((int)(1000 * t));
        }
      } catch(InterruptedException e) {
        throw new RuntimeException(e);
      }
      System.out.println(msg);
      System.exit(0);
    });
  }
  public TimedAbort(double t) {
    this(t, "TimedAbort " + t);
  }
  public void restart() { restart = true; }
}
```

我们使用 lambda 表达式创建一个 **Runnable** ，该表达式使用 **CompletableFuture** 的 `runAsync()` 静态方法执行。  `runAsync()` 方法的值会立即返回。 因此，**TimedAbort** 不会保持任何打开的任务，否则已完成任务，但如果它需要太长时间，它仍将终止该任务（ **TimedAbort** 有时被称为**守护进程**）。

**TimedAbort** 还允许你 `restart()` 方法重启任务，在有某些有用的活动进行时保持程序打开。

我们可以看到正在运行的 **TimedAbort** 示例:

```java
// lowlevel/TestAbort.java
import onjava.*;

public class TestAbort {
  public static void main(String[] args) {
    new TimedAbort(1);
    System.out.println("Napping for 4");
    new Nap(4);
  }
}
/* Output:
Napping for 4
TimedAbort 1.0
*/
```

如果你注释掉 **Nap** 创建实列那行，程序执行会立即退出，表明 **TimedAbort** 没有维持程序打开。

我们将看到第一个 **IntGenerator** 示例有一个生成一系列偶数值的 `next()` 方法：

```java
// lowlevel/EvenProducer.java
// When threads collide
// {VisuallyInspectOutput}

public class EvenProducer extends IntGenerator {
  private int currentEvenValue = 0;
  @Override
  public int next() {
    ++currentEvenValue; // [1]
    ++currentEvenValue;
    return currentEvenValue;
  }
  public static void main(String[] args) {
    EvenChecker.test(new EvenProducer());
  }
}
/* Output:
419 not even!
425 not even!
423 not even!
421 not even!
417 not even!
*/
```

* [1] 一个任务有可能在另外一个任务执行第一个对 **currentEvenValue** 的自增操作之后，但是没有执行第二个操作之前，调用 `next()` 方法。这将使这个值处于 “不恰当” 的状态。

为了证明这是可能发生的， `EvenChecker.test()` 创建了一组 **EventChecker** 对象，以连续读取 **EvenProducer** 的输出并测试检查每个数值是否都是偶数。如果不是，就会报告错误，而程序也将关闭。

多线程程序的部分问题是，即使存在 bug ，如果失败的可能性很低，程序仍然可以正确显示。

重要的是要注意到**==自增操作自身需要多个步骤，==**并且在自增过程中任务可能会被线程机制挂起 - 也就是说==**，在 Java 中，自增不是原子性的操作**==。因此，**如果不保护任务，即使单纯的自增也不是线程安全的。**

该示例程序并不总是在第一次非偶数产生时终止。所有任务都不会立即关闭，这是并发程序的典型特征。

### 解决资源竞争

前面的示例揭示了当你使用线程时的基本问题：你永远不知道线程哪个时刻运行。想象一下坐在一张桌子上，用叉子，将最后一块食物放在盘子上，当叉子到达时，食物突然消失...仅因为你的线程被挂起而另一个用餐者进来吃了食物了。这就是在编写并发程序时要处理的问题。为了使并发工作有效，你需要某种方式来阻止两个任务访问同一个资源，至少在关键时期是这样。

**防止这种冲突的方法**就是**当资源被一个任务使用时，在其上加锁。**第一个访问某项资源的任务必须锁定这项资源，使其他任务在其被解锁之前，就无法访问它，而在其被解锁时候，另一个任务就可以锁定并使用它，以此类推。如果汽车前排座位是受限资源，那么大喊着 “冲呀” 的孩子就会（在这次旅途过程中）获得该资源的锁。

为了解决线程冲突的问题，基本的并发方案将序列化访问共享资源。这意味着一次只允许一个任务访问共享资源。这通常是通过在访问资源的代码片段周围加上一个子句来实现的，该子句一次只允许一个任务访问这段代码。因为这个子句产生 *互斥* 效果，所以这种机制的通常称为是 *mutex* （互斥量）。

考虑一下屋子里的浴室：多个人（即多个由线程驱动的任务）都希望能独立使用浴室（即共享资源）。为了使用浴室，一个人先敲门来看看是否可用。如果没人的话，他就能进入浴室并锁上门。任何其他想使用浴室的任务就会被 “阻挡”，因此这些任务就在门口等待，直到浴室是可用的。

当浴室使用完毕，就是时候给其他任务进入，这时比喻就有点不准确了。事实上没有人排队，我们也不知道下一个使用浴室是谁，因为线程调度机制并不是确定性的。相反，就好像在浴室前面有一组被阻止的任务一样，当锁定浴室的任务解锁并出现时，线程调度机制将会决定下一个要进入的任务。

Java 以提供关键字 **synchronized** 的形式，为**防止资源冲突提供了内置支持。**当任务希望执行被 **synchronized** 关键字保护的代码片段的时候，Java 编译器会生成代码以查看锁是否可用。如果可用，该任务获取锁，执行代码，然后释放锁。

共享资源一般是以对象形式存在的内存片段，但也可以是文件、I/O 端口，或者类似打印机的东西。要控制对共享资源的访问，得先把它包装进一个对象。然后把任何访问该资源的方法标记为 **synchronized** 。 如果一个任务在调用其中一个 **synchronized** 方法之内，那么在这个任务从该方法返回之前，其他所有要调用该对象的 **synchronized** 方法的任务都会被阻塞。

通常你会将字段设为 **private**，并仅通过方法访问这些字段。你可用通过使用 **synchronized** 关键字声明方法来防止资源冲突。如下所示：

```java
synchronized void f() { /* ... */ }
synchronized void g() { /* ... */ }
```

所有对象都**自动包含独立的锁（也称为 *monitor*，即监视器）**。当你调用对象上任何 **synchronized** 方法，**此对象将被加锁**，并且该对象上的的==其他 **synchronized** 方法==调用只有等到前一个方法执行完成并释放了锁之后才能被调用。如果一个任务对对象调用了 `f()` ，对于同一个对象而言，就只能等到 `f()` 调用结束并释放了锁之后，其他任务才能调用 `f()` 和 `g()`。所以，某个特定对象的所有 **synchronized** 方法**共享同一个锁**，这个锁可以防止多个任务同时写入对象内存。

在使用并发时，将字段设为 **private** 特别重要；否则，**synchronized** 关键字不能阻止其他任务直接访问字段，从而产生资源冲突。

一个线程可以获取对象的锁多次。如果一个方法调用在同一个对象上的第二个方法，而后者又在同一个对象上调用另一个方法，就会发生这种情况。 JVM 会跟踪对象被锁定的次数。如果对象已解锁，则其计数为 0 。当一个线程首次获得锁时，计数变为 1 。每次同一线程在同一对象上获取另一个锁时，计数就会自增。显然，**只有首先获得锁的线程才允许多次获取多个锁**。每当线程离开 **synchronized** 方法时，计数递减，直到计数变为 0 ，完全释放锁以给其他线程使用。**每个类也有一个锁**（作为该类的 **Class** 对象的一部分），因此 **synchronized** 静态方法可以在类范围的基础上彼此锁定，不让同时访问静态数据。

你应该什么时候使用同步呢？可以永远 *Brian* 的同步法则[^2]。

> 如果你正在写一个变量，它可能接下来被另一个线程读取，或者正在读取一个上一次已经被另一个线程写过的变量，那么你必须使用同步，并且，读写线程都必须用相同的监视器锁同步。

如果在你的类中有超过一个方法在处理临界数据，那么你必须同步所有相关方法。如果只同步其中一个方法，那么其他方法可以忽略对象锁，并且可以不受惩罚地调用。这是很重要的一点：每个访问临界共享资源的方法都必须被同步，否则将不会正确地工作。

### 同步控制 EventProducer

通过在 **EvenProducer.java** 文件中添加 **synchronized** 关键字，可以防止不希望的线程访问：

```java
// lowlevel/SynchronizedEvenProducer.java
// Simplifying mutexes with the synchronized keyword
import onjava.Nap;

public class
SynchronizedEvenProducer extends IntGenerator {
  private int currentEvenValue = 0;
  @Override
  public synchronized int next() {
    ++currentEvenValue;
    new Nap(0.01); // Cause failure faster
    ++currentEvenValue;
    return currentEvenValue;
  }
  public static void main(String[] args) {
    EvenChecker.test(new SynchronizedEvenProducer());
  }
}
/* Output:
No odd numbers discovered
*/
```

在**两个自增操作之间插入 `Nap()` 构造器方法**，以提高在 **currentEvenValue** 是奇数的状态时**上下文切换的可能性。**因为互斥锁可以阻止多个任务同时进入临界区，所有这不会产生失败。第一个进入 `next()` 方法的任务将获得锁，任何试图获取锁的后续任务都将被阻塞，直到第一个任务释放锁。此时，调度机制选择另一个等待锁的任务。通过这种方式，任何时刻只能有一个任务通过互斥锁保护的代码。

<!-- The volatile Keyword -->

## volatile 关键字

**volatile** 可能是 Java 中最微妙和最难用的关键字。幸运的是，在现代 Java 中，你几乎总能避免使用它，如果你确实看到它在代码中使用，你应该保持怀疑态度和怀疑 - 这很有可能代码是过时的，或者编写代码的人不清楚使用它在大体上（或两者都有）易变性（**volatile**） 或并发性的后果。

使用 **volatile** 有三个理由。

### 字分裂

当你的 Java 数据类型足够大（在 Java 中 **long** 和 **double** 类型都是 64 位），写入变量的过程分两步进行，就会发生 ***Word tearing* （字分裂）情况**。 JVM 被允许**将64位数量的读写作为两个单独的32位操作执行**[^3]，这增加了在读写过程中发生上下文切换的可能性，因此其他任务会看到不正确的结果。这被称为 *Word tearing* （字分裂），因为你可能只看到其中一部分修改后的值。基本上，任务有时可以在第一步之后但在第二步之前读取变量，从而产生垃圾值（对于例如 **boolean** 或 **int** 类型的小变量是没有问题的；任何 **long** 或 **double** 类型则除外）。

在缺乏任何其他保护的情况下，用 **volatile** 修饰符定义一个 **long** 或 **double** 变量，可阻止字分裂情况。然而，如果使用 **synchronized** 或 **java.util.concurrent.atomic** 类之一保护这些变量，则 **volatile** 将被取代。此外，**volatile** 不会影响到增量操作并不是原子操作的事实。

### 可见性

第二个问题属于 [Java 并发的四句格言](./24-Concurrent-Programming.md#四句格言)里第二句格言 “一切都重要” 的部分。你必须假设每个任务拥有自己的处理器，并且每个处理器都有自己的本地内存缓存。该缓存准许处理器运行的更快，因为处理器并不总是需要从比起使用缓存显著花费更多时间的主内存中获取数据。

出现这个问题是因为 Java 尝试尽可能地提高执行效率。缓存的主要目的是避免从主内存中读取数据。当并发时，有时不清楚 Java 什么时候应该将值从主内存刷新到本地缓存 — 而这个问题称为 ***缓存一致性* （ *cache coherence* ）。**

每个线程都可以在处理器缓存中存储变量的本地副本。将字段定义为 **volatile** 可以防止这些编译器优化，**这样读写就可以直接进入内存，而不会被缓存**。一旦该字段发生写操作，所有任务的读操作都将看到更改。如果一个 **volatile** 字段刚好存储在本地缓存，则会立即将其写入主内存，并且**该字段的任何读取都始终发生在主内存中。**

**volatile** 应该在何时适用于变量：

1. 该变量同时被多个任务访问。
2. 这些访问中至少有一个是写操作。
3. 你尝试避免同步 （在现代 Java 中，你可以使用高级工具来避免进行同步）。

举个例子，如果你使用变量作为停止任务的标志值。那么该变量至少必须声明为 **volatile** （**尽管这并不一定能保证这种标志的线程安全**）。否则，当一个任务更改标志值时，这些更改可以存储在本地处理器缓存中，而不会刷新到主内存。当另一个任务查看标记值时，它不会看到更改。我更喜欢在 [并发编程](./24-Concurrent-Programming.md) 中 [终止耗时任务](./24-Concurrent-Programming.md#终止耗时任务) 章节中使用 **AtomicBoolean** 类型作为标志值的办法

任务对其自身变量所做的任何写操作都始终对该任务可见，因此，如果只在任务中使用变量，你不需要使其变量声明为 **volatile** 。

如果单个线程对变量写入而其他线程只读取它，你可以放弃该变量声明为 **volatile**。通常，如==果你有多个线程对变量写入，**volatile** 无法解决你的问题==，并且你必须使用 **synchronized** 来防止竞争条件。 这有一个特殊的例外：可以让多个线程对该变量写入，*只要它们不需要先读取它并使用该值创建新值来写入变量* 。如果这些多个线程在结果中使用旧值，则会出现竞争条件，因为其余一个线程之一可能会在你的线程进行计算时修改该变量。即使你开始做对了，想象一下在代码修改或维护过程中忘记和引入一个重大变化是多么容易，或者对于不理解问题的不同程序员来说是多么容易（这在 Java 中尤其成问题因为程序员倾向于严重依赖编译时检查来告诉他们，他们的代码是否正确）。

重要的是要理解原子性和可见性是两个不同的概念。在非 **volatile** 变量上的原子操作**是不能保证是否将其刷新到主内存。**

同步也会让主内存刷新，所以==如果一个变量完全由 **synchronized** 的方法或代码段(或者 **java.util.concurrent.atomic** 库里类型之一)所保护，则不需要让变量用 **volatile**。==

### 重排与 *Happen-Before* 原则

只要结果不会改变程序表现，Java 可以通过重排指令来优化性能。然而，重排可能会影响本地处理器缓存与主内存交互的方式，从而产生细微的程序 bug 。直到 Java 5 才理解并解决了这个无法阻止重排的问题。现在，**volatile** 关键字可以阻止重排 **volatile** 变量周围的读写指令。这种重排规则称为 *happens before* 担保原则 。

这项原则保证在 **volatile** 变量读写之前发生的指令先于它们的读写之前发生。同样，任何跟随 **volatile** 变量之后读写的操作都保证发生在它们的读写之后。例如：

```java
// lowlevel/ReOrdering.java

public class ReOrdering implements Runnable {
  int one, two, three, four, five, six;
  volatile int volaTile;
  @Override
  public void run() {
    one = 1;
    two = 2;
    three = 3;
    volaTile = 92;
    int x = four;
    int y = five;
    int z = six;
  }
}
```

例子中 **one**，**two**，**three** 变量赋值操作就可以被重排，只要它们都发生在 **volatile** 变量写操作之前。同样，只要 **volatile** 变量写操作发生在所有语句之前， **x**，**y**，**z** 语句可以被重排。这种 **volatile** （易变性）操作通常**称为 *memory barrier* （内存屏障）**。 *happens before* 担保原则确保 **volatile** 变量的读写指令不能跨过内存屏障进行重排。

*happens before* 担保原则还有另一个作用：当线程向一个 **volatile** 变量写入时，在线程写入之前的其他所有变量（包括非 **volatile** 变量）也会刷新到主内存。当线程读取一个 **volatile** 变量时，它也会读取其他所有变量（包括非 **volatile** 变量）与 **volatile** 变量一起刷新到主内存。尽管这是一个重要的特性，它解决了 Java 5 版本之前出现的一些非常狡猾的 bug ，**但是你不应该依赖这项特性来“自动”使周围的变量变得易变性 （ volatile ）的** 。如果你希望变量是易变性 （ **volatile** ）的，那么维护代码的任何人都应该清楚这一点。

### 什么时候使用 volatile

对于 Java 早期版本，编写一个证明需要 **volatile** 的示例并不难。如果你进行搜索，你可以找到这样的例子，但是如果你在 Java 8 中尝试这些例子，它们就不起作用了(我没有找到任何一个)。我努力写这样一个例子，但没什么用。这可能原因是 JVM 或者硬件，或两者都得到了改进。这种效果对现有的应该  **volatile** （易变性） 但不 **volatile** 的存储的程序是有益的；对于此类程序，失误发生的频率要低得多，而且问题更难追踪。

如果你尝试使用 **volatile** ，你可能**更应该尝试让一个变量线程安全而不是引起同步的成本**。因为 **volatile** 使用起来非常微妙和棘手，所以**==我建议根本不要使用它;==**相反，请使用本附录后面介绍的 **java.util.concurrent.atomic** 里面类之一。它们**以比同步低得多的成本提供了完全的线程安全性。**

如果你正在尝试调试其他人的并发代码，请首先查找使用 **volatile** 的代码并将其替换为**Atomic** 变量。除非你确定程序员对并发性有很高的理解，否则它们很可能会误用 **volatile** 。

<!-- Atomicity -->

## 原子性

在 Java 线程的讨论中，经常反复提交但不正确的知识是：“原子操作不需要同步”。 一个 *原子操作* 是**不能被线程调度机制中断的操作**；一旦操作开始，那么它一定可以在可能发生的“上下文切换”之前（切换到其他线程执行）执行完毕。依赖于原子性是很棘手且很危险的，如果你是一个并发编程专家，或者你得到了来自这样的专家的帮助，你才应该使用原子性来代替同步，如果你认为自己足够聪明可以应付这种玩火似的情况，那么请接受下面的测试：

> Goetz 测试：如果你可以编写用于现代微处理器的高性能 JVM ，那么就有资格考虑是否可以避免同步[^4] 。

了解原子性是很有用的，并且知道它与其他高级技术一起用于实现一些更加巧妙的  **java.util.concurrent** 库组件。 但是==**要坚决抵制自己依赖它的冲动。**==

原子性可以应用于除 **long** 和 **double** 之外的所有基本类型之上的 “简单操作”。对于读写和写入除 **long** 和 **double** 之外的基本类型变量这样的操作，可以保证它们作为不可分 (原子) 的操作执行。


因为原子操作不能被线程机制中断。专家程序员可以利用这个来编写无锁代码（*lock-free code*），这些代码不需要被同步。但即使这样也过于简单化了。**有时候，甚至看起来应该是安全的原子操作，实际上也可能不安全。**本书的读者通常不会通过前面提到的 Goetz 测试，因此也就不具备用原子操作来替换同步的能力。尝试着移除同步通常是一种表示不成熟优化的信号，并且会给你带来大量的麻烦，可能不会获得太多或任何的好处。

在多核处理器系统，相对于单核处理器而言，可见性问题远比原子性问题多得多。一个任务所做的修改，即使它们是原子性的，也可能对其他任务不可见（例如，**修改只是暂时性存储在本地处理器缓存中**），因此不同的任务对应用的状态有不同的视图。另一方面，同步机制强制多核处理器系统上的一个任务做出的修改必须在应用程序中是可见的。如果没有同步机制，那么修改时可见性将无法确认。

什么才属于原子操作时？对于属性中的值做赋值和返回操作通常都是原子性的，但是在 C++ 中，甚至下面的操作都可能是原子性的：

```c++
i++; // Might be atomic in C++
i += 2; // Might be atomic in C++
```

但是在 C++ 中，这取决于编译器和处理器。你无法编写出依赖于原子性的 C++ 跨平台代码，因为 C++ [^5]没有像 Java 那样的一致 *内存模型* （memory model）。

在 Java 中，上面的操作肯定不是原子性的，正如下面的方法产生的 JVM 指令中可以看到的那样：

```java
// lowlevel/NotAtomic.java
// {javap -c NotAtomic}
// {VisuallyInspectOutput}

public class NotAtomic {
  int i;
  void f1() { i++; }
  void f2() { i += 3; }
}
/* Output:
Compiled from "NotAtomic.java"
public class NotAtomic {
  int i;

  public NotAtomic();
    Code:
       0: aload_0
       1: invokespecial #1 // Method
java/lang/Object."<init>":()V
       4: return

  void f1();
    Code:
       0: aload_0
       1: dup
       2: getfield      #2 // Field
i:I
       5: iconst_1
       6: iadd
       7: putfield      #2 // Field
i:I
      10: return

  void f2();
    Code:
       0: aload_0
       1: dup
       2: getfield      #2 // Field
i:I
       5: iconst_3
       6: iadd
       7: putfield      #2 // Field
i:I
      10: return
}
*/
```

每条指令都会产生一个 “get” 和 “put”，它们之间还有一些其他指令。因此在获取指令和放置指令之间，另有一个任务可能会修改这个属性，所有，这些操作不是原子性的。

让我们通过定义一个抽象类来测试原子性的概念，这个抽象类的方法是将一个整数类型进行偶数自增，并且 `run()` 不断地调用这个方法:

```java
// lowlevel/IntTestable.java
import java.util.function.*;

public abstract class
IntTestable implements Runnable, IntSupplier {
  abstract void evenIncrement();
  @Override
  public void run() {
    while(true)
      evenIncrement();
  }
}
```

**IntSupplier** 是一个带 `getAsInt()` 方法的函数式接口。

现在我们可以创建一个测试，它作为一个独立的任务启动 `run()` 方法 ，然后获取值来检查它们是否为偶数:

```java
// lowlevel/Atomicity.java
import java.util.concurrent.*;
import onjava.TimedAbort;

public class Atomicity {
  public static void test(IntTestable it) {
    new TimedAbort(4, "No failures found");
    CompletableFuture.runAsync(it);
    while(true) {
      int val = it.getAsInt();
      if(val % 2 != 0) {
        System.out.println("failed with: " + val);
        System.exit(0);
      }
    }
  }
}
```

很容易盲目地应用原子性的概念。在这里，`getAsInt()` 似乎是安全的原子性方法：

```java
// lowlevel/UnsafeReturn.java
import java.util.function.*;
import java.util.concurrent.*;

public class UnsafeReturn extends IntTestable {
  private int i = 0;
  public int getAsInt() { return i; }
  public synchronized void evenIncrement() {
    i++; i++;
  }
  public static void main(String[] args) {
    Atomicity.test(new UnsafeReturn());
  }
}
/* Output:
failed with: 79
*/
```

但是， `Atomicity.test()` 方法还是出现有非偶数的失败。尽管，返回 **i** 变量确实是原子操作，但是**同步缺失允许了在对象处于不稳定的中间状态时读取值。**最重要的是，由于 **i** 也不是 **volatile** 变量，所以**存在可见性问题**。包括 `getValue()` 和 `evenIncrement()` **都必须同步(**这也顾及到没有使用 **volatile** 修饰的 **i** 变量):

```java
// lowlevel/SafeReturn.java
import java.util.function.*;
import java.util.concurrent.*;

public class SafeReturn extends IntTestable {
  private int i = 0;
  public synchronized int getAsInt() { return i; }
  public synchronized void evenIncrement() {
    i++; i++;
  }
  public static void main(String[] args) {
    Atomicity.test(new SafeReturn());
  }
}
/* Output:
No failures found
*/
```

只有并发编程专家有能力去尝试做像前面例子情况的优化；再次强调，请遵循 Brain 的同步法则。

### Josh 的序列号

作为第二个示例，考虑某些更简单的东西：创建一个产生序列号的类，灵感启发于 Joshua Bloch 的 *Effective Java Programming Language Guide* (Addison-Wesley 出版社, 2001) 第 190 页。每次调用 `nextSerialNumber()` 都必须返回唯一值。

```java
// lowlevel/SerialNumbers.java

public class SerialNumbers {
  private volatile int serialNumber = 0;
  public int nextSerialNumber() {
    return serialNumber++; // Not thread-safe
  }
}
```

**SerialNumbers**  是你可以想象到最简单的类，如果你具备 C++ 或者其他底层的知识背景，你可能会认为自增是一个原子操作，因为 C++ 的自增操作通常被单个微处理器指令所实现（尽管不是以任何一致，可靠，跨平台的方式）。但是，正如前面所提到的，**Java 自增操作不是原子性的**，并且**操作同时涉及读取和写入**，因此即使在这样一个简单的操作中，也存在有线程问题的空间。

我们在这里加入 volatile ，看看它是否有帮助。然而，真正的问题是 `nextSerialNumber()` 方法在不进行线程同步的情况下访问共享的可变变量值。

为了测试 **SerialNumbers**，我们将创建一个不会耗尽内存的集合，假如需要很长时间来检测问题。这里展示的 **CircularSet** 重用了存储 **int** 变量的内存，最终新值会覆盖旧值(复制的速度通常发生足够快，你也可以使用  **java.util.Set** 来代替):

```java
// lowlevel/CircularSet.java
// Reuses storage so we don't run out of memory
import java.util.*;

public class CircularSet {
  private int[] array;
  private int size;
  private int index = 0;
  public CircularSet(int size) {
    this.size = size;
    array = new int[size];
    // Initialize to a value not produced
    // by SerialNumbers:
    Arrays.fill(array, -1);
  }
  public synchronized void add(int i) {
    array[index] = i;
    // Wrap index and write over old elements:
    index = ++index % size;
  }
  public synchronized boolean contains(int val) {
    for(int i = 0; i < size; i++)
      if(array[i] == val) return true;
    return false;
  }
}
```

`add()` 和 `contains()` 方法是线程同步的，以防止线程冲突。
The add() and contains() methods are synchronized to prevent thread collisions.

**SerialNumberChecker** 类包含一个存储最近序列号的 **CircularSet** 变量，以及一个填充数值给 **CircularSet**  和确保它里面的序列号是唯一的 `run()` 方法。

```java
// lowlevel/SerialNumberChecker.java
// Test SerialNumbers implementations for thread-safety
import java.util.concurrent.*;
import onjava.Nap;

public class SerialNumberChecker implements Runnable {
  private CircularSet serials = new CircularSet(1000);
  private SerialNumbers producer;
  public SerialNumberChecker(SerialNumbers producer) {
    this.producer = producer;
  }
  @Override
  public void run() {
    while(true) {
      int serial = producer.nextSerialNumber();
      if(serials.contains(serial)) {
        System.out.println("Duplicate: " + serial);
        System.exit(0);
      }
      serials.add(serial);
    }
  }
  static void test(SerialNumbers producer) {
    for(int i = 0; i < 10; i++)
      CompletableFuture.runAsync(
        new SerialNumberChecker(producer));
    new Nap(4, "No duplicates detected");
  }
}
```

`test()` 方法创建多个任务来竞争单独的 **SerialNumbers** 对象。这时参于竞争的的 SerialNumberChecker 任务们就会试图生成重复的序列号（这情况在具有更多内核处理器的机器上发生得更快）。

当我们测试基本的 **SerialNumbers** 类，它会失败（产生重复序列号）：

```java
// lowlevel/SerialNumberTest.java

public class SerialNumberTest {
  public static void main(String[] args) {
    SerialNumberChecker.test(new SerialNumbers());
  }
}
/* Output:
Duplicate: 148044
*/
```

**volatile** 在这里没有帮助。要解决这个问题，将 **synchronized** 关键字添加到 `nextSerialNumber()` 方法 :

```java
// lowlevel/SynchronizedSerialNumbers.java

public class
SynchronizedSerialNumbers extends SerialNumbers {
  private int serialNumber = 0;
  public synchronized int nextSerialNumber() {
    return serialNumber++;
  }
  public static void main(String[] args) {
    SerialNumberChecker.test(
      new SynchronizedSerialNumbers());
  }
}
/* Output:
No duplicates detected
*/
```

**volatile** 不再是必需的，因为 **synchronized** 关键字保证了 volatile （易变性） 的特性。

读取和赋值原语应该是安全的原子操作。然后，正如在 **UnsafeReturn.java** 中所看到，**使用原子操作访问处于不稳定中间状态的对象仍然很容易。**对这个问题做出假设既棘手又危险。最明智的做法就是遵循 Brian 的同步规则**(如果可以，首先不要共享变量)。**

### 原子类

Java 5 引入了专用的原子变量类，例如 **AtomicInteger**、**AtomicLong**、**AtomicReference** 等。这些提供了原子性升级。这些快速、无锁的操作，它们是利用了现代处理器上可用的机器级原子性。

下面，我们可以使用 **atomicinteger** 重写 **unsafereturn.java** 示例：

```java
// lowlevel/AtomicIntegerTest.java
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.*;
import onjava.*;

public class AtomicIntegerTest extends IntTestable {
  private AtomicInteger i = new AtomicInteger(0);
  public int getAsInt() { return i.get(); }
  public void evenIncrement() { i.addAndGet(2); }
  public static void main(String[] args) {
    Atomicity.test(new AtomicIntegerTest());
  }
}
/* Output:
No failures found
*/
```

现在，我们通过使用 **AtomicInteger** 来消除了 **synchronized** 关键字。

下面使用 **AtomicInteger** 来重写 **SynchronizedEvenProducer.java** 示例：

```java
// lowlevel/AtomicEvenProducer.java
// Atomic classes: occasionally useful in regular code
import java.util.concurrent.atomic.*;

public class AtomicEvenProducer extends IntGenerator {
  private AtomicInteger currentEvenValue =
    new AtomicInteger(0);
  @Override
  public int next() {
    return currentEvenValue.addAndGet(2);
  }
  public static void main(String[] args) {
    EvenChecker.test(new AtomicEvenProducer());
  }
}
/* Output:
No odd numbers discovered
*/
```

再次，使用 **AtomicInteger** 消除了对所有其他同步方式的需要。

下面是一个使用 **AtomicInteger** 实现 **SerialNumbers** 的例子:

```java
// lowlevel/AtomicSerialNumbers.java
import java.util.concurrent.atomic.*;

public class
AtomicSerialNumbers extends SerialNumbers {
  private AtomicInteger serialNumber =
    new AtomicInteger();
  public int nextSerialNumber() {
    return serialNumber.getAndIncrement();
  }
  public static void main(String[] args) {
    SerialNumberChecker.test(
      new AtomicSerialNumbers());
  }
}
/* Output:
No duplicates detected
*/
```

这些都是对单一字段的简单示例； 当你创建更复杂的类时，你必须确定哪些字段需要保护，**在某些情况下，你可能仍然最**后在方法上使用 **synchronized** 关键字。

<!-- Critical Sections -->

## 临界区

有时，你只是想**防止多线程访问方法中的部分代码**，而**不是整个方法。**要**隔离的代码部分**称为**临界区**，它使用我们用于保护整个方法相同的 **synchronized** 关键字创建，但使用不同的语法。语法如下， **synchronized** 指定某个对象作为锁用于同步控制花括号内的代码：

```java
synchronized(syncObject) {
  // This code can be accessed
  // by only one task at a time
}
```

这也被称为 ***同步控制块* （synchronized block）；**在进入此段代码前，必须得到 **syncObject** 对象的锁。如果一些其他任务已经得到这个锁，那么就得等到锁被释放以后，才能进入临界区。当发生这种情况时，尝试获取该锁的任务就会挂起。线程调度会定期回来并检查锁是否已经释放；如果释放了锁则唤醒任务。

使用同步控制块而不是同步控制整个方法的**主要动机是性能**（有时，算法确实聪明，但还是要特别警惕来自并发性问题上的聪明）。下面的示例演示了同步控制代码块而不是整个方法可以使方法更容易被其他任务访问。该示例会统计成功访问 `method()` 的计数并且发起一些任务来尝试竞争调用 `method()` 方法。

```java
// lowlevel/SynchronizedComparison.java
// speeds up access.
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import onjava.Nap;

abstract class Guarded {
  AtomicLong callCount = new AtomicLong();
  public abstract void method();
  @Override
  public String toString() {
    return getClass().getSimpleName() +
      ": " + callCount.get();
  }
}

class SynchronizedMethod extends Guarded {
  public synchronized void method() {
    new Nap(0.01);
    callCount.incrementAndGet();
  }
}

class CriticalSection extends Guarded {
  public void method() {
    new Nap(0.01);
    synchronized(this) {
      callCount.incrementAndGet();
    }
  }
}

class Caller implements Runnable {
  private Guarded g;
  Caller(Guarded g) { this.g = g; }
  private AtomicLong successfulCalls =
    new AtomicLong();
  private AtomicBoolean stop =
    new AtomicBoolean(false);
  @Override
  public void run() {
    new Timer().schedule(new TimerTask() {
      public void run() { stop.set(true); }
    }, 2500);
    while(!stop.get()) {
      g.method();
      successfulCalls.getAndIncrement();
    }
    System.out.println(
      "-> " + successfulCalls.get());
  }
}

public class SynchronizedComparison {
  static void test(Guarded g) {
    List<CompletableFuture<Void>> callers =
      Stream.of(
        new Caller(g),
        new Caller(g),
        new Caller(g),
        new Caller(g))
        .map(CompletableFuture::runAsync)
        .collect(Collectors.toList());
    callers.forEach(CompletableFuture::join);
    System.out.println(g);
  }
  public static void main(String[] args) {
    test(new CriticalSection());
    test(new SynchronizedMethod());
  }
}
/* Output:
-> 243
-> 243
-> 243
-> 243
CriticalSection: 972
-> 69
-> 61
-> 83
-> 36
SynchronizedMethod: 249
*/
```

**Guarded** 类负责跟踪 **callCount** 中成功调用 `method()`  的次数。**SynchronizedMethod** 的方式是同步控制整个 `method` 方法，而 **CriticalSection** 的方式是使用同步控制块来仅同步 `method` 方法的一部分代码。这样，耗时的 **Nap** 对象可以被排除到同步控制块外。输出会显示 **CriticalSection** 中可用的 `method()` 有多少。

请记住，使用同步控制块是有风险；它要求**你确切知道同步控制块外的非同步代码是实际上要线程安全的。**

**Caller** 是尝试在给定的时间周期内尽可能多地调用 `method()` 方法（并报告调用次数）的任务。为了构建这个时间周期，我们会使用虽然有点过时但仍然可以很好地工作的 **java.util.Timer** 类。此类接收一个 **TimerTask** 参数, 但该参数并不是函数式接口，所以我们不能使用 **lambda** 表达式，必须显式创建该类对象（在这种情况下，使用匿名内部类）。当超时的时候，定时对象将设置 **AtomicBoolean** 类型的 **stop** 字段为 true ，这样循环就会退出。

`test()` 方法接收一个 **Guarded** 类对象并创建四个 **Caller** 任务。所有这些任务都添加到同一个 **Guarded** 对象上，因此它们竞争来获取使用 `method()` 方法的锁。

你通常会看到从一次运行到下一次运行的输出变化。结果表明， **CriticalSection** 方式比起 **SynchronizedMethod** 方式允许更多地访问 `method()` 方法。这通常是使用 **synchronized** 块取代同步控制整个方法的原因：允许其他任务更多访问(只要这样做是线程安全的)。

### 在其他对象上同步

**synchronized** 块必须给定一个在其上进行同步的对象。并且最**合理的方式是，使用其方法正在被调用的当前对象**： **synchronized(this)**，这正是前面示例中 **CriticalSection** 采取的方式。在这种方式中，当 **synchronized** 块获得锁的时候，那么该对象其他的 **synchronized** 方法和临界区就不能被调用了。因此，在进行同步时，临**界区的作用是减小同步的范围。**

有时必须在另一个对象上同步，但是如果你要这样做，就必须确保所有相关的任务都是在同一个任务上同步的。下面的示例演示了当对象中的方法在不同的锁上同步时，两个任务可以同时进入同一对象：

```java
// lowlevel/SyncOnObject.java
// Synchronizing on another object
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import onjava.Nap;

class DualSynch {
  ConcurrentLinkedQueue<String> trace =
    new ConcurrentLinkedQueue<>();
  public synchronized void f(boolean nap) {
    for(int i = 0; i < 5; i++) {
      trace.add(String.format("f() " + i));
      if(nap) new Nap(0.01);
    }
  }
  private Object syncObject = new Object();
  public void g(boolean nap) {
    synchronized(syncObject) {
      for(int i = 0; i < 5; i++) {
        trace.add(String.format("g() " + i));
        if(nap) new Nap(0.01);
      }
    }
  }
}

public class SyncOnObject {
  static void test(boolean fNap, boolean gNap) {
    DualSynch ds = new DualSynch();
    List<CompletableFuture<Void>> cfs =
      Arrays.stream(new Runnable[] {
        () -> ds.f(fNap), () -> ds.g(gNap) })
        .map(CompletableFuture::runAsync)
        .collect(Collectors.toList());
    cfs.forEach(CompletableFuture::join);
    ds.trace.forEach(System.out::println);
  }
  public static void main(String[] args) {
    test(true, false);
    System.out.println("****");
    test(false, true);
  }
}
/* Output:
f() 0
g() 0
g() 1
g() 2
g() 3
g() 4
f() 1
f() 2
f() 3
f() 4
****
f() 0
g() 0
f() 1
f() 2
f() 3
f() 4
g() 1
g() 2
g() 3
g() 4
*/
```

`DualSync.f()` 方法（通过同步整个方法）在 **this** 上同步，而 `g()` 方法有一个在 **syncObject** 上同步的 **synchronized** 块。因此，这两个同步是互相独立的。在 `test()` 方法中运行的两个调用 `f()` 和 `g()` 方法的独立任务演示了这一点。**fNap** 和 **gNap** 标志变量分别指示 `f()` 和 `g()` 是否应该在其 **for** 循环中调用 `Nap()` 方法。例如，当 f() 线程休眠时 ，该线程继续持有它的锁，但是你可以看到这并不阻止调用 `g()` ，反之亦然。

### 使用显式锁对象

**java.util.concurrent** 库包含在 **java.util.concurrent.locks** 中定义的显示互斥锁机制。 ==必须显式地创建，锁定和解锁 **Lock** 对象==，因此它产出的代码没有内置 **synchronized** 关键字那么优雅。然而，它在解决某些类型的问题时更加灵活。下面是使用显式 **Lock** 对象重写 **SynchronizedEvenProducer.java** 代码：

```java
// lowlevel/MutexEvenProducer.java
// Preventing thread collisions with mutexes
import java.util.concurrent.locks.*;
import onjava.Nap;

public class MutexEvenProducer extends IntGenerator {
  private int currentEvenValue = 0;
  private Lock lock = new ReentrantLock();
  @Override
  public int next() {
    lock.lock();
    try {
      ++currentEvenValue;
      new Nap(0.01); // Cause failure faster
      ++currentEvenValue;
      return currentEvenValue;
    } finally {
      lock.unlock();
    }
  }
  public static void main(String[] args) {
    EvenChecker.test(new MutexEvenProducer());
  }
}
/*
No odd numbers discovered
*/
```

**MutexEvenProducer** 添加一个名为 **lock** 的互斥锁并在 `next()` 中使用 `lock()` 和 `unlock()` 方法创建一个临界区。当你使用 **Lock** 对象时，==使用下面显示的习惯用法很重要：在调用 `Lock()` 之后，你必须放置 **try-finally** 语句，该语句在 **finally** 子句中带有 `unlock()` 方法 - 这是**确保锁总是被释放的惟一方法**==。注意，==**return** 语句必须出现在 **try** 子句中==，以确保 **unlock()** 不会过早发生并将数据暴露给第二个任务。

尽管 **try-finally** 比起使用 **synchronized** 关键字需要用得更多代码，但它也代表了显式锁对象的优势之一。==如果使用 **synchronized** 关键字失败，就会抛出异常，但是你没有机会进行任何清理以保持系统处于良好状态。而使用显式锁对象，可以使用 **finally** 子句在系统中维护适当的状态。==

一般来说，当你使用 **synchronized** 的时候，需要编写的代码更少，并且用户出错的机会也大大减少，因此**通常只在解决特殊问题时使用显式锁对象**。例如，使用 **synchronized** 关键字，你不能尝试获得锁并让其失败，或者你在一段时间内尝试获得锁，然后放弃 - 为此，你必须使用这个并发库。

```java
// lowlevel/AttemptLocking.java
// Locks in the concurrent library allow you
// to give up on trying to acquire a lock
import java.util.concurrent.*;
import java.util.concurrent.locks.*;
import onjava.Nap;

public class AttemptLocking {
  private ReentrantLock lock = new ReentrantLock();
  public void untimed() {
    boolean captured = lock.tryLock();
    try {
      System.out.println("tryLock(): " + captured);
    } finally {
      if(captured)
        lock.unlock();
    }
  }
  public void timed() {
    boolean captured = false;
    try {
      captured = lock.tryLock(2, TimeUnit.SECONDS);
    } catch(InterruptedException e) {
      throw new RuntimeException(e);
    }
    try {
      System.out.println(
        "tryLock(2, TimeUnit.SECONDS): " + captured);
    } finally {
      if(captured)
        lock.unlock();
    }
  }
  public static void main(String[] args) {
    final AttemptLocking al = new AttemptLocking();
    al.untimed(); // True -- lock is available
    al.timed();   // True -- lock is available
    // Now create a second task to grab the lock:
    CompletableFuture.runAsync( () -> {
        al.lock.lock();
        System.out.println("acquired");
    });
    new Nap(0.1);  // Give the second task a chance
    al.untimed(); // False -- lock grabbed by task
    al.timed();   // False -- lock grabbed by task
  }
}
/* Output:
tryLock(): true
tryLock(2, TimeUnit.SECONDS): true
acquired
tryLock(): false
tryLock(2, TimeUnit.SECONDS): false
*/
```

**ReentrantLock** 可以尝试或者放弃获取锁，因此如果某些任务已经拥有锁，**你可以决定放弃并执行其他操作，而不是一直等到锁释放**，就像 `untimed()` 方法那样。而在 `timed()` 方法中，则尝试获取可能在 2 秒后没成功而放弃的锁。在 `main()` 方法中，一个单独的线程被匿名类所创建，并且它会获得锁，因此让 `untimed()` 和 `timed() ` 方法有东西可以去竞争。

显式锁比起内置同步锁提供**更细粒度的加锁和解锁控制**。这对于实现专门的同步并发结构，比如用于遍历链表节点的 *交替锁* ( *hand-over-hand locking* ) ，也称为 *锁耦合* （ *lock coupling* ）- 该**遍历代码要求必须在当前节点的解锁之前捕获下一个节点的锁。**

<!-- Library Components -->

## 库组件

**java.util.concurrent** 库提供大量旨在解决并发问题的类，可以帮助你生成更简单，更鲁棒的并发程序。但请注意，这些工具是比起并行流和 **CompletableFuture** 更底层的机制。

在本节中，我们将看一些使用不同组件的示例，然后讨论一下 *lock-free*（无锁） 库组件是如何工作的。

### DelayQueue

这是一个无界阻塞队列 （ **BlockingQueue** ），用于放置实现了 **Delayed** 接口的对象，其中的对象只能在其到期时才能从队列中取走。这种队列是有序的，因此队首对象的延迟到期的时间最长。如果没有任何延迟到期，那么就不会有队首元素，并且 `poll()` 将返回 **null**（正因为这样，你不能将 **null** 放置到这种队列中）。

下面是一个示例，其中的 **Delayed** 对象自身就是任务，而 **DelayedTaskConsumer** 将**最“紧急”的任务（到期时间最长的任务）**从队列中取出，然后运行它。注意的是这样 **DelayQueue** 就成为了优先级队列的一种变体。

```java
// lowlevel/DelayQueueDemo.java
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import static java.util.concurrent.TimeUnit.*;

class DelayedTask implements Runnable, Delayed {
  private static int counter = 0;
  private final int id = counter++;
  private final int delta;
  private final long trigger;
  protected static List<DelayedTask> sequence =
    new ArrayList<>();
  DelayedTask(int delayInMilliseconds) {
    delta = delayInMilliseconds;
    trigger = System.nanoTime() +
      NANOSECONDS.convert(delta, MILLISECONDS);
    sequence.add(this);
  }
  @Override
  public long getDelay(TimeUnit unit) {
    return unit.convert(
      trigger - System.nanoTime(), NANOSECONDS);
  }
  @Override
  public int compareTo(Delayed arg) {
    DelayedTask that = (DelayedTask)arg;
    if(trigger < that.trigger) return -1;
    if(trigger > that.trigger) return 1;
    return 0;
  }
  @Override
  public void run() {
    System.out.print(this + " ");
  }
  @Override
  public String toString() {
    return
      String.format("[%d] Task %d", delta, id);
  }
  public String summary() {
    return String.format("(%d:%d)", id, delta);
  }
  public static class EndTask extends DelayedTask {
    EndTask(int delay) { super(delay); }
    @Override
    public void run() {
      sequence.forEach(dt ->
        System.out.println(dt.summary()));
    }
  }
}

public class DelayQueueDemo {
  public static void
  main(String[] args) throws Exception {
    DelayQueue<DelayedTask> tasks =
      Stream.concat( // Random delays:
        new Random(47).ints(20, 0, 4000)
          .mapToObj(DelayedTask::new),
        // Add the summarizing task:
        Stream.of(new DelayedTask.EndTask(4000)))
      .collect(Collectors
        .toCollection(DelayQueue::new));
    while(tasks.size() > 0)
      tasks.take().run();
  }
}
/* Output:
[128] Task 12 [429] Task 6 [551] Task 13 [555] Task 2
[693] Task 3 [809] Task 15 [961] Task 5 [1258] Task 1
[1258] Task 20 [1520] Task 19 [1861] Task 4 [1998] Task
17 [2200] Task 8 [2207] Task 10 [2288] Task 11 [2522]
Task 9 [2589] Task 14 [2861] Task 18 [2868] Task 7
[3278] Task 16 (0:4000)
(1:1258)
(2:555)
(3:693)
(4:1861)
(5:961)
(6:429)
(7:2868)
(8:2200)
(9:2522)
(10:2207)
(11:2288)
(12:128)
(13:551)
(14:2589)
(15:809)
(16:3278)
(17:1998)
(18:2861)
(19:1520)
(20:1258)
*/
```

**DelayedTask** 包含一个称为 **sequence** 的 **List&lt;DelayedTask&gt;** ，它<u>保存了任务被创建的顺序</u>，因此我们可以看到排序是按照实际发生的顺序执行的。

**Delay** 接口有一个方法， `getDelay()` ， 该方法<u>用来告知延迟到期有多长时间，或者延迟在多长时间之前已经到期了</u>。这个方法强制我们去使用 **TimeUnit** 类，因为这就是参数类型。这会产生一个非常方便的类，因为你可以很容易地转换单位而无需作任何声明。例如，**delta** 的值是以毫秒为单位存储的，但是 `System.nanoTime()` 产生的时间则是以纳秒为单位的。你可以转换 **delta** 的值，方法是声明它的单位以及你希望以什么单位来表示，就像下面这样：

```java
NANOSECONDS.convert(delta, MILLISECONDS);
```

在 `getDelay()` 中， 所希望的单位是作为 **unit** 参数传递进来的，你使用它将当前时间与触发时间之间的差转换为调用者要求的单位，而无需知道这些单位是什么（这是<u>*策略*设计模式</u>的一个简单示例，在这种模式中，算法的一部分是作为参数传递进来的）。

为了排序， **Delayed** 接口还继承了 **Comparable** 接口，因此必须实现 `compareTo()` , 使其可以产生合理的比较。

从输出中可以看到，任务创建的顺序对执行顺序没有任何影响 - 相反**，任务是按照所期望的延迟顺序所执行的。****

### PriorityBlockingQueue

这是一个很基础的优先级队列，它具有可阻塞的读取操作。在下面的示例中， **Prioritized** 对象会被赋予优先级编号。几个 **Producer** 任务的实例会插入 **Prioritized** 对象到 **PriorityBlockingQueue** 中，但插入之间会有随机延时。然后，单个 **Consumer** 任务在执行 `take()` 时会显示多个选项，**PriorityBlockingQueue** 会<u>将当前具有最高优先级的 **Prioritized** 对象</u>提供给它。

在 **Prioritized** 中的静态变量 **counter** 是 **AtomicInteger** 类型。这是必要的，因为有多个 **Producer** 并行运行；如果不是 **AtomicInteger** 类型，你将会看到重复的 **id** 号。 这个问题在 [并发编程](./24-Concurrent-Programming.md) 的 [构造函数非线程安全](./24-Concurrent-Programming.md) 一节中讨论过。

```java
// lowlevel/PriorityBlockingQueueDemo.java
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import onjava.Nap;

class Prioritized implements Comparable<Prioritized>  {
  private static AtomicInteger counter =
    new AtomicInteger();
  private final int id = counter.getAndIncrement();
  private final int priority;
  private static List<Prioritized> sequence =
    new CopyOnWriteArrayList<>();
  Prioritized(int priority) {
    this.priority = priority;
    sequence.add(this);
  }
  @Override
  public int compareTo(Prioritized arg) {
    return priority < arg.priority ? 1 :
      (priority > arg.priority ? -1 : 0);
  }
  @Override
  public String toString() {
    return String.format(
      "[%d] Prioritized %d", priority, id);
  }
  public void displaySequence() {
    int count = 0;
    for(Prioritized pt : sequence) {
      System.out.printf("(%d:%d)", pt.id, pt.priority);
      if(++count % 5 == 0)
        System.out.println();
    }
  }
  public static class EndSentinel extends Prioritized {
    EndSentinel() { super(-1); }
  }
}

class Producer implements Runnable {
  private static AtomicInteger seed =
    new AtomicInteger(47);
  private SplittableRandom rand =
    new SplittableRandom(seed.getAndAdd(10));
  private Queue<Prioritized> queue;
  Producer(Queue<Prioritized> q) {
    queue = q;
  }
  @Override
  public void run() {
    rand.ints(10, 0, 20)
      .mapToObj(Prioritized::new)
      .peek(p -> new Nap(rand.nextDouble() / 10))
      .forEach(p -> queue.add(p));
    queue.add(new Prioritized.EndSentinel());
  }
}

class Consumer implements Runnable {
  private PriorityBlockingQueue<Prioritized> q;
  private SplittableRandom rand =
    new SplittableRandom(47);
  Consumer(PriorityBlockingQueue<Prioritized> q) {
    this.q = q;
  }
  @Override
  public void run() {
    while(true) {
      try {
        Prioritized pt = q.take();
        System.out.println(pt);
        if(pt instanceof Prioritized.EndSentinel) {
          pt.displaySequence();
          break;
        }
        new Nap(rand.nextDouble() / 10);
      } catch(InterruptedException e) {
        throw new RuntimeException(e);
      }
    }
  }
}

public class PriorityBlockingQueueDemo {
  public static void main(String[] args) {
    PriorityBlockingQueue<Prioritized> queue =
      new PriorityBlockingQueue<>();
    CompletableFuture.runAsync(new Producer(queue));
    CompletableFuture.runAsync(new Producer(queue));
    CompletableFuture.runAsync(new Producer(queue));
    CompletableFuture.runAsync(new Consumer(queue))
      .join();
  }
}
/* Output:
[15] Prioritized 2
[17] Prioritized 1
[17] Prioritized 5
[16] Prioritized 6
[14] Prioritized 9
[12] Prioritized 0
[11] Prioritized 4
[11] Prioritized 12
[13] Prioritized 13
[12] Prioritized 16
[14] Prioritized 18
[15] Prioritized 23
[18] Prioritized 26
[16] Prioritized 29
[12] Prioritized 17
[11] Prioritized 30
[11] Prioritized 24
[10] Prioritized 15
[10] Prioritized 22
[8] Prioritized 25
[8] Prioritized 11
[8] Prioritized 10
[6] Prioritized 31
[3] Prioritized 7
[2] Prioritized 20
[1] Prioritized 3
[0] Prioritized 19
[0] Prioritized 8
[0] Prioritized 14
[0] Prioritized 21
[-1] Prioritized 28
(0:12)(2:15)(1:17)(3:1)(4:11)
(5:17)(6:16)(7:3)(8:0)(9:14)
(10:8)(11:8)(12:11)(13:13)(14:0)
(15:10)(16:12)(17:12)(18:14)(19:0)
(20:2)(21:0)(22:10)(23:15)(24:11)
(25:8)(26:18)(27:-1)(28:-1)(29:16)
(30:11)(31:6)(32:-1)
*/
```

与前面的示例一样，**Prioritized** 对象的创建顺序在 **sequence** 的 **list** 对象上所记入，以便与实际执行顺序进行比较。 **EndSentinel** 是用于告知 **Consumer** 对象关闭的特殊类型。

**Producer** 使用 **AtomicInteger** 变量为 **SplittableRandom** 设置随机生成种子，以便不同的 **Producer** 生成不同的队列。 这是必需的，因为多个生产者并行创建，如果不是这样，创建过程并不会是线程安全的。

<u>**Producer** 和 **Consumer** 通过 **PriorityBlockingQueue** 相互连接</u>。因为阻塞队列的性质提供了所有必要的同步，因为阻塞队列的性质提供了所有必要的同步，请注意，显式同步是并不需要的 — 从队列中读取数据时，你不用考虑队列中是否有任何元素，因为队列在没有元素时将阻塞读取。

### 无锁集合

[集合](./12-Collections.md) 章节强调集合是基本的编程工具，这也要求包含并发性。因此，早期的集合比如 **Vector** 和 **Hashtable** 有许多使用 **synchronized** 机制的方法。当这些集合不是在多线程应用中使用时，这就导致了不可接受的开销。在 Java 1.2 版本中，新的集合库是非同步的，而给 **Collection** 类赋予了各种 **static** **synchronized** 修饰的方法来同步不同的集合类型。虽然这是一个改进，因为它让你可以选择是否对集合使用同步，但是开销仍然基于同步锁定。 Java 5 版本添加新的集合类型，专门用于增加线程安全性能，使用巧妙的技术来消除锁定。

无锁集合有一个有趣的特性：只要读取者仅能看到已完成修改的结果，对集合的修改就可以同时发生在读取发生时。这是通过一些策略实现的。为了让你了解它们是如何工作的，我们来看看其中的一些。

#### 复制策略

使用“复制”策略，修改是在数据结构一部分的单独副本（或有时是整个数据的副本）上进行的，并且在整个修改过程期间这个副本是不可见的。仅当修改完成时，修改后的结构才与“主”数据结构安全地交换，然后读取者才会看到修改。

在 **CopyOnWriteArrayList** ，写入操作会复制整个底层数组。保留原来的数组，以便在修改复制的数组时可以线程安全地进行读取。当修改完成后，原子操作会将其交换到新数组中，以便新的读取操作能够看到新数组内容。 **CopyOnWriteArrayList** 的其中一个好处是，当多个迭代器遍历和修改列表时，它不会抛出 **ConcurrentModificationException** 异常，因此你不用就像过去必须做的那样，编写特殊的代码来防止此类异常。

**CopyOnWriteArraySet** 使用 **CopyOnWriteArrayList** 来实现其无锁行为。

**ConcurrentHashMap** 和 **ConcurrentLinkedQueue** 使用类似的技术来允许并发读写，但是只复制和修改集合的一部分，而不是整个集合。然而，读取者仍然不会看到任何不完整的修改。**ConcurrentHashMap** **不会抛出concurrentmodificationexception** 异常。

#### 比较并交换 (CAS)

在 <u>比较并交换 (CAS)</u> 中，你从内存中获取一个值，并在计算新值时保留原始值。然后使用 CAS 指令，它将原始值与当前内存中的值进行比较，如果这两个值是相等的，则将内存中的旧值替换为计算新值的结果，所有操作都在一个原子操作中完成。如果原始值比较失败，则不会进行交换，因为这意味着另一个线程同时修改了内存。在这种情况下，你的代码必须再次尝试，<u>获取一个新的原始值并重复该操作。</u>

如果内存仅轻量竞争，CAS操作几乎总是在没有重复尝试的情况下完成，因此它非常快。相反，**synchronized** 操作需要考虑每次获取和释放锁的成本，这要昂贵得多，而且没有额外的好处。随着内存竞争的增加，使用 CAS 的操作会变慢，因为它必须更频繁地重复自己的操作，但这是对更多资源竞争的动态响应。这确实是一种优雅的方法。

最重要的是，许多现代处理器的汇编语言中都有一条 CAS 指令，并且也被 JVM 中的 CAS 操作(例如 **Atomic** 类中的操作)所使用。CAS 指令在硬件层面中是原子性的，并且与你所期望的操作一样快。

<!-- Summary -->

## 本章小结

本附录主要是为了让你在遇到底层并发代码时能对此有一定的了解，尽管本文还远没对这个主题进行全面的讨论。为此，你需要先从阅读由 Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, David Holmes, and Doug Lea (Addison-Wesley 出版社, 2006)所著作的 <u>*Java Concurrency in Practice* （国内译名：Java并发编程实战）</u>开始了解。理想情况下，这本书会完全吓跑你在 Java 中尝试去编写底层并发代码。如果没有，那么你几乎肯定患上了达克效应(DunningKruger Effect)，这是<u>一种认知偏差，“你知道的越少，对自己的能力就越有信心”。</u>请记住，当前的语言设计人员仍然在清理早期语言设计人员过于自信造成的混乱(例如，查看 Thread 类中有多少方法被弃用，而 <u>volatile 直到 Java 5 才正确工作)</u>。

以下是并发编程的步骤:

1. 不要使用它。想一些其他方法来使你写的程序变的更快。
2. 如果你必须使用它，请使用在 [并发编程](./24-Concurrent-Programming.md) - parallel Streams and CompletableFutures 中展示的现代高级工具。
3. <u>不要在任务间共享变量</u>，在任务之间必须传递的任何信息都应该使用 Java.util.concurrent 库中的并发数据结构。
4. 如果必须在任务之间共享变量，请使用 java.util.concurrent.atomic 里面其中一种类型，或在<u>任何直接或间接访问这些变量的方法上应用 synchronized</u>。 当你不这样做时，很容易被愚弄，以为你已经把所有东西都包括在内。 说真的，尝试使用步骤 3。
5. 如果步骤 4 产生的结果太慢，你可以尝试使用volatile 或其他技术来调整代码，但是如果你正在阅读本书并认为你已经准备好尝试这些方法，那么你就超出了你的深度。 返回步骤＃1。

通常可以只使用 java.util.concurrent 库组件来编写并发程序，完全避免来自应用 volatile 和 synchronized 的挑战。注意，我可以通过 [并发编程](./24-Concurrent-Programming.md)  中的示例来做到这一点。

[^1]: 在某些平台上，特别是 Windows ，默认值可能非常难以查明。你可以使用 -Xss 标志调整堆栈大小。

[^2]: 引自 Brian Goetz, Java Concurrency in Practice 一书的作者 , 该书由 Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, David Holmes, and Doug Lea 联合著作 (Addison-Wesley 出版社, 2006)。↩

[^3]: 请注意，在64位处理器上可能不会发生这种情况，从而消除了这个问题。

[^4]: 这个测试的推论是，“如果某人表示线程是容易并且简单的，请确保这个人没有对你的项目做出重要的决策。如果那个人已经做出，那么你就已经陷入麻烦之中了。”

[^5]: 这在即将产生的 C++ 的标准中得到了补救。

<!-- 分页 -->

# summary

**==避免竞争条件的最好方法是避免可变的共享状态==**。我们可以称之为**==自私的孩子原则：什么都不分享==**。

使用 **InterferingTask** ，最好==**删除副作用并返回任务结果**==。为此，我们创建 **Callable** 而不是 **Runnable** ：

<!-- Appendix: Low-Level Concurrency -->

## 附录:并发底层原理-Summary

Summary

**资源共享使用原则**，同步(synchronized,lock锁)>原子类>volatile

**- 使用原子操作访问处于不稳定中间状态的对象仍然很容易。**对这个问题做出假设既棘手又危险。最明智的做法就是遵循 Brian 的同步规则**(如果可以，首先不要共享变量)。**

- **java中自增操作不是原子操作**。如i++；
- 并发中，尽量使用返回结果的方法（函数式编程），而不是产生副作用的方法。

## 同步

### synchronized关键字：

1. 可以用于方法，会为该方法的对象加锁，当对象加锁后，只有等对象无锁后，才能调用synchronized方法。
2. synchronized代码块，使用synchronized(object){}为object对象加锁，加锁范围更小，并发力度越大，同时可以为不为当前this对象加锁。

## lock锁

 ==必须显式地创建，锁定和解锁 **Lock** 对象==

<!-- Sharing Resources -->

### 资源共享

重要的是要注意到**==自增操作自身需要多个步骤，==**并且在自增过程中任务可能会被线程机制挂起 - 也就是说==**，在 Java 中，自增不是原子性的操作**==。因此，**如果不保护任务，即使单纯的自增也不是线程安全的。**

**防止这种冲突的方法**就是**当资源被一个任务使用时，在其上加锁。**第一个访问某项资源的任务必须锁定这项资源，使其他任务在其被解锁之前，就无法访问它，而在其被解锁时候，另一个任务就可以锁定并使用它，以此类推。

Java 以提供关键字 **synchronized** 的形式，为**防止资源冲突提供了内置支持。**当任务希望执行被 **synchronized** 关键字保护的代码片段的时候，Java 编译器会生成代码以查看锁是否可用。如果可用，该任务获取锁，执行代码，然后释放锁。

共享资源一般是以对象形式存在的内存片段，但也可以是文件、I/O 端口，或者类似打印机的东西。要控制对共享资源的访问，得先把它包装进一个对象。然后把任何访问该资源的方法标记为 **synchronized** 。 如果一个任务在调用其中一个 **synchronized** 方法之内，那么在这个任务从该方法返回之前，其他所有要调用该对象的 **synchronized** 方法的任务都会被阻塞。

通常你会将字段设为 **private**，并仅通过方法访问这些字段。你可用通过使用 **synchronized** 关键字声明方法来防止资源冲突。如下所示：

```java
synchronized void f() { /* ... */ }
synchronized void g() { /* ... */ }
```

所有对象都**自动包含独立的锁（也称为 *monitor*，即监视器）**。当你调用对象上任何 **synchronized** 方法，**此对象将被加锁**，并且该对象上的的==其他 **synchronized** 方法==调用只有等到前一个方法执行完成并释放了锁之后才能被调用。如果一个任务对对象调用了 `f()` ，对于同一个对象而言，就只能等到 `f()` 调用结束并释放了锁之后，其他任务才能调用 `f()` 和 `g()`。所以，某个特定对象的所有 **synchronized** 方法**共享同一个锁**，这个锁可以防止多个任务同时写入对象内存。

在使用并发时，将字段设为 **private** 特别重要；否则，**synchronized** 关键字不能阻止其他任务直接访问字段，从而产生资源冲突。

一个线程可以获取对象的锁多次。如果一个方法调用在同一个对象上的第二个方法，而后者又在同一个对象上调用另一个方法，就会发生这种情况。 JVM 会跟踪对象被锁定的次数。如果对象已解锁，则其计数为 0 。当一个线程首次获得锁时，计数变为 1 。每次同一线程在同一对象上获取另一个锁时，计数就会自增。显然，**只有首先获得锁的线程才允许多次获取多个锁**。每当线程离开 **synchronized** 方法时，计数递减，直到计数变为 0 ，完全释放锁以给其他线程使用。**每个类也有一个锁**（作为该类的 **Class** 对象的一部分），因此 **synchronized** 静态方法可以在类范围的基础上彼此锁定，不让同时访问静态数据。

你应该什么时候使用同步呢？可以永远 *Brian* 的同步法则[^2]。

> 如果你正在写一个变量，它可能接下来被另一个线程读取，或者正在读取一个上一次已经被另一个线程写过的变量，那么你必须使用同步，并且，读写线程都必须用相同的监视器锁同步。

如果在你的类中有超过一个方法在处理临界数据，那么你必须同步所有相关方法。如果只同步其中一个方法，那么其他方法可以忽略对象锁，并且可以不受惩罚地调用。这是很重要的一点：**每个访问临界共享资源的方法都必须被同步，否则将不会正确地工作。**

<!-- The volatile Keyword -->

### volatile 关键字

如果你尝试使用 **volatile** ，你可能**更应该尝试让一个变量线程安全而不是引起同步的成本**。因为 **volatile** 使用起来非常微妙和棘手，所以**==我建议根本不要使用它;==**相反，请使用本附录后面介绍的 **java.util.concurrent.atomic** 里面类之一。它们**以比同步低得多的成本提供了完全的线程安全性。**



**volatile** 可能是 Java 中最微妙和最难用的关键字。幸运的是，在现代 Java 中，你几乎总能避免使用它，如果你确实看到它在代码中使用，你应该保持怀疑态度和怀疑 - 这很有可能代码是过时的，或者编写代码的人不清楚使用它在大体上（或两者都有）易变性（**volatile**） 或并发性的后果。

使用 **volatile** 有三个理由。

#### 字分裂

当你的 Java 数据类型足够大（在 Java 中 **long** 和 **double** 类型都是 64 位），写入变量的过程分两步进行，就会发生 ***Word tearing* （字分裂）情况**。 JVM 被允许**将64位数量的读写作为两个单独的32位操作执行**[^3]，这增加了在读写过程中发生上下文切换的可能性，因此其他任务会看到不正确的结果。这被称为 *Word tearing* （字分裂），因为你可能只看到其中一部分修改后的值。基本上，任务有时可以在第一步之后但在第二步之前读取变量，从而产生垃圾值（对于例如 **boolean** 或 **int** 类型的小变量是没有问题的；任何 **long** 或 **double** 类型则除外）。

在缺乏任何其他保护的情况下，用 **volatile** 修饰符定义一个 **long** 或 **double** 变量，可阻止字分裂情况。然而，如果使用 **synchronized** 或 **java.util.concurrent.atomic** 类之一保护这些变量，则 **volatile** 将被取代。此外，**volatile** 不会影响到增量操作并不是原子操作的事实。

#### 可见性

如果单个线程对变量写入而其他线程只读取它，你可以放弃该变量声明为 **volatile**。通常，如==果你有多个线程对变量写入，**volatile** 无法解决你的问题==，并且你必须使用 **synchronized** 来防止竞争条件。 这有一个特殊的例外：可以让多个线程对该变量写入，*只要它们不需要先读取它并使用该值创建新值来写入变量* 。如果这些多个线程在结果中使用旧值，则会出现竞争条件，因为其余一个线程之一可能会在你的线程进行计算时修改该变量。即使你开始做对了，想象一下在代码修改或维护过程中忘记和引入一个重大变化是多么容易，或者对于不理解问题的不同程序员来说是多么容易（这在 Java 中尤其成问题因为程序员倾向于严重依赖编译时检查来告诉他们，他们的代码是否正确）。

重要的是要理解原子性和可见性是两个不同的概念。在非 **volatile** 变量上的原子操作**是不能保证是否将其刷新到主内存。**

同步也会让主内存刷新，所以==如果一个变量完全由 **synchronized** 的方法或代码段(或者 **java.util.concurrent.atomic** 库里类型之一)所保护，则不需要让变量用 **volatile**。==

#### 重排与 *Happen-Before* 原则

只要结果不会改变程序表现，Java 可以通过重排指令来优化性能。然而，重排可能会影响本地处理器缓存与主内存交互的方式，从而产生细微的程序 bug 。直到 Java 5 才理解并解决了这个无法阻止重排的问题。现在，**volatile** 关键字可以阻止重排 **volatile** 变量周围的读写指令。这种重排规则称为 *happens before* 担保原则 。

这项原则保证在 **volatile** 变量读写之前发生的指令先于它们的读写之前发生。同样，任何跟随 **volatile** 变量之后读写的操作都保证发生在它们的读写之后。例如：

```java
// lowlevel/ReOrdering.java

public class ReOrdering implements Runnable {
  int one, two, three, four, five, six;
  volatile int volaTile;
  @Override
  public void run() {
    one = 1;
    two = 2;
    three = 3;
    volaTile = 92;
    int x = four;
    int y = five;
    int z = six;
  }
}
```

例子中 **one**，**two**，**three** 变量赋值操作就可以被重排，只要它们都发生在 **volatile** 变量写操作之前。同样，只要 **volatile** 变量写操作发生在所有语句之前， **x**，**y**，**z** 语句可以被重排。这种 **volatile** （易变性）操作通常**称为 *memory barrier* （内存屏障）**。 *happens before* 担保原则确保 **volatile** 变量的读写指令不能跨过内存屏障进行重排。

*happens before* 担保原则还有另一个作用：当线程向一个 **volatile** 变量写入时，在线程写入之前的其他所有变量（包括非 **volatile** 变量）也会刷新到主内存。当线程读取一个 **volatile** 变量时，它也会读取其他所有变量（包括非 **volatile** 变量）与 **volatile** 变量一起刷新到主内存。尽管这是一个重要的特性，它解决了 Java 5 版本之前出现的一些非常狡猾的 bug ，**但是你不应该依赖这项特性来“自动”使周围的变量变得易变性 （ volatile ）的** 。如果你希望变量是易变性 （ **volatile** ）的，那么维护代码的任何人都应该清楚这一点。

#### 什么时候使用 volatile

对于 Java 早期版本，编写一个证明需要 **volatile** 的示例并不难。如果你进行搜索，你可以找到这样的例子，但是如果你在 Java 8 中尝试这些例子，它们就不起作用了(我没有找到任何一个)。我努力写这样一个例子，但没什么用。这可能原因是 JVM 或者硬件，或两者都得到了改进。这种效果对现有的应该  **volatile** （易变性） 但不 **volatile** 的存储的程序是有益的；对于此类程序，失误发生的频率要低得多，而且问题更难追踪。

如果你尝试使用 **volatile** ，你可能**更应该尝试让一个变量线程安全而不是引起同步的成本**。因为 **volatile** 使用起来非常微妙和棘手，所以**==我建议根本不要使用它;==**相反，请使用本附录后面介绍的 **java.util.concurrent.atomic** 里面类之一。它们**以比同步低得多的成本提供了完全的线程安全性。**

如果你正在尝试调试其他人的并发代码，请首先查找使用 **volatile** 的代码并将其替换为**Atomic** 变量。除非你确定程序员对并发性有很高的理解，否则它们很可能会误用 **volatile** 。

<!-- Atomicity -->

## 原子性

在 Java 线程的讨论中，经常反复提交但不正确的知识是：“原子操作不需要同步”。 一个 *原子操作* 是**不能被线程调度机制中断的操作**；一旦操作开始，那么它一定可以在可能发生的“上下文切换”之前（切换到其他线程执行）执行完毕。依赖于原子性是很棘手且很危险的，如果你是一个并发编程专家，或者你得到了来自这样的专家的帮助，你才应该使用原子性来代替同步，如果你认为自己足够聪明可以应付这种玩火似的情况，那么请接受下面的测试：

> Goetz 测试：如果你可以编写用于现代微处理器的高性能 JVM ，那么就有资格考虑是否可以避免同步[^4] 。

了解原子性是很有用的，并且知道它与其他高级技术一起用于实现一些更加巧妙的  **java.util.concurrent** 库组件。 但是==**要坚决抵制自己依赖它的冲动。**==

原子性可以应用于除 **long** 和 **double** 之外的所有基本类型之上的 “简单操作”。对于读写和写入除 **long** 和 **double** 之外的基本类型变量这样的操作，可以保证它们作为不可分 (原子) 的操作执行。

因为原子操作不能被线程机制中断。专家程序员可以利用这个来编写无锁代码（*lock-free code*），这些代码不需要被同步。但即使这样也过于简单化了。**有时候，甚至看起来应该是安全的原子操作，实际上也可能不安全。**本书的读者通常不会通过前面提到的 Goetz 测试，因此也就不具备用原子操作来替换同步的能力。尝试着移除

### 原子类

Java 5 引入了专用的原子变量类，例如 **AtomicInteger**、**AtomicLong**、**AtomicReference** 等。这些提供了原子性升级。这些快速、无锁的操作，它们是利用了现代处理器上可用的机器级原子性。

<!-- Critical Sections -->

## 临界区

有时，你只是想**防止多线程访问方法中的部分代码**，而**不是整个方法。**要**隔离的代码部分**称为**临界区**，它使用我们用于保护整个方法相同的 **synchronized** 关键字创建，但使用不同的语法。语法如下， **synchronized** 指定某个对象作为锁用于同步控制花括号内的代码：

```java
synchronized(syncObject) {
  // This code can be accessed
  // by only one task at a time
}
```

这也被称为 ***同步控制块* （synchronized block）；**在进入此段代码前，必须得到 **syncObject** 对象的锁。如果一些其他任务已经得到这个锁，那么就得等到锁被释放以后，才能进入临界区。当发生这种情况时，尝试获取该锁的任务就会挂起。线程调度会定期回来并检查锁是否已经释放；如果释放了锁则唤醒任务。

使用同步控制块而不是同步控制整个方法的**主要动机是性能**（有时，算法确实聪明，但还是要特别警惕来自并发性问题上的聪明）。下面的示例演示了同步控制代码块而不是整个方法可以使方法更容易被其他任务访问。该示例会统计成功访问 `method()` 的计数并且发起一些任务来尝试竞争调用 `method()` 方法。

```java
// lowlevel/SynchronizedComparison.java
// speeds up access.
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import onjava.Nap;

abstract class Guarded {
  AtomicLong callCount = new AtomicLong();
  public abstract void method();
  @Override
  public String toString() {
    return getClass().getSimpleName() +
      ": " + callCount.get();
  }
}

class SynchronizedMethod extends Guarded {
  public synchronized void method() {
    new Nap(0.01);
    callCount.incrementAndGet();
  }
}

class CriticalSection extends Guarded {
  public void method() {
    new Nap(0.01);
    synchronized(this) {
      callCount.incrementAndGet();
    }
  }
}

class Caller implements Runnable {
  private Guarded g;
  Caller(Guarded g) { this.g = g; }
  private AtomicLong successfulCalls =
    new AtomicLong();
  private AtomicBoolean stop =
    new AtomicBoolean(false);
  @Override
  public void run() {
    new Timer().schedule(new TimerTask() {
      public void run() { stop.set(true); }
    }, 2500);
    while(!stop.get()) {
      g.method();
      successfulCalls.getAndIncrement();
    }
    System.out.println(
      "-> " + successfulCalls.get());
  }
}

public class SynchronizedComparison {
  static void test(Guarded g) {
    List<CompletableFuture<Void>> callers =
      Stream.of(
        new Caller(g),
        new Caller(g),
        new Caller(g),
        new Caller(g))
        .map(CompletableFuture::runAsync)
        .collect(Collectors.toList());
    callers.forEach(CompletableFuture::join);
    System.out.println(g);
  }
  public static void main(String[] args) {
    test(new CriticalSection());
    test(new SynchronizedMethod());
  }
}
/* Output:
-> 243
-> 243
-> 243
-> 243
CriticalSection: 972
-> 69
-> 61
-> 83
-> 36
SynchronizedMethod: 249
*/
```

**Guarded** 类负责跟踪 **callCount** 中成功调用 `method()`  的次数。**SynchronizedMethod** 的方式是同步控制整个 `method` 方法，而 **CriticalSection** 的方式是使用同步控制块来仅同步 `method` 方法的一部分代码。这样，耗时的 **Nap** 对象可以被排除到同步控制块外。输出会显示 **CriticalSection** 中可用的 `method()` 有多少。

请记住，使用同步控制块是有风险；它要求**你确切知道同步控制块外的非同步代码是实际上要线程安全的。**

**Caller** 是尝试在给定的时间周期内尽可能多地调用 `method()` 方法（并报告调用次数）的任务。为了构建这个时间周期，我们会使用虽然有点过时但仍然可以很好地工作的 **java.util.Timer** 类。此类接收一个 **TimerTask** 参数, 但该参数并不是函数式接口，所以我们不能使用 **lambda** 表达式，必须显式创建该类对象（在这种情况下，使用匿名内部类）。当超时的时候，定时对象将设置 **AtomicBoolean** 类型的 **stop** 字段为 true ，这样循环就会退出。

`test()` 方法接收一个 **Guarded** 类对象并创建四个 **Caller** 任务。所有这些任务都添加到同一个 **Guarded** 对象上，因此它们竞争来获取使用 `method()` 方法的锁。

你通常会看到从一次运行到下一次运行的输出变化。结果表明， **CriticalSection** 方式比起 **SynchronizedMethod** 方式允许更多地访问 `method()` 方法。这通常是使用 **synchronized** 块取代同步控制整个方法的原因：允许其他任务更多访问(只要这样做是线程安全的)。

### 在其他对象上同步

**synchronized** 块必须给定一个在其上进行同步的对象。并且最**合理的方式是，使用其方法正在被调用的当前对象**： **synchronized(this)**，这正是前面示例中 **CriticalSection** 采取的方式。在这种方式中，当 **synchronized** 块获得锁的时候，那么该对象其他的 **synchronized** 方法和临界区就不能被调用了。因此，在进行同步时，临**界区的作用是减小同步的范围。**

有时必须在另一个对象上同步，但是如果你要这样做，就必须确保所有相关的任务都是在同一个任务上同步的。下面的示例演示了当对象中的方法在不同的锁上同步时，两个任务可以同时进入同一对象：

```java
// lowlevel/SyncOnObject.java
// Synchronizing on another object
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
import onjava.Nap;

class DualSynch {
  ConcurrentLinkedQueue<String> trace =
    new ConcurrentLinkedQueue<>();
  public synchronized void f(boolean nap) {
    for(int i = 0; i < 5; i++) {
      trace.add(String.format("f() " + i));
      if(nap) new Nap(0.01);
    }
  }
  private Object syncObject = new Object();
  public void g(boolean nap) {
    synchronized(syncObject) {
      for(int i = 0; i < 5; i++) {
        trace.add(String.format("g() " + i));
        if(nap) new Nap(0.01);
      }
    }
  }
}

public class SyncOnObject {
  static void test(boolean fNap, boolean gNap) {
    DualSynch ds = new DualSynch();
    List<CompletableFuture<Void>> cfs =
      Arrays.stream(new Runnable[] {
        () -> ds.f(fNap), () -> ds.g(gNap) })
        .map(CompletableFuture::runAsync)
        .collect(Collectors.toList());
    cfs.forEach(CompletableFuture::join);
    ds.trace.forEach(System.out::println);
  }
  public static void main(String[] args) {
    test(true, false);
    System.out.println("****");
    test(false, true);
  }
}
/* Output:
f() 0
g() 0
g() 1
g() 2
g() 3
g() 4
f() 1
f() 2
f() 3
f() 4
****
f() 0
g() 0
f() 1
f() 2
f() 3
f() 4
g() 1
g() 2
g() 3
g() 4
*/
```

`DualSync.f()` 方法（通过同步整个方法）在 **this** 上同步，而 `g()` 方法有一个在 **syncObject** 上同步的 **synchronized** 块。因此，这两个同步是互相独立的。在 `test()` 方法中运行的两个调用 `f()` 和 `g()` 方法的独立任务演示了这一点。**fNap** 和 **gNap** 标志变量分别指示 `f()` 和 `g()` 是否应该在其 **for** 循环中调用 `Nap()` 方法。例如，当 f() 线程休眠时 ，该线程继续持有它的锁，但是你可以看到这并不阻止调用 `g()` ，反之亦然。

### 使用显式锁对象

**java.util.concurrent** 库包含在 **java.util.concurrent.locks** 中定义的显示互斥锁机制。 ==必须显式地创建，锁定和解锁 **Lock** 对象==，因此它产出的代码没有内置 **synchronized** 关键字那么优雅。然而，它在解决某些类型的问题时更加灵活。下面是使用显式 **Lock** 对象重写 **SynchronizedEvenProducer.java** 代码：

```java
// lowlevel/MutexEvenProducer.java
// Preventing thread collisions with mutexes
import java.util.concurrent.locks.*;
import onjava.Nap;

public class MutexEvenProducer extends IntGenerator {
  private int currentEvenValue = 0;
  private Lock lock = new ReentrantLock();
  @Override
  public int next() {
    lock.lock();
    try {
      ++currentEvenValue;
      new Nap(0.01); // Cause failure faster
      ++currentEvenValue;
      return currentEvenValue;
    } finally {
      lock.unlock();
    }
  }
  public static void main(String[] args) {
    EvenChecker.test(new MutexEvenProducer());
  }
}
/*
No odd numbers discovered
*/
```

**MutexEvenProducer** 添加一个名为 **lock** 的互斥锁并在 `next()` 中使用 `lock()` 和 `unlock()` 方法创建一个临界区。当你使用 **Lock** 对象时，==使用下面显示的习惯用法很重要：在调用 `Lock()` 之后，你必须放置 **try-finally** 语句，该语句在 **finally** 子句中带有 `unlock()` 方法 - 这是**确保锁总是被释放的惟一方法**==。注意，==**return** 语句必须出现在 **try** 子句中==，以确保 **unlock()** 不会过早发生并将数据暴露给第二个任务。

尽管 **try-finally** 比起使用 **synchronized** 关键字需要用得更多代码，但它也代表了显式锁对象的优势之一。==如果使用 **synchronized** 关键字失败，就会抛出异常，但是你没有机会进行任何清理以保持系统处于良好状态。而使用显式锁对象，可以使用 **finally** 子句在系统中维护适当的状态。==

一般来说，当你使用 **synchronized** 的时候，需要编写的代码更少，并且用户出错的机会也大大减少，因此**通常只在解决特殊问题时使用显式锁对象**。例如，使用 **synchronized** 关键字，你不能尝试获得锁并让其失败，或者你在一段时间内尝试获得锁，然后放弃 - 为此，你必须使用这个并发库。

```java
// lowlevel/AttemptLocking.java
// Locks in the concurrent library allow you
// to give up on trying to acquire a lock
import java.util.concurrent.*;
import java.util.concurrent.locks.*;
import onjava.Nap;

public class AttemptLocking {
  private ReentrantLock lock = new ReentrantLock();
  public void untimed() {
    boolean captured = lock.tryLock();
    try {
      System.out.println("tryLock(): " + captured);
    } finally {
      if(captured)
        lock.unlock();
    }
  }
  public void timed() {
    boolean captured = false;
    try {
      captured = lock.tryLock(2, TimeUnit.SECONDS);
    } catch(InterruptedException e) {
      throw new RuntimeException(e);
    }
    try {
      System.out.println(
        "tryLock(2, TimeUnit.SECONDS): " + captured);
    } finally {
      if(captured)
        lock.unlock();
    }
  }
  public static void main(String[] args) {
    final AttemptLocking al = new AttemptLocking();
    al.untimed(); // True -- lock is available
    al.timed();   // True -- lock is available
    // Now create a second task to grab the lock:
    CompletableFuture.runAsync( () -> {
        al.lock.lock();
        System.out.println("acquired");
    });
    new Nap(0.1);  // Give the second task a chance
    al.untimed(); // False -- lock grabbed by task
    al.timed();   // False -- lock grabbed by task
  }
}
/* Output:
tryLock(): true
tryLock(2, TimeUnit.SECONDS): true
acquired
tryLock(): false
tryLock(2, TimeUnit.SECONDS): false
*/
```

**ReentrantLock** 可以尝试或者放弃获取锁，因此如果某些任务已经拥有锁，**你可以决定放弃并执行其他操作，而不是一直等到锁释放**，就像 `untimed()` 方法那样。而在 `timed()` 方法中，则尝试获取可能在 2 秒后没成功而放弃的锁。在 `main()` 方法中，一个单独的线程被匿名类所创建，并且它会获得锁，因此让 `untimed()` 和 `timed() ` 方法有东西可以去竞争。

显式锁比起内置同步锁提供**更细粒度的加锁和解锁控制**。这对于实现专门的同步并发结构，比如用于遍历链表节点的 *交替锁* ( *hand-over-hand locking* ) ，也称为 *锁耦合* （ *lock coupling* ）- 该**遍历代码要求必须在当前节点的解锁之前捕获下一个节点的锁。**

<!-- Summary -->

## 本章小结

本附录主要是为了让你在遇到底层并发代码时能对此有一定的了解，尽管本文还远没对这个主题进行全面的讨论。为此，你需要先从阅读由 Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, David Holmes, and Doug Lea (Addison-Wesley 出版社, 2006)所著作的 <u>*Java Concurrency in Practice* （国内译名：Java并发编程实战）</u>开始了解。理想情况下，这本书会完全吓跑你在 Java 中尝试去编写底层并发代码。如果没有，那么你几乎肯定患上了达克效应(DunningKruger Effect)，这是<u>一种认知偏差，“你知道的越少，对自己的能力就越有信心”。</u>请记住，当前的语言设计人员仍然在清理早期语言设计人员过于自信造成的混乱(例如，查看 Thread 类中有多少方法被弃用，而 <u>volatile 直到 Java 5 才正确工作)</u>。

以下是并发编程的步骤:

1. 不要使用它。想一些其他方法来使你写的程序变的更快。
2. 如果你必须使用它，请使用在 [并发编程](./24-Concurrent-Programming.md) - parallel Streams and CompletableFutures 中展示的现代高级工具。
3. <u>不要在任务间共享变量</u>，在任务之间必须传递的任何信息都应该使用 Java.util.concurrent 库中的并发数据结构。
4. 如果必须在任务之间共享变量，请使用 java.util.concurrent.atomic 里面其中一种类型，或在<u>任何直接或间接访问这些变量的方法上应用 synchronized</u>。 当你不这样做时，很容易被愚弄，以为你已经把所有东西都包括在内。 说真的，尝试使用步骤 3。
5. 如果步骤 4 产生的结果太慢，你可以尝试使用volatile 或其他技术来调整代码，但是如果你正在阅读本书并认为你已经准备好尝试这些方法，那么你就超出了你的深度。 返回步骤＃1。

通常可以只使用 java.util.concurrent 库组件来编写并发程序，完全避免来自应用 volatile 和 synchronized 的挑战。注意，我可以通过 [并发编程](./24-Concurrent-Programming.md)  中的示例来做到这一点。

# issue

要进一步深入这个领域，你还**必须阅读Brian Goetz等人的Java Concurrency in Practice。**

另一个有价值的资源是 Bill Venner 的 **Inside the Java Virtual Machine**，它详细描述了 JVM 的最内部工作方式，包括线程。