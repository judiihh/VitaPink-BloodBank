import React, { useState, useEffect } from 'react';
import { authUtils, authAPI } from '../utils/api';

const AuthStatus = () => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    // Check if user is logged in when component mounts
    if (authUtils.isLoggedIn()) {
      setUser(authUtils.getCurrentUser());
    }
  }, []);

  const handleLogout = async () => {
    setIsLoading(true);
    try {
      await authAPI.logout();
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error);
      // Clear local data even if API call fails
      authUtils.clearAuthData();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) {
    return null; // Don't show anything if not logged in
  }

  return (
    <div className="fixed top-4 right-4 z-40">
      <div className="bg-white rounded-xl shadow-lg border border-vitapink-extra1 p-4 max-w-sm">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span className="text-sm font-medium text-vitapink-extra3">Logged in</span>
          </div>
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="text-vitapink-extra2 hover:text-vitapink-extra3 text-xs"
          >
            {showDetails ? 'Hide' : 'Show'}
          </button>
        </div>
        
        <div className="text-sm text-gray-600 mb-3">
          Welcome, <span className="font-medium text-vitapink-extra3">{user.first_name} {user.last_name}</span>
        </div>

        {showDetails && (
          <div className="text-xs text-gray-500 mb-3 space-y-1">
            <div><strong>Email:</strong> {user.email}</div>
            <div><strong>Username:</strong> {user.username}</div>
            <div><strong>Role:</strong> {user.role}</div>
            <div><strong>Blood Type:</strong> {user.blood_type}</div>
            <div><strong>Eligible:</strong> {user.is_eligible ? 'Yes' : 'No'}</div>
          </div>
        )}
        
        <button
          onClick={handleLogout}
          disabled={isLoading}
          className={`w-full text-xs px-3 py-2 rounded-lg transition-colors ${
            isLoading 
              ? 'bg-gray-200 text-gray-500 cursor-not-allowed' 
              : 'bg-vitapink-extra2 text-white hover:bg-vitapink-extra3'
          }`}
        >
          {isLoading ? 'Logging out...' : 'Logout'}
        </button>
      </div>
    </div>
  );
};

export default AuthStatus; 