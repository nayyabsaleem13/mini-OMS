# import base64
# # from PIL import Image
# import os
# from io import BytesIO

# def convert_to_webp(b64_string):
#     img_data = base64.b64decode(b64_string)
#     # img = Image.open(BytesIO(img_data)).convert("RGB")
#     temp_path = "temp1.webp"
#     img.save(temp_path, "WEBP")
#     return temp_path

# def resize_image(input_path, size=(600, 600)):
#     img = Image.open(input_path)
#     resized = img.resize(size)
#     temp_path = "temp2.webp"
#     resized.save(temp_path, "WEBP")
#     return temp_path

# def compress_img(input_path, max_size_kb=100):
#     img = Image.open(input_path)
#     quality = 95
#     temp_path = "final.webp"
#     while quality > 5:
#         img.save(temp_path, "WEBP", quality=quality)
#         if os.path.getsize(temp_path) / 1024 <= max_size_kb:
#             return temp_path
#         quality -= 5
#     img.save(temp_path, "WEBP", quality=quality)
#     return temp_path

# def final_converter(b64_string):
#     step1 = convert_to_webp(b64_string)
#     step2 = resize_image(step1)
#     final = compress_img(step2)

#     for f in [step1, step2]:
#         if os.path.exists(f):
#             os.remove(f)

#     Image.open(final).show()

#     with open(final, "rb") as f:
#         final_b64 = base64.b64encode(f.read()).decode("utf-8")

#     os.remove(final)
#     return final_b64

# if __name__ == "__main__":
#     with open("input.jpg", "rb") as f: 
#         b64_string = base64.b64encode(f.read()).decode("utf-8")

#     result_b64 = final_converter(b64_string)





# import base64
# from io import BytesIO
# # from PIL import Image, ImageOps

# class Thumbnail:
#     def __init__(self, image_b64: str, size: tuple[int, int] = (600, 600), max_size_kb: int = 100, format_: str = 'webp'):
#         self._image = Image.open(BytesIO(base64.b64decode(image_b64))).convert("RGB")
#         self._size = size
#         self._max_size_kb = max_size_kb
#         self._format_ = format_

#     def __resize(self):
#         width, height = self._image.size

#         # Decide scaling factor
#         if width > height:
#             new_width = 600
#             new_height = int((height / width) * 600)
#         else:
#             new_height = 600
#             new_width = int((width / height) * 600)

#         self._image = self._image.resize((new_width, new_height), Image.LANCZOS)

#     def __compress(self):
#         buffer = BytesIO()
#         quality = 95

#         # Reduce quality until under max_size_kb
#         while quality > 10:
#             buffer.seek(0)
#             self._image.save(buffer, format=self._format_, quality=quality)
#             size_kb = buffer.tell() / 1024
#             if size_kb <= self._max_size_kb:
#                 break
#             quality -= 5

#         buffer.seek(0)
#         return buffer

#     def get_image(self) -> str:
#         self.__resize()
#         buffer = self.__compress()
#         return base64.b64encode(buffer.getvalue()).decode("utf-8")


# # Example usage
# if __name__ == "__main__":
#     with open("abc.jpg", "rb") as f:
#         img_b64 = base64.b64encode(f.read()).decode("utf-8")

#     thumb = Thumbnail(img_b64)
#     result_b64 = thumb.get_image()

#     # Save just for test (not needed in real case)
#     with open("output.webp", "wb") as f:
#         f.write(base64.b64decode(result_b64))