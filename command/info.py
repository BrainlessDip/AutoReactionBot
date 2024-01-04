import telebot
import asyncio
import os
import time
import aiofiles
import json
from telebot import types
from telebot.async_telebot import *
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("token")
bot = AsyncTeleBot(token)
uptime_start = int(time.time())
async def count(mode):
  if mode == "groups":
   filename = f'database/group_settings.json'
   async with aiofiles.open(filename, 'r') as f:
    group_settings = json.loads(await f.read())
  else:
   filename = f'database/user.json'
   async with aiofiles.open(filename, 'r') as f:
    group_settings = json.loads(await f.read())
  return len(group_settings)
async def info(message):
   total_groups = await count("groups")
   total_user = await count("user")
   uptime_seconds = int(time.time() - uptime_start)
   days = uptime_seconds // (24 * 3600)
   hours = (uptime_seconds % (24 * 3600)) // 3600
   minutes = (uptime_seconds % 3600) // 60
   seconds = uptime_seconds % 60
   if days > 0:
     uptime_text = f"{days}d:{hours}h:{minutes}m:{seconds}s"
   else:
     uptime_text = f"{hours}h:{minutes}m:{seconds}s"
   txt = f"*Bot Name:* Auto Reaction Bot\nUptime: *{uptime_text}*\n\n*Total User:* {total_user}\n*Total Groups:* {total_groups}\n\n*Support Group:* @AutoReactionSupport\n*Developer:* @DipDey\nMade With ❤️ By @PROJECTX69"
   if message.chat.type == "private":
    await bot.send_message(message.chat.id,txt,parse_mode="Markdown")
   else:
     await bot.reply_to(message,txt,parse_mode="Markdown")