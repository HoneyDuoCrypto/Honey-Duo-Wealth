#!/bin/bash
echo "=== HONEY DUO WEALTH Setup ==="

# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y curl wget git python3-pip python3-venv build-essential

# Install Docker
sudo apt install -y docker.io
sudo usermod -aG docker $USER

# Install Ollama for LLMs
curl -fsSL https://ollama.com/install.sh | sh

echo "Setup complete! Log out and back in for Docker permissions."

