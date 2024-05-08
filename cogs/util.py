import discord
from discord.ext import commands
from discord.ui import Button, View
import platform
import datetime

class Util(commands.Cog):
    """
    A utility class that provides various commands for checking bot's latency, uptime, and system information.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=['p'], brief="Ping command", help="Check the bot's latency.")
    async def ping(self, ctx):
        """
        Check the bot's latency.
        """
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency: {latency}ms")

    @commands.hybrid_command(aliases=['u'], brief="Uptime command", help="Check the bot's uptime.")
    async def uptime(self, ctx):
        """
        Check the bot's uptime.
        """
        uptime = datetime.datetime.utcnow() - self.bot.start_time
        await ctx.send(f"Uptime: {uptime}")

    @commands.hybrid_command(aliases=['si'], brief="System information command", help="Get system information.")
    async def sysinfo(self, ctx):
        """
        Get system information.
        """
        embed = discord.Embed(title="System Information", color=discord.Color.blue())
        embed.add_field(name="Discord.py Version", value=discord.__version__)
        embed.add_field(name="Python Version", value=platform.python_version())
        embed.add_field(name="System", value=platform.system())
        embed.add_field(name="Processor", value=platform.processor())
        embed.set_footer(text="Powered by Discord.py")

        # Create a button
        button = Button(label="🖤", style=discord.ButtonStyle.primary, custom_id="my_button")

        # Create a view and add the button
        view = View()
        view.add_item(button)

        # Send the initial message with the view
        message = await ctx.send(embed=embed, view=view)

        # Wait for the button to be clicked
        interaction = await self.bot.wait_for("button_click", check=lambda i: i.custom_id == "my_button")

        # Send an ephemeral response when the button is clicked
        await interaction.response.send_message("Button pressed!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Util(bot))
