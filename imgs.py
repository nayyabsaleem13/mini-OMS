import base64
from PIL import Image
import os
from io import BytesIO

def convert_to_webp(b64_string):
    img_data = base64.b64decode(b64_string)
    img = Image.open(BytesIO(img_data)).convert("RGB")
    temp_path = "temp1.webp"
    img.save(temp_path, "WEBP")
    return temp_path

def resize_image(input_path, size=(600, 600)):
    img = Image.open(input_path)
    resized = img.resize(size)
    temp_path = "temp2.webp"
    resized.save(temp_path, "WEBP")
    return temp_path

def compress_img(input_path, max_size_kb=100):
    img = Image.open(input_path)
    quality = 95
    temp_path = "final.webp"
    while quality > 5:
        img.save(temp_path, "WEBP", quality=quality)
        if os.path.getsize(temp_path) / 1024 <= max_size_kb:
            return temp_path
        quality -= 5
    img.save(temp_path, "WEBP", quality=quality)
    return temp_path

def final_converter(b64_string):
    step1 = convert_to_webp(b64_string)
    step2 = resize_image(step1)
    final = compress_img(step2)

    for f in [step1, step2]:
        if os.path.exists(f):
            os.remove(f)

    Image.open(final).show()

    with open(final, "rb") as f:
        final_b64 = base64.b64encode(f.read()).decode("utf-8")

    os.remove(final)
    return final_b64

if __name__ == "__main__":
    with open("input.jpg", "rb") as f: 
        b64_string = base64.b64encode(f.read()).decode("utf-8")

    result_b64 = final_converter(b64_string)
