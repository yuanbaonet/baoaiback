"""

RESTful API Category resource

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-04 10:04:19
"""

from app import db
from flask import current_app,request
from app.common.schema import *
from app.common.param import *
from app.common.wrap import *
from flask_restplus_patched import Resource, Namespace, abort, HTTPStatus
from sqlalchemy import or_
from .model import *
from .schema import *
from .param import *
from .dao import *

ns = Namespace("category", description="RESTful API Category resource")

@ns.route("/")
class CategoryAPI(Resource):
    """
    Category module resource main service: add/delete/edit/view
    """
    @auth()
    @ns.parameters(CategoryParameters(dump_only=['id']))
    @ns.response(CategorySchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        record = None
        categoryDao = CategoryDao()
        try:
            record = categoryDao.add(args)
        except Exception as e:
            abort(500, e)       
        return record

    @auth()
    @ns.parameters(CategoryParameters())
    @ns.response(CategorySchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        categoryDao = CategoryDao()            
        try:
            record = categoryDao.edit(args)
        except Exception as e:
            abort(500, e)        
        return record

    @auth()
    @ns.parameters(IDSParameters())
    @ns.response(BasicSchema(many=False))
    def delete(self, args):
        """
        delete
        """
        result = False
        ids = args.get('ids')
        categoryDao = CategoryDao()     
        try:
            result = categoryDao.delete(ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

    # @auth()
    @ns.parameters(IDParameters())
    @ns.response(CategorySchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        view
        """
        record = None
        categoryDao = CategoryDao() 
        id = args.get('id')
        record = categoryDao.getById(id)  
        return record

@ns.route("/list")
class CategoryListAPI(Resource):
    """
    Category module resource list service
    """
    @auth()
    @ns.parameters(ExtendPagerParameters())
    @ns.response(CategoryListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        view list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        args.setdefault('lang','')
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        lang = args.pop('lang')

        categoryDao = CategoryDao() 
        
        #args.setdefault('articles',0)
        #articles = args.pop('articles')
        # data = categoryDao.getListByLangAndArticles(search, sort, order, offset, limit, lang, articles)
        data = categoryDao.getListByLang(search, sort, order, offset, limit, lang)
        
        return data

@ns.route("/books_list")
class CategoryBookListAPI(Resource):
    """
    Book Category list service
    """
    # @auth()
    @ns.parameters(ExtendPagerParameters())
    @ns.response(CategoryListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        view list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        args.setdefault('lang','')
        args.setdefault('books_category_id',0)
        args.setdefault('is_book',False)
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        lang = args.pop('lang')
        books_category_id = args.pop('books_category_id')
        is_book = args.pop('is_book')
        categoryDao = CategoryDao() 
        
        #args.setdefault('articles',0)
        #articles = args.pop('articles')
        # data = categoryDao.getListByLangAndArticles(search, sort, order, offset, limit, lang, articles)
        data = categoryDao.getBooksListByLang(search, sort, order, offset, limit, lang, books_category_id, is_book)        
        return data

@ns.route("/news_list")
class CategoryNewsListAPI(Resource):
    """
    Book Category list service
    """
    @auth()
    @ns.parameters(NewsExtendPagerParameters())
    @ns.response(CategoryListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        view list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        args.setdefault('lang','')
        args.setdefault('news_category_id',0)
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        lang = args.pop('lang')
        news_category_id = args.pop('news_category_id')
        categoryDao = CategoryDao() 
        
        #args.setdefault('articles',0)
        #articles = args.pop('articles')
        # data = categoryDao.getListByLangAndArticles(search, sort, order, offset, limit, lang, articles)
        data = categoryDao.getNewsListByLang(search, sort, order, offset, limit, lang, news_category_id)        
        return data

@ns.route("/nav_list")
class CategoryNavListAPI(Resource):
    """
    Nav Category list service
    """
    # @auth()
    @ns.parameters(ExtendPagerParameters())
    @ns.response(CategoryListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        view list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        args.setdefault('lang','')
        args.setdefault('nav_category_id',0)
        args.setdefault('is_main',False)
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        lang = args.pop('lang')
        nav_category_id = args.pop('nav_category_id')
        is_main = args.pop('is_main')
        categoryDao = CategoryDao() 
        
        #args.setdefault('articles',0)
        #articles = args.pop('articles')
        # data = categoryDao.getListByLangAndArticles(search, sort, order, offset, limit, lang, articles)
        data = categoryDao.getNavListByLang(search, sort, order, offset, limit, lang, nav_category_id, is_main)        
        return data

@ns.route("/menu")
class CategoryMenuAPI(Resource):
    @auth()
    @ns.parameters(LangParameters())
    @ns.response(CategorySchema(only=['id', 'pid', 'title'], many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        Category Module Tree Menu (status=1) # 分类树形排序菜单
        """
        args.setdefault('lang','')
        lang = args.pop('lang')
        categoryDao = CategoryDao()
        menu = categoryDao.getMenu(lang)
        return menu

@ns.route("/books_menu")
class CategoryBooksMenuAPI(Resource):
    #@auth()
    @ns.parameters(LangParameters())
    @ns.response(CategorySchema(only=['id', 'pid', 'title'], many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        Books Tree Menu # 获取手册菜单树形排序第一级子菜单
        """
        args.setdefault('lang','')
        lang = args.pop('lang')
        categoryDao = CategoryDao()
        menu = categoryDao.getBooksMenu(lang)
        return menu

@ns.route("/news_menu")
class CategoryBooksMenuAPI(Resource):
    #@auth()
    @ns.parameters(LangParameters())
    @ns.response(CategorySchema(only=['id', 'pid', 'title'], many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        News Tree Menu # 获取新闻菜单树形排序第一级子菜单
        """
        args.setdefault('lang','')
        lang = args.pop('lang')
        categoryDao = CategoryDao()
        menu = categoryDao.getNewsMenu(lang)
        return menu

@ns.route("/nav_menu")
class CategoryNavMenuAPI(Resource):
    #@auth()
    @ns.parameters(LangParameters())
    @ns.response(CategorySchema(only=['id', 'pid', 'title'], many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        News Navigation Menu # 获取导航条树形排序第一级子菜单
        """
        args.setdefault('lang','')
        lang = args.pop('lang')
        categoryDao = CategoryDao()
        menu = categoryDao.getNavMenu(lang)
        return menu

@ns.route("/nav_menu_all")
class CategoryNavMenuAllAPI(Resource):
    #@auth()
    @ns.parameters(LangParameters())
    @ns.response(CategorySchema(only=['id', 'pid', 'title', 'link_type', 'inner_link', 'link_target', 'link', 'block_link', 'article_link', 'route_link'], many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        Category Module Navigation Tree Menu (status=1) # 所有导航分类树形排序菜单
        """
        args.setdefault('lang','')
        lang = args.pop('lang')
        categoryDao = CategoryDao()
        menu = categoryDao.getNavMenuAll(lang)
        return menu

@ns.route("/reorder")
class CategoryReorderAPI(Resource):
    @auth()
    @ns.response(BasicSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        Sort by tree # 分类重新树形排序
        """
        result = True
        categoryDao = CategoryDao()
        try:
            categoryDao.setTreeInfoWithAllRecord()
        except Exception as e:
            abort(500, e)
        return {"status":result}

        
