import os
import json
import time
import random
import requests
import openai

class FacebookUploadAgent:
    def __init__(self):
        self.llm_api_key = os.environ.get('LLM_API_KEY')
        self.fb_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        self.fb_page_id = os.environ.get('FACEBOOK_PAGE_ID')

    def random_delay(self, min_sec, max_sec):
        delay = random.uniform(min_sec, max_sec)
        print(f"Agent 3 (Facebook): Simulating human behavior with a delay of {delay:.2f} seconds...")
        time.sleep(delay)

    def generate_seo_metadata(self):
        print("Agent 3 (Facebook): Generating SEO Metadata using OpenAI LLM...")
        self.random_delay(2, 5) # Thinking delay
        
        if not self.llm_api_key:
            print("Warning: LLM_API_KEY not found. Using fallback metadata.")
            return {
                "caption": "Gold Price Adventure for Kids! 🪙✨\nLearn about the shiny gold price today! Subscribe to kidobum for more fun videos! #Gold #Kids #Learning #kidobum #FacebookReels"
            }

        try:
            client = openai.OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=self.llm_api_key
            )
            response = client.chat.completions.create(
                model="meta/llama3-8b-instruct",
                messages=[
                    {"role": "system", "content": "You are a Facebook Social Media Expert for a kids page named 'kidobum'. Your job is to create engaging captions for Facebook Reels. Emphasize engagement, use emojis, and add relevant hashtags."},
                    {"role": "user", "content": "Generate a JSON response with 'caption' (a string containing the full text and hashtags) for a short vertical video about today's Gold Price."}
                ],
                temperature=0.8,
                top_p=1,
                max_tokens=1024
            )
            content = response.choices[0].message.content
            content = content.replace("```json", "").replace("```", "").strip()
            metadata = json.loads(content)
            print("Agent 3 (Facebook): SEO Metadata Generated.")
            return metadata
        except Exception as e:
            print(f"Agent 3 (Facebook): LLM API error: {e}")
            raise

    def upload_to_facebook(self, video_path, metadata):
        print("Agent 3 (Facebook): Uploading to Facebook Reels...")
        if not self.fb_token or not self.fb_page_id:
            raise Exception("Facebook credentials missing.")

        self.random_delay(4, 8) # Pre-upload setup delay

        # 1. Initialize Upload
        init_url = f"https://graph.facebook.com/v18.0/{self.fb_page_id}/video_reels"
        init_payload = {"upload_phase": "start", "access_token": self.fb_token}
        init_res = requests.post(init_url, data=init_payload).json()
        
        if 'video_id' not in init_res:
            raise Exception(f"Facebook Init failed: {init_res}")
            
        video_id = init_res['video_id']
        upload_url = init_res['upload_url']

        self.random_delay(2, 5) # Delay between phases

        # 2. Upload Data
        headers = {"Authorization": f"OAuth {self.fb_token}"}
        with open(video_path, 'rb') as f:
            requests.post(upload_url, headers=headers, data=f.read())
            
        self.random_delay(5, 12) # Delay to let FB process chunk

        # 3. Publish
        publish_url = f"https://graph.facebook.com/v18.0/{self.fb_page_id}/video_reels"
        publish_payload = {
            "access_token": self.fb_token,
            "video_id": video_id,
            "upload_phase": "finish",
            "video_state": "PUBLISHED",
            "description": metadata.get('caption', 'Kidobum Video!')
        }
        pub_res = requests.post(publish_url, data=publish_payload).json()
        
        if 'success' in pub_res and pub_res['success']:
            fb_url = f"https://facebook.com/{self.fb_page_id}/videos/{video_id}"
            print(f"Agent 3 (Facebook): Uploaded to Facebook! URL: {fb_url}")
            return fb_url
        else:
            raise Exception(f"Facebook Publish failed: {pub_res}")

    def process(self, video_path):
        try:
            metadata = self.generate_seo_metadata()
            fb_url = self.upload_to_facebook(video_path, metadata)
            return {"status": "success", "url": fb_url, "metadata": metadata}
        except Exception as e:
            print(f"Agent 3 (Facebook): Error during processing: {e}")
            return {"status": "error", "error": str(e)}
