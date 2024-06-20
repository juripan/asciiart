from PIL import Image
from tkinter import filedialog
import numpy as np


def NSD(n: tuple):
    x, y = n
    while x != y:
        if x > y:
            x -= y
        elif x < y:
            y -= x
    return x


def drawASCII(pixel_values: list, palette: str, image_width: int) -> str:
    i = 0
    res: list[str] = [] # using a list because concatenating strings in large quantities is inefficient
    palette_length = len(palette)
    brightness_range = 255 / palette_length
    
    for pixel in pixel_values:
        brightness = sum(pixel)/3
        if i >= image_width:
            res.append("\n")
            i -= image_width
        
        start, end = 0, brightness_range
        for j in range(palette_length):
            if start <= brightness <= end:
                res.append(palette[j] * 2)
                break
            start += brightness_range
            end += brightness_range
        i += 1
    return "".join(res)


file_path = filedialog.askopenfilename(title="select an image", filetypes=(('png files', '*.png'), ('jpeg files', '*.jpeg')))
user_crop = input("write the crop size here(xy coords of 2 points with spaces in between(4 numbers or leave empty)): ").split()
user_size = float(input("what size do you want the art to be (gets corrected to image aspect ratio)(1 is default): "))
palette_size = input("palette size(big or small): ").lower()
palette_swap = input("Do zou want to reverse the palette?(y/n)").lower()

img = Image.open(file_path, "r").convert("RGB")

if user_crop:
    user_crop = tuple(map(int, user_crop))
    img = img.crop(user_crop)

intermediate_size = (img.size[0] // NSD(img.size) * user_size, img.size[1] // NSD(img.size) * user_size)
print(f"intermediate size: {intermediate_size}")

choice = input("do you want to change the size(y/n)? ")
if choice.lower() == "y":
    user_size = float(input("what size do you want the art to be (gets corrected to image aspect ratio): "))

final_size: tuple[int, int] = (int(img.size[0] // NSD(img.size) * user_size), int(img.size[1] // NSD(img.size) * user_size))
print(final_size)

img = img.resize(final_size)

pixel_values = np.array(img.getdata())
width: int = img.size[0]

#big palette tends to be noisier
big_palette: str = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:," + "^" + "`'. "
small_palette: str = "@%#*+=-:. "

if palette_size == "big":
    chosen_palette = big_palette
else:
    chosen_palette = small_palette

if palette_swap == "y":
    chosen_palette = chosen_palette[::-1]

with open("art.txt", "w") as f:
    f.write(drawASCII(pixel_values, chosen_palette, width))
print("done!")
