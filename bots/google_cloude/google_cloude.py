import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class GoogleDriveManager:
    def __init__(
        self,
        client_secrets_filename="client_secrets.json",
        credentials_filename="credentials.json",
    ):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.client_secrets_path = os.path.join(base_dir, client_secrets_filename)
        self.credentials_path = os.path.join(base_dir, credentials_filename)
        self.drive = None
        self._authenticate()

    def _authenticate(self):
        gauth = GoogleAuth()
        gauth.LoadClientConfigFile(self.client_secrets_path)

        if os.path.exists(self.credentials_path):
            gauth.LoadCredentialsFile(self.credentials_path)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()

        gauth.SaveCredentialsFile(self.credentials_path)
        self.drive = GoogleDrive(gauth)

    def upload_file(self, local_path: str, remote_name: str = None) -> str:
        if remote_name is None:
            remote_name = os.path.basename(local_path)
        file = self.drive.CreateFile({"title": remote_name})
        file.SetContentFile(local_path)
        file.Upload()
        return file["id"]


# if __name__ == "__main__":
#     gdrive = GoogleDriveManager()
#
#     file_path = os.path.join(os.path.dirname(__file__), "image.jpg")
#
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Файл не знайдено: {file_path}")
#
#     file_id = gdrive.upload_file(file_path)
#     print("✅ Файл завантажено! ID:", file_id)
#     print("Посилання:", f"https://drive.google.com/uc?id={file_id}")
