from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# API Token і ID групи
API_TOKEN = '8140756138:AAFw5wu_BZ_eMvbSPR1r5uUVLZ8-t7fezqs'
GROUP_ID = '-1002289551899'

# Функція для надсилання повідомлень до групи
async def send_message_to_group(context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    try:
        await context.bot.send_message(chat_id=GROUP_ID, text=text)
    except Exception as e:
        print(f"Помилка надсилання повідомлення до групи: {e}")

# Головне меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Приготувати кальян", callback_data='prepare_hookah')],
        [InlineKeyboardButton("Покликати кальянного майстра", callback_data='call_master')],
        [InlineKeyboardButton("Я пересів, знайшов стіл", callback_data='found_table')],
        [InlineKeyboardButton("Зворотній зв'язок", callback_data='feedback')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привіт, я chat-бот помічник Тяга.\nОберіть наступну дію:', reply_markup=reply_markup)

# Обробник для кнопки "Приготувати кальян"
async def prepare_hookah(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Покликати кальянного майстра", callback_data='call_master')],
        [InlineKeyboardButton("Написати самостійно", callback_data='write_own')],
        [InlineKeyboardButton("Повернутися назад", callback_data='back_to_main')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Оберіть наступну дію:", reply_markup=reply_markup)

# Обробник для "Покликати кальянного майстра"
async def call_master(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Я без столу", callback_data='no_table')],
        [InlineKeyboardButton("Повернутися назад", callback_data='prepare_hookah')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Введіть номер столу або оберіть дію:", reply_markup=reply_markup)

# Обробник для "Я без столу"
async def no_table(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Повернутися назад", callback_data='call_master')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Опишіть коротко, як вас знайти:", reply_markup=reply_markup)

# Обробник тексту для номера столу
async def handle_table_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response_message = f"Дякуємо, очікуйте на кальянного майстра за столом {update.message.text}"
    await update.message.reply_text(text=response_message, reply_markup=reply_markup)
    context.user_data["current_action"] = None

# Обробник тексту для "Я без столу"
async def handle_no_table_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response_message = "Дякуємо, очікуйте на кальянного майстра"
    await update.message.reply_text(text=response_message, reply_markup=reply_markup)
    context.user_data["current_action"] = None



# Обробник для кнопки "Написати самостійно"
async def write_own(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Повернутися назад", callback_data='prepare_hookah')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Напишіть міцність, смак та свої вподобання", reply_markup=reply_markup)

# Обробник тексту для "Написати самостійно"
async def handle_write_own_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["custom_preference"] = update.message.text  # зберігаємо текст
    keyboard = [
        [InlineKeyboardButton("Я без столу", callback_data='no_table')],
        [InlineKeyboardButton("Повернутися назад", callback_data='prepare_hookah')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text="Введіть номер столу або оберіть дію:", reply_markup=reply_markup)

# Обробник для "Я без столу" після введення уподобань
async def handle_no_table_response_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Повернутися назад", callback_data='write_own')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text="Опишіть коротко, як вас знайти:", reply_markup=reply_markup)

# Обробник тексту для "Я без столу" після введення тексту "як вас знайти"
async def handle_no_table_details_response_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response_message = "Дякуємо, Ваш кальян вже готується."
    await update.message.reply_text(text=response_message, reply_markup=reply_markup)
    context.user_data["current_action"] = None

# Обробник для номеру столу після введення уподобань
async def handle_table_response_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response_message = f"Дякуємо, Ваш кальян готується для номеру столу {update.message.text}."
    await update.message.reply_text(text=response_message, reply_markup=reply_markup)
    context.user_data["current_action"] = None




# Функція для натискання кнопки "Покликати кальянного майстра" з цифрою 3
async def call_master_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Замінити вугілля", callback_data='replace_coal_3')],
        [InlineKeyboardButton("Щось з кальяном", callback_data='something_with_hookah_3')],
        [InlineKeyboardButton("Прийняти замовлення", callback_data='accept_order_3')],
        [InlineKeyboardButton("Повернутися назад", callback_data='back_to_main')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Оберіть наступну дію:", reply_markup=reply_markup)

# Функція для натискання кнопки "Замінити вугілля" з цифрою 3
async def replace_coal_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Я без столу", callback_data='no_table_3')],
        [InlineKeyboardButton("Повернутися назад", callback_data='call_master_3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Введіть номер столу або оберіть дію:", reply_markup=reply_markup)

# Функція для натискання кнопки "Щось з кальяном" з цифрою 3
async def something_with_hookah_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Я без столу", callback_data='no_table_3')],
        [InlineKeyboardButton("Повернутися назад", callback_data='call_master_3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Введіть номер столу або оберіть дію:", reply_markup=reply_markup)

# Функція для натискання кнопки "Прийняти замовлення" з цифрою 3
async def accept_order_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await replace_coal_3(update, context)  # Викликаємо ту ж саму логіку, що й для "Замінити вугілля"

# Функція для натискання кнопки "Я без столу" (відповідно до введеного тексту) з цифрою 3
async def no_table_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Повернутися назад", callback_data='replace_coal_3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Опишіть коротко, як вас знайти:", reply_markup=reply_markup)

# Функція для обробки введеного номера столу або тексту "як вас знайти" з цифрою 3
async def handle_table_or_no_table_response_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message.text.isdigit():  # Якщо введено номер столу
        response_message = f"Прийнято, очікуйте на кальянного майстра за столом {update.message.text}."
    else:  # Якщо введено опис місцезнаходження
        response_message = "Прийнято, очікуйте на кальянного майстра."
    
    await update.message.reply_text(text=response_message, reply_markup=reply_markup)
    context.user_data["current_action"] = None





# Функція для натискання кнопки "Я пересів/знайшов стіл"
async def found_table_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Я пересів", callback_data='moved_seat_4')],
        [InlineKeyboardButton("Знайшов стіл", callback_data='found_table_4_action')],
        [InlineKeyboardButton("Повернутися назад", callback_data='back_to_main')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Оберіть наступну дію:", reply_markup=reply_markup)

# Функція для натискання кнопки "Я пересів" з цифрою 4
async def moved_seat_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Повернутися назад", callback_data='found_table_4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Напишіть попередній номер столу:", reply_markup=reply_markup)

# Функція для обробки попереднього столу
async def handle_previous_table_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["previous_table"] = update.message.text  # Зберігаємо попередній стіл
    keyboard = [
        [InlineKeyboardButton("Повернутися назад", callback_data='moved_seat_4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text="Напишіть актуальний номер столу:", reply_markup=reply_markup)

# Функція для обробки актуального столу
async def handle_current_table_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    previous_table = context.user_data.get("previous_table", "не вказано")
    current_table = update.message.text
    keyboard = [
        [InlineKeyboardButton("Головне меню", callback_data='back_to_main')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response_message = f"Дякуємо за уточнення, Ваш попередній стіл {previous_table} змінено на {current_table}."
    await update.message.reply_text(text=response_message, reply_markup=reply_markup)
    context.user_data["previous_table"] = None  # Очищаємо збережену інформацію про попередній стіл

# Функція для натискання кнопки "Знайшов стіл" з цифрою 4
async def found_table_4_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Повернутися назад", callback_data='found_table_4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Напишіть номер замовлення:", reply_markup=reply_markup)

# Функція для обробки номеру замовлення
async def handle_order_number_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["order_number"] = update.message.text  # Зберігаємо номер замовлення
    keyboard = [
        [InlineKeyboardButton("Повернутися назад", callback_data='found_table_4_action')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text="Напишіть актуальний номер столу:", reply_markup=reply_markup)

# Функція для обробки актуального столу після "Знайшов стіл"
async def handle_current_table_after_found_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    order_number = context.user_data.get("order_number", "не вказано")
    current_table = update.message.text
    keyboard = [
        [InlineKeyboardButton("Головне меню", callback_data='back_to_main')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response_message = "Дякуємо за уточнення!"
    await update.message.reply_text(text=response_message, reply_markup=reply_markup)
    context.user_data["order_number"] = None  # Очищаємо збережену інформацію про номер замовлення





# Функція для зворотного зв'язку
async def feedback_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Написати уточнення", callback_data='write_clarification_5')],
        [InlineKeyboardButton("Залишити чайові/відгук", callback_data='leave_tip_feedback_5')],
        [InlineKeyboardButton("Інстаграм", url='https://instagram.com/your_instagram_link')],
        [InlineKeyboardButton("Повернутися назад", callback_data='back_to_main_5')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Оберіть наступну дію:", reply_markup=reply_markup)

# Функція для "Написати уточнення"
async def write_clarification_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Повернутися назад", callback_data='feedback_5')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Напишіть будь ласка уточнення по замовленню, побажання, або відгук (повідомлення буде прийнято без зворотньої відповіді):", reply_markup=reply_markup)

# Обробник тексту для "Написати уточнення"
async def handle_clarification_response_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='back_to_main_5')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text="Дякуємо за відповідь!", reply_markup=reply_markup)

# Функція для "Залишити чайові/відгук"
async def leave_tip_feedback_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("monoБанка", url="https://monobank.link")],
        [InlineKeyboardButton("Повернутися назад", callback_data='feedback_5')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Напишіть будь ласка текст або оберіть наступну дію:", reply_markup=reply_markup)

# Обробник тексту для "Залишити чайові/відгук"
async def handle_tip_feedback_response_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Головне меню", callback_data='back_to_main_5')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text="Дякуємо за відповідь!", reply_markup=reply_markup)

# Функція для "Інстаграм" (посилання)
async def instagram_link_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Перейдіть на наш Instagram профіль за посиланням: https://instagram.com/your_instagram_link")

# Обробник для кнопки "Повернутися назад"
async def back_to_main_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Приготувати кальян", callback_data='prepare_hookah_5')],
        [InlineKeyboardButton("Покликати кальянного майстра", callback_data='call_master_5')],
        [InlineKeyboardButton("Я пересів, знайшов стіл", callback_data='found_table_5')],
        [InlineKeyboardButton("Зворотній зв'язок", callback_data='feedback_5')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Привіт, я chat-бот помічник Тяга.\nОберіть наступну дію:", reply_markup=reply_markup)





# Обробник для повернення в головне меню
async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Приготувати кальян", callback_data='prepare_hookah')],
        [InlineKeyboardButton("Покликати кальянного майстра", callback_data='call_master')],
        [InlineKeyboardButton("Я пересів, знайшов стіл", callback_data='found_table')],
        [InlineKeyboardButton("Зворотній зв'язок", callback_data='feedback')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Привіт, я chat-бот помічник Тяга.\nОберіть наступну дію:", reply_markup=reply_markup)

# Ініціалізація та запуск бота
application = Application.builder().token(API_TOKEN).build()
# Додавання обробників для команд
application.add_handler(CommandHandler("start", start))
# Обробники для кнопок
application.add_handler(CallbackQueryHandler(prepare_hookah, pattern="^prepare_hookah$"))
application.add_handler(CallbackQueryHandler(call_master, pattern="^call_master$"))
application.add_handler(CallbackQueryHandler(no_table, pattern="^no_table$"))
application.add_handler(CallbackQueryHandler(back_to_main, pattern="^back_to_main$"))
application.add_handler(CallbackQueryHandler(write_own, pattern="^write_own$"))  # обробник для "Написати самостійно"
application.add_handler(CallbackQueryHandler(call_master_3, pattern="^call_master_3$"))
application.add_handler(CallbackQueryHandler(replace_coal_3, pattern="^replace_coal_3$"))
application.add_handler(CallbackQueryHandler(something_with_hookah_3, pattern="^something_with_hookah_3$"))
application.add_handler(CallbackQueryHandler(accept_order_3, pattern="^accept_order_3$"))
application.add_handler(CallbackQueryHandler(no_table_3, pattern="^no_table_3$"))
application.add_handler(CallbackQueryHandler(found_table_4, pattern="^found_table_4$"))
application.add_handler(CallbackQueryHandler(moved_seat_4, pattern="^moved_seat_4$"))
application.add_handler(CallbackQueryHandler(found_table_4_action, pattern="^found_table_4_action$"))
application.add_handler(CallbackQueryHandler(found_table_5, pattern="^found_table_5$"))
application.add_handler(CallbackQueryHandler(moved_seat_5, pattern="^moved_seat_5$"))
application.add_handler(CallbackQueryHandler(found_table_5_action, pattern="^found_table_5_action$"))
application.add_handler(CallbackQueryHandler(feedback_5, pattern="^feedback_5$"))
application.add_handler(CallbackQueryHandler(write_clarification_5, pattern="^write_clarification_5$"))
application.add_handler(CallbackQueryHandler(leave_tip_feedback_5, pattern="^leave_tip_feedback_5$"))
application.add_handler(CallbackQueryHandler(instagram_link_5, pattern="^instagram_link_5$"))
application.add_handler(CallbackQueryHandler(back_to_main_5, pattern="^back_to_main_5$"))

# Додавання обробників для введених текстів
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_table_response))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_no_table_response))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_write_own_response))  # обробка тексту після "Написати самостійно"
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_table_response_2))  # обробка введеного номеру столу
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_no_table_details_response_2))  # обробка тексту для "Я без столу"
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_table_or_no_table_response_3))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_previous_table_4))  # Обробка попереднього столу
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_current_table_4))  # Обробка актуального столу після "Я пересів"
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order_number_4))  # Обробка номеру замовлення
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_current_table_after_found_4))  # Обробка актуального столу після "Знайшов стіл"
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_clarification_response_5))  # Обробка уточнень
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tip_feedback_response_5))  # Обробка чайових/відгуку

application.run_polling()
