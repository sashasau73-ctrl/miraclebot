from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
from config.states import LEAD_MAGNIT


async def gpt_talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client = OpenAI()
    response = client.completions.create(
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
