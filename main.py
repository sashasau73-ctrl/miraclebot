import logging
import os
from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from handlers.progrev_handler import (
    start,
    get_name,
    get_phone,
    get_email,
    get_answer,
    get_inline_button,
    lead_magnit,
)

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


from config.states import (
    FIRST_NAME,
    EMAIL_USER,
    NUMBER_PHONE,
    ANSWER,
    INLINE_BUTTON,
    LEAD_MAGNIT,
)

from db.database import create_tables
import asyncio

if __name__ == "__main__":
    application = (
        ApplicationBuilder().token(os.getenv("TOKEN")).post_init(create_tables).build()
    )

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
                    filters=filters.CONTACT | filters.TEXT & ~filters.COMMAND,
                    callback=get_phone,
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
            INLINE_BUTTON: [
                CallbackQueryHandler(callback=get_inline_button, pattern="yes"),
                CallbackQueryHandler(callback=get_email, pattern="no"),
            ],
            LEAD_MAGNIT: [
                CallbackQueryHandler(callback=lead_magnit, pattern="more"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()
