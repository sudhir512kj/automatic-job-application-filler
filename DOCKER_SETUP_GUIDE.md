# 🐳 Docker Setup Guide - Auto Form Filling GenAI Agent

This guide provides a complete walkthrough for running the Auto Form Filling GenAI Agent using Docker. Perfect for developers who want a consistent, isolated environment.

## 📋 Prerequisites

Before starting, ensure you have:

- **Docker Desktop** installed ([Download here](https://www.docker.com/products/docker-desktop/))
- **Docker Compose** (included with Docker Desktop)
- **Git** installed
- **API Keys** (we'll get these in Step 2)

### Verify Docker Installation
```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Test Docker is running
docker run hello-world
```

## 🚀 Step-by-Step Setup Process

### Step 1: Clone the Repository

```bash
# Clone the project
git clone <your-repo-url>
cd auto-form-filling-agent

# Verify project structure
ls -la
```

You should see:
```
├── backend/
├── frontend/
├── aws/
├── docker-compose.yml
├── .env.example
└── README.md
```

### Step 2: Get Required API Keys

#### 🔑 OpenRouter API Key (Free)

1. **Visit**: [OpenRouter.ai](https://openrouter.ai/)
2. **Sign Up**: Create a free account
3. **Navigate**: Go to "Keys" section in dashboard
4. **Create**: Click "Create Key"
5. **Copy**: Save the key (format: `sk-or-v1-...`)

#### 🔑 Llama Cloud API Key (Free)

1. **Visit**: [Llama Cloud](https://cloud.llamaindex.ai/)
2. **Sign Up**: Create a free account
3. **Navigate**: Go to "API Keys" section
4. **Create**: Click "Create API Key"
5. **Copy**: Save the key (format: `llx-...`)

### Step 3: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file
nano .env
# or use your preferred editor: code .env, vim .env, etc.
```

**Add your API keys to `.env`:**
```env
# OpenRouter API Key (for AI processing)
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here

# Llama Cloud API Key (for document parsing)
LLAMA_CLOUD_API_KEY=llx-your-actual-key-here

# Optional: Environment settings
ENVIRONMENT=development
DEBUG=true
```

### Step 4: Understanding Docker Configuration

#### Docker Compose Structure

The `docker-compose.yml` file defines two services:

```yaml
services:
  backend:
    # FastAPI server running on port 8000
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - LLAMA_CLOUD_API_KEY=${LLAMA_CLOUD_API_KEY}
    volumes:
      - ./backend:/app
    
  frontend:
    # React app running on port 3000
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
```

#### Container Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (React)       │────│   (FastAPI)     │
│   Port: 3000    │    │   Port: 8000    │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
              Docker Network
```

### Step 5: Build and Run with Docker

#### Option A: Quick Start (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Or run in background (detached mode)
docker-compose up --build -d
```

#### Option B: Step-by-Step Build

```bash
# Build containers first
docker-compose build

# Start services
docker-compose up

# Or start specific service
docker-compose up backend
docker-compose up frontend
```

### Step 6: Verify Installation

#### Check Running Containers
```bash
# List running containers
docker-compose ps

# Expected output:
# NAME                    COMMAND                  SERVICE    STATUS    PORTS
# auto-form-backend       "python main.py"         backend    Up        0.0.0.0:8000->8000/tcp
# auto-form-frontend      "npm start"              frontend   Up        0.0.0.0:3000->3000/tcp
```

#### Test Application Endpoints

**Backend Health Check:**
```bash
# Test backend API
curl http://localhost:8000/api/health

# Expected response:
# {"status": "healthy", "message": "Auto Form Filling Agent API is running"}
```

**Frontend Access:**
- Open browser: `http://localhost:3000`
- You should see the React application interface

**Backend API Documentation:**
- Open browser: `http://localhost:8000/docs`
- Interactive API documentation (Swagger UI)

## 🔧 Docker Management Commands

### Container Operations

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Stop and remove containers, networks, volumes
docker-compose down -v
```

### Development Commands

```bash
# View logs (all services)
docker-compose logs

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f

# Execute commands inside container
docker-compose exec backend bash
docker-compose exec frontend bash

# Rebuild specific service
docker-compose build backend
docker-compose build frontend
```

### Debugging Commands

```bash
# Check container status
docker-compose ps

# Inspect container details
docker inspect auto-form-backend

# View container resource usage
docker stats

# Remove unused containers/images
docker system prune
```

## 🛠️ Development Workflow

### Making Code Changes

**Backend Changes:**
1. Edit files in `./backend/`
2. Changes are automatically reflected (volume mounting)
3. If you add new dependencies, rebuild:
   ```bash
   docker-compose build backend
   docker-compose up backend
   ```

**Frontend Changes:**
1. Edit files in `./frontend/`
2. React hot-reload will update automatically
3. If you add new npm packages, rebuild:
   ```bash
   docker-compose build frontend
   docker-compose up frontend
   ```

### Adding New Dependencies

**Python Dependencies (Backend):**
```bash
# Add to backend/requirements.txt
echo "new-package==1.0.0" >> backend/requirements.txt

# Rebuild backend container
docker-compose build backend
docker-compose up backend
```

**Node Dependencies (Frontend):**
```bash
# Execute inside frontend container
docker-compose exec frontend npm install new-package

# Or rebuild container
docker-compose build frontend
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue: "Port already in use"
```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

#### Issue: "API keys not working"
```bash
# Check environment variables inside container
docker-compose exec backend env | grep API

# Verify .env file exists and has correct format
cat .env
```

#### Issue: "Container won't start"
```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose build --no-cache
```

#### Issue: "Cannot connect to backend"
```bash
# Verify backend is running
curl http://localhost:8000/api/health

# Check network connectivity
docker-compose exec frontend ping backend
```

### Performance Issues

#### Slow Build Times
```bash
# Use Docker build cache
docker-compose build

# Clean build (slower but fresh)
docker-compose build --no-cache

# Remove unused images
docker image prune
```

#### Memory Issues
```bash
# Check Docker resource usage
docker stats

# Increase Docker Desktop memory allocation
# Docker Desktop → Settings → Resources → Memory
```

## 📊 Container Monitoring

### Health Checks

```bash
# Check container health
docker-compose ps

# Detailed health information
docker inspect --format='{{.State.Health.Status}}' auto-form-backend
```

### Log Management

```bash
# View recent logs
docker-compose logs --tail=50

# Save logs to file
docker-compose logs > application.log

# Filter logs by service
docker-compose logs backend | grep ERROR
```

## 🔒 Security Best Practices

### Environment Variables
- Never commit `.env` file to version control
- Use strong API keys
- Rotate keys regularly

### Container Security
```bash
# Run containers as non-root user (already configured)
# Limit container resources
# Keep base images updated
```

## 🚀 Production Deployment

### Docker Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Run production containers
docker-compose -f docker-compose.prod.yml up -d
```

### Environment-Specific Configs

Create separate compose files:
- `docker-compose.yml` (development)
- `docker-compose.prod.yml` (production)
- `docker-compose.test.yml` (testing)

## 📝 Quick Reference

### Essential Commands
```bash
# Start everything
docker-compose up --build

# Stop everything
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose down && docker-compose up --build

# Clean restart
docker-compose down -v && docker-compose up --build
```

### Application URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 🎯 Next Steps

1. **Test the Application**: Upload a resume and try filling a Google Form
2. **Explore API**: Visit http://localhost:8000/docs
3. **Customize**: Modify code and see changes in real-time
4. **Deploy**: Use AWS deployment guide for production

## 🆘 Getting Help

If you encounter issues:

1. **Check logs**: `docker-compose logs`
2. **Verify setup**: Follow this guide step-by-step
3. **Clean restart**: `docker-compose down -v && docker-compose up --build`
4. **Create GitHub issue**: Include logs and error messages

---

**🎉 Congratulations!** You now have a fully functional Auto Form Filling Agent running in Docker containers.

*Happy Dockerizing! 🐳*