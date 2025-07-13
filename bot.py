from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Gems store karne ke liye
user_gems = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 VORTEX Bot Online! Type /play to start the game.")

# Play command
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    outcomes = ["✅ Jumped!", "🔥 Fell in pit!", "🚧 Hit obstacle!", "💎 Collected gem!"]
    result = random.choice(outcomes)

    if result == "💎 Collected gem!":
        user_gems[user_id] = user_gems.get(user_id, 0) + 1

    gems = user_gems.get(user_id, 0)
    await update.message.reply_text(f"{result}\n💎 Your gems: {gems}")

# Run the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.run_polling()
