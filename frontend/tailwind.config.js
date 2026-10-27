/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        signal: {
          navy: {
            DEFAULT: '#0C1A2D',
            dark: '#07101C',
            light: '#132640',
            border: '#1E3554',
          },
          lime: {
            DEFAULT: '#C9F16A',
            hover: '#BCE859',
            light: '#EAF9CC',
            dark: '#8EBB29',
          },
          mint: {
            DEFAULT: '#68DCC5',
            light: '#E0F8F3',
            dark: '#3AB59D',
          },
          coral: {
            DEFAULT: '#FF876D',
            light: '#FFEBE7',
            dark: '#E05A3D',
          },
          lavender: {
            DEFAULT: '#B8A8FA',
            light: '#F1EDFE',
            dark: '#866FE6',
          },
          gold: {
            DEFAULT: '#FFCE7D',
            light: '#FFF5E3',
            dark: '#D99F3B',
          },
          offwhite: '#F8FAFC',
          white: '#FFFFFF',
          slate: {
            DEFAULT: '#758193',
            light: '#A4B0C0',
            dark: '#4C5868',
            faint: '#CBD5E1',
          }
        }
      },
      fontFamily: {
        heading: ['"Space Grotesk"', 'sans-serif'],
        sans: ['"Be Vietnam Pro"', 'Inter', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      borderRadius: {
        'squircle': '30%',
        'pill': '9999px',
        'card': '20px',
        'box': '14px',
      },
      boxShadow: {
        'signal-glow': '0 0 25px -5px rgba(201, 241, 106, 0.25)',
        'signal-lavender': '0 0 25px -5px rgba(184, 168, 250, 0.25)',
        'signal-card': '0 10px 30px -10px rgba(12, 26, 45, 0.08)',
        'signal-card-hover': '0 20px 40px -15px rgba(12, 26, 45, 0.12)',
      },
      keyframes: {
        pulseSubtle: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.6 },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-6px)' },
        }
      },
      animation: {
        'pulse-subtle': 'pulseSubtle 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float-slow': 'float 4s ease-in-out infinite',
      }
    },
  },
  plugins: [],
}
