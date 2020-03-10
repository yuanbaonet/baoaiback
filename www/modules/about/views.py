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
from . import about

@about.route('/about', methods=['GET','POST'])
def index():
	baoai = {}
	baoai['title'] = 'BaoAI'
	return render_template('about/index.html',baoai=baoai)



