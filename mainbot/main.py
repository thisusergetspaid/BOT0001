import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from brain import Brain
from config import load_settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Project0001 online.\n\n"
        "Send me a text message and I will reply.\n"
        "Commands:\n"
        "/start - show this message\n"
        "/reset - clear conversation memory"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    brain: Brain = context.application.bot_data["brain"]
    brain.reset(update.effective_chat.id)
    await update.message.reply_text("Conversation memory cleared.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    brain: Brain = context.application.bot_data["brain"]
    chat_id = update.effective_chat.id
    user_text = update.message.text.strip()

    if not user_text:
        await update.message.reply_text("Send a text message and I will respond.")
        return

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        reply = await brain.respond(chat_id, user_text)
        await update.message.reply_text(reply.text)
    except Exception:
        logger.exception("Failed to generate reply for chat %s", chat_id)
        await update.message.reply_text(
            "Something went wrong while generating a reply. Please try again."
        )


def main() -> None:
    settings = load_settings()
    brain = Brain(api_key=settings.openai_api_key, model=settings.openai_model)

    app = (
        Application.builder()
        .token(settings.telegram_bot_token)
        .build()
    )
    app.bot_data["brain"] = brain

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Starting Project0001 Telegram bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
