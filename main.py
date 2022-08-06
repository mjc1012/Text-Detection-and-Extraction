
import cv2
import numpy as np
import pytesseract
import os
import re

roi = [ [(72, 62), (311, 80), 'text', 'source'],
        [(456, 15), (532, 31), 'text', 'labNumber'], 
        [(72, 29), (158, 47), 'text', 'pid'], 
        [(112, 100), (217, 116), 'text', 'dateRequested'],
        [(432, 100), (539, 117), 'text', 'dateReceived'],
        [(220, 192), (263, 210), 'float', 'whiteBloodCells'], 
        [(220, 210), (263, 228), 'float', 'redBloodCells'], 
        [(220, 228), (263, 246), 'float', 'hemoglobin'], 
        [(220, 246), (263, 264), 'float', 'hematocrit'], 
        [(210, 260), (263, 290), 'float', 'meanCorpuscularVolume'], 
        [(220, 272), (263, 310), 'float', 'meanCorpuscularHb'], 
        [(220, 300), (263, 318), 'float', 'meanCorpuscularHbConc'], 
        [(220, 318), (263, 336), 'float', 'rbcDistributionWidth'], 
        [(220, 336), (263, 354), 'float', 'plateletCount'], 
        [(220, 367), (263, 385), 'float', 'segmenters'], 
        [(220, 385), (263, 403), 'float', 'lymphocytes'], 
        [(220, 403), (263, 421), 'float', 'monocytes'], 
        [(216, 421), (263, 439), 'float', 'eosinophils'], 
        [(220, 439), (263, 457), 'float', 'basophils'], 
        [(220, 457), (263, 475), 'float', 'bands'], 
        [(220, 490), (263, 508), 'float', 'absoluteSeg'], 
        [(220, 508), (263, 526), 'float', 'absoluteLymphocyteCount'], 
        [(220, 526), (263, 544), 'float', 'absoluteMonocyteCount'], 
        [(220, 544), (263, 562), 'float', 'absoluteEosinophilCount'], 
        [(220, 562), (263, 580), 'float', 'absoluteBasophilCount'], 
        [(220, 580), (263, 598), 'float', 'absoluteBandCount']
     ]

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

per = 25
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

imgQ = cv2.imread('D:\\Django Projects\\OCR\images\\sample.png')
h,w,c = imgQ.shape
#imgQ = cv2.resize(imgQ, (w, h))
gray_image = grayscale(imgQ)
thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)

orb = cv2.ORB_create(1000)
kp1, des1 = orb.detectAndCompute(im_bw, None)
#impKp1 = cv2.drawKeypoints(imgQ, kp1, None)

path = 'D:\\Django Projects\\OCR\\test'
myPicList = os.listdir(path)
print(myPicList)
for j, y in enumerate(myPicList):
    img = cv2.imread(path +"/"+y)
    #img = cv2.resize(img, (w, h))
    gray_image = grayscale(img)
    thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    kp2, des2 = orb.detectAndCompute(im_bw, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des2, des1)
    list(matches).sort(key= lambda x: x.distance)
    good = matches[:int(len(matches) * (per/100))]
    imgMatch = cv2.drawMatches(img, kp2, imgQ, kp1, good, None, flags = 2)
    #imgMatch = cv2.resize(imgMatch, (w, h))
    #cv2.imshow(y, imgMatch)
    
    srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1,1,2)

    M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
    imgScan = cv2.warpPerspective(img, M, (w,h))
    #cv2.imshow(y, imgScan)
    imgShow = imgScan.copy()
    imgMask = np.zeros_like(imgShow)

    myData = {}
    for x, r in enumerate(roi):
        cv2.rectangle(imgMask, (r[0][0], r[0][1]), (r[1][0], r[1][1]), (0, 255, 0), cv2.FILLED)
        imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1, 0)
        imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        # cv2.imshow(str(x), imgCrop)

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
    
    cv2.imshow(y, imgShow)
    print(f'\n##### Image[{j}] #####')
    for x, y in myData.items():
        print(x, '=', y)
    


#cv2.imshow("KeypointsQuery  ", impKp1)
#cv2.imshow("Output", imgQ)
cv2.waitKey(0)

