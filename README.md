# Install system libraries
```shell
sudo apt install python3-picamera2
```
# Create a virtualenvironment
Using uv and system-packages
```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --system-site-packages --python /usr/bin/python3
```
# Hardware
Using Raspberry Pi Camera Module v3
| Param | Value |
| ----  | ----  |
| Still resolution | 4608x2592 |
| Sensor size  / diagonal | 7.4mm (1/2.43") |
| Pixel size | 1.4um x 1.4 um |

## Evaluation
Min exposure time: 36us @ 1280x720 - Filtered BW 27.777 kHz - 13.9kHz