from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def add_watermark(photo):
    base = Image.open(photo.image.path)
    width, height = base.size

    # 透かしの設定
    watermark = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark, 'RGBA')
    
    # 透かしのテキストと位置
    text = "© Your Name"
    font = ImageFont.truetype('path/to/font.ttf', 36)  # フォントのパスを指定
    textwidth, textheight = draw.textsize(text, font)
    draw.text((width - textwidth - 10, height - textheight - 10), text, fill=(255, 255, 255, 128), font=font)

    # 透かしを追加
    watermarked = Image.alpha_composite(base.convert('RGBA'), watermark)

    # 透かし付き画像を保存
    watermarked_path = f"watermarked_photos/{photo.id}_watermarked.jpg"
    watermarked.save(f"media/{watermarked_path}")

    # モデルのフィールドに保存したパスを設定
    photo.image_with_watermark = watermarked_path
    photo.save()