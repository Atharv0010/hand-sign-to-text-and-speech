# Real-Time Hand Gesture Recognition

A computer vision application that recognizes hand gestures in real-time and converts them to both text and speech.

## 📋 Overview

This project uses MediaPipe's hand tracking technology to detect hand gestures through a webcam feed and converts recognized gestures into spoken words. The application is designed to recognize a set of predefined gestures and provide real-time feedback through both visual display and speech synthesis.

## ✨ Features

- **Real-time hand gesture recognition** using computer vision
- **Text and speech output** of recognized gestures
- **Multi-threading** for non-blocking speech synthesis
- **Gesture history tracking** for stable predictions
- **Confidence scoring** for reliable gesture detection
- **Visual feedback** directly on the video feed

## 🛠️ Requirements

- Python 3.7+
- OpenCV (`cv2`)
- MediaPipe
- pyttsx3 (text-to-speech)
- Webcam or camera

## 📦 Installation

1. Install the required dependencies:

```bash
pip install opencv-python mediapipe numpy pyttsx3
```

2. Clone or download this repository:

```bash
git clone https://github.com/yourusername/hand-gesture-recognition.git
cd hand-gesture-recognition
```

3. Run the script:

```bash
python gesture_recognition.py
```

## 🚀 How It Works

1. The program captures video from your webcam
2. MediaPipe's hand tracking detects hand landmarks in each frame
3. The detection algorithm analyzes the hand positions to determine gestures
4. Recognized gestures are displayed on screen and spoken through text-to-speech
5. A history buffer ensures stability by requiring consistent detections

## 🤲 Supported Gestures

The program currently recognizes the following gestures:

- **Hello**: Wide spread between thumb and index finger
- **Fine**: Thumb below index finger
- **Not good**: Thumb above index finger
- **Cool**: Very wide spread between thumb and index finger
- **Help**: Thumb positioned to the left of index finger
- **Thank you**: Automatically detected based on the above conditions

## 🔧 How to Use

1. Run the program
2. Position your hand in front of the camera
3. Make one of the supported gestures
4. The recognized gesture will be displayed on screen and spoken
5. Press 'q' to quit the application

## 🖥️ Code Structure

- **Hand Detection**: Using MediaPipe to detect and track hand landmarks
- **Gesture Recognition**: Based on relative positions of finger landmarks
- **Speech Synthesis**: Multithreaded to avoid blocking the main video processing loop
- **History Tracking**: Maintains a history of detected gestures to avoid flickering

## 🔍 Customization

You can add or modify gestures by updating the `confidence_scores` dictionary in the `detect_single_hand_gesture` function:

```python
confidence_scores = {
    "Your New Gesture": condition_for_gesture,
    # Other gestures...
}
```

Also update the `text_to_speak` dictionary in the `speak_gesture` function to add speech output for your new gesture.

## ⚠️ Troubleshooting

- **No detection**: Make sure you have good lighting and your hand is clearly visible
- **Misidentification**: Try making more distinctive gestures and adjusting your hand position
- **No sound**: Check if your system's sound is on and pyttsx3 is properly installed

## 🔄 Future Improvements

- Add more complex gesture recognition
- Implement machine learning for better gesture detection
- Support for custom user-defined gestures
- Add support for sign language alphabets
- Improve UI with more visual feedback

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details. 
