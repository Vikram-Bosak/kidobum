import os
import sys
from agent5_tiktok import TikTokUploadAgent

def main():
    agent = TikTokUploadAgent()
    video_path = r"C:\Users\admin\Downloads\24 BUM Teaches RECTANGLE - Long Shapes with KidoBum!.mp4"
    video_name = os.path.basename(video_path)
    
    print(f"Testing TikTok upload with video: {video_name}")
    try:
        result = agent.process(video_path, video_name)
        print("\nTest Result:", result)
    except Exception as e:
        print(f"\nTest Failed: {e}")

if __name__ == "__main__":
    main()
