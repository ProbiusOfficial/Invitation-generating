# -*- coding: utf-8 -*-

import os
import requests
from PIL import ImageFont, ImageDraw, Image, ImageOps
from flask import Flask, request, send_file
from io import BytesIO

app = Flask(__name__)



def delete_local_file(src):

    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_local_file(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass

# def crop_circle_avatar(img):
#     bigsize = (img.size[0] * 3, img.size[1] * 3)
#     mask = Image.new('L', bigsize, 0)
#     draw = ImageDraw.Draw(mask)
#     draw.ellipse((0, 0) + bigsize, fill=255)
#     mask = mask.resize(img.size, Image.ANTIALIAS)
#     img.putalpha(mask)
#     return img

def crop_circle_avatar(img):
    img = img.resize((240, 240), Image.ANTIALIAS)  # 将头像调整为 240x240 大小
    bigsize = (img.size[0] * 3, img.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(img.size, Image.ANTIALIAS)
    img.putalpha(mask)
    return img

@app.route('/')
def hello_world():
    return 'LitCTF2023_generate_invitation_API is running!'

@app.route('/generate_invitation', methods=['POST'])
def generate_invitation():
    if not request.json or 'name' not in request.json or 'imgurl' not in request.json:
        return "Error: Missing 'name' or 'imgurl' in request data.", 400

    name = request.json['name']
    imgurl = request.json['imgurl']

    response = requests.get(imgurl)
    avatar = Image.open(BytesIO(response.content)).convert("RGBA")
    avatar = crop_circle_avatar(avatar)

    img = Image.open("./source.jpg")

    # if len(name) > 15:
    #     return "Error: Name is too long!", 400

    # if len(name) <= 15:
    #     font_pil = ImageFont.truetype("src\STXINWEI.TTF", 90)
    #     draw = ImageDraw.Draw(img)
    #     width = (img.width - len(name) * 90) / 2 + 5
    #     height = (img.height) / 2 - 30
    #     draw.text((width, height), name, font=font_pil, fill=(255, 255, 255))
    # else:
    #     pygame.init()
    #     font = pygame.font.Font('src\STXINWEI.TTF', 90)
    #     font.set_bold(True)
    #     font.set_italic(True)
    #     ftext = font.render(name, True, (255, 255, 255))
    #     pygame.image.save(ftext, "/tmp/image.png")
    #     mark = Image.open("/tmp/image.png")
    #     layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    #     width = (img.width - mark.width) // 2
    #     height = (img.height) // 2 - mark.height - 10
    #     layer.paste(mark.rotate(5, expand=1), (width, height))
    #     img = Image.composite(layer, img, layer)
    #     delete_local_file("/tmp/image.png")

    # def get_text_width(name, font):
    #     width = 0
    #     for char in name:
    #         if ord(char) >= 128:  # 中文字符
    #             width += 90
    #         else:  # 英文字符
    #             width += 30
    #     return width

    def get_text_width(name, font):
        width = 0
        has_chinese = any(ord(char) >= 128 for char in name)
        
        for char in name:
            if ord(char) >= 128:  # 中文字符
                width += 90
            else:  # 英文字符
                if has_chinese:
                    width += 30
                else:
                    width += 45
        return width

    # if len(name) > 20:
    #     return "Error: Name is too long!", 400

    # font_pil = ImageFont.truetype("./FZXIANGSU12.TTF", 80)
    # draw = ImageDraw.Draw(img)
    # text_width = get_text_width(name, font_pil)
    # width = (img.width - text_width) / 2 + 5
    # height = (img.height) / 2 - 30
    # draw.text((width, height), name, font=font_pil, fill=(255, 255, 255))


    # img.paste(avatar, (((img.width) //2 - 118),((img.height) // 2 - 300)), avatar)

    # output_buffer = BytesIO()
    # img.save(output_buffer, format='JPEG')
    # output_buffer.seek(0)

    # return send_file(output_buffer, mimetype='image/jpeg', as_attachment=True, attachment_filename='invitation.jpg')
    if len(name) > 20:
        return "Error: Name is too long!", 400

    font_pil = ImageFont.truetype("./FZXIANGSU12.TTF", 80)
    draw = ImageDraw.Draw(img)
    x0, y0 = img.size
    ascent, descent = font_pil.getsize(name)
    text_width = get_text_width(name, font_pil)
    x = x0 / 2 - ascent / 2
    height = (img.height) / 2 - 30
    draw.text((x, height), name.encode('unicode_escape').decode('unicode_escape'), font=font_pil, fill=(255, 255, 255))

    img.paste(avatar, (((img.width) //2 - 118),((img.height) // 2 - 300)), avatar)

    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    output_buffer.seek(0)

    return send_file(output_buffer, mimetype='image/jpeg', as_attachment=True, attachment_filename='invitation.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

