from importlib.metadata import files
import discord
from discord.ext import commands
from discord import app_commands
import json
from discord.ui import View, Select
from discord.app_commands import Choice
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from io import BytesIO
from discord.ui import View, Button , button
from ui.button import buttin
import math
import random
import time
from request_data import request

class command(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_app_command_completion(self,interaction, command):
            await self.statistic(command.name)

    async def statistic(self,func):
        with open("statistic.json", "r" ,encoding="utf8") as f:
            database = json.load(f)
        if database.get(func,None) == None:
            database[func] = {
                "times":1,
                "success": 0,
                "failure": 0
            }
        else:
            database[func]["times"] = database[func]["times"]+1

        with open("statistic.json", "w" ,encoding="utf8") as f:
            json.dump(database,f,ensure_ascii=False,indent=4)

    async def own_check(self,interaction:discord.Interaction,database):
        data:dict = database["owner"]
        owner = None
        if str(interaction.user.id) in data.keys():
            owner = data[str(interaction.user.id)]
        return owner

    @app_commands.command(name="getall_password",description="เพื่อเอารหัส")
    async def getall(self,interaction:discord.Interaction):
        await interaction.response.defer()
        with open("config.json", "r" ,encoding="utf8") as f:
            config = json.load(f)
        if str(interaction.user.id) not in config["dev"]:
            await interaction.followup.send("คำสั่งนี้ใช้ได้เฉพาะ Developer เท่านั้น",ephemeral=True)
            embed = discord.Embed(title = f"คำสั่งนี้ใช้ได้เฉพาะ Developer เท่านั้น",color = 0xEE2A2A,description="คำสั่งนี้ไม่อนุญาติให้บุคคลทั่วไปใช้") 
            embed.set_footer(icon_url=interaction.user.display_avatar.url,text=f'{interaction.user.display_name}#{interaction.user.discriminator}')
            await interaction.followup.send(embed=embed,ephemeral=True)
            return
        with open("student_data.json", "r" ,encoding="utf8") as f:
            database = json.load(f)
        data = database["studentdata"]
        lst = []
        for i in data:
            passw = i.split('-')
            lst.append(f"**code** : `{passw[0]}` **birth** : `{passw[1]}` **name** : `{data[i]['name-surname']}`")
        p = []
        page = math.ceil(len(lst)/10)
        for i in range(page):
            data = lst[0:10]
            line = ("\n--------------------------------\n").join(data)
            embed = discord.Embed(title = "Studentlist",color = 0x912FDC,description=line) 
            p.append(embed)
            del lst[0:10]
        view=buttin(p,300,interaction)
        await interaction.followup.send(embed = p[0],view=view)

    @app_commands.command(name="get_password",description="เพื่อเอารหัส")
    async def get_password(self,interaction:discord.Interaction):
        await interaction.response.defer()
        print("Initializing")
        start = time.time()
        re = request("student_data.json")
        database = re.request_access()
        data:dict = database["studentdata"]
        own = await self.own_check(interaction,database)
        if not own:
            if len(database["studentdata"].keys()) == len(database["owner"].keys()):
                embed = discord.Embed(title = f"รหัสถูกใช้ครบเเล้ว",
                                      color = 0xEE2A2A,
                                      description="ขออภัย ตอนนี้รหัสถูกใช้หมดเเล้วกรุณารอรอบทดสอบถัดไป") 
                embed.set_footer(icon_url=interaction.user.display_avatar.url,text=f'{interaction.user.display_name}#{interaction.user.discriminator}')
                await interaction.followup.send(embed=embed,ephemeral=True)
                return
            on = len(database["owner"].keys())
            own = list(database["studentdata"].keys())[on]
            database["owner"].update({
                str(interaction.user.id):own
            })
            data[own]["is_owned"] = True
        re.update_access(database)
        pas = own.split('-')
        embed = discord.Embed(title = f"รหัสผ่านของ {interaction.user.display_name}",
                              color = 0x912FDC,
                              description=f"**code** : `{pas[0]}` **birth** : `{pas[1]}` **name** : `{data[own]['name-surname']}`\n\nนำรหัสนี้ไปใช้กับคำสั่ง school-record ต่อไป")
        embed.set_footer(icon_url=interaction.user.display_avatar.url,text=f'{interaction.user.display_name}#{interaction.user.discriminator}')
        end = time.time()
        print(f"Get_password complete in {end-start}s")
        await interaction.followup.send(embed = embed,ephemeral=True)


    # #สร้างฟังชั่นดูข้อมูลส่วนตัว
    # @app_commands.command(name="ข้อมูลส่วนตัว",description="เพื่อดูข้อมูลส่วนตัวนักเรียน")
    # @app_commands.describe(
    #     รหัสประจำตัวนักเรียน="code",
    #     เลขบัตรประชาชน = "birth"
    # )
    # async def personal_information(self,interaction:discord.Interaction,รหัสประจำตัวนักเรียน:int,เลขบัตรประชาชน:int):
    #     await interaction.response.defer()
    #     student = str(รหัสประจำตัวนักเรียน) + "-" + str(เลขบัตรประชาชน)

    #     #เปิดไฟล์ข้อมูล
    #     with open("student_data.json", "r" ,encoding="utf8") as f:
    #         database = json.load(f)
    #     result = database["studentdata"].get(student)

    #     #ตรวจสอบว่ามีข้อมูลนร.หรือไม่
    #     if result:
    #         embed = discord.Embed(title="ข้อมูลส่วนตัว",color=0x03fcad)
    #         embed.set_thumbnail(url=result["face"])
    #         embed.add_field(name="ชื่อ-นามสกุล",value=f'`{result["name-surname"]}`',inline=True)
    #         embed.add_field(name="ชื่อเล่น",value=f'`{result["nickname"]}`',inline=True)
    #         embed.add_field(name="เพศ",value=f'`{result["gender"]}`',inline=True)
    #         embed.add_field(name="อายุ",value=f'`{result["age"]}`')
    #         embed.add_field(name="เกินวันที่",value=f'`{result["birthday"]}`')
    #         embed.add_field(name="สัญชาติ",value=f'`{result["nationality"]}`')
    #         embed.add_field(name="ศาสนา",value=f'`{result["region"]}`')
    #         embed.add_field(name="ที่อยู่",value=f'`{result["address"]}`')
    #         await interaction.followup.send(embed=embed)
    #     else:
    #         await interaction.followup.send("ไม่พบข้อมูลนักเรียนที่ระบุ")

    #ฟังชั่นในการหาตัวเลือกปี
    def get_optionlist(self,record):
        years = []     
        for term in record:
            option = discord.SelectOption(label=term,description=f"ผลการเรียนสำหรับปี {term}")
            years.append(option)
        return years

    def check_lenght(self,word,startpoint):
        font = ImageFont.truetype("FC Subject.ttf", 40)
        right = startpoint + font.getlength(word)
        i = 40
        while right > 680:
            font = ImageFont.truetype("FC Subject.ttf", i)
            i-=1
            right = startpoint + font.getlength(word)
        return font

    def image(self,data):
            font = ImageFont.truetype("FC Subject.ttf", 40)
            font2 = ImageFont.truetype("FC Subject.ttf", 30)
            record = data.get("school-record",None)
            y_ba = 612
            y_ad = 1104
            range_= 82
            f = []
            for term in record:
                img = Image.open("template.jpg")
                draw = ImageDraw.Draw(img)
                draw.text((195, 327),data.get("name-surname",None),(255,255,255),font=font)
                draw.text((607, 327),data.get("class",None),(255,255,255),font=font)
                draw.text((1040, 327),term,(255,255,255),font=font)
                for rec,i in zip(record[term]["basic"],range(len(record[term]["basic"]))):
                    font_s = self.check_lenght(record[term]["basic"][rec]["subject"],230)
                    ba = record[term]["basic"][rec]
                    draw.text((115 , y_ba + range_*i),ba["subject"],(255,255,255),font=font_s,anchor="lm")
                    draw.text((660, y_ba + range_*i),rec,(255,255,255),font=font2,anchor="mm")
                    draw.text((797, y_ba + range_*i),ba["weight"],(255,255,255),font=font2,anchor="mm")
                    draw.text((932, y_ba + range_*i),ba["get"],(255,255,255),font=font2,anchor="mm")
                    draw.text((1070, y_ba + range_*i),ba["grade"],(255,255,255),font=font2,anchor="mm")
                for rec,i in zip(record[term]["additional"],range(len(record[term]["additional"]))):
                    font_s = self.check_lenght(record[term]["additional"][rec]["subject"],230)
                    ad = record[term]["additional"][rec]
                    draw.text((115 , y_ad + range_*i),ad["subject"],(255,255,255),font=font_s,anchor="lm")
                    draw.text((660, y_ad + range_*i),rec,(255,255,255),font=font2,anchor="mm")
                    draw.text((797, y_ad + range_*i),ad["weight"],(255,255,255),font=font2,anchor="mm")
                    draw.text((932, y_ad + range_*i),ad["get"],(255,255,255),font=font2,anchor="mm")
                    draw.text((1070, y_ad + range_*i),ad["grade"],(255,255,255),font=font2,anchor="mm")

                draw.text((1070, 1515),record[term]["GPA"],(255,255,255),font=font2,anchor="mm")
                draw.text((1070, 1597),record[term]["GPAX"],(255,255,255),font=font2,anchor="mm")
                bytes = BytesIO()
                img.save(bytes,format="PNG")
                bytes.seek(0)
                f.append(bytes)
            return f 

    #สร้างฟังชั่นดูผลการเรียน
    @app_commands.command(name="school-record",description="to send School-record")
    @app_commands.describe(
        code="รหัสนักเรียน (ขอรหัสโดยใช้คำสั่ง /school-record) ",
        birthday = "วว/ดด/ปป (ขอรหัสโดยใช้คำสั่ง /school-record)"
    )
    async def school_record(self,interaction:discord.Interaction,code:str,birthday:str):
        await interaction.response.defer()
        print("Initializing")
        start = time.time()
        origin = interaction
        student = str(code) + "-" + str(birthday.replace("/",""))
        with open("student_data.json", "r" ,encoding="utf8") as f:
            database = json.load(f)
        data = database["studentdata"].get(student)
        if not data:
            embed = discord.Embed(title = f"ไม่พบข้อมูลนักเรียน",color = 0xEE2A2A,description="อาจเป็นเพราะรหัสผ่านหรือวันเกิดไม่ถูกต้อง ใช้คำสั่ง `get_password` เพื่อดูรหัส") 
            embed.set_footer(icon_url=interaction.user.display_avatar.url,text=f'{interaction.user.display_name}#{interaction.user.discriminator}')
            await interaction.followup.send(embed=embed,ephemeral=True)
            return
        if database["owner"].get(str(interaction.user.id)) != student:
            embed = discord.Embed(title = f"คุณไม่สามารถเข้าถึงรหัสนี้ได้",color = 0xEE2A2A,description="เนื่องจากรหัสนี้ไม่ใช่ของคุณ") 
            embed.set_footer(icon_url=interaction.user.display_avatar.url,text=f'{interaction.user.display_name}#{interaction.user.discriminator}')
            await interaction.followup.send(embed=embed,ephemeral=True)
            return
        f = self.image(data)
        select = Select(placeholder="เลือกภาคการศึกษา",
                        options=[discord.SelectOption(label = f"ชั้น {data['class']} ภาคเรียนที่ {term}",value=term) for term in data["school-record"]])
        but = Button(label="Form",style=discord.ButtonStyle.link,url="https://forms.gle/P7yBuB2C7pmu3RTw5")
        embed = discord.Embed(title = "ใบเเสดงผลการเรียน",color=0xe8994a)
        embed.add_field(name = "ชื่อ",value = f'`{data.get("name-surname")}`')
        embed.add_field(name ="ภาคเรียนที่",value = "`1`")
        embed.set_image(url=f"attachment://1.png")
        async def callback_(interaction:discord.Interaction):
            await interaction.response.defer()
            embed.set_field_at(index=1,name ="ภาคเรียนที่",value = f"`{select.values[0]}`")
            embed.set_image(url=f"attachment://{select.values[0]}.png")
            f[int(select.values[0])-1].seek(0)
            await em.edit(content='ใช้ได้15นาที',embed=embed,attachments=[discord.File(f[int(select.values[0])-1],filename=f"{select.values[0]}.png")])
        select.callback = callback_
        v = View(timeout=None)
        v.add_item(select)
        v.add_item(but)
        end = time.time()
        print(f"school-record complete in {end-start}s")
        em = await origin.followup.send(content='ใช้ได้15นาที',embed=embed,file=discord.File(f[0],filename="1.png"),view=v)

    @app_commands.command(name="เชิญ",description="ลิ้งสำหรับเชิญบอท")
    async def invitation(self,interaction:discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send("https://discord.com/api/oauth2/authorize?client_id=999337078934474752&permissions=8&scope=bot%20applications.commands")


async def setup(bot):
  await bot.add_cog(command(bot))