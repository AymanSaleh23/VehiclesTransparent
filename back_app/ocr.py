import cv2
import pytesseract
import PIL.Image

myconf = r"--psm 3 --oem 1"

text = pytesseract.image_to_string(PIL.Image.open("Vehicle_registration_plates_of_Transnistria.jpg"), config=myconf)
print(text)