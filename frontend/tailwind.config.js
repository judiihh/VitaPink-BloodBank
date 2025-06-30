/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        // VitaPink Brand Colors - Custom Color Palette
        primary: {
          50: '#fdf2f8',   // Very light pink
          100: '#fce7f3',  // Light pink
          200: '#fbcfe8',  // Lighter pink
          300: '#f9a8d4',  // Light pink
          400: '#f472b6',  // Medium pink
          500: '#ec4899',  // Pink
          600: '#db2777',  // Darker pink
          700: '#be185d',  // Dark pink
          800: '#9d174d',  // Very dark pink
          900: '#831843'   // Darkest pink
        },
        // VitaPink Custom Colors from color.txt
        vitapink: {
          main: '#ead1dc',      // MainColor: R234 G209 B220
          extra1: '#d5a6bd',    // ExtraColors: R213 G166 B189
          extra2: '#c27ba0',    // ExtraColors: R194 G123 B160
          extra3: '#a64d79',    // ExtraColors: R166 G077 B121
          extra4: '#741b47',    // ExtraColors: R116 G027 B071
          // Additional shades for better UI
          light: '#f5ebf0',     // Lighter version of main
          lighter: '#faf7f8',   // Even lighter
          dark: '#5c1a35',      // Darker version
          darker: '#3d1123'     // Even darker
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
    // Plugins can be added here when needed
    // require('@tailwindcss/forms'),
    // require('@tailwindcss/typography'),
    // require('@tailwindcss/aspect-ratio')
  ]
} 