"""dao

Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from .model import Resources
from flask import current_app
from sqlalchemy import distinct
from app.modules.roles.model import Roles
from app.modules.adminroles.model import AdminRoles
from app.modules.rolesresources.model import RolesResources
from sqlalchemy import func

class ResourcesDao(object):
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
                Resources.query.filter(Resources.id.in_(tuple(ids))).delete(synchronize_session=False)
                db.session.flush()
                for id in ids :
                    current_app.logger.debug(id)
                    rolesResources = RolesResources.query.filter(RolesResources.reid==id).all()
                    RolesResources.query.filter(RolesResources.reid==id).delete(synchronize_session=False)
                    db.session.flush()
                    for rolesResource in rolesResources:
                        role = Roles.query.get(rolesResource.rid)
                        if role:
                            resources_list = eval('[' + role.resources + ']')
                            current_app.logger.debug(str(resources_list))
                            resources_list.remove(id)
                            resources_str = str(resources_list)[1:len(str(resources_list))-1]
                            role.resources = resources_str
                            db.session.flush()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result                   

    def add(self, args):
        """add

        Args:
            args (collections.OrderedDict): request args
            
        Returns:
            object : Resources object

        """
        record = None
        try:
            record = Resources(**args)
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
            args (collections.OrderedDict): request args

        Returns:
            object: Resources object

        """
        id = args.pop('id')
        record = Resources.query.get(id)
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

    def getById(self, id):
        """view

        view condition: id

        Args:
            id (int): id
            
        Returns:
            object: Resources object

        """
        record = Resources.query.get(id)
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
        if search.strip() != '' :
            temp_query_obj = Resources.query.filter(Resources.title.like("%{search}%".format(search=search)))
        if sort.strip() != "" and temp_query_obj == None:
            temp_query_obj = Resources.query.order_by(eval("Resources."+sort+"."+order+"()"))
        if sort.strip() != "" and temp_query_obj != None: 
            temp_query_obj = temp_query_obj.order_by(eval("Resources."+sort+"."+order+"()"))
        if temp_query_obj == None :
            # pages = Resources.query.order_by(Resources.pid.asc()).order_by(Resources.weight.desc()).paginate(page, limit)
            pages = Resources.query.order_by(Resources.treepathweight.asc()).paginate(page, limit)
        else :
            pages = temp_query_obj.paginate(page, limit)
        lst = []
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getMenu(self):
        """view resources menu # 获取资源排序菜单
 
        condition: Resources.ismenu==1, Resources.status==1

        Args:
            
            
        Returns:
            list: Resources object list
        """
        resources = None
        resources = Resources.query.filter(Resources.ismenu==1, Resources.status==1).order_by(Resources.pid.asc()).order_by(Resources.weight.desc()).all()
        return resources

    def getAll(self):
        """view all resources # 获取所有资源

        condition: Resources.status==1

        Args:
            
            
        Returns:
            list: Resources object list
        """
        resources = None
        resources = Resources.query.filter(Resources.status==1).order_by(Resources.pid.asc()).order_by(Resources.weight.desc()).all()
        return resources

    def getRoutes(self, uid):
        """Get user resources with uid # 通过用户ID获取该用户所属角色有权限访问路由列表

        first get user roles with uid (AdminRoles relation object), second get user resources id with rid (Roles.resources), three get resources detail info with resources id

        Args:
            uid (int): admin id            
            
        Returns:
            list: Resources list

        """
        resources_ids_list = []
        roles = db.session.query(Roles.id.label('rid') , Roles.title.label('title'), Roles.resources.label('resources')). \
            filter(Roles.status == 1). \
            filter(Roles.id == AdminRoles.rid). \
            filter(AdminRoles.uid == uid). \
            order_by(Roles.weight.desc()). \
            all()   
        if roles :
            for role in roles :
                resources_ids_list = resources_ids_list + eval('['+role.resources+']')
        resources = None
        resources = Resources.query.filter(Resources.status==1, Resources.ismenu==1, Resources.id.in_(tuple(set(resources_ids_list)))).order_by(Resources.pid.asc()).order_by(Resources.weight.desc()).all()
        return resources

    def getWeightMax(self):
        """Get Weight Max Value # 获取最大权重

        Args:
            
            
        Returns:
            int: Weight Max Value

        """
        record = Resources.query.with_entities(func.max(Resources.weight).label('weight')).first()
        return record

    def getWeightMinUnderPid(self, pid):
        """Get Weight Min Value Under Pid # 获取某个父ID下最小权重

        Args:
            
            
        Returns:
            int: Weight Min Value Under Pid

        """
        weight = 0
        record = Resources.query.with_entities(func.min(Resources.weight).label('weight')).filter(Resources.pid==pid).first()
        if record[0] == None:
            current_app.logger.debug(str(record))
            record = self.getById(pid)
            weight = record.weight
        else :
            weight = record[0]
        return int(weight)

    def locked(self, id):
        """is locked # 是否锁定，锁定后不充许直接删除

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
        """get tree weight info with resource id  # 通过资源ID获取该条资源的树形权重信息，包括树路径、树深度和树路径权重

        Args:
            id (int): resource id # 资源ID
            
        Returns:
            dict: dict result, for example: {'treepath':'.25.26.', 'treegrade':2, 'treepathweight':'.9999998999.0000000025.9999999099.0000000026.'}

        """
        result = {}
        weight_base = 9999999999
        weight_base_len = 10
        # Get module info
        record = self.getById(id) 
        if not record :
            raise Exception('object(id=%s) is null'%id)
        id = record.id
        id_str = '0' * (weight_base_len - len(str(id))) + str(id)
        pid = record.pid
        weight = record.weight
        weight_str = '0' * (weight_base_len - len(str(weight_base-weight))) + str(weight_base-weight)
        treepath = ''
        treegrade = 1
        treepathweight = ''
        while pid!=0 :
            treegrade += 1
            treepath = '.' + str(pid) + treepath
            record_temp = self.getById(pid) 
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
        """update all record tree info ,include treepath ,treegrade and treepathweight # 更新所有记录树形信息，包括树路径、树深度和树路径权重

        Args:
           

        Returns:
            void: void

        """
        try:
            records = Resources.query.all()
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


