from flask import Flask, render_template, Response, jsonify
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import base64
import threading
import time

app = Flask(__name__)

# Global variables
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
offset = 20
imgSize = 300
labels = ["A", "B", "C"]
last_prediction = "None"
last_confidence = 0
processing = False

# Initialize camera (will be started in a separate thread)
camera = None
camera_lock = threading.Lock()

def init_camera():
    global camera
    with camera_lock:
        if camera is None:
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                camera = None
                return False
    return True

def release_camera():
    global camera
    with camera_lock:
        if camera is not None:
            camera.release()
            camera = None

def get_frame():
    global last_prediction, last_confidence, processing
    
    if not init_camera():
        return None, None
    
    with camera_lock:
        success, img = camera.read()
        if not success:
            return None, None

    # Only process if not already processing (to avoid lag)
    if not processing:
        processing = True
        try:
            imgOutput = img.copy()
            hands, img = detector.findHands(img)
            
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                
                # Create white image
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                
                # Crop and ensure we're not out of bounds
                try:
                    y_min = max(0, y - offset)
                    y_max = min(img.shape[0], y + h + offset)
                    x_min = max(0, x - offset)
                    x_max = min(img.shape[1], x + w + offset)
                    
                    imgCrop = img[y_min:y_max, x_min:x_max]
                    if imgCrop.size == 0:
                        processing = False
                        return None, img
                        
                    aspectRatio = h / w

                    if aspectRatio > 1:
                        k = imgSize / h
                        wCal = math.ceil(k * w)
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wCal + wGap] = imgResize
                        prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    else:
                        k = imgSize / w
                        hCal = math.ceil(k * h)
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hCal + hGap, :] = imgResize
                        prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    
                    # Update global prediction
                    last_prediction = labels[index]
                    last_confidence = float(prediction[index])
                    
                    # Draw rectangle and text
                    cv2.rectangle(imgOutput, (x_min, y_min-50),
                                (x_min+90, y_min), (255, 0, 255), cv2.FILLED)
                    cv2.putText(imgOutput, labels[index], (x_min, y_min-15), 
                                cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 2)
                    cv2.rectangle(imgOutput, (x_min, y_min),
                                (x_max, y_max), (255, 0, 255), 4)
                except Exception as e:
                    print(f"Error processing hand: {e}")
        except Exception as e:
            print(f"Processing error: {e}")
        finally:
            processing = False

    # We'll return both the regular frame and the output frame with annotations
    return imgOutput, last_prediction

def generate_frames():
    while True:
        frame, prediction = get_frame()
        if frame is None:
            continue
            
        # Convert to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        # Convert to bytes
        frame_bytes = buffer.tobytes()
        
        # Yield the frame in the response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        # Add a small delay to control frame rate
        time.sleep(0.03)  # ~30 FPS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_prediction')
def get_prediction():
    return jsonify({
        'prediction': last_prediction,
        'confidence': last_confidence
    })

@app.route('/shutdown', methods=['POST'])
def shutdown():
    release_camera()
    return "Camera released"

if __name__ == '__main__':
    try:
        app.run(debug=False, threaded=True)
    finally:
        release_camera()