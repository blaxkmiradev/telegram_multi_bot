import os
import telebot
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the bot using the token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found. Please check your .env file.")

bot = telebot.TeleBot(BOT_TOKEN)

# ==========================================
# 🚀 COMMAND HANDLERS
# ==========================================

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handles the /start and /help commands."""
    welcome_text = (
        "🤖 *Welcome to the Multi-Tool Bot!*\n\n"
        "Here is what I can do:\n"
        "✨ *Premium Emojis:* Send any custom emoji to get its ID.\n"
        "🖼️ *Stickers:* Send a sticker to get its File ID.\n"
        "📸 *Photos/GIFs:* Send a photo or GIF to get its File ID.\n"
        "🆔 */info:* Get your personal User ID and Chat ID.\n"
        "🏓 */ping:* Check if I am online."
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['info'])
def send_info(message):
    """Sends the user their User ID and the current Chat ID."""
    info_text = (
        f"👤 *Your User ID:* `{message.from_user.id}`\n"
        f"💬 *Current Chat ID:* `{message.chat.id}`"
    )
    bot.reply_to(message, info_text, parse_mode="Markdown")

@bot.message_handler(commands=['ping'])
def send_ping(message):
    """Simple ping command to check bot latency."""
    bot.reply_to(message, "🏓 *Pong!* I am online and working perfectly.", parse_mode="Markdown")


# ==========================================
# ✉️ CONTENT HANDLERS
# ==========================================

@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    """Extracts Premium Custom Emoji IDs from text messages."""
    if message.entities:
        custom_emoji_ids = []
        
        # Search for custom emojis in the message formatting entities
        for entity in message.entities:
            if entity.type == 'custom_emoji':
                custom_emoji_ids.append(entity.custom_emoji_id)
        
        # If custom emojis are found, return their IDs
        if custom_emoji_ids:
            reply_text = "✨ *Custom Emoji IDs detected:*\n\n`" + "`\n`".join(custom_emoji_ids) + "`"
            bot.reply_to(message, reply_text, parse_mode="Markdown")
            return

    # Fallback if it's just normal text
    bot.reply_to(message, "Send me a **Premium Custom Emoji**, or use /help to see what else I can do!", parse_mode="Markdown")

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    """Returns the File ID of any sticker sent to the bot."""
    bot.reply_to(message, f"🖼️ *Sticker File ID:*\n`{message.sticker.file_id}`", parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Returns the File ID of the highest quality version of a photo."""
    # Telegram sends multiple sizes of a photo; [-1] is the highest resolution
    photo_id = message.photo[-1].file_id
    bot.reply_to(message, f"📸 *Photo File ID:*\n`{photo_id}`", parse_mode="Markdown")

@bot.message_handler(content_types=['animation'])
def handle_animation(message):
    """Returns the File ID of a GIF/Animation."""
    bot.reply_to(message, f"🎞️ *GIF/Animation File ID:*\n`{message.animation.file_id}`", parse_mode="Markdown")


# ==========================================
# 🔄 BOT EXECUTION
# ==========================================

if __name__ == "__main__":
    print("🤖 Bot is starting up...")
    print("✅ Listening for messages...")
    # infinity_polling keeps the bot running even if there are temporary network errors
    bot.infinity_polling()
