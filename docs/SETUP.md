# Setup and Installation Guide

## Prerequisites

Before starting, ensure you have:

- **Python 3.8 or higher**
- **Node.js 14 or higher** 
- **PostgreSQL 12 or higher**
- **Git** (optional)
- **Code editor** (VS Code recommended)

## System-Specific Prerequisites

### Windows
```bash
# Check Python version
python --version

# Check Node version
node --version

# Install PostgreSQL from: https://www.postgresql.org/download/windows/
```

### macOS
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Install Node.js
brew install node

# Install PostgreSQL
brew install postgresql
```

### Linux (Ubuntu/Debian)
```bash
# Update package manager
sudo apt update

# Install Python
sudo apt install python3 python3-venv python3-pip

# Install Node.js
sudo apt install nodejs npm

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib
```

---

## Backend Setup (FastAPI + PostgreSQL)

### Step 1: Prepare Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Verify activation:**
```bash
# Windows - shows (venv) prefix
# macOS/Linux - shows (venv) in terminal
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Key packages:**
- `fastapi==0.104.1` - Web framework
- `sqlalchemy==2.0.23` - ORM
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `pydantic==2.5.0` - Data validation
- `python-jose==3.3.0` - JWT tokens

### Step 4: Setup PostgreSQL Database

#### Create Database and User

```sql
-- Connect to PostgreSQL (default user: postgres)
psql -U postgres

-- Create database
CREATE DATABASE fitness_tracker;

-- Create user
CREATE USER fitness_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
ALTER ROLE fitness_user SET client_encoding TO 'utf8';
ALTER ROLE fitness_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE fitness_user SET default_transaction_deferrable TO on;
ALTER ROLE fitness_user SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE fitness_tracker TO fitness_user;

-- Exit psql
\q
```

#### Verify Connection

```bash
psql -U fitness_user -d fitness_tracker
```

### Step 5: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env file with your settings
```

**Edit `.backend/.env`:**
```
# Database
DATABASE_URL=postgresql://fitness_user:your_secure_password@localhost:5432/fitness_tracker

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services (optional)
GEMINI_API_KEY=your-gemini-key-here
OPENAI_API_KEY=your-openai-key-here

# Server
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

**Generate SECRET_KEY (Unix/Linux/macOS):**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Generate SECRET_KEY (Windows):**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 6: Initialize Database

```bash
python init_db.py
```

**Expected output:**
```
Creating database tables...
Database tables created successfully!
```

### Step 7: Start Backend Server

```bash
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Access:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Step 8: Test Backend

```bash
# In a new terminal, test the health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy"}
```

---

## Frontend Setup (React + Tailwind CSS)

### Step 1: Navigate to Frontend

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

**Key packages:**
- `react==18.2.0` - UI library
- `react-router-dom==6.20.0` - Routing
- `tailwindcss==3.3.0` - Styling
- `axios==1.6.2` - HTTP client
- `chart.js==4.4.0` - Charts

### Step 3: Setup Environment Variables

```bash
# Copy example file
cp .env.example .env

# Verify .env content
cat .env
```

**`.env` file:**
```
REACT_APP_API_URL=http://localhost:8000
```

### Step 4: Start Development Server

```bash
npm start
```

**Expected output:**
```
Compiled successfully!

You can now view fitness-tracker in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Browser opens automatically at http://localhost:3000**

---

## Complete Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] PostgreSQL running
- [ ] Backend dependencies installed
- [ ] Database created
- [ ] Environment variables configured
- [ ] Backend database initialized
- [ ] Backend server running (port 8000)
- [ ] Frontend dependencies installed
- [ ] Frontend environment configured
- [ ] Frontend server running (port 3000)
- [ ] API docs accessible at /docs

---

## Quick Start Commands

### Start Everything (in separate terminals)

**Terminal 1: Backend**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

**Terminal 2: Frontend**
```bash
cd frontend
npm start
```

### Stop Everything

```bash
# In backend terminal: Ctrl+C
# In frontend terminal: Ctrl+C
```

---

## Troubleshooting

### PostgreSQL Connection Error

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solution:**
```bash
# Start PostgreSQL service
# Windows
net start postgresql-x64-15

# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find and kill process on port 8000 (backend)
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>

# For port 3000 (frontend)
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>
```

### Database Doesn't Exist

**Error:** `FATAL: database "fitness_tracker" does not exist`

**Solution:**
```bash
# Recreate database
psql -U postgres

# Inside psql:
DROP DATABASE IF EXISTS fitness_tracker;
CREATE DATABASE fitness_tracker;
GRANT ALL PRIVILEGES ON DATABASE fitness_tracker TO fitness_user;

# Then run
python init_db.py
```

### Virtual Environment Issues

**Problem:** Python packages not found

**Solution:**
```bash
# Ensure venv is activated (check for (venv) in terminal)
# If not activated:
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall packages
pip install -r requirements.txt
```

### CORS Errors

**Error:** `Access to XMLHttpRequest has been blocked by CORS policy`

**Solution:**
- Backend CORS is configured in `app/main.py`
- Ensure frontend API_URL matches backend address
- Verify `REACT_APP_API_URL=http://localhost:8000` in frontend `.env`

### Cannot Connect to Database

**Verify connection:**
```bash
# Test backend connection
python -c "from app.db.database import engine; engine.connect()"

# Test psql connection
psql -U fitness_user -d fitness_tracker -c "SELECT 1;"
```

---

## Development Tools

### Useful Commands

```bash
# Backend
python -m pytest  # Run tests
python -m black app  # Format code
python -m flake8 app  # Lint code

# Frontend
npm run build  # Production build
npm run test  # Run tests
npm run eject  # Eject from CRA (irreversible)
```

### Database Management

```bash
# Backup database
pg_dump -U fitness_user fitness_tracker > backup.sql

# Restore database
psql -U fitness_user fitness_tracker < backup.sql

# Connect to database
psql -U fitness_user -d fitness_tracker

# List tables
\dt

# View table structure
\d table_name
```

---

## Deployment Considerations

### Production Setup

1. **Security**
   - Change `SECRET_KEY` to a strong random value
   - Set `DEBUG=False`
   - Use environment variables for sensitive data
   - Setup HTTPS/SSL certificates

2. **Database**
   - Use managed PostgreSQL service (AWS RDS, Heroku)
   - Enable automated backups
   - Setup replication for high availability

3. **Backend**
   - Use production ASGI server (Gunicorn)
   - Setup load balancing (Nginx)
   - Enable logging and monitoring
   - Use environment-specific settings

4. **Frontend**
   - Build for production: `npm run build`
   - Deploy to CDN (Vercel, Netlify, AWS S3)
   - Enable caching headers
   - Setup monitoring

### Environment Variables for Production

```
DATABASE_URL=postgresql://user:pass@prod-db.rds.amazonaws.com:5432/fitness_tracker
SECRET_KEY=<strong-random-key-32-chars-minimum>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
CORS_ORIGINS=https://yourdomain.com
GEMINI_API_KEY=<your-api-key>
OPENAI_API_KEY=<your-api-key>
```

---

## Getting Help

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- PostgreSQL: https://www.postgresql.org/docs/
- Tailwind CSS: https://tailwindcss.com/docs

### Common Issues
See [Troubleshooting](#troubleshooting) section above

### Support
- Check existing GitHub issues
- Create new issue with error details
- Review error logs in terminal

---

## Next Steps

1. Explore the API at http://localhost:8000/docs
2. Register a new user account
3. Complete the onboarding flow
4. Start logging meals
5. Check weekly reports and AI insights

Enjoy your Fitness Tracker!
