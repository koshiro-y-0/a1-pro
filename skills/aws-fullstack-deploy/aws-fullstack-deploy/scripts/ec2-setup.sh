#!/bin/bash
# EC2 Initial Setup Script for Docker-based deployment
# Supports: Amazon Linux 2023 / Ubuntu 22.04+

set -e

echo "=== EC2 Initial Setup ==="

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS"
    exit 1
fi

echo "Detected OS: $OS"

# Update system
echo "Updating system packages..."
if [ "$OS" = "amzn" ]; then
    sudo yum update -y
elif [ "$OS" = "ubuntu" ]; then
    sudo apt-get update && sudo apt-get upgrade -y
fi

# Install Docker
echo "Installing Docker..."
if [ "$OS" = "amzn" ]; then
    sudo yum install -y docker
    sudo systemctl start docker
    sudo systemctl enable docker
elif [ "$OS" = "ubuntu" ]; then
    sudo apt-get install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose (standalone for Amazon Linux)
if [ "$OS" = "amzn" ]; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Install Git
echo "Installing Git..."
if [ "$OS" = "amzn" ]; then
    sudo yum install -y git
elif [ "$OS" = "ubuntu" ]; then
    sudo apt-get install -y git
fi

# Create app directory
echo "Creating app directory..."
sudo mkdir -p /var/www/app
sudo chown $USER:$USER /var/www/app

# Security: Disable SSH password authentication
echo "Hardening SSH configuration..."
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Install certbot for SSL (optional, run ssl-setup.sh later)
echo "Installing Certbot..."
if [ "$OS" = "amzn" ]; then
    sudo yum install -y certbot
elif [ "$OS" = "ubuntu" ]; then
    sudo apt-get install -y certbot
fi

echo ""
echo "=== Setup Complete ==="
echo "IMPORTANT: Log out and log back in for docker group to take effect"
echo ""
echo "Next steps:"
echo "1. Clone your repository: git clone YOUR_REPO /var/www/app"
echo "2. Navigate to app: cd /var/www/app"
echo "3. Start services: docker-compose up -d"
echo "4. (Optional) Setup SSL: ./ssl-setup.sh your-domain.com"
