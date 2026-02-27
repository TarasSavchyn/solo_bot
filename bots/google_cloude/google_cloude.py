import os
import logging
import tempfile
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


class GoogleDriveManager:
    def __init__(self, folder_name="EventAgencyUploads"):
        self.folder_name = folder_name
        self.folder_id = None
        self.drive = None
        self._authenticate()
        self._ensure_folder_exists()
        self._make_folder_public()

    def _authenticate(self):
        local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client_secrets.json")
        client_secret_env = os.getenv("GDRIVE_CLIENT_SECRETS")

        if os.path.exists(local_path):
            secret_path = local_path
            logger.info("Using local client_secrets.json")
        elif client_secret_env:
            with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
                f.write(client_secret_env)
                secret_path = f.name
            logger.info("Using client secrets from environment variable")
        else:
            raise RuntimeError("No client_secrets.json file or GDRIVE_CLIENT_SECRETS env variable found!")

        gauth = GoogleAuth()
        gauth.LoadClientConfigFile(secret_path)
        gauth.settings["get_refresh_token"] = True
        gauth.settings["access_type"] = "offline"
        gauth.settings["oauth_scope"] = ["https://www.googleapis.com/auth/drive.file"]

        creds_path = os.path.join(tempfile.gettempdir(), "credentials.json")
        if os.path.exists(creds_path):
            gauth.LoadCredentialsFile(creds_path)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()

        gauth.SaveCredentialsFile(creds_path)
        self.drive = GoogleDrive(gauth)
        logger.info("✅ Google Drive authentication successful.")

    def _ensure_folder_exists(self):
        file_list = self.drive.ListFile({
            "q": f"title='{self.folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        }).GetList()

        if file_list:
            self.folder_id = file_list[0]["id"]
            logger.info(f"📁 Existing folder found: {self.folder_name} (ID: {self.folder_id})")
        else:
            folder_metadata = {"title": self.folder_name, "mimeType": "application/vnd.google-apps.folder"}
            folder = self.drive.CreateFile(folder_metadata)
            folder.Upload()
            self.folder_id = folder["id"]
            logger.info(f"📁 New folder created: {self.folder_name} (ID: {self.folder_id})")

    def _make_folder_public(self):
        try:
            folder = self.drive.CreateFile({"id": self.folder_id})
            folder.InsertPermission({"type": "anyone", "value": "anyone", "role": "reader"})
            logger.info(f"🌐 Folder {self.folder_name} is now public")
        except Exception as e:
            logger.error(f"Failed to make folder public: {e}")

    def get_folder_link(self) -> str:
        return f"https://drive.google.com/drive/folders/{self.folder_id}?usp=sharing"

    def upload_file(self, local_path: str, remote_name: str = None) -> str | None:
        if not os.path.exists(local_path):
            logger.error(f"File does not exist: {local_path}")
            return None

        if remote_name is None:
            remote_name = os.path.basename(local_path)

        try:
            file_metadata = {"title": remote_name, "parents": [{"id": self.folder_id}]}
            file = self.drive.CreateFile(file_metadata)
            file.SetContentFile(local_path)
            file.Upload()
            logger.info(f"✅ File uploaded: {remote_name} (ID: {file['id']})")
            return file["id"]
        except Exception as e:
            logger.error(f"Failed to upload file '{remote_name}': {e}")
            return None


gdrive = GoogleDriveManager(folder_name="EventAgencyUploads")