"""configs

Init views module

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""
from flask import render_template,url_for,redirect,flash,current_app,\
		request,abort, make_response
from . import main
from flask_sqlalchemy import get_debug_queries

@main.after_app_request
def after_request(response):
	for query in get_debug_queries():
		if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
			current_app.logger.warning(
				'Slow query: %s\nParameters:%s\nDuration:%fs\nContext: %s\n'
						%(query.statement, query.parameters, query.duration, query.context))			
	return response

@main.route('/', methods=['GET','POST'])
def index():
	baoai = {}
	baoai['title'] = 'BaoAI'
	return render_template('main/index.html',baoai=baoai)



