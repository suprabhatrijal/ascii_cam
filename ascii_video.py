import cv2
import os
import numpy as np
import PIL.Image as Image
import datetime
from pynput import keyboard


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


def on_press(key):
    try:
        if key.char == "q":
            global close
            close = True

    except AttributeError:
        if key == keyboard.Key.space:
            save_image()


def save_image():
    date_now = str(datetime.datetime.utcnow()).replace(" ", "_")
    print(date_now)
    file = open(f"{date_now}.txt", "w")
    file.write(final_image)
    file.close()


def on_release(key):
    pass


def resize(image) -> Image.Image:
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height
    new_height = 100
    new_width = 150
    # new_width = int(new_height * aspect_ratio)
    return image.resize((new_width, new_height), Image.LANCZOS)


def grayify(image) -> Image.Image:
    return image.convert("L")


def pixel_to_ascii(image) -> None:
    image_from_array = Image.fromarray(image)
    processed_image = grayify(resize(image_from_array))
    array_of_pixels = np.array(processed_image)
    average = np.average(array_of_pixels)
    contrast = int(40 - 30 * ((256 - average) / 256))

    # An array of ascii chars of descending intensity
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
    # os.system("clear")
    global final_image
    final_image = ascii_image
    print(ascii_image)
    print()
    print()
    print(f"Press space to click a picture! {' '*30} Press q to quit")
    # print(contrast)


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()


close = False
while not close:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    pixel_to_ascii(frame)
    # Display the resulting frame
    # cv.imshow("Image to ASCII", gray)
    if cv2.waitKey(1) == ord("q"):
        break
    if close:
        os.system("cls" if os.name == "nt" else "clear")
        exit()
# When everything done, release the capture

cap.release()
cv2.destroyAllWindows()
