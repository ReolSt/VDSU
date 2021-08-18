import pickle
import os.path
from abc import abstractmethod
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport import requests

import datetime
import re
import hashlib
import io
import shutil

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


def load_credentials(client_secret_file_name):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.token or not creds.valid or creds.expired:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_file_name, SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_google_drive_v3_service(client_secret_file_name):
    creds = load_credentials(client_secret_file_name)
    service = build('drive', 'v3', credentials=creds)

    return service


def seperate_file_path(file_path, new_separator='//'):
    tokens = re.split(r'\\|/', file_path)
    if len(tokens) < 1:
        return ("", "")

    file_name = tokens.pop()
    parent = new_separator.join(tokens)
    return (parent, file_name)


def get_backup_file_name(file_name, time_string):
    tokens = file_name.split('.')
    tokens.insert(1, time_string)

    if file_name.find('.') == -1:
        return '{}_{}'.format(*tokens)

    return '{}_{}.{}'.format(*tokens)


def create_local_backup_file(file_path, time_string):
    parent, file_name = seperate_file_path(file_path)

    backup_file_name = get_backup_file_name(file_name, time_string)
    backup_file_path = parent + '//' + backup_file_name

    return shutil.copy(file_path, backup_file_path)


def get_md5_string(file_path):
    with open(file_path, "rb") as file:
        md5_string = hashlib.md5(file.read()).hexdigest()

    return md5_string


class SaveFileUpdater():
    def __init__(self,
                 client_secret_file_name,
                 drive_folder_id,
                 local_directory_path):
        self._drive_service = get_google_drive_v3_service(
            client_secret_file_name)

        self._drive_folder_id = drive_folder_id
        self._local_directory_path = local_directory_path.replace('/', '\\')

        path_length = len(self._local_directory_path)
        if self._local_directory_path[path_length - 1] != '\\':
            self._local_directory_path += '//'

        self._file_names = []

    def get_drive_file_list(self, fields):
        q = "'{}' in parents".format(self._drive_folder_id)

        results = self._drive_service.files().list(
            q=q, fields=fields).execute()

        return results.get('files', [])

    def get_metadata(self, file_name):
        return {
            'name': file_name,
            'parents': [self._drive_folder_id]
        }

    def download_from_drive(self, file_id, file_path_to_save):
        request = self._drive_service.files().get_media(fileId=file_id)
        file = io.FileIO(file_path_to_save, "wb")
        downloader = MediaIoBaseDownload(file, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download {}%.".format(int(status.progress() * 100)))

        return file

    def upload_to_drive(self, metadata, file_path):
        media = MediaFileUpload(file_path, resumable=True)
        file = self._drive_service.files().create(
            body=metadata, media_body=media, fields='id').execute()

        return file

    def update_local(self):
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        drive_data_file_info = self.get_drive_file_list(
            "files(id, name, md5Checksum)")

        file_paths = map(lambda s: self._local_directory_path + s, self._file_names)

        local_file_infos = []

        for i, file_path in enumerate(file_paths):
            try:
                md5 = get_md5_string(file_path)
                local_file_infos.append({
                    "name": self._file_names[i],
                    "path": file_path,
                    "md5": md5
                })
            except FileNotFoundError:
                local_file_infos.append({
                    "name": self._file_names[i],
                    "path": "",
                    "md5": ""
                })

        for drive_file_info in drive_data_file_info:
            drive_file_id = drive_file_info['id']
            drive_file_name = drive_file_info['name']
            drive_file_md5 = drive_file_info['md5Checksum']

            for index, local_file_info in enumerate(local_file_infos):
                if drive_file_name == local_file_info['name']:
                    local_file_infos[index]['drive_id'] = drive_file_id
                    local_file_infos[index]['drive_md5'] = drive_file_md5

        for local_file_info in local_file_infos:
            local_file_name = local_file_info['name']
            local_file_path = local_file_info['path']
            local_file_md5 = local_file_info['md5']

            try:
                drive_file_id = local_file_info['drive_id']
                drive_file_md5 = local_file_info['drive_md5']
            except KeyError:
                continue

            if local_file_md5 != drive_file_md5:
                if local_file_path != "":
                    create_local_backup_file(local_file_path, current_time)

                self.download_from_drive(drive_file_id, local_file_path)

    def update_drive(self):
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        drive_data_file_info = self.get_drive_file_list(
            "files(id, name, md5Checksum)")

        print(self._file_names)

        local_file_infos = []

        for index, file_path in enumerate(self._file_names):
            try:
                md5 = get_md5_string(file_path)
                local_file_infos.append({
                    'name': self._file_names[index],
                    'path': file_path,
                    'md5': md5
                })
            except FileNotFoundError:
                continue

        print(local_file_infos)
        for drive_file_info in drive_data_file_info:
            drive_file_id = drive_file_info['id']
            drive_file_name = drive_file_info['name']
            drive_file_md5 = drive_file_info['md5Checksum']

            for index, local_file_info in enumerate(local_file_infos):
                if drive_file_name == local_file_info['name']:
                    local_file_infos[index]['drive_id'] = drive_file_id
                    local_file_infos[index]['drive_md5'] = drive_file_md5

        for local_file_info in local_file_infos:
            local_file_name = local_file_info['name']
            local_file_path = local_file_info['path']
            local_file_md5 = local_file_info['md5']

            try:
                drive_file_id = local_file_info['drive_id']
                drive_file_md5 = local_file_info['drive_md5']
            except KeyError:
                drive_file_id = ""
                drive_file_md5 = ""

            metadata = self.get_metadata(local_file_info['name'])
            backup_file_name = get_backup_file_name(
                    drive_file_name, current_time)

            print(local_file_info)

            if local_file_md5 != drive_file_md5:
                if drive_file_id != "":
                    self._drive_service.files().update(
                                fileId=drive_file_id,
                                body={'name': backup_file_name}).execute()

                self.upload_to_drive(metadata, local_file_path)


class ValheimSaveFileUpdater(SaveFileUpdater):
    def __init__(self,
                 client_secret_file_name,
                 drive_folder_id,
                 local_directory_path,
                 world_name):
        super().__init__(
            client_secret_file_name,
            drive_folder_id,
            local_directory_path)

        self._world_name = world_name

        self._file_names = [
            self._world_name + ".fwl",
            self._world_name + ".db"
        ]


class TerrariaSaveFileUpdater(SaveFileUpdater):
    def __init__(self,
                 client_secret_file_name,
                 drive_folder_id,
                 local_directory_path,
                 world_name):
        super().__init__(
            client_secret_file_name,
            drive_folder_id,
            local_directory_path)

        self._world_name = world_name

        self._file_names = [
            self._world_name + ".wld"
        ]
