# 🚀 Quick Reference - Docker Commands

## 🎬 Starting & Stopping

```bash
# Start all services
docker compose up -d

# Start with logs visible
docker compose up

# Stop all services
docker compose down

# Stop and remove volumes (⚠️ DELETES DATA)
docker compose down -v
```

## 🔍 Monitoring

```bash
# Check container status
docker compose ps

# View all logs (follow)
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f qdrant
docker compose logs -f nginx

# Last 100 lines
docker compose logs --tail=100

# Real-time resource usage
docker stats
```

## 🔄 Restart & Rebuild

```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart backend

# Rebuild after code changes
docker compose build backend
docker compose up -d

# Rebuild everything (no cache)
docker compose build --no-cache
docker compose up -d
```

## 🐛 Debugging

```bash
# Execute command in container
docker exec -it nexora-backend bash
docker exec -it nexora-mongodb mongosh -u admin -p PASSWORD

# Check container logs
docker logs nexora-backend

# Inspect container
docker inspect nexora-backend

# Check networks
docker network ls
docker network inspect nexora001_nexora-network

# Test connectivity between containers
docker exec nexora-backend ping mongodb
docker exec nexora-backend curl http://qdrant:6333
```

## 🧹 Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Clean everything (⚠️ BE CAREFUL)
docker system prune -a
```

## 💾 Backup & Restore

```bash
# Backup MongoDB
docker exec nexora-mongodb mongodump \
  -u admin -p PASSWORD \
  --authenticationDatabase admin \
  --out /tmp/backup
docker cp nexora-mongodb:/tmp/backup ./backup

# Restore MongoDB
docker cp ./backup nexora-mongodb:/tmp/
docker exec nexora-mongodb mongorestore \
  -u admin -p PASSWORD \
  --authenticationDatabase admin \
  /tmp/backup

# Backup Qdrant (via volume)
docker run --rm \
  -v nexora001_qdrant_storage:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/qdrant_backup.tar.gz /data
```

## 🔗 Quick URLs

```bash
# Local development
Frontend:        http://localhost
API Docs:        http://localhost/api/docs
Qdrant Dashboard: http://localhost:6333/dashboard
Health Check:    http://localhost/health

# Production (replace with your IP/domain)
Frontend:        http://46.250.244.245
API Docs:        http://46.250.244.245/api/docs
Qdrant Dashboard: http://46.250.244.245:6333/dashboard
```

## 📊 Health Checks

```bash
# Check all services are healthy
docker compose ps

# Test endpoints
curl http://localhost/health
curl http://localhost/api/
curl http://localhost:6333

# MongoDB ping
docker exec nexora-mongodb mongosh \
  -u admin -p PASSWORD \
  --eval "db.adminCommand('ping')"
```

## ⚙️ Environment

```bash
# Edit environment variables
nano .env

# Restart after .env changes
docker compose down
docker compose up -d

# View environment in container
docker exec nexora-backend env | grep MONGODB
```

## 📁 Important Files

```
.env                     # Your secrets (NEVER commit!)
.env.example             # Template for .env
docker-compose.yml       # Service orchestration
Dockerfile               # Backend container build
nginx/default.conf       # Reverse proxy config
deploy.sh                # Deployment automation
```

## 🆘 Emergency Commands

```bash
# Force stop everything
docker compose kill

# Force remove all containers
docker rm -f $(docker ps -aq)

# Check what's using port 80
netstat -tulpn | grep :80
# Windows: netstat -ano | findstr :80

# Restart Docker daemon (Linux)
sudo systemctl restart docker

# View Docker daemon logs
journalctl -u docker -f
```

## 📈 Performance

```bash
# Limit container resources (add to docker-compose.yml)
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G

# View disk usage
docker system df

# See which containers use most space
docker ps -s
```

## 🔐 Security

```bash
# Generate secure JWT secret
openssl rand -hex 32

# Generate secure password
openssl rand -base64 32

# Check exposed ports
docker compose port nginx 80
```

---

**Need more details?**
- Local Testing: [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md)
- Server Deployment: [SERVER_DEPLOYMENT_GUIDE.md](SERVER_DEPLOYMENT_GUIDE.md)
- Full Summary: [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)
