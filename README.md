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