# Telegram Media Downloader Bot

A Telegram bot that downloads videos, images, and audio (up to 50MB) from YouTube, TikTok, Instagram, and Facebook. Users can select download quality (low, medium, high) via an inline keyboard. The bot uses polling to receive updates and is built with Python, `python-telegram-bot`, and `yt-dlp`.

Developed by [danukaji-M](https://github.com/danukaji-M).

## Features
- **Supported Platforms**: YouTube, TikTok, Instagram, Facebook
- **Media Types**: Videos (up to 1080p), images, audio (192kbps MP3)
- **File Size Limit**: 50MB
- **Quality Selection**: Low, medium, high via inline keyboard
- **Commands**:
  - `/start`: Welcome message
  - `/help`: Usage instructions
  - `/contact`: Developer’s GitHub
- **Modular Design**: Separate modules for each platform
- **Automated Setup**: `setup.sh` script installs dependencies and configures the bot

## Project Structure
```
media_downloader_bot/
├── main.py              # Main bot logic
├── youtube.py           # YouTube download module
├── facebook.py          # Facebook download module
├── insta.py             # Instagram download module
├── tiktok.py            # TikTok download module
├── sample.env           # Environment file template
├── setup.sh             # Automated setup script
├── README.md            # This file
└── .env                 # Created by setup.sh (contains bot token)
```

## Prerequisites
- **System**: Debian/Ubuntu-based Linux (for `apt` package manager)
- **Dependencies**:
  - `ffmpeg` (for audio/video processing)
  - Python 3.7+
  - Git
- **Telegram Bot Token**: Obtain from [BotFather](https://t.me/BotFather)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url> media_downloader_bot
   cd media_downloader_bot
   ```

2. **Run the Setup Script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   - The script will:
     - Install system packages (`ffmpeg`, `python3`, etc.)
     - Create a virtual environment (`venv`)
     - Install Python packages (`python-telegram-bot`, `yt-dlp`, `python-dotenv`)
     - Prompt for your Telegram bot API key
     - Rename `sample.env` to `.env` and set the token
   - Enter your bot token when prompted (e.g., `7532665180:AAEMeqBy5QlJGSdKTJ0I0V43L5TagirUz2o`).

3. **Run the Bot**:
   ```bash
   source venv/bin/activate
   python main.py
   ```
   - The bot starts polling and responds to Telegram messages.
   - Press `Ctrl+C` to stop.

## Usage
1. **Start the Bot**:
   - Send `/start` to receive a welcome message.
2. **View Help**:
   - Send `/help` for instructions and supported platforms.
3. **Contact Developer**:
   - Send `/contact` to get the developer’s GitHub ([danukaji-M](https://github.com/danukaji-M)).
4. **Download Media**:
   - Send a URL from YouTube, TikTok, Instagram, or Facebook.
   - Select quality (low, medium, high) from the inline keyboard.
   - Receive media (image, video, or audio, under 50MB).

## Troubleshooting
- **FFmpeg Not Installed**:
  - If `ffmpeg -version` prompts for package selection (e.g., `ffmpeg_7-full.bin`), choose `ffmpeg_7-full.bin` for full codec support.
  - Manually install:
    ```bash
    sudo apt install ffmpeg
    ```
- **Bot Fails to Start**:
  - Check `.env` for correct `TELEGRAM_TOKEN`:
    ```bash
    cat .env
    ```
  - Verify Python packages:
    ```bash
    source venv/bin/activate
    pip list
    ```
  - Share error output from `python main.py`.
- **Download Errors**:
  - Private or restricted content may fail (e.g., Instagram private posts).
  - Ensure URLs are valid and media is under 50MB.
- **Permission Issues**:
  - Run `sudo apt` commands if you have admin privileges.
  - Contact your server admin if you lack `sudo` access.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact
For issues or suggestions, contact the developer:
- GitHub: [danukaji-M](https://github.com/danukaji-M)