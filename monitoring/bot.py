import logging

from functools import wraps

from config.config import settings
from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


from main import collect_data


# TODO: logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def restricted_access(func):
    """Allow access only for user/group ids from ALLOWED_USERS list"""
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
    await update.message.reply_text("Hello! I am Awesome Monitoring Bot. For more info on how to comfigure me use /help")


@restricted_access
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("List of command will be here")


@restricted_access
async def get_data_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Getting data from servers. This can take some time...')
    result_list = await collect_data()
    for message in result_list:
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)


async def get_data_scheduled(context: ContextTypes.DEFAULT_TYPE) -> None:
    result_list = await collect_data()
    for message in result_list:
        await context.bot.send_message(context.job.chat_id, text=message, parse_mode=ParseMode.HTML)


def get_job_name(chat_id):
    return f'{str(chat_id)}_scheduled'


def remove_job_if_exists(job_name, context: ContextTypes.DEFAULT_TYPE) -> bool:
    current_jobs_list = context.job_queue.get_jobs_by_name(job_name)
    if not current_jobs_list:
        return False
    for job in current_jobs_list:
        job.schedule_removal()
    return True


@restricted_access
async def set_scheduled_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    # chat_id is taken from current chat 
    # (can be user chat with bot or group, where bot is added)
    chat_id = update.effective_message.chat_id

    # default interval is taken from settings
    interval = int(settings.DEFAULT_CHECK_INTERVAL)
    try:
        if len(context.args) == 1:
            interval = float(context.args[0])
            if interval < 0:
                await update.effective_message.reply_text("Seconds must be positive number!")
                return
                    
        job_name = get_job_name(chat_id)
        removed_job = remove_job_if_exists(job_name, context)
        # job_kwargs={'misfire_grace_time': None} - is requred to fix schedule errors
        # sometimes schedule is late by some seconds, withput this param set to None it will not fire at all
        context.job_queue.run_repeating(callback=get_data_scheduled, 
                                        interval=interval, 
                                        chat_id=chat_id, 
                                        name=job_name, 
                                        data=interval, 
                                        job_kwargs={'misfire_grace_time': None})
        
        if removed_job:
            await update.effective_message.reply_text("Timer was updated! (already existed)")
        else:
            await update.effective_message.reply_text("New timer was set!")
            
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set [<seconds>]")


@restricted_access
async def get_current_shedules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    jobs = context.job_queue.jobs()
    if not jobs:
        await update.effective_message.reply_text('No scheduled messages found!')
        return
    text = 'List of scheduled jobs:'
    for job in jobs:
        text += f'\nJob {job.name} is run every {job.data} seconds in chat with ID {job.chat_id}'
    await update.effective_message.reply_text(text)


@restricted_access
async def unset_scheduled_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    chat_id = update.effective_message.chat_id

    job_name = get_job_name(chat_id)
    removed_job = remove_job_if_exists(job_name, context)

    if removed_job:
        await update.effective_message.reply_text("Timer was removed!")
    else:
        await update.effective_message.reply_text("No active timer was found!")


if __name__ == '__main__':
    print('Starting')
    app = Application.builder().token(settings.TELEGRAM_ACCESS_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start_command))  # to run async use block=False
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('getdata', get_data_command))
    app.add_handler(CommandHandler('set', set_scheduled_message))
    app.add_handler(CommandHandler('unset', unset_scheduled_message))
    app.add_handler(CommandHandler('getshedule', get_current_shedules))


    print('Polling')
    app.run_polling(poll_interval=3)