import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from youtube import download_youtube
from facebook import download_facebook
from insta import download_instagram
from tiktok import download_tiktok

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot token
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Quality format mapping
QUALITY_FORMATS = {
    'low': 'worstvideo[filesize<50M]+worstaudio[filesize<50M]/worst[filesize<50M]',
    'medium': 'bestvideo[height<=720][filesize<50M]+bestaudio[filesize<50M]/best[height<=720][filesize<50M]',
    'high': 'bestvideo[height<=1080][filesize<50M]+bestaudio[filesize<50M]/best[height<=1080][filesize<50M]'
}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm a media downloader bot by danukaji-M. Send a TikTok, Instagram, Facebook, or YouTube link to download videos, images, or audio (under 50MB). Use /help for more info."
    )

# Help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📥 *Media Downloader Bot Help*\n\n"
        "This bot downloads media (videos, images, audio) from TikTok, Instagram, Facebook, and YouTube, with a 50MB size limit.\n\n"
        "*Commands:*\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/contact - Contact the developer\n\n"
        "*How to Use:*\n"
        "1. Send a valid URL from supported platforms.\n"
        "2. Choose quality (low, medium, high) from the inline keyboard.\n"
        "3. Receive the downloaded media.\n\n"
        "*Supported Platforms:*\n"
        "- YouTube\n- TikTok\n- Instagram\n- Facebook\n\n"
        "*Note*: Files over 50MB or private content may not download.\n\n"
        "Developed by danukaji-M: https://github.com/danukaji-M"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# Contact command handler
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Contact the developer:\nGitHub: https://github.com/danukaji-M",
        parse_mode="Markdown"
    )

# Inline keyboard for quality selection
def get_quality_keyboard(url):
    keyboard = [
        [
            InlineKeyboardButton("Low Quality", callback_data=f"low|{url}"),
            InlineKeyboardButton("Medium Quality", callback_data=f"medium|{url}"),
            InlineKeyboardButton("High Quality", callback_data=f"high|{url}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Message handler for URLs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    # Validate URL
    if not any(domain in url.lower() for domain in ["tiktok.com", "instagram.com", "facebook.com", "youtube.com", "youtu.be"]):
        await update.message.reply_text("Please send a valid TikTok, Instagram, Facebook, or YouTube URL.")
        return

    # Send quality selection keyboard
    await update.message.reply_text("Please select the download quality:", reply_markup=get_quality_keyboard(url))

# Callback query handler for quality selection
async def handle_quality_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    quality, url = query.data.split('|', 1)
    chat_id = query.message.chat_id

    await query.message.reply_text(f"Processing your request with {quality} quality...")

    # Determine platform and download
    try:
        if "youtube.com" in url.lower() or "youtu.be" in url.lower():
            file_path, file_type, error = download_youtube(url, chat_id, quality)
        elif "tiktok.com" in url.lower():
            file_path, file_type, error = download_tiktok(url, chat_id, quality)
        elif "instagram.com" in url.lower():
            file_path, file_type, error = download_instagram(url, chat_id, quality)
        elif "facebook.com" in url.lower():
            file_path, file_type, error = download_facebook(url, chat_id, quality)
        else:
            file_path, file_type, error = None, None, "Unsupported platform."

        if error:
            await query.message.reply_text(error)
            return

        # Send media based on type
        if file_type == 'image':
            with open(file_path, 'rb') as image:
                await context.bot.send_photo(chat_id=chat_id, photo=image)
            await query.message.reply_text("Image sent successfully!")
        elif file_type == 'video':
            with open(file_path, 'rb') as video:
                await context.bot.send_video(chat_id=chat_id, video=video)
            await query.message.reply_text("Video sent successfully!")
        elif file_type == 'audio':
            with open(file_path, 'rb') as audio:
                await context.bot.send_audio(chat_id=chat_id, audio=audio)
            await query.message.reply_text("Audio sent successfully!")

    except Exception as e:
        await query.message.reply_text(f"Error sending media: {str(e)}")
    finally:
        # Clean up
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("An error occurred. Please try again.")

def main():
    # Validate token
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN not found in .env file.")
        return

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_quality_selection))
    application.add_error_handler(error_handler)  # Correctly register error handler

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()