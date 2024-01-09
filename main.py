import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

#สร้างตัว BOT
class smd1(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(intents=intents,command_prefix="&",help_command=None,application_id=999337078934474752)

    async def setup_hook(self):
        #โหลด Cogs ทั้งหมด
        for filename in os.listdir('./cogs'):
         if filename.endswith('.py') and not filename.startswith("_"):
           await bot.load_extension(f'cogs.{filename[:-3]}')
        await self.tree.sync() 

bot = smd1()

#เเจ้งเตือนเมื่อบอทออนไลน์
@bot.event                              
async def on_ready():
      print('-------------------------------')
      print(f"{bot.user} is Ready")
      print('-------------------------------')

bot.run("OTk5MzM3MDc4OTM0NDc0NzUy.Gichke.u969yCLv0PcJWJH8jxhx8OhCM-gZhG-PCnoziM")