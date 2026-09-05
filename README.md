# DriveGuard 🚗👁️
**AI-Powered Real-Time Driver Drowsiness and Alertness Monitoring System**

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://driveguard-lrdm.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kanchi1109/driveguard)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

🌐 **Live Cloud Demo:** [https://driveguard-lrdm.onrender.com/](https://driveguard-lrdm.onrender.com/)

DriveGuard is a computer-vision safety application designed to detect driver drowsiness and fatigue in real time. It monitors facial landmarks using OpenCV and dlib, calculates the Eye Aspect Ratio (EAR) and mouth distance, and triggers audible alerts through a modern web dashboard.

---

## ⚡ Quickstart: Run Locally in 3 Steps (Recommended)

Running locally provides **instant zero-lag video** directly from your webcam with full hardware acceleration!

### Step 1: Clone the Repository
Open your terminal (PowerShell, Command Prompt, or Terminal) and run:
```bash
git clone https://github.com/kanchi1109/driveguard.git
cd driveguard
```

### Step 2: Install Requirements
```bash
pip install -r requirements.txt
```
*(Windows users: `dlib-bin` is included in `requirements.txt` so no C++ compiler or CMake is needed!)*

### Step 3: Start the Application
```bash
python app.py
```
> 💡 **Windows Shortcut:** You can also simply double-click **`run.bat`** in the project folder!

### Step 4: Open in Your Browser
Open Chrome, Edge, or Firefox and go to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

1. Select your camera from the dropdown menu (or leave Default).
2. Click **▶ START MONITORING**.
3. DriveGuard will start detecting facial landmarks in real time!

---

## 🖥️ Local Mode vs Cloud Mode

DriveGuard automatically detects where it is running:

| Feature | ⚡ Local Mode (`http://127.0.0.1:5000`) | ☁️ Cloud Mode (Render) |
|---|---|---|
| **Camera Feed** | Direct server MJPEG stream (Ultra fast) | Browser camera upload (`getUserMedia`) |
| **Latency** | **< 10ms (Zero lag)** | ~200ms - 400ms (Internet roundtrip) |
| **FPS** | Smooth **30 FPS** | ~10 FPS |
| **Requirements** | Laptop / PC with webcam | Any browser on phone, tablet, or PC |

---

## 🌟 Key Features

- **Direct MJPEG Streaming**: Ultra-low-latency real-time video stream with face mesh and eye contour overlays.
- **Drowsiness Detection**: Tracks Eye Aspect Ratio (EAR); triggers alerts when eyes remain closed continuously.
- **Yawn Detection**: Monitors mouth opening distance to detect fatigue-induced yawning.
- **Multi-Camera Selector**: Easily switch between internal webcam, external USB cameras, or capture cards.
- **Dual Audio Alerts**: Plays attention-grabbing alert audio clips for 3–4 seconds when drowsiness or yawns are detected.
- **Dark Modern Dashboard**: Displays real-time EAR values, closed frame counter, total alert tally, and detection history logs.
- **Auto Model Download**: Automatically downloads the dlib 68-landmarks model (~99MB) on the first run if missing.
- **Optimized Performance**: Includes CLAHE contrast enhancement for dim cabin lighting and intelligent frame-skipping to minimize CPU load.

---

## 📁 Project Structure

```text
driveguard/
├── app.py                     # Flask web server & MJPEG streaming endpoints
├── drawsiness_yawn.py         # DrowsinessDetector computer-vision engine
├── run.bat                    # 1-click Windows launcher
├── requirements.txt           # Python package dependencies
├── .gitignore                 # Excludes caches and large model files
├── static/
│   └── audio/                 # Alert audio clips (WAV)
│       ├── mixkit-bell-notification-933.wav
│       └── mixkit-urgent-simple-tone-loop-2976.wav
└── templates/
    └── dashboard.html         # Responsive web dashboard with dual-mode support
```

---

## ❓ Troubleshooting FAQ

<details>
<summary><b>1. The camera shows a black screen or fails to open</b></summary>

- Make sure no other application (like Zoom, Teams, Skype, or Windows Camera app) is currently using your webcam.
- Check Windows Settings: **Privacy & security > Camera**, and make sure **"Let desktop apps access your camera"** is turned **ON**.
</details>

<details>
<summary><b>2. "Port 5000 is already in use" error</b></summary>

If port 5000 is occupied by another process:
```bash
# Run on another port, for example 5050:
python -c "import os, app; os.environ['PORT']='5050'; app.app.run(host='0.0.0.0', port=5050)"
```
Then visit `http://127.0.0.1:5050`.
</details>

<details>
<summary><b>3. Dlib installation issues on Windows</b></summary>

The project uses `dlib-bin`, which includes pre-compiled Windows binary wheels for Python 3.9 through 3.14. You do **not** need Visual Studio C++ Build Tools or CMake. Simply run:
```bash
pip install dlib-bin
```
</details>

---

## ⚙️ Detection Thresholds

You can customize sensitivity in [drawsiness_yawn.py](drawsiness_yawn.py):
- `EYE_AR_THRESH = 0.3`: Eye aspect ratio below which eyes are considered closed.
- `EYE_AR_CONSEC_FRAMES = 30`: Number of consecutive closed frames before triggering a drowsiness alarm.
- `YAWN_THRESH = 20`: Mouth distance threshold for detecting yawns.

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
