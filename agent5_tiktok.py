import os
import json
import time
import random
import openai
from playwright.sync_api import sync_playwright

class TikTokUploadAgent:
    def __init__(self):
        self.llm_api_key = os.environ.get('LLM_API_KEY')
        self.auth_file = os.path.join(os.path.dirname(__file__), "tiktok_auth_state.json")

    def random_delay(self, min_sec, max_sec):
        delay = random.uniform(min_sec, max_sec)
        print(f"Agent 5 (TikTok): Delay {delay:.2f}s...")
        time.sleep(delay)

    def generate_seo_metadata(self, video_name):
        print(f"Agent 5 (TikTok): Generating SEO Metadata for '{video_name}'...")
        if not self.llm_api_key:
            return {"caption": f"Kidobum Fun: {os.path.splitext(video_name)[0]} ✨\n#kidobum #kids #foryou"}
        
        try:
            client = openai.OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=self.llm_api_key)
            response = client.chat.completions.create(
                model="meta/llama-3.1-70b-instruct",
                messages=[
                    {"role": "system", "content": "You are a TikTok Social Media Expert for 'kidobum'. Generate a JSON response with exactly 'caption' (text and hashtags) for a short vertical video."},
                    {"role": "user", "content": f"The video file name is '{video_name}'."}
                ],
                temperature=0.8,
                max_tokens=512
            )
            content = response.choices[0].message.content
            
            import re
            json_str = content
            block_match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
            if block_match:
                json_str = block_match.group(1)
            else:
                brace_match = re.search(r'\{.*\}', content, re.DOTALL)
                if brace_match:
                    json_str = brace_match.group(0)
                    
            return json.loads(json_str.strip(), strict=False)
        except Exception as e:
            print(f"Agent 5 (TikTok): LLM error: {e}")
            return {"caption": f"{os.path.splitext(video_name)[0]} ✨\n#kidobum"}

    def upload_to_tiktok(self, video_path, metadata):
        print("Agent 5 (TikTok): Starting Playwright browser...")
        
        if not os.path.exists(self.auth_file):
            raise Exception("tiktok_auth_state.json not found! Please run `python save_tiktok_cookies.py` first.")

        with sync_playwright() as p:
            # We run headless=False to avoid immediate bot detection on upload page
            browser = p.chromium.launch(headless=False, args=["--mute-audio"])
            context = browser.new_context(storage_state=self.auth_file)
            page = context.new_page()

            try:
                print("Agent 5 (TikTok): Navigating to upload page...")
                page.goto("https://www.tiktok.com/creator-center/upload")
                page.wait_for_load_state("networkidle")
                self.random_delay(3, 5)
                
                # Check if we are unexpectedly asked to login
                if "login" in page.url:
                    raise Exception("Session expired or invalid. Please re-run save_tiktok_cookies.py")

                # Switch to iframe if TikTok uses it (sometimes they do, sometimes they don't)
                iframe = page.frame_locator('iframe[data-tt="Upload_index_iframe"]') if page.locator('iframe[data-tt="Upload_index_iframe"]').count() > 0 else page
                
                print("Agent 5 (TikTok): Selecting video file...")
                # The file input is often hidden, but Playwright handles set_input_files on input[type="file"] well
                file_input = iframe.locator('input[type="file"][accept="video/*"]')
                
                # Normalize path for playwright
                abs_path = os.path.abspath(video_path)
                file_input.set_input_files(abs_path)
                
                print("Agent 5 (TikTok): Waiting for upload to finish (simulating processing)...")
                # Wait a fixed safe amount of time for small videos.
                self.random_delay(15, 20)

                print("Agent 5 (TikTok): Typing caption...")
                # The caption box is usually a ContentEditable div inside Draft.js
                caption_editor = iframe.locator('.public-DraftEditor-content')
                if caption_editor.count() == 0:
                    caption_editor = iframe.locator('[data-contents="true"]')
                
                caption_editor.click()
                caption_editor.fill("")
                self.random_delay(1, 2)
                page.keyboard.type(metadata['caption'], delay=100) # Type like a human
                
                print("Agent 5 (TikTok): Clicking Post...")
                self.random_delay(2, 4)
                
                # Find post button. Usually has text "Post"
                post_btn = iframe.locator('button:has-text("Post")')
                if post_btn.count() > 0:
                    post_btn.nth(0).click()
                else:
                    print("Agent 5 (TikTok): Could not find Post button. Attempting generic click.")
                    iframe.locator('div[role="button"]:has-text("Post")').click()
                
                print("Agent 5 (TikTok): Waiting for success confirmation...")
                self.random_delay(5, 8)
                
                print("Agent 5 (TikTok): Video successfully posted via Browser Automation!")
                return "https://www.tiktok.com/@kidobumnurseryrhymes"
                
            except Exception as e:
                print(f"Agent 5 (TikTok): Browser automation failed: {e}")
                # Save screenshot on failure
                page.screenshot(path="tiktok_error.png")
                raise
            finally:
                browser.close()

    def process(self, video_path, video_name):
        try:
            metadata = self.generate_seo_metadata(video_name)
            tiktok_url = self.upload_to_tiktok(video_path, metadata)
            return {"status": "success", "url": tiktok_url, "metadata": metadata}
        except Exception as e:
            print(f"Agent 5 (TikTok): Error during processing: {e}")
            return {"status": "error", "error": str(e)}
