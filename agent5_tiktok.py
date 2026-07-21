import os
import json
import time
import requests

class TikTokUploadAgent:
    def __init__(self):
        # Read the Webhook URL from the environment or default to a dummy URL
        self.webhook_url = os.environ.get('N8N_WEBHOOK_URL', 'YOUR_N8N_WEBHOOK_URL_HERE')

    def generate_metadata(self, video_path):
        print(f"Agent 5 (TikTok API): Generating SEO Metadata for '{video_path}'...")
        # Simulate LLM call
        time.sleep(1.5)
        title = "Learn Shapes with KidoBum! 🔵🟦🔺"
        tags = "#kidobum #kidslearning #shapes #nurseryrhymes #education #toddlers"
        return f"{title} {tags}"

    def upload_to_tiktok(self, video_path, metadata):
        print("Agent 5 (TikTok API): Forwarding video to n8n Webhook...")
        
        abs_video_path = os.path.abspath(video_path)
        if not os.path.exists(abs_video_path):
            raise Exception(f"Video file not found: {abs_video_path}")

        if self.webhook_url == 'YOUR_N8N_WEBHOOK_URL_HERE':
            print("Warning: N8N_WEBHOOK_URL is not set. Simulating a successful API call.")
            time.sleep(2)
            return "https://www.tiktok.com/@kidobumnurseryrhymes (Simulated via n8n)"

        try:
            # Prepare multipart/form-data for the Webhook
            files = {
                'video': (os.path.basename(abs_video_path), open(abs_video_path, 'rb'), 'video/mp4')
            }
            data = {
                'metadata': metadata,
                'platform': 'tiktok'
            }
            
            print(f"Agent 5 (TikTok API): Sending POST request to {self.webhook_url}...")
            response = requests.post(self.webhook_url, files=files, data=data)
            
            if response.status_code == 200:
                print("Agent 5 (TikTok API): Video successfully forwarded to n8n Webhook!")
                # Optional: Parse response if your n8n workflow returns JSON
                return "https://www.tiktok.com/@kidobumnurseryrhymes (Handled by n8n)"
            else:
                raise Exception(f"Failed to trigger n8n Webhook. Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            print(f"Agent 5 (TikTok API): Webhook error: {e}")
            raise e

    def process(self, video_path, video_name=None):
        try:
            metadata = self.generate_metadata(video_path)
            video_url = self.upload_to_tiktok(video_path, metadata)
            return {"platform": "TikTok", "url": video_url, "status": "Success"}
        except Exception as e:
            print(f"Agent 5 (TikTok API): Error during processing: {e}")
            return {"status": "error", "error": str(e)}
