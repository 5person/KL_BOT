# Телеграм Бот

Этот репозиторий содержит телеграм-бота на Python. Он принимает фотографию лица
и отправляет её в OpenAI, возвращая пользователю анализ кожи с рекомендациями.

## Требования

- Python 3.8+
- библиотеки `python-telegram-bot`, `openai` и `python-dotenv`

## Установка

```bash
pip install -r requirements.txt
```

Перед запуском создайте файл `.env` рядом с `bot.py` и укажите в нём
переменные `TELEGRAM_TOKEN` и `OPENAI_API_KEY`:

```env
TELEGRAM_TOKEN=ваш_токен
OPENAI_API_KEY=ваш_api_ключ
```

## Запуск

```bash
python bot.py
```

Бот работает в режиме polling и выводит информацию в консоль.
