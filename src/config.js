// API Configuration
// IMPORTANT: Always use the production backend URL in production
// The Vercel environment variable VITE_API_URL should be set to https://healthcare-backend-q3t8.onrender.com

// Check for environment variable first, then fallback to production URL
// This ensures it works on Vercel even if the env var isn't set yet
export const API_URL = import.meta.env.VITE_API_URL || "https://healthcare-backend-q3t8.onrender.com";
