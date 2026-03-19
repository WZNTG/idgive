from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8360173852:AAFyU1VUZ9RpntjZeQC0cAiUJG8IJe4q6rU"  # Вставь сюда токен от @BotFather


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    text = (
        f"👋 Привет, {user.first_name}!\n\n"
        f"🤖 *ID этого бота:* `{context.bot.id}`\n"
        f"🆔 *Твой ID:* `{user.id}`\n"
        f"💬 *ID чата:* `{chat.id}`\n\n"
        f"Перешли мне сообщение от другого пользователя, чтобы узнать его ID!"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    bot = context.bot
    text = (
        f"📋 *Твоя информация:*\n\n"
        f"🆔 Твой ID: `{user.id}`\n"
        f"👤 Имя: {user.full_name}\n"
        f"📛 Username: @{user.username or 'не указан'}\n"
        f"💬 ID чата: `{chat.id}`\n\n"
        f"🤖 *Информация о боте:*\n"
        f"🆔 ID бота: `{bot.id}`\n"
        f"📛 Username бота: @{bot.username}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    text = (
        f"💬 *Информация о чате:*\n\n"
        f"🆔 ID чата: `{chat.id}`\n"
        f"📂 Тип: {chat.type}\n"
        f"📛 Название: {chat.title or 'личный чат'}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.forward_from:
        user = msg.forward_from
        tag = "🤖 Бот" if user.is_bot else "👤 Пользователь"
        text = (
            f"📋 *Пересланное сообщение:*\n\n"
            f"{tag}\n"
            f"🆔 ID: `{user.id}`\n"
            f"👤 Имя: {user.full_name}\n"
            f"📛 Username: @{user.username or 'не указан'}"
        )
        await msg.reply_text(text, parse_mode="Markdown")

    elif msg.forward_from_chat:
        chat = msg.forward_from_chat
        text = (
            f"📋 *Пересланный канал/группа:*\n\n"
            f"🆔 ID: `{chat.id}`\n"
            f"📛 Название: {chat.title}\n"
            f"📂 Тип: {chat.type}\n"
            f"🔗 Username: @{chat.username or 'не указан'}"
        )
        await msg.reply_text(text, parse_mode="Markdown")

    elif msg.forward_sender_name:
        text = (
            f"⚠️ Пользователь скрыл свой профиль.\n\n"
            f"👤 Имя: {msg.forward_sender_name}\n"
            f"🆔 ID: скрыт настройками приватности"
        )
        await msg.reply_text(text, parse_mode="Markdown")

    else:
        await msg.reply_text("❓ Не удалось определить отправителя.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.forward_date:
        await handle_forward(update, context)
    else:
        await update.message.reply_text(
            "📌 Доступные команды:\n\n"
            "/start — приветствие и ID\n"
            "/myid — твой ID и ID бота\n"
            "/chatid — ID текущего чата\n\n"
            "Или перешли сообщение от другого пользователя/канала, чтобы узнать его ID."
        )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", my_id))
    app.add_handler(CommandHandler("chatid", chat_id))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
