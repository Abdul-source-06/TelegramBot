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
    user = botBD.get_user(user_id)  # Recupera l'usuari des de la base de dades

    if user:
        # Utilitzem la funció get_idioma per obtenir l'idioma de l'usuari
        idioma = botBD.get_idioma(user_id)
        
        if idioma == 'es':
            await update.message.reply_text(f"¡Bienvenido de nuevo, {user[1]}!")
        else:
            await update.message.reply_text(f"Welcome back, {user[1]}!")

        await main_menu(update, context)  # Llamada corregida aquí

    else:
        # Si l'usuari no existeix, demanem que seleccioni l'idioma
        await update.message.reply_text('¡Bienvenido a FitBot! Comencemos con tu entrenamiento. Primero, selecciona tu idioma.')

        # Crear botons per a la selecció de l'idioma
        keyboard = [
            [InlineKeyboardButton("English", callback_data='en'), InlineKeyboardButton("Español", callback_data='es')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Enviar el missatge amb els botons d'idioma
        await update.message.reply_text('Selecciona el idioma:', reply_markup=reply_markup)
        return LANGUAGE  # Continuar el flux després de la selecció de l'idioma

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

# Funció per processar el nom i manejar l'idioma
async def process_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    # Recuperem l'idioma seleccionat per l'usuari
    idioma = botBD.get_idioma(user_id)
    
    # Guardem el nom de l'usuari al context
    context.user_data['name'] = update.message.text
    
    # Enviem el missatge en l'idioma seleccionat
    if idioma == 'es':
        await update.message.reply_text("¿Cuántos años tienes?")  # Missatge en espanyol
    else:
        await update.message.reply_text("How old are you?")  # Missatge en anglès
    
    return AGE  # Continuem el flux de la conversa

# Funció per processar l'edat i manejar l'idioma
async def process_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    # Recuperar l'idioma seleccionat per l'usuari
    idioma = botBD.get_idioma(user_id)
    
    # Guardar l'edat de l'usuari al context
    context.user_data['age'] = int(update.message.text)
    
    # Enviar el missatge segons l'idioma seleccionat
    if idioma == 'es':
        await update.message.reply_text("¿Cuál es tu peso (en kg)?")  # Missatge en espanyol
    else:
        await update.message.reply_text("What is your weight (in kg)?")  # Missatge en anglès
    
    return WEIGHT  # Continuar el flux de la conversa

# Función para procesar el peso y guardar el usuario
async def process_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = context.user_data['name']
    age = context.user_data['age']
    weight = float(update.message.text)
    language = context.user_data['language']

    # Guardar el usuario en la base de datos
    botBD.addUsuario(user_id, name, age, weight, language)

    # Asegúrate de que el idioma se guarda correctamente
    botBD.guardar_idioma_en_bd(user_id, language)

    if language == 'en':
        await update.message.reply_text(f"Your data has been saved, {name}!")
        await main_menu(update, context)
    else:
        await update.message.reply_text(f"¡Tus datos han sido guardados, {name}!")
        await main_menu(update, context)

    return ConversationHandler.END
    
# Funció per mostrar el menú principal i manejar l'idioma
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Comprobar si el 'update' proviene de una interacción con un botón o un mensaje directo
    if hasattr(update, 'message') and update.message:
        message = update.message
    elif hasattr(update, 'callback_query') and update.callback_query:
        message = update.callback_query.message
    else:
        return  # En caso de que no se pueda determinar el origen, salir de la función

    user_id = message.from_user.id  # Cambiado a message

    # Recuperar l'idioma seleccionat per l'usuari
    idioma = botBD.get_idioma(user_id)  # Obtener el idioma actual del usuario

    # Definir els botons del menú segons l'idioma seleccionat
    if idioma == 'es':
        keyboard = [
            [InlineKeyboardButton("🔄 Cambiar idioma", callback_data='change_language'),
             InlineKeyboardButton("🆕 Nueva rutina", callback_data='new_routine')],
            [InlineKeyboardButton("📋 Mis rutinas", callback_data='my_routines')]
        ]
        menu_text = 'Menú principal:\n\n- 🔄 Cambiar idioma\n- 🆕 Nueva rutina\n- 📋 Mis rutinas'
    else:
        keyboard = [
            [InlineKeyboardButton("🔄 Change language", callback_data='change_language'),
             InlineKeyboardButton("🆕 New routine", callback_data='new_routine')],
            [InlineKeyboardButton("📋 My routines", callback_data='my_routines')]
        ]
        menu_text = 'Main menu:\n\n- 🔄 Change language\n- 🆕 New routine\n- 📋 My routines'

    # Crear el teclat amb els botons traduïts
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Enviar el missatge del menú principal amb els botons
    await message.reply_text(menu_text, reply_markup=reply_markup)

# Funció per gestionar els botons del menú
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id  # Obtener el ID del usuario
    idioma = botBD.get_idioma(user_id)  # Recuperar el idioma seleccionado por el usuario

    # Cambiar el idioma
    if query.data == 'change_language':
        # Cambiar el idioma al opuesto
        selected_idioma = 'es' if idioma == 'en' else 'en'

        # Guardar el nuevo idioma en la base de datos
        botBD.guardar_idioma_en_bd(user_id, selected_idioma)

        # Respuesta confirmando la actualización del idioma
        if selected_idioma == 'es':
            await query.edit_message_text(text="Idioma actualizado a Español.")
        else:
            await query.edit_message_text(text="Language updated to English.")
        
        # Mostrar el menú principal con el nuevo idioma
        await main_menu(query, context)  # Mostrar el menú en el nuevo idioma

    elif query.data == 'new_routine':
        # Al seleccionar una nueva rutina, hay que pedir el tipo de rutina
        if idioma == 'es':
            await query.edit_message_text(text="Selecciona el tipo de rutina:")
            routine_types = ["Cardio", "Fuerza", "Flexibilidad"]  # Tipos de rutina en español
        else:
            await query.edit_message_text(text="Select the type of routine:")
            routine_types = ["Cardio", "Strength", "Flexibility"]  # Tipos de rutina en inglés

        # Crear botones para seleccionar el tipo de rutina
        keyboard = [[InlineKeyboardButton(routine, callback_data=routine) for routine in routine_types]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_reply_markup(reply_markup=reply_markup)
            
    # Mostrar las rutinas guardadas del usuario
    elif query.data == 'my_routines':
        # Obtener las rutinas del usuario
        rutinas = botBD.get_usuarioRutina(user_id)
        
        # Si el usuario no tiene rutinas guardadas
        if not rutinas:
            text = "No tienes ninguna rutina guardada." if idioma == 'es' else "You don't have any saved routines."
        else:
            # Si tiene rutinas, las mostramos
            rutina_texts = []
            for rutina in rutinas:
                id_rutina = rutina[2]  # Suponiendo que el tercer campo es el idRutina
                info_rutina = botBD.get_tiposRutinas(id_rutina, idioma)
                nombre_rutina = rutina[1]  # Nombre de la rutina
                
                if idioma == 'es':
                    rutina_texts.append(f"Nombre: {nombre_rutina}\nTipo: {info_rutina[1]}")
                else:
                    rutina_texts.append(f"Name: {nombre_rutina}\nType: {info_rutina[1]}")
            
            # Unir todas las rutinas en un solo texto
            text_rutinas = "\n\n".join(rutina_texts)
            text = f"Estas son tus rutinas guardadas:\n\n{text_rutinas}" if idioma == 'es' else f"Here are your saved routines:\n\n{text_rutinas}"
        
        # Agregar el botón de volver al menú
        back_button = InlineKeyboardButton("⬅️ Volver al menú", callback_data='back_to_menu') if idioma == 'es' else InlineKeyboardButton("⬅️ Back to menu", callback_data='back_to_menu')

        keyboard = [[back_button]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text=text, reply_markup=reply_markup)

    # Volver al menú principal
    elif query.data == 'back_to_menu':
        await main_menu(query, context)

        
# Funció per gestionar la selecció de tipus de rutina
async def routine_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id  # Obtener el ID del usuario
    tipo_rutina = query.data  # Captura el tipo de rutina seleccionado
    context.user_data['routine_type'] = tipo_rutina  # Guardar el tipo de rutina en el contexto

    # Obtener el idioma del usuario
    idioma = botBD.get_idioma(user_id)
    
    # Comprobar si el tipo de rutina ya existe
    rutina_existente = botBD.get_tiposRutinas(tipo_rutina, idioma)

    if not rutina_existente:
        # Asignar un nuevo ID para el tipo de rutina
        next_id = botBD.get_next_rutina_id()  # Función para obtener el siguiente ID disponible
        # Añadir el nuevo tipo de rutina a la base de datos
        botBD.add_tipoRutina(next_id, tipo_rutina, "30-45 min", True, idioma)
        id_rutina = next_id  # Guardar el nuevo ID de rutina
    else:
        # Si la rutina existe, obtener el ID de la rutina
        id_rutina = rutina_existente[0]  # Suponiendo que el primer elemento de la tupla es el ID

    # Mensaje según el idioma
    if idioma == 'es':
        await query.edit_message_text(text="¿Cómo quieres nombrar la rutina?")
    else:
        await query.edit_message_text(text="What do you want to name the routine?")

    context.user_data['id_rutina'] = id_rutina  # Guardar el ID de la rutina en el contexto
    return ROUTINE_NAME

# Funció per processar el nom de la rutina
async def process_routine_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['routine_name'] = update.message.text  # Guardar el nombre de la rutina
    
    user_id = update.message.from_user.id  # Obtener l'ID de l'usuari
    idioma = botBD.get_idioma(user_id)  # Recuperar l'idioma seleccionat per l'usuari
    
    # Missatge segons l'idioma
    if idioma == 'es':
        await update.message.reply_text("¿Tienes acceso a materiales de gimnasio? (Sí/No)")
    else:
        await update.message.reply_text("Do you have access to gym materials? (Yes/No)")
    
    return GYM_ACCESS

# Funció per manejar l'accés a materials
async def handle_gym_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gym_access = update.message.text.lower()
    context.user_data['gym_access'] = gym_access in ['sí', 'si', 'yes']

    user_id = update.message.from_user.id  # Obtenir l'ID de l'usuari
    idioma = botBD.get_idioma(user_id)  # Recuperar l'idioma seleccionat per l'usuari
    
    # Missatge segons l'idioma
    if idioma == 'es':
        await update.message.reply_text("Indica una hora para completar la rutina (HH:MM).")
    else:
        await update.message.reply_text("Indicate a time to complete the routine (HH:MM).")
    
    return COMPLETION_TIME

async def process_completion_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    completion_time = update.message.text
    context.user_data['completion_time'] = completion_time

    # Obtener l'ID de l'usuari i l'idioma seleccionat
    user_id = update.message.from_user.id
    idioma = botBD.get_idioma(user_id)

    routine_name = context.user_data['routine_name']
    routine_type = context.user_data['routine_type']
    gym_access = context.user_data['gym_access']

    # Verificar si el tipo de rutina ya existe en la base de datos
    rutina = botBD.get_tiposRutinas(routine_type, idioma)
    
    # Si no existe, añadir el nuevo tipo de rutina a la base de datos
    if not rutina:
        # Asignar un nuevo ID para el tipo de rutina
        next_id = botBD.get_next_rutina_id()  # Función para obtener el siguiente ID disponible
        botBD.add_tipoRutina(next_id, routine_type, "30-45 min", gym_access, idioma)
        id_rutina = next_id
    else:
        # Si la rutina existe, obtener el ID de la rutina
        id_rutina = rutina[0]  # Suponiendo que el primer elemento de la tupla es el ID

    # Guarda la rutina del usuario en la base de datos
    botBD.add_usuarioRutina(user_id, routine_name, id_rutina)

    # Confirmación para el usuario
    if idioma == 'es':
        await update.message.reply_text(f"Rutina '{routine_name}' de tipo '{routine_type}' guardada con éxito.")
    else:
        await update.message.reply_text(f"Routine '{routine_name}' of type '{routine_type}' saved successfully.")

    # Volver al menú principal
    await main_menu(update.message, context)
    return ConversationHandler.END



# Funció per manejar missatges de text
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id  # Obtenir l'ID de l'usuari
    idioma = botBD.get_idioma(user_id)  # Recuperar l'idioma seleccionat per l'usuari

    # Resposta segons l'idioma
    if idioma == 'es':
        await update.message.reply_text("Acabas de enviar un mensaje de texto, pero actualmente no tenemos opción para responder a preguntas o cualquier cosa así. Si necesitas ayuda, selecciona /help.")
    else:
        await update.message.reply_text("You just sent a text message, but currently we don't have an option to answer questions or anything like that. If you need help, please select /help.")


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