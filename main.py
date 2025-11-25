import time

import cv2
import matplotlib.pyplot as plt
from libcamera import controls
from picamera2 import Picamera2, Preview

# Initialize Camera
cam = Picamera2()

# Configuration
config = cam.create_preview_configuration(
    main={
        "size": (1280, 720),
        "format": "RGB888",
    },
    lores={"size": (320, 240), "format": "YUV420"},
    buffer_count=4,
)

cam.configure(config)

props = cam.camera_properties
print("Camera properties:")
print(props)

controls_dict = {
    "AeEnable": False,
    "AnalogueGain": 2.0,
    "ExposureTime": 100,
    "FrameDurationLimits": (16666, 33333),
    "AwbEnable": False,
    "AwbMode": controls.AwbModeEnum.Auto,
    "AfMode": controls.AfModeEnum.Auto,
    "Brightness": 0.0,
    "Contrast": 1.0,
    "Saturation": 1.0,
    "Sharpness": 1.0,
    "HdrMode": controls.HdrModeEnum.Off,
}

cam.set_controls(controls_dict)

# Init capture
cam.start()
time.sleep(0.2)

cam_controls = cam.camera_controls
for name, (minv, maxv, current) in cam_controls.items():
    print(f"{name:25s}  min={minv}  max={maxv}  default={current}")

while True:
    frame = cam.capture_array("main")
    meta = cam.capture_metadata()

    fps = 1e6 / meta.get("FrameDuration", 33333)
    exp = meta.get("ExposureTime", 0) / 1000.0
    ag = meta.get("AnalogueGain", -1)

    text = f"FPS: {fps:.1f} Exp:{exp:.2f}ms AG:{ag:.2f}"
    cv2.putText(
        frame,
        text,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.imshow("Camera Preview", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.stop()
cv2.destroyAllWindows()

print("End capture.")
