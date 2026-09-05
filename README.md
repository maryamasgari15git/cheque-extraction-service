# Cheque Extraction Service

A FastAPI-based service for extracting structured information from a cheque image using a multimodal Gemini model.

## Overview

This service receives a single cheque image and extracts the following information:

* Sayad ID
* Cheque number
* Amount in digits
* Amount in words
* Due date
* Payee
* Description
* Bank name
* Account number
* Branch code

The service is stateless and does not store cheque images or extracted data.

## Features

* FastAPI REST API
* Multimodal cheque image understanding using Gemini
* API Key authentication
* JPG, PNG, and single-page PDF support
* Maximum file size: 5 MB
* Model request timeout: 30 seconds
* Retry mechanism for temporary model/network failures
* Structured JSON response
* Interactive Swagger/OpenAPI documentation
* Simple HTML page for testing the API

## Project Structure

```text
cheque-extraction-service/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── auth.py
│   ├── exceptions.py
│   │
│   ├── models/
│   │   └── cheque.py
│   │
│   ├── prompts/
│   │   └── cheque_prompt.py
│   │
│   ├── services/
│   │   ├── extraction_service.py
│   │   └── file_validator.py
│   │
│   ├── utils/
│   │   ├── json_parser.py
│   │   └── retry.py
│   │
│   └── static/
│       └── index.html
│
├── tests/
│   ├── images/
│   └── test_results.xlsx
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

* Python 3.10+
* Internet connection
* Gemini API key

## Installation

### 1. Clone the repository

```bash
git clone <REPOSITORY_URL>
cd cheque-extraction-service
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model
SERVICE_API_KEY=your_service_api_key
```

### Environment Variables Description

| Variable          | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| `GEMINI_API_KEY`  | API key used to access the Gemini model                       |
| `GEMINI_MODEL`    | Gemini model name                                             |
| `SERVICE_API_KEY` | API key required by clients to access the extraction endpoint |

Do not commit the `.env` file to GitHub.

## Running the Service

Start the FastAPI application with:

```bash
uvicorn app.main:app --reload
```

The service will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

## Health Check

Endpoint:

```text
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

## Cheque Extraction API

Endpoint:

```text
POST /api/v1/cheque/extract
```

### Headers

```text
X-API-Key: your_service_api_key
```

### Request

The endpoint accepts one file using `multipart/form-data`.

Supported formats:

* JPEG
* PNG
* Single-page PDF

Maximum file size:

```text
5 MB
```

### Example using cURL

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/cheque/extract" \
  -H "X-API-Key: your_service_api_key" \
  -F "file=@cheque.jpg"
```

## Response

Successful response:

```json
{
  "success": true,
  "data": {
    "sayad_id": {
      "value": "1234567890123456",
      "confidence": 0.97
    },
    "cheque_number": {
      "value": "40324/966352",
      "confidence": 0.95
    },
    "amount_digits": {
      "value": "150000000",
      "confidence": 0.95
    },
    "amount_words": {
      "value": "پانزده میلیون تومان",
      "confidence": 0.88
    },
    "due_date": {
      "value": "1405/07/15",
      "confidence": 0.93
    },
    "payee": {
      "value": null,
      "confidence": 0
    },
    "description": {
      "value": null,
      "confidence": 0
    },
    "bank_name": {
      "value": "بانک سامان",
      "confidence": 0.99
    },
    "account_number": {
      "value": null,
      "confidence": 0
    },
    "branch_code": {
      "value": "5608216",
      "confidence": 0.95
    }
  },
  "processing_time_ms": 2400
}
```

If a field cannot be reliably extracted:

```json
{
  "value": null,
  "confidence": 0
}
```

The model is instructed not to guess missing or unreadable information.

## Error Responses

The service can return errors for situations such as:

| HTTP Status | Error Code       | Description                                       |
| ----------: | ---------------- | ------------------------------------------------- |
|         400 | `INVALID_IMAGE`  | Invalid, corrupted, or unsupported file           |
|         401 | `UNAUTHORIZED`   | Missing or invalid API key                        |
|         413 | `FILE_TOO_LARGE` | File exceeds 5 MB                                 |
|         502 | `MODEL_ERROR`    | Error while processing the request with the model |
|         504 | `TIMEOUT`        | Model processing exceeded the allowed timeout     |

## HTML Test Page

A simple HTML interface is available for testing the API.

Open:

```text
http://127.0.0.1:8000/
```

The page allows you to:

1. Enter the API key.
2. Select a cheque image.
3. Send the image to the extraction API.
4. View the returned JSON response.


## Testing

A sample test has been performed using a real cheque image.

The test result is recorded in:

tests/test_results.xlsx

The test table contains the expected value, model output, and comparison result for the extracted fields.

The acceptance criteria require testing with at least 30 real cheque images in the final validation phase.

The target accuracy for the following fields is at least 90%:

- `sayad_id`
- `amount_digits`

## Important Notes

* The service does not use a database.
* The service does not store cheque images.
* The service does not perform business validation or decision-making.
* The service does not compare extracted information with external data.
* The service uses a multimodal model for image understanding.
* The Gemini API key must be kept private and must not be committed to the repository.
