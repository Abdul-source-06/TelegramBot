from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes




# Nou token i nom del bot
TOKEN: Final = '7623386182:AAH56qJBppCJvGK2NwHljE6txqgqF-WEboM'
BOT_USERNAME: Final = '@Fitbotbot'

# Comanda /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Missatge de benvinguda
    await update.message.reply_text(
        'Benvingut a FitBot! Comencem amb el teu entrenament. Abans de començar selecciona l\'idioma que vols:'
    )

    # Definim els botons inline d'idioma
    keyboard = [
        [InlineKeyboardButton("English", callback_data='english'), InlineKeyboardButton("Español", callback_data='spanish')]
    ]
    
    # Creem el markup per als botons inline
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Enviem el markup dels botons
    await update.message.reply_text(
        'Selecciona l\'idioma:',
        reply_markup=reply_markup
    )


# Funció per gestionar la selecció d'idioma
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Responem a la consulta del botó

    if query.data == 'english':
        await query.edit_message_text(text="You have selected English.")
        # Un cop seleccionat l'idioma, cridem al menú principal
        await main_menu(query.message, context)
    elif query.data == 'spanish':
        await query.edit_message_text(text="Has seleccionado Español.")
        # Un cop seleccionat l'idioma, cridem al menú principal
        await main_menu(query.message, context)

# Funció per mostrar el menú principal
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Definim els botons del menú principal
    keyboard = [
        [InlineKeyboardButton("🔄 Canviar llenguatge", callback_data='change_language'), 
         InlineKeyboardButton("🆕 Nova rutina", callback_data='new_routine')],
        [InlineKeyboardButton("📋 Les meves rutines", callback_data='my_routines')]
    ]
    
    # Creem el markup per als botons
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Missatge del menú principal amb els botons
    await update.reply_text(
        'Menú principal:\n\n- 🔄 Canviar llenguatge\n- 🆕 Nova rutina\n- 📋 Les meves rutines',
        reply_markup=reply_markup
    )

# Comanda /objectiu
async def objectiu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Quin és el teu objectiu d'entrenament? (Perdre pes, Guanyar múscul, Guanyar resistència, Guanyar força)"
    )

# Comanda /ajuda
async def ajuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aquí tens una llista de les comandes disponibles: /start, /objectiu, /alarma, /rutina, /progress, /equip, /ajuda.")


# Funció per gestionar els missatges de text
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f'Has enviat: {text}')

def main():
    # Crear l'aplicació
    app = Application.builder().token(TOKEN).build()

    # Afegir gestors de comandes
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("objectiu", objectiu_command))
    app.add_handler(CommandHandler("ajuda", ajuda_command))

    # Afegir un gestor per gestionar la selecció d'idioma
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.TEXT, button_callback))

    # Començar el bot
    app.run_polling()

if __name__ == "__main__":
    main()
