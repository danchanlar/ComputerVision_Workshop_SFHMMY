import cv2
import math
import numpy as np

def pipeline(image):
    height = image.shape[0]
    width = image.shape[1]

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cv2.imshow('gray', gray_image)
    cannyed_image = cv2.Canny(gray_image, 100, 200)
    cv2.imshow('cannyed', cannyed_image)

    #detect lines
    lines = cv2.HoughLinesP(cannyed_image, 1, np.pi/180, 80, np.array([]), 100, 10) #this function is the Hough transform:  technique used to detect shapes (especially lines, circles, or other parametric curves) in images

    for line in lines:
        print(line)

    left_line_x = []
    left_line_y = []
    right_line_x = []
    rigth_line_y = []
    largest_right_x = 0
    largest_left_y = 0

    for line in lines:
        for x1,y1,x2,y2 in line:
            slope = (y1-y2)/(x1-x2)
            if abs(slope) < 0.1:
                continue
            if slope < 0 and y1 > largest_left_y:
                largest_left_y = y1
                left_line_x = [x1,x2]
                left_line_y = [y1,y2]

            elif slope > 0 and y1 > largest_left_y:
                largest_right_y = y2
                right_line_x = [x1,x2]
                right_line_y = [y1,y2]

    linesToDraw = []

    if left_line_x != []:
        linesToDraw.append([left_line_x[0], left_line_x[1],left_line_y[0], left_line_y[1]])

    if right_line_x != []:
        linesToDraw.append([right_line_x[0], right_line_x[1],right_line_y[0], right_line_y[1]])

    line_img = np.zeros((
        height,
        width,
        3),
        dtype = np.uint8
    )
    result_image = np.copy(image)

    if linesToDraw is None: # in case there are no lines
        return

    for line in linesToDraw:
        for x1,x2,y1,y2 in line:
            cv2.line(line_image, (x1,y1), (x2,y2), [255,0,0],0.5)
    result_image = cv2.addWeighted(image, 0.8, line_img, 1, 0)
    resized_frame = cv2.resize(result_image, 843,480)
    cv2.imshow('houghlines', result_image)



image = cv2.imread("C:\\Users\\Administrator\\Desktop\\ntua.jpg")
pipeline(image)

#process for video
cap = cv2.VideoCapture("C:\\Users\\Administrator\\Desktop\\shell_eco_silesia_ring_autonomous.mp4")


while True:
    res,frame = cap.read()
    resized_frame = cv2.resize(frame, (843,480))
    pipeline(resized_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
