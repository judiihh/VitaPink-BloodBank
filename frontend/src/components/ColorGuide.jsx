import React from 'react';

const ColorGuide = () => {
  const colors = [
    {
      name: 'White',
      variable: '--color-white',
      hex: '#ffffff',
      tailwind: 'secondary-50',
      description: 'Pure white for backgrounds and text on dark surfaces'
    },
    {
      name: 'Light Magenta 3',
      variable: '--color-light-magenta-3',
      hex: '#e1bee7',
      tailwind: 'primary-100',
      description: 'Lightest magenta for subtle backgrounds and hover states'
    },
    {
      name: 'Light Magenta 2',
      variable: '--color-light-magenta-2',
      hex: '#ce93d8',
      tailwind: 'primary-200',
      description: 'Light magenta for badges and secondary elements'
    },
    {
      name: 'Light Magenta 1',
      variable: '--color-light-magenta-1',
      hex: '#ab47bc',
      tailwind: 'primary-400',
      description: 'Medium light magenta for accents and highlights'
    },
    {
      name: 'Dark Magenta 1',
      variable: '--color-dark-magenta-1',
      hex: '#8e24aa',
      tailwind: 'primary-600',
      description: 'Primary brand color for buttons and important elements'
    },
    {
      name: 'Dark Magenta 2',
      variable: '--color-dark-magenta-2',
      hex: '#4a148c',
      tailwind: 'primary-900',
      description: 'Darkest magenta for text and strong emphasis'
    }
  ];

  const usageExamples = [
    {
      title: 'Primary Button',
      className: 'btn-vitapink',
      text: 'Donate Blood'
    },
    {
      title: 'Outline Button',
      className: 'btn-vitapink-outline',
      text: 'Learn More'
    },
    {
      title: 'Ghost Button',
      className: 'btn-vitapink-ghost',
      text: 'Cancel'
    },
    {
      title: 'Badge',
      className: 'badge-vitapink',
      text: 'O+ Donor'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto p-8 space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          VitaPink Color Palette
        </h1>
        <p className="text-lg text-gray-600">
          Google Docs Magenta Colors Applied to Your Blood Bank App
        </p>
      </div>

      {/* Color Palette */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {colors.map((color, index) => (
          <div key={index} className="card-vitapink">
            <div 
              className="w-full h-24 rounded-lg mb-4 border border-gray-200"
              style={{ backgroundColor: color.hex }}
            ></div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {color.name}
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Hex:</span>
                <span className="font-mono font-medium">{color.hex}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Tailwind:</span>
                <span className="font-mono text-xs">{color.tailwind}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">CSS Variable:</span>
                <span className="font-mono text-xs">{color.variable}</span>
              </div>
            </div>
            <p className="text-gray-600 text-sm mt-3">
              {color.description}
            </p>
          </div>
        ))}
      </div>

      {/* Usage Examples */}
      <div className="bg-gray-50 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Component Examples
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {usageExamples.map((example, index) => (
            <div key={index} className="text-center">
              <h3 className="text-sm font-medium text-gray-600 mb-3">
                {example.title}
              </h3>
              <button className={example.className}>
                {example.text}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Blood Type Cards with New Colors */}
      <div className="bg-white rounded-xl p-8 border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Blood Inventory Cards (With Magenta Theme)
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].map((bloodType) => (
            <div key={bloodType} className="bg-primary-50 border border-primary-200 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-primary-800 mb-2">
                {bloodType}
              </div>
              <div className="text-sm text-primary-600">
                2,450 mL
              </div>
              <div className="mt-2">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                  Normal
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Status Indicators */}
      <div className="bg-white rounded-xl p-8 border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Status Indicators
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="status-critical p-4 rounded-lg text-center">
            <div className="font-semibold">Critical</div>
            <div className="text-sm">Below 50% threshold</div>
          </div>
          <div className="status-low p-4 rounded-lg text-center">
            <div className="font-semibold">Low Stock</div>
            <div className="text-sm">Below minimum threshold</div>
          </div>
          <div className="status-normal p-4 rounded-lg text-center">
            <div className="font-semibold">Normal</div>
            <div className="text-sm">Adequate supply</div>
          </div>
          <div className="notification-info text-center">
            <div className="font-semibold">Info</div>
            <div className="text-sm">Using VitaPink magenta</div>
          </div>
        </div>
      </div>

      {/* App Preview */}
      <div className="bg-gradient-to-br from-primary-50 to-primary-100 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-primary-900 mb-6">
          App Header Preview
        </h2>
        <div className="bg-white rounded-lg shadow-medium p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">VitaPink</h1>
                <p className="text-sm text-gray-600">Blood Bank System</p>
              </div>
            </div>
            <div className="flex space-x-3">
              <button className="btn-vitapink-ghost">
                Profile
              </button>
              <button className="btn-vitapink">
                Donate Now
              </button>
            </div>
          </div>
          <div className="border-t border-gray-200 pt-4">
            <p className="text-gray-600">
              Beautiful magenta theme applied throughout your blood bank application,
              creating a cohesive and professional appearance.
            </p>
          </div>
        </div>
      </div>

      {/* CSS Usage Instructions */}
      <div className="bg-gray-900 text-white rounded-xl p-8">
        <h2 className="text-2xl font-bold mb-6">
          How to Use These Colors
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-300">
              Tailwind Classes
            </h3>
            <div className="bg-gray-800 rounded p-4 font-mono text-sm space-y-2">
              <div><span className="text-blue-400">bg-primary-600</span> <span className="text-gray-400">// Dark Magenta 1</span></div>
              <div><span className="text-blue-400">text-primary-900</span> <span className="text-gray-400">// Dark Magenta 2</span></div>
              <div><span className="text-blue-400">border-primary-400</span> <span className="text-gray-400">// Light Magenta 1</span></div>
              <div><span className="text-blue-400">bg-primary-100</span> <span className="text-gray-400">// Light Magenta 3</span></div>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-3 text-primary-300">
              CSS Variables
            </h3>
            <div className="bg-gray-800 rounded p-4 font-mono text-sm space-y-2">
              <div><span className="text-green-400">var(--color-primary)</span></div>
              <div><span className="text-green-400">var(--color-primary-light)</span></div>
              <div><span className="text-green-400">var(--color-primary-dark)</span></div>
              <div><span className="text-green-400">var(--color-white)</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ColorGuide; 