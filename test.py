import json
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

img = Image.open("template.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("FC Subject.ttf", 60)
font2 = ImageFont.truetype("FC Subject.ttf", 65)
draw.text((390, 640),"Thanat Thappota",(255,255,255),font=font)
draw.text((1300, 640),"มัธยมศึกษาปีที่ 5/4",(255,255,255),font=font)
y = 1224
range_= 164
for i in range(5):
    draw.text((230, y + range_*i),"ภาษาไทย",(255,255,255),font=font2,anchor="lm")
    draw.text((1320, y + range_*i),"ท31101",(255,255,255),font=font2,anchor="mm")
    draw.text((1595, y + range_*i),"0.5",(255,255,255),font=font2,anchor="mm")
    draw.text((1865, y + range_*i),"89",(255,255,255),font=font2,anchor="mm")
    draw.text((2140, y + range_*i),"3",(255,255,255),font=font2,anchor="mm")
    print(y + range_*i)

draw.text((2140, 3030),"3.5",(255,255,255),font=font2,anchor="mm")
img.show()