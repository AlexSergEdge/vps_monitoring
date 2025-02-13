import logging

from functools import wraps

from core.config import settings
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from ssh.runner import run_client

settings.ALLOWED_USERS


def restricted_access(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if str(user_id) not in settings.ALLOWED_USERS:
            print(f'Unauthorized user tried to access bot: {user_id}')
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


@restricted_access
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("List of command will be here")

@restricted_access
async def get_data_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Just example call
    # result = await run_client('x.x.x.x', 22, 'root', '/path/to/key', 'ls /opt')
    # await update.message.reply_text(result)
    await update.message.reply_text('Test')


@restricted_access
async def send_data(data):
    bot = Bot(settings.TELEGRAM_ACCESS_TOKEN)
    await bot.send_message(chat_id = settings.TELEGRAM_CHAT_ID, text = data)


if __name__ == '__main__':
    print('Starting')
    app = Application.builder().token(settings.TELEGRAM_ACCESS_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('getdata', get_data_command))

    print('Polling')
    app.run_polling(poll_interval=3)