import telebot
import asyncio
import os
import aiofiles 
import json
import commands as command
from telebot import types
from telebot.async_telebot import *
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("token")
bot = AsyncTeleBot(token)
async def get_reaction(message,data,mode): 
   group_id = str(message.chat.id)
   filename = f'database/group_settings.json'
   async with aiofiles.open(filename, 'r') as f:
    group_settings = json.loads(await f.read())
   if group_id in group_settings:
     if mode == 1:
       reaction = group_settings[group_id]['username'][data]['reaction']
     else:
       reaction = group_settings[group_id]['user_id'][data]['reaction']
     return reaction
async def view_settings(message):
   group_id = str(message.chat.id)
   filename = f'database/group_settings.json'
   async with aiofiles.open(filename, 'r') as f:
    group_settings = json.loads(await f.read())
   text = "*Auto Reactions List*\n"
   if group_id in group_settings:
     for index,username in enumerate(group_settings[group_id]['username'],start=1):
       text += f"*[{index}]* @{username} {await get_reaction(message,username,mode=1)}\n"
     send = await bot.reply_to(message,"*Auto Reactions List*\n",parse_mode="Markdown")
     await bot.edit_message_text(text,message.chat.id,send.message_id,parse_mode="Markdown")
   else:
     send = await bot.reply_to(message,"*Ensure you set at least one auto reaction*\n",parse_mode="Markdown")
async def get_allowed_username(message,mode):
  group_id = str(message.chat.id)
  filename = f'database/group_settings.json'
  async with aiofiles.open(filename, 'r') as f:
   group_settings = json.loads(await f.read())
  if group_id not in group_settings:
    return []
  else:
    if mode == 1:
      allowed_username = ["@"+username for username in group_settings[group_id]['username']]
      return allowed_username
    else:
     allowed_user_id = [int(user_id) for user_id in group_settings[group_id]['user_id']]
     return allowed_user_id
async def add_auto_reaction(group_id:int,user_id:int,username:str,reaction:str):
  filename = f'database/group_settings.json'
  async with aiofiles.open(filename, 'r') as f:
   group_settings = json.loads(await f.read())
  if str(group_id) not in group_settings:
    group_settings[str(group_id)] = {"username":{},"user_id":{}}
  if username not in group_settings[str(group_id)]['username']:
    group_settings[str(group_id)]['username'] [username] = {"reaction": reaction}
  else:
    group_settings[str(group_id)]['username'][username] = {"reaction": reaction}
  if str(user_id) not in group_settings[str(group_id)]['user_id']:
    group_settings[str(group_id)]['user_id'] [str(user_id)] = {"reaction": reaction}
  else:
    group_settings[str(group_id)]['user_id'][str(user_id)]= {"reaction": reaction}
  async with aiofiles.open(filename, 'w') as f:
   await f.write(json.dumps(group_settings))
async def remove_auto_reaction_2(group_id:int,user_id:int,username:str):
  filename = f'database/group_settings.json'
  async with aiofiles.open(filename, 'r') as f:
   group_settings = json.loads(await f.read())
  if str(group_id) not in group_settings:
    group_settings[str(group_id)] = {"username":{},"user_id":{}}
  if username in group_settings[str(group_id)]['username']:
    del group_settings[str(group_id)]['username'][username]
  if str(user_id) in group_settings[str(group_id)]['user_id']:
    del group_settings[str(group_id)]['user_id'][str(user_id)]
    update = f"Auto Reaction Has Been Removed For @{username}"
    async with aiofiles.open(filename, 'w') as f:
      await f.write(json.dumps(group_settings))
  else:
    update = f"Auto Reaction Not Found For @{username}"
  return update
async def available_reactions(message):
   text = "Certainly! Here's a string of reaction emojis: 👍❤🔥🥰👏😁🤔🤯😱🤬😢🎉🤩🤮💩🙏👌🕊🤡🥱🥴😍🐳❤‍🔥🌚🌭💯🤣⚡🍌🏆💔🤨😐🍓🍾💋🖕😈😴😭🤓👻👨‍💻👀🎃🙈😇😨🤝✍🤗🫡🎅🎄☃💅🤪🗿🆒💘🙉🦄😘💊🙊😎👾🤷‍♂🤷🤷‍♀😡"
   await bot.reply_to(message,text,parse_mode="Markdown")



async def send_auto_reaction(message):
     reaction_emojis = ["👍", "👎", "❤", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂", "🤷", "🤷‍♀", "😡"]
     if message.reply_to_message is None:
       text = "*Reply To A User Text*\nExample: ``` /auto_reaction 🍌``` \n/reactions to see available reactions"
       await bot.reply_to(message,text,parse_mode="Markdown")
       return 0
     username = message.reply_to_message.from_user.username
     if username.lower().endswith('bot'):
       await bot.reply_to(message,"*Reply to a user message*\nExample: ``` /auto_reaction 🍌``` \n/reactions to see available reactions",parse_mode="Markdown")
       return 0
     try:
      reaction = message.text.split()[1]
     except:
       text = "*Don't Forgot To Specify a Reaction*\nExample: ``` /auto_reaction 🍌``` \n/reactions to see available reactions"
       await bot.reply_to(message,text,parse_mode="Markdown")
       return 0
     if reaction not in reaction_emojis:
       text = "*Use A Valid Reaction*\nExample: ``` /auto_reaction 🍌``` \n/reactions to see available reactions"
       await bot.reply_to(message,text,parse_mode="Markdown")
       return 0
     else:
       user_id = int(message.reply_to_message.from_user.id)
       username = message.reply_to_message.from_user.username
       await add_auto_reaction(message.chat.id,user_id,username,reaction)
       text = f"Auto Reaction Has Been Set For @{username} {reaction}"
       await bot.reply_to(message,text,parse_mode="Markdown")
       await command.send_new_reaction_alert(message,username,reaction)

async def remove_auto_reaction(message):
     if message.reply_to_message is None:
       text = "*Reply To A User Text*\nExample: ``` /remove_ar``` \n"
       await bot.reply_to(message,text,parse_mode="Markdown")
       return 0
     username = message.reply_to_message.from_user.username
     if username.lower().endswith('bot'):
       await bot.reply_to(message,"*Reply to a user message*\nExample: ``` /remove_ar```",parse_mode="Markdown")
       return 0
     else:
       user_id = int(message.reply_to_message.from_user.id)
       username = message.reply_to_message.from_user.username
       update = await remove_auto_reaction_2(message.chat.id,user_id,username)
       await bot.reply_to(message,update,parse_mode="Markdown")
       await command.send_remove_reaction_alert(message,username)