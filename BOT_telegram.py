from typing import final
from telegram import Update
from telegram.exe import Application, CommandHandler, filters, ContextTypes

TOKEN: Final  = '7623386182:AAH56qJBppCJvGK2NwHljE6txqgqF-WEboM'

BOT_USERNAME: Final = '@Fitbotbot'

async def start_command(update: Update, context: ContextTypes.DEAFAULT_TYPE):
    await update.message.reply_text('Hola! Gràcies por chatear conmigo ')