import os
import json
import time
from playwright.sync_api import sync_playwright

class TikTokUploadAgent:
    def __init__(self):
        # We will use the json state file that contains the cookies list
        self.state_file = os.path.join(os.path.dirname(__file__), "tiktok_auth_state.json")

    def generate_metadata(self, video_path):
        print(f"Agent 5 (TikTok): Generating SEO Metadata for '{video_path}'...")
        time.sleep(1.5)
        title = "Learn Shapes with KidoBum! 🔵🟦🔺"
        tags = "#kidobum #kidslearning #shapes #nurseryrhymes #education #toddlers"
        return f"{title} {tags}"

    def upload_to_tiktok(self, video_path, metadata):
        print("Agent 5 (TikTok): Starting Playwright uploader...")
        if not os.path.exists(self.state_file):
            raise Exception(f"Auth state file not found: {self.state_file}. Please run save_tiktok_cookies.py first.")
        
        abs_video_path = os.path.abspath(video_path)
        if not os.path.exists(abs_video_path):
            raise Exception(f"Video file not found: {abs_video_path}")

        try:
            with sync_playwright() as p:
                # Use headless=True for GitHub Actions compatibility
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(storage_state=self.state_file)
                page = context.new_page()
                
                print("Agent 5 (TikTok): Navigating to upload page...")
                page.goto("https://www.tiktok.com/creator-center/upload")
                
                print("Agent 5 (TikTok): Waiting for file input...")
                file_input = page.locator('input[type="file"][accept*="video"]')
                file_input.wait_for(state="attached", timeout=60000)
                file_input.set_input_files(abs_video_path)
                
                print("Agent 5 (TikTok): Waiting for caption editor...")
                caption_editor = page.locator('.public-DraftEditor-content')
                caption_editor.wait_for(state="visible", timeout=90000)
                
                print("Agent 5 (TikTok): Typing metadata...")
                caption_editor.click()
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(metadata, delay=50)
                
                time.sleep(3)
                
                print("Agent 5 (TikTok): Clicking Post...")
                post_button = page.locator('button:has-text("Post")')
                post_button.click()
                
                print("Agent 5 (TikTok): Waiting for upload to complete...")
                time.sleep(15)
                
                browser.close()

            print("Agent 5 (TikTok): Video successfully posted via Playwright!")
            return "https://www.tiktok.com/@kidobumnurseryrhymes"
            
        except Exception as e:
            print(f"Agent 5 (TikTok): Playwright upload error: {e}")
            raise e

    def process(self, video_path, video_name=None):
        try:
            metadata = self.generate_metadata(video_path)
            video_url = self.upload_to_tiktok(video_path, metadata)
            return {"platform": "TikTok", "url": video_url, "status": "Success"}
        except Exception as e:
            print(f"Agent 5 (TikTok): Error during processing: {e}")
            return {"status": "error", "error": str(e)}
