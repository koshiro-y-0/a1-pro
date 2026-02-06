#!/bin/bash

# EC2 Setup Script for A1-PRO
# Run this script on a fresh EC2 instance (Amazon Linux 2023 or Ubuntu)

set -e

echo "========================================="
echo "A1-PRO EC2 Setup Script"
echo "========================================="

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS. Exiting."
    exit 1
fi

echo "Detected OS: $OS"

# Update system packages
echo "Updating system packages..."
if [ "$OS" = "amzn" ] || [ "$OS" = "amazon" ]; then
    sudo yum update -y
elif [ "$OS" = "ubuntu" ]; then
    sudo apt-get update
    sudo apt-get upgrade -y
fi

# Install Docker
echo "Installing Docker..."
if [ "$OS" = "amzn" ] || [ "$OS" = "amazon" ]; then
    sudo yum install -y docker
    sudo systemctl start docker
    sudo systemctl enable docker
elif [ "$OS" = "ubuntu" ]; then
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
echo "Installing Git..."
if [ "$OS" = "amzn" ] || [ "$OS" = "amazon" ]; then
    sudo yum install -y git
elif [ "$OS" = "ubuntu" ]; then
    sudo apt-get install -y git
fi

# Clone repository
echo "Cloning A1-PRO repository..."
cd ~
if [ ! -d "a1-pro" ]; then
    git clone https://github.com/koshiro-y-0/a1-pro.git
    cd a1-pro
else
    cd a1-pro
    git pull origin main
fi

# Create .env file
echo "Creating .env file..."
cat > .env << EOF
# Database Configuration
MYSQL_ROOT_PASSWORD=your_root_password_here
MYSQL_PASSWORD=your_password_here

# API Keys
BUFFETT_CODE_API_KEY=your_buffett_code_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key

# Ollama Configuration
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1:8b

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost/api
EOF

echo ""
echo "========================================="
echo "IMPORTANT: Edit the .env file with your actual credentials:"
echo "  nano ~/.a1-pro/.env"
echo "========================================="
echo ""

# Install Ollama (optional - for RAG chatbot)
read -p "Do you want to install Ollama for the RAG chatbot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh

    echo "Pulling Llama 3.1 8B model..."
    ollama pull llama3.1:8b
fi

# Build and start Docker containers
echo "Building Docker containers..."
docker-compose build

echo "Starting Docker containers..."
docker-compose up -d

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
sleep 10

# Run database migrations
echo "Running database migrations..."
docker-compose exec -T backend alembic upgrade head

# Show status
echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Running containers:"
docker-compose ps
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop containers:"
echo "  docker-compose down"
echo ""
echo "Access your application at:"
echo "  http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo ""
echo "========================================="
echo "Next Steps:"
echo "1. Edit .env file with your credentials"
echo "2. Set up GitHub Actions secrets for CI/CD"
echo "3. Configure security groups (ports 22, 80, 443)"
echo "4. (Optional) Set up SSL with Let's Encrypt"
echo "========================================="
