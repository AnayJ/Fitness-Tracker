# Features Documentation

## Overview

This document provides detailed information about each feature of the Fitness Tracker application.

---

## 1. User Authentication & Management

### Registration
- **What it does**: Allows new users to create an account
- **Required information**: 
  - Full Name
  - Email address
  - Password (minimum 8 characters recommended)
- **Security**: Passwords are hashed using bcrypt
- **Response**: User is logged in and provided with JWT token
- **Redirect**: Onboarding flow

### Login
- **What it does**: Authenticate existing users
- **Required information**:
  - Email
  - Password
- **Token expiration**: 30 minutes (configurable)
- **Failed login**: Returns 401 Unauthorized
- **Redirect**: Dashboard if profile complete, else Onboarding

### Profile Management
- **Update profile**: Edit weight, height, and fitness goal
- **View profile**: See all profile information
- **BMI calculation**: Automatic calculation when weight/height updated
- **Maintenance calories**: Automatic calculation using Mifflin-St Jeor formula

---

## 2. Onboarding Flow

### Step 1: Measurements
- **Input**: Weight (kg) and Height (cm)
- **Output**: BMI calculation
- **Validation**: Both fields required, positive numbers only

### Step 2: Fitness Goal Selection
- **Three options**:
  1. **Lose Weight** - 15% calorie deficit from maintenance
  2. **Gain Weight** - 15% calorie surplus from maintenance
  3. **Ask AI** - Get personalized recommendation

### Step 3: Review & Confirm
- **Summary of all settings**:
  - Weight, Height, BMI
  - Fitness Goal
  - Daily Target Calories
  - Weekly projection (estimated weight change)
- **Confirmation**: Saves profile to database

---

## 3. Meal Logging

### Quick Add
- **Fields**:
  - Meal Name (required, e.g., "Breakfast", "Chicken and Rice")
  - Description (optional, e.g., "Grilled chicken with brown rice")
  - Calories (required)
  - Protein in grams (required)
  - Carbs in grams (required)
  - Fats in grams (required)

### Batch Logging
- **Add multiple meals** in single session
- **Total calculator** shows running totals
- **Delete meals** from the entry form before saving

### Meal History
- **View all meals** logged for a date
- **Edit meals** after logging
- **Delete meals** individually
- **Time tracking** shows when each meal was logged

### Macro Validation
- **Calorie calculation**: `Protein(g) × 4 + Carbs(g) × 4 + Fats(g) × 9`
- **System validates** entered calories match calculated macros (approximately)
- **Flexibility**: Some rounding tolerance allowed

---

## 4. Daily Dashboard

### Calorie Progress
- **Visual progress bar**:
  - Green when under target
  - Red when over target
  - Shows percentage of target reached
- **Display metrics**:
  - Consumed vs Target
  - Remaining calories
  - Excess (if any)

### Macro Breakdown
- **Pie chart showing**:
  - Protein (green) - essential for muscle growth
  - Carbohydrates (amber) - energy source
  - Fats (red) - hormone and nutrient absorption
- **Numerical display** of grams for each macro

### Meals List
- **Today's meals** displayed chronologically
- **Per-meal information**:
  - Name and description
  - Calorie count (highlighted)
  - Macro breakdown (icons + numbers)
- **Quick add button** to log new meal

### Prediction System
- **ML-based estimate** of end-of-day totals
- **Confidence level** based on data volume
- **Warning** if projected to exceed target
- **Recalculates** as new meals added

### Budget Warning System
- **Real-time prediction** using linear regression
- **Logic**:
  - Calculates hourly consumption rate
  - Projects remaining hours' consumption
  - Compares to daily target
  - Shows warning if exceeding
- **Confidence score** (0-100%) based on meals logged so far

---

## 5. Weekly Health Report

### AI-Generated Report
- **Automatic generation** from weekly data
- **Includes**:
  - Summary statistics (days tracked, averages)
  - Personalized insights based on goal
  - Recommendations for improvement
  - Motivational message

### Weekly Summary Stats
- **Days tracked** (count of non-zero days)
- **Average daily calories**
- **Average protein/carbs/fats**
- **vs Target** comparison

### Daily Breakdown
- **7-day history** displayed
- **Each day shows**:
  - Date (formatted, e.g., "Mon, Jan 15")
  - Total calories
  - Macro breakdown
- **Visual formatting** for easy scanning

### AI Insights
- **Personalized based on goal**:
  - For lose: Comments on deficit achievement
  - For gain: Comments on surplus achievement
  - For maintain: Comments on consistency
- **Macro balance feedback** (too much/little of something)
- **Actionable recommendations** specific to user data

---

## 6. AI Fitness Chatbot

### Features
- **Real-time responses** to fitness questions
- **Context-aware** using user profile data
- **Suggestion areas**:
  - What to eat for meals
  - Macro ratios
  - Progress tracking
  - Fitness tips

### Integration Options
1. **Gemini API**: If key configured, uses Google's LLM
2. **OpenAI API**: If key configured, uses OpenAI's GPT
3. **Rule-based fallback**: If no API available

### Chat History
- **Session history** maintained during browsing
- **Allows follow-up questions** with context
- **Clears** when user leaves page or logs out

### Response Examples
- Question: "What should I eat for dinner?"
  - Response: Balanced meal suggestions based on remaining calories
- Question: "Am I on track?"
  - Response: Compares current progress to goal targets
- Question: "What's a good macro ratio?"
  - Response: Personalized recommendations based on goal

---

## 7. Calculations & Formulas

### BMI (Body Mass Index)
```
BMI = weight (kg) / (height in meters)²

Example: 75 kg, 180 cm
BMI = 75 / (1.8)² = 75 / 3.24 = 23.15
```

### Maintenance Calories (Mifflin-St Jeor)
```
For Men:
BMR = 10×weight(kg) + 6.25×height(cm) - 5×age + 5
Maintenance = BMR × 1.55 (moderate activity)

For Women:
BMR = 10×weight(kg) + 6.25×height(cm) - 5×age - 161
Maintenance = BMR × 1.55 (moderate activity)

Example: 75kg, 180cm, 30-year-old male
BMR = 10×75 + 6.25×180 - 5×30 + 5 = 1680
Maintenance = 1680 × 1.55 = 2,604 calories/day
```

### Calorie Deficit/Surplus Projections
```
Weight change per week = Weekly calorie deficit ÷ 7,700
(1 kg body weight ≈ 7,700 calories)

Example: 15% deficit from 2,600 cal = 2,210 cal/day
Daily deficit = 2,600 - 2,210 = 390 calories
Weekly = 390 × 7 = 2,730 calories
Weight loss = 2,730 ÷ 7,700 = 0.35 kg/week
```

### Macro Calories
```
Protein: 1g = 4 calories
Carbohydrates: 1g = 4 calories
Fats: 1g = 9 calories

Example: 100g protein, 150g carbs, 60g fats
Protein: 100 × 4 = 400 cal
Carbs: 150 × 4 = 600 cal
Fats: 60 × 9 = 540 cal
Total: 400 + 600 + 540 = 1,540 calories
```

---

## 8. Data Predictions

### Calorie Consumption Prediction
- **Algorithm**: Linear regression (current intake / hours passed × total hours)
- **Updates**: Recalculates with each new meal
- **Confidence**: Based on percentage of day completed and meals logged
- **Use case**: Warn users if trending over budget early in day

### Weekly Trend Analysis
- **Displays**: 7-day calorie consumption history
- **Shows**: Daily totals across past week
- **Use case**: Identify patterns (weekends higher, weekdays lower, etc.)

---

## 9. Mobile Responsiveness

### Layout Breakpoints
- **Mobile** (< 640px): Single column, stacked layout
- **Tablet** (640px - 1024px): Two columns where applicable
- **Desktop** (> 1024px): Full multi-column layout

### Mobile Optimizations
- **Touch-friendly buttons**: Minimum 44×44 px
- **Simplified navigation**: Hamburger menu for mobile
- **Readable text**: Minimum 16px font on mobile
- **Optimized forms**: Single field per line on mobile
- **Performance**: Lazy loading of charts and data

### Responsive Components
- Dashboard: Collapses to single column
- Meal entry: Stacks inputs vertically
- Charts: Resize to available width
- Navigation: Hamburger menu on mobile

---

## 10. Security Features

### Password Security
- **Hashing**: bcrypt with salt
- **Requirements**: Can enforce minimum length
- **Reset**: Would require email verification (future feature)

### JWT Tokens
- **Encoding**: HS256 algorithm
- **Expiration**: 30 minutes (configurable)
- **Refresh**: Would need to re-login (future enhancement)
- **Storage**: localStorage on frontend

### Data Protection
- **CORS**: Configured for frontend origin only
- **SQL Injection**: Protected via SQLAlchemy ORM
- **XSS**: React escapes by default
- **HTTPS**: Recommended for production

---

## Future Enhancement Ideas

- [ ] **Barcode scanning** for quick meal logging
- [ ] **Recipe database** with common foods
- [ ] **Social features** (friends, challenges)
- [ ] **Advanced analytics** (trends, correlations)
- [ ] **Export functionality** (PDF reports)
- [ ] **Mobile app** (React Native)
- [ ] **Voice input** for hands-free logging
- [ ] **Reminder notifications** (time to log meals)
- [ ] **Integration with wearables** (Apple Watch, Fitbit)
- [ ] **Meal planning** (AI-generated weekly menus)
- [ ] **Restaurant database** (real meal values)
- [ ] **Achievement badges** (gamification)
- [ ] **Team/group tracking** (family goals)
- [ ] **API for third-party apps**

---

## Performance Metrics

### Target Performance
- **Page load time**: < 2 seconds
- **API response time**: < 500ms
- **Chart rendering**: < 1 second
- **Meal logging**: < 2 seconds to save

### Optimization Techniques
- Code splitting with React Router
- Image optimization
- Database query optimization
- Caching strategies
- CDN for static assets (production)

---

## Accessibility Features

### Current
- Semantic HTML elements
- Keyboard navigation support
- Color contrast compliance
- Icon + text labels

### Recommended Additions
- ARIA labels for complex components
- Screen reader testing
- Keyboard-only navigation guide
- High contrast mode option
- Larger text size option

---

## Support & Help

For detailed setup instructions, see [SETUP.md](SETUP.md)
For API reference, see [API.md](API.md)
For database details, see [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)
