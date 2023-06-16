# flask 部署
# 1.第一步
### 1.为什么用Linux
- 日常 window 收费+图形化界面慢
- 部署 Linux 免费+图形化界面/非图形化
### 2.公网ip  (例如：82.156.54.134)
### 3.登录服务员
- Web界面（非主流）
- ssh工具
  - win(xshell)
    - ssh root@82.156.54.134
  - mac(item2)  [基于公钥+私钥]
    - cd ~/.ssh
        - id_rsa  ，id_rsa.pub
    - 用ssh-copy-id将公钥复制到远程机器中
    - ssh-copy-id -i ~/.ssh/id_rsa/pub root@82.156.54.134
    - ssh root@82.156.54.134
# 2.第二步
### 1.电脑安装git
### 2.远程仓库
- https://gitee.com/xxx/xxx.git
### 3. (.gitigonre)
- git要忽略的文件
### 4.命令
- 4.1 一次性的命令
  - git config --global user.name 'testname'
  - git config --global user.email 'xxxxxx@qq.com'
  -
  - cd project1
  - git init
  - git remote add origin https://gitee.com/xxx/xxx.git
- 4.2 经常执行
  - git add
  - git commit -m 'init'
  - git push origin master
# 3.第三步（代码下载）
- 安装git
  -yum install git
- 第一次
  - cd /data/
  - mkdirs www
  - cd /data/www/
  - git clone https://gitee.com/xxx/xxx.git
  - 码云账号+密码
- 之后
  - cd /data/www/project1/
  - git pull origin master
# 第三步
### 1.安装gcc
- yum install gcc -y
### 2.安装python依赖
```
yum install zlib zilb-devel -y
yum install bzip2 bzip2-devel -y
yum install ncurses ncurses-devel -y
yum install readline realine-devel -y
yum install openssl openssl-devel -y
yum install xz lzma xz-devel -y
yum install sqlite sqlite-devel -y
yum install gdbm gdbm-devel -y
yum install tk tk-devel -y
yum install mysql-devel -y
yum install python-devel -y
yum install libffi-devel -y
```
### 3.下载源码
- yum install wget -y
- cd /data/
- wget http://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
### 4.解压 & 编译 & 安装
- tar -xvf Python-3.9.5.tgz
- ./configure
- make all
- make install
# 4.第四步
### 1.安装virtualenv
- pip3 install virtualenv
### 2.创建虚拟环境
- 代码： /data/www/project1
- 环境： 
  - /envs/nb
  - mkdir /envs
  - virtualenv /envs/nb --python=python3.9
### 3.激活虚拟环境
- source /envs/nb/bin/activate
### 4.虚拟环境本地运行
- source /envs/nb/bin/activate
- cd /data/www/project1
- python app.py

# 5.uwsgi
### 1.安装
- source /envs/nb/bin/activate
- pip install uwsgi
### 2.基于uwsgi运行flask项目
- cd 项目目录
- 命令方式：
  - uwsgi --http :8000 --wsgi-file app.py --callable app（--wsgi-file 执行文件， --callable app.py执行的app对象）
- 配置文件（推荐）
  - nb_uwsgi.ini
    - [uwsgi]
    - socket = 127.0.0.1:8001
    - chdir = /data/www/project1
    - wsgi-file = app.py
    - callable = app
    - processes =1
    - virtualenv = /envs/nb/
  - source /envs/nb/bin/activate
  - uwsgi --ini nb_uwsgi.ini
- 停止
  - ps -ef|grep nb_wsgi
  - kill -9 12324
# 6.Nginx
### 1.安装
- yum install nginx -y
### 2.配置
- 普通请求 -> 8001端口
- /static/ -> /data/www/project1/static
- nginx的默认配置文件路径 /etc/nginx/nginx.conf
#### 2.1 修改默认配置
- cd etc/nginx/
- vim nginx.conf  
修改内容:
```
upstream flask {
  sever 127.0.0.1:8001;
}

server {
  listen 80;
  listen [::]:80;
  location /static {
    alias /data/www/project1/static;
  }
  
  localtion / {
    uwsgi_pass flask;
    include uwsgi_params;
  }  
}
```
### 3.启动nginx
- systemctl start nginx
- systemctl stop nginx
- systemctl restart nginx
#### 3.1 开机自启动
- systemctl enable nginx
#### 备注
- git 提交代码后，需要重新加载uwsgi ,否则最新的代码加载不到内存

# 7.重启和停止uwsgi脚本
### 重启 reboot.sh
```
#!/usr/bin/env bash

echo -e "\033[34m---------------wsgi process---------------\033[0m"
ps -ef|grep nb_uwsgi.ini | grep -v grep
sleep 0.5
echo -e '\n---------------going to close---------------'
ps -ef | grep nb_uwsgi.ini | grep -v grep | awk '{print $2}' | xargs kill -9
sleep 0.5
echo -e '\n------check if the kill action is correct--------'
/envs/nb/uwsgi --ini nb_uwsgi.ini & >/dev/null
echo -e "\n\033[42;lm---------------started...---------------\033[0m"
sleep 1
ps -ef | grep nb_uwsgi.ini | grep -v grep
```
- 修改权限 chmod 755 reboot.sh
- 运行：./reboot.sh
### 停止 stop.sh
```
#!/usr/bin/env bash

echo -e "\033[34m---------------wsgi process---------------\033[0m"
ps -ef|grep nb_uwsgi.ini | grep -v grep
sleep 0.5
echo -e '\n---------------going to close---------------'
ps -ef | grep nb_uwsgi.ini | grep -v grep | awk '{print $2}' | xargs kill -9
sleep 0.5
```
- 修改权限 chmod 755 stop.sh
- 运行：./stop.sh

# 8.项目mysql依赖
### 1.安装MySQL服务
```
yum install mariadb-server -y
yum install mariadb -y
```
### 2.授权
```
- 创建数据库 proapp
create database proapp1db default charset utf8 collate utf_general_ci;
- 创建用户 s5
insert into mysql.user(user,host,password) values('s5','%',password('test123'));
flush privileges;
- 授权
grant all privileges on proapp1db.* to s5@'%';
flush privileges;
- 测试
  - 远程测试 --ok
  - 本地测试 
    - 无密码可以登录 --> 去除密码为空的用户

```
### 3.启动
```
systemctl start mariadb
- 停止
systemctl stop mariadb
- 设置开机自启动
systemctl enable mariadb
- 登录
mysql -u root -p
```
# 9.项目依赖redis
```
- 安装
yum install redis -y
- 配置  /etc/redis.config
  - 密码 vim /etc/redis.config 寻找 ?requirepass 修改密码
  - bing 127.0.0.1  远程 bing 0.0.0.0
- 启动
systemctl start redis
- 停止
systemctl stop redis
- 设置开机自启动
systemctl enable redis
- 项目代码
pip install redis
```