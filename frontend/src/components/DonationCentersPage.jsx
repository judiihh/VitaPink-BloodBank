import React from 'react';

const DonationCentersPage = ({ isOpen, onClose, onSwitchToRegister }) => {
  const handleGoogleMapsRedirect = () => {
    // Open Google Maps with search for blood donation centers
    window.open('https://www.google.com/maps/search/blood+donation+centers+near+me', '_blank');
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-3xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto custom-scrollbar">
        {/* Header */}
        <div className="bg-gradient-to-r from-vitapink-main to-vitapink-extra1 text-vitapink-extra4 p-6 rounded-t-3xl">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Find Donation Centers</h2>
            <button
              onClick={onClose}
              className="text-vitapink-extra4 hover:text-vitapink-extra3 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p className="text-vitapink-extra3 mt-2">Choose how you'd like to connect with donation centers</p>
        </div>

        {/* Content */}
        <div className="p-8 space-y-8">
          {/* Quick Lab Finder Option */}
          <div className="bg-gradient-to-br from-vitapink-lighter to-vitapink-light rounded-2xl p-6 border border-vitapink-extra1">
            <div className="text-center space-y-4">
              {/* Location Icon */}
              <div className="w-20 h-20 mx-auto bg-vitapink-extra2 rounded-full flex items-center justify-center shadow-lg">
                <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                </svg>
              </div>

              <h3 className="text-2xl font-bold text-vitapink-extra4">Quick Location Finder</h3>
              
              <p className="text-vitapink-extra3 text-lg leading-relaxed max-w-2xl mx-auto">
                Looking for nearby blood donation centers and laboratories? 
                Get instant directions and contact information for the closest facilities in your area.
              </p>

              <div className="pt-4">
                <button
                  onClick={handleGoogleMapsRedirect}
                  className="inline-flex items-center px-8 py-4 bg-vitapink-extra2 text-white rounded-2xl hover:bg-vitapink-extra3 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 text-lg font-semibold"
                >
                  <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                  </svg>
                  Find Centers Near Me
                </button>
              </div>

              <p className="text-sm text-vitapink-extra3">
                Opens Google Maps with nearby donation centers
              </p>
            </div>
          </div>

          {/* Divider */}
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t-2 border-vitapink-extra1"></div>
            </div>
            <div className="relative flex justify-center">
              <span className="px-6 bg-white text-vitapink-extra3 font-medium text-lg">OR</span>
            </div>
          </div>

          {/* Full Experience Option */}
          <div className="bg-gradient-to-br from-vitapink-light to-vitapink-main rounded-2xl p-6 border border-vitapink-extra1">
            <div className="text-center space-y-4">
              {/* Heart + Plus Icon */}
              <div className="w-20 h-20 mx-auto bg-vitapink-extra3 rounded-full flex items-center justify-center shadow-lg">
                <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" />
                </svg>
              </div>

              <h3 className="text-2xl font-bold text-vitapink-extra4">Complete Donor Experience</h3>
              
              <div className="text-vitapink-extra3 text-lg leading-relaxed max-w-2xl mx-auto space-y-3">
                <p>
                  Join our VitaPink community for a comprehensive donation experience:
                </p>
                
                <ul className="text-left space-y-2">
                  <li className="flex items-center">
                    <svg className="w-5 h-5 text-vitapink-extra2 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Track your complete donation history
                  </li>
                  <li className="flex items-center">
                    <svg className="w-5 h-5 text-vitapink-extra2 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Receive notifications when your blood type is urgently needed
                  </li>
                  <li className="flex items-center">
                    <svg className="w-5 h-5 text-vitapink-extra2 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Connect with certified donation centers in your area
                  </li>
                  <li className="flex items-center">
                    <svg className="w-5 h-5 text-vitapink-extra2 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Earn recognition for your life-saving contributions
                  </li>
                </ul>
              </div>

              <div className="pt-4">
                <button
                  onClick={() => {
                    onClose();
                    onSwitchToRegister && onSwitchToRegister();
                  }}
                  className="inline-flex items-center px-8 py-4 bg-vitapink-extra3 text-white rounded-2xl hover:bg-vitapink-extra4 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 text-lg font-semibold"
                >
                  <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z" />
                  </svg>
                  Join VitaPink Community
                </button>
              </div>

              <p className="text-sm text-vitapink-extra3">
                Start your journey as a registered VitaPink donor
              </p>
            </div>
          </div>

          {/* Back to Home */}
          <div className="text-center pt-4">
            <button
              onClick={onClose}
              className="text-vitapink-extra2 hover:text-vitapink-extra3 transition-colors font-medium"
            >
              ← Back to Home
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DonationCentersPage; 