# ==========================================================
# 🌟 AstroPulse Support Bot
# Clean • Structured • Hosting Ready
# ==========================================================

import logging
import threading
import os
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================== CONFIG ==================

BOT_TOKEN = "8621124805:AAE7HXhOXg7NQqxSXkWx3__eRLZmv1KuLtY"
OWNER_ID = 6808803040

# ================== LOGGING ==================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

# ================== FLASK WEB SERVER ==================

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "✨ AstroPulse Bot is Running Successfully! ✨"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

# ================== FAQ DATA ==================

FAQ_DATA = {
    "prices": """💰 *AstroPulse Pricing*
━━━━━━━━━━━━━━━━━━

❤️ 1K Likes – ₹15
👁️ 1K Views – ₹5
💬 1K Comments – ₹15
👤 1K Followers – ₹40
🔁 1K Shares – ₹5

✨ High quality & fast delivery
""",

    "payment": """💳 *Payment Method*
━━━━━━━━━━━━━━━━━━

✅ UPI Accepted

📸 After payment send screenshot:
/owner I have paid for my order
""",

    "delivery": """🚀 *Delivery Info*
━━━━━━━━━━━━━━━━━━

⏳ Starts within minutes
⚡ Completed within 24 hours
""",

    "refund": """🔁 *Refund Policy*
━━━━━━━━━━━━━━━━━━

Refund only if service is not delivered.
""",

    "services": """📌 *Our Services*
━━━━━━━━━━━━━━━━━━

📷 Instagram
• Likes • Followers • Views • Comments • Shares

✈️ Telegram
• Channel Members • Group Members • Post Views

📘 Facebook
• Page Likes • Post Likes • Followers • Shares

🐦 Twitter
• Followers • Likes • Retweets
"""
}

# ================== KEYBOARD ==================

KEYBOARD = ReplyKeyboardMarkup(
    [
        ["💰 Prices", "💳 Payment"],
        ["🚀 Delivery", "🔁 Refund"],
        ["📌 Services"],
        ["📨 Contact Owner"]
    ],
    resize_keyboard=True
)

# ================== HANDLERS ==================

# 🔹 Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """✨ *Welcome to AstroPulse Support* ✨
━━━━━━━━━━━━━━━━━━

🚀 Your Trusted SMM Panel

Use the menu below to explore services or contact support.
"""
    await update.message.reply_text(
        welcome_message,
        parse_mode="Markdown",
        reply_markup=KEYBOARD
    )

# 🔹 Contact Owner Guide
async def contact_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✍️ Send your message like this:\n\n"
        "/owner Your message here"
    )

# 🔹 User → Owner
async def owner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage:\n/owner Your message")
        return

    user = update.effective_user
    message = " ".join(context.args)
    username = f"@{user.username}" if user.username else "Not available"

    owner_message = f"""📩 *New Support Request*
━━━━━━━━━━━━━━━━━━

👤 Name: {user.full_name}
🔗 Username: {username}
🆔 User ID: {user.id}

💬 Message:
{message}
"""

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=owner_message,
        parse_mode="Markdown"
    )

    await update.message.reply_text("✅ Your message has been sent to support.")

# 🔹 Owner Reply via /reply
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage:\n/reply USER_ID your message")
        return

    try:
        user_id = int(context.args[0])
        message = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=user_id,
            text=f"💼 *AstroPulse Support*\n━━━━━━━━━━━━━━━━━━\n\n{message}",
            parse_mode="Markdown"
        )

        await update.message.reply_text("✅ Reply sent successfully.")

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("❌ Failed to send message.")

# 🔹 FAQ Handler
async def faq_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "price" in text:
        await update.message.reply_text(FAQ_DATA["prices"], parse_mode="Markdown")

    elif "payment" in text:
        await update.message.reply_text(FAQ_DATA["payment"], parse_mode="Markdown")

    elif "delivery" in text:
        await update.message.reply_text(FAQ_DATA["delivery"], parse_mode="Markdown")

    elif "refund" in text:
        await update.message.reply_text(FAQ_DATA["refund"], parse_mode="Markdown")

    elif "service" in text:
        await update.message.reply_text(FAQ_DATA["services"], parse_mode="Markdown")

    elif "contact" in text:
        await contact_owner(update, context)

    else:
        await update.message.reply_text(
            "❓ Please use the menu below.",
            reply_markup=KEYBOARD
        )

# ================== MAIN ==================

def main():
    # Run web server in background (important for free hosting)
    threading.Thread(target=run_web, daemon=True).start()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("owner", owner_command))
    application.add_handler(CommandHandler("reply", reply_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, faq_handler))

    print("🚀 AstroPulse Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
