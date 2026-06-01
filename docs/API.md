# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "weight": null,
    "height": null,
    "bmi": null,
    "maintenance_calories": null,
    "fitness_goal": null,
    "target_calories": null,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

### Login
**POST** `/auth/login`

Authenticate user and receive access token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": { ... }
}
```

### Verify Token
**POST** `/auth/verify`

Verify if a token is valid.

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200):**
```json
{
  "valid": true,
  "user_id": 1
}
```

---

## User Endpoints

### Get User Profile
**GET** `/users/profile`

Get the current user's profile information.

**Response (200):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "weight": 75.5,
  "height": 180,
  "bmi": 23.29,
  "maintenance_calories": 2500,
  "fitness_goal": "lose",
  "target_calories": 2125,
  "created_at": "2024-01-15T10:30:00"
}
```

### Update User Profile
**PUT** `/users/profile`

Update user profile information.

**Request Body:**
```json
{
  "weight": 74.5,
  "height": 180,
  "fitness_goal": "maintain"
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "weight": 74.5,
  "height": 180,
  "bmi": 22.97,
  "maintenance_calories": 2500,
  "fitness_goal": "maintain",
  "target_calories": 2500,
  "created_at": "2024-01-15T10:30:00"
}
```

### Complete Onboarding
**POST** `/users/onboarding`

Complete user onboarding with fitness goal.

**Request Body:**
```json
{
  "weight": 75.5,
  "height": 180,
  "fitness_goal": "lose"
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "weight": 75.5,
  "height": 180,
  "bmi": 23.29,
  "maintenance_calories": 2500,
  "fitness_goal": "lose",
  "target_calories": 2125,
  "created_at": "2024-01-15T10:30:00"
}
```

### Get AI Goal Suggestion
**POST** `/users/suggest-goal`

Get AI-powered fitness goal suggestion.

**Query Parameters:**
- `weight` (float, required): Weight in kg
- `height` (float, required): Height in cm

**Response (200):**
```json
{
  "suggested_goal": "lose",
  "explanation": "Your BMI indicates you're overweight. A calorie deficit may help...",
  "target_calories": 2125,
  "weekly_projection": "At this goal, you may lose ~0.5 kg/week"
}
```

---

## Meal Endpoints

### Create Meal
**POST** `/meals/`

Log a new meal.

**Request Body:**
```json
{
  "name": "Chicken and Rice",
  "description": "Grilled chicken breast with brown rice and vegetables",
  "calories": 650,
  "protein": 45,
  "carbs": 65,
  "fats": 15
}
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Chicken and Rice",
  "description": "Grilled chicken breast with brown rice and vegetables",
  "calories": 650,
  "protein": 45,
  "carbs": 65,
  "fats": 15,
  "meal_date": "2024-01-15T12:00:00",
  "created_at": "2024-01-15T12:00:00"
}
```

### Get Daily Meals
**GET** `/meals/daily`

Get all meals for a specific date.

**Query Parameters:**
- `meal_date` (date, optional): Date in YYYY-MM-DD format (defaults to today)

**Response (200):**
```json
{
  "meals": [
    {
      "id": 1,
      "user_id": 1,
      "name": "Breakfast",
      "description": "Oatmeal with berries",
      "calories": 400,
      "protein": 15,
      "carbs": 60,
      "fats": 8,
      "meal_date": "2024-01-15T08:00:00",
      "created_at": "2024-01-15T08:00:00"
    }
  ],
  "total_calories": 400,
  "total_protein": 15,
  "total_carbs": 60,
  "total_fats": 8
}
```

### Get Specific Meal
**GET** `/meals/{meal_id}`

Get details of a specific meal.

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Breakfast",
  "description": "Oatmeal with berries",
  "calories": 400,
  "protein": 15,
  "carbs": 60,
  "fats": 8,
  "meal_date": "2024-01-15T08:00:00",
  "created_at": "2024-01-15T08:00:00"
}
```

### Update Meal
**PUT** `/meals/{meal_id}`

Update an existing meal.

**Request Body:**
```json
{
  "name": "Breakfast Updated",
  "description": "Oatmeal with berries and honey",
  "calories": 450,
  "protein": 15,
  "carbs": 65,
  "fats": 10
}
```

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Breakfast Updated",
  "description": "Oatmeal with berries and honey",
  "calories": 450,
  "protein": 15,
  "carbs": 65,
  "fats": 10,
  "meal_date": "2024-01-15T08:00:00",
  "created_at": "2024-01-15T08:00:00"
}
```

### Delete Meal
**DELETE** `/meals/{meal_id}`

Delete a meal.

**Response (200):**
```json
{
  "message": "Meal deleted successfully"
}
```

---

## Dashboard Endpoints

### Get Daily Summary
**GET** `/dashboard/summary`

Get today's dashboard summary.

**Query Parameters:**
- `meal_date` (date, optional): Date in YYYY-MM-DD format

**Response (200):**
```json
{
  "date": "2024-01-15",
  "target_calories": 2125,
  "consumed_calories": 1850,
  "remaining_calories": 275,
  "protein": 120,
  "carbs": 210,
  "fats": 65,
  "meal_count": 3,
  "meals": [ ... ],
  "exceeded": false,
  "prediction": {
    "current_calories": 1850,
    "projected_total": 2100,
    "target_calories": 2125,
    "remaining_calories": 25,
    "will_exceed": false,
    "exceeded_by": 0,
    "confidence": 66.7,
    "meals_logged": 3
  }
}
```

### Get Weekly Report
**GET** `/dashboard/weekly-report`

Get AI-generated weekly health report.

**Response (200):**
```json
{
  "report": "Weekly Health Report\n====================\n\nUser: John Doe\n...",
  "summary": {
    "days_tracked": 5,
    "avg_calories": 2000,
    "avg_protein": 120,
    "avg_carbs": 210,
    "avg_fats": 65,
    "target_calories": 2125,
    "daily_breakdown": {
      "2024-01-15": {
        "total_calories": 2100,
        "total_protein": 120,
        "total_carbs": 210,
        "total_fats": 65
      }
    }
  }
}
```

### Get Calorie Prediction
**GET** `/dashboard/prediction`

Get ML-based calorie prediction for today.

**Response (200):**
```json
{
  "current_calories": 1850,
  "projected_total": 2100,
  "target_calories": 2125,
  "remaining_calories": 25,
  "will_exceed": false,
  "exceeded_by": 0,
  "confidence": 66.7,
  "meals_logged": 3
}
```

### Get Weekly Trend
**GET** `/dashboard/weekly-trend`

Get 7-day calorie consumption trend.

**Response (200):**
```json
{
  "trend": {
    "2024-01-15": 2100,
    "2024-01-14": 2050,
    "2024-01-13": 1900,
    "2024-01-12": 2200,
    "2024-01-11": 2000,
    "2024-01-10": 2150,
    "2024-01-09": 1950
  },
  "target_calories": 2125
}
```

---

## AI Endpoints

### Chat with AI
**POST** `/ai/chat`

Get response from fitness AI chatbot.

**Request Body:**
```json
{
  "message": "What should I eat for dinner?",
  "history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hi! I'm your fitness assistant."
    }
  ]
}
```

**Response (200):**
```json
{
  "response": "For dinner, I'd recommend a balanced meal with lean protein, vegetables, and whole grains...",
  "suggested_action": null
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Token required"
}
```

### 404 Not Found
```json
{
  "detail": "Meal not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding in production.

## Pagination

Currently no pagination is implemented for list endpoints. Consider adding for scalability.

## Filtering

Currently limited filtering support. Consider enhancing for date ranges and user preferences.
