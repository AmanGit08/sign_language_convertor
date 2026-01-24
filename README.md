# Sign Language to Speech Converter

This Python application captures sign language gestures from your laptop camera, recognizes American Sign Language (ASL) alphabet letters using hand landmarks, builds words from consecutive letters, and converts the recognized text to speech using pyttsx3.

## Features

- Real-time video capture using OpenCV
- Hand detection and tracking with MediaPipe
- Basic ASL letter recognition based on finger extension patterns
- Word building from recognized letters
- Automatic speech synthesis when signing pauses
- User-friendly interface with visual feedback

## Requirements

- Python 3.7 or higher
- Webcam (built-in laptop camera or external)
- Windows/Linux/Mac OS

## Installation

1. Ensure Python is installed on your system.
2. Clone or download this repository to your local machine.
3. Navigate to the project directory.
4. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script:

   ```
   python mainsl.py
   ```

2. A window will open showing the camera feed.
3. Position your hand in front of the camera and make ASL letter signs.
4. Recognized letters will be added to the current word displayed on the screen.
5. When you stop signing (no hand detected for 2 seconds), the current word will be spoken aloud.
6. Press 'q' in the video window to quit the application.

## ASL Recognition

The application recognizes ASL alphabet letters based on which fingers are extended and their relative positions. The recognition is basic and may not be 100% accurate. Supported letters include A, B, D, E, F, G, H, I, K, L, M, N, O, P, Q, S, T, U, V, W, X, Y.

## Troubleshooting

- **Camera not opening**: Ensure no other application is using the camera. Try closing other video apps.
- **Hand not detected**: Make sure there's good lighting, your hand is clearly visible, and the camera is focused.
- **Poor recognition**: The recognition is rule-based and may misclassify similar hand shapes. Practice clear ASL signs.
- **No speech output**: Check your system's audio settings and ensure speakers are working.
- **Performance issues**: Close other resource-intensive applications. The app runs hand detection on each frame.
- **Import errors**: Ensure all dependencies are installed correctly. Try reinstalling with `pip install -r requirements.txt --force-reinstall`.

## Limitations

- Recognizes only static ASL alphabet letters, not full words or dynamic signs.
- Accuracy depends on lighting, hand position, and individual signing style.
- Designed for single-hand signing (right hand assumed).
- Word boundary detection is based on pause duration, which may not always be accurate.

## Future Improvements

- Machine learning-based recognition for better accuracy
- Support for two-handed signs
- Word and phrase recognition
- Custom gesture for word boundaries
- Voice selection and speed adjustment

## License

This project is open-source. Feel free to modify and distribute.