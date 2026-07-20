import os
import json
import requests
import openai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class SEOPublisherAgent:
    def __init__(self):
        self.llm_api_key = os.environ.get('LLM_API_KEY')
        self.discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')
        
        self.fb_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        self.fb_page_id = os.environ.get('FACEBOOK_PAGE_ID')
        
        self.yt_creds_json = os.environ.get('YOUTUBE_CLIENT_SECRETS')

    def generate_seo_metadata(self):
        print("Agent 2: Generating SEO Metadata using OpenAI LLM...")
        if not self.llm_api_key:
            print("Warning: LLM_API_KEY not found. Using fallback metadata.")
            return {
                "title": "Gold Price Adventure for Kids! 🪙✨",
                "description": "Learn about the shiny gold price today! Subscribe to kidobum for more fun videos! #Gold #Kids #Learning",
                "tags": ["Kids", "Gold", "kidobum", "Education", "Fun"]
            }

        try:
            client = openai.OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=self.llm_api_key
            )
            response = client.chat.completions.create(
                model="z-ai/glm-5.1",
                messages=[
                    {"role": "system", "content": "You are an SEO expert for a kids YouTube channel named 'kidobum'."},
                    {"role": "user", "content": "Generate a JSON response with 'title', 'description', and 'tags' for a short vertical video about today's Gold Price."}
                ],
                temperature=1,
                top_p=1,
                max_tokens=1024
            )
            content = response.choices[0].message.content
            metadata = json.loads(content)
            print(f"Agent 2: SEO Metadata Generated -> {metadata['title']}")
            return metadata
        except Exception as e:
            print(f"Agent 2: LLM API error: {e}")
            raise

    def upload_to_facebook(self, video_path, metadata):
        print("Agent 2: Uploading to Facebook Reels...")
        if not self.fb_token or not self.fb_page_id:
            raise Exception("Facebook credentials missing.")

        # 1. Initialize Upload
        init_url = f"https://graph.facebook.com/v18.0/{self.fb_page_id}/video_reels"
        init_payload = {"upload_phase": "start", "access_token": self.fb_token}
        init_res = requests.post(init_url, data=init_payload).json()
        
        if 'video_id' not in init_res:
            raise Exception(f"Facebook Init failed: {init_res}")
            
        video_id = init_res['video_id']
        upload_url = init_res['upload_url']

        # 2. Upload Data
        headers = {"Authorization": f"OAuth {self.fb_token}"}
        with open(video_path, 'rb') as f:
            upload_res = requests.post(upload_url, headers=headers, data=f.read())
            
        # 3. Publish
        publish_url = f"https://graph.facebook.com/v18.0/{self.fb_page_id}/video_reels"
        publish_payload = {
            "access_token": self.fb_token,
            "video_id": video_id,
            "upload_phase": "finish",
            "video_state": "PUBLISHED",
            "description": f"{metadata['title']}\n\n{metadata['description']}"
        }
        pub_res = requests.post(publish_url, data=publish_payload).json()
        
        if 'success' in pub_res and pub_res['success']:
            fb_url = f"https://facebook.com/{self.fb_page_id}/videos/{video_id}"
            print(f"Agent 2: Uploaded to Facebook! URL: {fb_url}")
            return fb_url
        else:
            raise Exception(f"Facebook Publish failed: {pub_res}")

    def upload_to_youtube(self, video_path, metadata):
        print("Agent 2: Uploading to YouTube Shorts (kidobum)...")
        if not self.yt_creds_json:
            raise Exception("YouTube credentials missing.")

        creds_dict = json.loads(self.yt_creds_json)
        creds = Credentials.from_authorized_user_info(creds_dict)
        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {
                "title": metadata['title'],
                "description": metadata['description'],
                "tags": metadata['tags'],
                "categoryId": "27" # Education
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": True
            }
        }

        media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"YouTube Upload {int(status.progress() * 100)}%.")

        yt_url = f"https://youtube.com/shorts/{response['id']}"
        print(f"Agent 2: Uploaded to YouTube! URL: {yt_url}")
        return yt_url

    def notify_discord(self, fb_url, yt_url, metadata):
        print("Agent 2: Sending report to Discord...")
        if not self.discord_webhook:
            print("Agent 2: Discord Webhook URL not configured. Skipping.")
            return

        report = f"✅ **New Video Uploaded Successfully!**\n\n" \
                 f"**Title:** {metadata['title']}\n" \
                 f"**Facebook Reel:** {fb_url}\n" \
                 f"**YouTube Short:** {yt_url}\n"

        payload = {"content": report}
        try:
            requests.post(self.discord_webhook, json=payload)
            print("Agent 2: Discord Notification Sent.")
        except Exception as e:
            print(f"Agent 2: Failed to send Discord notification: {e}")

    def process(self, video_path):
        try:
            metadata = self.generate_seo_metadata()
            fb_url = self.upload_to_facebook(video_path, metadata)
            yt_url = self.upload_to_youtube(video_path, metadata)
            self.notify_discord(fb_url, yt_url, metadata)
            return True
        except Exception as e:
            print(f"Agent 2: Error during processing: {e}")
            return False
