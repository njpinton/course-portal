#!/bin/bash
# Deployment script for Presenter App to RackNerd VPS

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
VPS_IP="148.135.17.59"
VPS_USER="root"
APP_DIR="/root/presenter_app"
VENV_DIR="$APP_DIR/.venv"

echo -e "${GREEN}=== Presenter App Deployment ===${NC}\n"

# Step 1: Build/prepare locally (if needed)
echo -e "${YELLOW}[1/7] Preparing local files...${NC}"
# Add any build steps here if needed
echo "✓ Local preparation complete"

# Step 2: Sync code to VPS
echo -e "\n${YELLOW}[2/7] Syncing code to VPS...${NC}"
rsync -avz --exclude='.git' \
           --exclude='__pycache__' \
           --exclude='*.pyc' \
           --exclude='.env.local' \
           --exclude='.coverage' \
           --exclude='node_modules' \
           --exclude='.vercel' \
           --exclude='tests' \
           ./ $VPS_USER@$VPS_IP:$APP_DIR/

echo "✓ Code synced successfully"

# Step 3: Install dependencies on VPS
echo -e "\n${YELLOW}[3/7] Installing dependencies on VPS...${NC}"
ssh $VPS_USER@$VPS_IP << 'ENDSSH'
cd /root/presenter_app

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate and install dependencies
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
ENDSSH

echo "✓ Dependencies installed"

# Step 4: Create log directory
echo -e "\n${YELLOW}[4/7] Setting up logging...${NC}"
ssh $VPS_USER@$VPS_IP "mkdir -p /var/log/presenter_app /var/log/caddy"
echo "✓ Log directories created"

# Step 5: Setup systemd service
echo -e "\n${YELLOW}[5/7] Configuring systemd service...${NC}"
ssh $VPS_USER@$VPS_IP << 'ENDSSH'
# Copy service file
cp /root/presenter_app/deploy/presenter_app.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable service to start on boot
systemctl enable presenter_app.service
ENDSSH

echo "✓ Systemd service configured"

# Step 6: Restart application
echo -e "\n${YELLOW}[6/7] Restarting application...${NC}"
ssh $VPS_USER@$VPS_IP "systemctl restart presenter_app.service"
sleep 3

# Check service status
if ssh $VPS_USER@$VPS_IP "systemctl is-active --quiet presenter_app.service"; then
    echo -e "✓ Application started successfully"
else
    echo -e "${RED}✗ Application failed to start${NC}"
    echo "Check logs with: ssh $VPS_USER@$VPS_IP 'journalctl -u presenter_app.service -n 50'"
    exit 1
fi

# Step 7: Verify deployment
echo -e "\n${YELLOW}[7/7] Verifying deployment...${NC}"
sleep 2

if curl -s -o /dev/null -w "%{http_code}" http://$VPS_IP:5001 | grep -q "200\|302"; then
    echo -e "✓ Application is responding"
else
    echo -e "${YELLOW}⚠ Application may not be fully ready yet${NC}"
fi

echo -e "\n${GREEN}=== Deployment Complete! ===${NC}"
echo -e "\nApplication URLs:"
echo -e "  • Direct: http://$VPS_IP:5001"
echo -e "  • Via Caddy: http://$VPS_IP (configure Caddy first)"
echo -e "\nUseful commands:"
echo -e "  • View logs: ssh $VPS_USER@$VPS_IP 'journalctl -u presenter_app.service -f'"
echo -e "  • Restart: ssh $VPS_USER@$VPS_IP 'systemctl restart presenter_app.service'"
echo -e "  • Status: ssh $VPS_USER@$VPS_IP 'systemctl status presenter_app.service'"
