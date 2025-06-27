/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        // VitaPink Brand Colors - Google Docs Magenta Palette
        primary: {
          50: '#f3e5f5',   // Very light magenta
          100: '#e1bee7',  // Light magenta 3
          200: '#ce93d8',  // Light magenta 2
          300: '#ba68c8',  // Light magenta 1
          400: '#ab47bc',  // Light magenta 1
          500: '#9c27b0',  // Main magenta
          600: '#8e24aa',  // Dark magenta 1
          700: '#7b1fa2',  // Darker magenta
          800: '#6a1b9a',  // Dark magenta 1
          900: '#4a148c'   // Dark magenta 2
        },
        secondary: {
          50: '#ffffff',   // White
          100: '#f8f5f9',  // Very light tint
          200: '#f3e5f5',  // Light tint
          300: '#e1bee7',  // Light magenta 3
          400: '#ce93d8',  // Light magenta 2
          500: '#ba68c8',  // Medium magenta
          600: '#ab47bc',  // Light magenta 1
          700: '#9c27b0',  // Main magenta
          800: '#8e24aa',  // Dark magenta 1
          900: '#6a1b9a'   // Dark magenta 1
        },
        // VitaPink specific colors using Google Docs Magenta
        vitapink: {
          white: '#ffffff',        // White
          lightMagenta3: '#e1bee7', // Light magenta 3
          lightMagenta2: '#ce93d8', // Light magenta 2
          lightMagenta1: '#ab47bc', // Light magenta 1
          darkMagenta1: '#8e24aa',  // Dark magenta 1
          darkMagenta2: '#4a148c'   // Dark magenta 2
        },
        success: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d'
        },
        warning: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f'
        },
        danger: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d'
        },
        // Blood type colors
        blood: {
          'A+': '#ff6b6b',
          'A-': '#ff5252',
          'B+': '#4ecdc4',
          'B-': '#26a69a',
          'AB+': '#ab47bc',
          'AB-': '#8e24aa',
          'O+': '#66bb6a',
          'O-': '#43a047'
        }
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'ui-sans-serif', 'system-ui', 'sans-serif']
      },
      fontSize: {
        'xs': '0.75rem',
        'sm': '0.875rem',
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
        '5xl': '3rem',
        '6xl': '3.75rem'
      },
      spacing: {
        '18': '4.5rem',
        '72': '18rem',
        '84': '21rem',
        '96': '24rem'
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        }
      },
      boxShadow: {
        'soft': '0 2px 15px 0 rgba(0, 0, 0, 0.1)',
        'medium': '0 4px 25px 0 rgba(0, 0, 0, 0.15)',
        'strong': '0 10px 40px 0 rgba(0, 0, 0, 0.2)',
        'colored': '0 4px 14px 0 rgba(239, 68, 68, 0.25)'
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem'
      },
      backdropBlur: {
        xs: '2px'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms')({
      strategy: 'class'
    }),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio')
  ]
} 