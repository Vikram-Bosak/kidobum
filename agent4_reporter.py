import os
import requests
import json

class ReportAgent:
    def __init__(self):
        self.discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

    def send_report(self, yt_result, fb_result):
        print("Agent 4 (Reporter): Sending final report to Discord...")
        if not self.discord_webhook:
            print("Agent 4 (Reporter): Discord Webhook URL not configured. Skipping.")
            return

        report_lines = ["✅ **Kidobum Auto-Upload Report**\n"]

        # YouTube Report
        if yt_result.get('status') == 'success':
            title = yt_result.get('metadata', {}).get('title', 'N/A')
            report_lines.append(f"🔴 **YouTube:** Success\n**Title:** {title}\n**Link:** {yt_result.get('url')}\n")
        else:
            report_lines.append(f"🔴 **YouTube:** Failed\n**Error:** {yt_result.get('error')}\n")

        # Facebook Report
        if fb_result.get('status') == 'success':
            report_lines.append(f"🔵 **Facebook:** Success\n**Link:** {fb_result.get('url')}\n")
        else:
            report_lines.append(f"🔵 **Facebook:** Failed\n**Error:** {fb_result.get('error')}\n")

        report = "\n".join(report_lines)
        payload = {"content": report}

        try:
            requests.post(self.discord_webhook, json=payload)
            print("Agent 4 (Reporter): Discord Notification Sent.")
        except Exception as e:
            print(f"Agent 4 (Reporter): Failed to send Discord notification: {e}")
