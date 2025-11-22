# AWS EC2 Deployment Guide

Simple deployment of both frontend and backend to a single EC2 instance with fixed IP.

## 🚀 Quick Deploy

### Deploy Full Stack
```bash
./deploy-fullstack-ec2.sh
```

**Output:**
- Frontend: `http://[EC2-IP]`
- Backend: `http://[EC2-IP]:8000`
- SSH: `ssh -i ~/.ssh/auto-form-filler-key.pem ec2-user@[EC2-IP]`

### Add API Keys
```bash
# SSH into instance
ssh -i ~/.ssh/auto-form-filler-key.pem ec2-user@[EC2-IP]

# Edit environment file
nano auto-form-filling-agent/backend/.env

# Add your keys:
OPENROUTER_API_KEY=your_openrouter_key_here
LLAMA_CLOUD_API_KEY=your_llama_cloud_key_here

# Restart backend
docker restart backend
```

### Clean Up (Stop All Charges)
```bash
./cleanup-all-resources.sh
```

## 💰 Cost

- **Running**: ~$17/month (t3.small EC2 instance)
- **After cleanup**: $0/month

## 🔧 What Gets Deployed

- **EC2 Instance**: t3.small with Docker, Nginx, Node.js
- **Backend**: FastAPI server on port 8000
- **Frontend**: React app served by Nginx on port 80
- **Security Group**: Allows HTTP (80), API (8000), SSH (22)
- **Key Pair**: For SSH access

## 🗑️ What Gets Cleaned Up

- EC2 instances
- Security groups  
- Key pairs
- Elastic IPs
- ECS services/clusters
- Load balancers
- ECR repositories
- CloudWatch logs
- Secrets Manager secrets

## 🔒 Security Features

- SSH key-based access only
- Security groups restrict access to necessary ports
- Environment variables for API keys
- Docker containerization

## 📁 Files

- `deploy-fullstack-ec2.sh` - Main deployment script
- `fullstack-user-data.sh` - EC2 initialization script
- `cleanup-all-resources.sh` - Resource cleanup script