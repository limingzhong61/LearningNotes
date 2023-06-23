# Collection - fail-fast(快速失败)机制

## 引入

在JDK的Collection中我们时常会看到类似于这样的话：

例如，ArrayList:

> 注意，迭代器的快速失败行为无法得到保证，因为一般来说，不可能对是否出现不同步并发修改做出任何硬性保证。快速失败迭代器会尽最大努力抛出 ConcurrentModificationException。因此，为提高这类迭代器的正确性而编写一个依赖于此异常的程序是错误的做法：迭代器的快速失败行为应该仅用于检测 bug。

HashMap中：

> 注意，迭代器的快速失败行为不能得到保证，一般来说，存在非同步的并发修改时，不可能作出任何坚决的保证。快速失败迭代器尽最大努力抛出 ConcurrentModificationException。因此，编写依赖于此异常的程序的做法是错误的，正确做法是：迭代器的快速失败行为应该仅用于检测程序错误。

在这两段话中反复地提到”快速失败”。那么何为”快速失败”机制呢？

“快速失败”也就是fail-fast，它是Java集合的一种错误检测机制。当多个线程对集合进行结构上的改变的操作时，有**可能会产生fail-fast机制。记住是有可能，而不是一定。**例如：假设存在两个线程（线程1、线程2），线程1通过Iterator在遍历集合A中的元素，在某个时候线程2修改了集合A的结构（是结构上面的修改，而不是简单的修改集合元素的内容），那么这个时候程序就会抛出 ConcurrentModificationException 异常，从而产生fail-fast机制。



在前面介绍 ArrayList的扩容问题时对于modCount的操作没有详细说明，该变量的操作在add，remove等操作中都会发生改变。那么该变量到底有什么作用呢？

## 简介

fail-fast 机制，即快速失败机制，是java集合(Collection)中的一种错误检测机制。当在迭代集合的过程中该集合在结构上发生改变的时候，就有可能会发生fail-fast，即抛出 ConcurrentModificationException异常。fail-fast机制并不保证在不同步的修改下一定会抛出异常，它只是尽最大努力去抛出，所以这种机制一般仅用于检测bug。

## fail-fast的出现场景

在我们常见的java集合中就可能出现fail-fast机制,比如ArrayList，HashMap。在多线程和单线程环境下都有可能出现快速失败。
1、单线程环境下的fail-fast：
ArrayList发生fail-fast例子：
     public static void main(String[] args) {
           List<String> list = new ArrayList<>();
           for (int i = 0 ; i < 10 ; i++ ) {
                list.add(i + "");
           }
           Iterator<String> iterator = list.iterator();
           int i = 0 ;
           while(iterator.hasNext()) {
                if (i == 3) {
                     list.remove(3);
                }
                System.out.println(iterator.next());
                i ++;
           }
     }
该段代码定义了一个Arraylist集合，并使用迭代器遍历，在遍历过程中，刻意在某一步迭代中remove一个元素，这个时候，就会发生fail-fast。


HashMap发生fail-fast：
     public static void main(String[] args) {
           Map<String, String> map = new HashMap<>();
           for (int i = 0 ; i < 10 ; i ++ ) {
                map.put(i+"", i+"");
           }
           Iterator<Entry<String, String>> it = map.entrySet().iterator();
           int i = 0;
           while (it.hasNext()) {
                if (i == 3) {
                     map.remove(3+"");
                }
                Entry<String, String> entry = it.next();
                System.out.println("key= " + entry.getKey() + " and value= " + entry.getValue());
                i++;
        }
     }
该段代码定义了一个hashmap对象并存放了10个键值对，在迭代遍历过程中，使用map的remove方法移除了一个元素，导致抛出了 ConcurrentModificationException异常：

## 2、多线程环境下：

public class FailFastTest {
     public static List<String> list = new ArrayList<>();

     private static class MyThread1 extends Thread {
           @Override
           public void run() {
                Iterator<String> iterator = list.iterator();
                while(iterator.hasNext()) {
                     String s = iterator.next();
                     System.out.println(this.getName() + ":" + s);
                     try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                }
                super.run();
           }
     }
     
     private static class MyThread2 extends Thread {
           int i = 0;
           @Override
           public void run() {
                while (i < 10) {
                     System.out.println("thread2:" + i);
                     if (i == 2) {
                           list.remove(i);
                     }
                     try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                     i ++;
                }
           }
     }
     
     public static void main(String[] args) {
           for(int i = 0 ; i < 10;i++){
            list.add(i+"");
        }
           MyThread1 thread1 = new MyThread1();
           MyThread2 thread2 = new MyThread2();
           thread1.setName("thread1");
           thread2.setName("thread2");
           thread1.start();
           thread2.start();
     }
}
启动两个线程，分别对其中一个对list进行迭代，另一个在线程1的迭代过程中去remove一个元素，结果也是抛出了java.util.ConcurrentModificationException

## fail-fast的原理

fail-fast是如何抛出ConcurrentModificationException异常的，又是在什么情况下才会抛出?
我们知道，对于集合如list，map类，我们都可以通过迭代器来遍历，而Iterator其实只是一个接口，具体的实现还是要看具体的集合类中的内部类去实现Iterator并实现相关方法。这里我们就以ArrayList类为例。在ArrayList中，当调用list.iterator()时，其源码是：
    public Iterator<E> iterator() {
        return new Itr();
    }
即它会返回一个新的Itr类，而Itr类是ArrayList的内部类，实现了Iterator接口，下面是该类的源码：
    /**
     * An optimized version of AbstractList.Itr
     */
    private class Itr implements Iterator<E> {
        int cursor;       // index of next element to return
        int lastRet = -1; // index of last element returned; -1 if no such
        int expectedModCount = modCount;

        public boolean hasNext() {
            return cursor != size;
        }
     
        @SuppressWarnings("unchecked")
        public E next() {
            checkForComodification();
            int i = cursor;
            if (i >= size)
                throw new NoSuchElementException();
            Object[] elementData = ArrayList.this.elementData;
            if (i >= elementData.length)
                throw new ConcurrentModificationException();
            cursor = i + 1;
            return (E) elementData[lastRet = i];
        }
     
        public void remove() {
            if (lastRet < 0)
                throw new IllegalStateException();
            checkForComodification();
     
            try {
                ArrayList.this.remove(lastRet);
                cursor = lastRet;
                lastRet = -1;
                expectedModCount = modCount;
            } catch (IndexOutOfBoundsException ex) {
                throw new ConcurrentModificationException();
            }
        }
     
        @Override
        @SuppressWarnings("unchecked")
        public void forEachRemaining(Consumer<? super E> consumer) {
            Objects.requireNonNull(consumer);
            final int size = ArrayList.this.size;
            int i = cursor;
            if (i >= size) {
                return;
            }
            final Object[] elementData = ArrayList.this.elementData;
            if (i >= elementData.length) {
                throw new ConcurrentModificationException();
            }
            while (i != size && modCount == expectedModCount) {
                consumer.accept((E) elementData[i++]);
            }
            // update once at end of iteration to reduce heap write traffic
            cursor = i;
            lastRet = i - 1;
            checkForComodification();
        }
     
        final void checkForComodification() {
            if (modCount != expectedModCount)
                throw new ConcurrentModificationException();
        }
    }
其中，有三个属性：
int cursor;       // index of next element to return
int lastRet = -1; // index of last element returned; -1 if no such
int expectedModCount = modCount;
cursor是指集合遍历过程中的即将遍历的元素的索引，lastRet是cursor -1，默认为-1，即不存在上一个时，为-1，它主要用于记录刚刚遍历过的元素的索引。expectedModCount这个就是fail-fast判断的关键变量了，它初始值就为ArrayList中的modCount。（modCount是抽象类AbstractList中的变量，默认为0，而ArrayList 继承了AbstractList ，所以也有这个变量，modCount用于记录集合操作过程中作的修改次数，与size还是有区别的，并不一定等于size）
我们一步一步来看：
        public boolean hasNext() {
            return cursor != size;
        }
迭代器迭代结束的标志就是hasNext()返回false，而该方法就是用cursor游标和size(集合中的元素数目)进行对比，当cursor等于size时，表示已经遍历完成。
接下来看看最关心的next()方法，看看为什么在迭代过程中，如果有线程对集合结构做出改变，就会发生fail-fast：
       @SuppressWarnings("unchecked")
        public E next() {
            checkForComodification();
            int i = cursor;
            if (i >= size)
                throw new NoSuchElementException();
            Object[] elementData = ArrayList.this.elementData;
            if (i >= elementData.length)
                throw new ConcurrentModificationException();
            cursor = i + 1;
            return (E) elementData[lastRet = i];
        }
从源码知道，每次调用next()方法，在实际访问元素前，都会调用checkForComodification方法，该方法源码如下：
        final void checkForComodification() {
            if (modCount != expectedModCount)
                throw new ConcurrentModificationException();
        }
可以看出，该方法才是判断是否抛出ConcurrentModificationException异常的关键。在该段代码中，当modCount != expectedModCount
时，就会抛出该异常。但是在一开始的时候，expectedModCount初始值默认等于modCount，为什么会出现modCount != expectedModCount，很明显expectedModCount在整个迭代过程除了一开始赋予初始值modCount外，并没有再发生改变，所以可能发生改变的就只有modCount，在前面关于ArrayList扩容机制的分析中，可以知道在ArrayList进行add，remove，clear等涉及到修改集合中的元素个数的操作时，modCount就会发生改变(modCount ++),所以当另一个线程(并发修改)或者同一个线程遍历过程中，调用相关方法使集合的个数发生改变，就会使modCount发生变化，这样在checkForComodification方法中就会抛出ConcurrentModificationException异常。
类似的，hashMap中发生的原理也是一样的。
避免fail-fast
了解了fail-fast机制的产生原理，接下来就看看如何解决fail-fast
方法1
在单线程的遍历过程中，如果要进行remove操作，可以调用迭代器的remove方法而不是集合类的remove方法。看看ArrayList中迭代器的remove方法的源码：
        public void remove() {
            if (lastRet < 0)
                throw new IllegalStateException();
            checkForComodification();

            try {
                ArrayList.this.remove(lastRet);
                cursor = lastRet;
                lastRet = -1;
                expectedModCount = modCount;
            } catch (IndexOutOfBoundsException ex) {
                throw new ConcurrentModificationException();
            }
        }

可以看到，该remove方法并不会修改modCount的值，并且不会对后面的遍历造成影响，因为该方法remove不能指定元素，只能remove当前遍历过的那个元素，所以调用该方法并不会发生fail-fast现象。该方法有局限性。
例子：
     public static void main(String[] args) {
           List<String> list = new ArrayList<>();
           for (int i = 0 ; i < 10 ; i++ ) {
                list.add(i + "");
           }
           Iterator<String> iterator = list.iterator();
           int i = 0 ;
           while(iterator.hasNext()) {
                if (i == 3) {
                     iterator.remove(); //迭代器的remove()方法
                }
                System.out.println(iterator.next());
                i ++;
           }
     }
方法2
使用java并发包(java.util.concurrent)中的类来代替 ArrayList 和hashMap。
比如使用 CopyOnWriterArrayList代替 ArrayList， CopyOnWriterArrayList在是使用上跟 ArrayList几乎一样， CopyOnWriter是写时复制的容器(COW)，在读写时是线程安全的。该容器在对add和remove等操作时，并不是在原数组上进行修改，而是将原数组拷贝一份，在新数组上进行修改，待完成后，才将指向旧数组的引用指向新数组，所以对于 CopyOnWriterArrayList在迭代过程并不会发生fail-fast现象。但 CopyOnWrite容器只能保证数据的最终一致性，不能保证数据的实时一致性。
对于HashMap，可以使用ConcurrentHashMap， ConcurrentHashMap采用了锁机制，是线程安全的。在迭代方面，ConcurrentHashMap使用了一种不同的迭代方式。在这种迭代方式中，当iterator被创建后集合再发生改变就不再是抛出ConcurrentModificationException，取而代之的是在改变时new新的数据从而不影响原有的数据 ，iterator完成后再将头指针替换为新的数据 ，这样iterator线程可以使用原来老的数据，而写线程也可以并发的完成改变。即迭代不会发生fail-fast，但不保证获取的是最新的数据。
参考链接：
http://www.jb51.net/article/84468.htm
http://www.cnblogs.com/ccgjava/p/6347425.html?utm_source=itdadao&utm_medium=referral

原文链接：https://blog.csdn.net/zymx14/article/details/78394464