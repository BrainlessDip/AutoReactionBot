import telebot
import asyncio
import os
import json
import aiofiles
from telebot import types
from telebot.async_telebot import *
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("token")
bot = AsyncTeleBot(token)

async def add_user(message):
  filename = f'database/user.json'
  async with aiofiles.open(filename, 'r') as f:
   users = json.loads(await f.read())
   if message.from_user.id not in users:
     users.append(message.from_user.id)
   async with aiofiles.open(filename, 'w') as f:
     await f.write(json.dumps(users))