#!/bin/bash
cd /var/www/blog/blog_system
pkill gunicorn
source venv/bin/activate  # 若有虚拟环境必加，无则删除
gunicorn --bind 127.0.0.1:8000 blog_system.wsgi:application &
echo "博客服务已重启！"
