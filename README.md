<div align="center">
  <h1>Local-EXIF-Inspector</h1>
  <p>
    <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Frontend-React-61DAFB?style=flat&logo=react&logoColor=black" alt="React" />
    <img src="https://img.shields.io/badge/Bundler-Vite-646CFF?style=flat&logo=vite&logoColor=white" alt="Vite" />
    <img src="https://img.shields.io/badge/Styling-TailwindCSS-38B2AC?style=flat&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  </p>
</div>


## Overview

This project extracts camera, EXIF, and GPS metadata from image files using a custom parser stack.
It runs entirely on your machine: images are uploaded only to the local backend, parsed, and then returned to the browser.

Supported image formats:
- JPEG
- PNG
- TIFF
- WEBP

## How it works

1. The frontend uploads a local image to the backend `POST /extract` endpoint.
2. The backend validates file size, filename, and magic bytes to enforce local-only parsing.
3. The extractor detects the image container format and parses binary metadata directly from the image bytes.
4. JPEG metadata is found inside the APP1 EXIF segment, TIFF metadata is parsed from the TIFF header and IFD chains, PNG metadata comes from chunks such as `gAMA`, `tEXt`, and `eXIf`, and WEBP metadata is extracted from the EXIF chunk when present.
5. Parsed fields are serialized as JSON and returned to the browser for display.

## Supported formats

| Format | Extracts |
|---|---|
| JPEG | IFD0, EXIF, GPS |
| PNG | Chunk metadata (`gAMA`, `tEXt`, `eXIf`) |
| TIFF | Full IFD0 + EXIF |
| WEBP | EXIF chunk if present |

## Key features

- Local-only metadata extraction
- FastAPI backend with file upload endpoint
- React/Vite frontend with drag-and-drop and file picker support
- Safe upload validation and temporary file cleanup
- JSON metadata display with EXIF, GPS, and TIFF fields

## Setup

### Prerequisites

- Python 3.11+ (or compatible)
- Node.js 18+ / npm
- `git` to clone and publish the repository

### Backend

From the project root:

```bash
python -m pip install -r backend/requirements.txt
uvicorn backend.app:app --reload
```

The backend will be available at `http://localhost:8000`.

### Frontend

From the project root:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## How to use

1. Start the backend and frontend.
2. Open the frontend in the browser.
3. Upload or drag an image into the interface.
4. View parsed metadata in the browser.

## Testing

Run the Python unit test suite from the project root:

```bash
python -m unittest discover -s tests
```

## Project structure

- `backend/` — FastAPI application and backend logic
- `frontend/` — React/Vite user interface
- `src/` — core metadata extraction and parser modules
- `tests/` — unit tests for sanitizer, parser, and extractor behavior
- `cli/` — optional command-line extractor entry point

## Security and privacy

- No external upload or telemetry code is included in the repository.
- Uploaded files are validated by magic bytes and file size.
- Temporary upload files are cleaned up after extraction.
- Browser requests are proxied to the local backend for development.



