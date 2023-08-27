import asyncio 
import discord 
from discord.ext import  commands 
from discord import  app_commands,ButtonStyle 
from discord.app_commands import locale_str as _t
from discord.ui import * 
import random 
import os
from .checks import check

class reboot(commands.Cog): 
    def __init__(self,bot:commands.Bot) -> None: 
        self.bot = bot 

    @app_commands.command(
        name=_t(
            "reboot",
            fr="redémmarage",
            en="restart"
        ),
        description=_t(
            "description",
            fr="redémarre le bot et le mets a jour",
            en="restart the bot and update it"
        ),
    )
    @check.is_SonHaon()
    async def reboot(self,interaction:discord.Interaction):
        await self.bot.change_presence(status=discord.Status.offline)
        await interaction.response.send_message("le bot va redémarrer",ephemeral=True)
        os.system("sudo systemctl restart botarchauds.service")
        