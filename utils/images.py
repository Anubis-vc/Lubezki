from PIL import Image


def resize_image_with_max(path: str, upper_bound: int):
    image = Image.open(path)
    width, height = image.size
    if width > upper_bound or height > upper_bound:
        # thumbnail resizes while keeping aspect ratio
        image.thumbnail((upper_bound, upper_bound))
    return image
