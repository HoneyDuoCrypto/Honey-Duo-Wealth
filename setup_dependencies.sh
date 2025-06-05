#!/bin/bash

# HONEY DUO WEALTH - Complete Dependencies Setup
# Run this script to install all required packages

echo "🏠 HONEY DUO WEALTH - Setting up dependencies..."
echo "============================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update

# Python dependencies with virtual environment
echo "🐍 Setting up Python environment..."
sudo apt install -y python3-full python3-venv python3-pip

# Create virtual environment
echo "🔧 Creating virtual environment..."
cd ~/honey_duo_wealth
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python packages
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install ollama
pip install requests
pip install pandas
pip install numpy
pip install fastapi
pip install uvicorn
pip install redis
pip install psycopg2-binary
pip install python-dotenv
pip install ccxt  # For crypto trading
pip install yfinance  # For stock data
pip install ta  # Technical analysis
pip install schedule  # Task scheduling
pip install plotly  # For charts
pip install streamlit  # For dashboard

# System dependencies
echo "🔧 Installing system dependencies..."
sudo apt install -y git
sudo apt install -y docker.io docker-compose
sudo apt install -y redis-server
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y nginx
sudo apt install -y certbot python3-certbot-nginx
sudo apt install -y htop  # System monitoring
sudo apt install -y tmux  # Terminal multiplexer

# Docker setup
echo "🐳 Setting up Docker..."
sudo usermod -aG docker $USER

# Create activation helper
echo "📝 Creating activation script..."
cat > ~/honey_duo_wealth/activate.sh << 'EOF'
#!/bin/bash
# Quick activation script
cd ~/honey_duo_wealth
source venv/bin/activate
echo "✅ HONEY DUO WEALTH environment activated"
echo "Run: python3 ai_family/ai_orchestrator.py"
EOF

chmod +x ~/honey_duo_wealth/activate.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source ~/honey_duo_wealth/activate.sh"
echo ""
echo "Then test with:"
echo "  python3 ai_family/ai_orchestrator.py"