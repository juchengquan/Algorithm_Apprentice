# 傻瓜式在CentOS 7下配置Python Flask + Nginx + uwsgi

## 0. 准备步骤
配置基础环境，用于下载包及编译
```
yum install wget gcc make 
```

安装相关依赖
```
yum install bzip2-devel ncurses-devel sqlite-devel gdbm-devel xz-devel tk-devel readline-devel libffi-devel openssl-devel expat-devel 
```

## 1. 使用源码进行编译安装Python (ver. 3.7.4)
从Python官网下载源码包，并且解压缩到当前路径：
```
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz
xz -d Python-3.7.4.tar.xz
tar -xvf Python-3.7.4.tar
```

选择安装路径为 ```/usr/local/python3.7``` 进行编译(sudo)：
```
cd Python-3.7.4
./configure --prefix=/usr/local/python3.7 --enable-optimizations
make && make install
```

- 为避免root权限，可以选择安装路径为```/home/user_name/software/python3.7```：
```
cd Python-3.7.4
./configure --prefix=/home/user_name/software/python3.7 --enable-optimizations
make && make install
```

为Python3添加环境变量：打开 ```.bashrc```:
```
vi .bashrc
```
在最后添加```PATH```的路径（注意其中路径与上面的安装路径对应）：
```
export PATH=$PATH:/home/user_name/software/python3.7/bin
```

下面，创建Python3的软连接。

由于```yum```使用Python2，因此需要修改配置文件使其正常工作。

首先复制原Python2.7的目录：
```sh
cd /usr/bin/
mv python python.bak
```

连接python安装路径至 ```/usr/bin/``` :
```sh
ln -s /usr/local/python3.7/bin/python3.7 /usr/bin/python
```

打开```yum```的配置文件：

```sh
vi /usr/bin/yum
```

将第一行改为：
```
#!/usr/bin/python2.7
```

同样地，打开urlgrabber的配置文件：
```
vi /usr/libexec/urlgrabber-ext-down
```

将第一行改为：
```
#!/usr/bin/python2.7
```

为pip3创建软连接：

```
ln -s /usr/local/python3.7/bin/pip3 /usr/bin/pip3
```

最后，测试python的版本：
```
python -V
```

## 2. 创建Python虚拟环境

创建虚拟环境目录，路径为```~/py_env0```：
```
virtualenv py_env0
```

激活虚拟环境：
```
source py_env0/bin/activate
```
- 取消激活可用如下命令：
```
deactivate
```


## 3. 配置Nginx
通过yum安装Nginx：
```
yum install nginx
```

配置conf文件，使其在root用户下运行：
- 打开 ```nginx.conf```：
```
vi /etc/nginx/nginx.conf
```
- 更改第一行如下：
```
user root
```
- 同时更改配置文件```/etc/nginx/nginx.conf```, 使其可以自定义文件夹内的配置文件：
```
22 # include /etc/nginx/conf.d/*.conf;
23 # include /home/supper-user/misc_setting/nginx/*.conf;
```

启动nginx服务(可能需要sudo)：
```
nginx  # 开启nginx服务(可能需要sudo权限)
```

此时查看```http://localhost:80```，会出现如下的欢迎页面：
![nginx_welcome](./fig/nginx_welcome.png)


同时，新建文件夹存放配置文件，注意与上述路径对应：
```
mkdir -p misc_setting/nginx
```
重启nginx服务：
```
nginx -s reload #sudo
```

## 4. 配置Flask

- 安装Flask

```
pip3 install flask
```

- 新建一个样例，测试flask是否能正常运行：

```
vi flask_test.py
```

编辑文件如下：

```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World</h1>"

if __name__ == "__main__":
    app.run() # 默认端口为5000，与nginx配置对应
```


接下来，在```misc_setting/nginx/```下创建配置文件(文件名称自定义)：

```
vi misc_setting/nginx/flask_api.conf
```
```
server {
    listen 8080;
    server_name  xxx.xxx.xxx.xxx; # External IP

    location / {
        proxy_pass http://127.0.0.1:5000; # Local IP with port ID
        proxy_set_header Host $http_host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

重启nginx服务：
```
nginx -s reload #sudo
```

运行sample script
```
python flask_test.py
```

- 在浏览器中打开``` http://xxx.xxx.xxx.xxx:8080```，会出现以下页面：

![hello_world](./fig/hello_world.png)


## 4. 配置uwsgi
安装uwsgi：
```
pip3 install uwsgi
```

新建配置文件 ```flask_uwsgi.conf``` 如下：
```
vi misc_setting/nginx/flask_uwsgi.conf
```
```
upstream flask{
        server 127.0.0.1:50819;
    }

    # Virtual host, with this option, we can visit our web site on server_name.
    # If the server_name is an ip address and we has configured a DNS,
    # we can also use the corresponding domain name.

    server {

        listen              5000;

        server_name         xxx.xxx.xxx.xxx;
        charset             utf-8;

        # the web site resources path
        location / {
            include         uwsgi_params;
            uwsgi_pass      flask;
            }
    }
```
**注意**：分配的端口号为50819，server_name与端口需要与之后的uwsgi服务一致。


接下来，为提供特定的服务(如OptService)创建文件夹:
```
mkdir en_opt
```

创建uwsgi 配置文件```uwsgi_conf.ini```如下：
```
vi en_opt/uwsgi_conf.ini
```

```
[uwsgi]

http = :50819

chdir = ./en_opt

wsgi-file = flask_service.py

callable = app

processes = 2

threads = 2

stats = 127.0.0.1:9191
```
注意端口号须与配置的nginx服务端口号一致(端口号：50819)

将文件复制到新文件夹：
```
mv flask_test.py en_opt/flask_text.py
```


**注意**：禁用之前设置的```flask_api.conf```:
```
mv en_opt/flask_api.conf en_opt/flask_api.bak
```


重启nginx:
```
nginx -s reload # sudo
```

挂载uwsgi服务：
```
uwsgi en_opt/uwsgi_conf.ini
```
放于后台运行，并且退出后不终止：
```
nohup uwsgi en_opt/uwsgi_conf.ini &
```

完毕。
