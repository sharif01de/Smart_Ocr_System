import cv2
import pytesseract
from PIL import Image
import os
import json
from datetime import datetime

#folder annd json file setup

if not os.path.exists("captures"):
    os.makedirs("captures")

json_path="ocr_data.json"
if not os.path.exists(json_path):
    with open(json_path, "w") as f:
        json.dump([], f)   #initialize with empty list


cap=cv2.VideoCapture(0)
print(" press space")

counter = 1


while True:
    ret, frame= cap.read()
    if not ret:
        print("failed to access cameera")
        break

    cv2.imshow(" press space to capture", frame)
    key= cv2.waitKey(1)

    if key == 27:
        break
    elif key == 32:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captures/capture_{counter}_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f" Saved: {filename}")

        text = pytesseract.image_to_string(Image.open(filename)).strip()
        print(" OCR Result:\n", text)

        # Append to JSON file
        with open(json_path, "r+") as f:
            data = json.load(f)
            data.append({
                "filename": filename,
                "timestamp": timestamp,
                "text": text
            })
            f.seek(0)
            json.dump(data, f, indent=4)

    counter += 1

cap.realease()
cv2.destroyAllWindows()
 



