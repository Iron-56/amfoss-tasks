import cv2
import pytesseract

img = cv2.imread("captcha.png")
#img = cv2.imread("task-02/captcha.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print(eval(pytesseract.image_to_string(gray)))