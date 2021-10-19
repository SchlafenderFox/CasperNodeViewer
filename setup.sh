#!/bin/bash

# Installing docker-compose

sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
echo -ne '\n' | sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(. /etc/os-release; echo "$UBUNTU_CODENAME") stable"
sudo apt update
sudo apt install -y docker-ce docker-compose
usermod -aG docker $USER

echo "Enter master server ip ( EXAMPLE: 127.0.0.1 )"
read MASTER_SERVER_IP

if [ -z "$MASTER_SERVER_IP" ]
then
  MASTER_SERVER_IP="127.0.0.1"
fi

echo "[INFO] MASTER_SERVER_IP set $MASTER_SERVER_IP"

echo "MASTER_SERVER_IP=$MASTER_SERVER_IP" >> settings.env

echo "[INFO] Starting node explorer..."
docker-compose up -d --build
echo "[INFO] Node explorer is up!"

IP=$(curl ifconfig.co)
echo "[INFO] Firewall reloaded seccessful! Checking info on http://$IP:10100/metrics"
echo "[INFO] You can change any settings in settings.env file."
echo "[INFO] For apply your changes execute docker-compose up -d --build"
