"""Rebuild files/share-card.png (the link-preview image) from files/photo.jpg.

Run from the project folder:  python tools/make_share_card.py
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
NAVY = (25, 50, 95)

card = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(card)
d.rectangle((0, 0, W, 10), fill=NAVY)
photo = Image.open('files/photo.jpg').convert('RGB').resize((400, 400), Image.LANCZOS)
mask = Image.new('L', (400, 400), 0)
ImageDraw.Draw(mask).ellipse((0, 0, 399, 399), fill=255)
px, py = 90, (H - 400) // 2 + 5
d.ellipse((px - 9, py - 9, px + 409, py + 409), outline=(160, 172, 194), width=2)
card.paste(photo, (px, py), mask)
name = ImageFont.truetype(r'C:\Windows\Fonts\georgiab.ttf', 66)
sub = ImageFont.truetype(r'C:\Windows\Fonts\georgia.ttf', 33)
small = ImageFont.truetype(r'C:\Windows\Fonts\georgia.ttf', 27)
x = 570
d.text((x, 232), 'Gabriel Devoto', font=name, fill=NAVY)
d.text((x, 325), 'Economist', font=sub, fill=(60, 60, 60))
d.text((x, 368), 'International Monetary Fund', font=sub, fill=(60, 60, 60))
d.line((x, 434, x + 80, 434), fill=NAVY, width=3)
d.text((x, 452), 'gabrieldevoto.com', font=small, fill=(110, 110, 110))
card.save('files/share-card.png', optimize=True)
print('Wrote files/share-card.png')
