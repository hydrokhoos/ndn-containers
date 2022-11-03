import cv2


img = cv2.imread('test.jpg')

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

threshold = 100
ret, th_img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

cv2.imwrite('out.jpg', th_img)
