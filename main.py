import os
from agent1_fetcher import ContentManagerAgent
from agent2_publisher import SEOPublisherAgent

def main():
    print("Starting 24x7 Video Upload Automation Workflow...")
    
    # Initialize Agents
    agent1 = ContentManagerAgent()
    agent2 = SEOPublisherAgent()

    try:
        # Agent 1: Fetch and verify the video
        video_path = agent1.process()
        
        # Agent 2: Generate SEO, Upload and Notify
        success = agent2.process(video_path)
        
        if success:
            print("Workflow completed successfully.")
        else:
            print("Workflow failed during Agent 2 execution.")
            
    except Exception as e:
        print(f"Error occurred during workflow: {e}")
    finally:
        # Cleanup temporary video file
        if os.path.exists("temp_video_720p.mp4"):
            os.remove("temp_video_720p.mp4")
            print("Cleaned up temporary video file.")

if __name__ == "__main__":
    main()
