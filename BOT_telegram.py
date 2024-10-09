from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Configura la clau d'API d'OpenAI


TOKEN: Final = '7623386182:AAH56qJBppCJvGK2NwHljE6txqgqF-WEboM'
BOT_USERNAME: Final = '@Fitbotbot'

# Comanda start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Benvingut a FitBot! Comencem amb el teu entrenament.Posa la comanda /objectiu per seleccionar el objetiu que vols')

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

# Comanda /equip
async def equip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tens accés a equip de gimnàs? (Sí/No)")

# Comanda /alarma
async def alarma_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A quina hora vols configurar l'alarma? (Format HH:MM)")

# Comanda /rutina
async def rutina_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aquesta és la teva rutina d'exercicis personalitzada per avui.")

# Comanda /progress
async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Has completat X sessions aquesta setmana. Segueix així!")

# Comanda /ajuda
async def ajuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aquí tens una llista de les comandes disponibles: /start, /objectiu, /alarma, /rutina, /progress, /equip, /ajuda.")

# Funció per obtenir una resposta resumida de l'objectiu a través de l'API de ChatGPT
def obtenir_resposta_resumida(objectiu_usuari):
    prompt = f"L'usuari vol aconseguir l'objectiu: {objectiu_usuari}. Respon de forma resumida amb consells o passos a seguir."

    resposta = openai.Completion.create(
        engine="text-davinci-004",
        prompt=prompt,
        max_tokens=50,
        temperature=0.7
    )

    return resposta.choices[0].text.strip()

def main():
    # Crear l'aplicació
    app = Application.builder().token(TOKEN).build()

    # Afegir gestors de comandes
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("objectiu", objectiu_command))
    app.add_handler(CommandHandler("equip", equip_command))
    app.add_handler(CommandHandler("alarma", alarma_command))
    app.add_handler(CommandHandler("rutina", rutina_command))
    app.add_handler(CommandHandler("progress", progress_command))
    app.add_handler(CommandHandler("ajuda", ajuda_command))

    # Afegir un gestor per a les respostes de text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Començar el bot
    app.run_polling()

if __name__ == "__main__":
    main()
