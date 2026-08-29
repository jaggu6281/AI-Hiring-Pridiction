# GitHub & Render Deployment Guide

## 🚀 Step 1: Create GitHub Repository

### 1.1 Initialize Git locally

```bash
# Navigate to your project
cd AI-Hiring-Prediction

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI Hiring Prediction System"
```

### 1.2 Create Repository on GitHub

1. Go to [GitHub.com](https://github.com)
2. Sign in to your account
3. Click **"+"** → **"New repository"**
4. Fill in:
   - Repository name: `ai-hiring-prediction`
   - Description: "AI-powered hiring prediction and candidate evaluation system"
   - Visibility: **Public** (for portfolio) or **Private**
   - DO NOT initialize with README (we already have one)
5. Click **"Create repository"**

### 1.3 Push to GitHub

```bash
# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-hiring-prediction.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main

# Verify
git remote -v
```

---

## 🌐 Step 2: Deploy on Render

### 2.1 Create Render Account

1. Go to [Render.com](https://render.com)
2. Sign up with GitHub (recommended for easier integration)
3. Authorize Render to access your GitHub account

### 2.2 Deploy Backend Service

**Option A: Using render.yaml (Recommended)**

1. In Render Dashboard → **"+ New"** → **"Web Service"**
2. Select your GitHub repository: `ai-hiring-prediction`
3. Render will auto-detect `render.yaml`
4. Configuration should pre-fill:
   - Name: `ai-hiring-backend`
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port 8080`
5. Choose Plan: **Starter** (free - will sleep after 15 min inactivity)
6. Click **"Create Web Service"**
7. Wait 5-10 minutes for build and deployment

**Option B: Manual Configuration (if auto-detect fails)**

1. In Render Dashboard → **"+ New"** → **"Web Service"**
2. Connect your GitHub repository
3. Fill in:
   - **Name**: `ai-hiring-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Starter (free)
4. Under **Environment**:
   - Add environment variables:
     - `PYTHONUNBUFFERED=true`
     - `PYTHONDONTWRITEBYTECODE=true`
     - `ENVIRONMENT=production`
5. Click **"Create Web Service"**

### 2.3 Deploy Frontend Service

**Option A: Using render.yaml (Recommended)**

The frontend will be auto-deployed as a static site service.

**Option B: Manual Configuration**

1. In Render Dashboard → **"+ New"** → **"Static Site"**
2. Connect your GitHub repository
3. Fill in:
   - **Name**: `ai-hiring-frontend`
   - **Build Command**: `echo "Static site"` (leave empty, we have no build)
   - **Publish Directory**: `frontend`
   - **Plan**: Free
4. Click **"Create Static Site"**

### 2.4 Configure Frontend to Talk to Backend

After backend deployment, get its URL (e.g., `https://ai-hiring-backend-xxx.onrender.com`)

**Update Frontend Configuration:**

In `frontend/index.html`, the JavaScript already auto-detects the backend:

```javascript
// Auto-detects:
// - Development: http://localhost:8000
// - Production: Uses same domain
// - Custom: You can manually set API_BASE_URL
```

The frontend's `script.js` will automatically:
1. Detect it's running on Render domain
2. Use the same domain to reach the backend
3. Fallback to port 8000 if needed

**If needed, manually update:**

Open `frontend/script.js` and modify the API URL resolution:

```javascript
// For Render, you might need:
const getAPIBaseURL = () => {
    if (window.location.hostname.includes('onrender.com')) {
        return 'https://' + window.location.hostname.replace('-frontend-', '-backend-');
    }
    // ... rest of logic
};
```

---

## 🔗 Step 3: Verify Deployment

### Check Backend Status

```bash
# Get your backend URL from Render Dashboard
# Then check health:
curl https://ai-hiring-backend-xxx.onrender.com/health

# Should respond with:
{"status": "healthy"}
```

### Check Frontend Access

1. Open frontend URL from Render Dashboard
2. You should see the AI Hiring Prediction UI
3. Status indicator should show "✅ API Connected"

### Full Integration Test

1. Navigate to frontend URL
2. Fill in candidate form
3. Click "Predict"
4. Should see results (not errors)

---

## 🔐 Environment Variables on Render

### Set Production Variables

1. Go to Web Service settings → **"Environment"**
2. Add variables:

```
ENVIRONMENT=production
PYTHONUNBUFFERED=true
PYTHONDONTWRITEBYTECODE=true
SECRET_KEY=<generate-random-string>
ALLOWED_ORIGINS=https://ai-hiring-frontend-xxx.onrender.com
```

To generate SECRET_KEY:
```bash
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

### Configure CORS in Backend

The backend already has CORS enabled. For production, update in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-hiring-frontend-xxx.onrender.com",
        "http://localhost:3000"  # Development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Monitoring Deployment

### View Logs

**Render Dashboard:**
1. Select your service
2. Click **"Logs"** tab
3. Watch real-time deployment logs

**Command Line:**
```bash
# Not directly available, but you can check Render Dashboard logs
```

### Common Issues & Fixes

**❌ Backend shows "Down"**
- Check logs for errors
- Verify `requirements.txt` is up to date
- Ensure `main.py` is in `backend/` folder
- Restart service: Dashboard → "Manual Deploy"

**❌ Frontend can't reach backend**
- Verify backend is running (check health endpoint)
- Check CORS configuration
- Update API URL in `frontend/script.js`

**❌ Build fails**
- Check logs for Python errors
- Verify `requirements.txt` syntax
- Try manual redeploy: Dashboard → "Manual Deploy" → "Deploy latest commit"

**❌ Service keeps crashing**
- Check memory/CPU limits
- Verify start command is correct
- Check for infinite loops in startup code

---

## 🚀 Auto-Deployment Setup

### Enable Auto-Deploy

**Default:** Already enabled with `render.yaml`

When you push to GitHub:
```bash
git add .
git commit -m "Update features"
git push origin main
```

Render automatically:
1. Detects the push
2. Builds your code
3. Deploys changes
4. Takes ~5-10 minutes

### Disable Auto-Deploy (if needed)

1. Service Settings → **"Auto-Deploy"**
2. Toggle **Off**
3. Deploy manually when needed

---

## 📈 Performance Optimization

### Reduce Build Time
- Smaller Docker image
- Fewer dependencies
- Use build caching

### Reduce Runtime
- Deploy closer to users
- Enable caching in Nginx
- Optimize database queries

### Minimize Costs
- Use **Starter** plan (sleeps after 15 min)
- Upgrade to **Standard** when needed
- Monitor usage in Dashboard

---

## 🔄 Update & Maintenance

### Deploy Updates

```bash
# Make changes locally
vim backend/main.py  # or any file

# Commit and push
git add .
git commit -m "Fix: description of change"
git push origin main

# Render auto-deploys in 5-10 minutes
# Check Logs tab to verify
```

### Rollback to Previous Version

1. Render Dashboard → **"Deployments"**
2. Click older deployment version
3. Click **"Redeploy"**

### Manual Redeploy

1. Service settings → **"Manual Deploy"**
2. Click **"Deploy latest commit"**

---

## 🎯 Your Service URLs (after deployment)

```
Frontend:  https://ai-hiring-frontend-xxx.onrender.com
Backend:   https://ai-hiring-backend-xxx.onrender.com
API Docs:  https://ai-hiring-backend-xxx.onrender.com/docs
Health:    https://ai-hiring-backend-xxx.onrender.com/health
```

Replace `xxx` with your actual Render service IDs.

---

## 📝 Troubleshooting Checklist

- [ ] GitHub repository created and code pushed
- [ ] Render account created and GitHub connected
- [ ] Backend service deployed and healthy
- [ ] Frontend service deployed and accessible
- [ ] Frontend can reach backend (check status indicator)
- [ ] Test form submission works
- [ ] Environment variables set correctly
- [ ] CORS configured for production domain
- [ ] Auto-deploy enabled
- [ ] Logs checked for errors

---

## 🎓 Next Steps

### Phase 1: Current (Render Free Tier)
- ✅ Deployed and working
- Learn from usage patterns
- Get feedback

### Phase 2: Upgrade (When Ready)
- Upgrade to Paid Plan (no sleep timeout)
- Add custom domain
- Enable more features
- Monitor performance

### Phase 3: Scale (High Traffic)
- Use Professional plan
- Add database (PostgreSQL on Render)
- Increase workers
- Add CDN for assets

---

## 📞 Support & Resources

- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **GitHub Docs**: https://docs.github.com
- **Your Project Repo**: https://github.com/YOUR_USERNAME/ai-hiring-prediction

---

**Last Updated**: 2026-08-29  
**Version**: 1.0.0
