# Quick Start Guide

## 30-Second Overview

Fitness Tracker is a full-stack application that helps users log daily meals, track calories and macros, and get AI-powered health insights.

## ⚡ Get Started in 5 Minutes

### Prerequisites
- Python 3.8+, Node.js 14+, PostgreSQL

### 1. Backend Setup (Terminal 1)
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

cp .env.example .env
# Edit .env with your PostgreSQL credentials

pip install -r requirements.txt
python init_db.py
python main.py
```

**Backend running at:** http://localhost:8000

### 2. Frontend Setup (Terminal 2)
```bash
cd frontend
npm install
cp .env.example .env
npm start
```

**Frontend running at:** http://localhost:3000

### 3. Start Using
1. Register new account
2. Complete onboarding (weight, height, goal)
3. Log meals on dashboard
4. View weekly reports

## 📚 Key Sections

| Section | Purpose |
|---------|---------|
| [README.md](../README.md) | Project overview & features |
| [SETUP.md](SETUP.md) | Detailed installation guide |
| [API.md](API.md) | Complete API reference |
| [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) | Database structure |
| [FEATURES.md](FEATURES.md) | Feature explanations |

## 🔑 Key Features

- ✅ User registration/login with JWT
- ✅ Profile setup with BMI and calorie calculations
- ✅ Daily meal logging with macros
- ✅ Real-time dashboard with progress charts
- ✅ AI fitness chatbot
- ✅ Weekly health reports
- ✅ ML-based calorie predictions
- ✅ Mobile responsive UI
- ✅ Secure password hashing

## 📁 Project Structure

```
backend/          # FastAPI application
├── app/          # Main code
│   ├── api/      # API routes
│   ├── core/     # Config & security
│   ├── db/       # Database
│   ├── models/   # SQLAlchemy models
│   ├── schemas/  # Pydantic schemas
│   ├── services/ # Business logic
│   ├── ml/       # Predictions
│   └── utils/    # Helpers

frontend/         # React application
├── src/
│   ├── pages/    # Page components
│   ├── context/  # Auth context
│   ├── services/ # API client
│   └── styles/   # Tailwind CSS

docs/             # Documentation
```

## 🔗 Useful URLs

| URL | Purpose |
|-----|---------|
| http://localhost:3000 | Frontend application |
| http://localhost:8000 | Backend API |
| http://localhost:8000/docs | API documentation |
| http://localhost:8000/redoc | API ReDoc |

## 🚀 Common Tasks

### Add a New API Endpoint
1. Create route in `backend/app/api/routes/`
2. Add business logic to `backend/app/services/`
3. Update schema in `backend/app/schemas/schemas.py`
4. Test at http://localhost:8000/docs

### Add a Frontend Component
1. Create component in `backend/src/components/`
2. Import and use in page
3. Style with Tailwind CSS classes
4. Test in browser

### Modify Database
1. Update model in `backend/app/models/models.py`
2. Delete and recreate database OR create migration
3. Run `python init_db.py`

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | Kill process: `lsof -i :8000` |
| DB connection error | Start PostgreSQL service |
| CORS error | Check REACT_APP_API_URL in .env |
| Module not found | Run `pip install -r requirements.txt` |

## 📝 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/fitness_tracker
SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## 💡 Next Steps

1. Read [SETUP.md](SETUP.md) for detailed instructions
2. Explore API at http://localhost:8000/docs
3. Check out [API.md](API.md) for endpoint details
4. Review [FEATURES.md](FEATURES.md) for feature documentation
5. Look at [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) for data structure

## 🎯 Common Use Cases

### User Registration
```
POST /auth/register
Body: {
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

### Log a Meal
```
POST /meals/
Body: {
  "name": "Breakfast",
  "calories": 400,
  "protein": 20,
  "carbs": 50,
  "fats": 10
}
```

### Get Daily Summary
```
GET /dashboard/summary
```

### Chat with AI
```
POST /ai/chat
Body: {
  "message": "What should I eat for dinner?"
}
```

## 📞 Support

- Check documentation files in `/docs`
- Review API docs at `/docs` endpoint
- Look for errors in terminal/console
- Verify database connection

---

**Ready to build your fitness tracker? Start with [SETUP.md](SETUP.md)!**
