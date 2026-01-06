# 🔄 DEPLOYMENT WORKFLOW - Nexora001 Docker

Complete workflow for making changes locally, testing, and deploying to production server.

---

## 📋 WORKFLOW OVERVIEW

```
Local Development → Test Locally → Git Push → Server Pull → Deploy
```

---

## 🖥️ PHASE 1: LOCAL DEVELOPMENT & TESTING

### Location: Windows Machine (`D:\SelfLearning\AIChatBot\docker\`)

### Step 1.1: Make Code Changes
```powershell
# Open your code editor
cd D:\SelfLearning\AIChatBot\docker\Nexora001

# Make changes to backend code
# Example: Edit src/nexora001/api/routes/chat.py

# Or make changes to frontend
cd ..\Nexora001_Frontend
# Example: Edit src/components/ChatInterface.jsx
```

### Step 1.2: Test Backend Changes Locally
```powershell
# Terminal 1 - Backend
cd D:\SelfLearning\AIChatBot\docker\Nexora001

# Rebuild backend only (if code changed)
docker compose build backend

# Restart backend
docker compose up -d backend

# Check logs
docker compose logs -f backend

# Test API
curl http://localhost/api/
curl http://localhost/api/docs
```

### Step 1.3: Test Frontend Changes Locally
```powershell
# Terminal 2 - Frontend
cd D:\SelfLearning\AIChatBot\docker\Nexora001_Frontend

# Rebuild frontend only (if code changed)
docker compose -f ../Nexora001/docker-compose.yml build frontend

# Restart frontend
docker compose -f ../Nexora001/docker-compose.yml up -d frontend

# Open browser
start http://localhost
```

### Step 1.4: Test with Postman
```powershell
# Import collection
# File: Nexora001_Complete_API.postman_collection.json

# Update environment variables:
# - base_url: http://localhost/api
# - test_email: your test email
# - test_password: your test password

# Run tests in order:
# 1. Register/Login → Get token
# 2. Test your new changes
# 3. Verify everything works
```

### Step 1.5: Verify All Services
```powershell
# Check all containers
docker compose ps

# Should show all healthy:
# - nexora-mongodb (healthy)
# - nexora-qdrant (healthy)
# - nexora-backend (healthy)
# - nexora-frontend (healthy)
# - nexora-nginx (running)

# Test full workflow:
# 1. Login at http://localhost
# 2. Upload document
# 3. Chat with RAG
# 4. Check Qdrant dashboard: http://localhost:6333/dashboard
```

---

## 📦 PHASE 2: COMMIT & PUSH TO GITHUB

### Location: Windows Machine

### Step 2.1: Backend Changes
```powershell
cd D:\SelfLearning\AIChatBot\docker\Nexora001

# Check status
git status

# Add changed files
git add .

# Commit with descriptive message
git commit -m "Fix: Improve chat response accuracy"
# Or: "Feature: Add document filtering"
# Or: "Update: Optimize Qdrant search"

# Push to GitHub
git push origin main

# Verify push succeeded
git log --oneline -5
```

### Step 2.2: Frontend Changes
```powershell
cd D:\SelfLearning\AIChatBot\docker\Nexora001_Frontend

# Check status
git status

# Add changed files
git add .

# Commit
git commit -m "UI: Improve chat interface styling"

# Push to GitHub
git push origin main
```

### Step 2.3: Verify on GitHub
```powershell
# Open browser and verify commits appear
start https://github.com/Bhanura/Nexora001
start https://github.com/Bhanura/Nexora001_Frontend
```

---

## 🚀 PHASE 3: DEPLOY TO PRODUCTION SERVER

### Location: SSH to Server (`root@46.250.244.245`)

### Step 3.1: Connect to Server
```powershell
# From Windows PowerShell
ssh root@46.250.244.245
```

### Step 3.2: Pull Backend Changes
```bash
# Navigate to backend
cd ~/Nexora001

# Check current status
git status
docker compose ps

# Pull latest changes
git pull origin main

# View what changed
git log --oneline -3
```

### Step 3.3: Pull Frontend Changes (if needed)
```bash
# Navigate to frontend
cd ~/Nexora001_Frontend

# Pull changes
git pull origin main
```

### Step 3.4: Rebuild & Deploy

#### Option A: Rebuild Everything (Safest)
```bash
cd ~/Nexora001

# Stop all services
docker compose down

# Rebuild all images
docker compose build --no-cache

# Start all services
docker compose up -d

# Wait for startup
sleep 30

# Check status
docker compose ps
```

#### Option B: Rebuild Specific Service (Faster)
```bash
cd ~/Nexora001

# If only backend changed:
docker compose build backend
docker compose up -d backend

# If only frontend changed:
docker compose build frontend
docker compose up -d frontend

# If only nginx config changed:
docker cp ~/Nexora001/nginx/default.conf nexora-nginx:/etc/nginx/conf.d/default.conf
docker exec nexora-nginx nginx -s reload

# Wait and check
sleep 10
docker compose ps
```

#### Option C: Use Deploy Script (Recommended)
```bash
cd ~/Nexora001

# Make script executable (first time only)
chmod +x deploy.sh

# Run deployment
./deploy.sh

# Script does:
# 1. Pull latest code
# 2. Rebuild changed services
# 3. Restart containers
# 4. Check health
```

### Step 3.5: Verify Deployment
```bash
# Check all containers healthy
docker compose ps

# Expected output:
# nexora-backend    Up (healthy)
# nexora-frontend   Up (healthy)
# nexora-mongodb    Up (healthy)
# nexora-qdrant     Up (healthy)
# nexora-nginx      Up

# Check logs for errors
docker compose logs backend --tail=50
docker compose logs frontend --tail=20

# Test API
curl http://46.250.244.245/api/
curl http://46.250.244.245/api/status

# Test frontend
curl -I http://46.250.244.245/
```

### Step 3.6: Test in Browser
```bash
# Print URL
echo "Test at: http://46.250.244.245"

# Exit SSH (from Windows, test in browser)
exit
```

```powershell
# From Windows - open browser
start http://46.250.244.245

# Test your changes:
# 1. Login
# 2. Test new feature
# 3. Verify everything works
```

---

## 🔍 PHASE 4: MONITORING & ROLLBACK

### Step 4.1: Monitor Logs
```bash
# SSH back to server
ssh root@46.250.244.245

# Watch logs in real-time
docker compose logs -f

# Or specific service
docker compose logs -f backend
docker compose logs -f frontend

# Press Ctrl+C to stop watching
```

### Step 4.2: Check Resource Usage
```bash
# Container stats
docker stats

# Disk usage
docker system df

# Overall system
htop
# Press q to quit
```

### Step 4.3: Rollback if Needed
```bash
cd ~/Nexora001

# View git history
git log --oneline -10

# Rollback to previous commit
git revert HEAD
# Or: git reset --hard PREVIOUS_COMMIT_HASH

# Rebuild and deploy
docker compose down
docker compose build
docker compose up -d
```

---

## 🛠️ COMMON SCENARIOS

### Scenario 1: Changed Python Code (Backend)
```powershell
# WINDOWS (Local)
cd D:\SelfLearning\AIChatBot\docker\Nexora001
# Edit: src/nexora001/api/routes/chat.py
docker compose build backend
docker compose up -d backend
# Test at http://localhost/api/docs

git add .
git commit -m "Fix: Improve chat routing"
git push origin main
```

```bash
# SERVER (Production)
ssh root@46.250.244.245
cd ~/Nexora001
git pull origin main
docker compose build backend
docker compose up -d backend
docker compose logs backend --tail=50
# Test at http://46.250.244.245/api/docs
```

---

### Scenario 2: Changed React Code (Frontend)
```powershell
# WINDOWS (Local)
cd D:\SelfLearning\AIChatBot\docker\Nexora001_Frontend
# Edit: src/components/ChatInterface.jsx
cd ..\Nexora001
docker compose build frontend
docker compose up -d frontend
# Test at http://localhost

git -C ../Nexora001_Frontend add .
git -C ../Nexora001_Frontend commit -m "UI: Update chat interface"
git -C ../Nexora001_Frontend push origin main
```

```bash
# SERVER (Production)
ssh root@46.250.244.245
cd ~/Nexora001_Frontend
git pull origin main
cd ~/Nexora001
docker compose build frontend
docker compose up -d frontend
# Test at http://46.250.244.245
```

---

### Scenario 3: Changed Nginx Config
```powershell
# WINDOWS (Local)
cd D:\SelfLearning\AIChatBot\docker\Nexora001
# Edit: nginx/default.conf
docker compose restart nginx
# Test routing at http://localhost

git add nginx/default.conf
git commit -m "Config: Update nginx routing"
git push origin main
```

```bash
# SERVER (Production)
ssh root@46.250.244.245
cd ~/Nexora001
git pull origin main
docker cp nginx/default.conf nexora-nginx:/etc/nginx/conf.d/default.conf
docker exec nexora-nginx nginx -s reload
# Test at http://46.250.244.245
```

---

### Scenario 4: Changed .env Configuration
```powershell
# WINDOWS (Local)
cd D:\SelfLearning\AIChatBot\docker\Nexora001
# Edit: .env (NEVER commit this file!)
docker compose down
docker compose up -d
# Test changes
```

```bash
# SERVER (Production)
ssh root@46.250.244.245
cd ~/Nexora001
nano .env  # Make same changes manually
docker compose down
docker compose up -d
# Verify with: docker compose ps
```

---

### Scenario 5: Added New Python Dependencies
```powershell
# WINDOWS (Local)
cd D:\SelfLearning\AIChatBot\docker\Nexora001
# Edit: requirements.txt (add new package)
docker compose build --no-cache backend
docker compose up -d backend
# Test import works

git add requirements.txt
git commit -m "Dependencies: Add new-package"
git push origin main
```

```bash
# SERVER (Production)
ssh root@46.250.244.245
cd ~/Nexora001
git pull origin main
docker compose build --no-cache backend
docker compose up -d backend
docker compose logs backend --tail=50
```

---

## 📊 QUICK REFERENCE COMMANDS

### Local Testing (Windows)
```powershell
# Rebuild & restart
docker compose build <service>
docker compose up -d <service>

# View logs
docker compose logs -f <service>

# Check status
docker compose ps

# Access containers
docker exec -it nexora-backend bash
docker exec -it nexora-mongodb mongosh

# Test endpoints
curl http://localhost/api/
curl http://localhost/health
```

### Git Operations (Windows)
```powershell
git status                    # Check changes
git add .                     # Stage all
git add file.py               # Stage specific file
git commit -m "message"       # Commit
git push origin main          # Push to GitHub
git log --oneline -5          # View recent commits
git diff                      # See changes
```

### Server Deployment (Linux)
```bash
# Update code
cd ~/Nexora001
git pull origin main

# Quick rebuild
docker compose up -d --build <service>

# Full rebuild
docker compose down
docker compose build --no-cache
docker compose up -d

# Check health
docker compose ps
docker compose logs <service> --tail=50

# Monitor
docker compose logs -f
docker stats
```

---

## ⚠️ IMPORTANT NOTES

1. **Always test locally first** before deploying to server
2. **Never commit .env files** (they contain secrets)
3. **Use descriptive commit messages** for easy rollback
4. **Check logs** after every deployment
5. **Monitor for 5-10 minutes** after production deploy
6. **Keep backups** of MongoDB data (automated in docker-compose)
7. **Use `--no-cache`** when changing dependencies
8. **Restart nginx** after config changes
9. **Update Postman collection** after API changes
10. **Test with real user accounts** on production

---

## 🚨 TROUBLESHOOTING DEPLOYMENT

### Container won't start
```bash
docker compose ps                    # Check status
docker compose logs <service>        # View errors
docker compose down && docker compose up -d  # Full restart
```

### Code changes not applied
```bash
docker compose build --no-cache <service>  # Force rebuild
docker system prune -a -f                  # Clean old images
```

### Can't access frontend
```bash
curl -I http://46.250.244.245/          # Test nginx
docker compose logs nginx               # Check routing
docker compose restart nginx            # Reload config
```

### Database connection errors
```bash
docker compose logs backend              # Check MongoDB URI
docker exec nexora-mongodb mongosh       # Test MongoDB
docker network inspect nexora-network    # Check networking
```

---

## 📝 DEPLOYMENT CHECKLIST

- [ ] Changes tested locally at http://localhost
- [ ] All tests pass in Postman collection
- [ ] No errors in local container logs
- [ ] Code committed with descriptive message
- [ ] Pushed to GitHub successfully
- [ ] SSH to production server
- [ ] Git pull latest changes
- [ ] Rebuild affected containers
- [ ] All containers show healthy status
- [ ] No errors in production logs
- [ ] Tested in browser at http://46.250.244.245
- [ ] API endpoints working correctly
- [ ] Monitor logs for 5-10 minutes
- [ ] Document any issues or changes

---

**Happy Deploying! 🚀**
