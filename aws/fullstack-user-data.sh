#!/bin/bash

# Full Stack User Data - Install both frontend and backend
# Exit on any error and log everything
set -e
set -x
exec > >(tee /var/log/user-data.log) 2>&1
echo "$(date): Starting user data script"
echo "$(date): Installing packages..."

# Update system
sudo apt update -y

# Install required packages
sudo apt install -y git awscli python3 python3-pip nginx nodejs npm curl

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "$(date): Packages installed successfully"

echo "$(date): Starting services..."
systemctl start nginx
systemctl enable nginx
echo "$(date): Services started successfully"



echo "$(date): Cloning repository..."
cd /home/ubuntu
git clone https://github.com/sudhir512kj/auto-form-filling-agent.git
cd auto-form-filling-agent
echo "$(date): Repository cloned successfully"

# Setup backend - Get secrets from AWS Secrets Manager
echo "$(date): Setting up backend..."
OPENROUTER_KEY=$(aws secretsmanager get-secret-value --secret-id auto-form-filler/openrouter-key --query SecretString --output text --region $(curl -s http://169.254.169.254/latest/meta-data/placement/region) 2>/dev/null || echo "")
LLAMA_KEY=$(aws secretsmanager get-secret-value --secret-id auto-form-filler/llama-key --query SecretString --output text --region $(curl -s http://169.254.169.254/latest/meta-data/placement/region) 2>/dev/null || echo "")

cat > backend/.env << EOF
OPENROUTER_API_KEY=${OPENROUTER_KEY}
LLAMA_CLOUD_API_KEY=${LLAMA_KEY}
EOF

# Use Docker Compose to run the application
echo "$(date): Starting application with Docker Compose..."
sudo docker-compose up -d --build
echo "$(date): Application started successfully"

# Configure nginx as reverse proxy
sudo tee /etc/nginx/sites-available/default > /dev/null << EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo systemctl restart nginx
echo "$(date): Nginx configured successfully"

# Log setup completion
echo "$(date): Full stack setup complete" >> /var/log/user-data.log
echo "Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)" >> /var/log/user-data.log
echo "Backend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000" >> /var/log/user-data.log