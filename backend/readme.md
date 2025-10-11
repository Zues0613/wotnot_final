# Backend Setup Instructions

This backend is powered by **FastAPI** and uses **Uvicorn** as the ASGI server. We also use **Dramatiq** for task processing.

---

## 🔧 Setup Instructions

## make sure you use python 3.12.3
### 1. Create and Activate a Virtual Environment

Open your terminal and navigate to the `backend/` folder:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

---

### 2. Install Dependencies

Install the required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 3. Database Migration

Before running the server for the first time, create the database tables:

```bash
python migrate_db.py --action create
```

**Migration Options:**
- `--action create` - Create all tables (default)
- `--action drop` - Drop all tables (requires confirmation)
- `--action recreate` - Drop and recreate all tables (requires confirmation)

**Note:** The tables will also be created automatically when you start the server for the first time.

---

## 🚀 Running the Backend Server

To start the FastAPI server with **Uvicorn**:

```bash
uvicorn wati.main:app --reload --port 8000
```

- `--reload` enables hot-reloading during development.
- The server will be available at: `http://localhost:8000`

---

## 🧵 Running the Dramatiq Worker

## pip install dramatiq
Open a **new terminal window**, and make sure to activate the same virtual environment:

```bash
cd backend
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Then run the Dramatiq worker:

```bash
dramatiq wati.services.tasks
```

This command will start the worker that processes background tasks defined in `wati/services/tasks.py`.

---

## 📁 Project Structure Overview

```
backend/
│
├── venv/                   # Virtual environment
├── wati/
│   ├── main.py             # FastAPI app entry point
│   └── services/
│       └── tasks.py        # Dramatiq tasks
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ✅ Prerequisites & Notes

### **Redis is REQUIRED for Background Tasks**

This application uses **Dramatiq** for background task processing (broadcasts, scheduled messages). Dramatiq requires **Redis** to be running.

#### **Install Redis:**
- **Windows:** Download from [https://redis.io/download](https://redis.io/download) or use [Memurai](https://www.memurai.com/)
- **macOS:** `brew install redis`
- **Linux:** `sudo apt-get install redis-server` or `sudo yum install redis`

#### **Start Redis:**

**Option 1: Using the provided startup script (Recommended):**
```bash
# From backend directory
.\start_redis.bat
```

**Option 2: Manual start:**
```bash
# Navigate to Redis folder
cd %USERPROFILE%\Redis
redis-server.exe redis.windows.conf
```

#### **Verify Redis is Running:**
```bash
redis-cli ping
# Should respond: PONG
```

**Note:** Redis is installed at: `C:\Users\[YourUsername]\Redis\`

### **Important Configuration Notes:**

1. **Redis URL Configuration:**
   - Default: `redis://localhost:6379`
   - Configured in: `wati/services/tasks.py` (line 170)
   - Change if your Redis runs on a different host/port

2. **WhatsApp Business API:**
   - Templates MUST be approved by WhatsApp before use
   - Rate limit: ~80 messages/second (implemented at 20 msg/sec for safety)
   - Templates saved locally even if API disabled for testing

3. **Database:**
   - Uses PostgreSQL (async SQLAlchemy)
   - Configure connection in `.env` file

4. **Environment Variables:**
   - Use `.env` file for sensitive configuration (DB URLs, API keys, Redis URI)

### **Performance Optimizations Applied:**

✅ **Batch Database Commits** - Commits all logs after broadcast completion (not per message)
✅ **Rate Limiting** - 20 messages/second to prevent WhatsApp throttling
✅ **Error Resilience** - Broadcasts complete even if some messages fail
✅ **Async Processing** - Non-blocking broadcast execution via Dramatiq

---

Happy hacking! 🚀
