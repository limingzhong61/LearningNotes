模式篇
同步模式之保护性暂停

1. 定义
即 Guarded Suspension，用在一个线程等待另一个线程的执行结果
要点
有一个结果需要从一个线程传递到另一个线程，让他们关联同一个 GuardedObject
如果有结果不断从一个线程到另一个线程那么可以使用消息队列（见生产者/消费者）
JDK 中，join 的实现、Future 的实现，采用的就是此模式
因为要等待另一方的结果，因此归类到同步模式
2. 实现
class GuardedObject {
private Object response;
private final Object lock = new Object();
public Object get() {
synchronized (lock) {
// 条件不满足则等待
while (response == null) {
try {
lock.wait();
} catch (InterruptedException e) {
e.printStackTrace();
}
}
return response;
}

## 同步模式之顺序控制

### 1固定运行顺序

比如，必须先 2 后 1 打印

#### 1.1 wait notify 版

```java
public class WaitNotify {
    // 用来同步的对象
    static Object obj = new Object();
    // t2 运行标记， 代表 t2 是否执行过
    static boolean t2runed = false;
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            synchronized (obj) {
                // 如果 t2 没有执行过
                while (!t2runed) {
                    try {
                        // t1 先等一会
                        obj.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
            System.out.println(1);
        });
        Thread t2 = new Thread(() -> {
            System.out.println(2);
            synchronized (obj) {
                // 修改运行标记
                t2runed = true;
                // 通知 obj 上等待的线程（可能有多个，因此需要用 notifyAll）
                obj.notifyAll();
            }
        });
        t1.start();
        t2.start();
    }
}
```

#### 1.2 Park Unpark 版

可以看到，实现上很麻烦：

- 首先，需要保证先 wait 再 notify，否则 wait 线程永远得不到唤醒。因此使用了『运行标记』来判断该不该
  wait
- 第二，如果有些干扰线程错误地 notify 了 wait 线程，条件不满足时还要重新等待，使用了 while 循环来解决此问题
- 最后，唤醒对象上的 wait 线程需要使用 notifyAll，因为『同步对象』上的等待线程可能不止一个
  可以使用 LockSupport 类的 park 和 unpark 来简化上面的题目：

```java
public class ParkUnPark {
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            try { Thread.sleep(1000); } catch (InterruptedException e) { }
            // 当没有『许可』时，当前线程暂停运行；有『许可』时，用掉这个『许可』，当前线程恢复运行
            LockSupport.park();
            System.out.println("1");
        });
        Thread t2 = new Thread(() -> {
            System.out.println("2");
            // 给线程 t1 发放『许可』（多次连续调用 unpark 只会发放一个『许可』）
            LockSupport.unpark(t1);
        });
        t1.start();
        t2.start();
    }
}
```

park 和 unpark 方法比较灵活，他俩谁先调用，谁后调用无所谓。并且是以线程为单位进行『暂停』和『恢复』，不需要『同步对象』和『运行标记』

### 2. 交替输出

线程 1 输出 a 5 次，线程 2 输出 b 5 次，线程 3 输出 c 5 次。现在要求输出 abcabcabcabcabc 怎么实现

#### 2.1 wait notify 版

```java
public class WaitNotify {
    public static void main(String[] args) {

        SyncWaitNotify syncWaitNotify = new SyncWaitNotify(1, 5);
        new Thread(() -> {
            syncWaitNotify.print(1, 2, "a");
        }).start();
        new Thread(() -> {
            syncWaitNotify.print(2, 3, "b");
        }).start();
        new Thread(() -> {
            syncWaitNotify.print(3, 1, "c");
        }).start();
    }
}
class SyncWaitNotify {
    private int flag;
    private int loopNumber;
    public SyncWaitNotify(int flag, int loopNumber) {
        this.flag = flag;
        this.loopNumber = loopNumber;
    }
    public void print(int waitFlag, int nextFlag, String str) {
        for (int i = 0; i < loopNumber; i++) {
            synchronized (this) {
                while (this.flag != waitFlag) {
                    try {
                        this.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                System.out.print(str);
                flag = nextFlag;
                this.notifyAll();
            }
        }
    }
}
```

#### 2.2 Lock 条件变量版

```java
@Slf4j
public class ConditionObject {
    public static void main(String[] args) throws InterruptedException {
        CountDownLatch countDownLatch = new CountDownLatch(3);
        AwaitSignal as = new AwaitSignal(5);
        Condition aWaitSet = as.newCondition();
        Condition bWaitSet = as.newCondition();
        Condition cWaitSet = as.newCondition();
        new Thread(() -> {
            as.print("a", aWaitSet, bWaitSet);
            countDownLatch.countDown();
        }).start();
        new Thread(() -> {
            as.print("b", bWaitSet, cWaitSet);
            countDownLatch.countDown();
        }).start();
        new Thread(() -> {
            as.print("c", cWaitSet, aWaitSet);
            countDownLatch.countDown();
        }).start();
        as.start(aWaitSet);
        countDownLatch.await();
    }
}
@Slf4j
class AwaitSignal extends ReentrantLock {
    public void start(Condition first) {
        this.lock();
        try {
            log.info("start");
            first.signal();
        } finally {
            this.unlock();
        }
    }
    public void print(String str, Condition current, Condition next) {
        for (int i = 0; i < loopNumber; i++) {
            this.lock();
            try {
                current.await();
                log.info(str);
                next.signal();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                this.unlock();
            }
        }
    }
    // 循环次数
    private int loopNumber;
    public AwaitSignal(int loopNumber) {
        this.loopNumber = loopNumber;
    }
}
```

注意：该实现没有考虑 a，b，c 线程都就绪再开始

#### 2.3 Park Unpark 版

```java
public class SyncPark {
    private int loopNumber;
    private Thread[] threads;
    
    public SyncPark(int loopNumber) {
        this.loopNumber = loopNumber;
    }
    public void setThreads(Thread... threads) {
        this.threads = threads;
    }
    public void print(String str) {
        for (int i = 0; i < loopNumber; i++) {
            LockSupport.park();
            System.out.print(str);
            LockSupport.unpark(nextThread());
        }
    }
    private Thread nextThread() {
        Thread current = Thread.currentThread();
        int index = 0;
        for (int i = 0; i < threads.length; i++) {
            if(threads[i] == current) {
                index = i;
                break;
            }
        }
        if(index < threads.length - 1) {
            return threads[index+1];
        } else {
            return threads[0];
        }
    }
    public void start() {
        for (Thread thread : threads) {
            thread.start();
        }
        LockSupport.unpark(threads[0]);
    }
    public static void main(String[] args) {
        SyncPark syncPark = new SyncPark(5);
        Thread t1 = new Thread(() -> {
            syncPark.print("a");
        });
        Thread t2 = new Thread(() -> {
            syncPark.print("b");
        });
        Thread t3 = new Thread(() -> {
            syncPark.print("c\n");
        });
        syncPark.setThreads(t1, t2, t3);
        syncPark.start();
    }

}
```



## 异步模式之生产者/消费者

### 定义

要点

- 与前面的保护性暂停中的 GuardObject 不同，不需要产生结果和消费结果的线程一一对应
- 消费队列可以用来平衡生产和消费的线程资源
- 生产者仅负责产生结果数据，不关心数据该如何处理，而消费者专心处理结果数据
- 消息队列是有容量限制的，满时不会再加入数据，空时不会再消耗数据
- JDK 中各种阻塞队列，采用的就是这种模式

![image-20230701204955539](img/img_java-concurrent-%E6%A8%A1%E5%BC%8F/image-20230701204955539.png)



### 异步模式之生产者/消费者实现√

#### synchronized

- 一个消费者
- 一个生成者
- 一个阻塞队列（核心）
  - 对内部队列设置一个容量，**对内部队列操作时都加上同一把锁**
  - 当条件不住wait()【生产者——队列慢了，消费者——队列为空】,
  - 当生产者生产notify(),消费者消费notify()
  - **使用循环判断**是否队列为空、或者不为空;防止虚假唤醒

```java
/**
 * 异步模式之生产者/消费者实现:
 *  使用synchronized 实现
 */
@Slf4j(topic = "MyProducerConsumer")
public class MyProducerConsumer {
    public static void main(String[] args) throws InterruptedException {
        int queueCapacity = 2,productCnt = 10;
        MyQueue<String> myQueue = new MyQueue<>(queueCapacity);
        CountDownLatch countDownLatch = new CountDownLatch(productCnt * 2);
        for (int i = 0; i < productCnt; i++) {
            int id = i;
            new Thread(() -> {
                log.debug("try put message[{}]", id);
                myQueue.put("product" + id);
                countDownLatch.countDown();
            }, "生产者" + i).start();
        }

        for (int i = 0; i < productCnt; i++) {
            int id = i;
            new Thread(() -> {
                String message = myQueue.take();
                log.debug("take message[{}]", message);
                countDownLatch.countDown();
            }, "消费者" + i).start();
        }

        countDownLatch.await();
    }
}


@Slf4j(topic = "MyQueue")
class MyQueue<T> {
    private LinkedList<T> queue;
    private int capacity;

    public MyQueue(int capacity) {
        this.capacity = capacity;
        queue = new LinkedList<>();
    }

    public T take() {
        synchronized (queue) {
            //使用循环判断是否队列为空、或者不为空;防止虚假唤醒
            while (queue.isEmpty()) {
                log.debug("queue.isEmpty, wait");
                try {
                    queue.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            T message = queue.removeFirst();
            queue.notifyAll();
            return message;
        }
    }

    public void put(T message) {
        synchronized (queue) {
            //使用循环判断是否队列为空、或者不为空;防止虚假唤醒
            while (queue.size() == capacity) {
                log.debug("queue.size() == capacity, wait");
                try {
                    queue.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            queue.addLast(message);
            queue.notifyAll();
        }
    }
}
```

#### ReentrantLock更好

- **注意：Condition 可以达到精确通知哪个线程要被唤醒的。很方便。而synchronized办不到精确通知的效果**。

```java
//定义资源类
@Slf4j(topic = "c")
class MyQueue {

    int num = 0;//共享资源：生产和消费product
    //队列中中实际存储的数据个数
    private int count = 0;
    //队列中中允许存放的资源数目
    private int capacity = 5;
    Queue<String> queue;

    MyQueue(int capacity) {
        this.capacity = capacity;
        queue = new LinkedList<>();
    }

    //创建可重入的非公平锁
    Lock lock = new ReentrantLock();
    //使用两个条件队列condition来实现精确通知
    Condition productCondition = lock.newCondition();
    Condition consumerCondition = lock.newCondition();

    //定义操作资源类的方法：生产方法
    public void product(String s) throws InterruptedException {
        lock.lock();//加锁
        try {
            //1.判断什么时候等待,并防止虚假唤醒
            if (queue.size() == capacity) {//当达到最大容量，则阻塞等待，生产者阻塞
                productCondition.await();
            }
            //2.干活
            queue.add(s);
            log.info(Thread.currentThread().getName() +
                    "\t 生产了一个商品：[{}]" + "，现在队列中剩余数据个数：{}",s,queue.size());
            //3.通知。生产者生产完立马通知消费者来消费
            consumerCondition.signal();//消费者条件队列被唤醒
        } finally {
            lock.unlock();//解锁
        }
    }

    //定义操作资源类的方法：生产方法
    public void consumer() throws InterruptedException {
        lock.lock();//加锁,同一把锁
        try {
            //1.判断什么时候等待,并防止虚假唤醒
            if (queue.size() == 0) {//没数据时，则阻塞等待，消费者阻塞
                consumerCondition.await();
            }
            //2.干活
            String product = queue.poll();
            log.info(Thread.currentThread().getName() +
                    "\t 消费了一个商品：[{}]，现在队列中剩余数据个数：{}",product, queue.size());
            //3.通知。消费者 消费完 立马通知生产者来生产
            productCondition.signal();//生产者条件队列被唤醒
        } finally {
            lock.unlock();//解锁
        }
    }
}

public class ProductAndConsumerTest2 {
    public static void main(String[] args) throws IOException, InterruptedException {
        CountDownLatch countDownLatch = new CountDownLatch(10);
        MyQueue myQueue = new MyQueue(5);
        //可以定义多个生产者和消费者，这里分别定义了一个
        for (int i = 0; i < 10; i++) {//10轮生产
            int id = i;
            new Thread(() -> {
                try {
                    myQueue.product("procuct" + id);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                countDownLatch.countDown();
            }, "生产者" + i).start();
        }


        for (int i = 0; i < 10; i++) {//10轮消费
            new Thread(() -> {
                try {
                    myQueue.consumer();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                countDownLatch.countDown();
            }, "消费者" + i).start();
        }


        countDownLatch.await();
    }
}
```

**注意：Condition 可以达到精确通知哪个线程要被唤醒的。很方便。而synchronized办不到精确通知的效果**。

```
22:23:08.228 c [生产者0] - 生产者0	 生产了一个商品：[procuct0]，现在队列中剩余数据个数：1
22:23:08.232 c [生产者1] - 生产者1	 生产了一个商品：[procuct1]，现在队列中剩余数据个数：2
22:23:08.232 c [生产者2] - 生产者2	 生产了一个商品：[procuct2]，现在队列中剩余数据个数：3
22:23:08.232 c [生产者3] - 生产者3	 生产了一个商品：[procuct3]，现在队列中剩余数据个数：4
22:23:08.232 c [生产者4] - 生产者4	 生产了一个商品：[procuct4]，现在队列中剩余数据个数：5
22:23:08.232 c [消费者0] - 消费者0	 消费了一个商品：[procuct0]，现在队列中剩余数据个数：4
22:23:08.232 c [消费者1] - 消费者1	 消费了一个商品：[procuct1]，现在队列中剩余数据个数：3
22:23:08.232 c [消费者2] - 消费者2	 消费了一个商品：[procuct2]，现在队列中剩余数据个数：2
22:23:08.232 c [消费者3] - 消费者3	 消费了一个商品：[procuct3]，现在队列中剩余数据个数：1
22:23:08.232 c [消费者4] - 消费者4	 消费了一个商品：[procuct4]，现在队列中剩余数据个数：0
22:23:08.232 c [生产者5] - 生产者5	 生产了一个商品：[procuct5]，现在队列中剩余数据个数：1
22:23:08.232 c [生产者6] - 生产者6	 生产了一个商品：[procuct6]，现在队列中剩余数据个数：2
22:23:08.233 c [生产者7] - 生产者7	 生产了一个商品：[procuct7]，现在队列中剩余数据个数：3
22:23:08.233 c [生产者9] - 生产者9	 生产了一个商品：[procuct9]，现在队列中剩余数据个数：4
22:23:08.233 c [生产者8] - 生产者8	 生产了一个商品：[procuct8]，现在队列中剩余数据个数：5
22:23:08.233 c [消费者5] - 消费者5	 消费了一个商品：[procuct5]，现在队列中剩余数据个数：4
22:23:08.233 c [消费者6] - 消费者6	 消费了一个商品：[procuct6]，现在队列中剩余数据个数：3
22:23:08.233 c [消费者7] - 消费者7	 消费了一个商品：[procuct7]，现在队列中剩余数据个数：2
22:23:08.233 c [消费者8] - 消费者8	 消费了一个商品：[procuct9]，现在队列中剩余数据个数：1
22:23:08.233 c [消费者9] - 消费者9	 消费了一个商品：[procuct8]，现在队列中剩余数据个数：0
```

## 线程安全单例

单例模式有很多实现方法，饿汉、懒汉、静态内部类、枚举类，试分析每种实现下获取单例对象（即调用 getInstance）时的线程安全，并思考注释中的问题

- 饿汉式：类加载就会导致该单实例对象被创建
- 懒汉式：类加载不会导致该单实例对象被创建，而是首次使用该对象时才会创建

### 1. 饿汉单例

```java
// 问题1：为什么加 final
// 问题2：如果实现了序列化接口, 还要做什么来防止反序列化破坏单例
public final class Singleton implements Serializable {
    // 问题3：为什么设置为私有? 是否能防止反射创建新的实例?
    private Singleton() {}
    // 问题4：这样初始化是否能保证单例对象创建时的线程安全?
    private static final Singleton INSTANCE = new Singleton();
    // 问题5：为什么提供静态方法而不是直接将 INSTANCE 设置为 public, 说出你知道的理由
    public static Singleton getInstance() {
        return INSTANCE;
    }
    public Object readResolve() {
        return INSTANCE;
    }
}
```

### 2. 枚举单例

```java
// 问题1：枚举单例是如何限制实例个数的
// 问题2：枚举单例在创建时是否有并发问题
// 问题3：枚举单例能否被反射破坏单例
// 问题4：枚举单例能否被反序列化破坏单例
// 问题5：枚举单例属于懒汉式还是饿汉式
// 问题6：枚举单例如果希望加入一些单例创建时的初始化逻辑该如何做
enum Singleton {
    INSTANCE;
}
```

### 3. 懒汉单例

```java
public final class Singleton {
    private Singleton() { }
    private static Singleton INSTANCE = null;
    // 分析这里的线程安全, 并说明有什么缺点
    public static synchronized Singleton getInstance() {
        if( INSTANCE != null ){
            return INSTANCE;
        }
        INSTANCE = new Singleton();
        return INSTANCE;
    }
}
```

### 4. DCL 懒汉单例

```java
public final class Singleton {
    private Singleton() { }
    // 问题1：解释为什么要加 volatile ?
    private static volatile Singleton INSTANCE = null;
    // 问题2：对比实现3, 说出这样做的意义
    public static Singleton getInstance() {
        if (INSTANCE != null) {
            return INSTANCE;
        }
        synchronized (Singleton.class) {
            // 问题3：为什么还要在这里加为空判断, 之前不是判断过了吗
            if (INSTANCE != null) { // t2
                return INSTANCE;
            }
            INSTANCE = new Singleton();
            return INSTANCE;
        }
    }
}
```

### 5. 静态内部类懒汉单例

```java
public final class Singleton {
    private Singleton() { }
    // 问题1：属于懒汉式还是饿汉式
    private static class LazyHolder {
        static final Singleton INSTANCE = new Singleton();
    }
    // 问题2：在创建时是否有并发问题
    public static Singleton getInstance() {
        return LazyHolder.INSTANCE;
    }
}
```



## Reference

详见 模式.pdf

- 代码地址：D:\Codes\java\learning-project\java-learning\java-concurrent