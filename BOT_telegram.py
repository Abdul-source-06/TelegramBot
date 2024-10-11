from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from componentes import botBD

# Nou token i nom del bot
TOKEN: Final = '7623386182:AAH56qJBppCJvGK2NwHljE6txqgqF-WEboM'
BOT_USERNAME: Final = '@Fitbotbot'

# Etapes per a la conversa
NAME, AGE, WEIGHT, LANGUAGE, ROUTINE_TYPE, ROUTINE_NAME, GYM_ACCESS, COMPLETION_TIME = range(8)

# Comanda /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = botBD.get_user(user_id)

    if user:
        await update.message.reply_text(f"¡Bienvenido de nuevo, {user[1]}!")
        await main_menu(update.message, context)
    else:
        await update.message.reply_text('¡Bienvenido a FitBot! Comencemos con tu entrenamiento. Primero, selecciona tu idioma.')

        # Crear botones para selección de idioma
        keyboard = [
            [InlineKeyboardButton("English", callback_data='en'), InlineKeyboardButton("Español", callback_data='es')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Selecciona el idioma:', reply_markup=reply_markup)
        return LANGUAGE

# Función para manejar la selección de idioma
async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    language = query.data
    context.user_data['language'] = language

    if language == 'en':
        await query.edit_message_text(text="You have selected English. What's your name?")
    else:
        await query.edit_message_text(text="Has seleccionado Español. ¿Cuál es tu nombre?")

    return NAME

# Función para procesar el nombre
async def process_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("¿Cuántos años tienes?")
    return AGE

# Función para procesar la edad
async def process_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['age'] = int(update.message.text)
    await update.message.reply_text("¿Cuál es tu peso (en kg)?")
    return WEIGHT

# Función para procesar el peso y guardar el usuario
async def process_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = context.user_data['name']
    age = context.user_data['age']
    weight = int(update.message.text)
    language = context.user_data['language']

    # Guardar el usuario en la base de datos
    botBD.addUsuario(user_id, name, age, weight, language)

    if language == 'en':
        await update.message.reply_text(f"Your data has been saved, {name}!")
    else:
        await update.message.reply_text(f"¡Tus datos han sido guardados, {name}!")

    await main_menu(update.message, context)
    return ConversationHandler.END

# Función para mostrar el menú principal
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔄 Cambiar idioma", callback_data='change_language'), 
         InlineKeyboardButton("🆕 Nueva rutina", callback_data='new_routine')],
        [InlineKeyboardButton("📋 Mis rutinas", callback_data='my_routines')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.reply_text('Menú principal:\n\n- 🔄 Cambiar idioma\n- 🆕 Nueva rutina\n- 📋 Mis rutinas', reply_markup=reply_markup)

# Función para gestionar los botones del menú
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'change_language':
        await query.edit_message_text(text="Función para cambiar el idioma aún no implementada.")
    elif query.data == 'new_routine':
        await query.edit_message_text(text="Selecciona el tipo de rutina:")
        
        # Crear botones para seleccionar tipo de rutina
        routine_types = ["Cardio", "Fuerza", "Flexibilidad"]  # Modifica según los tipos de rutina disponibles
        keyboard = [[InlineKeyboardButton(routine, callback_data=routine) for routine in routine_types]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_reply_markup(reply_markup=reply_markup)
        return ROUTINE_TYPE
    elif query.data == 'my_routines':
        await query.edit_message_text(text="Función para mostrar tus rutinas aún no implementada.")

# Función para gestionar la selección de tipo de rutina
async def routine_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data['routine_type'] = query.data
    await query.edit_message_text(text="¿Cómo quieres nombrar la rutina?")
    
    return ROUTINE_NAME

# Función para procesar el nombre de la rutina
async def process_routine_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['routine_name'] = update.message.text
    await update.message.reply_text("¿Tienes acceso a materiales de gimnasio? (Sí/No)")
    
    return GYM_ACCESS

# Función para manejar el acceso a materiales
async def handle_gym_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gym_access = update.message.text.lower()
    context.user_data['gym_access'] = gym_access in ['sí', 'si', 'yes']

    await update.message.reply_text("Indica una hora para completar la rutina (HH:MM).")
    
    return COMPLETION_TIME

# Función para procesar la hora de completado
async def process_completion_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    completion_time = update.message.text
    context.user_data['completion_time'] = completion_time

    # Aquí puedes guardar la rutina en la base de datos
    user_id = update.message.from_user.id
    routine_name = context.user_data['routine_name']
    routine_type = context.user_data['routine_type']
    gym_access = context.user_data['gym_access']

    # Guarda la rutina en la base de datos
    # Aquí podrías crear una función en botBD que guarde la rutina en la base de datos

    await update.message.reply_text(f"Rutina '{routine_name}' de tipo '{routine_type}' guardada con éxito.")
    await main_menu(update.message, context)
    return ConversationHandler.END

# Función para manejar mensajes de texto
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f'Has enviado: {text}')

def main():
    # Crear la aplicación
    app = Application.builder().token(TOKEN).build()

    # Crear un manejador de conversación para la recopilación de datos
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            LANGUAGE: [CallbackQueryHandler(language_selection)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_age)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_weight)],
            ROUTINE_TYPE: [CallbackQueryHandler(routine_type_selection)],
            ROUTINE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_routine_name)],
            GYM_ACCESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gym_access)],
            COMPLETION_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_completion_time)]
        },
        fallbacks=[]
    )

    # Añadir manejadores
    app.add_handler(conversation_handler)
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Comenzar el bot
    app.run_polling()

if __name__ == "__main__":
    main()
