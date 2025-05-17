# Hand Gesture Recognition Web Application

A web-based application for real-time hand gesture recognition using webcam input. The application uses computer vision and machine learning to detect hand gestures and classify them.

## Features

- Real-time hand detection using a webcam
- Classification of hand gestures into predefined categories (A, B, C)
- Interactive web interface displaying prediction results
- Visual feedback for detected gestures

## Requirements

- Python 3.6+
- OpenCV
- cvzone
- TensorFlow/Keras
- Flask
- A webcam

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/hand-gesture-recognition.git
cd hand-gesture-recognition
```

2. Install the required packages:
```
pip install opencv-python cvzone tensorflow flask numpy
```

## Usage

1. Run the Flask application:
```
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

3. Show hand gestures to your webcam and see the predictions in real-time.

## Project Structure

- `app.py`: Flask web application
- `templates/index.html`: Web interface
- `Model/`: Contains the trained model files
- `Data/`: Training and test image data
- `dataCollection.py`: Script for collecting training data
- `test.py`: Script for testing the model locally

## License

[MIT License](LICENSE)

## Acknowledgments

- Hand tracking is implemented using the cvzone library
- The gesture classification model is trained using TensorFlow/Keras