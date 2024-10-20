from io import BytesIO
from typing import Annotated
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import uuid

router = APIRouter()

from .client import minio_client, bucket_name

@router.get("/list")
async def list_objects():
    """
    List all objects in the given bucket
    """
    return minio_client.list_objects(bucket_name)

@router.get("/{object_name}/info")
async def get_object_data(object_name: str):
    return minio_client.stat_object(bucket_name, object_name)

# @router.get("/get/{object_name}")
# async def get_object(object_name: str):
#     # return minio_client.get_object(bucket_name, object_name)
#     return StreamingResponse(minio_client.get_object(bucket_name, object_name))

@router.post("/upload/")
async def upload_object(file: Annotated[bytes, File()]):
    object_name = str(uuid.uuid4())
    minio_client.put_object(bucket_name, object_name, BytesIO(file), len(file))
    return {"object_name": object_name}

        