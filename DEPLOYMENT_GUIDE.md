# HealthSecure Deployment Guide

## Architecture
- **Frontend**: Vercel (React)
- **Backend**: Render (FastAPI)  
- **Database**: MongoDB Atlas (Cloud)

---

## Important: MongoDB Atlas Configuration

Your MongoDB Atlas connection details:
- **Connection String**: `mongodb+srv://ahmed_db:Uloom%40123@cluster0.3i5uuip.mongodb.net/?appName=Cluster0`
- **Database Name**: `healthsecure`

### Step 1: Configure MongoDB Atlas Network Access
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Login and select your cluster (Cluster0)
3. Click **Network Access** in the left sidebar
4. Click **Add IP Address**
5. Select **Allow Access from Anywhere** (0.0.0.0/0)
6. Click **Confirm**

---

## Backend - Render

### Step 1: Push Code to GitHub
1. Create a GitHub repository (e.g., `healthsecure-dashboard`)
2. Push all project files to GitHub:
   
```
bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/healthsecure-dashboard.git
   git push -u origin main
   
```

### Step 2: Deploy to Render
1. Go to [Render.com](https://render.com/) and sign up
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `healthsecure-api`
   - **Runtime**: Python
   - **Build Command**: (leave blank)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**

### Step 3: Add Environment Variable on Render
1. In your Render dashboard, go to your web service
2. Click **Environment** in the left sidebar
3. Add a new environment variable:
   - **Key**: `MONGO_URL`
   - **Value**: `mongodb+srv://ahmed_db:Uloom%40123@cluster0.3i5uuip.mongodb.net/?appName=Cluster0`
4. Click **Save Changes**

### Step 4: Get Your Render URL
After deployment, you'll get a URL like:
`https://healthsecure-api.onrender.com`

---

## Frontend - Vercel

### Step 1: Configure Environment Variable
In `src/config.js`, the frontend is already configured to use Vite environment variables:
```
javascript
export const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
```

### Step 2: Deploy to Vercel
1. Go to [Vercel.com](https://vercel.com/)
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: React
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
4. Click **Deploy**

### Step 3: Add Environment Variable on Vercel (After Backend is Deployed)
1. In your Vercel dashboard, go to project settings
2. Click **Environment Variables**
3. Add:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://healthsecure-api.onrender.com` (your Render URL)
4. Redeploy the frontend to apply the changes

---

## Quick Checklist
- [ ] MongoDB Atlas network access configured (0.0.0.0/0)
- [ ] Backend deployed on Render
- [ ] MONGO_URL environment variable added on Render
- [ ] Frontend deployed on Vercel
- [ ] VITE_API_URL environment variable added on Vercel
- [ ] Test the application

---

## Your URLs (After Deployment)
- **Backend**: `https://healthsecure-api.onrender.com`
- **Frontend**: `https://your-project.vercel.app`

---

## Troubleshooting

### 1. CORS Error
- Backend already has `allow_origins=["*"]` in main.py
- Should work automatically

### 2. API Not Connecting
- Check that VITE_API_URL is set correctly on Vercel
- Verify your Render backend is running

### 3. MongoDB Error
- Verify network access in MongoDB Atlas (0.0.0.0/0)
- Check that MONGO_URL is correctly set on Render

### 4. Database Empty
- Run the seed script to populate data:
  
```
bash
  python seed.py
  
```
- Or use the `/seed` endpoint on your deployed backend

---

## Files to Commit to GitHub

Ensure these files are in your GitHub repository:
```
/
├── main.py              # FastAPI app
├── database.py          # MongoDB connection (updated with Atlas URL)
├── auth_utils.py        # Authentication utilities
├── hash_password.py    # Password hashing
├── requirements.txt    # Python dependencies
├── Procfile            # Render deployment config
├── runtime.txt         # Python version
├── routes/             # API route handlers
│   ├── __init__.py
│   ├── assets.py
│   ├── vulnerabilities.py
│   ├── compliance.py
│   ├── phi_risks.py
│   ├── anomalies.py
│   ├── dashboard.py
│   └── auth.py
├── healthsecure-dashboard/  # Frontend React app
│   ├── package.json
│   ├── public/
│   ├── src/
│   └── vercel.json
└── src/                    # Frontend source (alternate location)
    ├── config.js
    ├── pages/
    ├── components/
    └── context/
