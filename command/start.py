import telebot
import asyncio
import os
from telebot import types
from telebot.async_telebot import *
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("token")
bot = AsyncTeleBot(token)

async def send_start(message):
   text = """
Welcome to Auto Reaction Bot! 🤖

🌟 *Features:*
- *Mention Reaction:* Experience instant reactions when mentioning a triggered user
- *Reply Trigger:* Set a specific user for automatic reply reactions

🔧 *Customize:*
- Desire personalized reactions? Simply let me know!

Begin chatting and enjoy the cascade of reactions! 🚀
/help ? 
   """
   keyboard = types.InlineKeyboardMarkup()
   join_button = types.InlineKeyboardButton(text="Join Support Chat", url="https://t.me/AutoReactionSupport")
   keyboard.add(join_button)
   await bot.reply_to(message,text,parse_mode="Markdown",reply_markup=keyboard)