"""dao

Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from .model import Roles
from flask import current_app
from app.modules.rolesresources.model import RolesResources

class RolesDao(object):
    def delete(self, ids):
        """delete

        Args:
            ids (list): id list
            
        Returns:
            bool: True or False

        """
        result = False
        if ids:
            for id in ids :
                locked = self.locked(id)
                if locked :
                    raise Exception('object(id=%s) is locked'%(id))
            try:
                Roles.query.filter(Roles.id.in_(tuple(ids))).delete(synchronize_session=False)
                RolesResources.query.filter(RolesResources.rid.in_(tuple(ids))).delete(synchronize_session=False)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def addResources(self, rid, reids):
        """Setting Roles Corresponding Resources. # 增加与角色相关的资源

        According to the role rid and the corresponding resource list reids, the record is inserted into the RolesResources model.
        根据角色rid和相应的资源列表里，将记录插入到RolesResources模型中

        Args:
            rid (int): Roles id
            reids (str): Resources id list string, for example : 3,5,7

        Returns:
            bool: True or False

        """
        result = False
        if rid and reids:
            reids_list = reids.split(",")
            try:
                RolesResources.query.filter(RolesResources.rid==rid).delete(synchronize_session=False)
                for reid in reids_list:
                    rolesResources = RolesResources(rid=rid, reid = reid)
                    db.session.add(rolesResources)
                db.session.commit()
                result = True
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
        return result

    def add(self, args):
        """add

        Args:
            args (collections.OrderedDict): request args
            
        Returns:
            object : Roles object

        """
        roles = None
        reids = args.get('resources')
        try:
            roles = Roles(**args)
            db.session.add(roles)
            db.session.flush()
            if roles:
                rid = roles.id
                if rid and reids:
                    reids_list = reids.split(",")
                    RolesResources.query.filter(RolesResources.rid==rid).delete(synchronize_session=False)
                    db.session.flush()
                    for reid in reids_list:
                        rolesResources = RolesResources(rid=rid, reid = reid)
                        db.session.add(rolesResources)
                        db.session.flush()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return roles

    def edit(self, args):
        """edit

        Args:
            args (collections.OrderedDict): request args

        Returns:
            object: Roles object

        """
        rid = args.pop('id')
        reids = args.get('resources')
        record = Roles.query.get(rid)
        if record :
            try:
                for k,v in args.items():
                    setattr(record,k,v)
                # self.addResources(id,resources)
                db.session.flush()
                if rid and reids:
                    reids_list = reids.split(",")
                    RolesResources.query.filter(RolesResources.rid==rid).delete(synchronize_session=False)
                    db.session.flush()
                    for reid in reids_list:
                        rolesResources = RolesResources(rid=rid, reid = reid)
                        db.session.add(rolesResources)
                        db.session.flush()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)            
        return record

    def getById(self, id):
        """view

        view condition: id

        Args:
            id (int): id
            
        Returns:
            object: Resources object

        """
        record = Roles.query.get(id)
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
            pages = Roles.query.filter(Roles.id.in_(ids)).paginate(page, limit)
            if pages:
                for item in pages.items:
                    lst.append(item)
                data =  {"rows": lst, "total":pages.total}
            return data
        if search.strip() != '' :
            temp_query_obj = Roles.query.filter(Roles.title.like("%{search}%".format(search=search))) 
        if sort.strip() != "" and temp_query_obj == None:
            temp_query_obj = Roles.query.order_by(eval("Roles."+sort+"."+order+"()"))
        if sort.strip() != "" and temp_query_obj != None: 
            temp_query_obj = temp_query_obj.order_by(eval("Roles."+sort+"."+order+"()"))
        if temp_query_obj == None :
            pages = Roles.query.order_by(Roles.pid.asc()).order_by(Roles.weight.desc()).paginate(page, limit)
        else :
            pages = temp_query_obj.paginate(page, limit)
        
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getMenu(self):
        """view menu menu

        condition: Roles.status==1

        Args:
            
            
        Returns:
            list: Roles object list
        """
        menu = None
        menu = Roles.query.filter(Roles.status==1).order_by(Roles.pid.asc()).order_by(Roles.weight.desc()).all()
        return menu

    def locked(self, id):
        """locked # 锁定，无法正常删除

        Args:
            id (int): id
            
        Returns:
            bool: True or False

        """
        result = False
        # Get module info
        record = self.getById(id)  
        if not record:
             raise Exception('object(id=%s) is null'%id)
        if record.locked == 1 :
            result = True
        return result

    def getTreeInfo(self, id):
        """get tree weight info with roles id  # 通过角色ID获取该条角色的树形权重信息，包括树路径、树深度和树路径权重

        Args:
            id (int): id
            
        Returns:
            dict: dict result, for example: {'treepath':'.25.26.', 'treegrade':2, 'treepathweight':'.9999998999.0000000025.9999999099.0000000026.'}

        """
        result = {}
        weight_base = 10000000
        # Get module info
        record = self.getById(id) 
        if not record :
            raise Exception('object(id=%s) is null'%id)
        id = record.id
        pid = record.pid
        weight = weight_base - record.weight
        treepath = ''
        treegrade = 1
        treepathweight = ''
        while pid!=0 :
            treegrade += 1
            treepath = '.' + str(pid) + treepath
            record_temp = self.getById(pid) 
            if not record_temp :
                raise Exception('object(id=%s) is null'%id)
            weight_temp = weight_base - record_temp.weight
            treepathweight = '.' + str(weight_temp) + '.' + str(pid) + treepathweight
            pid = record_temp.pid                       
        treepath = treepath + '.' + str(id) + '.'
        treepathweight = treepathweight + '.' + str(weight) + '.' + str(id) + '.'
        result['treepath'] = treepath
        result['treegrade'] = treegrade
        result['treepathweight'] = treepathweight
        return result

    def setTreeInfoWithAllRecord(self):
        """update all record tree info ,include treepath ,treegrade and treepathweight # 更新所有记录树形信息，包括树路径、树深度和树路径权重

        Args:
           

        Returns:
            void: void

        """
        try:
            records = Roles.query.all()
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

