# ai_processor.py
import base64
import io
import os
from PIL import Image
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_profession_image(image_stream, goal):
    """
    Image → Image using Gemini 3 Pro Image Preview
    with correct Part(text=...) and Part(inline_data=Blob)
    """

    # Load camera image
    input_img = Image.open(io.BytesIO(image_stream.getvalue()))

    # Convert to PNG bytes
    buf = io.BytesIO()
    input_img.save(buf, "PNG")
    img_bytes = buf.getvalue()

    # Correct image input format
    image_part = types.Part(
        inline_data=types.Blob(
            mime_type="image/png",
            data=img_bytes
        )
    )

    # Profession transformation prompt
    prompt = f"""
    Transform this SAME person into a future {goal} in India.

    PRESERVE:
    - facial identity exactly
    - beard, glasses, hairstyle
    - skin tone
    - age and gender

    CHANGE ONLY:
    - Clothing → authentic Indian {goal} outfit
    - Background → realistic Indian professional environment
    """

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=prompt),   # ✔ FIXED HERE
                image_part
            ]
        )
    ]

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(image_size="1K")
    )

    output_img_bytes = None

    # Stream model output
    for chunk in client.models.generate_content_stream(
        model="gemini-3.1-flash-image-preview",
        contents=contents,
        config=config
    ):
        if (
            chunk.candidates
            and chunk.candidates[0].content
            and chunk.candidates[0].content.parts
        ):
            part = chunk.candidates[0].content.parts[0]

            if part.inline_data and part.inline_data.data:
                output_img_bytes = part.inline_data.data

    if not output_img_bytes:
        raise Exception("Gemini did not return an image. Possibly quota or model issue.")

    # Convert to valid PNG
    final_img = Image.open(io.BytesIO(output_img_bytes))
    final_buf = io.BytesIO()
    final_img.save(final_buf, "PNG")

    return final_buf.getvalue()
