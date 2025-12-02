import time
from typing import Any, Dict

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from libcamera import controls
from picamera2 import Picamera2

matplotlib.use("TkAgg")

# Initialize Camera
cam = Picamera2()
print(cam.sensor_modes)
# Configuration
config = cam.create_preview_configuration(
    main={
        "size": (1536, 864),
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
    "AnalogueGain": 1.0,
    "ExposureTime": 8,
    "FrameDurationLimits": (8333, 8333),
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


# Take N consecutive frames
MAX_FRAMES = 10

frame = cam.capture_array("main")
height, width = frame.shape[:2]
frames = np.zeros((MAX_FRAMES, height, width))
for i in range(MAX_FRAMES):
    frame = cam.capture_array("main")
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frames[i, :, :] = frame

stacked_frames = frames.reshape(height * MAX_FRAMES, width)

averaged_frames = np.mean(stacked_frames, axis=1)

fig, ax = plt.subplots(1, 2, figsize=(16, 8), constrained_layout=True)
ax[0].plot(averaged_frames)
ax[0].set_title(f"Column averaged signal of {MAX_FRAMES} consecutive frames")
ax[0].set_box_aspect(height / width)

meta: Dict[str, Any] = cam.capture_metadata()

fps = 1e6 / meta.get("FrameDuration", 33333)
exp = meta.get("ExposureTime", 0) / 1000.0
ag = meta.get("AnalogueGain", -1)

ax[1].imshow(frame)
ax[1].set_title(f"FPS: {fps:.1f} Exp:{exp:.4f}ms AG:{ag:.2f}")


def on_key(event):
    print(f"Pressed: {event.key}")
    if event.key == "q":
        plt.close(fig)


fig.canvas.mpl_connect("key_press_event", on_key)
plt.show()
