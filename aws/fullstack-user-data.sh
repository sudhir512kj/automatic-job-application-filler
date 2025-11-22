#!/bin/bash

# Full Stack User Data - Install both frontend and backend
# Exit on any error and log everything
set -e
set -x
exec > >(tee /var/log/user-data.log) 2>&1
echo "$(date): Starting user data script"
echo "$(date): Installing packages..."
apt update -y
apt install -y git awscli python3 python3-pip nginx nodejs npm curl
# Create symlinks for convenience
ln -sf /usr/bin/python3 /usr/local/bin/python3
ln -sf /usr/bin/pip3 /usr/local/bin/pip3

echo "$(date): Packages installed successfully"

echo "$(date): Starting services..."
systemctl start nginx
systemctl enable nginx
echo "$(date): Services started successfully"



echo "$(date): Cloning repository..."
cd /home/ubuntu
git clone https://github.com/sudhir512kj/automatic-job-application-filler.git
cd automatic-job-application-filler
echo "$(date): Repository cloned successfully"

# Setup backend - Get secrets from AWS Secrets Manager
echo "$(date): Setting up backend..."
OPENROUTER_KEY=$(aws secretsmanager get-secret-value --secret-id auto-form-filler/openrouter-key --query SecretString --output text --region $(curl -s http://169.254.169.254/latest/meta-data/placement/region) 2>/dev/null || echo "")
LLAMA_KEY=$(aws secretsmanager get-secret-value --secret-id auto-form-filler/llama-key --query SecretString --output text --region $(curl -s http://169.254.169.254/latest/meta-data/placement/region) 2>/dev/null || echo "")

cat > backend/.env << EOF
OPENROUTER_API_KEY=${OPENROUTER_KEY}
LLAMA_CLOUD_API_KEY=${LLAMA_KEY}
EOF

# Install Python dependencies
cd backend
# Use the exact requirements.txt
pip3 install -r requirements.txt

# Create systemd service for backend
cat > /etc/systemd/system/backend.service << EOF
[Unit]
Description=Auto Form Filler Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/automatic-job-application-filler/backend
EnvironmentFile=/home/ubuntu/automatic-job-application-filler/backend/.env
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable backend
systemctl start backend
echo "$(date): Backend started successfully"

echo "$(date): Setting up frontend..."
cd frontend
npm install
echo "$(date): Building frontend..."
REACT_APP_API_URL=http://localhost:8000 npm run build
echo "$(date): Frontend built successfully"

# Configure nginx for frontend
cat > /etc/nginx/conf.d/frontend.conf << EOF
server {
    listen 80;
    root /home/ubuntu/automatic-job-application-filler/frontend/build;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

systemctl restart nginx

# Log setup completion
echo "$(date): Full stack setup complete" >> /var/log/user-data.log
echo "Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)" >> /var/log/user-data.log
echo "Backend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000" >> /var/log/user-data.log