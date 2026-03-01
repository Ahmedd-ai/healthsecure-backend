# HealthSecure Deployment Guide

## Architecture
- **Frontend**: Vercel (React)
- **Backend**: Render (FastAPI)  
- **Database**: MongoDB Atlas (Cloud)

---

## Backend - Render (Recommended)

### Step 1: Push Code to GitHub
1. Create a GitHub repository
2. Push your code (include these files at root level):
   - main.py
   - database.py
   - auth_utils.py
   - hash_password.py
   - requirements.txt
   - Procfile
   - routes/ (entire folder)

### Step 2: Deploy to Render
1. Go to [Render.com](https://render.com/) and sign up
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: healthsecure-api
   - **Runtime**: Python
   - **Build Command**: (leave blank)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**

### Step 3: Get Your Render URL
After deployment, you'll get a URL like:
`https://healthsecure-api.onrender.com`

### Step 4: Allow MongoDB Network Access
1. Go to MongoDB Atlas → **Network Access**
2. Click **Add IP Address**
3. Add **Allow Access from Anywhere** (0.0.0.0/0)

---

## Frontend - Vercel

### Step 1: Update API URL
Edit `frontend/my-app/src/config.js`:
```
javascript
export const API_URL = "https://your-render-url.onrender.com";
```

### Step 2: Deploy to Vercel
1. Go to [Vercel.com](https://vercel.com/)
2. Import your GitHub repository
3. Configure:
   - Framework: React
   - Build Command: `npm run build`
   - Output Directory: `build`
4. Click **Deploy**

---

## Quick Checklist
- [ ] Backend deployed on Render
- [ ] MongoDB Atlas network access configured
- [ ] Frontend API URL updated in config.js
- [ ] Frontend deployed on Vercel
- [ ] Test the application

---

## Your URLs (After Deployment)
- **Backend**: `https://healthsecure-api.onrender.com`
- **Frontend**: `https://your-project.vercel.app`

---

## Troubleshooting
1. **CORS Error**: Backend already has `allow_origins=["*"]` in main.py
2. **API Not Connecting**: Check that config.js has correct Render URL
3. **MongoDB Error**: Verify network access in MongoDB Atlas
