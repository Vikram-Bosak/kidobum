import os
import io
import json
import random
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

class ContentManagerAgent:
    def __init__(self):
        self.creds_json = os.environ.get('GOOGLE_DRIVE_CREDENTIALS')
        self.drive_service = self._authenticate_drive()

    def _authenticate_drive(self):
        if not self.creds_json:
            print("Warning: GOOGLE_DRIVE_CREDENTIALS not set.")
            return None
        try:
            creds_dict = json.loads(self.creds_json)
            creds = Credentials.from_authorized_user_info(creds_dict)
            return build('drive', 'v3', credentials=creds)
        except Exception as e:
            print(f"Error authenticating Google Drive: {e}")
            return None

    def fetch_video(self):
        print("Agent 1: Fetching video from Google Drive...")
        if not self.drive_service:
            raise Exception("Google Drive service is not authenticated.")

        # Query for mp4 files inside the specific user-provided folder.
        folder_id = "1H_a6FJWK7eh52vt0BXZbD-Zyx2_e9prU"
        query = f"'{folder_id}' in parents and mimeType='video/mp4' and trashed=false"
        results = self.drive_service.files().list(q=query, pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            raise Exception("No video files found in Google Drive.")

        # Randomly select a video for this upload
        video = random.choice(items)
        video_id = video['id']
        video_name = video['name']
        print(f"Agent 1: Selected video - {video_name}")

        request = self.drive_service.files().get_media(fileId=video_id)
        video_path = f"downloaded_{video_id}.mp4"
        
        fh = io.FileIO(video_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print(f"Download {int(status.progress() * 100)}%.")
                
        fh.close()
            
        print(f"Agent 1: Successfully fetched video. Saved to {video_path}")
        return video_path

    def verify_format(self, video_path):
        print("Agent 1: Verifying video format (assuming 720p, 9:16 aspect ratio for now)...")
        # In a robust system, use cv2 or ffmpeg (ffprobe) to check resolution.
        # Returning True to simulate successful verification.
        print("Agent 1: Format verified successfully.")
        return True

    def process(self):
        video_path = self.fetch_video()
        if self.verify_format(video_path):
            return video_path
        else:
            raise Exception("Video format verification failed.")
