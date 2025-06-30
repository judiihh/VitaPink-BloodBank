import React, { useState, useEffect } from 'react';
import RegisterForm from './components/RegisterForm';
import LoginForm from './components/LoginForm';
import DonationCentersPage from './components/DonationCentersPage';
import AuthStatus from './components/AuthStatus';
import HomePage from './components/HomePage';
import { authUtils } from './utils/api';

function App() {
  const [showRegisterForm, setShowRegisterForm] = useState(false);
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [showDonationCenters, setShowDonationCenters] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check if user is logged in when component mounts
  useEffect(() => {
    setIsLoggedIn(authUtils.isLoggedIn());
  }, []);

  // Handle successful login/registration
  const handleAuthSuccess = () => {
    setIsLoggedIn(true);
    setShowLoginForm(false);
    setShowRegisterForm(false);
  };

  // Handle logout
  const handleLogout = () => {
    authUtils.clearAuthData();
    setIsLoggedIn(false);
  };

  // If user is logged in, show the HomePage
  if (isLoggedIn) {
    return <HomePage onLogout={handleLogout} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-vitapink-lighter via-vitapink-light to-vitapink-main">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="h-full w-full bg-repeat" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.3'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
      </div>
      
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4">
        {/* Header Section */}
        <div className="text-center mb-16">
          {/* Logo */}
          <div className="mb-8">
            <div className="w-32 h-32 mx-auto drop-shadow-lg">
              <svg viewBox="0 0 120 120" className="w-full h-full">
                {/* Background Circle */}
                <circle
                  cx="60"
                  cy="60"
                  r="55"
                  fill="#faf7f8"
                  stroke="#d5a6bd"
                  strokeWidth="2"
                />
                
                {/* Blood Drop Shape */}
                <path
                  d="M60 25 C45 35, 35 50, 35 65 C35 80, 47 90, 60 90 C73 90, 85 80, 85 65 C85 50, 75 35, 60 25 Z"
                  fill="#741b47"
                  className="drop-shadow-md"
                />
                
                {/* Heart inside the drop */}
                <path
                  d="M60 70 C55 65, 45 60, 45 52 C45 48, 48 45, 52 45 C55 45, 58 47, 60 50 C62 47, 65 45, 68 45 C72 45, 75 48, 75 52 C75 60, 65 65, 60 70 Z"
                  fill="#ead1dc"
                  className="drop-shadow-sm"
                />
              </svg>
            </div>
          </div>
          
          {/* Title */}
          <h1 className="text-5xl md:text-6xl font-bold text-vitapink-extra4 mb-6 drop-shadow-sm">
            VitaPink BloodBank
          </h1>
          
          {/* Subtitle */}
          <p className="text-lg md:text-xl text-vitapink-extra4 max-w-2xl mx-auto leading-relaxed font-serif italic">
            "Connecting donors, saving lives."
          </p>
        </div>

        {/* Main Action Buttons */}
        <div className="w-full max-w-md space-y-6">
          {/* Sign In Button */}
          <button 
            onClick={() => setShowLoginForm(true)}
            className="w-full bg-vitapink-extra4 hover:bg-vitapink-darker text-white font-semibold py-4 px-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 text-lg"
          >
            <span className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1zm7.707 3.293a1 1 0 010 1.414L9.414 9H17a1 1 0 110 2H9.414l1.293 1.293a1 1 0 01-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Sign In
            </span>
          </button>

          {/* Sign Up Button */}
          <button 
            onClick={() => setShowRegisterForm(true)}
            className="w-full bg-vitapink-extra3 hover:bg-vitapink-extra4 text-white font-semibold py-4 px-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 text-lg"
          >
            <span className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z" />
              </svg>
              Sign Up Here!
            </span>
          </button>

          {/* Donation Centers Button */}
          <button 
            onClick={() => setShowDonationCenters(true)}
            className="w-full bg-vitapink-extra2 hover:bg-vitapink-extra3 text-white font-semibold py-4 px-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 text-lg"
          >
            <span className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
              </svg>
              Donation Centers
            </span>
          </button>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center">
          <p className="text-vitapink-dark text-sm">
            © 2025 VitaPink BloodBank. Connecting donors, saving lives.
          </p>
        </div>
      </div>

      {/* Register Form Modal */}
      <RegisterForm 
        isOpen={showRegisterForm} 
        onClose={() => setShowRegisterForm(false)}
        onSwitchToLogin={() => {
          setShowRegisterForm(false);
          setShowLoginForm(true);
        }}
        onAuthSuccess={handleAuthSuccess}
      />

      {/* Login Form Modal */}
      <LoginForm 
        isOpen={showLoginForm} 
        onClose={() => setShowLoginForm(false)}
        onSwitchToRegister={() => {
          setShowLoginForm(false);
          setShowRegisterForm(true);
        }}
        onAuthSuccess={handleAuthSuccess}
      />

      {/* Donation Centers Page Modal */}
      <DonationCentersPage
        isOpen={showDonationCenters}
        onClose={() => setShowDonationCenters(false)}
        onSwitchToRegister={() => {
          setShowDonationCenters(false);
          setShowRegisterForm(true);
        }}
      />

      {/* Auth Status Component - only show on landing page */}
      {!isLoggedIn && <AuthStatus />}
    </div>
  );
}

export default App; 