import os
import json
import logging
from dotenv import load_dotenv
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

class GoogleDriveManager:
    def __init__(self, folder_name="MyUploads"):
        self.drive = None
        self.folder_name = folder_name
        self.folder_id = None
        self._authenticate()
        self._ensure_folder_exists()
        self._make_folder_public()

    def _authenticate(self):
        service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT")
        if not service_account_json:
            raise ValueError("GOOGLE_SERVICE_ACCOUNT env variable not set")
        creds_dict = json.loads(service_account_json)
        gauth = GoogleAuth()
        gauth.settings["client_config_backend"] = "service"
        gauth.settings["service_config"] = {
            "client_user_email": creds_dict["client_email"],
            "client_json_dict": creds_dict,
        }
        gauth.ServiceAuth()
        self.drive = GoogleDrive(gauth)
        logger.info("✅ Аутентифікація пройдена")

    def _ensure_folder_exists(self):
        query = f"title='{self.folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        file_list = self.drive.ListFile({"q": query}).GetList()
        if file_list:
            self.folder_id = file_list[0]["id"]
            logger.info(f"📁 Знайдено папку: {self.folder_name} (ID: {self.folder_id})")
        else:
            folder_metadata = {"title": self.folder_name, "mimeType": "application/vnd.google-apps.folder"}
            folder = self.drive.CreateFile(folder_metadata)
            folder.Upload()
            self.folder_id = folder["id"]
            logger.info(f"📁 Створено папку: {self.folder_name} (ID: {self.folder_id})")

    def _make_folder_public(self):
        try:
            folder = self.drive.CreateFile({"id": self.folder_id})
            folder.InsertPermission({"type": "anyone", "value": "anyone", "role": "reader"})
            logger.info(f"🌐 Папка {self.folder_name} стала публічною")
        except Exception as e:
            logger.error(f"Не вдалося зробити папку публічною: {e}")

    def get_folder_link(self) -> str:
        return f"https://drive.google.com/drive/folders/{self.folder_id}?usp=sharing"

    def upload_file(self, local_path: str, remote_name: str = None) -> str | None:
        if not os.path.exists(local_path):
            logger.error(f"Файл не знайдено: {local_path}")
            return None
        if remote_name is None:
            remote_name = os.path.basename(local_path)
        try:
            file_metadata = {"title": remote_name, "parents": [{"id": self.folder_id}]}
            file = self.drive.CreateFile(file_metadata)
            file.SetContentFile(local_path)
            file.Upload()
            logger.info(f"✅ Файл завантажено: {remote_name} (ID: {file['id']})")
            return file["id"]
        except Exception as e:
            logger.error(f"Не вдалося завантажити файл '{remote_name}': {e}")
            return None

gdrive = GoogleDriveManager(folder_name="EventAgencyUploads")