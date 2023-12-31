import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import locale_str as _t
from discord.ui import *
import random
import os
from io import BytesIO
from PIL import Image,ImageFont,ImageDraw,ImageOps
import logging

logger = logging.getLogger('discord.artichauds')

class ping(commands.Cog):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name=_t(
            "ping",
            fr="ping",
            en="ping"
        ),
        description=_t(
            "description",
            fr="verifie si le bot marche",
            en="check if the bot works"
        )
    )
    async def ping(self,interaction:discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.edit_original_response(content=f"le ping du bot est de {round(self.bot.latency*1000)}ms")
