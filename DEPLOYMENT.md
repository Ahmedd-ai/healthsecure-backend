# HealthSecure Dashboard - Deployment Guide

## Prerequisites
- Vercel account (for frontend)
- Render account (for backend)
- GitHub/GitLab repository

---

## Backend Deployment (Render)

### 1. Prepare the Backend
The following files have been configured for Render deployment:
- `backend/main.py` - Updated with port configuration
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification
- `Procfile` - Render startup command

### 2. Deploy to Render
1. Log in to [Render](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `MONGO_URL`: Your MongoDB Atlas connection string
   - `SECRET_KEY`: A secure random string for JWT tokens
6. Click "Deploy"

### 3. Get Your Backend URL
After deployment, you'll get a URL like: `https://your-backend.onrender.com`

---

## Frontend Deployment (Vercel)

### 1. Prepare the Frontend
The following files have been configured for Vercel deployment:
- `frontend/my-app/src/config.js` - Updated with environment variable support
- `frontend/my-app/vercel.json` - Vercel configuration for React routing

### 2. Deploy to Vercel
1. Log in to [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Configure the following settings:
   - **Framework Preset**: `Create React App` (or `Other` if not detected)
   - **Build Command**: `npm run build` (or leave empty)
   - **Output Directory**: `build` (or leave empty)
4. Add Environment Variables:
   - `REACT_APP_API_URL`: Your Render backend URL (e.g., `https://your-backend.onrender.com`)
5. Click "Deploy"

### 3. Get Your Frontend URL
After deployment, you'll get a URL like: `https://your-app.vercel.app`

---

## Environment Variables Summary

### Backend (Render)
| Variable | Description | Example |
|----------|-------------|---------|
| MONGO_URL | MongoDB Atlas connection string | `mongodb+srv://...` |
| SECRET_KEY | JWT secret key | `your-secret-key` |
| PORT | Port number (automatically set by Render) | `10000` |

### Frontend (Vercel)
| Variable | Description | Example |
|----------|-------------|---------|
| REACT_APP_API_URL | Backend API URL | `https://your-backend.onrender.com` |

---

## Important Notes

1. **CORS**: The backend is already configured to allow all origins (`allow_origins=["*"]`), which works for development. For production, you may want to restrict this to your Vercel domain.

2. **MongoDB**: The database is already configured to use MongoDB Atlas. Make sure the `MONGO_URL` environment variable is set on Render.

3. **After Deployment**: Once both services are deployed, update your frontend environment variable on Vercel to point to your Render backend URL.

---

## Testing the Deployment

1. Visit your Vercel frontend URL
2. Try logging in or registering a new user
3. If you encounter issues, check:
   - Browser console for CORS errors
   - Network tab for failed API calls
   - Render logs for backend errors
