import os
import requests
import json

class ReportAgent:
    def __init__(self):
        self.discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

    def send_report(self, yt_result, fb_result, tiktok_result, video_name):
        print("Agent 4 (Reporter): Sending final report to Discord...")
        if not self.discord_webhook:
            print("Agent 4 (Reporter): Discord Webhook URL not configured. Skipping.")
            return

        yt_status = "Success" if yt_result.get('status') == 'success' else f"Failed ({yt_result.get('error')})"
        fb_status = "Success" if fb_result.get('status') == 'success' else f"Failed ({fb_result.get('error')})"
        tiktok_status = "Success" if tiktok_result.get('status') == 'success' else f"Failed ({tiktok_result.get('error')})"
        
        yt_title = yt_result.get('metadata', {}).get('title', 'N/A')
        # Prefer FB caption for the description block as it typically contains emojis/hashtags 
        description = fb_result.get('metadata', {}).get('caption', yt_result.get('metadata', {}).get('description', 'N/A'))
        
        fb_url = fb_result.get('url', 'N/A')
        yt_url = yt_result.get('url', 'N/A')
        tiktok_url = tiktok_result.get('url', 'N/A')
        
        repo = os.environ.get('GITHUB_REPOSITORY', 'Vikram-Bosak/kidobum')
        run_id = os.environ.get('GITHUB_RUN_ID', 'unknown')
        server_url = os.environ.get('GITHUB_SERVER_URL', 'https://github.com')
        run_url = f"{server_url}/{repo}/actions/runs/{run_id}"

        # Ensure video_name without extension for the Video Name field, but keep extension for Original File
        short_video_name = video_name.rsplit('.', 1)[0] if '.' in video_name else video_name

        report = f"""✅ Pipeline Run Completed

🎬 Video Name:
{short_video_name}

📤 Facebook Upload Status: {fb_status}
📤 YouTube Upload Status: {yt_status}
📤 TikTok Upload Status: {tiktok_status}

🏷️ SEO Title:
{yt_title}

📝 Description:
{description}

Original File: {video_name}

🔗 Facebook Reel URL:
{fb_url}

▶️ YouTube Video URL:
{yt_url}

🎵 TikTok Video URL:
{tiktok_url}

📦 GitHub Repository:
https://github.com/Vikram-Bosak/kidobum

📄 Workflow Run:
{run_url}"""

        payload = {"content": report}

        try:
            requests.post(self.discord_webhook, json=payload)
            print("Agent 4 (Reporter): Discord Notification Sent.")
        except Exception as e:
            print(f"Agent 4 (Reporter): Failed to send Discord notification: {e}")
