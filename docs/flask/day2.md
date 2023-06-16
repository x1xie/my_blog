# flask 进阶编笔记
# 1.项目启动
```python
from flask import Flask
def create_app():
    app = Flask(__name__, template_folder="templates", static_folder='static', static_url_path='/static')
    app.secret_key = app.config['SECRET_KEY']
    # 加载配置文件
    app.config.from_object('config.settings')
    print(app.config['DB_HOST'])
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return 'Hello World!'
    return app
```
1) 读取配置文件中的所有键值对，将键值对全部放到config对象中。（config为一个字典）
2) 把包含所有配置文件的config对象赋值给app.config
3) 添加路由映射：  
    3-1.将url=/index和methods=['GET', 'POST']和endpoint封装到Rule对象  
    3-2.将Rule对象添加到app.url_map中。
    3-3.把endpoint和函数的对应关系放到app.view_functions中
# 2.用户请求到来
1) 创建ctx=RequestContext对象，其内部封装了Request对象和session数据
2) 创建app_ctx=AppContext对象，其内封装了app和g。
3) 然后ctx.push触发ctx和app_ctx分别通过自己的LoclaStack对象将其放入Local中，Local的本质是以线程ID为key，以{"stack":[]}为value的字典。
```
{
    1111:{"stack":[ctx,]}
}
注意：之后再想要获取request/ session/ app/ g 时，都需要去local中获取。
```
4) 执行所有的before_request函数
5) 执行视图函数
6) 执行所有after_request函数（session加密放到cookie中）
7) 销毁ctx和app_ctx
# 3.g是什么
1) 再一次请求的周期，可以再g中设置值，在本次的请求周期中都可以读取或者复制。相当于是一次请求周期的全局变量。
```python
from flask import Flask
app = Flask(__name__)
@app.before_request
def f1():
    g.x1 = 123
@app.route('/index')
def index():
    print(g.x1)
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
# 4.flask信号(flask内部扩展点)
- 信号是在flask框架中为我们预留的构子，让我们进行一些自定义操作。  
根据flask项目的请求流程来进行设置扩展点 
- 信号没有返回值，可以通过抛出异常来控制
### 安装
```
pip3 install blinker
```
### 中间件
很少使用，中间件使用不了flask，中间件使用之后才到flask中RequestContext，AppContext
```python
from flask import Flask,render_template
app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello World!'
class MyMiddleWare(object):
    def __init__(self, old_wsgi_app):
        self.old_wsgi_app = old_wsgi_app

    def __call__(self, environ, start_response):
        print('开始之前')
        response = self.old_wsgi_app(environ, start_response)
        print('结束之后')
        return response
if __name__ == '__main__':
    # 把原来的wsgi_app替换为自定义的
    app.wsgi_app = MyMiddleWare(app.wsgi_app)
    app.run()
```
#### @signals.appcontext_pushed.connect()
- 当app_ctx被push到local中栈之后，会被触发appcontext_push信号，之前注册在这个信号中的方法，就会被执行。
  (运行之后打印：appcontext_push信号触发 <Flask 'pro_app1.testapp'>)
```python
from flask import signals
from flask import Flask
app = Flask(__name__)
@signals.appcontext_pushed.connect
def f1(arg):
   print('appcontext_push信号触发',arg)

@app.route('/index')
def index():
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
#### @app.before_first_request 将在Flask 2.3中移除
只在第一个请求之前调用，第一个请求之后不再调用。
```python
@app.before_first_request
def f1():
   print('before_first_request信号被触发')
```
#### @signals.request_started.connect
请求开始之前执行（运行打印：request_started信号被触发 <Flask 'pro_app1.testapp'>）
```python
from flask import signals
from flask import Flask
app = Flask(__name__)
@signals.request_started.connect
def f1(arg):
    print('request_started信号被触发',arg)
@app.route('/index')
def index():
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
#### @app.url_value_preprocessor 与 @app.before_request
- before_request 请求之前执行装饰器下的函数
- url_value_preprocessor装饰器执行在before_request之前，可以与g连用，g中设置的值可以在请求周期内生效
（运行打印：f2  ；    before_request信号被触发 123）
```python
from flask import Flask, g
app = Flask(__name__)
@app.url_value_preprocessor
def f2(enpoint,args):
    g.xx = 123
    print('f2')
@app.before_request
def f1():
    print('before_request信号被触发', g.xx)
@app.route('/index')
def index():
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
### 视图函数
#### before_render_template 与 template_rendered.connect
- @signals.before_render_template.connect视图渲染之前执行装饰器下的函数。
- @signals.template_rendered.connect 视图模板渲染之后执行装饰器下的函数。
- render_template相关。    运行结果：f1  ;  f2
```python
from flask import signals
from flask import Flask,render_template
app = Flask(__name__)
@signals.before_render_template.connect
def f1(app, template, context):
    print('f1')

@signals.template_rendered.connect
def f2(app, template, context):
    print('f2')
@app.route('/')
def index():
    return render_template('md.html')
if __name__ == '__main__':
    app.run()
```
#### @app.after_request
- 请求后执行装饰器下的函数
```python
from flask import Flask
app = Flask(__name__)
@app.after_request
def f1(response):
    print('after_request信号被触发')
    return response
@app.route('/index')
def index():
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
#### @signals.request_finished.connect
- 请求完成时，在@app.after_request之后执行，还在一个请求周期内
```python
from flask import signals
from flask import Flask
app = Flask(__name__)
@signals.request_finished.connect
def f1(app, response):
    print('f1')
@app.route('/index')
def index():
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
#### @signals.got_request_exception.connect
触发异常之后，@app.after_request 和request_finished 还会被执行一遍

```python
from flask import signals
from flask import Flask
app = Flask(__name__)
@app.before_request
def test():
    int('2323')
@signals.got_request_exception.connect
def f2(app, exception):
    print('f2异常操作')
@app.route('/index')
def index():
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
#### @app.teardown_request
- 请求之后，成功与否都会执行
```python
from flask import Flask
app = Flask(__name__)
@app.teardown_request
def f1(exc):
    print('f1')
@app.route('/index')
def index():
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
#### @signals.request_tearing_down.connect
```python
from flask import signals
from flask import Flask
app = Flask(__name__)
@signals.request_tearing_down.connect
def f1(app, exc):
    print('f1')
@app.route('/index')
def index():
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
#### appcontext_popped
```python
from flask import signals
from flask import Flask
app = Flask(__name__)
@signals.appcontext_popped.connect
def f1(app):
    print('app销毁')
@app.route('/index')
def index():
    return 'hello world'
if __name__ == '__main__':
    app.run()
```
# 5.flask-script组件
pip下载
```
pip3 install flask-script
```
运用：
```python
from pro_app1 import create_app
from flask_script import Manager

app = create_app()
manager = Manager(app)
@Manager.command
def custom(arg):
    """
    自定义命令
    python manage.py custom 123
    """
    print (arg)
@Manager.option('-n', '--name', dest='name')
@Manager.option('-u', '--url', dest='url')
def cmd(name,url):
     """
    自定义命令
    python manage.py cmd -n testname -u http://www.baidu.com
    :param name,url
    :return
    """
     print(name,url)
if __name__ == '__main__':
    manager.run()
```
#### 其他
```
结合：flask-migrate / flask-sqlalchemy
实现数据库迁移
python manage.py migrate
```