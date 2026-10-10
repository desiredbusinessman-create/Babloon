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
@bot.tree.command(name="balance", description="Check your Babloons wallet and
bank balance")
async def balance(interaction: discord.Interaction, member: discord.Member =
None):
target = member or interaction.user
data = load_data()
user_data = get_user_data(target.id, data)
embed = discord.Embed(title=f"{target.name}'s Wealth",
color=discord.Color.gold())
embed.add_field(name="👛 Wallet", value=f"{user_data['wallet']} Babloons",
inline=False)
embed.add_field(name="🏦 Bank", value=f"{user_data['bank']} Babloons",
inline=False)
embed.set_thumbnail(url=target.display_avatar.url)
await interaction.response.send_message(embed=embed)
@bot.tree.command(name="work", description="Work to earn some Babloons")
@app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.user.id))
async def work(interaction: discord.Interaction):
data = load_data()
user_data = get_user_data(interaction.user.id, data)
jobs = [
"cleaned out the server channels", "designed a custom emoji",
"moderated a rowdy voice chat", "wrote a Python script on iOS"
]
earnings = random.randint(20, 150)
job = random.choice(jobs)
user_data["wallet"] += earnings
save_data(data)
await interaction.response.send_message(
f"👷 You {job} and earned **{earnings} Babloons**!"
)
@work.error
async def work_error(interaction: discord.Interaction, error:
app_commands.AppCommandError):
if isinstance(error, app_commands.CommandOnCooldown):
await interaction.response.send_message(
f"⏳ Take a break! You can work again in **{error.retry_after:.1f}
s**.",
ephemeral=True
)
@bot.tree.command(name="coinflip", description="Flip a coin to double your bet
or lose it all")
async def coinflip(interaction: discord.Interaction, bet: int, choice: str):
if choice.lower() not in ["heads", "tails"]:
await interaction.response.send_message("Please pick either 'heads' or
'tails'!", ephemeral=True)
return
if bet <= 0:
await interaction.response.send_message("Bet must be a positive
integer!", ephemeral=True)
return
data = load_data()
user_data = get_user_data(interaction.user.id, data)
if user_data["wallet"] < bet:
await interaction.response.send_message("You don't have enough Babloons
in your wallet!", ephemeral=True)
return
result = random.choice(["heads", "tails"])
if choice.lower() == result:
user_data["wallet"] += bet
msg = f"🪙 The coin landed on **{result}**. You won **{bet}
Babloons**!"
else:
user_data["wallet"] -= bet
msg = f"🪙 The coin landed on **{result}**. You lost **{bet}
Babloons**."
save_data(data)
await interaction.response.send_message(msg)
@bot.tree.command(name="gamble_mines", description="Play Mines! Specify your
bet and the number of hidden bombs (1-24)")
async def gamble_mines(interaction: discord.Interaction, bet: int, bombs: int):
if bombs < 1 or bombs > 24:
await interaction.response.send_message("Bombs must be between 1 and
24!", ephemeral=True)
return
if bet <= 0:
await interaction.response.send_message("Bet must be greater than 0!",
ephemeral=True)
return
data = load_data()
user_data = get_user_data(interaction.user.id, data)
if user_data["wallet"] < bet:
await interaction.response.send_message("Insufficient funds in your
wallet!", ephemeral=True)
return
# Simulate a fast simplified Mines outcome based on risk multiplier
# Probability of survival for 1 click: (25 - bombs) / 25
success_chance = (25 - bombs) / 25
multiplier = round(1.5 * (25 / (25 - bombs)), 2)
if random.random() < success_chance:
winnings = int(bet * multiplier) - bet
user_data["wallet"] += winnings
await interaction.response.send_message(
f"💣 **Mines Game**: You avoided the {bombs} bomb(s)! 🎉
"
f"Multiplier: **{multiplier}x**
"
f"You won **{winnings} Babloons**!"
)
else:
user_data["wallet"] -= bet
await interaction.response.send_message(
f"💥 **BOOM!** You hit a mine. You lost your bet of **{bet}
Babloons**."
)
save_data(data)
# Replace with your actual token from the Developer Portal
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
if __name__ == "__main__":
if BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE":
print("Please replace YOUR_DISCORD_BOT_TOKEN_HERE with your actual bot
token.")
else:
bot.run(BOT_TOKEN)
