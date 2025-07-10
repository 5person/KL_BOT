import base64
import logging
import os
from io import BytesIO

import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Пришлите фото лица, и я дам рекомендации по уходу за кожей."
    )


async def analyze_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.photo:
        await update.message.reply_text("Пожалуйста, отправьте фотографию.")
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    bio = BytesIO()
    await file.download_to_memory(out=bio)
    bio.seek(0)
    encoded = base64.b64encode(bio.read()).decode()

    key = os.getenv("OPENAI_API_KEY")
    if not key:
        await update.message.reply_text(
            "OPENAI_API_KEY environment variable is not set"
        )
        return
    openai.api_key = key

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Определи тип кожи, проблемы и дай рекомендации по уходу.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded}"
                        },
                    },
                ],
            }
        ],
    )

    answer = response.choices[0].message.content.strip()
    await update.message.reply_text(answer)


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN environment variable is not set")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, analyze_photo))
    app.run_polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
