from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

BOT_TOKEN = "8360173852:AAFyU1VUZ9RpntjZeQC0cAiUJG8IJe4q6rU"  # Вставь сюда токен от @BotFather


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"👋 Привет, {user.first_name}!\n\n"
        f"🆔 *Твой ID:* `{user.id}`\n"
        f"👤 Имя: {user.full_name}\n"
        f"📛 Username: @{user.username or 'не указан'}\n\n"
        f"🔍 Используй /getid @username — чтобы узнать ID по юзернейму\n"
        f"📩 Или перешли мне сообщение от другого пользователя"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"📋 *Твоя информация:*\n\n"
        f"🆔 ID: `{user.id}`\n"
        f"👤 Имя: {user.full_name}\n"
        f"📛 Username: @{user.username or 'не указан'}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❗ Укажи юзернейм.\n\nПример: /getid @username"
        )
        return

    username = context.args[0].lstrip("@")

    try:
        chat = await context.bot.get_chat(f"@{username}")

        if chat.type == "private":
            text = (
                f"✅ *Пользователь найден:*\n\n"
                f"🆔 ID: `{chat.id}`\n"
                f"👤 Имя: {chat.full_name}\n"
                f"📛 Username: @{chat.username or 'не указан'}"
            )
        else:
            text = (
                f"✅ *Канал/группа найдена:*\n\n"
                f"🆔 ID: `{chat.id}`\n"
                f"📛 Название: {chat.title}\n"
                f"📂 Тип: {chat.type}\n"
                f"🔗 Username: @{chat.username or 'не указан'}"
            )

        await update.message.reply_text(text, parse_mode="Markdown")

    except BadRequest:
        await update.message.reply_text(
            f"❌ Пользователь @{username} не найден.\n\n"
            f"⚠️ Поиск по юзернейму работает только для:\n"
            f"• Публичных каналов и групп\n"
            f"• Пользователей, которые ранее писали этому боту"
        )


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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.forward_date:
        await handle_forward(update, context)
        return

    text = msg.text or ""
    if text.startswith("@"):
        context.args = [text]
        await get_id(update, context)
        return

    await update.message.reply_text(
        "📌 Доступные команды:\n\n"
        "/start — приветствие и твой ID\n"
        "/myid — твой ID\n"
        "/getid @username — узнать ID по юзернейму\n\n"
        "Или перешли сообщение от другого пользователя/канала."
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", my_id))
    app.add_handler(CommandHandler("getid", get_id))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
