# Vision AI API

A FastAPI-based application for document processing using vision models and AI agents. Supports OCR on images/PDFs, text extraction from DOCX/MD files, and automated approval checks.

## Features

- **OCR Processing**: Extract text from images and PDFs using vision models.
- **Document Approval**: AI agent evaluates documents for approval/rejection.
- **Multi-format Support**: Handles PDFs, images (JPG, PNG, etc.), DOCX, and MD files.
- **Database Integration**: PostgreSQL support for proposal and document management.
- **API Endpoints**: RESTful APIs for health checks, proposal processing, and pending proposals.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables (see .env.example).
4. Run the application:
    ```bash
    python main.py
    ```
    
## Usage
- Start the server: uvicorn main:app --host 0.0.0.0 --port 8000
- Access API docs at http://localhost:8000/docs

## API Endpoints
- GET /health: Health check.
- POST /check_proposal: Process pending proposals.
- GET /pending-proposals: Get list of pending proposal IDs.