import telebot
import asyncio
import os
from telebot import types
from telebot.async_telebot import *
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("token")
bot = AsyncTeleBot(token)

async def send_help(message):
   text = """
To get started, follow these steps:

1. *Add me to your group as an admin:*
   - Use the "Add Me To Group" button.

2. *Setting up Auto Reactions:*
   - Explore various methods to trigger automatic reactions.

Let the fun begin! 🚀
*How To Set Up Auto Reaction ?:*
  - Set up auto reactions effortlessly by replying to a user's message with the command:
```
/auto_reaction ❤️
```"❤️" is the auto reaction.

*How To Remove Auto Reaction ?:*
  - Remove auto reactions effortlessly by replying to a user's message with the command:
```
/remove_ar 
```"ar" mean auto reaction.
/reactions to see available reaction
/view to see current auto reaction set up
   """
   keyboard = types.InlineKeyboardMarkup()
   add_button = types.InlineKeyboardButton(text="Add Me To Group", url="http://t.me/AutoReactionRoBot?startgroup=botstart")
   keyboard.add(add_button)
   await bot.reply_to(message,text,parse_mode="Markdown",reply_markup=keyboard)