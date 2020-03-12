"""dao

Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from .model import Attachments
from flask import current_app
from sqlalchemy import distinct
from datetime import datetime
import uuid
import os
from app.modules.admin.model import *
from app.modules.admin.dao import *
from app.modules.category.dao import *
import requests

class AttachmentsDao(object):
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
                Attachments.query.filter(Attachments.id.in_(tuple(ids))).delete(synchronize_session=False)
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
            object: Attachments object

        """
        attachments = None
        try:
            attachments = Attachments(**args)
            db.session.add(attachments)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return attachments

    def edit(self, args):
        """edit

        Args:
            args (OrderedDict): form args

        Returns:
            object: Attachments object

        """
        id = args.pop('id')
        record = Attachments.query.get(id)
        if record :
            try:
                for k,v in args.items():
                    setattr(record,k,v)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)            
        return record

    def getById(self, id):
        """view by id

        Args:
            id (int): id
            
        Returns:
            object: Attachments object

        """
        record = Attachments.query.get(id)
        return record

    def getList(self, search, sort, order, offset, limit, lang, module_name, module_obj_id, category_id):
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
        if search.startswith( 'id=' ) and len(search)>len('id=') :
            ids = search[len('id='):]
            ids = eval('['+ids+']')
            pages = Attachments.query.filter(Attachments.id.in_(ids)).filter(Attachments.lang.in_((lang, 'all'))).paginate(page, limit)
            if pages:
                for item in pages.items:
                    lst.append(item)
                data =  {"rows": lst, "total":pages.total}
            return data
        temp_query_obj = Attachments.query
        if search.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Attachments.title.like("%{search}%".format(search=search)))
        if lang.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Attachments.lang.in_((lang, 'all')))     
        if sort.strip() != '' :
            temp_query_obj = temp_query_obj.order_by(eval("Attachments."+sort+"."+order+"()"))
        if module_name :
            temp_query_obj = temp_query_obj.filter(Attachments.module_name==module_name)
        if module_obj_id :
            temp_query_obj = temp_query_obj.filter(Attachments.module_obj_id==module_obj_id)
        if category_id :
            categoryDao = CategoryDao()
            records = categoryDao.getSubTreeList(category_id)
            category_ids = []
            if records :
                for record in records :
                    category_ids.append(record.id)
                temp_query_obj = temp_query_obj.filter(Attachments.category_id.in_(tuple(category_ids)))

        if search.strip() == '' and sort.strip() == '' :
            pages = temp_query_obj.order_by(Attachments.weight.desc()).order_by(Attachments.created.desc()).paginate(page, limit) 
        else :
            pages = temp_query_obj.paginate(page, limit)  
        lst = []
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data        

    def upload(self, uid, rfile, filesize, module_name, module_obj_id):
        """upload attachments

        Args:
            uid (int): user id
            rfile (object): request files # 请求文件对象
            filesize (int): file size
            module_name (str): module name # 模块名
            module_obj_id (int): module object id # 模块ID
        Returns:
            object: Attachmrents object

        """
        data = {}
        data['title'] = rfile.filename
        data['mimetype'] = rfile.mimetype
        data['filesize'] = filesize
        current_app.logger.debug(dir(rfile))
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        dt = datetime.now()
        dtlist = dt.strftime('%Y %m %d').split(' ')
        uuidstr = str(uuid.uuid4())
        uuidstr = ''.join(uuidstr.split('-'))
        data['uuid'] = uuidstr
        img_type_list = rfile.filename.rsplit(".", maxsplit=1)
        img_type = ""
        if len(img_type_list) == 2:
            img_type = img_type_list[1]
        data['imagetype'] = img_type
        data['isimage'] = False
        # gif,jpg,jpeg,bmp,png
        if img_type.lower() in ['gif','jpg','jpeg','bmp','png','ico'] :
            data['isimage'] = True
        main_path = os.path.join(UPLOAD_FOLDER, dtlist[0], dtlist[1], dtlist[2])
        url = "/".join([dtlist[0], dtlist[1], dtlist[2], uuidstr + "." + img_type])
        data['url'] = url
        data['admin_id'] = uid
        if  not os.path.exists(main_path): 
            os.makedirs(main_path)
        rfile.save(os.path.join(main_path, uuidstr + "." + img_type))
        attachments = None
        try:
            attachments = Attachments()
            attachments.admin_id = data['admin_id']
            attachments.url = data['url']
            attachments.title = data['title']
            attachments.mimetype = data['mimetype']
            attachments.filesize = data['filesize']
            attachments.uuid = data['uuid']
            attachments.imagetype = data['imagetype']
            attachments.isimage = data['isimage']
            if module_name :
                attachments.module_name = module_name
            if module_obj_id :
                attachments.module_obj_id = module_obj_id            
            db.session.add(attachments)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e) 
        return data

    def upload_avatar(self, uid, rfile, filesize):
        """upload avatar

        Args:
            uid (int): user id
            rfile (object): request files
            filesize (int): file size
            
        Returns:
            object: Attachmrents object

        """
        data = {}
        data['title'] = rfile.filename
        data['mimetype'] = rfile.mimetype
        data['filesize'] = filesize
        current_app.logger.debug(dir(rfile))
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        dt = datetime.now()
        dtlist = dt.strftime('%Y %m %d').split(' ')
        uuidstr = str(uuid.uuid4())
        uuidstr = ''.join(uuidstr.split('-'))
        data['uuid'] = uuidstr
        img_type_list = rfile.filename.rsplit(".", maxsplit=1)
        img_type = ""
        if len(img_type_list) == 2:
            img_type = img_type_list[1]
        data['imagetype'] = img_type
        main_path = os.path.join(UPLOAD_FOLDER, dtlist[0], dtlist[1], dtlist[2])
        url = "/".join([dtlist[0], dtlist[1], dtlist[2], uuidstr + "." + img_type])
        data['url'] = url
        data['admin_id'] = uid
        if  not os.path.exists(main_path):
            os.makedirs(main_path)
        rfile.save(os.path.join(main_path, uuidstr + "." + img_type))
        attachments = None
        admin = Admin.query.get(uid)
        if admin :
            try:
                admin.avatar = url
                db.session.add(admin)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e) 
        return data

    def ckeditor_browser_upload(self, uid, rfile, filename, filesize, module_name, module_obj_id):
        """ckeditor upload attachment # ckeditor上传附件

        Args:
            uid (int): user id
            rfile (object): request files
            filesize (int): file size
            module_name (str): module name # 模块名
            module_obj_id (int): module object id # 模块ID
            
        Returns:
            object: Attachmrents object

        """
        data = {}
        data['title'] = filename
        current_app.logger.debug('dir(rfile)')
        current_app.logger.debug(dir(rfile))
        data['mimetype'] = rfile.mimetype
        data['filesize'] = int(filesize)                
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        dt = datetime.now()
        dtlist = dt.strftime('%Y %m %d').split(' ')
        uuidstr = str(uuid.uuid4())
        uuidstr = ''.join(uuidstr.split('-'))
        data['uuid'] = uuidstr
        img_type_list = rfile.filename.rsplit(".", maxsplit=1)
        img_type = ""
        if len(img_type_list) == 2:
            img_type = img_type_list[1]
        data['imagetype'] = img_type
        data['isimage'] = False
        # gif,jpg,jpeg,bmp,png
        if img_type.lower() in ['gif','jpg','jpeg','bmp','png','ico'] :
            data['isimage'] = True
        main_path = os.path.join(UPLOAD_FOLDER, dtlist[0], dtlist[1], dtlist[2])
        url = "/".join([dtlist[0], dtlist[1], dtlist[2], uuidstr + "." + img_type])
        data['url'] = url
        data['admin_id'] = uid
        if  not os.path.exists(main_path): 
            os.makedirs(main_path)
        rfile.save(os.path.join(main_path, uuidstr + "." + img_type))
        attachments = None
        try:
            attachments = Attachments()
            attachments.admin_id = data['admin_id']
            attachments.url = data['url']
            attachments.title = data['title']
            attachments.mimetype = data['mimetype']
            attachments.filesize = data['filesize']
            attachments.uuid = data['uuid']
            attachments.imagetype = data['imagetype']
            attachments.isimage = data['isimage']
            if module_name :
                attachments.module_name = module_name
            attachments.module_obj_id = int(module_obj_id)          
            db.session.add(attachments)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e) 
        return data

    def getLocalImgURL(self, uid, remote_img_url):
        """Get Local Image URL # 获取本地图像URL

        Download image data through the image URL and save it locally, and return the locally saved URL
        通过图像的URL下载图像数据并保存至本地，返回本地保存的URL

        Args:
            uid (int): user id
            remote_img_url (str): remote image url # 远程图像URL
            
        Returns:
            object: Attachmrents object # 返回保存后的图像对象

        """
        data = {}
        if not remote_img_url :
            raise Exception('Image URL is NULL')
        if not uid :
            raise Exception('User ID is NULL')
        # imagetype and mimetype
        img_filename = ""
        img_filename_list = remote_img_url.rsplit("/", maxsplit=1)
        if len(img_filename_list) == 2:
            img_filename = img_filename_list[1]
            new_img_filename_list = img_filename.split("?")
            img_filename = new_img_filename_list[0]
        img_type_list = img_filename.rsplit(".", maxsplit=1)
        img_type = ""
        if len(img_type_list) == 2:
            img_type = img_type_list[1]
        data['imagetype'] = img_type
        data['mimetype'] = "image/" + img_type
        data['title'] = remote_img_url
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        dt = datetime.utcnow()
        dtlist = dt.strftime('%Y %m %d').split(' ')
        uuidstr = str(uuid.uuid4())
        uuidstr = ''.join(uuidstr.split('-'))
        data['uuid'] = uuidstr
        data['isimage'] = False
        # gif,jpg,jpeg,bmp,png
        if img_type.lower() in ['gif','jpg','jpeg','bmp','png','ico'] :
            data['isimage'] = True
        main_path = os.path.join(UPLOAD_FOLDER, dtlist[0], dtlist[1], dtlist[2])
        url = "/".join([dtlist[0], dtlist[1], dtlist[2], uuidstr + "." + img_type])
        data['url'] = url
        data['admin_id'] = uid
        if  not os.path.exists(main_path):
            os.makedirs(main_path)
        real_file_path = os.path.join(main_path, uuidstr + "." + img_type)
        r = requests.get(remote_img_url)
        with open(real_file_path, 'wb') as f:
            f.write(r.content) 
        filesize = os.path.getsize(real_file_path)
        data['filesize'] = filesize
        attachments = None
        try:
            attachments = Attachments()
            attachments.admin_id = data['admin_id']
            attachments.url = data['url']
            attachments.title = data['title']
            attachments.mimetype = data['mimetype']
            attachments.filesize = data['filesize']
            attachments.uuid = data['uuid']
            attachments.imagetype = data['imagetype']
            attachments.isimage = data['isimage']
            module_name = ''
            module_obj_id = 0
            if module_name :
                attachments.module_name = module_name
            if module_obj_id :
                attachments.module_obj_id = module_obj_id            
            db.session.add(attachments)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e) 
        return attachments





