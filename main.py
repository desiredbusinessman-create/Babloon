import discord
from discord import app_commands
import json
import random
import os
# Initialize bot client with standard intents
intents = discord.Intents.default()
intents.message_content = True
class BabloonsBot(discord.Client):
def __init__(self):
super().__init__(intents=intents)
self.tree = app_commands.CommandTree(self)
async def setup_hook(self):
# Syncing commands globally. Note: Global sync can take up to an hour
to update everywhere.
await self.tree.sync()
bot = BabloonsBot()
DATA_FILE = "balances.json"
def load_data():
if not os.path.exists(DATA_FILE):
return {}
with open(DATA_FILE, "r") as f:
try:
return json.load(f)
except json.JSONDecodeError:
return {}
def save_data(data):
with open(DATA_FILE, "w") as f:
json.dump(data, f, indent=4)
def get_user_data(user_id, data):
uid = str(user_id)
if uid not in data:
data[uid] = {"wallet": 100, "bank": 0}
return data[uid]
@bot.event
async def on_ready():
print(f"Logged in as {bot.user} (ID: {bot.user.id})")
print("------")
