# DriveGuard 🚗👁️
**AI-Powered Real-Time Driver Drowsiness and Alertness Monitoring System**

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://driveguard-lrdm.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kanchi1109/driveguard)

🌐 **Live Deployment:** [https://driveguard-lrdm.onrender.com/](https://driveguard-lrdm.onrender.com/)

DriveGuard is a computer-vision safety application designed to detect driver drowsiness and fatigue in real time. It monitors facial landmarks using OpenCV and dlib, calculates the Eye Aspect Ratio (EAR) and lip distance, and sounds customizable audible alerts directly through a web dashboard.

---

## 🌟 Key Features

- **Live Video Streaming**: Real-time MJPEG camera stream with face and eye contour overlays.
- **Drowsiness Detection**: Tracks Eye Aspect Ratio (EAR); triggers alerts when eyes remain closed continuously for a defined threshold.
- **Yawn Detection**: Monitors mouth opening distance to detect fatigue-induced yawning.
- **Multi-Camera Support**: Automatically detects connected cameras (webcams, USB cameras, external capture devices) and allows real-time switching from the dashboard.
- **Randomized Audio Alerts**: Plays attention-grabbing alert audio clips for 3–4 seconds in the browser when fatigue is detected.
- **Interactive Dashboard**: Modern dark-mode web dashboard displaying live EAR values, closed frame counter, total alert tally, and recent detection event logs.
- **Auto-Download Model**: Automatically checks and downloads the required dlib 68-face-landmarks model on first run.

---

## 📁 Project Structure

```text
driveguard/
├── app.py                     # Flask web server & streaming API
├── drawsiness_yawn.py         # DrowsinessDetector computer-vision engine
├── requirements.txt           # Python package dependencies
├── .gitignore                 # Files excluded from version control
├── static/
│   └── audio/                 # Alert audio files (WAV)
│       ├── mixkit-bell-notification-933.wav
│       └── mixkit-urgent-simple-tone-loop-2976.wav
└── templates/
    └── dashboard.html         # Responsive web UI & monitoring controls
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/driveguard.git
cd driveguard
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note for Windows users**: `dlib-bin` is included in `requirements.txt` to provide prebuilt wheels so you do not need CMake or Visual Studio C++ build tools installed.

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Dashboard
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```
Select your camera from the dropdown, click **START MONITORING**, and DriveGuard will begin tracking alertness.

---

## ⚙️ Detection Thresholds

You can tune the sensitivity in `drawsiness_yawn.py`:
- `EYE_AR_THRESH = 0.3`: Eye aspect ratio below which eyes are considered closed.
- `EYE_AR_CONSEC_FRAMES = 30`: Number of consecutive frames eyes must be closed before triggering a drowsiness alert.
- `YAWN_THRESH = 20`: Lip distance threshold for detecting yawns.

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
