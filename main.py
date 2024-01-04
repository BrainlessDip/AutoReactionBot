import telebot
import asyncio
import os
import commands as command
import admin
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from keep_alive import keep_alive
load_dotenv()
token = os.getenv("token")
bot = AsyncTeleBot(token)
# Start Command
@bot.message_handler(commands=['start'])
async def send_message(message):
  await command.send_start(message)
  if message.chat.type == "private":
    await admin.add_user(message)
# Help Command
@bot.message_handler(commands=['help'])
async def send_message(message):
  await command.send_help(message)
# Info Command
@bot.message_handler(commands=['info'])
async def send_message(message):
  await command.info(message)
# View Command
@bot.message_handler(commands=['view','v'])
async def send_message(message):
   if message.chat.type == "private":
     await bot.reply_to(message,f"*This Command Is Only For Group Chat*",parse_mode="MarkdownV2")
   else:
     admins = await bot.get_chat_administrators(message.chat.id)
     admin_ids = [admin.user.id for admin in admins]
     if message.from_user.id not in admin_ids:
       text = f"*You Don't Have Administration Permission*"
       await bot.reply_to(message,text,parse_mode='MarkdownV2')
     else:
       await command.view_settings(message)
# Available Reactions Command
@bot.message_handler(commands=['reactions'])
async def send_message(message):
  await command.available_reactions(message)
# Auto Reaction Command
@bot.message_handler(commands=['auto_reaction','ar'])
async def send_message(message):
   if message.chat.type == "private":
     await bot.reply_to(message,f"*This Command Is Only For Group Chat*",parse_mode="MarkdownV2")
     return 0
   admins = await bot.get_chat_administrators(message.chat.id)
   admin_ids = [admin.user.id for admin in admins]
   if message.from_user.id not in admin_ids:
     text = f"*You Don't Have Administration Permission*"
     await bot.reply_to(message,text,parse_mode='MarkdownV2')
   else:
    await command.send_auto_reaction(message)
# Auto Reaction Command
@bot.message_handler(commands=['remove_ar'])
async def send_message(message):
   if message.chat.type == "private":
     await bot.reply_to(message,f"*This Command Is Only For Group Chat*",parse_mode="MarkdownV2")
     return 0
   admins = await bot.get_chat_administrators(message.chat.id)
   admin_ids = [admin.user.id for admin in admins]
   if message.from_user.id not in admin_ids:
     text = f"*You Don't Have Administration Permission*"
     await bot.reply_to(message,text,parse_mode='MarkdownV2')
   else:
     await command.remove_auto_reaction(message)
 
@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
    'text', 'location', 'contact', 'sticker'])
async def get_text(message):
   allowed = await command.get_allowed_username(message,mode=1)
   allowed_id = await command.get_allowed_username(message,mode=2)
   triggered_username = None
   if message.content_type == "text":
     for username in allowed:
      if username in message.text:
        triggered_username = username
        break
   if triggered_username is not None:
    reaction = await command.get_reaction(message,triggered_username[1:],mode=1)
    await bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji(reaction)])
    await command.send_reaction_alert(message,reaction)
   else:
     if message.reply_to_message is not None:
       reply_from_id = int(message.reply_to_message.from_user.id)
       if reply_from_id in allowed_id:
         reaction = await command.get_reaction(message,str(reply_from_id),mode=2)
         await bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji(reaction)])
         await command.send_reaction_alert(message,reaction)
print("BOT IS RUNNING..")
if __name__ == "__main__":
   keep_alive()
   asyncio.run(bot.polling(non_stop=True))