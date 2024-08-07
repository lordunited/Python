from minio import Minio
import urllib.request
import os
import sys
import glob
import magic
import mimetypes
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

def check_file_type(file_path):
  """
  Checks the file type of a given file.

  Args:
    file_path: The path to the file.

  Returns:
    A tuple of (file_extension, mime_type).
  """

  # Get the file extension
  file_extension = os.path.splitext(file_path)[1].lower()

  # Get the MIME type
  mime_type, _ = mimetypes.guess_type(file_path)

  return file_extension, mime_type

def show_extension(file_path):
    """
    Adds an appropriate extension to a file path.

    Args:
        file_path: Path to the file.

    Returns:
        The updated file path with an extension.
    """

    base_name, ext = os.path.splitext(file_path)

    if ext:
        return file_path  # File already has an extension

    mime = magic.from_file(file_path, mime=True)
    extension = get_extension_from_mime(mime)

    if extension:
        return extension



def add_extension(file_path):
    """
    Adds an appropriate extension to a file path.

    Args:
        file_path: Path to the file.

    Returns:
        The updated file path with an extension.
    """

    base_name, ext = os.path.splitext(file_path)

    if ext:
        return file_path  # File already has an extension

    mime = magic.from_file(file_path, mime=True)
    extension = get_extension_from_mime(mime)

    if extension:
        return base_name + extension

    return base_name + ".bin"  # Default extension

def get_extension_from_mime(mime):
    """
    Maps MIME types to common file extensions.

    Args:
        mime: MIME type of the file.

    Returns:
        The appropriate file extension or None if unknown.
    """

    # Expand this mapping as needed
    mime_to_extension = {
        "application/octet-stream": ".octet",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/bmp": ".bmp",
        "image/webp" : ".webp",
        "image/tiff": ".tiff",
        "application/pdf": ".pdf",
        "video/mp4": ".mp4",
        "video/avi": ".avi",
        "video/quicktime": "quicktime",
        "application/zip": ".zip",
        "audio/mpeg": "mpeg",
        "audio/wav": "wav",
        "audio/ogg": ".ogg",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
        "text/plain": ".txt",
        "application/json": ".json",
        # ... other mappings
    }
    return mime_to_extension.get(mime)

def get_mime_type(file_extension):
  """Returns the MIME type based on the file extension."""
  if file_extension == "application/octet-stream":
      return file_extension
  else:
    file_extension = file_extension.lower()  # Convert to lowercase for consistency

    if file_extension == ".jpg" or file_extension == ".jpeg":
      return "image/jpeg"
    elif file_extension == ".png":
      return "image/png"
    elif file_extension == ".gif":
      return "image/gif"
    elif file_extension == ".pdf":
      return "application/pdf"
    elif file_extension == ".webp":
      return "image/webp"
    elif file_extension == ".txt":
      return "text/plain"
    elif file_extension == ".docx":
      return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif file_extension  == ".xlsx":
      return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif file_extension == ".json":
      return "application/json"
    elif file_extension == ".octet":
      return "application/octet-stream"
    else:
      return "application/octet-stream" # Or handle unknown extensions as needed

def extract_path_after_bucket(bucket_name, local_path):
  """Extracts the path after the bucket name from the local path.

  Args:
    bucket_name: The name of the bucket.
    local_path: The full local path.

  Returns:
    The path after the bucket name, or None if the bucket name is not found.
  """

  bucket_dir = os.path.join(os.path.sep, bucket_name)
  index = local_path.find(bucket_dir)
  if index != -1:
    return local_path[index + len(bucket_dir):]
  else:
    return None

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
        print("start uploading")
        self.second_login_var = self.login(MINIO_SECOND_ADDRES,MINIO_SECOND_ACCESS_KEY,MINIO_SECOND_SECRET_KEY)
        cosntructed_path = local_path + bucket_name
        object_addresses = []
        counter_name = 0
        object_minio_address = []
        objects = self.second_login_var.list_objects(bucket_name,prefix='',recursive=True)
        for obj in objects:
            object_minio_address.append(obj.object_name)
        print("Remote", object_minio_address)
        extenstions = [".png",".jpg",".jpeg",".thumbnail",".pdf",".text",".txt",".xlsx"]
        print("objects exist in bucket count is ", len(object_minio_address))
        for root, _ , files in os.walk(cosntructed_path):
            for file in files:
                counter_name = counter_name + 1

                join_paths = os.path.join( root , file)
                parts = join_paths.split(bucket_name, 1)
        # # Extract the object address (relative path within the bucket)
        # #add dict in list file
        #>uncomment if you need to add extenstion on file names
                # for b in extenstions:
                #   if b in join_paths:
                #     print(join_paths , "it has",b)
                #     object_addresses.append(join_paths)
                #   else:
                #     object_address_ext= add_extension(join_paths)
                #     object_addresses.append(object_address_ext)
                #     print(object_address_ext)           
        #/>uncomment if you need to add extenstion on file names 
                object_addresses.append(join_paths)
        final_path_list = []
        
        for i in object_minio_address:
          final_path = local_path + bucket_name + "/" + i
          final_path_list.append(final_path)
        for a in object_addresses:
           print("for 1")
           part_for_two = a.split(bucket_name, 1)
           part_for_two_complete = os.path.normpath(str(part_for_two[1]))
           cosntructed_path_two = local_path  + bucket_name + part_for_two_complete     
           if cosntructed_path_two in final_path_list:
            print("if 1")

            print("object exist",part_for_two_complete)
            
           else:
            print("if 1 else")

            for s in extenstions:
              print("for 2")
 
              if s in part_for_two_complete:
                print("if 2 ")
                print( "has extention", part_for_two_complete)
                self.second_login_var.fput_object(bucket_name, part_for_two_complete , a )

              else:
                
                print("if 2 else")
                print("before extentsion",a)
                file_extension = show_extension(a)
                file_meme = get_mime_type(file_extension)
                part_for_two = a.split(bucket_name, 1)
                print("uploading",part_for_two_complete)
                
                self.second_login_var.fput_object(bucket_name, part_for_two_complete , a ,content_type=file_meme)
                break

           #   final_path = local_path + bucket_name + "/" + a
              #self.second_login_var.fput_object(bucket_name, a , final_path,content_type=file_meme)
               # ext_file = get_extension_from_mime(os.walk(a))
          #  print(ext_file)
           #     final_path = local_path + bucket_name + "/" + a
 #           sel#f.second_login_var.put_object(bucket_name, a , final_path,content_type=)
                # try:
                #     # Attempt to get object stat (raises an exception if it doesn't exist)
                #     self.second_login_var.stat_object(bucket_name, address)
                #     print(f"Object '{address}' already exists in the bucket.")
                #     continue
                # except Except
                # ion as err:
                #     # Likely a NoSuchKey error if the object doesn't exist
                #     if "NoSuchKey" in str(err):
                #         print(f"Uploading object: {address}")
                #         self.second_login_var.fput_object(bucket_name, address , join_paths)
                #     else:
                #         print(f"An error occurred checking '{address}': {err}")
                #     print(len(object_addresses))
    def list_file(self,bucket,type):
      if type == "download":
        counter = 0
        self.login_var = self.login(MINIO_ADDRESS,MINIO_ACCESS_KEY,MINIO_SECRET_KEY)
        objects = self.login_var.list_objects(bucket,recursive=True)
        for obj in objects:
          counter = 1 + counter
 #        print(obj.object_name,obj.etag,obj.last_modified,obj.size,obj.version_id)
          print(obj.object_name)
        print(counter)
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
        
        for item in self.login_var.list_objects(bucket,prefix='',recursive=True):
          print(path + "/" + bucket + "/" + item.object_name)
          bucket_construced_path = path + "/" + bucket + "/" + item.object_name
          if bucket_construced_path in list_dir:
            print("object exist in ", path)
          else:
            self.login_var.fget_object(bucket,item.object_name,bucket_construced_path)
        print(len(object_addresses))
                

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

#minio().download_object("bucket",'/home/mohammadreza/minio')
minio().upload_object("/home/mohammadreza/minio/","bucket","/")
#minio().download_object("bucket",'/home/mohammadreza/minio')
#minio().list_file("bucket","upload")
#minio().upload_object("/home/mohammadreza/minio/bucket/","bucket","/")