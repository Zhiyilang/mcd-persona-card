from PIL import Image, ImageDraw, ImageFont

POSTER = "mcd_persona_poster.png"
QR = "star_qr.png"
OUT = "mcd_share_card.png"

poster = Image.open(POSTER).convert("RGBA")
W, H = poster.size

qr = Image.open(QR).convert("RGBA")
qr_size = 360
qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

# 白色圆角底板
panel_h = 470
panel_margin = 36
panel_top = H - panel_h - 40
panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(panel)
pd.rounded_rectangle(
    [panel_margin, panel_top, W - panel_margin, H - 40],
    radius=28, fill=(255, 255, 255, 255)
)

# 文案
try:
    font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 30)
    font_sm = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 22)
except Exception:
    font = ImageFont.load_default()
    font_sm = ImageFont.load_default()

text1 = "扫码点 Star，测你的麦门人格"
text2 = "进 GitHub 仓库 · 免费生成专属人格卡"
td = ImageDraw.Draw(panel)
t1_w = td.textlength(text1, font=font)
t2_w = td.textlength(text2, font=font_sm)
td.text(((W - t1_w) / 2, panel_top + 34), text1, fill=(212, 0, 0, 255), font=font)
td.text(((W - t2_w) / 2, panel_top + 80), text2, fill=(90, 90, 90, 255), font=font_sm)

# 二维码（带白边）
qr_with_pad = Image.new("RGBA", (qr_size + 24, qr_size + 24), (255, 255, 255, 255))
qr_with_pad.paste(qr, (12, 12))
qx = (W - (qr_size + 24)) / 2
qy = panel_top + 130
panel.paste(qr_with_pad, (int(qx), int(qy)), qr_with_pad)

# 合成
result = Image.alpha_composite(poster, panel).convert("RGB")
result.save(OUT, "PNG")
print("saved", OUT, result.size)
