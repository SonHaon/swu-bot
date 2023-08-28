import asyncio
from io import BytesIO 
import discord 
from discord.ext import  commands 
from discord.app_commands import locale_str as _t
from discord import  app_commands,ButtonStyle 
from discord.ui import * 
from PIL import Image, ImageDraw,ImageFont
import os
import random 
import logging
logger = logging.getLogger('discord.artichauds') 
from .fonction import image_bienvenue

async def embed_fr(bot,member:discord.Member):
    embed = discord.Embed(
            title=f"Bienvenue {member.guild.name}",
            description=f"Hello {member.mention}, Bienvenue sur Star Wars : Unlimited FR !\nCe discord a été créé pour regrouper le plus de joueurs francophone possibles pour partager autour du jeu.\nCommence par un petit tour sur #règles et mets une petite ✅ pour les accepter.\nTu trouveras dans #ressources ce qu’il te faut pour jouer en PnP ou en ligne.\nN’hésites pas à te présenter la suite de ce message 🙂",
            color=discord.Color.darker_grey())
    embed.set_image(url= await image_bienvenue(bot,member))
    return embed


class member_join(commands.Cog): 
    def __init__(self,bot:commands.Bot) -> None: 
        self.bot = bot 

    @commands.Cog.listener(name="on_member_join")
    async def timeout(self,member:discord.Member):
        channel = member.guild.get_channel(934114546304553012)
        if member.id == 931236217465471066:
            channel = member.guild.get_channel(934114546304553012)
        embed = await embed_fr(self.bot,member)
        await channel.send(member.mention,embed=embed)
        await asyncio.sleep(2)
        os.remove(f"/home/sonhaon/swu-bot/{member.name}.png")