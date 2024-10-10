from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Configura la clau d'API d'OpenAI
openai.api_key = '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'

TOKEN: Final = '7623386182:AAH56qJBppCJvGK2NwHljE6txqgqF-WEboM'
BOT_USERNAME: Final = '@Fitbotbot'

# Funció per obtenir una resposta de la IA basada en els objectius triats
async def obtenir_resposta_ia(objectius_usuari):
    prompt = f"L'usuari vol aconseguir els objectius: {objectius_usuari}. Respon amb consells o passos a seguir per aconseguir-los combinats."
    
    resposta = openai.Completion.create(
        engine="text-davinci-004",  # O usa "gpt-3.5-turbo" si vols utilitzar un altre model
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    
    return resposta.choices[0].text.strip()

# Comanda start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Benvingut a FitBot! Posa la comanda /objectiu per començar a definir el teu entrenament.')

# Comanda /objectiu
async def objectiu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Selecciona un o més objectius d'entrenament escrivint els noms (separats per comes) o tria combinacions:\n\n"
        "1. **Perdre pes**: Centrat en la pèrdua de greix corporal.\n"
        "2. **Guanyar múscul**: Augmentar la massa muscular mitjançant exercicis de força.\n"
        "3. **Guanyar resistència**: Millorar la teva capacitat cardiovascular i durada física.\n"
        "4. **Guanyar força**: Augmentar la teva força muscular mitjançant exercicis amb peses.\n\n"
        "Exemple: Pots combinar 'Perdre pes' i 'Guanyar múscul'."
    )
    await update.message.reply_text(text)

# Gestió de respostes amb combinacions d'objectius
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # Processar les combinacions d'objectius triats
    objectius_valids = ["perdre pes", "guanyar múscul", "guanyar resistència", "guanyar força"]
    objectius_triats = [obj.strip() for obj in text.split(',') if obj.strip() in objectius_valids]

    if objectius_triats:
        objectius_str = ", ".join(objectius_triats)
        resposta_ia = await obtenir_resposta_ia(objectius_str)
    else:
        resposta_ia = "No he entès els teus objectius. Si us plau, selecciona un o més d'aquests: 'Perdre pes', 'Guanyar múscul', 'Guanyar resistència', 'Guanyar força'."

    await update.message.reply_text(resposta_ia)

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

# Funció principal
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
