import os
import time
import random
from dotenv import load_dotenv
from agent1_fetcher import ContentManagerAgent
from agent2_youtube import YouTubeUploadAgent
from agent3_facebook import FacebookUploadAgent
from agent4_reporter import ReportAgent
from agent5_tiktok import TikTokUploadAgent

load_dotenv()

def human_delay(min_minutes, max_minutes, reason=""):
    delay_seconds = random.uniform(min_minutes * 60, max_minutes * 60)
    print(f"--- Simulating Human Delay: {reason} ({delay_seconds / 60:.2f} minutes) ---")
    time.sleep(delay_seconds)

def main():
    print("Starting 24x7 Video Upload Automation Workflow...")
    
    # Initialize Agents
    agent1 = ContentManagerAgent()
    agent2 = YouTubeUploadAgent()
    agent3 = FacebookUploadAgent()
    agent4 = ReportAgent()
    agent5 = TikTokUploadAgent()

    video_path = None

    try:
        # Agent 1: Fetch and verify the video
        video_path, video_name, video_id = agent1.process()
        
        # YouTube & Facebook Upload (Temporarily Disabled for TikTok Testing)
        print("YouTube & Facebook uploads are temporarily disabled.")
        yt_result = {"status": "disabled", "url": "N/A", "metadata": {"title": "N/A", "description": "N/A"}}
        fb_result = {"status": "disabled", "url": "N/A", "metadata": {"caption": "N/A"}}
        
        # Agent 5: TikTok Upload
        tiktok_result = agent5.process(video_path, video_name)
        
        # Simulate final checks
        human_delay(0.5, 1.5, "Finalizing and writing report")
        
        # Agent 4: Report
        agent4.send_report(yt_result, fb_result, tiktok_result, video_name)
        
        # Move video to Uploaded folder if at least one upload succeeded
        if yt_result.get('status') == 'success' or fb_result.get('status') == 'success' or tiktok_result.get('status') == 'success':
            agent1.mark_as_uploaded(video_id)
        
        print("Workflow completed successfully.")
            
    except Exception as e:
        print(f"Error occurred during workflow orchestration: {e}")
    finally:
        # Cleanup temporary video file
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
            print("Cleaned up temporary video file.")

if __name__ == "__main__":
    main()
