from discord.ext import tasks, commands
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import logging

logger = logging.getLogger('discord.artichauds')
paris=ZoneInfo("Europe/Paris")
sortie = datetime(year=2024,month=3,day=8,tzinfo=paris)

class compteur_jour(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot=bot
        self.compteur.start()
        self.compteur

    def cog_unload(self):
        self.compteur.cancel()

    @tasks.loop(hours=1)
    async def compteur(self):
        logger.info("heure changé")
        now=datetime.now(tz=paris)
        ecart=sortie-now
        days=ecart.days
        hours=datetime.fromtimestamp(ecart.seconds,tz=paris).hour
        channel=self.bot.get_channel(1207644048588804096)
        await channel.edit(name=f"Sortie dans : {days}j {hours}h")
    
    @compteur.before_loop
    async def before_compteur(self):
        logger.info("attend")
        await self.bot.wait_until_ready()