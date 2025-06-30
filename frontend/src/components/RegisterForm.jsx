import React, { useState } from 'react';

const RegisterForm = ({ isOpen, onClose, onSwitchToLogin, onAuthSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    phoneNumber: '',
    birthDate: '',
    gender: '',
    bloodType: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
    country: '',
    canDonateNow: '',
    lastDonationDate: '',
    isActive: true
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
  const genders = ['Male', 'Female'];

  // Common input styling with proper text visibility and light pink theme
  const inputClassName = "w-full px-4 py-3 border border-vitapink-extra1 rounded-xl focus:outline-none focus:ring-2 focus:ring-vitapink-extra2 focus:border-transparent text-gray-900 bg-white placeholder-gray-500";
  
  // Common label styling with light pink theme
  const labelClassName = "block text-sm font-medium text-vitapink-extra3 mb-2";

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrors({});
    setMessage('');

    try {
      const response = await fetch('http://localhost:5000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          username: formData.username,
          password: formData.password,
          confirmPassword: formData.confirmPassword,
          firstName: formData.firstName,
          lastName: formData.lastName,
          phone: formData.phoneNumber, // Backend expects 'phone', not 'phoneNumber'
          birthDate: formData.birthDate,
          gender: formData.gender,
          bloodType: formData.bloodType,
          address: formData.address,
          city: formData.city,
          state: formData.state,
          zipCode: formData.zipCode,
          country: formData.country,
          canDonateNow: formData.canDonateNow,
          lastDonationDate: formData.lastDonationDate || null,
        }),
      });

      const data = await response.json();

      if (data.success) {
        // Store JWT tokens in localStorage
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        setMessage('Registration successful! Welcome to VitaPink BloodBank.');
        
        // Trigger auth success callback after a brief delay to show success message
        setTimeout(() => {
          onAuthSuccess && onAuthSuccess();
        }, 2000);
      } else {
        setErrors({ general: data.message || 'Registration failed' });
      }
    } catch (error) {
      console.error('Registration error:', error);
      setErrors({ general: 'Network error. Please check your connection and try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-3xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto custom-scrollbar">
        {/* Header */}
        <div className="bg-gradient-to-r from-vitapink-main to-vitapink-extra1 text-vitapink-extra4 p-6 rounded-t-3xl">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Register New Donor</h2>
            <button
              onClick={onClose}
              className="text-vitapink-extra4 hover:text-vitapink-extra3 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Account Information */}
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-vitapink-extra3 border-b border-vitapink-extra1 pb-2">
              Account Information
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Email *
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                  placeholder="your.email@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Username *
                </label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                  placeholder="Choose a username"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Password *
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                  placeholder="Create a secure password"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Confirm Password *
                </label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                  placeholder="Confirm your password"
                />
              </div>
            </div>
          </div>

          {/* Personal Information */}
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-vitapink-extra3 border-b border-vitapink-extra1 pb-2">
              Personal Information
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  First Name *
                </label>
                <input
                  type="text"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                  placeholder="Your first name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Last Name *
                </label>
                <input
                  type="text"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                  placeholder="Your last name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Phone Number *
                </label>
                <input
                  type="tel"
                  name="phoneNumber"
                  value={formData.phoneNumber}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                  placeholder="(555) 123-4567"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Birth Date *
                </label>
                <input
                  type="date"
                  name="birthDate"
                  value={formData.birthDate}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Gender *
                </label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                >
                  <option value="">Select gender</option>
                  {genders.map(gender => (
                    <option key={gender} value={gender}>{gender}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Blood Type *
                </label>
                <select
                  name="bloodType"
                  value={formData.bloodType}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                >
                  <option value="">Select blood type</option>
                  {bloodTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Address Information */}
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-vitapink-extra3 border-b border-vitapink-extra1 pb-2">
              Address Information
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Street Address *
                </label>
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                  required
                  className={inputClassName}
                  placeholder="123 Main Street"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-vitapink-dark mb-2">
                    City *
                  </label>
                  <input
                    type="text"
                    name="city"
                    value={formData.city}
                    onChange={handleChange}
                    required
                    className={inputClassName}
                    placeholder="City"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-vitapink-dark mb-2">
                    State *
                  </label>
                  <input
                    type="text"
                    name="state"
                    value={formData.state}
                    onChange={handleChange}
                    required
                    className={inputClassName}
                    placeholder="State"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-vitapink-dark mb-2">
                    Zip Code *
                  </label>
                  <input
                    type="text"
                    name="zipCode"
                    value={formData.zipCode}
                    onChange={handleChange}
                    required
                    className={inputClassName}
                    placeholder="12345"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-vitapink-dark mb-2">
                    Country *
                  </label>
                  <input
                    type="text"
                    name="country"
                    value={formData.country}
                    onChange={handleChange}
                    required
                    className={inputClassName}
                    placeholder="Country"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Donation Information */}
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-vitapink-extra3 border-b border-vitapink-extra1 pb-2">
              Donation Information
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Can you donate right now? *
                </label>
                <div className="flex space-x-4">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="canDonateNow"
                      value="yes"
                      checked={formData.canDonateNow === 'yes'}
                      onChange={handleChange}
                      className="text-vitapink-extra2 focus:ring-vitapink-extra2"
                    />
                    <span className="ml-2 text-vitapink-extra3">Yes</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="canDonateNow"
                      value="no"
                      checked={formData.canDonateNow === 'no'}
                      onChange={handleChange}
                      className="text-vitapink-extra2 focus:ring-vitapink-extra2"
                    />
                    <span className="ml-2 text-vitapink-extra3">No</span>
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-vitapink-dark mb-2">
                  Last Donation Date (if applicable)
                </label>
                <input
                  type="date"
                  name="lastDonationDate"
                  value={formData.lastDonationDate}
                  onChange={handleChange}
                  className={inputClassName}
                />
              </div>
            </div>
          </div>

          {/* Error/Success Messages */}
          {errors.general && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl">
              <p className="text-red-600 text-sm">{errors.general}</p>
            </div>
          )}
          
          {message && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-xl">
              <p className="text-green-600 text-sm">{message}</p>
            </div>
          )}

          {/* Submit Buttons */}
          <div className="flex justify-end space-x-4 pt-6 border-t border-vitapink-extra1">
            <button
              type="button"
              onClick={onClose}
              disabled={isLoading}
              className={`px-6 py-3 border border-vitapink-extra1 text-vitapink-extra2 rounded-xl transition-colors font-medium ${
                isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-vitapink-light'
              }`}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className={`px-6 py-3 text-white rounded-xl font-medium shadow-lg transition-colors ${
                isLoading 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-vitapink-extra2 hover:bg-vitapink-extra3'
              }`}
            >
              {isLoading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Registering...
                </span>
              ) : (
                'Register Now'
              )}
            </button>
          </div>

          {/* Login Link */}
          <div className="text-center pt-4 border-t border-vitapink-extra1">
            <p className="text-sm text-vitapink-extra3">
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => {
                  onClose();
                  onSwitchToLogin && onSwitchToLogin();
                }}
                className="text-vitapink-extra2 hover:text-vitapink-extra3 transition-colors font-medium"
              >
                Sign in here!
              </button>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterForm; 