#!/bin/bash

# Delete all AWS resources to stop charges
set -e

AWS_REGION=${AWS_DEFAULT_REGION:-$(aws configure get region)}

echo "🗑️ Cleaning up all AWS resources..."

# 1. Delete ECS Services
echo "Deleting ECS services..."
aws ecs update-service --cluster auto-form-filler-cluster --service auto-form-filler-demo --desired-count 0 2>/dev/null || true
aws ecs update-service --cluster auto-form-filler-cluster --service auto-form-filler-frontend --desired-count 0 2>/dev/null || true
sleep 30
aws ecs delete-service --cluster auto-form-filler-cluster --service auto-form-filler-demo --force 2>/dev/null || true
aws ecs delete-service --cluster auto-form-filler-cluster --service auto-form-filler-frontend --force 2>/dev/null || true

# 2. Delete ECS Cluster
echo "Deleting ECS cluster..."
aws ecs delete-cluster --cluster auto-form-filler-cluster 2>/dev/null || true

# 3. Delete EC2 Instances
echo "Terminating EC2 instances..."
BACKEND_INSTANCE=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=auto-form-filler-backend" "Name=instance-state-name,Values=running,pending,stopped" --query 'Reservations[0].Instances[0].InstanceId' --output text 2>/dev/null)
FULLSTACK_INSTANCE=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=auto-form-filler-fullstack" "Name=instance-state-name,Values=running,pending,stopped" --query 'Reservations[0].Instances[0].InstanceId' --output text 2>/dev/null)

[ "$BACKEND_INSTANCE" != "None" ] && aws ec2 terminate-instances --instance-ids $BACKEND_INSTANCE 2>/dev/null || true
[ "$FULLSTACK_INSTANCE" != "None" ] && aws ec2 terminate-instances --instance-ids $FULLSTACK_INSTANCE 2>/dev/null || true

# 4. Delete Security Groups
echo "Deleting security groups..."
aws ec2 delete-security-group --group-name auto-form-filler-sg 2>/dev/null || true
aws ec2 delete-security-group --group-name auto-form-filler-demo-sg 2>/dev/null || true
aws ec2 delete-security-group --group-name auto-form-filler-frontend-sg 2>/dev/null || true
aws ec2 delete-security-group --group-name auto-form-filler-fullstack-sg 2>/dev/null || true
aws ec2 delete-security-group --group-name auto-form-filler-alb-sg 2>/dev/null || true

# 5. Release Elastic IPs
echo "Releasing Elastic IPs..."
BACKEND_EIP_ID=$(aws ec2 describe-addresses --filters "Name=tag:Name,Values=backend-eip" --query 'Addresses[0].AllocationId' --output text 2>/dev/null)
FRONTEND_EIP_ID=$(aws ec2 describe-addresses --filters "Name=tag:Name,Values=frontend-eip" --query 'Addresses[0].AllocationId' --output text 2>/dev/null)

[ "$BACKEND_EIP_ID" != "None" ] && aws ec2 release-address --allocation-id $BACKEND_EIP_ID 2>/dev/null || true
[ "$FRONTEND_EIP_ID" != "None" ] && aws ec2 release-address --allocation-id $FRONTEND_EIP_ID 2>/dev/null || true

# 6. Delete Load Balancers
echo "Deleting load balancers..."
ALB_ARN=$(aws elbv2 describe-load-balancers --names auto-form-filler-alb --query 'LoadBalancers[0].LoadBalancerArn' --output text 2>/dev/null)
[ "$ALB_ARN" != "None" ] && aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN 2>/dev/null || true

# 7. Delete Target Groups
echo "Deleting target groups..."
aws elbv2 delete-target-group --target-group-arn $(aws elbv2 describe-target-groups --names backend-tg --query 'TargetGroups[0].TargetGroupArn' --output text) 2>/dev/null || true
aws elbv2 delete-target-group --target-group-arn $(aws elbv2 describe-target-groups --names frontend-tg --query 'TargetGroups[0].TargetGroupArn' --output text) 2>/dev/null || true

# 8. Delete ECR Repositories
echo "Deleting ECR repositories..."
aws ecr delete-repository --repository-name auto-form-filler --force 2>/dev/null || true
aws ecr delete-repository --repository-name auto-form-filler-frontend --force 2>/dev/null || true

# 9. Delete CloudWatch Log Groups
echo "Deleting CloudWatch log groups..."
aws logs delete-log-group --log-group-name /ecs/auto-form-filler 2>/dev/null || true
aws logs delete-log-group --log-group-name /ecs/auto-form-filler-frontend 2>/dev/null || true

# 10. Delete Secrets Manager secrets
echo "Deleting secrets..."
aws secretsmanager delete-secret --secret-id auto-form-filler/openrouter-key --force-delete-without-recovery 2>/dev/null || true
aws secretsmanager delete-secret --secret-id auto-form-filler/llama-key --force-delete-without-recovery 2>/dev/null || true

# 11. Delete Key Pairs
echo "Deleting key pairs..."
aws ec2 delete-key-pair --key-name auto-form-filler-key 2>/dev/null || true
rm -f ~/.ssh/auto-form-filler-key.pem 2>/dev/null || true

echo "✅ Cleanup complete! All resources deleted."
echo "💰 Monthly charges should now be $0"