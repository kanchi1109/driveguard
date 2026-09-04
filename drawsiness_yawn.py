from scipy.spatial import distance as dist
from imutils import face_utils
from imutils.video import VideoStream
import numpy as np
import time
import os
import dlib
import cv2


class DrowsinessDetector:
    """Encapsulates drowsiness and yawn detection logic.

    Usage:
        detector = DrowsinessDetector()
        detector.start()
        frame, status = detector.process_frame()
        detector.stop()
    """

    # Detection thresholds
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 30
    YAWN_THRESH = 20

    def __init__(self, predictor_path="shape_predictor_68_face_landmarks.dat",
                 alarm_path="Alert.wav"):
        self.predictor_path = predictor_path
        self.alarm_path = alarm_path

        # State
        self.counter = 0
        self.alarm_status = False
        self.yawn_status = False
        self.total_alerts = 0
        self.current_ear = 0.0
        self.is_drowsy = False
        self.is_yawning = False

        # Detection log (last 20 events)
        self.detection_log = []

        # Camera
        self.vs = None
        self.running = False

        # Check and download model if missing
        if not os.path.exists(self.predictor_path):
            print(f"[INFO] Landmark file '{self.predictor_path}' not found. Downloading...")
            import urllib.request, bz2
            url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
            bz2_file = self.predictor_path + ".bz2"
            urllib.request.urlretrieve(url, bz2_file)
            data = bz2.open(bz2_file, "rb").read()
            with open(self.predictor_path, "wb") as f:
                f.write(data)
            if os.path.exists(bz2_file):
                os.remove(bz2_file)
            print("[INFO] Landmark file downloaded successfully.")

        # Load dlib models
        print("[INFO] Loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.predictor_path)

        # Landmark indices for eyes
        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def start(self, cam_index=0):
        """Start the video stream on the given camera index."""
        if self.running:
            return

        print(f"[INFO] Starting camera {cam_index}...")
        self.vs = VideoStream(src=cam_index).start()
        time.sleep(2.0)
        self.running = True

        # Reset state
        self.counter = 0
        self.alarm_status = False
        self.yawn_status = False
        self.is_drowsy = False
        self.is_yawning = False

    def stop(self):
        """Stop the video stream."""
        if not self.running:
            return

        self.running = False
        if self.vs is not None:
            self.vs.stop()
            self.vs = None
        print("[INFO] Camera stopped.")

    @staticmethod
    def eye_aspect_ratio(eye):
        """Calculate the eye aspect ratio (EAR)."""
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    @staticmethod
    def lip_distance(shape):
        """Calculate lip distance for yawn detection."""
        top_lip = shape[50]
        bottom_lip = shape[58]
        distance = dist.euclidean(top_lip, bottom_lip)
        return distance

    def sound_alarm(self):
        """Log that alarm was triggered (actual sound plays in the browser)."""
        print("[ALARM] Alert triggered!")

    def _add_log_entry(self, alert_type):
        """Add an entry to the detection log."""
        entry = {
            "time": time.strftime("%H:%M:%S"),
            "ear": round(self.current_ear, 2),
            "closed_frames": self.counter,
            "eye_status": "Closed" if self.current_ear < self.EYE_AR_THRESH else "Open",
            "alert_type": alert_type,
            "alarm": "ON" if self.alarm_status else "OFF",
        }
        self.detection_log.insert(0, entry)
        # Keep only the last 20 entries
        self.detection_log = self.detection_log[:20]

    def process_frame(self):
        """Process a single frame from the video stream.

        Returns:
            tuple: (annotated_frame_as_jpeg_bytes, status_dict)
                   Returns (None, status_dict) if no frame available.
        """
        if not self.running or self.vs is None:
            return None, self.get_status()

        frame = self.vs.read()

        if frame is None:
            return None, self.get_status()

        frame = cv2.resize(frame, (800, 450))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)

        for rect in rects:
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # ----- Eye detection -----
            leftEye = shape[self.lStart:self.lEnd]
            rightEye = shape[self.rStart:self.rEnd]

            leftEAR = self.eye_aspect_ratio(leftEye)
            rightEAR = self.eye_aspect_ratio(rightEye)

            ear = (leftEAR + rightEAR) / 2.0
            self.current_ear = ear

            # ----- Yawn detection -----
            lip = self.lip_distance(shape)

            # ----- Draw eye landmarks -----
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)

            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # ----- Drowsiness detection -----
            if ear < self.EYE_AR_THRESH:
                self.counter += 1

                if self.counter >= self.EYE_AR_CONSEC_FRAMES:
                    self.is_drowsy = True

                    if not self.alarm_status:
                        self.alarm_status = True
                        self.total_alerts += 1
                        self._add_log_entry("Drowsiness")
                        self.sound_alarm()

                    cv2.putText(
                        frame, "DROWSINESS ALERT!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
                    )
            else:
                self.counter = 0
                self.alarm_status = False
                self.is_drowsy = False

            # ----- Yawn detection -----
            if lip > self.YAWN_THRESH:
                self.is_yawning = True

                cv2.putText(
                    frame, "Yawn Alert", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
                )

                if not self.yawn_status:
                    self.yawn_status = True
                    self.total_alerts += 1
                    self._add_log_entry("Yawn")
                    self.sound_alarm()
            else:
                self.yawn_status = False
                self.is_yawning = False

            # ----- Display values on frame -----
            cv2.putText(
                frame, "EAR: {:.2f}".format(ear), (600, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
            )

            cv2.putText(
                frame, "Closed Frames: {}".format(self.counter), (550, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
            )

        # Encode frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return None, self.get_status()

        return jpeg.tobytes(), self.get_status()

    def get_status(self):
        """Return the current detection status as a dict."""
        return {
            "ear": round(self.current_ear, 2),
            "closed_frames": self.counter,
            "alarm": self.alarm_status,
            "drowsy": self.is_drowsy,
            "yawn": self.is_yawning,
            "total_alerts": self.total_alerts,
            "running": self.running,
            "log": self.detection_log,
        }