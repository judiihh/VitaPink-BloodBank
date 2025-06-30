# VitaPink BloodBank Backend

A Flask-based REST API for the VitaPink BloodBank management system with authentication, user management, and MySQL database integration.

## Features

- **User Authentication**: JWT-based login and registration
- **User Management**: Profile updates, password changes, account management
- **Database Integration**: MySQL database with proper connection management
- **Data Validation**: Comprehensive input validation for all user data
- **Security**: Password hashing with bcrypt, secure JWT tokens
- **CORS Support**: Configured for React frontend integration

## Database Schema

The backend expects a MySQL database with a `users` table containing:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('donor','admin','lab') DEFAULT 'donor',
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,
    gender ENUM('Male','Female') NOT NULL,
    blood_type ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    address VARCHAR(500) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    is_eligible TINYINT(1) DEFAULT 1,
    last_donation_date DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Database Configuration

Create a `.env` file in the backend directory with your database settings:

```env
# Flask Environment
FLASK_ENV=development

# Flask Security
SECRET_KEY=vitapink-bloodbank-secret-key-2025-change-this-in-production
JWT_SECRET_KEY=vitapink-jwt-secret-2025-change-this-in-production

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=vitapink_bloodbank
DB_USER=root
DB_PASSWORD=your_mysql_password_here

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

### 3. Create Database

1. Create a MySQL database named `vitapink_bloodbank` (or your preferred name)
2. Run the SQL schema above to create the `users` table
3. Update the `.env` file with your database credentials

### 4. Run the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication (`/api/auth`)

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/profile` - Get current user profile
- `POST /api/auth/logout` - Logout user

### User Management (`/api/users`)

- `PUT /api/users/profile` - Update user profile
- `PUT /api/users/change-password` - Change password
- `PUT /api/users/deactivate` - Deactivate account
- `PUT /api/users/eligibility` - Update donation eligibility

### Health Check

- `GET /health` - Health check endpoint
- `GET /` - API information

## Request/Response Format

### Registration Request
```json
{
    "email": "user@example.com",
    "username": "username123",
    "password": "password123",
    "confirmPassword": "password123",
    "firstName": "John",
    "lastName": "Doe",
    "phone": "555-1234567",
    "birthDate": "1990-01-01",
    "gender": "Male",
    "bloodType": "O+",
    "address": "123 Main St",
    "city": "City",
    "state": "State",
    "zipCode": "12345",
    "country": "Country",
    "canDonateNow": "yes",
    "lastDonationDate": "2024-01-01"
}
```

### Login Request
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

### Success Response
```json
{
    "success": true,
    "message": "Operation successful",
    "user": {
        "id": 1,
        "username": "username123",
        "email": "user@example.com",
        "role": "donor",
        "first_name": "John",
        "last_name": "Doe",
        // ... other user fields
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Error Response
```json
{
    "success": false,
    "message": "Error description"
}
```

## Frontend Integration

The backend is configured to work with the React frontend running on `http://localhost:3000`. Make sure both servers are running:

1. Backend: `python app.py` (runs on port 5000)
2. Frontend: `npm start` (runs on port 3000)

The frontend forms (LoginForm.jsx and RegisterForm.jsx) should make requests to:
- Login: `POST http://localhost:5000/api/auth/login`
- Register: `POST http://localhost:5000/api/auth/register`

## Security Features

- Password hashing with bcrypt
- JWT tokens for authentication
- Input validation and sanitization
- CORS protection
- SQL injection prevention with parameterized queries

## Development

The backend uses Flask application factory pattern for better organization:

- `app.py` - Main application entry point
- `config.py` - Configuration management
- `models/` - Database models
- `routes/` - API route handlers
- `utils/` - Utility functions (database, validation)

## Testing

To test the API endpoints, you can use tools like Postman or curl:

```bash
# Health check
curl http://localhost:5000/health

# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123","confirmPassword":"password123","firstName":"Test","lastName":"User","phone":"555-1234567","birthDate":"1990-01-01","gender":"Male","bloodType":"O+","address":"123 Test St","city":"Test City","state":"Test State","zipCode":"12345","country":"Test Country","canDonateNow":"yes"}'
``` 