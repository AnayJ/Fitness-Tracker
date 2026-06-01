# Database Schema

## Overview
The Fitness Tracker uses PostgreSQL with three main tables: Users, Meals, and DailyLogs.

## Entity Relationship Diagram

```
┌─────────────┐
│    Users    │
├─────────────┤
│ id (PK)     │◄──────────┐
│ name        │           │
│ email       │           │
│ password    │           │
│ weight      │      ┌────────────┐
│ height      │      │   Meals    │
│ bmi         │      ├────────────┤
│ maintenance │      │ id (PK)    │
│ _calories   │      │ user_id (FK)
│ fitness_goal│      │ name       │
│ target_cal  │      │ description
│ created_at  │      │ calories   │
│ updated_at  │      │ protein    │
└─────────────┘      │ carbs      │
       ▲             │ fats       │
       │             │ meal_date  │
       │             │ created_at │
    ┌──┴──────┐      └────────────┘
    │ DailyLog│
    ├─────────┤
    │ id (PK) │
    │ user_id │
    │ (FK)    │
    │ log_date│
    │ total_* │
    │ exceeded
    │ created_at
    └─────────┘
```

## Tables

### Users Table

Stores user account and profile information.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    weight FLOAT,                    -- in kg
    height FLOAT,                    -- in cm
    bmi FLOAT,
    maintenance_calories FLOAT,
    fitness_goal VARCHAR(50),        -- 'lose', 'gain', 'maintain'
    target_calories FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

**Columns:**
- `id`: Unique user identifier
- `name`: User's full name
- `email`: Unique email address
- `password`: Hashed password
- `weight`: Body weight in kilograms
- `height`: Height in centimeters
- `bmi`: Calculated Body Mass Index
- `maintenance_calories`: Daily calorie burn at rest
- `fitness_goal`: Selected fitness goal (lose/gain/maintain)
- `target_calories`: Daily calorie target for goal
- `created_at`: Account creation timestamp
- `updated_at`: Last profile update timestamp

### Meals Table

Stores individual meal entries with nutritional information.

```sql
CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    calories FLOAT NOT NULL,
    protein FLOAT NOT NULL,          -- in grams
    carbs FLOAT NOT NULL,            -- in grams
    fats FLOAT NOT NULL,             -- in grams
    meal_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_meals_user_date ON meals(user_id, meal_date);
```

**Columns:**
- `id`: Unique meal identifier
- `user_id`: Foreign key to users table
- `name`: Meal name (e.g., "Breakfast", "Chicken and Rice")
- `description`: Detailed meal description
- `calories`: Total calories in meal
- `protein`: Protein content in grams
- `carbs`: Carbohydrate content in grams
- `fats`: Fat content in grams
- `meal_date`: When the meal was consumed
- `created_at`: When the entry was created

### DailyLogs Table

Stores daily aggregated nutrition data.

```sql
CREATE TABLE daily_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_calories FLOAT DEFAULT 0,
    total_protein FLOAT DEFAULT 0,
    total_carbs FLOAT DEFAULT 0,
    total_fats FLOAT DEFAULT 0,
    exceeded_target INTEGER DEFAULT 0,      -- boolean flag
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_daily_logs_user_date ON daily_logs(user_id, log_date);
```

**Columns:**
- `id`: Unique log identifier
- `user_id`: Foreign key to users table
- `log_date`: Date of the log entry
- `total_calories`: Sum of all meal calories for the day
- `total_protein`: Sum of all meal proteins for the day
- `total_carbs`: Sum of all meal carbs for the day
- `total_fats`: Sum of all meal fats for the day
- `exceeded_target`: Whether daily target was exceeded
- `created_at`: When log was created

## Relationships

### One-to-Many: User → Meals
- One user can have many meals
- Deleting a user cascades delete to all their meals

### One-to-Many: User → DailyLogs
- One user can have many daily log entries
- Deleting a user cascades delete to all their logs

## Data Types

| Type | Usage |
|------|-------|
| SERIAL | Auto-incrementing integer ID |
| VARCHAR(n) | Variable-length strings |
| TEXT | Long text descriptions |
| FLOAT | Decimal numbers (weight, calories) |
| TIMESTAMP | Date and time |
| INTEGER | Boolean flags (0/1) |

## Indexes

Indexes are created on frequently queried columns for performance:

1. `idx_users_email`: Fast email lookup for login
2. `idx_meals_user_date`: Fast meal retrieval by date for a user
3. `idx_daily_logs_user_date`: Fast daily log lookup by date

## Normalization

The schema follows **Third Normal Form (3NF)**:

1. **1NF**: All attributes are atomic (no repeating groups)
2. **2NF**: All non-key attributes are fully dependent on primary key
3. **3NF**: No transitive dependencies (non-key attributes don't depend on other non-key attributes)

## Sample Queries

### Get user's daily summary
```sql
SELECT 
    u.target_calories,
    COALESCE(SUM(m.calories), 0) as total_calories,
    COALESCE(SUM(m.protein), 0) as total_protein,
    COALESCE(SUM(m.carbs), 0) as total_carbs,
    COALESCE(SUM(m.fats), 0) as total_fats
FROM users u
LEFT JOIN meals m ON u.id = m.user_id 
    AND DATE(m.meal_date) = CURRENT_DATE
WHERE u.id = $1
GROUP BY u.id, u.target_calories;
```

### Get weekly trend
```sql
SELECT 
    DATE(meal_date) as meal_day,
    SUM(calories) as daily_calories
FROM meals
WHERE user_id = $1 
    AND meal_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE(meal_date)
ORDER BY meal_day DESC;
```

### Get user with highest calorie day
```sql
SELECT 
    u.name,
    SUM(m.calories) as total_calories,
    DATE(m.meal_date) as meal_date
FROM users u
JOIN meals m ON u.id = m.user_id
WHERE DATE(m.meal_date) = CURRENT_DATE
GROUP BY u.id, u.name, DATE(m.meal_date)
ORDER BY total_calories DESC
LIMIT 1;
```

## Constraints

### Primary Keys
- Ensure unique identification of each record
- Auto-increment for user convenience

### Foreign Keys
- Maintain referential integrity
- CASCADE delete prevents orphaned records

### Unique Constraints
- Email must be unique (prevents duplicate accounts)

### NOT NULL Constraints
- User name, email, password are required
- Meal name and calories are required
- Nutritional data is required

## Performance Considerations

1. **Indexing**: Composite indexes on user_id + date for fast filtering
2. **Partitioning**: Could partition daily_logs by date for large datasets
3. **Archive**: Old logs could be archived to improve query performance
4. **Denormalization**: Consider caching daily totals if data grows significantly

## Migration Strategy

When updating schema in development:

```bash
# List current tables
\dt

# Backup data
pg_dump fitness_tracker > backup.sql

# Make schema changes
ALTER TABLE table_name ADD COLUMN column_name TYPE;

# Verify changes
\d table_name
```

## Backup and Recovery

Regular backups are recommended:

```bash
# Full backup
pg_dump fitness_tracker > fitness_tracker_$(date +%Y%m%d).sql

# Restore from backup
psql fitness_tracker < fitness_tracker_20240115.sql
```
