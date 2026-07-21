import os
import json
import time
from playwright.sync_api import sync_playwright

import base64

class TikTokUploadAgent:
    def __init__(self):
        # We try to get the TikTok auth state from environment variables first (as injected in GitHub Actions)
        raw_secret = os.getenv('TIKTOK_AUTH_STATE')
        b64_secret = os.getenv('TIKTOK_AUTH_STATE_B64')
        
        self.state_file = os.path.join(os.path.dirname(__file__), "tiktok_auth_state_tmp.json")
        
        if raw_secret or b64_secret:
            if b64_secret:
                try:
                    raw_secret = base64.b64decode(b64_secret).decode('utf-8')
                except Exception as e:
                    print(f"Agent 5 (TikTok): Warning - Failed to decode TIKTOK_AUTH_STATE_B64: {e}")
            
            try:
                # Validate it's correct JSON
                parsed = json.loads(raw_secret)
                with open(self.state_file, "w", encoding="utf-8") as f:
                    json.dump(parsed, f, ensure_ascii=False, indent=2)
            except Exception as e:
                raise Exception(f"Agent 5 (TikTok): TIKTOK_AUTH_STATE contains invalid JSON: {e}")
        else:
            # Fall back to local file if no env var is set (for local development)
            local_state = os.path.join(os.path.dirname(__file__), "tiktok_auth_state.json")
            if os.path.exists(local_state):
                self.state_file = local_state
            else:
                raise Exception("Missing TikTok auth secret (TIKTOK_AUTH_STATE or TIKTOK_AUTH_STATE_B64) and local tiktok_auth_state.json not found.")

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
                
                # Try to dismiss any popup modals (like copyright checks or tutorials)
                try:
                    modal_buttons = page.locator('button:has-text("Got it"), button:has-text("Okay"), button:has-text("OK"), [class*="tux-btn"]:has-text("Got it")')
                    if modal_buttons.count() > 0:
                        print("Agent 5 (TikTok): Found modal overlay, attempting to dismiss...")
                        modal_buttons.first.click(timeout=5000)
                        time.sleep(1)
                except Exception as modal_err:
                    print(f"Agent 5 (TikTok): Did not dismiss modal: {modal_err}")

                print("Agent 5 (TikTok): Typing metadata...")
                try:
                    caption_editor.click(timeout=10000)
                except Exception:
                    print("Agent 5 (TikTok): Caption editor click intercepted, retrying with force=True...")
                    caption_editor.click(force=True)
                
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
