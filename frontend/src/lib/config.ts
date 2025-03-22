// Frontend configuration settings

// Load environment variables from import.meta.env (Vite)
interface EnvConfig {
  API_BASE_URL: string;
  APP_ENV: string;
}

// Get the environment variables with validation
const getEnvVariables = (): EnvConfig => {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
  const appEnv = import.meta.env.VITE_APP_ENV || 'development';
  
  // Validate critical environment variables
  if (!apiBaseUrl) {
    console.error('❌ Error: VITE_API_BASE_URL environment variable is not set!');
    console.error('   This is required for API communication to function correctly.');
    console.error('   Please set this in your .env or .env.production file.');
    
    // For development, provide a fallback
    if (appEnv === 'development') {
      console.warn('⚠️ Using fallback API URL for development: http://localhost:8000');
      return {
        API_BASE_URL: 'http://localhost:8000',
        APP_ENV: appEnv
      };
    }
    
    // For production, show a more serious error
    throw new Error('VITE_API_BASE_URL environment variable is required');
  }
  
  // Log configuration in development
  if (appEnv === 'development') {
    console.log('🔧 Environment Configuration:');
    console.log(`   - API Base URL: ${apiBaseUrl}`);
    console.log(`   - Environment: ${appEnv}`);
  }
  
  return {
    API_BASE_URL: apiBaseUrl,
    APP_ENV: appEnv
  };
};

// Export the configuration
export const config = getEnvVariables();

// Helper function to check if we're in production
export const isProduction = (): boolean => config.APP_ENV === 'production';

// Helper function to check if we're in development
export const isDevelopment = (): boolean => config.APP_ENV === 'development'; 