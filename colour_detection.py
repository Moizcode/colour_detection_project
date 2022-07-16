from inspect import getcallargs
import cv2 as cv
import pandas as pd

img = cv.imread('image/steve-johnson-u5bCqoJKYDQ-unsplash.jpg')
temp = img
dimension = (int(img.shape[1]*0.2), int(img.shape[0]*0.2))
img = cv.resize(img, dimension, interpolation=cv.INTER_AREA)

index = ["color", "color_name", "hex", "R", "G", "B"]
data = pd.read_csv('colors.csv', names=index, header=None)
# print(data)


def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(data)):
        d = abs(R - int(data.loc[i, "R"])) + abs(G -
                                                 int(data.loc[i, "G"])) + abs(B - int(data.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = data.loc[i, "color_name"]
    return cname


# global variable
clicked = False
r = g = b = 0


def find_color(event, x, y, flag, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        global r, g, b, clicked
        b, g, r = img[y, x]
        r = int(r)
        g = int(g)
        b = int(b)
        clicked = True


# for taking img from camera
vid = cv.VideoCapture(0)
ret, frame = vid.read()
img = frame


# creating window
cv.namedWindow('img2')
# set mouse call on the window
cv.setMouseCallback('img2', find_color)


while True:

    #cv.imshow('img2', img)
    cv.imshow('img2', img)
    if (clicked):
        # this make a rectangle
        cv.rectangle(img, (20, 20), (750, 60), (b, g, r), thickness=-1)
        text = getColorName(r, g, b) + ' R=' + str(r) + \
            ' G=' + str(g) + ' B=' + str(b)
        cv.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv.LINE_AA)
  # For very light colours we will display text in black colour
        if(r+g+b >= 600):
            cv.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv.LINE_AA)
        clicked = False
    # Break the loop when user hits 'esc' key
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()
