from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import (
    FIRST_NAME,
    EMAIL_USER,
    NUMBER_PHONE,
    ANSWER,
    INLINE_BUTTON,
    LEAD_MAGNIT,
)
from handlers.jobs import send_job_message
from datetime import timedelta
from db.users_crud import create_user, get_user, update_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[update.effective_user.first_name]]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на своё имя или напишите",
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет, как ваше имя?",
        reply_markup=markup,
    )
    if not await get_user(update.effective_user.id):
        await create_user(update.effective_user.id)
    
    return FIRST_NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_message.text
    await update_user(update.effective_user.id, name=name)
    keyboard = [[KeyboardButton("Отправить номер телефона", request_contact=True)]]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку",
    )
    context.user_data["name"] = name
    if name:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Приятно познакомиться, {name}! Уточните ваш номер телефона для дальнейшего взаимодействия.",
            reply_markup=markup,
        )
        return NUMBER_PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.effective_message.contact.phone_number
    context.user_data["phone_number"] = phone
    await update_user(update.effective_user.id, phone=phone)
    if phone:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Спасибо! Напишите ваш email для регистрации.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return EMAIL_USER


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.effective_message.text
    await update_user(update.effective_user.id, email=email)
    keyboard = [["Да", "Нет"], ["Я подумаю"]]
    markup = ReplyKeyboardMarkup(keyboard)
    context.user_data["email"] = email
    if email:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ваша регистрация завершена. Я должен у вас уточнить, согласны ли вы на обработку персональных данных?",
            reply_markup=markup,
        )
        return ANSWER


async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.effective_message.text.strip().lower()
    await update_user(update.effective_user.id, agreement=1)
    if answer == "да":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Отлично! Спасибо что доверились нам.",
            reply_markup=ReplyKeyboardRemove(),
        )
        keyboard = [
            [
                InlineKeyboardButton(
                    "Получить", url="https://rules-ring-okj.craft.me/PBOF7N4wwWBmun"
                ),
                InlineKeyboardButton("Хочу больше", callback_data="more"),
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Вот ваш лид-магнит.",
            reply_markup=markup,
        )

        await context.bot.send_message(
            chat_id=591650405,
            text=f"Имя: {context.user_data['name']}\nТелефон: {context.user_data['phone_number']}\nEmail: {context.user_data['email']}\nUser ID: {update.effective_user.id}",
        )
        return LEAD_MAGNIT

    else:
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data="yes"),
                InlineKeyboardButton("Нет", callback_data="no"),
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Тогда всё!", reply_markup=markup
        )
        return INLINE_BUTTON


async def get_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "yes":
        await query.edit_message_text(text="Спасибо за ответ!")
    return FIRST_NAME


async def lead_magnit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "more":
        keyboard = [
            [
                InlineKeyboardButton(
                    "Получить", url="https://rules-ring-okj.craft.me/JTs9GTTHqrznRk"
                )
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Вот второй лид-магнит с дополнительной информацией!",
            reply_markup=markup,
        )
        context.job_queue.run_once(
            send_job_message,
            when=timedelta(hours=1),
            data={"message": "Вы забыли забрать свой материал!"},
            name="send_job_message",
            chat_id=update.effective_user.id,
        )
        return ANSWER

    return ANSWER
