"""

Category Module Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-04 10:04:19
"""

from app import db, Config
from .model import *
from flask import current_app
from sqlalchemy import or_
from collections import OrderedDict
from ..attachments.model import *

class CategoryDao(object):
    def delete(self, ids):
        """delete

        Args:
            ids (list): id list
            
        Returns:
            bool: True or False

        """
        result = False
        if ids:
            try:
                Category.query.filter(Category.id.in_(tuple(ids))).delete(synchronize_session=False)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def add(self, args):
        """add

        Args:
            args (OrderedDict): form args
            
        Returns:
            object: Category object

        """
        record = None
        try:
            record = Category(**args)
            db.session.add(record)
            db.session.flush()
            id = record.id
            result = self.getTreeInfo(id)
            record.treegrade = result['treegrade']
            record.treepath = result['treepath']
            record.treepathweight = result['treepathweight']                
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return record

    def edit(self, args):
        """edit

        Args:
            args (OrderedDict): form args

        Returns:
            object: Category object

        """
        id = args.pop('id')
        record = Category.query.get(id)
        if record :
            try:
                for k,v in args.items():
                    setattr(record,k,v)
                result = self.getTreeInfo(id)
                record.treegrade = result['treegrade']
                record.treepath = result['treepath']
                record.treepathweight = result['treepathweight']                        
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)            
        return record

    def _getById(self, id):
        """view by id

        Args:
            id (int): id
            
        Returns:
            object: Category object

        """
        record = Category.query.get(id)
        return record

    def getById(self, id):
        """view by id

        Args:
            id (int): id
            
        Returns:
            object: Category object

        """
        record = Category.query.get(id)
        if record :
            try:
                if not record.views :
                    record.views = 0
                record.views = record.views + 1
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e) 
        return record

    def getList(self, search, sort, order, offset, limit):
        """view list

        condition: pagination

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []

        if search.startswith( 'id=' ) and len(search)>3 :
            ids = search[3:]
            ids = eval('['+ids+']')
            pages = Category.query.filter(Category.id.in_(ids)).paginate(page, limit)
            if pages:
                for item in pages.items:
                    lst.append(item)
                data =  {"rows": lst, "total":pages.total}
            return data
        temp_query_obj = Category.query
        if search.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Category.title.like("%{search}%".format(search=search)))
        if sort.strip() != '' :
            temp_query_obj = temp_query_obj.order_by(eval("Category."+sort+"."+order+"()"))
        if search.strip() == '' and sort.strip() == '' :
            pages = temp_query_obj.order_by(Category.treepathweight.asc()).paginate(page, limit)
        else :
            pages = temp_query_obj.paginate(page, limit)
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getListByLang(self, search, sort, order, offset, limit, lang):
        """view list

        condition: pagination by lang

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            lang (str): language
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []
        if search.startswith( 'id=' ) and len(search)>3 :
            ids = search[3:]
            ids = eval('['+ids+']')
            Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
            query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
            pages = query_obj.filter(Category.id.in_(ids)).filter(Category.lang.in_((lang, 'all'))).paginate(page, limit)
            if pages:
                for item in pages.items:
                    lst.append(item)
                data =  {"rows": lst, "total":pages.total}
            return data
        Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
        query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
        if lang.strip() != '' :
            query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))
        if search.strip() != '' :
            query_obj = query_obj.filter(Category.title.like("%{search}%".format(search=search)))
        if sort.strip() != '' :
            query_obj = query_obj.order_by(eval("Category."+sort+"."+order+"()"))
        if search.strip() == '' and sort.strip() == '' :
            pages = query_obj.order_by(Category.treepathweight.asc()).paginate(page, limit)
        else :
            pages = query_obj.paginate(page, limit)
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getBooksListByLang(self, search, sort, order, offset, limit, lang, books_category_id, is_book):
        """view list

        condition: pagination by lang

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            lang (str): language
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        # Category id of books
        # books_category_id = 6
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []
        if not books_category_id :
            books_category_id = 6
        if books_category_id == 6 :
            if search.startswith( 'id=' ) and len(search)>3 :
                ids = search[3:]
                ids = eval('['+ids+']')
                Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
                query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
                
                query_obj = query_obj.filter(Category.treepath.like(".{books_category_id}.%".format(books_category_id=books_category_id))).filter(Category.id!=books_category_id).filter(Category.id.in_(ids)).filter(Category.lang.in_((lang, 'all')))
                if is_book :
                    query_obj = query_obj.filter(Category.treegrade==2)
                pages = query_obj.paginate(page, limit)  
                if pages:
                    for item in pages.items:
                        lst.append(item)
                    data =  {"rows": lst, "total":pages.total}
                return data
            Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
            query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id).filter(Category.treepath.like(".{books_category_id}.%".format(books_category_id=books_category_id))).filter(Category.id!=books_category_id)
            if lang.strip() != '' :
                query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))
            if search.strip() != '' :
                query_obj = query_obj.filter(Category.title.like("%{search}%".format(search=search)))
            if is_book :
                query_obj = query_obj.filter(Category.treegrade==2)
            if sort.strip() != '' :
                query_obj = query_obj.order_by(eval("Category."+sort+"."+order+"()"))
            if search.strip() == '' and sort.strip() == '' :
                pages = query_obj.order_by(Category.treepathweight.asc()).paginate(page, limit)
            else :
                pages = query_obj.paginate(page, limit)
        else :
            if search.startswith( 'id=' ) and len(search)>3 :
                ids = search[3:]
                ids = eval('['+ids+']')
                Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
                query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
                pages = query_obj.filter(Category.pid==books_category_id).filter(Category.id.in_(ids)).filter(Category.lang.in_((lang, 'all'))).paginate(page, limit)
                if pages:
                    for item in pages.items:
                        lst.append(item)
                    data =  {"rows": lst, "total":pages.total}
                return data
            Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
            query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id).filter(Category.pid==books_category_id)
            if lang.strip() != '' :
                query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))
            if search.strip() != '' :
                query_obj = query_obj.filter(Category.title.like("%{search}%".format(search=search)))
            if sort.strip() != '' :
                query_obj = query_obj.order_by(eval("Category."+sort+"."+order+"()"))
            if search.strip() == '' and sort.strip() == '' :
                pages = query_obj.order_by(Category.weight.desc()).order_by(Category.created.desc()).paginate(page, limit)
            else :
                pages = query_obj.paginate(page, limit)            
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getNavListByLang(self, search, sort, order, offset, limit, lang, nav_category_id, is_main):
        """view list

        condition: pagination by lang

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            lang (str): language
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        # Category id of books
        # books_category_id = 6
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []
        if not nav_category_id :
            nav_category_id = Config.NAV_CATEGORY_ROOT_ID
        if nav_category_id == Config.NAV_CATEGORY_ROOT_ID :
            if search.startswith( 'id=' ) and len(search)>3 :
                ids = search[3:]
                ids = eval('['+ids+']')
                Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
                query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
                
                query_obj = query_obj.filter(Category.treepath.like(".{nav_category_id}.%".format(nav_category_id=nav_category_id))).filter(Category.id!=nav_category_id).filter(Category.id.in_(ids)).filter(Category.lang.in_((lang, 'all')))
                if is_main :
                    query_obj = query_obj.filter(Category.treegrade==2)
                pages = query_obj.paginate(page, limit)  
                if pages:
                    for item in pages.items:
                        lst.append(item)
                    data =  {"rows": lst, "total":pages.total}
                return data
            Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
            query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id).filter(Category.treepath.like(".{nav_category_id}.%".format(nav_category_id=nav_category_id))).filter(Category.id!=nav_category_id)
            if lang.strip() != '' :
                query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))
            if search.strip() != '' :
                query_obj = query_obj.filter(Category.title.like("%{search}%".format(search=search)))
            if is_main :
                query_obj = query_obj.filter(Category.treegrade==2)
            if sort.strip() != '' :
                query_obj = query_obj.order_by(eval("Category."+sort+"."+order+"()"))
            if search.strip() == '' and sort.strip() == '' :
                pages = query_obj.order_by(Category.treepathweight.asc()).paginate(page, limit)
            else :
                pages = query_obj.paginate(page, limit)
        else :
            if search.startswith( 'id=' ) and len(search)>3 :
                ids = search[3:]
                ids = eval('['+ids+']')
                Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
                query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
                pages = query_obj.filter(Category.pid==nav_category_id).filter(Category.id.in_(ids)).filter(Category.lang.in_((lang, 'all'))).paginate(page, limit)
                if pages:
                    for item in pages.items:
                        lst.append(item)
                    data =  {"rows": lst, "total":pages.total}
                return data
            Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
            query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id).filter(Category.pid==nav_category_id)
            if lang.strip() != '' :
                query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))
            if search.strip() != '' :
                query_obj = query_obj.filter(Category.title.like("%{search}%".format(search=search)))
            if sort.strip() != '' :
                query_obj = query_obj.order_by(eval("Category."+sort+"."+order+"()"))
            if search.strip() == '' and sort.strip() == '' :
                pages = query_obj.order_by(Category.weight.desc()).order_by(Category.created.desc()).paginate(page, limit)
            else :
                pages = query_obj.paginate(page, limit)            
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getNewsListByLang(self, search, sort, order, offset, limit, lang, news_category_id):
        """view list

        condition: pagination by lang

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            lang (str): language
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        # Category id of books
        # books_category_id = 6
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []
        if not news_category_id :
            news_category_id = 1
        if news_category_id == 1 :
            if search.startswith( 'id=' ) and len(search)>3 :
                ids = search[3:]
                ids = eval('['+ids+']')
                Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
                query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
                pages = query_obj.filter(Category.treepath.like(".{news_category_id}.%".format(news_category_id=news_category_id))).filter(Category.id!=news_category_id).filter(Category.id.in_(ids)).filter(Category.lang.in_((lang, 'all'))).paginate(page, limit)
                if pages:
                    for item in pages.items:
                        lst.append(item)
                    data =  {"rows": lst, "total":pages.total}
                return data
            Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
            query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id).filter(Category.treepath.like(".{news_category_id}.%".format(news_category_id=news_category_id))).filter(Category.id!=news_category_id)
            if lang.strip() != '' :
                query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))
            if search.strip() != '' :
                query_obj = query_obj.filter(Category.title.like("%{search}%".format(search=search)))
            if sort.strip() != '' :
                query_obj = query_obj.order_by(eval("Category."+sort+"."+order+"()"))
            if search.strip() == '' and sort.strip() == '' :
                pages = query_obj.order_by(Category.treepathweight.asc()).paginate(page, limit)
            else :
                pages = query_obj.paginate(page, limit)
        else :
            if search.startswith( 'id=' ) and len(search)>3 :
                ids = search[3:]
                ids = eval('['+ids+']')
                Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
                query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
                pages = query_obj.filter(Category.pid==news_category_id).filter(Category.id.in_(ids)).filter(Category.lang.in_((lang, 'all'))).paginate(page, limit)
                if pages:
                    for item in pages.items:
                        lst.append(item)
                    data =  {"rows": lst, "total":pages.total}
                return data
            Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
            query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.weight, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.content, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.link, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id).filter(Category.pid==news_category_id)
            if lang.strip() != '' :
                query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))
            if search.strip() != '' :
                query_obj = query_obj.filter(Category.title.like("%{search}%".format(search=search)))
            if sort.strip() != '' :
                query_obj = query_obj.order_by(eval("Category."+sort+"."+order+"()"))
            if search.strip() == '' and sort.strip() == '' :
                pages = query_obj.order_by(Category.weight.desc()).order_by(Category.created.desc()).paginate(page, limit)
            else :
                pages = query_obj.paginate(page, limit)            
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data                    

    def getMenu(self, lang):
        """Category Module Tree Menu # 分类树形排序菜单

        condition: Category.status==1

        Args:
            lang (str): language  
            
        Returns:
            list: Category object list
        """
        menu = None
        query_obj = Category.query.filter(Category.status==1)
        if lang.strip() != '' :
            query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))  
        menu = query_obj.order_by(Category.pid.asc()).order_by(Category.weight.desc()).all()
        return menu

    def getBooksMenu(self, lang):
        """Category Module Books Menu：first submenu # 手册分类第一级菜单

        condition: Category.status==1

        Args:
            lang (str): language
            
        Returns:
            list: Category object list
        """
        books_category_id = Config.BOOK_CATEGORY_ROOT_ID
        menu = None
        query_obj = Category.query.filter(Category.status==1).filter(Category.treepath.like(".{books_category_id}.%".format(books_category_id=books_category_id))).filter(Category.treegrade==2)
        if lang.strip() != '' :
            query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))  
        menu = query_obj.order_by(Category.pid.asc()).order_by(Category.weight.desc()).all() 
        return menu

    def getNewsMenu(self, lang):
        """Category Module News Menu：first submenu # 新闻分类第一级子菜单

        condition: Category.status==1

        Args:
            lang (str): language
            
        Returns:
            list: Category object list
        """
        news_category_id = Config.NEWS_CATEGORY_ROOT_ID
        menu = None
        query_obj = Category.query.filter(Category.status==1).filter(Category.treepath.like(".{news_category_id}.%".format(news_category_id=news_category_id))).filter(Category.treegrade==2)
        if lang.strip() != '' :
            query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))  
        menu = query_obj.order_by(Category.pid.asc()).order_by(Category.weight.desc()).all() 
        return menu

    def getNavMenu(self, lang):
        """Category Module Nav Menu：first submenu # 导航分类第一级子菜单

        condition: Category.status==1 and treegrade==2

        Args:
            lang (str): language
            
        Returns:
            list: Category object list
        """
        nav_category_id = Config.NAV_CATEGORY_ROOT_ID
        menu = None
        query_obj = Category.query.filter(Category.status==1).filter(Category.treepath.like(".{nav_category_id}.%".format(nav_category_id=nav_category_id))).filter(Category.treegrade==2)
        if lang.strip() != '' :
            query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))  
        menu = query_obj.order_by(Category.pid.asc()).order_by(Category.weight.desc()).all() 
        return menu

    def getNavMenuAll(self, lang):
        """Category Module Nav Menu # 导航分类所有菜单

        condition: Category.status==1

        Args:
            lang (str): language
            
        Returns:
            list: Category object list
        """
        nav_category_id = Config.NAV_CATEGORY_ROOT_ID
        menu = None
        query_obj = Category.query.filter(Category.status==1).filter(Category.treepath.like(".{nav_category_id}.%".format(nav_category_id=nav_category_id)))
        if lang.strip() != '' :
            query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))  
        menu = query_obj.order_by(Category.pid.asc()).order_by(Category.weight.desc()).all() 
        return menu

    def getTreeInfo(self, id):
        """
        Get  tree info with id # 通过ID得到树信息

        Args:
            id (int): id
            
        Returns:
            dict: dict result, for example: {'treepath':'.2.180', 'treegrade':2, 'treepathweight':'.6000.2.5000.180'}

        """
        result = {}
        weight_base = 9999999999
        weight_base_len = 10
        # Get module info
        record = self._getById(id) 
        if not record :
            raise Exception('object(id=%s) is null'%id)
        id = record.id
        id_str = '0' * (weight_base_len - len(str(id))) + str(id)
        pid = record.pid
        weight = record.weight
        if not weight :
          weight = 0
        weight_str = '0' * (weight_base_len - len(str(weight_base-weight))) + str(weight_base-weight)
        treepath = ''
        treegrade = 1
        treepathweight = ''
        while pid!=0 :
            treegrade += 1
            treepath = '.' + str(pid) + treepath
            record_temp = self._getById(pid) 
            if not record_temp :
                raise Exception('object(id=%s) is null'%id)
            weight_temp = record_temp.weight
            pid_str = '0' * (weight_base_len - len(str(pid))) + str(pid)
            weight_temp_str = '0' * (weight_base_len - len(str(weight_base-weight_temp))) + str(weight_base-weight_temp)
            treepathweight = '.' + weight_temp_str + '.' + pid_str + treepathweight
            pid = record_temp.pid           
            
        treepath = treepath + '.' + str(id) + '.'
        treepathweight = treepathweight + '.' + weight_str + '.' + id_str + '.'
        result['treepath'] = treepath
        result['treegrade'] = treegrade
        result['treepathweight'] = treepathweight
        return result

    def setTreeInfoWithAllRecord(self):
        """update all record tree info ,include treepath, treegrade and treepathweight # 更新所有记录树信息

        Args:
            

        Returns:
            void: void

        """
        try:
            records = Category.query.all()
            for record in records :
                id = record.id
                result = self.getTreeInfo(id)
                record.treegrade = result['treegrade']
                record.treepath = result['treepath']
                record.treepathweight = result['treepathweight']
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def getListByBlock(self, search, sort, order, offset, limit, lang, category, customquery):
            """view list

            condition: pagination by lang

            Args:
                search (str): search field, default is title field
                sort (str): sort field
                order (str): order type (asc/desc), default is asc
                offset (int): Paging offset
                limit (int): Maximum number of records per page
                lang (str): language
                category (int): refer to category's id
                customquery (str): custom query
                
            Returns:
                object: data, for example: {"rows": lst, "total":pages.total}

            """
            data = {}
            page = offset // limit + 1
            temp_query_obj = None
            pages = None
            lst = []
            if search.startswith( 'id=' ) and len(search)>3 :
                ids = search[3:]
                ids = eval('['+ids+']')
                Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
                query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
                pages = query_obj.filter(Category.id.in_(ids)).filter(Category.lang.in_((lang, 'all'))).paginate(page, limit)
                if pages:
                    for item in pages.items:
                        lst.append(item)
                    data =  {"rows": lst, "total":pages.total}
                return data
            Attachments_subquery = db.session.query(Attachments.module_obj_id,Attachments.module_name,Attachments.url).filter(Attachments.module_name=='category' , Attachments.iscover==1).subquery()
            query_obj =db.session.query(Category.id, Category.pid, Category.status, Category.created, Category.updated, Category.lang, Category.uid, Category.title, Category.alias, Category.keywords, Category.summary, Category.treepath, Category.treegrade, Category.treepathweight, Category.link_type, Category.articles, Category.article_link, Category.block_link, Category.inner_link, Category.ismenu, Category.link_target, Category.route_link, Attachments_subquery.c.url.label('cover')).outerjoin(Attachments_subquery, Category.id==Attachments_subquery.c.module_obj_id)
            if lang.strip() != '' :
                query_obj = query_obj.filter(Category.lang.in_((lang, 'all')))
            if search.strip() != '' :
                query_obj = query_obj.filter(Category.title.like("%{search}%".format(search=search)))
            if sort.strip() != '' :
                query_obj = query_obj.order_by(eval("Category."+sort+"."+order+"()"))
            if category :
                query_obj = query_obj.filter(Category.id.in_(eval('['+category+']')))
            if customquery.strip() :
                query_obj = eval(customquery.strip())
            pages = query_obj.paginate(page, limit)
            if pages:
                for item in pages.items:
                    lst.append(item)
                data =  {"rows": lst, "total":pages.total}
            return data

    def getSubTreeList(self, id):
        """
        update tree info with id # 获取子树信息

        Args:
            id (int): id
            
        Returns:
            dict: dict result, for example: {'treepath':'.2.180', 'treegrade':2, 'treepathweight':'.6000.2.5000.180'}

        """
        result = None
        record = self.getById(id)
        if not record :
            return result
        treepath = record.treepath
        result = Category.query.filter(Category.treepath.like("{treepath}%".format(treepath=treepath))).order_by(Category.treepathweight.asc()).all()
        return result

    def getListByCategoryAndField(self, category, field):
        """get field list with category # 使用分类id获取子类列表，列表字段是field变量指定和title

        Args:
            category (int): category
            field (str): field
            
        Returns:
            list: one field values list

        """
        lst = []
        records = db.session.query(eval("Category.%s.label('field')"%field), Category.title).filter(Category.pid==category).all()        
        return records 

        