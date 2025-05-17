import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

# Initialize
cap        = cv2.VideoCapture(0)
detector   = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
offset     = 20
imgSize    = 300
labels     = ["A", "B", "C"]

while True:
    success, img = cap.read()
    if not success:
        break

    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        x, y, w, h = hands[0]['bbox']

        # Create white canvas & crop hand
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop  = img[y-offset:y+h+offset, x-offset:x+w+offset]

        # Resize & center on white
        aspectRatio = h / w
        if aspectRatio > 1:
            k      = imgSize / h
            wCal   = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            wGap      = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k      = imgSize / w
            hCal   = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            hGap      = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize

        # Predict
        prediction, index = classifier.getPrediction(imgWhite, draw=False)

        # Draw label & bounding box
        cv2.rectangle(imgOutput,
                      (x-offset,     y-offset-50),
                      (x-offset+90,  y-offset),
                      (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index],
                    (x, y-26),
                    cv2.FONT_HERSHEY_COMPLEX, 1.7,
                    (255,255,255), 2)
        cv2.rectangle(imgOutput,
                      (x-offset,     y-offset),
                      (x + w+offset, y + h+offset),
                      (255, 0, 255), 4)

        # Optional: show intermediate windows
        cv2.imshow("ImageCrop",  imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    # Final output
    cv2.imshow("Image", imgOutput)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
