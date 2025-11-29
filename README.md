# yt-dlp Service for YouTube Video URLs

A simple Flask API that uses yt-dlp to extract direct video URLs from YouTube without downloading.

## Deploy to Render (FREE - No Credit Card Needed!)

### Step 1: Push to GitHub

```bash
cd yt-dlp-service
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to: https://render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Configure:
   - **Name**: `yt-dlp-service`
   - **Environment**: `Docker`
   - **Plan**: **Free**
   - **Build Command**: (leave empty - uses Dockerfile)
   - **Start Command**: (leave empty - uses Dockerfile CMD)

5. Click **"Create Web Service"**

6. Wait 5-10 minutes for deployment

7. Your service will be at: `https://yt-dlp-service.onrender.com`

### Step 3: Test

Visit: `https://yt-dlp-service.onrender.com/download?url=https://www.youtube.com/watch?v=VIDEO_ID`

Returns:
```json
{
  "success": true,
  "url": "https://direct-video-url...",
  "video_id": "...",
  "title": "...",
  "duration": 600,
  "quality": 1080
}
```

### Step 4: Use in n8n

In your "Get Direct Video URL" node:

**Method**: GET
**URL**: `https://yt-dlp-service.onrender.com/download?url=https://www.youtube.com/watch?v={{$json.videoId}}`

That's it!

## API Endpoints

### GET /
Health check

### GET /download
Parameters:
- `url` (required): YouTube video URL
- `quality` (optional): Max quality (default: 1080)

Returns direct MP4 video URL

## Notes

- Render free tier: Service sleeps after 15 min of inactivity (first request takes 30s to wake up)
- No credit card needed!
- 750 hours/month free
