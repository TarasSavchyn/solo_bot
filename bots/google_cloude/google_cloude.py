import os
import logging
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import ApiRequestError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


class GoogleDriveManager:
    def __init__(
        self,
        client_secrets_filename="client_secrets.json",
        credentials_filename="credentials.json",
        folder_name="MyUploads",
    ):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.client_secrets_path = os.path.join(base_dir, client_secrets_filename)
        self.credentials_path = os.path.join(base_dir, credentials_filename)
        self.drive = None
        self.folder_name = folder_name
        self.folder_id = None
        self._authenticate()
        self._ensure_folder_exists()

    def _authenticate(self):
        try:
            gauth = GoogleAuth()
            gauth.LoadClientConfigFile(self.client_secrets_path)

            gauth.settings["get_refresh_token"] = True
            gauth.settings["access_type"] = "offline"
            gauth.settings["oauth_scope"] = [
                "https://www.googleapis.com/auth/drive.file"
            ]

            if os.path.exists(self.credentials_path):
                gauth.LoadCredentialsFile(self.credentials_path)

            if gauth.credentials is None:
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                gauth.Refresh()

            gauth.SaveCredentialsFile(self.credentials_path)
            self.drive = GoogleDrive(gauth)
            logger.info("✅ Authentication successful.")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise

    def _ensure_folder_exists(self):
        try:
            file_list = self.drive.ListFile(
                {
                    "q": f"title='{self.folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
                }
            ).GetList()

            if file_list:
                self.folder_id = file_list[0]["id"]
                logger.info(
                    f"📁 Existing folder found: {self.folder_name} (ID: {self.folder_id})"
                )
            else:
                folder_metadata = {
                    "title": self.folder_name,
                    "mimeType": "application/vnd.google-apps.folder",
                }
                folder = self.drive.CreateFile(folder_metadata)
                folder.Upload()
                self.folder_id = folder["id"]
                logger.info(
                    f"📁 New folder created: {self.folder_name} (ID: {self.folder_id})"
                )
        except Exception as e:
            logger.error(f"Failed to create or get folder: {e}")
            raise

    def upload_file(self, local_path: str, remote_name: str = None) -> str | None:
        if not os.path.exists(local_path):
            logger.error(f"File does not exist: {local_path}")
            return None

        if remote_name is None:
            remote_name = os.path.basename(local_path)

        file_metadata = {"title": remote_name, "parents": [{"id": self.folder_id}]}

        try:
            file = self.drive.CreateFile(file_metadata)
            file.SetContentFile(local_path)
            file.Upload()
            logger.info(f"✅ File uploaded: {remote_name} (ID: {file['id']})")
            return file["id"]
        except ApiRequestError as e:
            logger.error(f"Google Drive API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            return None


gdrive = GoogleDriveManager(folder_name="EventAgencyUploads")
