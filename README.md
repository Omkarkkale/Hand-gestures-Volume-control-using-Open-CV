# Hand Tracking Gesture Volume Control

This project uses Computer Vision and Hand Tracking (via MediaPipe) to control the system volume using hand gestures. It includes a basic volume control script and an advanced version with visual feedback.

## Features

- **Real-time Hand Tracking:** Uses MediaPipe to detect hand landmarks.
- **Gesture Control:** Adjust system volume by changing the distance between your thumb and index finger.
- **Visual Feedback:** Shows volume percentage, a volume bar, and framerate (FPS).
- **Smoothed Control:** (In Advanced version) Volume changes are smoothed to prevent jitter.

## Prerequisites

- Python 3.x
- Webcam

## Installation

1. Clone the repository (or download the source code).
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Volume Control

Run the basic volume control script:

```bash
python VolHandContol.py
```

### Advanced Volume Control

Run the advanced volume control script (includes smoother transitions and more visual indicators):

```bash
python ADV_VOL_CTRL.py
```

**Controls:**
- **Adjust Volume:** Pinch thumb and index finger. Move them apart to increase volume, bring them closer to decrease.
- **Lock/Set Volume:** (Advanced Only) Flex pinky finger to lock/set the volume.
- **Exit:** Press various keys depending on the script (usually standard OpenCV `waitKey`).

## Troubleshooting

- **Webcam:** If the script crashes or doesn't show video, try changing the `cv2.VideoCapture(0)` index to `1` or `2` in the script.
- **Audio:** Ensure your system's audio device is active. This script uses `pycaw` which controls the Windows system volume.

## Credits

- Built using [OpenCV](https://opencv.org/) and [MediaPipe](https://google.github.io/mediapipe/).
