import minio
import os

minio_client = minio.Minio(
    'localhost:9000',
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET'),
    secure=False
)
bucket_name = 'what-to-eat-temporary'

def upload_file(file_path, object_name):
    minio_client.fput_object(bucket_name, object_name, file_path)

def download_file(object_name, file_path):
    minio_client.fget_object(bucket_name, object_name, file_path)

if __name__ == '__main__':
    print(f'Access key: {os.getenv("MINIO_ACCESS_KEY")}')
    upload_file('requirements.txt', 'test.txt')
    download_file('test.txt', 'test.txt')