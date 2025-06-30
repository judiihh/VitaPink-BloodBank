import React, { useState, useEffect } from 'react';
import { authUtils, userAPI } from '../utils/api';

const HomePage = ({ onLogout }) => {
  const [user, setUser] = useState(null);
  const [isActiveForDonation, setIsActiveForDonation] = useState(false);
  const [isUpdatingStatus, setIsUpdatingStatus] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Get user data from localStorage
    const userData = authUtils.getCurrentUser();
    if (userData) {
      setUser(userData);
      setIsActiveForDonation(userData.is_active || false);
    }
  }, []);

  const handleActiveStatusToggle = async () => {
    setIsUpdatingStatus(true);
    setMessage('');

    try {
      const newStatus = !isActiveForDonation;
      const response = await userAPI.updateActiveStatus({ isActive: newStatus });
      
      if (response.success) {
        setIsActiveForDonation(newStatus);
        
        // Update localStorage with new user data
        const updatedUser = { ...user, is_active: newStatus };
        localStorage.setItem('user', JSON.stringify(updatedUser));
        setUser(updatedUser);
        
        setMessage(newStatus ? 'You are now active for donation!' : 'You are now inactive for donation.');
      }
    } catch (error) {
      console.error('Error updating donation status:', error);
      setMessage('Error updating status. Please try again.');
    } finally {
      setIsUpdatingStatus(false);
      // Clear message after 3 seconds
      setTimeout(() => setMessage(''), 3000);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'No donations yet';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return 'Invalid date';
    }
  };

  const calculateAge = (birthDate) => {
    if (!birthDate) return 'N/A';
    try {
      const today = new Date();
      const birth = new Date(birthDate);
      let age = today.getFullYear() - birth.getFullYear();
      const monthDiff = today.getMonth() - birth.getMonth();
      
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
      }
      
      return age;
    } catch {
      return 'N/A';
    }
  };

  const getBloodTypeColor = (bloodType) => {
    const colors = {
      'A+': 'bg-red-100 text-red-800 border-red-200',
      'A-': 'bg-red-50 text-red-700 border-red-100',
      'B+': 'bg-blue-100 text-blue-800 border-blue-200',
      'B-': 'bg-blue-50 text-blue-700 border-blue-100',
      'AB+': 'bg-purple-100 text-purple-800 border-purple-200',
      'AB-': 'bg-purple-50 text-purple-700 border-purple-100',
      'O+': 'bg-green-100 text-green-800 border-green-200',
      'O-': 'bg-green-50 text-green-700 border-green-100'
    };
    return colors[bloodType] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-vitapink-lighter via-vitapink-light to-vitapink-main flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-vitapink-extra3 mx-auto mb-4"></div>
          <p className="text-vitapink-extra3">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-vitapink-lighter via-vitapink-light to-vitapink-main">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="h-full w-full bg-repeat" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.3'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
      </div>

      <div className="relative z-10 min-h-screen flex items-center justify-center p-4">
        {/* Main Dashboard Card */}
        <div className="w-full max-w-4xl bg-white rounded-3xl shadow-2xl overflow-hidden">
          
          {/* Header */}
          <div className="bg-gradient-to-r from-vitapink-main to-vitapink-extra1 text-vitapink-extra4 p-6">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-4">
                {/* Logo */}
                <div className="w-12 h-12">
                  <svg viewBox="0 0 120 120" className="w-full h-full">
                    <circle cx="60" cy="60" r="55" fill="#faf7f8" stroke="#d5a6bd" strokeWidth="2" />
                    <path d="M60 25 C45 35, 35 50, 35 65 C35 80, 47 90, 60 90 C73 90, 85 80, 85 65 C85 50, 75 35, 60 25 Z" fill="#741b47" />
                    <path d="M60 70 C55 65, 45 60, 45 52 C45 48, 48 45, 52 45 C55 45, 58 47, 60 50 C62 47, 65 45, 68 45 C72 45, 75 48, 75 52 C75 60, 65 65, 60 70 Z" fill="#ead1dc" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-2xl font-bold">Home</h1>
                  <p className="text-vitapink-extra3">VitaPink BloodBank Dashboard</p>
                </div>
              </div>
              
              <button
                onClick={onLogout}
                className="text-vitapink-extra4 hover:text-vitapink-extra3 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="p-8 space-y-8">
            
            {/* Welcome Message */}
            <div className="text-center">
              <h2 className="text-3xl font-bold text-vitapink-extra4 mb-2">
                ¡Bienvenido, {user.first_name}!
              </h2>
              <p className="text-vitapink-extra3">Welcome to your VitaPink BloodBank dashboard</p>
            </div>

            {/* Status Message */}
            {message && (
              <div className={`p-4 rounded-xl text-center ${
                message.includes('Error') 
                  ? 'bg-red-50 border border-red-200 text-red-600' 
                  : 'bg-green-50 border border-green-200 text-green-600'
              }`}>
                {message}
              </div>
            )}

            {/* Dashboard Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              {/* Blood Type Card */}
              <div className="bg-vitapink-main border border-vitapink-extra1 rounded-xl p-6 text-center">
                <h3 className="text-lg font-medium text-vitapink-extra4 mb-4">Tipo de Sangre</h3>
                <div className={`inline-block px-4 py-2 rounded-lg font-bold text-2xl ${getBloodTypeColor(user.blood_type)}`}>
                  {user.blood_type}
                </div>
                <p className="text-vitapink-extra3 text-sm mt-2">Your blood type</p>
              </div>

              {/* Donations Count Card */}
              <div className="bg-vitapink-main border border-vitapink-extra1 rounded-xl p-6 text-center">
                <h3 className="text-lg font-medium text-vitapink-extra4 mb-4">Donaciones</h3>
                <div className="text-4xl font-bold text-vitapink-extra4 mb-2">0</div>
                <p className="text-vitapink-extra3 text-sm">Total donations made</p>
              </div>

              {/* Last Donation Date Card */}
              <div className="bg-vitapink-main border border-vitapink-extra1 rounded-xl p-6 text-center">
                <h3 className="text-lg font-medium text-vitapink-extra4 mb-4">Última fecha de donación</h3>
                <div className="text-vitapink-extra4 font-medium mb-2">
                  {formatDate(user.last_donation_date)}
                </div>
                <p className="text-vitapink-extra3 text-sm">Last donation</p>
              </div>
            </div>

            {/* Active Status Toggle */}
            <div className="bg-vitapink-main border border-vitapink-extra1 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-medium text-vitapink-extra4 mb-2">
                    ¿Está Activo para donar?
                  </h3>
                  <p className="text-vitapink-extra3 text-sm">
                    Toggle your availability for blood donation
                  </p>
                </div>
                
                <div className="flex items-center space-x-4">
                  <span className={`text-sm font-medium ${!isActiveForDonation ? 'text-vitapink-extra4' : 'text-gray-400'}`}>
                    No
                  </span>
                  
                  <button
                    onClick={handleActiveStatusToggle}
                    disabled={isUpdatingStatus}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-vitapink-extra2 focus:ring-offset-2 ${
                      isActiveForDonation ? 'bg-green-500' : 'bg-vitapink-extra2'
                    } ${isUpdatingStatus ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        isActiveForDonation ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                  
                  <span className={`text-sm font-medium ${isActiveForDonation ? 'text-green-600' : 'text-gray-400'}`}>
                    Sí
                  </span>
                </div>
              </div>
              
              {isUpdatingStatus && (
                <div className="mt-4 text-center">
                  <div className="inline-flex items-center text-vitapink-extra3 text-sm">
                    <svg className="animate-spin -ml-1 mr-3 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Updating status...
                  </div>
                </div>
              )}
            </div>

            {/* User Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Contact Information */}
              <div className="bg-vitapink-main border border-vitapink-extra1 rounded-xl p-6">
                <div className="flex items-center mb-4">
                  <svg className="w-5 h-5 text-vitapink-extra4 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                  </svg>
                  <h4 className="font-medium text-vitapink-extra4">Contact Information</h4>
                </div>
                <div className="space-y-2 text-sm text-vitapink-extra3">
                  <p>{user.email}</p>
                  <p>{user.phone_number}</p>
                </div>
              </div>
              
              {/* Personal Information */}
              <div className="bg-vitapink-main border border-vitapink-extra1 rounded-xl p-6">
                <div className="flex items-center mb-4">
                  <svg className="w-5 h-5 text-vitapink-extra4 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                  </svg>
                  <h4 className="font-medium text-vitapink-extra4">Personal Information</h4>
                </div>
                <div className="space-y-2 text-sm text-vitapink-extra3">
                  <p>Name: <span className="font-medium text-vitapink-extra4">{user.first_name} {user.last_name}</span></p>
                  <p>Gender: <span className="font-medium text-vitapink-extra4">{user.gender}</span></p>
                  <p>Age: <span className="font-medium text-vitapink-extra4">{calculateAge(user.birth_date)} years</span></p>
                  <p>City: <span className="font-medium text-vitapink-extra4">{user.city}</span></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 