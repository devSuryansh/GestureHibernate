# 👋 Gesture Hibernate

This project enables gesture-based commands to **hibernate your PC** using computer vision and hand tracking powered by **MediaPipe** and **OpenCV**.

Currently, it supports:

- 👋 **Waving with an open palm** to hibernate (`byebye.py`)
- 🖕 **Showing middle finger** to hibernate (`middlefinger.py`)

> **Note:** By default, actual hibernation is disabled (`ENABLE_HIBERNATE = False`) for testing purposes.

---

## 📁 Project Structure

```

devSuryansh-gesturehibernate/
├── byebye.py # Detects waving gesture (open palm left-right)
└── middlefinger.py # Detects middle finger gesture

```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/devSuryansh/gesturehibernate.git
cd gesturehibernate
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
# Create venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install opencv-python mediapipe
```

---

## 🚀 Usage

### 1. Run waving gesture detection (open palm)

```bash
python byebye.py
```

### 2. Run middle finger gesture detection

```bash
python middlefinger.py
```

> Press `Esc` key to exit either script.

---

## 🔐 Enabling Hibernation

To allow actual hibernation:

1. Open the script (`byebye.py` or `middlefinger.py`)
2. Change the configuration at the top:

```python
ENABLE_HIBERNATE = True
HIBERNATE_DELAY = 5  # Optional: Add delay in seconds before hibernating
```

3. Save and run. Your system will hibernate when the corresponding gesture is detected.

> On **Linux** , you may need superuser privileges or `systemctl hibernate` permissions.

---

## ✨ Features

- ✅ Real-time gesture recognition using webcam
- ✅ Cross-platform hibernation support (Windows, macOS, Linux)
- ✅ Motion-based waving detection with noise filtering
- ✅ Fully testable without performing real hibernation
- ✅ Easily extendable for more gestures

---

## 🤝 Contribution Guide

You're welcome to contribute new gestures, bug fixes, or performance improvements!

### Steps to Contribute:

1. **Fork** this repository
2. **Clone** your fork and create a new branch:
   ```bash
   git checkout -b feature/your-gesture
   ```
3. **Make your changes** (follow the structure of existing files)
4. **Test** thoroughly before committing
5. **Push** to your fork:
   ```bash
   git push origin feature/your-gesture
   ```
6. **Open a Pull Request** and describe your changes

---

## 📦 Todo / Ideas

- [ ] Add more gestures like thumbs-up/down
- [ ] Optimize for low-light or background noise
- [ ] Add a GUI toggle for test/real hibernation mode
- [ ] Export gestures to JSON logs

---

## 🧠 Credits

Built with:

- [OpenCV](https://opencv.org/) for camera and image processing
- [MediaPipe](https://mediapipe.dev/) for accurate hand tracking

Made with 💻 and 😄 by [@devSuryansh](https://github.com/devSuryansh)

---

## 📜 License

This project is open-source under the [MIT License](https://opensource.org/licenses/MIT).
