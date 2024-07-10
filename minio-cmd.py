 from minio import Minio
import urllib.request
import requests
import os
import redis
MINIO_ADDRESS=
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
client = Minio(MINIO_ADDRESS,access_key=MINIO_ACCESS_KEY,secret_key=MINIO_SECRET_KEY,secure=True)
#using self in class is  a way to call def of class in another def. we call it instance. 
class minio:
    def __init__(self):
      print('Hello')
    def login(self,address,accesskey,secretkey):
      minioClient = Minio(address,access_key=accesskey,secret_key=secretkey,secure=True)
      self.minio_clients = minioClient
      return self.minio_clients
    def list_bucket(self):
      self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
      buckets = self.login_var.list_buckets()
      for bucket in buckets:
        print(bucket.name, bucket.creation_date)
    def upload_object(self,bucket,key,value):
        self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)

        result = self.login_var.fput_object(
        bucket,key,value
        )
        print(
        "created {0} object; etag: {1}, version-id: {2}".format(
        result.object_name, result.etag, result.version_id,),
        )
    def list_file(self,bucket):
        self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
        objects = self.login_var.list_objects(bucket,recursive=True)
        for obj in objects:
         print(obj.object_name,obj.etag,obj.last_modified,obj.size,obj.version_id)
    def download_object(self,bucket,path):
        self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
        for item in self.login_var.list_objects(bucket,recursive=True):
            print(item.object_name,item.metadata)
            direct_path = path  + '/' + bucket + '/' + item.object_name 
            print(direct_path)
            self.login_var.fget_object(bucket,item.object_name,direct_path)
    def list_sort_file(self,bucket):
        self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
        sort_data = dict()
        objects = self.login_var.list_objects(bucket)
        for obj in objects:
          sort_data[obj.object_name] = obj.last_modified
        for key,value in  sort_data.items():
          print (key,value)
        print(sorted(sort_data.values()))
minio().download_object("bucket",'/root')

