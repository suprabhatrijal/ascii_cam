import cv2 as cv
import os

import numpy as np
import PIL.Image as Image

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


def resize(image):
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height
    new_height = 150
    new_width = int(new_height * aspect_ratio)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    return resized_image


def grayify(image):
    gray_image = image.convert("L")
    return gray_image


def pixel_to_ascii(image):
    image_from_array = Image.fromarray(image)
    array_of_pixels = np.array(grayify(resize(image_from_array)))

    # An array of ascii chars of descending intensity
    average = np.average(array_of_pixels)
    contrast = int(40 - 30 * ((256 - average) / 256))
    ASCII_CHARS = (
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|"
        "()1{}[]?-_+~<>i!lI;:,\"^`'.                                         "
    )
    ASCII_CHARS = ASCII_CHARS[: -41 + contrast]

    n = len(ASCII_CHARS)
    indexes = np.floor(array_of_pixels / 256 * n)
    ascii_image = ""
    for i in range(0, array_of_pixels.shape[0]):
        for j in range(0, array_of_pixels.shape[1]):
            k = int(indexes[i, j])
            ascii_char = ASCII_CHARS[n - 1 - k]
            ascii_image += ascii_char
        ascii_image += "\n"
    os.system("clear")
    print(ascii_image)
    print(contrast)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    pixel_to_ascii(frame)
    # Display the resulting frame
    # cv.imshow("Image to ASCII", gray)
    if cv.waitKey(1) == ord("q"):
        break
# When everything done, release the capture


cap.release()
cv.destroyAllWindows()
