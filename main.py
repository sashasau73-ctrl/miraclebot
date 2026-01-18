import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    PicklePersistence,
)

from handlers.progrev_handler import (
    start,
    get_name,
    get_phone,
    get_email,
    get_answer,
    get_inline_button,
    lead_magnit,
    gpt5_click,
)

from config.states import (
    FIRST_NAME,
    EMAIL_USER,
    NUMBER_PHONE,
    ANSWER,
    INLINE_BUTTON,
    LEAD_MAGNIT,
    GPT_TALK,
    ADMIN_START,
)

from db.database import create_tables
from logs.logger import logger
from handlers.gpt_talk import gpt_talk
from config.config import TOKEN
from handlers.admins_handler import (
    hot_users_list,
    send_message_all,
    users_list,
    user_list_csv,
    normal_users_list,
    cold_users_list,
    bought_users_list,
)


if __name__ == "__main__":
    persistence = PicklePersistence(filepath="MiracleBot")
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .persistence(persistence)
        .post_init(create_tables)
        .build()
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
                CallbackQueryHandler(callback=get_inline_button, pattern="no"),
            ],
            LEAD_MAGNIT: [
                CallbackQueryHandler(callback=lead_magnit, pattern="more"),
                CallbackQueryHandler(callback=gpt5_click, pattern="gpt5"),
            ],
            GPT_TALK: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND, callback=gpt_talk
                )
            ],
            # Admin handlers
            ADMIN_START: [
                CallbackQueryHandler(callback=users_list, pattern="users_list"),
                CallbackQueryHandler(callback=user_list_csv, pattern="user_list_csv"),
                CallbackQueryHandler(
                    callback=send_message_all, pattern="send_message_all"
                ),
                CallbackQueryHandler(callback=hot_users_list, pattern="hot_users_list"),
                CallbackQueryHandler(
                    callback=normal_users_list, pattern="normal_users_list"
                ),
                CallbackQueryHandler(
                    callback=cold_users_list, pattern="cold_users_list"
                ),
                CallbackQueryHandler(
                    callback=bought_users_list, pattern="bought_users_list"
                ),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        persistent=True,
        name="my_conversation",
    )

    application.add_handler(conv_handler)
    logger.info("Бот полетел!🤟")
    application.run_polling()
