import requests
import logging
import os
from datetime import datetime

class TelegramAlert:
    def __init__(self, config):
        self.config = config['telegram']
        self.token = self.config['bot_token']
        self.chat_id = self.config['chat_id']
        self.enabled = self.config['enabled']
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_alert(self, message, photo_path=None):
        if not self.enabled or self.token == "YOUR_BOT_TOKEN_HERE":
            logging.info("Telegram: Alert triggered but bot not configured or enabled.")
            print(f"--- TELEGRAM SIMULATION ---\n{message}\n---------------------------")
            return

        try:
            if photo_path and os.path.exists(photo_path):
                url = f"{self.base_url}/sendPhoto"
                with open(photo_path, 'rb') as photo:
                    files = {'photo': photo}
                    data = {'chat_id': self.chat_id, 'caption': message}
                    requests.post(url, data=data, files=files)
            else:
                url = f"{self.base_url}/sendMessage"
                data = {'chat_id': self.chat_id, 'text': message}
                requests.post(url, data=data)
        except Exception as e:
            logging.error(f"Telegram: Failed to send alert: {e}")

    def get_updates(self):
        if not self.enabled or self.token == "YOUR_BOT_TOKEN_HERE":
            return []
        
        try:
            url = f"{self.base_url}/getUpdates"
            # We use a small timeout to not block too long
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('result', [])
        except Exception as e:
            logging.error(f"Telegram: Failed to get updates: {e}")
        return []

    def handle_commands(self, system_status_callback):
        updates = self.get_updates()
        for update in updates:
            if 'message' in update and 'text' in update['message']:
                text = update['message']['text']
                chat_id = str(update['message']['chat']['id'])
                
                if chat_id != self.chat_id:
                    continue

                if text == "/status":
                    status = system_status_callback()
                    self.send_alert(f"SYSTEM STATUS:\n{status}")
                elif text == "/photo":
                    # This would need to trigger a capture
                    self.send_alert("Capturing latest photo...")
                elif text == "/help":
                    help_text = "/status - Check system\n/photo - Get latest photo\n/scan on/off - Control motor"
                    self.send_alert(help_text)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        msg = f"AIRCRAFT SPOTTED - TURRET ZERO\n\n"
        msg += f"Time: {now}\n"
        msg += f"Object: {detection_data['label']} (Confidence: {detection_data['confidence']*100:.1f}%)\n\n"
        
        pos = detection_data['gps']
        msg += f"CURRENT POSITION:\n"
        msg += f"- Latitude: {pos['lat']:.4f} N\n"
        msg += f"- Longitude: {pos['lon']:.4f} W\n"
        msg += f"- Altitude: {pos['alt']:,.0f} ft\n"
        msg += f"- Distance: {pos['distance_km']:.1f} km from you\n"
        msg += f"- Direction: {detection_data['direction']}\n"
        
        if 'prediction' in detection_data and detection_data['prediction']:
            pred = detection_data['prediction']
            msg += f"- Speed: {pred['speed_knots']:.0f} knots\n\n"
            msg += f"PREDICTED PATH:\n"
            for sec, coords in pred['predictions'].items():
                msg += f"- In {sec} seconds: {coords[0]:.4f} N, {coords[1]:.4f} W\n"
        
        google_maps_link = f"https://www.google.com/maps?q={pos['lat']},{pos['lon']}"
        msg += f"\nGoogle Maps: {google_maps_link}"
        
        return msg
