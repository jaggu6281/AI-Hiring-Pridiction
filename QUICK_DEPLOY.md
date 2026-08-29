# 🚀 Quick Start: GitHub & Render Deployment

## ⚡ 3-Step Quick Deploy

### Step 1: Push to GitHub (5 minutes)

**Windows Users:**
```bash
# Double-click this file:
push-to-github.bat
```

**Mac/Linux Users:**
```bash
chmod +x push-to-github.sh
./push-to-github.sh
```

**Manual Setup:**
```bash
git init
git add .
git commit -m "Initial commit: AI Hiring Prediction System"
git remote add origin https://github.com/YOUR_USERNAME/ai-hiring-prediction.git
git branch -M main
git push -u origin main
```

---

### Step 2: Create Render Account (2 minutes)

1. Go to [Render.com](https://render.com)
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"** (easiest)
4. Authorize Render to access your GitHub

---

### Step 3: Deploy on Render (5 minutes)

1. **Go to Render Dashboard**
2. Click **"+ New"** → **"Web Service"**
3. Select repository: `ai-hiring-prediction`
4. Render auto-configures using `render.yaml` ✅
5. Click **"Create Web Service"**
6. Wait 5-10 minutes for deployment
7. **Done!** 🎉

---

## 🔗 Your Deployed URLs

After deployment, you'll get:

```
Frontend:  https://ai-hiring-frontend-xxx.onrender.com
Backend:   https://ai-hiring-backend-xxx.onrender.com
API Docs:  https://ai-hiring-backend-xxx.onrender.com/docs
```

---

## 📊 What Render Does Automatically

✅ Detects Python project  
✅ Installs requirements.txt  
✅ Runs FastAPI backend  
✅ Serves static frontend  
✅ Auto-deploys on every git push  
✅ Monitors health checks  
✅ Provides logs and metrics  
✅ SSL/HTTPS included  

---

## 💰 Pricing (As of 2026)

| Plan | Cost | Best For |
|------|------|----------|
| **Free** | $0 | Testing, demos |
| **Starter** | $7/month | Small projects |
| **Standard** | $12/month | Production |

**Note:** Free tier services sleep after 15 minutes of inactivity.

---

## 🔄 Auto-Deployment

Every time you push code:

```bash
git add .
git commit -m "Your message"
git push origin main
```

Render automatically:
1. Pulls latest code
2. Rebuilds application
3. Deploys changes
4. Restarts services

Takes ~5-10 minutes. Check logs in Render Dashboard.

---

## 🆘 Troubleshooting

### Frontend shows "❌ API Disconnected"
- Wait for backend to fully deploy (5-10 min)
- Check backend health: https://ai-hiring-backend-xxx.onrender.com/health

### Backend shows "Down"
- Check deployment logs in Render Dashboard
- Common issues:
  - Missing requirements
  - Wrong start command
  - Python version mismatch

### Can't push to GitHub
- Verify git is installed: `git --version`
- Check GitHub credentials
- Create SSH key if needed

---

## 📚 Full Documentation

- **GitHub & Render Guide**: See `GITHUB_RENDER_DEPLOYMENT.md`
- **Deployment Options**: See `DEPLOYMENT.md`
- **Project Setup**: See `README.md`

---

## ✨ Next Steps After Deployment

1. ✅ Test all 3 features (Predict, Job-Fit, Report)
2. ✅ Share link with friends/colleagues
3. ✅ Add to portfolio
4. ✅ Monitor Render Dashboard
5. ✅ Upgrade plan if needed

---

## 🎯 One-Command Summary

```bash
# 1. Push to GitHub
./push-to-github.bat  # Windows
# OR
./push-to-github.sh   # Mac/Linux

# 2. Create account at Render.com (GitHub sign-up)

# 3. Deploy: Click "New" → "Web Service" → Select repo → "Create"

# Done! Your app is live 🎉
```

---

**Version**: 1.0.0  
**Last Updated**: 2026-08-29
