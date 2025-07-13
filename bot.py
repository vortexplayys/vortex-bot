from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")

user_gems = {}
user_wallets = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Welcome to VORTEX Bot!\nUse /play to start running.\nUse /wallet to link your BNB address.\nUse /convert to turn gems into tokens.")

# /play command
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    outcomes = ["✅ Jumped!", "🔥 Fell in pit!", "🚧 Hit obstacle!", "💎 Collected gem!"]
    result = random.choice(outcomes)

    if result == "💎 Collected gem!":
        user_gems[user_id] = user_gems.get(user_id, 0) + 1

    gems = user_gems.get(user_id, 0)
    await update.message.reply_text(f"{result}\n💎 Your gems: {gems}")

# /wallet command
async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        wallet_address = context.args[0]
        if wallet_address.startswith("0x") and len(wallet_address) == 42:
            user_wallets[user_id] = wallet_address
            await update.message.reply_text(f"✅ Wallet set: {wallet_address}")
        else:
            await update.message.reply_text("❌ Invalid BNB wallet address. Must start with 0x and be 42 characters.")
    else:
        await update.message.reply_text("🔗 Send like this:\n/wallet 0xYourWalletAddressHere")

# /convert command
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    wallet = user_wallets.get(user_id)
    gems = user_gems.get(user_id, 0)

    if not wallet:
        await update.message.reply_text("❌ Wallet not set. Use /wallet to set your BNB address.")
    elif gems == 0:
        await update.message.reply_text("💎 You have no gems to convert.")
    else:
        # Fake conversion rate: 1 gem = 10 VORTEX
        tokens = gems * 10
        user_gems[user_id] = 0  # Reset gems after convert
        await update.message.reply_text(f"🎉 {gems} gems converted into {tokens} VORTEX tokens!\nSent to: {wallet}")

# Deploy bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("wallet", wallet))
    app.add_handler(CommandHandler("convert", convert))
    app.run_polling()
