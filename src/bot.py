import logging
import os
from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHANNEL_ID=os.getenv("CHANNEL_ID")

# Define conversation states
ADD_POST_CONTENT, ADD_MESSAGE_ADDRESS, ADD_WEBSITE, CONFIRM = range(4)


async def start(update, context):
    await update.message.reply_text("Please add the post content:")
    return ADD_POST_CONTENT

async def handle_add_post_content(update, context):
    context.chat_data['post_content'] = update.message
    await update.message.reply_text("Please enter telegram username where a people can message you.")
    return ADD_MESSAGE_ADDRESS

async def handle_add_message_address(update, context):
    username = update.message.text
    context.chat_data['message_address'] = username
    await update.message.reply_text("Please enter a website url https://www.--- format:")
    return ADD_WEBSITE

async def handle_add_website_url(update, context):
    url = update.message.text
    context.chat_data['website_url'] = url
    await update.message.reply_text("Here's what the post look like with the buttons")

    post_content = context.chat_data.get('post_content')
    message_address = context.chat_data.get('message_address')
    website_url = context.chat_data.get('website_url')

    message_keyboard = InlineKeyboardButton('✍️  Message Us', url=f"https://t.me/{message_address}")
    website_keyboard = InlineKeyboardButton('🌐 Website', url=website_url)
    reply_markup = InlineKeyboardMarkup([[message_keyboard, website_keyboard]])

    if post_content.text:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=post_content.text, parse_mode="HTML", reply_markup=reply_markup)
    if post_content.photo:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=post_content.photo[-1].file_id, caption=post_content.caption,parse_mode="HTML", reply_markup=reply_markup)
    if post_content.video:
        await context.bot.send_video(chat_id=update.effective_chat.id, video=post_content.video.file_id, caption=post_content.caption, parse_mode="HTML", reply_markup=reply_markup)

    approve_keyboard = InlineKeyboardButton('Approve Post', callback_data="yes")
    decline_keyboard = InlineKeyboardButton('Decline Post', callback_data="no")
    confirmation_markup  = InlineKeyboardMarkup([[approve_keyboard, decline_keyboard]])

    await update.message.reply_text("Do you want to publish the post?", parse_mode="HTML", reply_markup=confirmation_markup)

    return CONFIRM

# Handle the callback from InlineKeyboardButtons
async def button_callback(update, context):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "yes":
        # User confirmed, proceed with posting
        await post_message(update, context)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Post sent successfully.', parse_mode="HTML")
    else:
        # User declined, cancel the post
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Post canceled.', parse_mode="HTML")
    # Reset chat data
    context.chat_data.pop('post_content', None)
    context.chat_data.pop('website_url', None)
    context.chat_data.pop('message_address', None)

    return ConversationHandler.END

async def cancel(update, context):

    await update.message.reply_text("use /start command to create a new post.")
    # Reset chat data
    context.chat_data.pop('post_content', None)
    context.chat_data.pop('website_url', None)
    context.chat_data.pop('message_address', None)

    return ConversationHandler.END

async def handle_posting(update, context):
    choice = update.message.text.lower()
    if choice == "yes":
        # User confirmed, proceed with posting
        await post_message(update, context)
        await update.message.reply_text('Post sent successfully.')
    else:
        # User declined, cancel the post
        await update.message.reply_text("Post canceled." )
    # Reset chat data
    context.chat_data.pop('post_content', None)
    context.chat_data.pop('website_url', None)
    context.chat_data.pop('message_address', None)

    return ConversationHandler.END


async def post_message(update, context):
    post_content = context.chat_data.get('post_content')
    message_address = context.chat_data.get('message_address')
    website_url = context.chat_data.get('website_url')

    message_keyboard = InlineKeyboardButton('✍️  Message Us', url=f"https://t.me/{message_address}")
    website_keyboard = InlineKeyboardButton('🌐 Website', url=website_url)
    reply_markup = InlineKeyboardMarkup([[message_keyboard, website_keyboard]])

    channel_id = CHANNEL_ID
    try:
        if post_content.text:
            await context.bot.send_message(chat_id=channel_id, text=post_content.text, parse_mode="HTML", reply_markup=reply_markup)
        if post_content.photo:
            await context.bot.send_photo(chat_id=channel_id, photo=post_content.photo[-1].file_id, caption=post_content.caption, parse_mode="HTML", reply_markup=reply_markup)
        if post_content.video:
            await context.bot.send_video(chat_id=channel_id, video=post_content.video.file_id, caption=post_content.caption, parse_mode="HTML", reply_markup=reply_markup)

    except TelegramError as e:
        await update.message.reply_text("Sorry I'm unable to post the message.")
        print(e)

def main():
    application = Application.builder().token(BOT_TOKEN or '').build()
    CallbackQueryHandler(button_callback)
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states= {
            ADD_POST_CONTENT:[MessageHandler(filters.ALL, handle_add_post_content)],
            ADD_WEBSITE:[MessageHandler(filters.TEXT, handle_add_website_url  )],
            ADD_MESSAGE_ADDRESS:[MessageHandler(filters.TEXT,handle_add_message_address )],
            CONFIRM:[CallbackQueryHandler(button_callback)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    #Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
