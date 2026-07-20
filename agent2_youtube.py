import os
import json
import time
import random
import openai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeUploadAgent:
    def __init__(self):
        self.llm_api_key = os.environ.get('LLM_API_KEY')
        self.yt_creds_json = os.environ.get('YOUTUBE_CLIENT_SECRETS')

    def random_delay(self, min_sec, max_sec):
        delay = random.uniform(min_sec, max_sec)
        print(f"Agent 2 (YouTube): Simulating human behavior with a delay of {delay:.2f} seconds...")
        time.sleep(delay)

    def generate_seo_metadata(self):
        print("Agent 2 (YouTube): Generating SEO Metadata using OpenAI LLM...")
        self.random_delay(2, 5) # Thinking delay
        
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
                model="meta/llama-3.1-8b-instruct",
                messages=[
                    {"role": "system", "content": "You are an expert YouTube SEO specialist for a kids channel named 'kidobum'. Focus on catchy titles, detailed kid-friendly descriptions, relevant tags and hashtags."},
                    {"role": "user", "content": "Generate a JSON response with 'title', 'description', and 'tags' (list of strings) for a short vertical video about today's Gold Price."}
                ],
                temperature=0.8,
                top_p=1,
                max_tokens=1024
            )
            content = response.choices[0].message.content
            
            import re
            # Use non-greedy match to extract just the first JSON object
            match = re.search(r'\{.*?\}', content, re.DOTALL)
            if match:
                json_str = match.group(0)
            else:
                json_str = content
                
            try:
                metadata = json.loads(json_str)
            except Exception as e:
                print(f"Agent 2 (YouTube): JSON Parsing Error: {e}\nRaw LLM Content:\n{content}")
                raise

            print(f"Agent 2 (YouTube): SEO Metadata Generated -> Title: {metadata.get('title')}")
            return metadata
        except Exception as e:
            print(f"Agent 2 (YouTube): LLM API error: {e}")
            raise

    def upload_to_youtube(self, video_path, metadata):
        print("Agent 2 (YouTube): Uploading to YouTube Shorts...")
        if not self.yt_creds_json:
            raise Exception("YouTube credentials missing.")

        self.random_delay(5, 10) # Delay before upload starts
        
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
                self.random_delay(0.5, 2.5) # Network jitter during chunk upload

        yt_url = f"https://youtube.com/shorts/{response['id']}"
        print(f"Agent 2 (YouTube): Uploaded to YouTube! URL: {yt_url}")
        return yt_url

    def process(self, video_path):
        try:
            metadata = self.generate_seo_metadata()
            yt_url = self.upload_to_youtube(video_path, metadata)
            return {"status": "success", "url": yt_url, "metadata": metadata}
        except Exception as e:
            print(f"Agent 2 (YouTube): Error during processing: {e}")
            return {"status": "error", "error": str(e)}
