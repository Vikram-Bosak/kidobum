import os
import time
import random
from dotenv import load_dotenv
from agent1_fetcher import ContentManagerAgent
from agent2_youtube import YouTubeUploadAgent
from agent3_facebook import FacebookUploadAgent
from agent4_reporter import ReportAgent

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

    video_path = None

    try:
        # Agent 1: Fetch and verify the video
        video_path, video_name = agent1.process()
        
        # Simulate user preparing to upload
        human_delay(1, 3, "Preparing to upload on YouTube")
        
        # Agent 2: YouTube Upload
        yt_result = agent2.process(video_path)
        
        # Simulate user taking a break / switching tabs
        human_delay(2, 5, "Switching to Facebook")
        
        # Agent 3: Facebook Upload
        fb_result = agent3.process(video_path)
        
        # Simulate final checks
        human_delay(0.5, 1.5, "Finalizing and writing report")
        
        # Agent 4: Report
        agent4.send_report(yt_result, fb_result, video_name)
        
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
