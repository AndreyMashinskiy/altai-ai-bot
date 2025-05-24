import logging
import json
import asyncio
import datetime
import threading
import http.server
import socketserver
import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from avito_api import get_market_stats
from nspd_services import check_kadastr_data
import openai

# Фиктивный HTTP-сервер для Render
def dummy_server():
    PORT = int(os.environ.get("PORT", 10000))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("🔵 Фиктивный сервер на порту", PORT, "запущен")
        httpd.serve_forever()

# Настройки
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")
DATA_FILE = "data.json"
user_data = {}

logging.basicConfig(level=logging.INFO)

# Загрузка данных
try:
    with open(DATA_FILE, "r") as f:
        user_data = json.load(f)
except:
    user_data = {}

# Сохранение
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f, indent=2)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in user_data:
        user_data[uid] = {"role": "гость", "tasks": [], "ads": [], "reminders": []}
    await update.message.reply_text(
        "👋 Привет! Я Altai.AI — твой ассистент.",
        reply_markup=ReplyKeyboardMarkup([["🧠 План", "⏰ Напоминание"],
                                          ["📈 Инвестиции", "🏡 Объявления"],
                                          ["⚙️ Сменить роль"]], resize_keyboard=True)
    )

async def role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    role = update.message.text
    user_data.setdefault(uid, {})["role"] = role
    save_data()
    await update.message.reply_text(f"Роль установлена: {role}")

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    task = " ".join(context.args)
    user_data[uid]["tasks"].append(task)
    save_data()
    await update.message.reply_text(f"Задача добавлена: {task}")

async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    tasks = user_data[uid].get("tasks", [])
    if not tasks:
        await update.message.reply_text("Задач нет.")
    else:
        await update.message.reply_text("📝 Твои задачи:
" + "\n".join(f"{i+1}. {t}" for i, t in enumerate(tasks)))

async def kadastr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = " ".join(context.args)
    result = check_kadastr_data(num)
    await update.message.reply_text(f"📍 Ответ по участку {num}:
{result}")

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    region = " ".join(context.args)
    stats = get_market_stats(region)
    await update.message.reply_text(
        f"📊 Статистика по региону {region}:
"
        f"Средняя цена: {stats['avg_price_per_sqm']}₽/м²
"
        f"Мин: {stats['min_price']}₽, Макс: {stats['max_price']}₽
"
        f"Объявлений в выборке: {stats['sample_size']}"
    )

# Запуск
def main():
    threading.Thread(target=dummy_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("role", role))
    app.add_handler(CommandHandler("add_task", add_task))
    app.add_handler(CommandHandler("tasks", show_tasks))
    app.add_handler(CommandHandler("kadastr", kadastr))
    app.add_handler(CommandHandler("market", market))
    print("🤖 Бот Altai.AI запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
