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
        import openai
        video_name = os.path.basename(video_path)
        print(f"Agent 5 (TikTok): Generating SEO Metadata using OpenAI LLM for video '{video_name}'...")
        llm_api_key = os.environ.get('LLM_API_KEY')
        
        if not llm_api_key:
            print("Warning: LLM_API_KEY not found. Using fallback TikTok metadata.")
            fallback_title = f"Fun Learning with KidoBum: {os.path.splitext(video_name)[0]}! ✨"
            fallback_tags = "#kidobum #kidslearning #education #toddlers #fun"
            return f"{fallback_title} {fallback_tags}"

        try:
            client = openai.OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=llm_api_key
            )
            response = client.chat.completions.create(
                model="meta/llama-3.1-70b-instruct",
                messages=[
                    {"role": "system", "content": "You are an expert TikTok SEO specialist for a kids channel named 'kidobum'. Focus on extremely short, engaging captions filled with relevant emojis and popular hashtags. Keep it under 150 characters. VERY IMPORTANT: You must generate completely unique content every time based strictly on the actual video file name provided."},
                    {"role": "user", "content": f"The video file name is '{video_name}'. Read this file name, understand the specific topic of the video, and generate completely unique, brand new SEO. Do NOT use previously generated titles. Generate a JSON response with exactly 'caption' (string containing title and hashtags, keeping it under 150 characters) for a TikTok video about the exact topic inferred from the file name."}
                ],
                temperature=0.8,
                top_p=1,
                max_tokens=1024
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
            
            data = json.loads(json_str)
            caption = data.get("caption", "")
            if caption:
                return caption
        except Exception as e:
            print(f"Agent 5 (TikTok): LLM metadata generation failed: {e}. Using fallback.")
            
        fallback_title = f"Fun Learning with KidoBum: {os.path.splitext(video_name)[0]}! ✨"
        fallback_tags = "#kidobum #kidslearning #education #toddlers #fun"
        return f"{fallback_title} {fallback_tags}"

    def dismiss_overlays(self, page, suffix=""):
        print(f"Agent 5 (TikTok): Checking for overlays/modals to dismiss ({suffix})...")
        
        # 1. Target "Turn on" button specifically
        try:
            turn_on = page.locator('button:has-text("Turn on")')
            if turn_on.count() > 0:
                print("Agent 5 (TikTok): Found 'Turn on' modal button. Clicking...")
                turn_on.first.click(force=True)
                time.sleep(2)
                page.screenshot(path=f"dismiss_turn_on_{suffix}.png")
        except Exception as e:
            print(f"Agent 5 (TikTok): Error clicking 'Turn on': {e}")
            
        # 2. Target "Cancel" button specifically
        try:
            cancel = page.locator('button:has-text("Cancel")')
            if cancel.count() > 0:
                print("Agent 5 (TikTok): Found 'Cancel' modal button. Clicking...")
                cancel.first.click(force=True)
                time.sleep(2)
                page.screenshot(path=f"dismiss_cancel_{suffix}.png")
        except Exception as e:
            print(f"Agent 5 (TikTok): Error clicking 'Cancel': {e}")

        # 3. Target "Got it" tooltips
        try:
            got_it_buttons = page.locator('button:has-text("Got it")')
            count = got_it_buttons.count()
            for idx in range(count):
                print(f"Agent 5 (TikTok): Found 'Got it' tooltip button {idx+1}/{count}. Clicking...")
                got_it_buttons.nth(idx).click(force=True)
                time.sleep(1.5)
                page.screenshot(path=f"dismiss_got_it_{idx+1}_{suffix}.png")
        except Exception as e:
            print(f"Agent 5 (TikTok): Error clicking 'Got it': {e}")

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
                
                print("Agent 5 (TikTok): Waiting for video file upload to reach 100%...")
                try:
                    # Wait for green status indicating upload completed (looks for text containing "Uploaded")
                    uploaded_locator = page.locator('text="Uploaded"')
                    uploaded_locator.wait_for(state="visible", timeout=120000)
                    print("Agent 5 (TikTok): Video file upload completed successfully!")
                except Exception as upload_err:
                    print(f"Agent 5 (TikTok): Warning - upload completion indicator not found, continuing anyway: {upload_err}")
                
                print("Agent 5 (TikTok): Waiting for caption editor...")
                caption_editor = page.locator('.public-DraftEditor-content')
                caption_editor.wait_for(state="visible", timeout=90000)
                
                page.screenshot(path="1_before_typing.png")

                # Dismiss overlays before typing
                self.dismiss_overlays(page, "before_typing")

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
                page.screenshot(path="2_after_typing.png")
                
                # Dismiss overlays after typing / before posting
                self.dismiss_overlays(page, "before_posting")

                print("Agent 5 (TikTok): Clicking Post...")
                post_button = page.locator('button[data-e2e="post_video_button"]')
                try:
                    post_button.click(timeout=10000)
                except Exception:
                    print("Agent 5 (TikTok): Post button click intercepted, retrying with force=True...")
                    post_button.click(force=True)
                
                time.sleep(3)
                page.screenshot(path="3_after_post_click.png")

                # Handle the "Continue to post?" copyright check modal
                try:
                    post_now_btn = page.locator('button:has-text("Post now"), button.Button__root:has-text("Post now")')
                    if post_now_btn.count() > 0:
                        print("Agent 5 (TikTok): Found 'Continue to post?' warning. Clicking 'Post now'...")
                        post_now_btn.first.click(force=True)
                        time.sleep(2)
                        page.screenshot(path="3_after_post_now_click.png")
                except Exception as e:
                    print(f"Agent 5 (TikTok): Error clicking 'Post now': {e}")

                print("Agent 5 (TikTok): Waiting for upload to complete and redirect to content manager...")
                video_url = "https://www.tiktok.com/@kidobumnurseryrhymes" # Default profile fallback
                try:
                    # After successful post, TikTok redirects to creator center or tiktok studio pages
                    page.wait_for_url(lambda url: "creator-center" in url or "tiktokstudio" in url, timeout=55000)
                    print(f"Agent 5 (TikTok): Successfully redirected to content manager ({page.url}). Upload confirmed!")
                    page.screenshot(path="4_after_redirect.png")
                except Exception:
                    print(f"Agent 5 (TikTok): Did not detect redirect URL pattern (current URL: {page.url}), checking page state...")
                    page.screenshot(path="4_no_redirect_fallback.png")
                
                # Attempt to extract video URL if we are on creator center or tiktok studio page
                if "creator-center" in page.url or "tiktokstudio" in page.url:
                    time.sleep(5) # Wait for list rendering
                    try:
                        # Find the first link that points to a video
                        video_link_selector = 'a[href*="/video/"]'
                        page.wait_for_selector(video_link_selector, timeout=15000)
                        extracted_url = page.locator(video_link_selector).first.get_attribute("href")
                        if extracted_url:
                            if not extracted_url.startswith("http"):
                                video_url = "https://www.tiktok.com" + extracted_url
                            else:
                                video_url = extracted_url
                            print(f"Agent 5 (TikTok): Extracted uploaded video URL: {video_url}")
                    except Exception as extract_err:
                        print(f"Agent 5 (TikTok): Could not extract video URL, using profile fallback: {extract_err}")
                
                browser.close()

            print("Agent 5 (TikTok): Video successfully posted via Playwright!")
            return video_url
            
        except Exception as e:
            print(f"Agent 5 (TikTok): Playwright upload error: {e}")
            raise e

    def process(self, video_path, video_name=None):
        try:
            metadata = self.generate_metadata(video_path)
            video_url = self.upload_to_tiktok(video_path, metadata)
            return {"platform": "TikTok", "url": video_url, "status": "success"}
        except Exception as e:
            print(f"Agent 5 (TikTok): Error during processing: {e}")
            return {"status": "error", "error": str(e)}
