import os
from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

import httpx
from fastapi import HTTPException, UploadFile


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "uploads")


def _extract_object_path_from_public_url(file_url: str) -> str | None:
    if not SUPABASE_URL:
        return None

    public_prefix = f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/"
    if not file_url.startswith(public_prefix):
        return None

    parsed = urlparse(file_url)
    path_without_query = parsed.path
    expected_prefix = f"/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/"
    if not path_without_query.startswith(expected_prefix):
        return None

    return path_without_query.replace(expected_prefix, "", 1)


async def upload_file_to_supabase(file: UploadFile, folder: str) -> str:
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(status_code=500, detail="Missing Supabase storage configuration")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    extension = Path(file.filename or "").suffix or ".jpg"
    object_path = f"{folder}/{uuid4().hex}{extension}"
    upload_url = f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/{SUPABASE_STORAGE_BUCKET}/{object_path}"

    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": file.content_type,
        "x-upsert": "true",
    }

    content = await file.read()

    async with httpx.AsyncClient() as client:
        response = await client.post(upload_url, headers=headers, content=content, timeout=30)

    if response.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail="Upload to Supabase Storage failed")

    return f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/{object_path}"


async def delete_file_from_supabase(file_url: str | None) -> None:
    if not file_url:
        return

    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(status_code=500, detail="Missing Supabase storage configuration")

    object_path = _extract_object_path_from_public_url(file_url)
    if not object_path:
        return

    delete_url = f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/{SUPABASE_STORAGE_BUCKET}/{object_path}"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.delete(delete_url, headers=headers, timeout=30)

    if response.status_code not in (200, 204):
        raise HTTPException(status_code=502, detail="Failed to delete cover from Supabase Storage")
