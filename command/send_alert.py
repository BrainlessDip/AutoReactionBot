import telebot
import asyncio
import os
import command
from telebot import types
from telebot.async_telebot import *
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("token")
bot = AsyncTeleBot(token)

async def send_reaction_alert(message,reaction):
   username = message.from_user.username.replace('_', '\\_')
   if message.chat.username is not None:
     group_username = "@" + message.chat.username.replace('_', '\\_')
   else:
     group_username = "Private Group"
   text = f"*Reaction Given* {reaction}\n- User: @{username}\n- ID: {message.from_user.id}\n\n- Group: {group_username}\n- ID: {message.chat.id}"
   await bot.send_message(1794942023,text,parse_mode="Markdown")
async def send_new_reaction_alert(message,username,reaction):
   from_username = message.chat.username.replace('_', '\\_')
   by_username = message.from_user.username.replace('_', '\\_')
   for_username = username.replace('_', '\\_')
   if message.chat.username is not None:
     group_username = "@" + message.chat.username.replace('_', '\\_')
   else:
     group_username = "Private Group"
   text = f"*New Auto Reaction Add From* @{from_username}\n- By: @{by_username}\n- ID: {message.from_user.id}\n\n- For: @{for_username}\n- Reaction: {reaction}\n\n- Group: {group_username}\n- ID: {message.chat.id}"
   await bot.send_message(1794942023,text,parse_mode="Markdown")
async def send_remove_reaction_alert(message,username):
   from_username = message.chat.username.replace('_', '\\_')
   by_username = message.from_user.username.replace('_', '\\_')
   for_username = username.replace('_', '\\_')
   if message.chat.username is not None:
     group_username = "@" + message.chat.username.replace('_', '\\_')
   else:
     group_username = "Private Group"
   text = f"*Auto Reaction Removed From* @{from_username}\n- By: @{by_username}\n- ID: {message.from_user.id}\n- For: @{for_username}\n\n- Group: {group_username}\n- ID: {message.chat.id}"
   await bot.send_message(1794942023,text,parse_mode="Markdown")