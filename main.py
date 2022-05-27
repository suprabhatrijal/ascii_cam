import PIL.Image as Image
import numpy as np

# An array of ascii chars of descending intensity
contrast = 10
ASCII_CHARS = (
    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|"
    "()1{}[]?-_+~<>i!lI;:,\"^`'.                                          "
)
ASCII_CHARS = ASCII_CHARS[: -41 + contrast]

try:
    image = Image.open("./isaac.jpg")
except FileNotFoundError:
    print("Unable to open the given file")


# Resize the image
def resize_image(image):
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height
    new_height = 150
    new_width = int(aspect_ratio * new_height)
    new_image = image.resize((new_width, new_height), Image.LANCZOS)
    return new_image


# Turn it into grey scale
def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image


# Use the intensity of the greyscale pixel to assign ascii char
def pixel_to_ascii(image):
    array_of_pixels = np.array(image)
    print(array_of_pixels.shape)
    n = len(ASCII_CHARS)
    ascii_image = ""
    for i in range(0, array_of_pixels.shape[0]):
        for j in range(0, array_of_pixels.shape[1]):
            pixel = array_of_pixels[i, j]
            k = int(np.floor(pixel / 256 * n))
            ascii_char = ASCII_CHARS[n - 1 - k]
            ascii_image += ascii_char
        ascii_image += "\n"
    print(ascii_image)
    file = open("image.txt", "w")
    file.write(ascii_image)
    file.close()


pixel_to_ascii(grayify(resize_image(image)))
