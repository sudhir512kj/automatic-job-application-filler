#!/bin/bash

# Deploy both frontend and backend to same EC2 instance
set -e

AWS_REGION=${AWS_DEFAULT_REGION:-$(aws configure get region)}
KEY_NAME="auto-form-filler-key"
INSTANCE_NAME="auto-form-filler-fullstack"

echo "🚀 Deploying Full Stack to EC2..."

# 0. Create IAM role for Secrets Manager access
aws iam create-role --role-name EC2SecretsManagerRole --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "ec2.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}' 2>/dev/null || echo "Role exists"

aws iam attach-role-policy --role-name EC2SecretsManagerRole --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite 2>/dev/null || true

aws iam create-instance-profile --instance-profile-name EC2SecretsManagerRole 2>/dev/null || echo "Instance profile exists"
aws iam add-role-to-instance-profile --instance-profile-name EC2SecretsManagerRole --role-name EC2SecretsManagerRole 2>/dev/null || true

# Wait for IAM propagation
sleep 10

# 1. Create key pair
if [ ! -f ~/.ssh/$KEY_NAME.pem ]; then
  aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > ~/.ssh/$KEY_NAME.pem
  chmod 400 ~/.ssh/$KEY_NAME.pem
else
  echo "Key pair file exists"
fi

# 2. Create security group
SG_ID=$(aws ec2 create-security-group \
  --group-name auto-form-filler-fullstack-sg \
  --description "Fullstack security group" \
  --query 'GroupId' --output text 2>/dev/null || \
  aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=auto-form-filler-fullstack-sg" \
  --query 'SecurityGroups[0].GroupId' --output text)

aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0 2>/dev/null || true
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0 2>/dev/null || true
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 8000 --cidr 0.0.0.0/0 2>/dev/null || true

# 3. Check if instance exists, create if not
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=$INSTANCE_NAME" "Name=instance-state-name,Values=running,pending,stopped" \
  --query 'Reservations[0].Instances[0].InstanceId' --output text 2>/dev/null)

if [ "$INSTANCE_ID" = "None" ] || [ -z "$INSTANCE_ID" ]; then
  echo "Creating new EC2 instance..."
  INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0c7217cdde317cfec \
    --count 1 \
    --instance-type t3.small \
    --key-name $KEY_NAME \
    --security-group-ids $SG_ID \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
    --iam-instance-profile Name=EC2SecretsManagerRole \
    --user-data file://aws/fullstack-user-data.sh \
    --query 'Instances[0].InstanceId' --output text)
else
  echo "Using existing instance: $INSTANCE_ID"
  # Start instance if stopped
  aws ec2 start-instances --instance-ids $INSTANCE_ID 2>/dev/null || true
fi

echo "⏳ Waiting for instance to start..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# 4. Get public IP
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo "✅ Full Stack deployed!"
echo "🌐 Frontend: http://$PUBLIC_IP"
echo "🌐 Backend: http://$PUBLIC_IP:8000"
echo "🔑 SSH: ssh -i ~/.ssh/$KEY_NAME.pem ubuntu@$PUBLIC_IP"
echo "💰 Cost: ~$17/month (t3.small)"