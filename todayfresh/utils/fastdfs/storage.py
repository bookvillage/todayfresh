# 自定义文件存储类
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings
import os


class FDFSStorage(Storage):
    def __init__(self,client_conf=None,nginx_url=None):
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf
        if nginx_url is None:
            nginx_url = settings.FDFS_NGINX_URL
        self.nginx_url = nginx_url

    def _open(self,name,mode='rb'):
        '''打开文件调用'''
        pass

    def _save(self,name,content):
        '''保存文件时调用'''
        # 创建client对象
        client = Fdfs_client(self.client_conf)
        content = content.read()
        # return dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # } if success else None
        # 上传文件
        res = client.upload_by_buffer(content)
        if res.get('Status') != 'Upload successed.':
            # 上传文件失败
            raise Exception("上传文件到fastdfs文件系统失败")
        file_id = res.get('Remote file_id')
        return file_id

    def url(self,name):
        # 输入文件id，返回一个可以访问的url
        return self.nginx_url + name

    def exists(self, name):
        return False
