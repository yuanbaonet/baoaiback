# deploy文件夹

存放本工程的配置文件

- `gunicorn_config.py`：gunicorn配置文件
- `baoai.ini`：BaoAI API服务的supervisor配置文件
- `beat.ini`：开启celery定时任务调度的supervisor配置文件
- `worker.ini`：启动celery的supervisor配置文件
- `nginx.conf`：前端Web服务器nginx配置文件，包含反向代理后端的API服务


