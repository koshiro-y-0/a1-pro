#!/bin/bash
# SSL Setup Script using Let's Encrypt
# Usage: sudo ./ssl-setup.sh your-domain.com

set -e

if [ -z "$1" ]; then
    echo "Usage: sudo $0 your-domain.com"
    exit 1
fi

DOMAIN=$1

echo "=== SSL Setup for $DOMAIN ==="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo)"
    exit 1
fi

# Stop nginx container temporarily if running
echo "Stopping nginx if running..."
docker stop nginx 2>/dev/null || true

# Obtain certificate
echo "Obtaining SSL certificate..."
certbot certonly --standalone -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# Create SSL directory for nginx
mkdir -p /var/www/app/nginx/ssl

# Copy certificates
cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem /var/www/app/nginx/ssl/
cp /etc/letsencrypt/live/$DOMAIN/privkey.pem /var/www/app/nginx/ssl/

# Set permissions
chmod 644 /var/www/app/nginx/ssl/fullchain.pem
chmod 600 /var/www/app/nginx/ssl/privkey.pem

# Setup auto-renewal cron job
echo "Setting up auto-renewal..."
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet --post-hook 'docker restart nginx'") | crontab -

echo ""
echo "=== SSL Setup Complete ==="
echo ""
echo "Certificates installed to: /var/www/app/nginx/ssl/"
echo "Auto-renewal configured (runs daily at 3am)"
echo ""
echo "Update your nginx.conf to use SSL, then restart:"
echo "  docker-compose restart nginx"
