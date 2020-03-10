ps aux|grep python |grep -v grep|grep -v supervisord|awk '{print $2}'|xargs kill -9
