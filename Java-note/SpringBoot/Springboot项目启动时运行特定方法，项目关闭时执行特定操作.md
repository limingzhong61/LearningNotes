# Springboot项目启动时运行特定方法，项目关闭时执行特定操作

做微信授权时遇到的问题，项目启动时要先获取accesstoken，保证后面程序能够读取，记录下解决方法：

首先项目启动时运行

```java
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
 
@Component
@Order(value = 1)
public class StartGlobalKeyboard implements CommandLineRunner{
 
	@Override
	public void run(String... args) throws Exception {
			//你的要执行的代码
	}
 
}
```

@Component就不用解释了

@Order(value = 1)定义执行顺序，告诉项目加载完优先执行

项目关闭时运行

```java
import javax.annotation.PreDestroy;

import org.springframework.stereotype.Component;


@Component
public class EndGlobalKeyboard {

    @PreDestroy
    public void destory() throws Exception {
    	//你的代码
    }

}
```

被@PreDestroy修饰的方法会在服务器卸载Servlet的时候运行，并且只会被服务器调用一次，类似于Servlet的destroy()方法。被@PreDestroy修饰的方法会在destroy()方法之后运行，在Servlet被彻底卸载之前。
————————————————
参考链接

- 原文链接：https://blog.csdn.net/qq_38361800/article/details/95943547