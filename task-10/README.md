# Operation Pixel Merge

## My Approach

First I drew a background to final image using draw.rectangle() function of PILLOW. For all the images, I checked if the image exists and using OpenCV I checked for points by converting the source image to grayscale and using built in blob detector class of OpenCV. If the point exist and the last point also exists then I draw a line using a color from the color at the blob's position. If no point exists I set the reset as True.

## Review

The task was overall good but the incorrect indexing of the assets was quite frustrating.