# Deployment Guide

This guide provides step-by-step instructions for deploying the Multi-Agent Deep Document Intelligence System to various cloud platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Backend Deployment](#backend-deployment)
  - [Option 1: Render](#option-1-render-recommended)
  - [Option 2: Railway](#option-2-railway)
  - [Option 3: Heroku](#option-3-heroku)
- [Frontend Deployment](#frontend-deployment)
  - [Option 1: Vercel](#option-1-vercel-recommended)
  - [Option 2: Netlify](#option-2-netlify)
- [Environment Variables](#environment-variables)
- [Post-Deployment Testing](#post-deployment-testing)

## Prerequisites

- GitHub account
- API key for Groq, OpenAI, or OpenRouter
- Account on your chosen deployment platform(s)

## Backend Deployment

### Option 1: Render (Recommended)

Render offers a free tier and is easy to set up.

1. **Push your code to GitHub** (see main README)

2. **Create a new Web Service on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure the service**
   - **Name**: `multi-agent-doc-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   - Click "Advanced" → "Add Environment Variable"
   - Add the following:
     ```
     LLM_PROVIDER=groq
     GROQ_API_KEY=your_actual_groq_api_key
     MAX_CHUNK_SIZE=1200
     MIN_CHUNK_SIZE=800
     LLM_TIMEOUT=30
     PARALLEL_AGENTS=true
     LOG_LEVEL=INFO
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Copy your backend URL (e.g., `https://multi-agent-doc-backend.onrender.com`)

### Option 2: Railway

Railway offers $5 free credit per month.

1. **Push your code to GitHub**

2. **Create a new project on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure the service**
   - Railway will auto-detect Python
   - Add a `Procfile` (already included in this repo)

4. **Add Environment Variables**
   - Go to "Variables" tab
   - Add the same variables as listed in Render option

5. **Deploy**
   - Railway will automatically deploy
   - Go to "Settings" → "Generate Domain" to get your URL

### Option 3: Heroku

Heroku requires a credit card but offers free dynos.

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create multi-agent-doc-backend
   ```

3. **Set environment variables**
   ```bash
   heroku config:set LLM_PROVIDER=groq
   heroku config:set GROQ_API_KEY=your_actual_groq_api_key
   heroku config:set MAX_CHUNK_SIZE=1200
   heroku config:set MIN_CHUNK_SIZE=800
   heroku config:set LLM_TIMEOUT=30
   heroku config:set PARALLEL_AGENTS=true
   heroku config:set LOG_LEVEL=INFO
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

## Frontend Deployment

### Option 1: Vercel (Recommended)

Vercel is optimized for React/Vite applications.

1. **Push your code to GitHub**

2. **Import project on Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New" → "Project"
   - Import your GitHub repository

3. **Configure the project**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add Environment Variable**
   - Add `VITE_API_URL` with your backend URL from step 1
   - Example: `https://multi-agent-doc-backend.onrender.com`

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Copy your frontend URL (e.g., `https://your-app.vercel.app`)

### Option 2: Netlify

Netlify is another excellent option for static sites.

1. **Push your code to GitHub**

2. **Create a new site on Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub and select your repository

3. **Configure build settings**
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

4. **Add Environment Variable**
   - Go to "Site settings" → "Environment variables"
   - Add `VITE_API_URL` with your backend URL

5. **Deploy**
   - Click "Deploy site"
   - Wait for deployment to complete

## Environment Variables

### Backend Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `LLM_PROVIDER` | LLM provider to use | Yes | `groq` |
| `GROQ_API_KEY` | Groq API key | If using Groq | `gsk_...` |
| `OPENAI_API_KEY` | OpenAI API key | If using OpenAI | `sk-...` |
| `OPENROUTER_API_KEY` | OpenRouter API key | If using OpenRouter | `sk-or-...` |
| `MAX_CHUNK_SIZE` | Maximum chunk size | No | `1200` |
| `MIN_CHUNK_SIZE` | Minimum chunk size | No | `800` |
| `LLM_TIMEOUT` | LLM call timeout (seconds) | No | `30` |
| `PARALLEL_AGENTS` | Enable parallel execution | No | `true` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

### Frontend Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Backend API URL | Yes | `https://your-backend.onrender.com` |

## Post-Deployment Testing

### Test Backend

1. **Check health endpoint**
   ```bash
   curl https://your-backend-url.com/health
   ```

2. **Test API documentation**
   - Visit `https://your-backend-url.com/docs`
   - Should see Swagger UI

3. **Test document analysis**
   ```bash
   curl -X POST https://your-backend-url.com/analyze-document \
     -H "Content-Type: application/json" \
     -d '{"document_text": "Your test document text here..."}'
   ```

### Test Frontend

1. **Visit your frontend URL**
   - Should load without errors

2. **Test document upload**
   - Upload a test document
   - Verify analysis completes successfully

3. **Check browser console**
   - Open DevTools (F12)
   - Should see no errors

## Troubleshooting

### Backend Issues

**Problem**: "Module not found" errors
- **Solution**: Ensure all dependencies are in `requirements.txt`

**Problem**: API calls failing
- **Solution**: Verify environment variables are set correctly

**Problem**: Timeout errors
- **Solution**: Increase `LLM_TIMEOUT` or use a faster LLM provider

### Frontend Issues

**Problem**: "Failed to fetch" errors
- **Solution**: Check `VITE_API_URL` is set correctly and includes `https://`

**Problem**: CORS errors
- **Solution**: Backend CORS is set to allow all origins. If still seeing errors, check backend logs

**Problem**: Build fails
- **Solution**: Ensure Node.js version is 18+ and all dependencies install correctly

## Updating Your Deployment

### Render/Railway/Heroku
- Push changes to GitHub
- Platform will automatically redeploy

### Vercel/Netlify
- Push changes to GitHub
- Platform will automatically rebuild and redeploy

## Cost Considerations

### Free Tier Limits

**Render**
- 750 hours/month free
- Spins down after 15 minutes of inactivity
- Cold start time: ~30 seconds

**Railway**
- $5 free credit/month
- ~100 hours of uptime

**Vercel**
- 100 GB bandwidth/month
- Unlimited deployments

**Netlify**
- 100 GB bandwidth/month
- 300 build minutes/month

## Support

If you encounter issues:
1. Check the platform's status page
2. Review deployment logs
3. Verify environment variables
4. Test locally first

---

**Need help?** Open an issue on GitHub with:
- Platform you're using
- Error messages
- Deployment logs
