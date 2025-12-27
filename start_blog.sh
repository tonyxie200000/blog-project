#!/bin/bash
# 博客服务一键启动脚本

# 激活虚拟环境
source /var/www/blog/blog_system/venv/bin/activate

# 杀死旧的Gunicorn进程（避免端口占用）
pkill gunicorn

# 启动Gunicorn（后台运行）
nohup gunicorn --bind 127.0.0.1:8000 blog_system.wsgi:application > /var/www/blog/gunicorn.log 2>&1 &

# 启动Nginx（确保开机自启）
systemctl start nginx
systemctl enable nginx

# 输出启动成功提示
echo "========================"
echo "博客服务启动成功！"
echo "后台地址：http://你的服务器IP/admin"
echo "前台地址：http://你的服务器IP"
echo "日志文件：/var/www/blog/gunicorn.log"
echo "========================"
