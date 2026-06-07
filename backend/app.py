from __future__ import annotations
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from src.extractor import EXIFExtractor, EXIFExtractorError
from .sanitizer import (
    sanitize,
    sanitize_exif_output,
    SanitizationError,
    UnsupportedImageFormatError,
    MAX_SIZE,
)

def make_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(i) for i in obj]
    if isinstance(obj, bytes):
        try:
            return obj.decode("ascii").strip("\x00")
        except UnicodeDecodeError:
            return obj.hex()
    return obj


app = FastAPI(title="EXIF Extractor API")
allowed_origins = os.environ.get(
    "CORS_ALLOW_ORIGINS", "https://yourproductiondomain.com"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/extract")
async def extract_exif(file: UploadFile = File(...)) -> JSONResponse:
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are supported")

    temp_path = None
    try:
        # Read up to MAX_SIZE + 1 to detect oversized uploads without streaming complexities
        data = await file.read(MAX_SIZE + 1)
        print(f"File size: {len(data)} bytes")
        print(f"First 8 bytes: {data[:8].hex()}")
        print(f"Filename: {file.filename}")
        try:
            data, image_format = sanitize(file, data)
        except UnsupportedImageFormatError as s_err:
            raise HTTPException(status_code=415, detail=str(s_err))
        except SanitizationError as s_err:
            raise HTTPException(status_code=422, detail=str(s_err))

        # Persist to a temp file for the extractor to read from disk
        suffix = f".{image_format}"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            temp_path = Path(tmp.name)
            tmp.write(data)

        extractor = EXIFExtractor(str(temp_path))
        metadata = extractor.extract()
        serializable_metadata = make_serializable(metadata)
        safe_metadata = sanitize_exif_output(serializable_metadata)
        return JSONResponse(content={"metadata": safe_metadata})
    except EXIFExtractorError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
