import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter


def Random_color():#生成随机颜色
    return (random.randint(32,127),random.randint(32,127),random.randint(32,127))

def generate_text():#生成四位随机验证码
    return ''.join(random.sample(string.ascii_letters+string.digits,4))

def draw_line(draw,numbel,width,heigth):#下划线
    for temp in range(numbel):
        x1 =random.randint(0,width/2)
        y1 =random.randint(0,heigth/2)
        x2 =random.randint(0,width)
        y2 =random.randint(heigth/2,heigth)
        draw.line(((x1,y1),(x2,y2)),fill='black',width=1)

def get_verify_code():#生成验证码图片
    code =generate_text()
    width,height =120,50
    CodeIMG =Image.new("RGB",(width,height),"white")
    font =ImageFont.truetype("/home/yzy/recreatingProject/apps/static/Arial.ttf",40)
    draw =ImageDraw.Draw(CodeIMG)
    for it in range(4):
        draw.text((5+random.randint(-3,3)+23*it, 5+random.randint(-3,3)),
                  text=code[it], fill=Random_color(),font=font )
    draw_line(draw,2,width,height)
    CodeIMG =CodeIMG.filter(ImageFilter.GaussianBlur(radius=1.0))#模糊处理

    return CodeIMG,code
