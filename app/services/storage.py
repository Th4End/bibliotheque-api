import os
from pathlib import Path
from uuid import uuid4

import requests
from fastapi import HTTPException, UploadFile


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "uploads")


async def upload_file_to_supabase(file: UploadFile, folder: str) -> str:
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(
            status_code=500,
            detail="Missing Supabase storage configuration",
        )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    extension = Path(file.filename or "").suffix
    if not extension:
        extension = ".jpg"

    object_path = f"{folder}/{uuid4().hex}{extension}"
    upload_url = (
        f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/"
        f"{SUPABASE_STORAGE_BUCKET}/{object_path}"
    )

    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": file.content_type,
        "x-upsert": "true",
    }

    content = await file.read()
    response = requests.post(upload_url, headers=headers, data=content, timeout=30)
    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=502,
            detail="Upload to Supabase Storage failed",
        )

    return (
        f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/public/"
        f"{SUPABASE_STORAGE_BUCKET}/{object_path}"
    )
