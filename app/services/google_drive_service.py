import os
import io
from typing import List, Dict, Optional, Set
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import logging
import time

class GoogleDriveService:
    """A service class for interacting with Google Drive API."""

    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    def __init__(self, credentials_path: str, token_path: str, monitored_folder_id: Optional[str] = None):
        """Initialize Google Drive service."""
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.monitored_folder_id = monitored_folder_id
        self.service = None
        self.user_email = None
        self.logger = logging.getLogger(__name__)

    def login(self) -> None:
        """Perform login and authentication."""
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

        about = self.service.about().get(fields='user').execute()
        self.user_email = about['user']['emailAddress']
        self.logger.info(f"Logged in as: {self.user_email}")

    def _ensure_authenticated(self) -> None:
        """Ensure the service is authenticated before making API calls."""
        if not self.service:
            self.login()

    def list_files(self, folder_id: str) -> List[Dict[str, str]]:
        """List files in a Google Drive folder."""
        self._ensure_authenticated()

        results = self.service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='files(id, name, mimeType, createdTime)'
        ).execute()

        return results.get('files', [])

    def download_file(self, file_id: str, save_path: str) -> None:
        """Download a file from Google Drive."""
        self._ensure_authenticated()

        request = self.service.files().get_media(fileId=file_id)
        with io.BytesIO() as file_stream:
            downloader = MediaIoBaseDownload(file_stream, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(file_stream.getvalue())

    def get_folder_id_by_name(self, folder_name: str) -> str:
        """Get folder ID using folder name."""
        self._ensure_authenticated()
        results = self.service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields='files(id)'
        ).execute()

        files = results.get('files', [])
        if not files:
            raise ValueError(f"Folder '{folder_name}' not found")
        return files[0]['id']

    def monitor_folder(self, folder_id: str, interval: int = 60) -> None:
        """Monitor a Google Drive folder and download new files."""
        self._ensure_authenticated()
        known_files: Set[str] = set()

        while True:
            try:
                files = self.list_files(folder_id)
                for file in files:
                    if file['id'] not in known_files:
                        self.logger.info(f"New file detected: {file['name']}")
                        save_path = os.path.join('downloads', file['name'])
                        self.download_file(file['id'], save_path)
                        known_files.add(file['id'])
                        self.logger.info(f"Downloaded: {file['name']}")
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {e}")
                time.sleep(interval)