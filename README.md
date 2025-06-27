# VitaPink BloodBank App

A comprehensive platform connecting blood donors with blood centers, featuring real-time inventory tracking, donor management, and efficient communication systems.

## 🎯 Project Overview

The VitaPink BloodBank App addresses challenges in the blood donation ecosystem by:
- Increasing donor engagement through intuitive interfaces
- Improving inventory management with real-time tracking
- Streamlining communication between donors and blood centers
- Targeting Puerto Rico and Dominican Republic markets

## 🚀 Features

### Donor Portal
- **Profile Management**: Complete donor registration and profile updates
- **Interactive Map**: Find nearby donation centers with real-time directions
- **Donation History**: Track personal donation records and milestones
- **Smart Alerts**: Receive push notifications for blood type-specific urgent needs
- **Digital Forms**: Complete health questionnaires and consent forms
- **Eligibility Tracking**: Countdown to next donation eligibility

### Administrator Portal
- **Real-time Inventory**: Track blood units by type and expiration
- **Donor Management**: View and manage donor information
- **Stock Alerts**: Automated low-stock notifications
- **Compliance Reporting**: AABB/FDA standards reporting
- **Role-based Access**: Different permissions for technicians and supervisors

## 🛠 Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **API Design**: RESTful architecture

### Frontend
- **Web**: React with HTML5/CSS3/JavaScript
- **Mobile**: React Native (cross-platform)
- **Maps**: Google Maps API integration
- **Notifications**: OneSignal push notifications

### Development Tools
- **Version Control**: Git + GitHub
- **API Testing**: Postman
- **Testing**: pytest (backend), Jest (frontend)

## 📦 Project Structure

```
VitaPink-BloodBank/
├── backend/                 # Flask API server
│   ├── app/
│   ├── models/
│   ├── routes/
│   └── requirements.txt
├── frontend/                # React web application
│   ├── src/
│   ├── public/
│   └── package.json
├── mobile/                  # React Native app
│   ├── src/
│   ├── android/
│   ├── ios/
│   └── package.json
├── database/               # Database schemas and migrations
└── docs/                   # Project documentation
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

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Database Setup**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Donor Management
- `GET /api/donors` - Get all donors (admin only)
- `GET /api/donors/{id}` - Get donor by ID
- `PUT /api/donors/{id}` - Update donor profile

### Inventory Management
- `GET /api/inventory` - Get blood inventory
- `PUT /api/inventory/{blood_type}` - Update stock levels
- `GET /api/inventory/alerts` - Get low stock alerts

### Donations
- `GET /api/donations` - Get donation history
- `POST /api/donations` - Record new donation
- `GET /api/donations/user/{id}` - Get user's donations

### Locations
- `GET /api/locations` - Get donation centers
- `GET /api/locations/{id}` - Get location details

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- HIPAA compliance considerations
- Data encryption for sensitive information

## 🌍 Internationalization

- English and Spanish language support
- Localized content for Puerto Rico and Dominican Republic
- Cultural adaptations for target markets

## 📱 Mobile Support

- Cross-platform React Native app
- Offline capability planning
- Push notification integration
- GPS-based location services

## 🧪 Testing

- Unit tests for backend API
- Integration tests for database operations
- Frontend component testing
- Manual testing protocols

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Judith Espinal** - Project Manager, Developer, Designer
- **Lic. Yojanny Rosario** - Medical Technologist, Researcher

## 📞 Contact

For questions or support, please contact:
- Email: your.email@example.com
- Project Repository: https://github.com/yourusername/VitaPink-BloodBank

## 🎯 Roadmap

### Phase 1 (MVP) - Current
- Basic donor and admin portals
- Real-time inventory tracking
- Interactive maps
- Push notifications

### Phase 2 - Future
- Advanced analytics
- Gamification features
- Extended language support
- Hospital system integration

---

*Building a healthier future, one donation at a time* 🩸❤️ 