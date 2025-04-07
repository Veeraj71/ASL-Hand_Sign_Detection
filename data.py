from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np
import math
import os

# Initialize video capture and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

# Configuration parameters
offset = 20
imgSize = 300
folder = "data/Z"
counter = 0

# Create target directory if it doesn't exist
os.makedirs(folder, exist_ok=True)

while True:
    success, img = cap.read()
    if not success:
        continue
    
    # Detect hands
    hands, img = detector.findHands(img)
    
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        
        # Calculate safe crop coordinates with boundary checks
        y_start = max(y - offset, 0)
        y_end = min(y + h + offset, img.shape[0])
        x_start = max(x - offset, 0)
        x_end = min(x + w + offset, img.shape[1])
        
        imgCrop = img[y_start:y_end, x_start:x_end]
        
        if imgCrop.size == 0:
            continue
        
        # Prepare white canvas
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        h_crop, w_crop, _ = imgCrop.shape
        aspectRatio = h_crop / w_crop

        # Resize and center image
        if aspectRatio > 1:  # Vertical image
            k = imgSize / h_crop
            wCal = math.ceil(k * w_crop)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:  # Horizontal image
            k = imgSize / w_crop
            hCal = math.ceil(k * h_crop)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize

        # Display windows
        cv2.imshow("Hand Crop", imgCrop)
        cv2.imshow("Processed Image", imgWhite)

    # Main feed display
    cv2.imshow("Camera Feed", img)
    
    # Key handling
    key = cv2.waitKey(1)
    if key == ord("s"):
        cv2.imwrite(f'{folder}/Image_{counter}.jpg', imgWhite)
        print(f"Saved: Image_{counter}.jpg")
        counter += 1
    elif key == ord("q"):
        break

# Cleanup resources
cap.release()
cv2.destroyAllWindows()