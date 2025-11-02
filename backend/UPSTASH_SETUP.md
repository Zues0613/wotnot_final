# Upstash Redis Setup Guide

## 🚀 Quick Setup for WotNot Backend

### 1. Create Upstash Account
1. Go to [https://console.upstash.com/](https://console.upstash.com/)
2. Sign up for a free account
3. Verify your email

### 2. Create Redis Database
1. Click "Create Database"
2. Choose "Global" region (closest to your users)
3. Select "Free" tier (10,000 requests/day)
4. Give it a name like "wotnot-redis"
5. Click "Create"

### 3. Get Redis Credentials
1. Click on your database
2. Go to "Details" tab
3. You'll see several connection options. For Dramatiq, you need:
   - **REST URL** (e.g., `https://fast-bluejay-19956.upstash.io`) - for REST API
   - **REST Token** (a long alphanumeric string) - for REST API
   
   **Note:** The code automatically constructs the Redis protocol URL from these REST credentials for Dramatiq to use.
   
   **Alternative:** If you prefer, Upstash also provides a direct **Redis URL** (starts with `redis://`) that you can use with the `REDIS_URL` environment variable instead.

### 4. Add to Environment Variables
Add both environment variables to your backend:

**For local development (.env file):**
```env
ENVIRONMENT="dev"
UPSTASH_REDIS_REST_URL="https://fast-bluejay-19956.upstash.io"
UPSTASH_REDIS_REST_TOKEN="your-token-here"
```
**Note:** `ENVIRONMENT="dev"` will force local Redis usage. Remove it to use Upstash in development.

**For production (Render/Heroku/etc.):**
1. Go to your deployment platform dashboard
2. Select your web service
3. Go to "Environment" tab
4. Add these environment variables:
   - **Key**: `ENVIRONMENT`
   - **Value**: `prod` (or leave unset, defaults to prod)
   - **Key**: `UPSTASH_REDIS_REST_URL`
   - **Value**: Your Upstash REST URL
   - **Key**: `UPSTASH_REDIS_REST_TOKEN`
   - **Value**: Your Upstash REST Token
5. Click "Save Changes"

### 5. Deploy
1. Your app will automatically redeploy
2. Check logs to see "✅ Upstash Redis configured" message
3. You should see: "ℹ️  Skipping local Redis installation (using cloud Redis)"
4. Background tasks will now work with Upstash Redis

## 🔧 Features You Get
- ✅ **Free Tier**: 10,000 requests per day
- ✅ **Global**: Low latency worldwide
- ✅ **Reliable**: 99.9% uptime SLA
- ✅ **Secure**: TLS encryption
- ✅ **Scalable**: Easy to upgrade when needed

## 📝 What You Need from Upstash

**Only Redis** - You don't need Vector or QStash for this application:
- ✅ **Redis**: Used for Dramatiq background task queue (broadcasts, scheduled messages)
- ❌ **Vector**: Not used (would be for AI embeddings/similarity search)
- ❌ **QStash**: Not used (you use Dramatiq instead)

## 📊 Monitoring
- View usage in Upstash console
- Monitor request count and bandwidth
- Set up alerts for limits

## 🆘 Troubleshooting
- **Connection failed**: Check if REDIS_URL is correct
- **Rate limited**: You've hit the free tier limit
- **Timeout**: Check your region selection

## 💰 Pricing
- **Free**: 10,000 requests/day, 256MB storage
- **Pay-as-you-go**: $0.2 per 100K requests
- **Pro**: $0.1 per 100K requests (with commitment)

Perfect for development and small production workloads! 🎉
