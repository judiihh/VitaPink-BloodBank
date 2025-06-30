import React, { useState } from 'react';

const LoginForm = ({ isOpen, onClose, onSwitchToRegister, onAuthSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

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
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (data.success) {
        // Store JWT tokens in localStorage
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        setMessage('Login successful! Welcome back.');
        
        // Trigger auth success callback after a brief delay to show success message
        setTimeout(() => {
          onAuthSuccess && onAuthSuccess();
        }, 1500);
      } else {
        setErrors({ general: data.message || 'Login failed' });
      }
    } catch (error) {
      console.error('Login error:', error);
      setErrors({ general: 'Network error. Please check your connection and try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-3xl shadow-2xl max-w-md w-full custom-scrollbar">
        {/* Header */}
        <div className="bg-gradient-to-r from-vitapink-main to-vitapink-extra1 text-vitapink-extra4 p-6 rounded-t-3xl">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Welcome Back!</h2>
            <button
              onClick={onClose}
              className="text-vitapink-extra4 hover:text-vitapink-extra3 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p className="text-vitapink-extra3 mt-2">Sign in to your VitaPink Account</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Login Information */}
          <div className="space-y-4">
            <div>
              <label className={labelClassName}>
                Email Address *
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
              <label className={labelClassName}>
                Password *
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className={inputClassName}
                placeholder="Enter your password"
              />
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="rememberMe"
                  checked={formData.rememberMe}
                  onChange={handleChange}
                  className="text-vitapink-extra2 focus:ring-vitapink-extra2 rounded"
                />
                <span className="ml-2 text-sm text-vitapink-extra3">Remember me</span>
              </label>
              
              <button
                type="button"
                className="text-sm text-vitapink-extra2 hover:text-vitapink-extra3 transition-colors"
              >
                Forgot password?
              </button>
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

          {/* Submit Button */}
          <div className="space-y-4">
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full px-6 py-3 text-white rounded-xl font-medium shadow-lg transition-colors ${
                isLoading 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-vitapink-extra2 hover:bg-vitapink-extra3'
              }`}
            >
              <span className="flex items-center justify-center">
                {isLoading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Signing In...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M3 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1zm7.707 3.293a1 1 0 010 1.414L9.414 9H17a1 1 0 110 2H9.414l1.293 1.293a1 1 0 01-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Sign In
                  </>
                )}
              </span>
            </button>

            <button
              type="button"
              onClick={onClose}
              className="w-full px-6 py-3 border border-vitapink-extra1 text-vitapink-extra2 rounded-xl hover:bg-vitapink-light transition-colors font-medium"
            >
              Cancel
            </button>
          </div>

          {/* Divider */}
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-vitapink-extra1"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-vitapink-extra3">Don't have an account?</span>
            </div>
          </div>

          {/* Sign Up Link */}
          <div className="text-center">
            <button
              type="button"
              onClick={() => {
                onClose();
                onSwitchToRegister && onSwitchToRegister();
              }}
              className="text-vitapink-extra2 hover:text-vitapink-extra3 transition-colors font-medium"
            >
              Create a new account
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm; 