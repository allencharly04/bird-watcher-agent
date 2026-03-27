import cv2
import requests
import time
import os
from dotenv import load_dotenv
from ultralytics import YOLO

# --- BULLETPROOF KEY LOADING ---
# Find the exact folder where this Python file is saved and load the .env file
project_folder = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(project_folder, ".env"))

# --- CONFIGURATION ---
CAMERA_URL = "http://192.168.0.236:8080/video" 

# Grabbing the keys from your secret .env file!
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Load the YOLOv8 AI Model 
model = YOLO('yolov8n.pt') 

# Time tracking so it doesn't spam you with 100 messages a minute
last_alert_time = 0
alert_cooldown_seconds = 2 

def send_telegram_photo(image_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as img:
        files = {"photo": img}
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": "🐦 Bird detected at the feeder!"}

        response = requests.post(url, files=files, data=data)
        print("Telegram says:", response.text)

def main():
    global last_alert_time
    
    # Connect to the tablet's video stream
    cap = cv2.VideoCapture(CAMERA_URL)

    if not cap.isOpened():
        print("Error: Could not connect to tablet camera.")
        return

    print("Agent started. Watching for birds...")

    while True:
        # Clear the buffer to eliminate lag and "overread" errors
        for _ in range(4): 
            cap.grab()
            
        ret, frame = cap.read()
        if not ret:
            continue

        # Lower confidence to 0.35 to catch more birds
        results = model(frame, classes=[14], conf=0.35, verbose=False)

        # Check if any birds were found
        if len(results[0].boxes) > 0:
            
            # Record the current time
            current_time = time.time()
            
            # Check if we are past the cooldown to prevent spam
            if current_time - last_alert_time > alert_cooldown_seconds:
                print("Bird detected! Sending alert...")
                
                # Draw boxes around the bird and save the image
                annotated_frame = results[0].plot()
                cv2.imwrite("bird_alert.jpg", annotated_frame)
                
                # Send to Telegram 
                send_telegram_photo("bird_alert.jpg")
                
                last_alert_time = current_time

        # Optional: Show the video feed on your computer screen
        cv2.imshow("Bird Watcher", frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()