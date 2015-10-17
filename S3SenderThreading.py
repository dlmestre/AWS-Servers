import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.connection import OrdinaryCallingFormat
from filechunkio import FileChunkIO
import datetime
import urllib2
import math
import os
import threading

class s3bucket:
    def __init__(self,path):
        self.ACCESS_KEY = "access_key" 
        self.SECRET_KEY = "secret_key"
        self.bucket_name = "bucket_name"
        self.path = path
    def ModificationDate(self,filename):
        day = os.path.getmtime(filename)
        return datetime.date.fromtimestamp(day)
    def ListFiles(self):
        files = []
        for name in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path,name)):
                files.append(os.path.join(self.path,name))
        return files
    def GetFiles(self):
        files = []
        for File in self.ListFiles():
            filedate = self.ModificationDate(File)
            if filedate == datetime.date.today():
                if File.endswith('.bak'):
                    files.append(File)
    def Send(self,File):
        conn = S3Connection(self.ACCESS_KEY,self.SECRET_KEY)
        bucket = conn.get_bucket(self.bucket_name)
        chunk_size = 542880000 #500 MG
        
        source_size = os.stat(File).st_size
        print("File Name ", File)
        print("File Size", source_size)
        source_size = os.stat(File).st_size
        if source_size > chunk_size:
            mp = bucket.initiate_multipart_upload("dbvs_backups/" + str(os.path.basename(File)))
            chunk_count = int(math.ceil(source_size / float(chunk_size)))

            for i in range(chunk_count):
                offset = chunk_size * i
                bytes = min(chunk_size, source_size - offset)
                with FileChunkIO(File, 'r', offset=offset,bytes=bytes) as fp:
                    mp.upload_part_from_file(fp, part_num=i + 1)
            # Finish the upload
            mp.complete_upload()
        else:
            k = Key(bucket)
            k.name = "dbvs_backups/" + str(os.path.basename(File))
            k.set_contents_from_filename(File)

    
    
path = r"/mnt/sqlbackups"

s3_object = s3bucket(path)
Files = s3_object.GetFiles()
print("Files to upload :", Files)
print("")
for File in Files:
    t = threading.Thread(target = s3_object.Send, args=(File,)).start()
