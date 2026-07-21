import os
from playwright.sync_api import sync_playwright

def save_tiktok_cookies():
    print("🚀 Starting Playwright to save TikTok session...")
    print("A browser window will open. Please log into your TikTok account.")
    print("Once you are fully logged in and see the homepage, return here and press ENTER.")

    with sync_playwright() as p:
        # Open a visible browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Go to TikTok login page
        page.goto("https://www.tiktok.com/login")
        
        # Wait for user to log in manually
        input("\nPress ENTER here ONLY AFTER you have successfully logged in to TikTok in the browser... ")

        # Save the authentication state
        auth_file = "tiktok_auth_state.json"
        context.storage_state(path=auth_file)
        
        print(f"✅ Success! Your TikTok session has been saved to '{auth_file}'.")
        print("Agent 5 will use this file to upload videos automatically without asking for passwords.")

        browser.close()

if __name__ == "__main__":
    save_tiktok_cookies()
