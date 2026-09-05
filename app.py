from flask import Flask, render_template, Response, jsonify, request
import cv2
import os
from drawsiness_yawn import DrowsinessDetector

app = Flask(__name__)

# Create a single shared detector instance
detector = DrowsinessDetector()


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/cameras")
def list_cameras():
    """Probe camera indices 0-4 and return available ones."""
    available = []
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available.append({"index": i, "label": f"Camera {i}"})
            cap.release()
    return jsonify(available)


@app.route("/start", methods=["POST"])
def start_monitoring():
    """Start the drowsiness detection and camera."""
    data = request.get_json(silent=True) or {}
    cam_index = int(data.get("cam_index", 0))
    detector.start(cam_index=cam_index)
    return jsonify({"message": "Monitoring started", "running": True})


@app.route("/stop", methods=["POST"])
def stop_monitoring():
    """Stop the drowsiness detection and release camera."""
    detector.stop()
    return jsonify({"message": "Monitoring stopped", "running": False})


@app.route("/status")
def status():
    """Return current detection status as JSON."""
    return jsonify(detector.get_status())


@app.route("/process_frame", methods=["POST"])
def process_frame_route():
    """Accept a JPEG frame from the browser, run detection, return annotated frame.

    Browser sends: { "frame": "data:image/jpeg;base64,..." }
    Server returns: { "frame": "data:image/jpeg;base64,...", "status": {...} }
    """
    import base64

    data = request.get_json(silent=True) or {}
    frame_data = data.get("frame", "")

    # Strip the data URI prefix (data:image/jpeg;base64,...)
    if "," in frame_data:
        frame_data = frame_data.split(",", 1)[1]

    try:
        jpeg_bytes = base64.b64decode(frame_data)
    except Exception:
        return jsonify({"error": "Invalid frame data", "status": detector.get_status()}), 400

    annotated, status_dict = detector.process_external_frame(jpeg_bytes)

    if annotated is None:
        return jsonify({"frame": None, "status": status_dict})

    annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(annotated).decode("utf-8")
    return jsonify({"frame": annotated_b64, "status": status_dict})


def generate_frames():
    """Generator that yields MJPEG frames for video streaming."""
    while detector.running:
        frame_bytes, _ = detector.process_frame()
        if frame_bytes is not None:
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                frame_bytes +
                b'\r\n'
            )


@app.route("/video_feed")
def video_feed():
    """MJPEG video stream endpoint."""
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)