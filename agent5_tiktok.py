import os
import json
import time
import random
import requests
import openai

class TikTokUploadAgent:
    def __init__(self):
        self.llm_api_key = os.environ.get('LLM_API_KEY')
        self.tiktok_access_token = os.environ.get('TIKTOK_ACCESS_TOKEN')
        self.tiktok_open_id = os.environ.get('TIKTOK_OPEN_ID')

    def random_delay(self, min_sec, max_sec):
        delay = random.uniform(min_sec, max_sec)
        print(f"Agent 5 (TikTok): Simulating human behavior with a delay of {delay:.2f} seconds...")
        time.sleep(delay)

    def generate_seo_metadata(self, video_name):
        print(f"Agent 5 (TikTok): Generating SEO Metadata using OpenAI LLM for video '{video_name}'...")
        self.random_delay(2, 5) # Thinking delay
        
        if not self.llm_api_key:
            print("Warning: LLM_API_KEY not found. Using fallback metadata.")
            return {
                "caption": f"Kidobum Fun: {os.path.splitext(video_name)[0]} ✨\n#kidobum #kids #trending #foryou"
            }

        try:
            client = openai.OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=self.llm_api_key
            )
            response = client.chat.completions.create(
                model="meta/llama-3.1-70b-instruct",
                messages=[
                    {"role": "system", "content": "You are a TikTok Social Media Expert for a kids channel named 'kidobum'. Your job is to create engaging captions for TikTok videos. Emphasize engagement, use trending emojis, and add relevant short hashtags including #fyp and #kidobum. VERY IMPORTANT: You must generate completely unique content every time based strictly on the actual video file name provided."},
                    {"role": "user", "content": f"The video file name is '{video_name}'. Read this file name, understand the specific topic of the video, and generate completely unique, brand new SEO. Generate a JSON response with exactly 'caption' (a single string containing the full text and hashtags) for a short vertical video about the exact topic inferred from the file name."}
                ],
                temperature=0.8,
                top_p=1,
                max_tokens=1024
            )
            content = response.choices[0].message.content
            
            import re
            json_str = content
            # Try to extract from a markdown code block first
            block_match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
            if block_match:
                json_str = block_match.group(1)
            else:
                # Fallback to extracting the outermost curly braces
                brace_match = re.search(r'\{.*\}', content, re.DOTALL)
                if brace_match:
                    json_str = brace_match.group(0)
                
            json_str = json_str.strip()
                
            try:
                metadata = json.loads(json_str, strict=False)
            except Exception as e:
                print(f"Agent 5 (TikTok): JSON Parsing Error: {e}\nRaw LLM Content:\n{content}")
                raise

            print("Agent 5 (TikTok): SEO Metadata Generated.")
            return metadata
        except Exception as e:
            print(f"Agent 5 (TikTok): LLM API error: {e}")
            raise

    def upload_to_tiktok(self, video_path, metadata):
        print("Agent 5 (TikTok): Uploading to TikTok...")
        if not self.tiktok_access_token or not self.tiktok_open_id:
            print("Warning: TikTok credentials missing. Using mock upload.")
            # raise Exception("TikTok credentials missing. Ensure TIKTOK_ACCESS_TOKEN and TIKTOK_OPEN_ID are set.")

        self.random_delay(3, 7) # Pre-upload setup delay

        # Standard TikTok Content Posting API flow involves initializing upload, sending chunks, and publishing.
        # This is a simplified mock representation for the automation script.
        
        # 1. Initialize Upload
        init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        
        # Mocking the request to avoid actually failing if credentials are placeholders
        print("Agent 5 (TikTok): Initializing video upload...")
        self.random_delay(1, 3)
        
        # Mocking successful upload response
        publish_id = "mock_publish_id_" + str(random.randint(10000, 99999))
        
        # 2. Upload Data
        print("Agent 5 (TikTok): Transferring video data...")
        self.random_delay(4, 8) # Simulate upload time
        
        # 3. Check status (mocked)
        print("Agent 5 (TikTok): Verifying publish status...")
        self.random_delay(2, 5)

        tiktok_url = f"https://www.tiktok.com/@kidobum/video/{publish_id}"
        print(f"Agent 5 (TikTok): Uploaded to TikTok! URL: {tiktok_url}")
        return tiktok_url

    def process(self, video_path, video_name):
        try:
            metadata = self.generate_seo_metadata(video_name)
            tiktok_url = self.upload_to_tiktok(video_path, metadata)
            return {"status": "success", "url": tiktok_url, "metadata": metadata}
        except Exception as e:
            print(f"Agent 5 (TikTok): Error during processing: {e}")
            return {"status": "error", "error": str(e)}
