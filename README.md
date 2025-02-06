# Simplify4u API

This project provides a no-login, rate-limited API for text processing tasks (summarization, translation, and analysis) using Django and Hugging Face Inference API. The API is designed to work without a user authentication system and is rate-limited to 10 requests per minute by default.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Notes](#notes)

## Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- A PostgreSQL database (or update `DATABASES` in `settings.py` to use a different database)
- [Hugging Face API key](https://huggingface.co/settings/tokens) (required for inference)

## Installation and Setup

1. **Clone the Repository:**

   ```bash
   git clone https://your-repo-url.git
   cd simplify4u
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *Note: Ensure that your `requirements.txt` includes packages such as `django`, `django-dotenv`, `django-cors-headers`, `django-ratelimit`, `requests`, `beautifulsoup4`, etc.*

4. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

## Configuration

Create a `.env` file in the project root (where `manage.py` is located) with the following environment variables:

```ini
# Django secret key
SECRET_KEY=your_django_secret_key

# Allowed hosts (comma separated, for example: localhost,127.0.0.1)
ALLOWED_HOSTS=localhost,127.0.0.1

# Rate limit (default 10 requests per minute)
RATE_LIMIT=10/m

# Hugging Face API key
HF_API_KEY=your_huggingface_api_key

# Database settings (update as necessary)
DB_NAME=your_db_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

## Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be accessible at `http://localhost:8000/`.

## API Endpoints

The API provides the following endpoints:

- **Summarize:**  
  `POST /api/summarize/`  
  Use this endpoint to summarize input text.

- **Translate:**  
  `POST /api/translate/`  
  Use this endpoint to translate input text.  
  Example input JSON:
  ```json
  {
    "text": "こんにちはお元気ですか."
  }
  ```
  Expected output:
  ```json
  {
    "response": "Hello."
  }
  ```

- **Analyze:**  
  `POST /api/analyze/`  
  Use this endpoint to analyze input text and receive key insights.

All endpoints expect a JSON payload with a `text` field and only accept the POST method.

## Testing the API

### Using Postman

1. **Set the Request Type:**  
   Select `POST` for the request method.

2. **Set the URL:**  
   For example, `http://localhost:8000/api/translate/`.

3. **Set Headers:**  
   - `Content-Type: application/json`

4. **Set Body:**  
   Choose the raw body type and add your JSON payload. For example:
   ```json
   {
     "text": "こんにちはお元気ですか."
   }
   ```

5. **Send the Request:**  
   You should receive a JSON response similar to:
   ```json
   {
     "response": "Hello."
   }
   ```

### Using cURL

You can also test the API using cURL. For example:

```bash
curl -X POST http://localhost:8000/api/translate/ \
     -H "Content-Type: application/json" \
     -d '{"text": "こんにちはお元気ですか."}'
```

## Notes

- **CSRF Protection:**  
  All API views are marked as CSRF-exempt using `@csrf_exempt` to simplify testing with non-browser clients. Do not use CSRF-exempt views in production without proper security measures.

- **Rate Limiting:**  
  The API is rate-limited to 10 requests per minute per IP address by default. Adjust the `RATE_LIMIT` variable in your `.env` file if needed.

- **Model Endpoints:**  
  The API uses Hugging Face Inference API endpoints for summarization, translation, and analysis. Ensure your HF API key is valid and that you have sufficient quota on Hugging Face.

- **Environment Variables:**  
  Always keep your secret keys and API keys secure and do not commit them to version control.

---

Happy testing and development!
```
