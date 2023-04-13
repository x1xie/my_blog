# flask面试题
# 1. django与flask的区别
```
django大而全；flask小而精
- 概括的区别
- django中提供的功能列例
- 请求处理机制不同，django是通过参的形式，flask是通过上下文管理的方式实现。
```
# 2.wsgi
django和flask内部都没有实现socket，而是wsgi实现。  
wsgi是web服务网关接口，它是一个协议，实现它的协议有：wsgiref/werkzurg/uwsgi
```python
# django之前
from  wsgiref.simple_server import make_server
def run(environ, start_response):
    start_response('200 OK',[('Content-TYpe','text/html')])
    return [bytes('<h1>Hello world</h1>', encoding='utf-8'),]
if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 8000, run)
    httpd.serve_forever()

# flask 之前
from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
def func(environ, start_response):
    response = Response('hello world')
    print('请求到来')
    return response(environ, start_response)
if __name__ == '__main__':
    run_simple('127.0.0.1', 7000, func)
```
# 3. web框架都有的功能：
```
路由、视图、模板
```

# 4. before_request/ after_request
```
相当于django的中间件，对所有的请求定制功能
```
# 5. tempalte_global/ template_filter
```
定制在所有模板中都可以只有的函数（蓝图的话是一个蓝图中使用）
```
# 6. 路由系统处理的本质@app.route
```
将url和函数打包成rule, 添加到map对象，map对象在放到app中
```
# 7.路由
```
- 装饰器实现 / add_url_rule
- endpoint 起别名 给url_for('别名')使用
- 如果给视图加装饰器：放在route下面、functools防止装饰器函数重名
```
# 8. 视图
```
- FBV
- CBV (返回一个view函数，闭包的应用场景)
- 应用到的功能都是通过导入方式：request/session
```
# 9. flask中支持session
```
默认将session加密，然后保存在浏览器cookie中
```
10. 模板比django更方便，支持python原生的语法
# 11. 蓝图
```
- 帮助我们可以多很多的业务功能做拆分，创建多个py文件，把各个功能放置到各个蓝图中，
最后再将蓝图注册到flask对象中。
- 帮助我们做目录结构的拆分。
```
```
12. threading.local对象 自动为每个线程开辟空间，让你进行存取值
13. 数据库连接池dbutils (SQLHelper)
14. 面向对象上下文管理器（with）
15.在app=Flask()对象中可以传入静态文件、模板的配置。
16.通过app.config读取配置文件（localsettings.py）。
17.Flask可以定义FBV和CBV
18.flask中内置了session,session的数据以加密的形式放入cokie中。
19.flask自己没有模板，而是用的第三方的jinja2模板。
```
# 20.flask的蓝图和django的app有什么区别
```
相同点：都是用于做业务拆分 / 需要注册才能使用 /都可以在自己内部定义模板和静态文件。
不同的：注册位置不同、flask before/after_request和django中间件的应用粒度更细、django的app内置了很多，flask蓝图没有内置
```
# 21.特殊装饰器
```
before_first_request
before_request
route
after_request
template_global
template_filter
```
# 22.为flask的视图设置装饰器时，需要
 - 位置   
 - functools.wraps  
 - functools.partoal
# 23.从看flask源码你学到了什么
```
- 新的编程思路。
    -django 、drf数据是通过传递
    -flask, 存储在一个地方，以后用的时候去取。
    哪种好？两个不同的实现机制，没有好坏之分。
    django好，如果是一个初学者对于django的机制比较好理解，flask学习代价比较大（了解上下文管理机制之后才能更好理解）。
- 技术点
    -单例模式的应用场景
    -LocalProxy
    -装饰器 注意functools
```
# 24.在flask的Local对象中为什么要通过线程ID进行区分？
```
因为在flask中可以开启多线程的模式，当开启多线程模式进行处理用户请求时，需要将线程之间的数据进行隔离，
以防止数据混乱。
```
# 25.在flask的Local对象中为什么要维持成一个栈
```
{
    111：{stack:[ctx,]}
}
# 在写离线脚本时，才会用在栈中放多个对象。（创建一个py文件本地运行）
from flask import current_app,g
from pro_app1 import create_app
app1 = create_app()
with app1.app_context(): #AppContext对象(app.g) -> local对象
    print(current_app.config) #app1
    app2 = create_app()
    with app2.app_context(): #AppContext对象(app.g) -> local对象
        print(current_app.config)
    print(current_app.config)
# 写离线脚本且多个上下文嵌套时，才会在栈中添加多个对象。
# 注意：在flask中很少出现嵌套的脚本
```
