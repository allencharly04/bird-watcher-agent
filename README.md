# 🐦 Bird Feeder Watcher 

A real-time computer vision agent that monitors a bird feeder using a live camera stream, detects birds using YOLOv8, and instantly sends a photo alert to your phone via Telegram.

---

## How It Works

1. Connects to a live video stream (e.g. an Android tablet running IP Webcam)
2. Runs every frame through a **YOLOv8n** object detection model, filtering for the "bird" class
3. When a bird is detected, draws a bounding box annotation and saves the frame
4. Sends the annotated photo to a **Telegram chat** with a caption
5. A cooldown timer prevents notification spam

---

## Tech Stack

| Component | Tool |
|---|---|
| Object Detection | [YOLOv8](https://github.com/ultralytics/ultralytics) (Ultralytics) |
| Video Capture | OpenCV (`cv2.VideoCapture`) |
| Notifications | Telegram Bot API |
| Camera Source | IP Webcam (Android) or any MJPEG stream |
| Config Management | `python-dotenv` |

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/allencharly04/bird-watcher-agent.git
cd bird-watcher-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the YOLOv8 model
The model file is not included in this repo (it's ~6MB). It will be **auto-downloaded** the first time you run the script, or you can download it manually:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### 4. Create your `.env` file
```bash
cp .env.example .env
```
Then fill in your credentials:
```
TELEGRAM_BOT_TOKEN=your_bot_token_from_@BotFather
TELEGRAM_CHAT_ID=your_chat_id
```

> **How to get these:** Create a bot via [@BotFather](https://t.me/BotFather) on Telegram. Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot).

### 5. Set your camera URL
In `main.py`, update this line with your stream's IP address:
```python
CAMERA_URL = "http://<your-tablet-ip>:8080/video"
```

### 6. Run the agent
```bash
python main.py
```

Press `Q` in the video window to stop.

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `alert_cooldown_seconds` | `2` | Minimum seconds between alerts |
| `conf` | `0.35` | Detection confidence threshold (lower = more sensitive) |
| `classes` | `[14]` | COCO class ID for "bird" |

---

## Example Alert

When a bird is detected, you receive a Telegram message like this:

> 🐦 **Bird detected at the feeder!**
> *(annotated photo attached)*

---

## Project Structure

```
bird-watcher-agent/
├── main.py           # Main agent loop
├── requirements.txt  # Python dependencies
├── .env.example      # Credentials template (safe to commit)
├── .gitignore        # Keeps .env and model weights out of git
└── README.md
```
