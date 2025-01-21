# URL Shortener with Expiry and Analytics

## Overview
This project implements a URL shortener system using Django. 
It allows users to shorten URLs, track their usage analytics, 
and set expiration times for the shortened URLs. 
The system includes features like IP logging, timestamp logging, 
and optional configuration for future enhancements.

## Features
1. **Core Functionality**:
   - Create a unique shortened URL for any given long URL.
   - Ensures idempotency: the same long URL always generates the same shortened URL.
2. **Expiration**:
   - Allows users to set an expiration time for shortened URLs (default is 24 hours).
   - Expired URLs do not redirect to the original URL.
3. **Analytics**:
   - Tracks the number of accesses for each shortened URL.
   - Logs the timestamp and IP address for each access.
4. **Storage**:
   - Uses SQLite to store the original URL, shortened URL, creation timestamp, expiration timestamp, and access logs.
5. **API Endpoints**:
   - `POST /shorten`: Create a shortened URL.
   - `GET /<short_url>`: Redirect to the original URL if not expired.
   - `GET /analytics/<short_url>`: Retrieve analytics data for a specific shortened URL.
6. **Bonus Features**:
   - Hash-based short URL generation using `hashlib`.

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Django (Install via `pip install django`)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd url_shortener
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the SQLite database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Run the server:
   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`.

---

## API Endpoints

### 1. **Create a Shortened URL**
- **Endpoint**: `POST /shorten`
- **Description**: Creates a shortened URL for a given long URL.
- **Request Body**:
  ```json
  {
    "original_url": "http://example.com",
    "expiration_hours": 48
  }
  ```
- **Response**:
  ```json
  {
    "short_url": "http://127.0.0.1:8000/abc123"
  }
  ```

### 2. **Redirect to Original URL**
- **Endpoint**: `GET /<short_url>`
- **Description**: Redirects to the original URL if the shortened URL is not expired.
- **Response**:
  - **302 Found**: Redirects to the original URL.
  - **410 Gone**: If the URL has expired.
  - **404 Not Found**: If the short URL does not exist.

### 3. **Retrieve Analytics Data**
- **Endpoint**: `GET /analytics/<short_url>`
- **Description**: Fetches analytics data for a specific shortened URL.
- **Response**:
  ```json
  {
    "short_url": "abc123",
    "analytics": [
      {
        "access_time": "2025-01-20T12:34:56",
        "ip_address": "192.168.1.1"
      },
      {
        "access_time": "2025-01-20T13:01:12",
        "ip_address": "192.168.1.2"
      }
    ]
  }
  ```

---

## Future Enhancements
1. Add password protection for accessing shortened URLs.
2. Improve performance with caching for frequently accessed URLs.
3. Implement user authentication for personalized URL tracking.
4. Use a more scalable database (e.g., PostgreSQL) for production use.

---

## Example Data
To pre-populate the database with sample data, you can use the Django admin panel or a custom script. Example entries include:

- Original URL: `http://example.com`
- Shortened URL: `abc123`
- Expiration: 24 hours from creation.

---

