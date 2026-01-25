from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
from db.users_crud import get_users
from logs.logger import logger
import csv
from config.states import ADMIN_START
import asyncio

from utils.escape_sym import escape_sym


async def admins_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Список пользователей", callback_data="users_list")],
        [
            InlineKeyboardButton(
                "Спсиок пользователей с тегом Горячий", callback_data="hot_users_list"
            )
        ],
        [
            InlineKeyboardButton(
                "Спсиок пользователей с тегом Обычный",
                callback_data="normal_users_list",
            )
        ],
        [
            InlineKeyboardButton(
                "Спсиок пользователей с тегом Холодный", callback_data="cold_users_list"
            )
        ],
        [
            InlineKeyboardButton(
                "Спсиок пользователей с тегом Купил", callback_data="bought_users_list"
            )
        ],
        [
            InlineKeyboardButton(
                "Список пользователей csv", callback_data="user_list_csv"
            )
        ],
        [
            InlineKeyboardButton(
                "Рассылка всем пользователям", callback_data="send_message_all"
            )
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Добро пожаловать в панель администратора!",
        reply_markup=markup,
    )
    return ADMIN_START


async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    print(users)
    text = "Список пользователей\:\n"
    text += "№. [Имя](tg://user?id=ID) - Телефон - Email\n"
    for n, user in enumerate(users, 1):
        text += f'{n}. <a href="tg://user?id={user['id_tg']}">{user['name']}</a> - {user['phone']} - {user['email']}\n'
    
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
        parse_mode="HTML",
    )
    await admins_start(update, context)


async def user_list_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    with open("users_list.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["№", "Name", "Phone", "Email"])
        for n, user in enumerate(users, 1):
            writer.writerow([n, user[2], user[3], user[4]])
    await context.bot.send_document(
        chat_id=update.effective_user.id,
        document=open("users_list.csv", "rb"),
        caption="Список пользователей в формате CSV",
    )
    await admins_start(update, context)


async def send_message_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    logger.info(f"Рассылка пользователей началась {len(users)}")
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user[1],
                text="Всем общий!",
            )
            await asyncio.sleep(0.07)
        except Exception as e:
            logger.error(f"Ошибка при отправке пользователю {user[1]}: {e}")
            continue
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Рассылка завершена.",
    )
    await admins_start(update, context)


async def hot_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    text = "Список пользователей с тегом Горячий\:\n"
    for n, user in enumerate(users, 1):
        text += f"{n}\. [{user[2]}](tg://user?id={user[1]}) \- {user[3]} \- {user[4]}\n"
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
        parse_mode="MarkdownV2",
    )
    await admins_start(update, context)


async def normal_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    text = "Список пользователей с тегом Обычный\:\n"
    for n, user in enumerate(users, 1):
        text += f"{n}\. [{user[2]}](tg://user?id={user[1]}) \- {user[3]} \- {user[4]}\n"
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
        parse_mode="MarkdownV2",
    )
    await admins_start(update, context)


async def cold_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    text = "Список пользователей с тегом Холодный\:\n"
    for n, user in enumerate(users, 1):
        text += f"{n}\. [{user[2]}](tg://user?id={user[1]}) \- {user[3]} \- {user[4]}\n"
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
        parse_mode="MarkdownV2",
    )
    await admins_start(update, context)

async def bought_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    text = "Список пользователей с тегом Купил\:\n"
    for n, user in enumerate(users, 1):
        text += f"{n}\. [{user[2]}](tg://user?id={user[1]}) \- {user[3]} \- {user[4]}\n"
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
        parse_mode="MarkdownV2",
    )
    await admins_start(update, context)
    