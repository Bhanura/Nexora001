# 🧪 LOCAL TESTING GUIDE - Nexora001 Docker Migration

This guide will help you test the complete Docker setup on your local Windows machine before deploying to the server.

## Prerequisites

- ✅ Docker Desktop installed and running on Windows
- ✅ Git installed
- ✅ Google API Key (for Gemini)
- ✅ Ports available: 80, 6333, 27017

---

## 📋 Step 1: Prepare Environment

### 1.1 Navigate to Backend Directory
```powershell
cd D:\SelfLearning\AIChatBot\docker\Nexora001
```

### 1.2 Create .env File
```powershell
# Copy example file
Copy-Item .env.example .env

# Edit with your values
notepad .env
```

### 1.3 Update .env for Local Testing
```env
# Local MongoDB
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=localtest123
MONGODB_URI=mongodb://admin:localtest123@mongodb:27017
MONGODB_DATABASE=nexora001

# Qdrant (container name)
USE_QDRANT=true
QDRANT_URL=http://qdrant:6333

# Your Google API Key
GOOGLE_API_KEY=your-actual-api-key-here

# JWT Secret (generate with: openssl rand -hex 32)
JWT_SECRET_KEY=your-local-secret-key-for-testing

# Local settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

---

## 🏗️ Step 2: Build and Start Containers

### 2.1 Build All Services
```powershell
# Build without cache (fresh build)
docker-compose build --no-cache

# Or build with cache (faster)
docker-compose build
```

### 2.2 Start All Services
```powershell
# Start in detached mode
docker-compose up -d

# Or start with logs visible (good for debugging)
docker-compose up
```

### 2.3 Check Container Status
```powershell
# View running containers
docker-compose ps

# Should see 5 containers:
# - nexora-mongodb (healthy)
# - nexora-qdrant (healthy)
# - nexora-backend (healthy)
# - nexora-frontend (healthy)
# - nexora-nginx (healthy)
```

---

## 🔍 Step 3: Verify Each Service

### 3.1 Check MongoDB
```powershell
# Test connection
docker exec -it nexora-mongodb mongosh -u admin -p localtest123

# In MongoDB shell:
show dbs
use nexora001
show collections
exit
```

### 3.2 Check Qdrant
```powershell
# Open in browser
Start-Process "http://localhost:6333/dashboard"

# Or use curl
curl http://localhost:6333
curl http://localhost:6333/collections
```

### 3.3 Check Backend API
```powershell
# Health check
curl http://localhost/api/

# API documentation
Start-Process "http://localhost/api/docs"

# Test connection endpoint
curl http://localhost/api/system/test-connections
```

### 3.4 Check Frontend
```powershell
# Open frontend
Start-Process "http://localhost"
```

---

## 📊 Step 4: View Logs

### View All Logs
```powershell
docker-compose logs -f
```

### View Specific Service Logs
```powershell
# Backend logs
docker-compose logs -f backend

# Qdrant logs
docker-compose logs -f qdrant

# Nginx logs
docker-compose logs -f nginx

# Frontend logs
docker-compose logs -f frontend
```

---

## 🧪 Step 5: Test API Endpoints

### 5.1 Test Authentication
```powershell
# Register a test user (PowerShell)
$headers = @{"Content-Type"="application/json"}
$body = @{
    username = "testuser"
    email = "test@example.com"
    password = "Test123456!"
    full_name = "Test User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost/api/auth/register" -Method POST -Headers $headers -Body $body
```

### 5.2 Test Document Ingestion
```powershell
# First, get auth token from login
# Then test document upload (use Postman or API docs at /docs)
Start-Process "http://localhost/api/docs#/Ingest"
```

### 5.3 Test RAG Chat
```powershell
# Use API docs to test chat
Start-Process "http://localhost/api/docs#/Chat"
```

---

## 🐛 Step 6: Troubleshooting

### Container Not Starting?
```powershell
# Check specific container logs
docker-compose logs backend

# Check if ports are in use
netstat -ano | findstr "80"
netstat -ano | findstr "6333"
netstat -ano | findstr "27017"
```

### Backend Can't Connect to MongoDB?
```powershell
# Verify MongoDB is healthy
docker inspect nexora-mongodb

# Check network connectivity
docker exec nexora-backend ping -c 3 mongodb
```

### Qdrant Connection Issues?
```powershell
# Check Qdrant health
docker exec nexora-qdrant curl http://localhost:6333

# Check from backend
docker exec nexora-backend curl http://qdrant:6333
```

### Frontend Not Loading?
```powershell
# Check frontend build
docker-compose logs frontend

# Check nginx config
docker exec nexora-nginx cat /etc/nginx/conf.d/default.conf
```

---

## 🔄 Step 7: Restart/Rebuild Services

### Restart All Services
```powershell
docker-compose restart
```

### Restart Specific Service
```powershell
docker-compose restart backend
```

### Rebuild After Code Changes
```powershell
# Stop containers
docker-compose down

# Rebuild specific service
docker-compose build backend

# Start again
docker-compose up -d
```

---

## 🧹 Step 8: Clean Up

### Stop All Containers
```powershell
docker-compose down
```

### Remove Volumes (WARNING: Deletes data!)
```powershell
docker-compose down -v
```

### Remove Images
```powershell
docker-compose down --rmi all
```

### Complete Cleanup
```powershell
docker-compose down -v --rmi all
docker system prune -a
```

---

## ✅ Step 9: Success Checklist

Before deploying to server, verify:

- [ ] All 5 containers are running and healthy
- [ ] MongoDB accepts connections
- [ ] Qdrant dashboard accessible at http://localhost:6333/dashboard
- [ ] Backend API docs work at http://localhost/api/docs
- [ ] Frontend loads at http://localhost
- [ ] Can register a user
- [ ] Can login and get JWT token
- [ ] Can upload a document
- [ ] Can query with RAG chat
- [ ] Qdrant collections show embeddings
- [ ] No errors in any container logs

---

## 📝 Common Issues & Solutions

### Issue: "Port already in use"
**Solution**: Stop other services using ports 80, 6333, or 27017
```powershell
# Find process using port 80
netstat -ano | findstr :80
# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue: "Backend can't connect to Qdrant"
**Solution**: Ensure QDRANT_URL uses container name
```env
QDRANT_URL=http://qdrant:6333  # NOT localhost!
```

### Issue: "Frontend shows connection refused"
**Solution**: Check backend is running and nginx config is correct
```powershell
docker-compose logs nginx
docker exec nexora-nginx nginx -t
```

---

## 🎯 Next Steps

Once local testing is successful:
1. ✅ Commit changes to GitHub
2. ✅ Review SERVER_DEPLOYMENT_GUIDE.md
3. ✅ Deploy to production server

---

**Need Help?** Check logs with: `docker-compose logs -f`
