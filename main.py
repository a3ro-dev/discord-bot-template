import subprocess
import sys
import os

# Python 3.10 or higher is required
if sys.version_info < (3, 10):
    print("You need at least Python 3.10.x to run this script")
    sys.exit(1)

# Check if requirements.txt exists
if not os.path.isfile('requirements.txt'):
    print("requirements.txt does not exist")
    sys.exit(1)

# Install required packages
print("Installing required packages...")
subprocess.run('pip install -r requirements.txt', shell=True)

import os
import discord
from discord.ext import commands
import config.configuration as cfg
import psutil
import random
import asyncio
from pretty_help import PrettyHelp
from difflib import get_close_matches

class Bot(commands.Bot):
    """
    A custom bot class that extends the `commands.Bot` class from the discord.py library.
    """

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(case_insensitive=True,
                         command_prefix=commands.when_mentioned_or(cfg.PREFIX),
                         intents=intents,
                         owner_ids=cfg.OWNERS,
                         help_command=PrettyHelp())

    # async def command_prefix(self, bot, message):
    #     prefixes = [cfg.PREFIX]  # List of possible prefixes
    
    #     for prefix in prefixes:
    #         if message.content.startswith(prefix):
    #             return prefix
    
    #     return cfg.PREFIX  # Default prefix

    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandNotFound):
    #         if callable(self.command_prefix):
    #             prefixes = list(self.command_prefix(self, ctx.message))  # Convert the coroutine object to a list
    #         else:
    #             prefixes = self.command_prefix()

    #         cmd = ctx.message.content
    #         for prefix in prefixes:
    #             cmd = cmd.replace(prefix, "")

    #         matches = get_close_matches(cmd, [command.name for command in self.commands])
    #         if matches:
    #             await ctx.send(f"Command not found, did you mean `{matches[0]}`?")
    #         else:
    #             await ctx.send("Command not found.")
    #     else:
    #         await super().on_command_error(ctx, error)

bot = Bot()

async def update_presence():
    while True:
        # Get memory usage and CPU usage
        memory_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent(interval=None)

        # Create the name list with the number of members in the guild at the 2nd index
        name = [
            f"Memory: {memory_usage:.1f}% | CPU: {cpu_usage:.1f}%",
            f"", #status 1
            f"", #status 2
            f"", #status 3
        ]

        # Set the presence with memory and CPU usage info
        await bot.change_presence(
            activity=discord.Streaming(
                name=random.choice(name),
                url="https://www.twitch.tv/",
            )
        )

        # Wait for 5 seconds before updating the presence again
        await asyncio.sleep(5)


@bot.event
async def on_ready():
    await bot.wait_until_ready()  # Wait until the bot is ready
    print(f'Logged in as {bot.user.name} | {bot.user.id}') # Print the bots name and ID #type: ignore
    print(f'Discord.py API version: {discord.__version__}')
    print(f'Successfully logged in and booted...!')
    await bot.load_extension('jishaku') # Load Jishaku
    print("Now loading cogs!")
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{file[:-3]}')
                print(f'Loaded {file[:-3]}')
            except Exception as e:
                print(f'Failed to load {file[:-3]} because: {str(e)}')
    await update_presence()


bot.run(cfg.TOKEN)
