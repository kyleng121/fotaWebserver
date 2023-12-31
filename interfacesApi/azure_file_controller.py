from io import BytesIO
import uuid
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient,BlobServiceClient
from django.conf import settings

from . import models


ALLOWED_EXTENTIONS = ['.pdf','.doc','.docx','.bin','.zip']

storage_account_key = "79xt7Bov9aGr3UxCIO+CJ3nGDNfeZXSkV33E1bxOVgfzz787mMDXrrBS91Nvnd+WaoQSZb5PPVI1+AStRV5jzA=="
storage_account_name = "fotafwstorage2"
connection_string = "DefaultEndpointsProtocol=https;AccountName=fotafwstorage2;AccountKey=79xt7Bov9aGr3UxCIO+CJ3nGDNfeZXSkV33E1bxOVgfzz787mMDXrrBS91Nvnd+WaoQSZb5PPVI1+AStRV5jzA==;EndpointSuffix=core.windows.net"
container_name = "fwupload"

def upload_to_blob_storage(file,file_name):
    print("in upload function to blob")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    print("in upload function to blob1")
    blob_client = blob_service_client.get_blob_client(container=container_name,blob=file_name)
    print("in upload function to blob2")
    blob_client.upload_blob(data=file)
    print("in upload function to blob3")
    file_object = save_file_url_to_db(blob_client.url)
    print("in upload function to blob4")
    return file_object

# def create_blob_client(file_name):

#     account_url = 'https://fotafwstorage.blob.core.windows.net'
#     # container_name = container_name
#     default_credential = DefaultAzureCredential()
#     blob_service_client = BlobServiceClient(account_url, credential=default_credential)
#     container_client = blob_service_client.create_container(container_name)
#     # secret_client = SecretClient(
#     #     vault_url=settings.AZURE_VAULT_ACCOUNT, credential=default_credential
#     # )

#     # storage_credentials = secret_client.get_secret(name=settings.AZURE_STORAGE_KEY_NAME)

#     return BlobClient(
#         account_url,
#         container_name,
#         blob_name=file_name,
#         # credential=storage_credentials.value,
#     )

def check_file_ext(path):
    ext = Path(path).suffix
    return ext in ALLOWED_EXTENTIONS


# def download_blob(file):
#     blob_client = create_blob_client(file)
#     if not blob_client.exists():
#         return
#     blob_content = blob_client.download_blob()
#     return blob_content
    

def save_file_url_to_db(file_url):
    new_file = models.File.objects.create(file_url=file_url)
    new_file.save()
    return new_file

def upload_file_to_blob(file):
    print("start")
    if not check_file_ext(file.name):
        return
    print("pass check file")
    file_prefix = str(file.name)
    ext = Path(file.name).suffix
    file_name = f"{file_prefix}"
    file_content = file.read()
    file_io = BytesIO(file_content)
    file_object = upload_to_blob_storage(file_io,file_name)
    print("end of line")
    # blob_client.upload_blob(data=file_io)
    # file_object = save_file_url_to_db(blob_client.url)

    return file_object
