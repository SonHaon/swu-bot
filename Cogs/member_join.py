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
            description=f"Hello {member.mention}, Bienvenue sur **{member.guild.name}** !\nCe discord a été créé pour regrouper le plus de joueurs francophones possibles pour partager autour du jeu.\nCommence par un petit tour sur #règles et mets une petite ✅ pour les accepter.\nTu trouveras dans #ressources ce qu’il te faut pour jouer en PnP ou en ligne.\nN’hésites pas à te présenter la suite de ce message 🙂",
            color=discord.Color.darker_grey())
    embed2=discord.Embed(description=" ")
    embed2.set_image(url= await image_bienvenue(bot,member))
    return [embed,embed2]


class member_join(commands.Cog): 
    def __init__(self,bot:commands.Bot) -> None: 
        self.bot = bot 

    @commands.Cog.listener(name="on_member_join")
    async def timeout(self,member:discord.Member):
        channel = member.guild.get_channel(934114546304553012)
        if member.id == 931236217465471066:
            channel = member.guild.get_channel(934114546304553012)
        embeds = await embed_fr(self.bot,member)
        await channel.send(member.mention,embeds=embeds)
        await asyncio.sleep(2)
        os.remove(f"/home/sonhaon/swu-bot/{member.name}.png")