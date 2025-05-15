import torch
import cv2
import os
import time
import pygame
from dotenv import load_dotenv
from twilio.rest import Client
from pathlib import Path

# Load .env variables
load_dotenv()

CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.6))
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

# Department numbers
FIRE_DEPT_NUMBER = os.getenv("FIRE_DEPT_NUMBER")
POLICE_NUMBER = os.getenv("POLICE_NUMBER")
AMBULANCE_NUMBER = os.getenv("AMBULANCE_NUMBER")

# Twilio client setup
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Load models
print("[INFO] Loading YOLOv8 model...")
from ultralytics import YOLO

yolov8_model = YOLO('D:/notes/projects/major/models/yolov8_saved_model.pt')

# Use video file instead of webcam
cap = cv2.VideoCapture("C:/Users/vivek/OneDrive/Desktop/New folder/test_video.mp4")


def play_siren():
    print("[ALERT] Playing siren...")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("siren.mp3")
    pygame.mixer.music.play()

    # Wait for the sound to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def send_sms(activity):
    if activity.lower() == 'fire':
        number = FIRE_DEPT_NUMBER
        message_body = "🚨 Fire Alert: A fire has been detected on surveillance. Immediate response needed!"
    elif activity.lower() == 'fight':
        number = POLICE_NUMBER
        message_body = "🚨 Crime Alert: A fight is taking place. Police intervention required!"
    elif activity.lower() == 'accident':
        number = AMBULANCE_NUMBER
        message_body = "🚨 Accident Alert: A road accident has been detected. Medical assistance required!"
    elif activity.lower() == 'burglary':
        number = POLICE_NUMBER
        message_body = "🚨 Burglary Alert: A burglary is happening. Immediate police intervention needed!"
    elif activity.lower() == 'explosion':
        number = POLICE_NUMBER
        message_body = "🚨 Explosion Alert: An explosion has occurred. Immediate action required!"
    elif activity.lower() == 'fighting':
        number = POLICE_NUMBER
        message_body = "🚨 Fighting Alert: A violent altercation is taking place. Immediate police intervention required!"
    elif activity.lower() == 'ill-treatment':
        number = POLICE_NUMBER
        message_body = "🚨 Ill-treatment Alert: Abuse or ill-treatment has been detected. Police response required!"
    elif activity.lower() == 'traffic irregularities':
        number = POLICE_NUMBER
        message_body = "🚨 Traffic Irregularity Alert: Traffic rule violations detected. Immediate attention required!"
    elif activity.lower() == 'violence':
        number = POLICE_NUMBER
        message_body = "🚨 Violence Alert: Violent behavior detected. Police intervention required!"
    else:
        return

    print(f"[SMS] Sending to {number}: {message_body}")
    client.messages.create(
        body=message_body,
        from_=TWILIO_FROM_NUMBER,
        to=number
    )


print("[INFO] Starting video stream...")
already_alerted = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] End of video stream.")
        break

    yolov8_results = yolov8_model(frame)

    # Convert to DataFrame
    class_preds = yolov8_results[0].to_df()

    # Print the DataFrame to inspect the structure
    print(class_preds)  # Add this line to inspect the structure

    for _, row in class_preds.iterrows():
        activity = row['name']
        confidence = row['confidence']

        # Print the row to inspect for bounding box info
        print(row)  # Add this line to print the entire row and inspect where the box data might be

        # Try to extract the bounding box from other potential column names
        try:
            # Check if 'box' exists or try using a different name
            bbox = row.get('box', None)  # Use .get to avoid KeyError

            if bbox is None:
                print("Bounding box not found in 'box' column.")
                continue

            # If bounding box data exists, unpack it into xmin, ymin, xmax, ymax
            xmin, ymin, xmax, ymax = bbox[0], bbox[1], bbox[2], bbox[3]
            print(f"[INFO] BBox: {xmin}, {ymin}, {xmax}, {ymax}")  # Displaying the bounding box for debugging

        except Exception as e:
            print(f"[ERROR] Error extracting bounding box: {str(e)}")
            continue

        if confidence >= CONFIDENCE_THRESHOLD and activity.lower() in ['fire', 'fight', 'accident', 'burglary', 'explosion', 'fighting', 'ill-treatment', 'traffic irregularities', 'violence']:
            print(f"[DETECTED] {activity.upper()} | Confidence: {confidence:.2f} | BBox: {xmin}, {ymin}, {xmax}, {ymax}")

            if not already_alerted:
                play_siren()
                send_sms(activity)
                already_alerted = True
                time.sleep(5)

    # Display the frame (optional)
    cv2.imshow("Live Feed", frame)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()