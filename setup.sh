#!/bin/bash

# Automated setup script for Telegram media downloader bot
# Installs dependencies, prompts for API key, sets up .env, and provides run instructions

# Exit on any error
set -e

# Define project directory (current directory by default)
PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo "Starting setup for Telegram media downloader bot..."

# 1. Install system packages (ffmpeg, python3, venv)
echo "Installing system packages..."
sudo apt update
sudo apt install -y ffmpeg python3 python3-venv python3-pip

# 2. Create and activate virtual environment
echo "Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# 3. Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install python-telegram-bot yt-dlp python-dotenv

# 4. Prompt for Telegram bot API key
echo "Please enter your Telegram bot API key (token from BotFather):"
read -r BOT_TOKEN
if [ -z "$BOT_TOKEN" ]; then
    echo "Error: No API key provided. Exiting..."
    exit 1
fi

# 5. Rename sample.env to .env and set bot token
echo "Configuring .env file..."
if [ -f "sample.env" ]; then
    mv sample.env .env
    echo "TELEGRAM_TOKEN=$BOT_TOKEN" > .env
    echo ".env file created with bot token."
else
    echo "Warning: sample.env not found. Creating .env with bot token..."
    echo "TELEGRAM_TOKEN=$BOT_TOKEN" > .env
fi

# 6. Deactivate virtual environment
deactivate

# 7. Provide instructions to run the bot
echo ""
echo "Setup complete! To run the bot, follow these steps:"
echo "1. Activate the virtual environment:"
echo "   source $VENV_DIR/bin/activate"
echo "2. Run the bot:"
echo "   python main.py"
echo ""
echo "To stop the bot, press Ctrl+C."
echo "If you encounter issues, check logs in main.py output or ensure FFmpeg is installed (ffmpeg -version)."

exit 0