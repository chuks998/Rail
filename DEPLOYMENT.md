# Deploying RAIL Banking App to Render

## Prerequisites

- GitHub account
- Render account (sign up at https://render.com)
- Your application code pushed to GitHub

## Files Created for Deployment

✅ `requirements.txt` - Python dependencies
✅ `build.sh` - Build script for Render
✅ `render.yaml` - Render service configuration
✅ `.env.example` - Environment variables template
✅ Updated `settings.py` - Production-ready Django settings

## Step-by-Step Deployment Guide

### 1. Push Your Code to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create a Render Account

1. Go to https://render.com
2. Sign up or log in with your GitHub account

### 3. Create a New Web Service

#### Option A: Using render.yaml (Recommended)

1. In Render Dashboard, click **"New +"** → **"Blueprint"**
2. Connect your GitHub repository
3. Render will automatically detect `render.yaml` and create services
4. Click **"Apply"**

#### Option B: Manual Setup

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure the service:
   - **Name:** `rail-banking-app` (or your preferred name)
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn RAILmicrofinace.wsgi:application`
   - **Instance Type:** `Free`

### 4. Create PostgreSQL Database (Free)

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `rail_db`
   - **Database:** `rail_db`
   - **User:** `rail_user`
   - **Region:** Choose closest to your users
   - **Instance Type:** `Free`
3. Click **"Create Database"**
4. Copy the **Internal Database URL** (it looks like: `postgresql://user:pass@host/db`)

### 5. Configure Environment Variables

In your Web Service settings, go to **"Environment"** tab and add:

**Required Variables:**

- `SECRET_KEY` → Click "Generate" or use a secure random string
- `DEBUG` → `False`
- `ALLOWED_HOSTS` → Your Render app URL (e.g., `rail-banking-app.onrender.com`)
- `DATABASE_URL` → Paste the Internal Database URL from step 4
- `PYTHON_VERSION` → `3.10.0`

**Optional Variables (for email features):**

- `EMAIL_HOST` → `smtp.gmail.com`
- `EMAIL_PORT` → `587`
- `EMAIL_USE_TLS` → `True`
- `EMAIL_HOST_USER` → Your email address
- `EMAIL_HOST_PASSWORD` → Your app password
- `WHATSAPP_NUMBER` → Your WhatsApp number
- `SUPPORT_EMAIL` → Your support email

### 6. Deploy

1. Click **"Create Web Service"** (or **"Manual Deploy"** if already created)
2. Wait for the build to complete (5-10 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

### 7. Update ALLOWED_HOSTS

After deployment, update the `ALLOWED_HOSTS` environment variable:

- Add your Render URL: `your-app-name.onrender.com`
- Format: `localhost,127.0.0.1,your-app-name.onrender.com`

### 8. Create Superuser (Admin Account)

1. In Render Dashboard, go to your Web Service
2. Click **"Shell"** tab
3. Run: `python manage.py createsuperuser`
4. Follow prompts to create admin account

## Important Notes

### Free Tier Limitations

- **Web Service:** Spins down after 15 minutes of inactivity
- **Database:** 90 days free, then requires upgrade
- **First request after sleep:** May take 30-60 seconds

### Static Files

- Managed by WhiteNoise automatically
- No external storage needed for free tier

### Media Files (User Uploads)

⚠️ **Important:** Free tier does NOT persist uploaded files

- Files uploaded will be deleted when service restarts
- For persistent storage, upgrade to paid plan or use:
  - AWS S3
  - Cloudinary
  - Render Disks (paid feature)

### Database Backups

- Free PostgreSQL includes daily backups
- Download backups from Render Dashboard

## Troubleshooting

### Build Fails

- Check build logs in Render Dashboard
- Ensure `build.sh` has execute permissions: `chmod +x build.sh`
- Verify all packages in `requirements.txt` are compatible

### Application Errors

- Check application logs in Render Dashboard
- Verify environment variables are set correctly
- Ensure `ALLOWED_HOSTS` includes your Render URL

### Database Connection Issues

- Verify `DATABASE_URL` is set correctly
- Check database is running in Render Dashboard
- Ensure using **Internal Database URL** (not External)

### Static Files Not Loading

- Run: `python manage.py collectstatic --no-input`
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py
- Verify WhiteNoise is in `MIDDLEWARE`

## Post-Deployment Tasks

### Update Contact Information

Update these TODO items in `dashboard.html`:

1. WhatsApp number: Line 544 - Replace `YOUR_WHATSAPP_NUMBER_HERE`
2. Support email: Line 557 - Replace `YOUR_SUPPORT_EMAIL_HERE`

### Configure Custom Domain (Optional)

1. In Render Dashboard, go to Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed
4. Update `ALLOWED_HOSTS` with custom domain

### Monitor Your App

- Check logs regularly in Render Dashboard
- Set up health checks if needed
- Monitor database size (free tier: 1GB limit)

## Useful Commands

### Access Shell

```bash
# In Render Dashboard → Shell tab
python manage.py shell
```

### View Logs

```bash
# In Render Dashboard → Logs tab
# Real-time logs automatically displayed
```

### Manual Migration

```bash
# In Render Dashboard → Shell tab
python manage.py migrate
```

### Collect Static Files

```bash
# In Render Dashboard → Shell tab
python manage.py collectstatic --no-input
```

## Need Help?

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Render Community: https://community.render.com

## Upgrading to Paid Plan

Consider upgrading if you need:

- No spin-down (always-on service)
- Persistent file storage
- More database storage
- Better performance
- Custom domains with SSL

Render pricing: https://render.com/pricing
