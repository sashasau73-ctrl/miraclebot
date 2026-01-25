from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
from config.states import LEAD_MAGNIT, GPT_TALK
from config.config import OPENAI_API_KEY



async def gpt5_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Отлично! Теперь напишите ваш вопрос для GPT-5:"
    )
    return GPT_TALK

async def gpt_talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-5",
        reasoning={"effort": "low"},
        input=[
            {
                "role": "developer",
                "content": "Говори с пользователем как высококвалифицированный помощник.",
            },
            {"role": "user", "content": update.effective_message.text},
        ],
    )
    print(response.output_text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=response.output_text
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Задайте ещё вопрос или напишите /start для выхода",
    )
    return LEAD_MAGNIT
