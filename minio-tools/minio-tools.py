from minio import Minio
import urllib.request
import os
import sys
import glob
from dotenv import load_dotenv
from threading import Thread

###Progress class ENV
_BAR_SIZE = 20
_KILOBYTE = 1024
_FINISHED_BAR = '#'
_REMAINING_BAR = '-'
_UNKNOWN_SIZE = '?'
_STR_MEGABYTE = ' MB'
_HOURS_OF_ELAPSED = '%d:%02d:%02d'
_MINUTES_OF_ELAPSED = '%02d:%02d'
_RATE_FORMAT = '%5.2f'
_PERCENTAGE_FORMAT = '%3d%%'
_HUMANINZED_FORMAT = '%0.2f'
_DISPLAY_FORMAT = '|%s| %s/%s %s [elapsed: %s left: %s, %s MB/sec]'
_REFRESH_CHAR = '\r'
###
###MINIO_CLASS_ENV
# Load environment variables from the .env file
load_dotenv()
 
# Access environment variables
MINIO_SECOND_ADDRES = os.getenv("MINIO_UPLOAD_ADDRESS")
MINIO_SECOND_ACCESS_KEY = os.getenv("MINIO_UPLOAD_ACCESS_KEY")
MINIO_SECOND_SECRET_KEY = os.getenv("MINIO_UPLOAD_SECRET_KEY")
MINIO_ACCESS_KEY = os.getenv("MINIO_DOWNLOAD_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_DOWNLOAD_SECRET_KEY")
MINIO_ADDRESS = os.getenv("MINIO_DOWNLOAD_ADDRESS")
print(MINIO_ADDRESS)
print(MINIO_ACCESS_KEY)
print(MINIO_SECRET_KEY)
print(MINIO_SECOND_SECRET_KEY)
print(MINIO_SECOND_ACCESS_KEY)
print(MINIO_SECOND_ADDRES)
client = Minio(MINIO_ADDRESS,access_key=MINIO_ACCESS_KEY,secret_key=MINIO_SECRET_KEY,secure=True)
client_second = Minio(MINIO_SECOND_ADDRES,access_key=MINIO_SECOND_ACCESS_KEY,secret_key=MINIO_SECOND_SECRET_KEY,secure=True)
###
#using self in class is  way to call def of class in another def. we call it instance. 

 


class minio:
    def __init__(self):
      print('Minio class')
    def login(self,address,accesskey,secretkey):
      minioClient = Minio(address,access_key=accesskey,secret_key=secretkey,secure=True)
      self.minio_clients = minioClient
      return self.minio_clients
    def list_bucket(self):
      self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
      buckets = self.login_var.list_buckets()
      for bucket in buckets:
        print(bucket.name, bucket.creation_date)
    def upload_object(self,local_path,bucket_name, minio_path):
        self.second_login_var = self.login(MINIO_SECOND_ADDRES,MINIO_SECOND_ACCESS_KEY,MINIO_SECOND_SECRET_KEY)
        cosntructed_path = local_path + "/" + bucket_name
        object_addresses = []

        for root, _ , files in os.walk(cosntructed_path):
            for file in files:
                join_paths = os.path.join( root , file)
                parts = join_paths.split(bucket_name, 1)
                if len(parts) > 1:
        # Extract the object address (relative path within the bucket)
                    object_address = parts[1].strip("/")
                    object_addresses.append(object_address)
            for address in object_addresses:
                print(join_paths)
                try:
                    # Attempt to get object stat (raises an exception if it doesn't exist)
                    self.second_login_var.stat_object(bucket_name, address)
                    print(f"Object '{address}' already exists in the bucket.")
                    continue
                except Exception as err:
                    # Likely a NoSuchKey error if the object doesn't exist
                    if "NoSuchKey" in str(err):
                        print(f"Uploading object: {address}")
                        self.second_login_var.fput_object(bucket_name, address , join_paths)
                    else:
                        print(f"An error occurred checking '{address}': {err}")

        
    def list_file(self,bucket,type):
      if type == "download":
        self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
        objects = self.login_var.list_objects(bucket,recursive=True)
        for obj in objects:
 #        print(obj.object_name,obj.etag,obj.last_modified,obj.size,obj.version_id)
          print(obj.object_name)
      if type == "upload":
        self.login_var = self.login(MINIO_SECOND_ADDRES,MINIO_SECOND_ACCESS_KEY,MINIO_SECOND_SECRET_KEY)
        objects = self.login_var.list_objects(bucket,recursive=True)
        for obj in objects:
          print(obj.object_name)
        return objects
    def download_object(self,bucket,path):
        object_addresses = []

        print("start donwloading")
        self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
        list_dir = []
        constructed_path = path + "/" + bucket
        print(constructed_path)
        for root, _ , files in os.walk(constructed_path):
            for file in files:
                constructed_path_local = root + "/" + file
                list_dir.append(constructed_path_local)
        
        for item in self.login_var.list_objects(bucket,recursive=True):
          print(path + "/" + bucket + "/" + item.object_name)
          bucket_construced_path = path + "/" + bucket + "/" + item.object_name
          if bucket_construced_path in list_dir:
            print("object exist in ", path)
          else:
            self.login_var.fget_object(bucket,item.object_name,bucket_construced_path)

        
                

      #   for item in self.login_var.list_objects(bucket,recursive=True):
      #       direct_path = path  + '/' + bucket + '/' + item.object_name 
      #       object_addresses.append(direct_path)
      #  # print(object_addresses[1])
      #   constructed_path  = path + "/" + bucket
      #   for root, _ , files in os.walk(constructed_path):
      #       for file in files:
      #           constructed_path_local = root + file
      #      #     print(constructed_path_local)
      #           if constructed_path_local in object_addresses: 
      #              print("object", constructed_path_local , "exists")
                # else:
                #   print("downloading" ,constructed_path_local )
                #   self.login_var.fget_object(bucket,item.object_name,direct_path)
        print("downloading have finished")
    def download_object_second(self,bucket,path):
        print("start donwloading")
        self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
        for item in self.login_var.list_objects(bucket,recursive=True):
            print("start listing")
            direct_path = path  + '/' + bucket + '/' + item.object_name 
            print(item.object_name)
            self.login_var.fget_object(bucket,item.object_name,direct_path)
            # for local_file in glob.glob(direct_path + '/**'):
            #   local_file = local_file.replace(os.sep, "/") # Replace \ with / on Windows
            #   print("Start downloading")
            #   if not os.path.ex(local_file):
            #     self.login_var.fget_object(bucket,item.object_name,direct_path)
            #     print(bucket,item.object_name,"if worked")
            #   else:
            #     self.login_var.fget_object(bucket,item.object_name,direct_path)
            #     print("else worked")
    def list_sort_file(self,bucket):
        self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
        sort_data = dict()
        objects = self.login_var.list_objects(bucket)
        for obj in objects:
          sort_data[obj.object_name] = obj.last_modified
        for key,value in  sort_data.items():
          print (key,value)
        print(sorted(sort_data.values()))
#######################################PROGRESS CLASS########################
# class Progress(Thread):
#     """
#         Constructs a :class:`Progress` object.
#         :param interval: Sets the time interval to be displayed on the screen.
#         :param stdout: Sets the standard output
#         :return: :class:`Progress` object
#     """

#     def __init__(self, interval=1, stdout=sys.stdout):
#         Thread.__init__(self)
#         self.daemon = True
#         self.total_length = 0
#         self.interval = interval
#         self.object_name = None

#         self.last_printed_len = 0
#         self.current_size = 0

#         self.display_queue = Queue()
#         self.initial_time = time.time()
#         self.stdout = stdout
#         self.start()

#     def set_meta(self, total_length, object_name):
#         """
#         Metadata settings for the object. This method called before uploading
#         object
#         :param total_length: Total length of object.
#         :param object_name: Object name to be showed.
#         """
#         self.total_length = total_length
#         self.object_name = object_name
#         self.prefix = self.object_name + ': ' if self.object_name else ''

#     def run(self):
#         displayed_time = 0
#         while True:
#             try:
#                 # display every interval secs
#                 task = self.display_queue.get(timeout=self.interval)
#             except Empty:
#                 elapsed_time = time.time() - self.initial_time
#                 if elapsed_time > displayed_time:
#                     displayed_time = elapsed_time
#                 self.print_status(current_size=self.current_size,
#                                   total_length=self.total_length,
#                                   displayed_time=displayed_time,
#                                   prefix=self.prefix)
#                 continue

#             current_size, total_length = task
#             displayed_time = time.time() - self.initial_time
#             self.print_status(current_size=current_size,
#                               total_length=total_length,
#                               displayed_time=displayed_time,
#                               prefix=self.prefix)
#             self.display_queue.task_done()
#             if current_size == total_length:
#                 self.done_progress()

#     def update(self, size):
#         """
#         Update object size to be showed. This method called while uploading
#         :param size: Object size to be showed. The object size should be in
#                      bytes.
#         """
#         if not isinstance(size, int):
#             raise ValueError('{} type can not be displayed. '
#                              'Please change it to Int.'.format(type(size)))

#         self.current_size += size
#         self.display_queue.put((self.current_size, self.total_length))

#     def done_progress(self):
#         self.total_length = 0
#         self.object_name = None
#         self.last_printed_len = 0
#         self.current_size = 0

#     def print_status(self, current_size, total_length, displayed_time, prefix):
#         formatted_str = prefix + format_string(
#             current_size, total_length, displayed_time)
#         self.stdout.write(_REFRESH_CHAR + formatted_str + ' ' *
#                           max(self.last_printed_len - len(formatted_str), 0))
#         self.stdout.flush()
#         self.last_printed_len = len(formatted_str)


# def seconds_to_time(seconds):
#     """
#     Consistent time format to be displayed on the elapsed time in screen.
#     :param seconds: seconds
#     """
#     minutes, seconds = divmod(int(seconds), 60)
#     hours, m = divmod(minutes, 60)
#     if hours:
#         return _HOURS_OF_ELAPSED % (hours, m, seconds)
#     else:
#         return _MINUTES_OF_ELAPSED % (m, seconds)


# def format_string(current_size, total_length, elapsed_time):
#     """
#     Consistent format to be displayed on the screen.
#     :param current_size: Number of finished object size
#     :param total_length: Total object size
#     :param elapsed_time: number of seconds passed since start
#     """

#     n_to_mb = current_size / _KILOBYTE / _KILOBYTE
#     elapsed_str = seconds_to_time(elapsed_time)

#     rate = _RATE_FORMAT % (
#         n_to_mb / elapsed_time) if elapsed_time else _UNKNOWN_SIZE
#     frac = float(current_size) / total_length
#     bar_length = int(frac * _BAR_SIZE)
#     bar = (_FINISHED_BAR * bar_length +
#            _REMAINING_BAR * (_BAR_SIZE - bar_length))
#     percentage = _PERCENTAGE_FORMAT % (frac * 100)
#     left_str = (
#         seconds_to_time(
#             elapsed_time / current_size * (total_length - current_size))
#         if current_size else _UNKNOWN_SIZE)

#     humanized_total = _HUMANINZED_FORMAT % (
#         total_length / _KILOBYTE / _KILOBYTE) + _STR_MEGABYTE
#     humanized_n = _HUMANINZED_FORMAT % n_to_mb + _STR_MEGABYTE

#     return _DISPLAY_FORMAT % (bar, humanized_n, humanized_total, percentage,
#                               elapsed_str, left_str, rate)

#######################################PROGRESS CLASS########################
minio().download_object("bucket",'/home/mohammadreza/minio')
#minio().list_file("bucket","download")
#minio().upload_object("/home/mohammadreza/minio/bucket/","bucket","/")
