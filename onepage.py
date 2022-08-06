
import cv2
import numpy as np
import pytesseract
import os
import re

roi = [ [(250, 235), (837, 293), 'text', 'source'],
        [(1193, 89), (1500, 144), 'text', 'labNumber'], 
        [(253, 143), (590, 190), 'text', 'pid'], 
        [(376, 374), (739, 425), 'text', 'dateRequested'],
        [(1158,381), (1512, 434), 'text', 'dateReceived'],
        [(645, 675), (803, 730), 'float', 'whiteBloodCells'], 
        [(645, 735), (803, 790), 'float', 'redBloodCells'], 
        [(645, 795), (803, 850), 'float', 'hemoglobin'], 
        [(645, 855), (803, 910), 'float', 'hematocrit'], 
        [(645, 915), (803, 970), 'float', 'meanCorpuscularVolume'], 
        [(645, 973), (803, 1028), 'float', 'meanCorpuscularHb'], 
        [(645, 1034), (803, 1089), 'float', 'meanCorpuscularHbConc'], 
        [(645, 1093), (803, 1146), 'float', 'rbcDistributionWidth'], 
        [(645, 1153), (803, 1208), 'float', 'plateletCount'], 
        [(645, 1270), (803, 1327), 'float', 'segmenters'], 
        [(645, 1327), (803, 1384), 'float', 'lymphocytes'], 
        [(645, 1386), (803, 1443), 'float', 'monocytes'], 
        [(645, 1445), (803, 1505), 'float', 'eosinophils'], 
        [(645, 1506), (803, 1560), 'float', 'basophils'], 
        [(645, 1562), (803, 1619), 'float', 'bands'], 
        [(645, 1684), (803, 1741), 'float', 'absoluteSeg'], 
        [(645, 1743), (803, 1800), 'float', 'absoluteLymphocyteCount'], 
        [(645, 1802), (803, 1863), 'float', 'absoluteMonocyteCount'], 
        [(645, 1860), (803, 1919), 'float', 'absoluteEosinophilCount'], 
        [(645, 1920), (803, 1978), 'float', 'absoluteBasophilCount'], 
        [(645, 1978), (803, 2036), 'float', 'absoluteBandCount']
     ]

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

per = 25
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

imgQ = cv2.imread('D:\\Django Projects\\OCR\images\\sample.png')
h,w,c = imgQ.shape
gray_image = grayscale(imgQ)
thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)

orb = cv2.ORB_create(1000)
kp1, des1 = orb.detectAndCompute(im_bw, None)

img = cv2.imread('D:\\Django Projects\\OCR\\test\\1.png')
gray_image = grayscale(img)
thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
kp2, des2 = orb.detectAndCompute(im_bw, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = bf.match(des2, des1)
list(matches).sort(key= lambda x: x.distance)
good = matches[:int(len(matches) * (per/100))]

srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1,1,2)
dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1,1,2)

M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
imgScan = cv2.warpPerspective(img, M, (w,h))
imgShow = imgScan.copy()
imgMask = np.zeros_like(imgShow)

myData = {}
for x, r in enumerate(roi):
    cv2.rectangle(imgMask, (r[0][0], r[0][1]), (r[1][0], r[1][1]), (0, 255, 0), cv2.FILLED)
    imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.5, 0)
    imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]

    if r[2] == 'float':
        text = pytesseract.image_to_string(imgCrop)
        value = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", text)
        if len(value) != 0:
            myData[r[3]] = float(value[0])
        else:
            myData[r[3]] = "None"
    elif r[2] == 'text':
        text = pytesseract.image_to_string(imgCrop)
        newText = re.sub(r"[^a-zA-Z0-9-(): ]","",text)
        if newText != '':
            myData[r[3]] = newText
        else:
            myData[r[3]] = "None"

for x, y in myData.items():
    print(x, '=', y)

#cv2.imshow("KeypointsQuery  ", impKp1)
h,w,c = imgShow.shape
imgShow = cv2.resize(imgShow, (w//3, h//3))
cv2.imshow("Output", imgShow)
# cv2.imshow("Output", imgQ)
cv2.waitKey(0)

