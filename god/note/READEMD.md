## Arthas 查看数据库密码
```shell
vmtool --action getInstances --className java.sql.Connection --limit 1 -x 4 
```

## Apt-get 代理加速下载

```shell
apt-get -o Acquire::http::proxy="http://172.17.0.1:7891/" install fonts-noto-cjk-extra
```

## nginx 镜像反代理网址

```nginx
server {
    listen 8023; # 监听端口
    server_name du.ironblog.cn; # 匹配域名


    # 屏蔽搜索引擎
    if ($http_user_agent ~* (baiduspider|360spider|haosouspider|googlebot|soso|bing|sogou|yahoo|sohu-search|yodao|YoudaoBot|robozilla|msnbot|MJ12bot|NHN|Twiceler)) {
        return  403;
    }


    location / {
            sub_filter byr.pt  byr.ironblog.cn; # 替换域名
            sub_filter bt.byr.cn  byr.ironblog.cn; # 替换域名
            sub_filter_once off; # 是否只替换一次
            proxy_set_header X-Real-IP $remote_addr; # 传递真实IP
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
            proxy_set_header Referer https://byr.pt; # 设置请求来源
            proxy_set_header Host byr.pt; # 设置请求HOST 
            port_in_redirect off; # 目标服务器 302 转发时，禁止添加内网端口
            proxy_pass https://byr.pt; # 目标服务器
            proxy_set_header Accept-Encoding ""; # 设置允许所有编码
    }

    location /js/echarts.min.js {  # 替换指定的文件
        alias /data/js/echarts.min.js;
    }       

}

```