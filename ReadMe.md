# Django 简易图床
由于 `七牛图床` 需要绑定需要备案的域名，过程比较麻烦与漫长。所以使用 `Django` 框架写了一个简易版的图床存储，方便部署在自己的服务器上，以后就能开心继续写 `Markdown` 了 (原来保存在`七牛图床`上的图都用不了了.此项目更好的让大家保存图片，防止丢失[**PS:当然前提你服务器没问题!**])

# Usage:

### 1. 首先拉去项目到服务器本地
```
git clone https://github.com/swlfigo/djangoImageContainer.git
```

### 2. 安装 `Python` 相关依赖库

**此项目在`Python3`, `Django (2.0.5)`,                                                                                                `djangorestframework (3.9.0)` 下运行正常**

```
pip install -r require.txt
```

### 3. 使用 `PM2` 拉起项目(推荐)

> PM2是node进程管理工具，可以利用它来简化很多node应用管理的繁琐任务，如性能监控、自动重启、负载均衡等，而且使用非常简单。

当然，`PM2` 也是能跑 `.sh` , `.py` 等脚本的

**Q:为什么使用`PM2`呢？**
**A:** 简单啊，网上拉起 `Django` 项目是通过 `uswgi` 和 `supervisior` 和 `nginx` 配合，达到重启还能启动网站，配置过一次也是非常麻烦, `PM2`也能达到如此效果，所以选择 `PM2` 来管理

####3.1 安装 NodeJS
新版本的 `Nodejs` 里面已经包含了 `npm` , `Centos` 可以使用下面代码安装 `NodeJS`,如果本机已经有 `NodeJS` 环境可跳过此步
```
sudo yum install nodejs
```

### 3.2 安装PM2
根据官网安装方法
```
npm install pm2 -g 
```

### 4. 拉起项目

安装 `PM2` 成功后进入项目目录，你会发现目录下有 `start.sh` , 这个脚本其实就是启动 `Django` 项目的脚本,默认启动端口 `8002`, 使用者可以打开自行修改

```
pm2 start start.sh --name imageContainer
```

通过上面方法可以拉起项目, `--name` 意思是标识这个服务名字，可自行修改

拉起成功后输入
```
pm2 list
```
可以看到已经成功拉起了

![](http://img.isylar.com/media/15429543834332.jpg)

最后保存修改
```
pm2 save
```
保存修改后，即使重启也能自动开启服务，达到重启也能打开网站功能!

### 5. Nginx 配置(可选)
(以下配置非必须但建议)
成功拉起网站后，可以通过服务器ip访问到，

访问 `ip:8002/file`

能看到网页页面有以下输出,就是成功拉起了项目

`Hello, world. You're at the file index.`

#### 5.1 Nginx 内网转发

**【此段写给萌新(我)看，大佬可忽略】**

打开 `Nginx` 的配置文件,在内容里面修改添加(`只是截取重要部分,更详细配置自行百度 nginx proxy_pass`)


```
server{
    listen 80;
    server_name 自定义域名(域名可通过阿里云等途径购买);
    
    location / {
        proxy_pass http://127.0.0.1:8002; #此端口为上面修改过的项目端口(默认就是8002)
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   Host      $http_host;
    }

}
```

此段意思是，凡是通过自定义域名访问 `80` 端口，自动转发到本地 `8002` 端口

例: `customdomain(自定义域名).com/file`

也能看到上面内容输出,不需要手动加入端口号，使用自定义域名好处是以后写完 Markdown , 添加了图片上图床，即使搞了新的服务器，只需要将旧服务器上的图片数据转移到新服务器上，也可以通过域名访问到。

到此，服务器配置完成

### 6. 项目额外配置

打开项目中 `djangoImageContainer/imageContainer` 目录下的 `setting.py`

![](http://img.isylar.com/media/15429573822131.jpg)

**再此处将 `DEBUG = False` 设置为 `False`, 默认是 `True` 是因为方便调试，上线项目之后不再打印信息，防止别人窥探信息！！！**

`ALLOWED_HOSTS ` 里面添加自定义域名，访问时候只能通过对应的自定义域名访问数据，其他域名访问返回 `404`


### 7 配置 上传信息(非必须但需要看)

#### 7.1 `MWeb` 自定义图床使用
此处使用的 Markdown 工具是  `MWeb`, 因为自带上传图床功能，可以配合此项目使用

![](http://img.isylar.com/media/15429576397165.jpg)

分别有3处地方注意:
1. API 地址填写你服务器地址或(自定义域名) + /file/upload
`http://server/file/upload`

1. `POST文件名` 与 `图片URL路径` 写死 `file`

因为是通过类似表单 `file` 为 key 上传，成功后通过 `file` 为key 的 `JSON` 获得成功上传后的图片地址信息，然后配合下方 `图片URL前缀` 合并出图床的图的具的地址

`http://server/media/xxx.jpg`

1. `remark` 并没有什么用，作为一个表示，随便写即刻,当然你可以修改项目源码里面，加一个权限控制，那么别人也就不会上传图片去你的图床了

#### 7.2 PostMan 测试

![](http://img.isylar.com/media/15429579415368.jpg)


同理返回的信息如下


# The End

项目纯属个人爱好，简单可使用，肯定还是 `七牛` 最好，但是可以避免域名报备需要，有兴趣的可以拉本项目使用.
本`ReadMe`中的图片也是使用本项目的。