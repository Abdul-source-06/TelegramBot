from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final  = '7623386182:AAH56qJBppCJvGK2NwHljE6txqgqF-WEboM'

BOT_USERNAME: Final = '@Fitbotbot'

# Comanda start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Benvingut a FitBot! Comencem amb el teu entrenament.')

# Comanda /objectiu
async def objectiu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Quin és el teu objectiu d'entrenament? (Perdre pes, Guanyar múscul, Guanyar resistència, Guanyar força)"
    )

# Gestió de respostes d'objectius
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "perdre pes" in text:
        resposta = (
            "Per perdre pes, t'aconsello mantenir una dieta hipocalòrica amb aliments saludables, fer exercici cardiovascular "
            "com córrer, caminar ràpid o anar amb bicicleta 3-5 vegades a la setmana, i afegir entrenament de força per mantenir la massa muscular."
        )
    elif "guanyar múscul" in text:
        resposta = (
            "Per guanyar múscul, necessites entrenar amb pesos moderats a pesats, amb repeticions de 6-12 per sèrie. "
            "Assegura't de consumir prou proteïnes (al voltant de 2 g per kg de pes corporal) i descansar bé."
        )
    elif "guanyar resistència" in text:
        resposta = (
            "Per guanyar resistència, practica exercicis cardiovasculars com córrer, nedar o anar amb bicicleta. "
            "També pots incorporar entrenaments HIIT per augmentar la resistència cardiovascular i muscular."
        )
    elif "guanyar força" in text:
        resposta = (
            "Per guanyar força, entrena amb pesos pesats i repeticions baixes (3-6 per sèrie). "
            "Focalitza't en moviments compostos com el 'deadlift', la 'squat', el 'bench press' i descansa adequadament entre sèries."
        )
    else:
        resposta = (
            "No he entès el teu objectiu. Si us plau, especifica si vols 'Perdre pes', 'Guanyar múscul', 'Guanyar resistència' o 'Guanyar força'."
        )

    await update.message.reply_text(resposta)

def main():
    # Crear l'aplicació
    app = Application.builder().token(TOKEN).build()

    # Afegir gestors de comandes
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("objectiu", objectiu_command))

    # Afegir un gestor per a les respostes de text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Començar el bot
    app.run_polling()

if __name__ == "__main__":
    main()
