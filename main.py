import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

FIRST_NAME, EMAIL_USER, NUMBER_PHONE, ANSWER = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Привет, как ваше имя?"
    )
    return FIRST_NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_message.text
    if name:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Приятно познакомиться, {name}! Уточните ваше номер телефона для дальнейшего взаимодействия.",
        )
        return NUMBER_PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.effective_message.text
    if phone_number:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Спасибо! Напишите ваш email для регестрации.",
        )
        return EMAIL_USER


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.effective_message.text
    if email:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Ваша регистрация завершена. Я должен у вас уточнить, согласны ли вы на обработку персональных данных?",
        )
        return ANSWER


async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.effective_message.text
    if answer.lower() == "Да":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Отлично! Спасибо что доверились нам. Вот ваш лид-магнит.",
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_NAME: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND, callback=get_name
                )
            ],
            NUMBER_PHONE: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND, callback=get_phone
                )
            ],
            EMAIL_USER: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND, callback=get_email
                )
            ],
            ANSWER: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND, callback=get_answer
                )
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()
    # вроде сделал публичный
