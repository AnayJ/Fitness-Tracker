# Fitness Tracker - Comprehensive User-Friendly Application

A full-stack fitness tracking application built with React, FastAPI, and PostgreSQL, featuring AI-powered health insights and machine learning for calorie predictions.

## Features

### Core Features
- **User Management**: Secure registration and login with JWT authentication
- **Onboarding Flow**: Interactive profile setup with BMI calculation and maintenance calorie estimation
- **AI-Powered Goal Suggestion**: Let the LLM suggest personalized fitness goals based on your metrics
- **Meal Logging**: Easy daily meal tracking with macro nutrients
- **Dashboard**: Real-time visualization of daily progress, macro breakdown, and calorie predictions
- **Weekly Health Report**: AI-generated insights and recommendations
- **Fitness Chatbot**: Ask questions about your fitness journey and meal suggestions
- **Budget Warning System**: ML-based predictions for calorie surplus/deficit

## Tech Stack

### Frontend
- **React 18**: Modern UI with hooks
- **Tailwind CSS**: Responsive design
- **Chart.js**: Data visualization
- **Lucide Icons**: Beautiful icons
- **Axios**: API communication
- **React Router**: Navigation

### Backend
- **FastAPI**: High-performance Python framework
- **SQLAlchemy**: ORM for database interactions
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation
- **JWT**: Secure authentication
- **Scikit-learn**: ML predictions

### AI/ML
- **Gemini/OpenAI API**: LLM integration for AI suggestions
- **Linear Regression**: Calorie consumption predictions
- **Rule-based System**: Fallback recommendations

## Project Structure

```
P2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   ├── users.py         # User profile endpoints
│   │   │   │   ├── meals.py         # Meal logging endpoints
│   │   │   │   ├── dashboard.py     # Dashboard endpoints
│   │   │   │   └── ai.py            # AI chat endpoints
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py            # Configuration
│   │   │   ├── security.py          # JWT and password utilities
│   │   │   └── __init__.py
│   │   ├── db/
│   │   │   ├── database.py          # Database connection
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── models.py            # SQLAlchemy models
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── schemas.py           # Pydantic schemas
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── user_service.py      # User business logic
│   │   │   ├── meal_service.py      # Meal business logic
│   │   │   ├── ai_service.py        # AI/LLM integration
│   │   │   └── __init__.py
│   │   ├── ml/
│   │   │   ├── prediction_service.py # ML predictions
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   ├── calculators.py       # Calculation utilities
│   │   │   └── __init__.py
│   │   ├── main.py                  # FastAPI app
│   │   └── __init__.py
│   ├── main.py                      # Entry point
│   ├── init_db.py                   # Database initialization
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment template
│   └── README.md
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/              # Reusable components
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Onboarding.js
│   │   │   ├── Dashboard.js
│   │   │   ├── MealEntry.js
│   │   │   └── WeeklyReport.js
│   │   ├── services/
│   │   │   └── api.js               # API client
│   │   ├── context/
│   │   │   └── AuthContext.js       # Auth state management
│   │   ├── styles/
│   │   │   └── App.css
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   ├── .env.example
│   └── README.md
│
├── docs/
│   ├── API.md                       # API documentation
│   ├── DATABASE_SCHEMA.md           # Database schema
│   ├── SETUP.md                     # Setup instructions
│   └── FEATURES.md                  # Feature documentation
│
└── README.md (this file)
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

### Backend Setup

1. **Clone or navigate to the backend directory**
```bash
cd backend
```

2. **Create a virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials and API keys
```

5. **Initialize the database**
```bash
python init_db.py
```

6. **Run the server**
```bash
python main.py
```

The API will be available at `http://localhost:8000`. Access the interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

1. **Navigate to the frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Setup environment variables**
```bash
cp .env.example .env
# Make sure REACT_APP_API_URL points to your backend
```

4. **Start the development server**
```bash
npm start
```

The application will open at `http://localhost:3000`.

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/verify` - Verify token

### Users
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile
- `POST /users/onboarding` - Complete onboarding
- `POST /users/suggest-goal` - Get AI goal suggestion

### Meals
- `POST /meals/` - Create meal
- `GET /meals/daily` - Get meals for a date
- `GET /meals/{id}` - Get specific meal
- `PUT /meals/{id}` - Update meal
- `DELETE /meals/{id}` - Delete meal

### Dashboard
- `GET /dashboard/summary` - Get daily summary
- `GET /dashboard/weekly-report` - Get weekly report
- `GET /dashboard/prediction` - Get calorie prediction
- `GET /dashboard/weekly-trend` - Get weekly trend

### AI
- `POST /ai/chat` - Chat with fitness AI

## Usage Guide

### 1. Registration & Login
- Create a new account with name, email, and password
- Login with existing credentials

### 2. Onboarding
- Enter weight (kg) and height (cm)
- View your calculated BMI
- Choose fitness goal:
  - **Lose Weight** (15% calorie deficit)
  - **Gain Weight** (15% calorie surplus)
  - **Ask AI** (let LLM suggest based on BMI)
- Review and confirm settings

### 3. Daily Meal Logging
- Go to Dashboard → "Add Meal"
- Enter meal details:
  - Name and description
  - Calories
  - Macros (Protein, Carbs, Fats)
- View real-time daily progress

### 4. Dashboard Features
- **Calorie Progress**: Visual representation of daily intake vs target
- **Macro Breakdown**: Pie chart showing protein/carbs/fats
- **Meals List**: All logged meals with macro details
- **AI Prediction**: See if you'll exceed daily target
- **AI Chat**: Ask fitness questions

### 5. Weekly Report
- View 7-day summary statistics
- AI-generated insights and recommendations
- Daily breakdown with macros

## Features in Detail

### BMI Calculation
Formula: `BMI = weight (kg) / (height in meters)²`

### Maintenance Calories (Mifflin-St Jeor)
- For Men: `BMR = 10×weight + 6.25×height - 5×age + 5`
- For Women: `BMR = 10×weight + 6.25×height - 5×age - 161`
- Maintenance = BMR × 1.55 (moderate activity level)

### Calorie Prediction
Uses linear regression to predict end-of-day calorie consumption based on current intake and time of day.

### AI Integration
The system integrates with Gemini/OpenAI API to:
- Suggest personalized fitness goals
- Estimate weight change projections
- Generate weekly health reports
- Provide fitness chatbot responses

If no API is configured, the system uses rule-based suggestions.

## Mobile Responsiveness

All components are designed to be fully responsive:
- Mobile-first approach
- Tailwind CSS responsive classes
- Touch-friendly interface
- Optimized layouts for different screen sizes

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configured for frontend
- Token expiration (default: 30 minutes)
- Secure database connections with connection pooling

## Performance Optimizations

- Lazy loading of components
- Efficient database queries with SQLAlchemy ORM
- Caching of frequently accessed data
- Optimized Redux state management
- Code splitting with React Router

## Error Handling

- Comprehensive error messages
- Proper HTTP status codes
- Input validation with Pydantic
- Try-catch blocks for user-facing operations
- Database transaction rollback on failures

## Future Enhancements

- [ ] Recipe database integration
- [ ] Barcode scanning for meal logging
- [ ] Social features (friend tracking)
- [ ] Advanced analytics and trends
- [ ] Export reports to PDF
- [ ] Mobile app (React Native)
- [ ] Voice input for meal logging
- [ ] Detailed nutrition info from external APIs

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on the repository
- Check existing documentation in `/docs`
- Review API documentation at `/api/docs`

## Acknowledgments

- FastAPI for the excellent backend framework
- React for the powerful frontend library
- Chart.js for beautiful visualizations
- Tailwind CSS for utility-first styling
