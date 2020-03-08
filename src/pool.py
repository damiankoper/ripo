# import the necessary packages
import numpy as np
import cv2
import time
# construct the argument parse and parse the arguments
# load the image
start = time.time()

image = cv2.imread('test/images/test1.png')
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
width = image.shape[1]
height = image.shape[0]

# define the list of boundaries
boundaries = [
    ([70, 150, 50], [95, 255, 220]),
]

#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('image', 1280, 720)


# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(imageHSV, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    contours = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours[0], key=cv2.contourArea)
    minarea = cv2.minAreaRect(c)
    rect = cv2.boxPoints(minarea)
    cv2.drawContours(output, [np.int0(rect)], -1, (0, 255, 0), 3)

    dest = np.float32([
        [width-1, height-1],
        [0, height-1],
        [0, 0],
        [width-1, 0],
    ])
    M = cv2.getPerspectiveTransform(rect, dest)


outputKeyed = cv2.subtract(image, output)
warp = cv2.warpPerspective(image, M, (width, height))
warp2 = cv2.warpPerspective(outputKeyed, M, (width, height))

gray = cv2.cvtColor(warp2, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,
                           1, 20, param1=50, param2=30, minRadius=30, maxRadius=65)

if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(warp2, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(warp2, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)


# show the images
end = time.time()
print(end - start)
#cv2.imshow("image", np.hstack([image, output]))
cv2.imwrite("tests/results/detect2.png", warp2)
cv2.imwrite("tests/results/detect1.png", output)
cv2.imwrite("tests/results/detect.png", np.hstack([image, warp]))
# cv2.waitKey(0)
