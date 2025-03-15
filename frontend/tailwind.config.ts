import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb',
          dark: '#1d4ed8',
          light: '#3b82f6',
        },
        futuristic: {
          dark: '#0f172a',
          DEFAULT: '#1e293b',
          light: '#334155',
          accent: '#38bdf8',
        },
        'futuristic-dark': '#0F172A',
        'futuristic-light': '#1E293B',
        'futuristic-accent': '#38BDF8',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'circuit-pattern': "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")",
      },
      keyframes: {
        'spin-slow': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        'spin-reverse': {
          '0%': { transform: 'rotate(360deg)' },
          '100%': { transform: 'rotate(0deg)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.5', transform: 'scale(0.9)' },
        },
      },
      animation: {
        'spin-slow': 'spin-slow 3s linear infinite',
        'spin-reverse': 'spin-reverse 2s linear infinite',
        'pulse-glow': 'pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      typography: {
        DEFAULT: {
          css: {
            color: '#fff',
            maxWidth: 'none',
            hr: {
              borderColor: '#334155',
              marginTop: '2rem',
              marginBottom: '2rem',
            },
            h1: {
              color: '#38BDF8',
              fontWeight: '700',
            },
            h2: {
              color: '#38BDF8',
              fontWeight: '600',
            },
            h3: {
              color: '#38BDF8',
              fontWeight: '600',
            },
            h4: {
              color: '#38BDF8',
              fontWeight: '600',
            },
            p: {
              color: '#fff',
              fontSize: '0.875rem',
              lineHeight: '1.5rem',
            },
            a: {
              color: '#38BDF8',
              textDecoration: 'none',
              '&:hover': {
                color: '#0EA5E9',
                textDecoration: 'underline',
              },
            },
            strong: {
              color: '#38BDF8',
              fontWeight: '600',
            },
            ul: {
              li: {
                '&::marker': {
                  color: '#38BDF8',
                },
              },
            },
            ol: {
              li: {
                '&::marker': {
                  color: '#38BDF8',
                },
              },
            },
            blockquote: {
              borderLeftColor: '#38BDF8',
              color: '#94A3B8',
              fontStyle: 'italic',
            },
            code: {
              color: '#38BDF8',
              backgroundColor: '#1E293B',
              padding: '0.25rem',
              borderRadius: '0.25rem',
              fontSize: '0.875rem',
            },
            pre: {
              backgroundColor: '#1E293B',
              code: {
                backgroundColor: 'transparent',
                color: '#fff',
              },
            },
            table: {
              thead: {
                borderBottomColor: '#334155',
                th: {
                  color: '#38BDF8',
                },
              },
              tbody: {
                tr: {
                  borderBottomColor: '#334155',
                },
                td: {
                  color: '#fff',
                },
              },
            },
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
export default config; 