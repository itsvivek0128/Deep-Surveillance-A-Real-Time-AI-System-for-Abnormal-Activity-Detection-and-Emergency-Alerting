# 🔍 Deep Surveillance: A Real-Time AI System for Abnormal Activity Detection and Emergency Alerting

This project is an AI-powered real-time surveillance system designed to detect abnormal activities such as violence, accidents, and fire, and immediately alert relevant emergency services using Twilio SMS and live dashboard monitoring.

---

## 🚨 Features

- 🎯 Real-time **Object Detection** and **Abnormal Activity Classification** using YOLOv8
- 🛎️ Local **audio alerts** (siren) for high-confidence detections
- 📩 **SMS notifications** to:
  - 🚒 Fire Department for fire-related activities
  - 🚓 Police for crimes like burglary, fighting, or violence
  - 🚑 Ambulance for accidents and medical emergencies
- 🌐 Live **Flask Dashboard** with real-time video feed
- 🗃️ Activity log (in-memory) for the last 10 alerts
- ✅ Configurable **confidence threshold** to reduce false alarms
- 📍 Tagged **location** in alerts using environment variables

---

## 🧠 Abnormal Activities Detected

- Arrest
- Attack
- Burglary
- Explosion
- Fighting
- Fire-raising
- Ill-treatment
- Traffic Irregularities
- Violence

---

## 📁 Project Structure

```
DeepSurveillance_Package/
├── app.py                        # Main Flask app
├── yolov8_saved_model.pt         # Trained YOLOv8 model
├── test_video.mp4                # Sample video input
├── templates/
│   └── index.html                # Dashboard HTML UI
├── .env                          # Environment configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/deep-surveillance-ai.git
cd deep-surveillance-ai
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create `.env` file with these keys:**

```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM_NUMBER=+1234567890
FIRE_DEPT_NUMBER=+911234567890
POLICE_NUMBER=+911234567891
AMBULANCE_NUMBER=+911234567892
CONFIDENCE_THRESHOLD=0.6
LOCATION_TAG=Hyderabad City
```

4. **Run the application**

```bash
python app.py
```

Visit `http://localhost:5000` to view the dashboard.

---

## 🧪 Model Used

- **YOLOv8** (custom trained)
  - File: `yolov8_saved_model.pt`
  - Used for multi-activity classification

---

## ✅ Requirements

- Python 3.8+
- Flask
- OpenCV
- Ultralytics
- Twilio
- python-dotenv

Install via:

```bash
pip install -r requirements.txt
```

---

## 📸 Screenshots

> *(You can add live detection screenshots here)*

---

## 🧑‍💻 Author

- **Your Name**
- GitHub: [@your_username](https://github.com/your_username)
- Email: your_email@example.com

---

## 📄 License

This project is licensed under the MIT License.

---

## 🧠 Acknowledgements

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLOv8
- [Twilio](https://www.twilio.com/) for SMS APIs