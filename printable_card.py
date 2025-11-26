# printable_card.py
from PIL import Image, ImageDraw, ImageFont
import io

A4_WIDTH_PX = 2480   # 8.27 inch × 300 DPI
A4_HEIGHT_PX = 3508  # 11.69 inch × 300 DPI


def generate_printable_card(name, school, goal, captured_img, ai_img, logo_file):
    """
    Build a high-quality A4 printable card.
    - name (str)
    - school (str)
    - goal (str)
    - captured_img (PIL Image)
    - ai_img (PIL Image)
    - logo_file (file-like bytes)  <-- Robokalam logo
    """

    # ---------------------------------------------
    # 1. Create A4 canvas (white background)
    # ---------------------------------------------
    card = Image.new("RGB", (A4_WIDTH_PX, A4_HEIGHT_PX), "white")
    draw = ImageDraw.Draw(card)

    # ---------------------------------------------
    # 2. Load Robokalam logo (file-like object)
    # ---------------------------------------------
    logo_file.seek(0)
    logo = Image.open(logo_file).convert("RGBA")

    # Resize logo
    logo_w = 600
    logo_ratio = logo_w / logo.width
    logo_h = int(logo.height * logo_ratio)
    logo = logo.resize((logo_w, logo_h))

    # Paste logo top-center
    card.paste(logo, ((A4_WIDTH_PX - logo_w)//2, 80), logo)


    # ---------------------------------------------
    # 3. Title Text
    # ---------------------------------------------
    try:
        font_title = ImageFont.truetype("arial.ttf", 80)
        font_sub = ImageFont.truetype("arial.ttf", 50)
        font_body = ImageFont.truetype("arial.ttf", 60)
    except:
        # fallback fonts
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_body = ImageFont.load_default()

    title_y = logo_h + 150
    title_text = "Future Goal Profile"
    draw.text(
        ((A4_WIDTH_PX - draw.textlength(title_text, font=font_title)) // 2,
         title_y),
        title_text,
        fill="black",
        font=font_title
    )

    # ---------------------------------------------
    # 4. Student Details Section
    # ---------------------------------------------
    detail_y = title_y + 180

    draw.text((200, detail_y), f"Name : {name}", fill="black", font=font_body)
    draw.text((200, detail_y + 100), f"School: {school}", fill="black", font=font_body)
    draw.text((200, detail_y + 200), f"Future Goal: {goal}", fill="black", font=font_body)


    # ---------------------------------------------
    # 5. Insert Captured Image & AI Image
    # ---------------------------------------------
    # Resize both images
    img_w = 900
    ratio1 = img_w / captured_img.width
    ratio2 = img_w / ai_img.width

    cap_h = int(captured_img.height * ratio1)
    ai_h = int(ai_img.height * ratio2)

    captured_resized = captured_img.resize((img_w, cap_h))
    ai_resized = ai_img.resize((img_w, ai_h))

    # Left photo (captured)
    cap_x = 200
    cap_y = detail_y + 400
    card.paste(captured_resized, (cap_x, cap_y))

    draw.text((cap_x, cap_y + cap_h + 20),
              "Captured Photo", fill="black", font=font_sub)

    # Right photo (AI Future)
    ai_x = A4_WIDTH_PX - img_w - 200
    ai_y = detail_y + 400
    card.paste(ai_resized, (ai_x, ai_y))

    draw.text((ai_x, ai_y + ai_h + 20),
              f"Future {goal}", fill="black", font=font_sub)


    # ---------------------------------------------
    # 6. Save to BytesIO (PNG)
    # ---------------------------------------------
    out = io.BytesIO()
    card.save(out, format="PNG", dpi=(300, 300))
    out.seek(0)

    return Image.open(out)
