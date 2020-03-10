"""resource

API Resource Of attachments Module 

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from flask import current_app, request
from app.common.status import Status
from app.common.schema import *
from app.common.param import *
from flask_marshmallow import base_fields
from flask_restplus import reqparse
from flask_restplus_patched import Resource, Namespace, abort, HTTPStatus
from app.common.result import Result
from app.common.wrap import auth
from .model import *
from .schema import *
from .param import *
from .dao import *
import random
import string
from sqlalchemy import or_
from datetime import datetime
import uuid
import os
from app.modules.admin.model import *
from app.modules.admin.dao import *


ns = Namespace("attachments", description="attachments API Resource")

@ns.route("/")
class AttachmentsAPI(Resource):
    """
    attachments module resource main service: add/delete/edit/view
    """

    @auth()
    @ns.response(AttachmentsSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        view
        """
        record = None
        attachmentsDao = AttachmentsDao() 
        id = request.uid
        record = attachmentsDao.getById(id)  
        return record

    @ns.parameters(AttachmentsParameters(dump_only=['id']))
    @ns.response(AttachmentsSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        attachments = None
        attachmentsDao = AttachmentsDao()
        try:
            attachments = attachmentsDao.add(args)
        except Exception as e:
            abort(500, e)       
        return attachments

    @auth()
    @ns.parameters(IDSParameters())
    @ns.response(BasicSchema(many=False))
    def delete(self, args):
        """
        delete
        """
        result = False
        ids = args.get('ids')
        attachmentsDao = AttachmentsDao()      
        try:
            result = attachmentsDao.delete(ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

    @ns.parameters(AttachmentsParameters())
    @ns.response(AttachmentsSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        attachmentsDao = AttachmentsDao()            
        try:
            record = attachmentsDao.edit(args)
        except Exception as e:
            abort(500, e)        
        return record

@ns.route("/list")
class AttachmentsListAPI(Resource):
    """
    attachments module resource list service
    """
    @auth()
    @ns.parameters(ExtendPagerParameters())
    @ns.response(AttachmentsListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        view list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        args.setdefault('lang','')
        args.setdefault('module_name','')
        args.setdefault('module_obj_id',0)
        args.setdefault('category_id',0)
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        lang = args.pop('lang')
        module_name = args.pop('module_name')
        module_obj_id = args.pop('module_obj_id')
        category_id = args.pop('category_id')
        attachmentsDao = AttachmentsDao()
        data = attachmentsDao.getList(search, sort, order, offset, limit, lang, module_name, module_obj_id, category_id)
        return data

@ns.route("/upload")
class AttachmentsUploadAPI(Resource):
    @auth()
    @ns.response(BasicSchema(many=False)) 
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self):
        """
        upload
        """
        uid = request.uid
        rfile = request.files.get('file')
        filesize = request.form['size']
        module_name = request.headers.get("module_name")
        module_obj_id = request.headers.get("module_obj_id")
        current_app.logger.debug("module_name:"+str(module_name))
        current_app.logger.debug("module_obj_id:"+str(module_obj_id))
        data = {}
        attachmentsDao = AttachmentsDao()
        try:
            data = attachmentsDao.upload(uid, rfile, filesize, module_name, module_obj_id)
        except Exception as e:
            abort(500, e)        
        return Result.success(data)

@ns.route("/ckeditor_browser_upload")
class AttachmentsCKeditorBrowserUploadAPI(Resource):
    @auth()
    @ns.parameters(CEditorFileBrowserUploadParameters())
    @ns.response(AttachmentsCKeditorUploadSchema()) 
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        ckeditor browser upload response api # ckeditor上传附件
        """
        args.setdefault('CKEditorFuncNum',0)
        args.setdefault('CKEditor','')
        args.setdefault('langCode','')
        args.setdefault('ckCsrfToken','')
        CKEditorFuncNum = args.pop('CKEditorFuncNum')
        CKEditor = args.pop('CKEditor')
        langCode = args.pop('langCode')
        ckCsrfToken = args.pop('ckCsrfToken')
        uid = request.uid
        rfile = request.files.get('file')
        module_name = request.headers.get("X-Module-Name")
        module_obj_id = request.headers.get("X-Module-Obj-Id")
        filename = request.headers.get("X-File-Name")
        filesize = request.headers.get("X-File-Size")
        static_url = request.headers.get("X-STATIC_URL")        
        current_app.logger.debug("module_name:"+module_name)
        current_app.logger.debug("module_obj_id:"+str(module_obj_id))
        data = {
            "uploaded": 0,
            "fileName": "",
            "url": "",
            "error": {
                "message": ""
            }
        }
        message = ''
        save_data = {}
        attachmentsDao = AttachmentsDao()
        try:
            save_data = attachmentsDao.ckeditor_browser_upload(uid, rfile, filename, filesize, module_name, module_obj_id)
        except Exception as e:
            message = str(e)
            data['uploaded'] = 0
            data['fileName']  = filename   
            data['url']  = ''
            data['error']['message'] = message  
            return data          
            # abort(500, e)  
        # Check the $_FILES array and save the file. Assign the correct path to a variable ($url).
        # url = '/path/to/uploaded/file.ext'
        # # Usually you will only assign something here if the file could not be uploaded.
        message = 'The uploaded file has been renamed' 
        data['uploaded'] = 1
        data['fileName']  = filename   
        data['url']  = static_url + save_data['url']
        # return "<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction({CKEditorFuncNum}, {url}, {message});</script>".format(CKEditorFuncNum=CKEditorFuncNum, url=url, message=message)
        return data

@ns.route("/upload_avatar")
class AttachmentsUploadAvatarAPI(Resource):
    @auth()
    @ns.response(BasicSchema(many=False)) 
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self):
        """
        upload avatar # 上传头像
        """
        uid = request.uid
        rfile = request.files.get('file')
        filesize = request.form['size']
        data = {}
        attachmentsDao = AttachmentsDao()
        try:
            data = attachmentsDao.upload_avatar(uid, rfile, filesize)
        except Exception as e:
            abort(500, e)        
        return Result.success(data)

@ns.route("/local_imgurl")
class AttachmentsLocalImgURLAPI(Resource):
    @auth()
    @ns.parameters(RemoteImgURLParameters())
    @ns.response(AttachmentsSchema(many=False)) 
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        Download image data through the image URL and save it locally, and return the locally saved URL
        通过图像的URL下载图像数据并保存至本地，返回本地保存的URL

        """
        uid = request.uid
        args.setdefault('remote_img_url','')
        remote_img_url = args.pop('remote_img_url')
        data = {}
        attachmentsDao = AttachmentsDao()
        try:
            data = attachmentsDao.getLocalImgURL(uid, remote_img_url)
        except Exception as e:
            abort(500, e)        
        return data
