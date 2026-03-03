# HealthSecure - "Failed to fetch" Error Resolution

## Root Cause Analysis

### Primary Issue: Render Free Tier Sleep
The most likely cause is **Render's free tier auto-sleep behavior**. Free tier services sleep after 15 minutes of inactivity. When the frontend tries to make a request to a sleeping backend, it results in a network error ("Failed to fetch") because:
1. The server is starting up (cold start)
2. The connection times out before the server responds

### Secondary Issues Found:

1. **config.js is hardcoded** - The user mentioned using VITE_API_URL in Vercel, but the code isn't using it
2. **No error handling for network failures** in AuthContext
3. **vercel.json has incorrect rewrite rule** for API proxying

---

## Solutions

### Solution 1: Fix Frontend Configuration (config.js)

Update the config.js to properly use environment variables:

```
javascript
// API Configuration
// Use environment variable in production, fallback to localhost for development

// Check if we're in production (Vercel)
const isProduction = import.meta.env.PROD;

// Use VITE_API_URL from environment if available, otherwise use default
// For Vercel: Set VITE_API_URL in Vercel dashboard to https://healthcare-backend-q3t8.onrender.com
export const API_URL = import.meta.env.VITE_API_URL || 
  (isProduction ? "https://healthcare-backend-q3t8.onrender.com" : "http://localhost:8001");
```

### Solution 2: Add Error Handling in AuthContext

Update AuthContext.jsx to handle network errors properly:

```
javascript
const login = async (username, password) => {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Login failed with status ${response.status}`);
    }
    
    const data = await response.json();
    setToken(data.access_token);
    setUser(data.user || { username, role: "user" });
    return data;
  } catch (error) {
    // Network error or CORS issue
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error('Unable to connect to server. The backend may be sleeping (free tier). Please try again after a moment.');
    }
    throw error;
  }
};
```

### Solution 3: Fix vercel.json

```
json
{
  "build": {
    "command": "cd frontend/my-app && CI=false npm run build",
    "outputDirectory": "frontend/my-app/build",
    "env": {
      "CI": "false"
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://healthcare-backend-q3t8.onrender.com/$1"
    }
  ]
}
```

### Solution 4: Backend CORS Configuration (Already Correct)

The current backend CORS is already set to allow all origins:

```
python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - correct for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Vercel Environment Setup

1. Go to your Vercel Dashboard
2. Select your project
3. Go to **Settings** > **Environment Variables**
4. Add the following variables:
   - `VITE_API_URL` = `https://healthcare-backend-q3t8.onrender.com`
5. **Redeploy** the frontend for changes to take effect

---

## How to Debug Using Browser DevTools

### 1. Open DevTools (F12 or Right-click > Inspect)

### 2. Check the Network Tab:
- Look for the failed request to `/auth/login`
- Check the **Status** column - if it shows "(failed)" it's a network error
- Check **Type** column - if it shows "fetch" or "xhr"

### 3. Check the Console Tab:
- **CORS errors** will show as: "Access to fetch at 'https://healthcare-backend-q3t8.onrender.com/auth/login' from origin 'https://healthsecuredashboard-beta.vercel.app' has been blocked by CORS policy"
- **Network errors** will show as: "Failed to fetch" or "NetworkError when attempting to fetch resource"

### 4. Check Response Details:
- Click on the failed request
- Look at the **Response** tab - if empty, the server didn't respond (likely sleeping)
- Check **Timing** - if it shows very long times, the server is taking too long to respond

---

## Production API Call Example

Here's the correct pattern for production API calls:

```
javascript
// Using fetch with proper error handling
async function login(username, password) {
  const API_URL = import.meta.env.VITE_API_URL || "https://healthcare-backend-q3t8.onrender.com";
  
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error.name === 'TypeError') {
      console.error('Network error - server may be down or sleeping');
      throw new Error('Unable to connect to server. Please try again.');
    }
    throw error;
  }
}
```

---

## Fix for Render Free Tier (Recommended)

### Option A: Upgrade to Render Paid Plan
- $7/month for a dedicated server that never sleeps

### Option B: Use Render's Health Check
Add a health endpoint and use Render's health check feature:

```
python
# In backend/main.py
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

Then in Render dashboard:
1. Go to your backend service
2. Set Health Check path to `/health`
3. This will ping your backend every 5 minutes to keep it awake

### Option C: Use a Free Alternative (Railway, Fly.io, etc.)
These offer free tiers that stay awake longer or have better cold start times.

---

## Summary Checklist

- [ ] Set `VITE_API_URL` in Vercel Environment Variables
- [ ] Update config.js to use environment variable
- [ ] Redeploy frontend on Vercel
- [ ] Set up Render Health Check to prevent sleeping
- [ ] Test the login again
- [ ] Check DevTools Network tab for errors
