import os
from dotenv import load_dotenv
from agent1_fetcher import ContentManagerAgent
from agent2_publisher import SEOPublisherAgent

# Load environment variables from .env file
load_dotenv()
def main():
    print("Starting 24x7 Video Upload Automation Workflow...")
    
    # Initialize Agents
    agent1 = ContentManagerAgent()
    agent2 = SEOPublisherAgent()

    video_path = None

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
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
            print("Cleaned up temporary video file.")

if __name__ == "__main__":
    main()
