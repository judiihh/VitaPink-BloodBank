# VitaPink BloodBank App

A comprehensive platform connecting blood donors with blood centers, featuring real-time inventory tracking, donor management, and efficient communication systems.

## 🎯 Project Overview

The VitaPink BloodBank App addresses challenges in the blood donation ecosystem by:
- Increasing donor engagement through intuitive interfaces
- Improving inventory management with real-time tracking
- Streamlining communication between donors and blood centers
- Targeting Puerto Rico and Dominican Republic markets

## 🚀 Features

### Currently Implemented
- **User Authentication**: Secure registration, login, and JWT-based authentication
- **Profile Management**: Complete donor registration and profile updates
- **Database Integration**: MySQL with comprehensive schema for users, donations, locations, and inventory
- **Responsive Web Interface**: React-based frontend with modern UI components
- **Interactive Maps**: Leaflet/OpenStreetMap integration for location services
- **Multi-language Support**: Spanish and English interface
- **Real-time API**: RESTful Flask backend with comprehensive validation

### Donor Portal (Current & Planned)
- ✅ **Profile Management**: Complete donor registration and profile updates
- ✅ **Interactive Map**: Find nearby donation centers using Leaflet maps
- 🔄 **Donation History**: Track personal donation records and milestones
- 🔄 **Smart Alerts**: Receive notifications for blood type-specific urgent needs
- 🔄 **Digital Forms**: Complete health questionnaires and consent forms
- 🔄 **Eligibility Tracking**: Countdown to next donation eligibility

### Administrator Portal (Planned)
- 🔄 **Real-time Inventory**: Track blood units by type and expiration
- 🔄 **Donor Management**: View and manage donor information
- 🔄 **Stock Alerts**: Automated low-stock notifications
- 🔄 **Compliance Reporting**: AABB/FDA standards reporting
- 🔄 **Role-based Access**: Different permissions for technicians and supervisors

*Legend: ✅ Implemented | 🔄 In Development/Planned*

## 🛠 Technology Stack

### Backend
- **Framework**: Flask (Python 3.8+)
- **Database**: MySQL 8.0+
- **Authentication**: JWT (Flask-JWT-Extended)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **API Design**: RESTful architecture
- **Validation**: Marshmallow with custom validators
- **Security**: bcrypt password hashing, CORS support

### Frontend
- **Framework**: React 18.2.0
- **Styling**: Tailwind CSS 3.2.7
- **State Management**: React Query for API state
- **Forms**: React Hook Form 7.43.5
- **Maps**: React Leaflet 4.2.1 (OpenStreetMap/Leaflet)
- **Notifications**: React Hot Toast 2.4.0
- **Charts**: Recharts 2.5.0
- **Icons**: Heroicons 2.0.16

### Development Tools
- **Version Control**: Git + GitHub
- **Package Management**: npm (frontend), pip (backend)
- **API Testing**: Built-in health check endpoints
- **Testing**: pytest (backend), Jest (frontend) - *planned*
- **Linting**: ESLint for frontend
- **Cross-platform**: cross-env for environment variables

## 📦 Project Structure

```
VitaPink-BloodBank/
├── backend/                 # Flask API server
│   ├── app.py              # Application factory and main entry point
│   ├── config.py           # Configuration settings
│   ├── models/             # Database models
│   │   └── __init__.py
│   ├── routes/             # API route blueprints
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── users.py        # User management endpoints
│   │   └── __init__.py
│   ├── utils/              # Utility functions
│   │   ├── database.py     # Database utilities
│   │   └── __init__.py
│   ├── requirements.txt    # Python dependencies
│   └── venv/              # Virtual environment
├── frontend/               # React web application
│   ├── src/
│   │   ├── App.js         # Main application component
│   │   ├── components/    # React components
│   │   │   ├── AuthStatus.jsx
│   │   │   ├── ColorGuide.jsx
│   │   │   ├── DonationCentersPage.jsx
│   │   │   ├── HomePage.jsx
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── utils/
│   │   │   └── api.js      # API communication utilities
│   │   ├── index.css      # Global styles
│   │   └── index.js       # Application entry point
│   ├── assets/            # Static assets
│   ├── package.json       # Node.js dependencies
│   ├── tailwind.config.js # Tailwind CSS configuration
│   └── LogoVitaPink.png   # Application logo
├── database/              # Database schemas and setup
│   └── schema.sql         # MySQL database schema
├── color.txt              # Color scheme reference
└── README.md              # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/VitaPink-BloodBank.git
   cd VitaPink-BloodBank
   ```

2. **Database Setup**
   ```bash
   # Create MySQL database
   mysql -u root -p
   source database/schema.sql
   ```

3. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   
   # Set environment variables (create .env file)
   # FLASK_ENV=development
   # DATABASE_URL=mysql+pymysql://username:password@localhost/vitapink_bloodbank
   # JWT_SECRET_KEY=your-secret-key
   
   python app.py
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Health Check: http://localhost:5000/health

## 🌐 API Endpoints

### Current Implementation

#### Authentication (`/api/auth`)
- `POST /api/auth/register` - User registration with comprehensive validation
- `POST /api/auth/login` - User login with JWT token generation
- `POST /api/auth/refresh` - Refresh JWT access token
- `GET /api/auth/profile` - Get current user profile
- `POST /api/auth/logout` - User logout

#### User Management (`/api/users`)
- `PUT /api/users/profile` - Update user profile information
- `PUT /api/users/change-password` - Change user password
- `PUT /api/users/deactivate` - Deactivate user account
- `PUT /api/users/eligibility` - Update donation eligibility status

#### System
- `GET /health` - API health check
- `GET /` - API information and available endpoints

### Planned Endpoints

#### Inventory Management
- `GET /api/inventory` - Get blood inventory status
- `PUT /api/inventory/{blood_type}` - Update stock levels
- `GET /api/inventory/alerts` - Get low stock alerts

#### Donations
- `GET /api/donations` - Get donation history
- `POST /api/donations` - Record new donation
- `GET /api/donations/user/{id}` - Get user's donation history

#### Locations
- `GET /api/locations` - Get donation centers
- `GET /api/locations/{id}` - Get location details

## 🔒 Security Features

- JWT-based authentication with refresh tokens
- Password hashing using bcrypt
- Input validation and sanitization
- CORS configuration for cross-origin requests
- Role-based access control (donor, admin, lab)
- Account activation/deactivation controls
- HIPAA compliance considerations for future implementation

## 🌍 Internationalization

- English and Spanish language support
- Localized content for Puerto Rico market
- Cultural adaptations for target regions
- Support for both languages in database schema

## 📱 Future Mobile Support

- React Native app development planned
- Cross-platform iOS and Android support
- Push notification integration
- Offline capability planning
- GPS-based location services

## 🧪 Testing & Quality Assurance

### Current
- Backend input validation and error handling
- API health check endpoints
- Frontend linting with ESLint

### Planned
- Unit tests for backend API (pytest)
- Integration tests for database operations
- Frontend component testing (Jest)
- End-to-end testing protocols
- API documentation with Swagger/OpenAPI

## 🚀 Development Workflow

### Running in Development
```bash
# Backend (Terminal 1)
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py

# Frontend (Terminal 2)
cd frontend
npm start
```

### Environment Configuration
Create a `.env` file in the backend directory:
```env
FLASK_ENV=development
DATABASE_URL=mysql+pymysql://username:password@localhost/vitapink_bloodbank
JWT_SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript/React
- Write descriptive commit messages
- Update documentation for new features
- Test thoroughly before submitting PRs

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Judith Espinal** - Project Manager, Full-Stack Developer, UI/UX Designer
- **Lic. Yojanny Rosario** - Medical Technologist, Domain Expert, Researcher

## 📞 Contact

For questions or support, please contact:
- **Project Repository**: git@github.com:judiihh/VitaPink-BloodBank.git
- **Issues**: Please use GitHub Issues for bug reports and feature requests

## 🎯 Roadmap

### Phase 1 (Current - MVP)
- ✅ User authentication and profile management
- ✅ Database schema and basic API structure
- ✅ Frontend foundation with React
- 🔄 Interactive maps integration
- 🔄 Basic donation tracking

### Phase 2 (Q2 2024)
- 🔄 Complete inventory management system
- 🔄 Advanced donation scheduling
- 🔄 Push notifications system
- 🔄 Advanced reporting and analytics
- 🔄 Mobile app development

### Phase 3 (Q3-Q4 2024)
- 🔄 Hospital system integration
- 🔄 Advanced gamification features
- 🔄 Multi-region expansion support
- 🔄 AI-powered donor matching
- 🔄 Compliance and certification features

---

*Building a healthier future, one donation at a time* 🩸❤️ 