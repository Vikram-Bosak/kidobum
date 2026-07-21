import os
import json
import time
from tiktok_uploader.upload import upload_video

class TikTokUploadAgent:
    def __init__(self):
        # We will use the json state file that contains the cookies list
        self.state_file = os.path.join(os.path.dirname(__file__), "tiktok_auth_state.json")

    def generate_metadata(self, video_path):
        print(f"Agent 5 (TikTok): Generating SEO Metadata for '{video_path}'...")
        # Simulate LLM call
        time.sleep(1.5)
        title = "Learn Shapes with KidoBum! 🔵🟦🔺"
        tags = "#kidobum #kidslearning #shapes #nurseryrhymes #education #toddlers"
        return f"{title} {tags}"

    def upload_to_tiktok(self, video_path, metadata):
        print("Agent 5 (TikTok): Starting tiktok-uploader...")
        if not os.path.exists(self.state_file):
            raise Exception(f"Auth state file not found: {self.state_file}. Please run save_tiktok_cookies.py first.")

        try:
            with open(self.state_file, "r") as f:
                cookies_list = json.load(f)

            # tiktok-uploader uses headless=False by default to avoid bot detection
            failed_videos = upload_video(
                filename=video_path,
                description=metadata,
                cookies_list=cookies_list,
                headless=False,
                browser="chromium"
            )

            if failed_videos:
                print(f"Agent 5 (TikTok): tiktok-uploader failed for videos: {failed_videos}")
                raise Exception("tiktok-uploader reported failure.")
            
            print("Agent 5 (TikTok): Video successfully posted via tiktok-uploader!")
            return "https://www.tiktok.com/@kidobumnurseryrhymes"
            
        except Exception as e:
            print(f"Agent 5 (TikTok): tiktok-uploader error: {e}")
            raise e

    def process(self, video_path):
        try:
            metadata = self.generate_metadata(video_path)
            video_url = self.upload_to_tiktok(video_path, metadata)
            return {"platform": "TikTok", "url": video_url, "status": "Success"}
        except Exception as e:
            print(f"Agent 5 (TikTok): Error during processing: {e}")
            return {"status": "error", "error": str(e)}
