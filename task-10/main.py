import os
import cv2
from PIL import Image, ImageDraw

final = Image.open("final.png")
draw = ImageDraw.Draw(final)
draw.rectangle((0, 0, 512, 512), fill=(255, 255, 255, 0))

detector = cv2.SimpleBlobDetector_create(cv2.SimpleBlobDetector_Params())

(x1, y1) = (0, 0)
(x2, y2) = (0, 0)
reset = True

index = 0
color = None

while index<97:
	index += 1
	path = "assets/Layer "+ str(index)+".png"
    
	if not os.path.exists(path):
		continue

	x2 = x1
	y2 = y1
	img = cv2.imread(path, cv2.COLOR_RGB2BGR)
	grayscale = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	points = detector.detect(grayscale)
	if len(points) == 0:
		reset = True
		continue
	else:
		(x1, y1) = points[0].pt
		x1 = round(x1)
		y1 = round(y1)
		color = img[y1, x1]

	if reset == False:
		draw.line((x1, y1, x2, y2), fill=(color[2], color[1], color[0], 0), width=3)

	reset = False


final.show()