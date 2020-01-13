"""Odpowiada za połączenie z bazą danych znajdującą się na dropboxie"""
import os
import sys

import dropbox as dropbox
from dropbox.exceptions import AuthError, ApiError, DropboxException
from dropbox.files import WriteMode

from dropbox_token import TOKEN

FILE = r'\\Raspberrypi\PBPZ\poo.db'
BACKUP_PATH = '/poo.db'  # Keep the forward slash before destination filename


def _auth():
    dbx = dropbox.Dropbox(TOKEN)
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit(
            "BŁĄD: Błędny Token; Spróbuj wygenerować nowy token"
        )
    return dbx


# Uploads contents of LOCALFILE to Dropbox
def backup(BACKUPPATH=BACKUP_PATH, LOCALFILE=FILE):
    """Wgrywa plik na dropboxa. Wymaga LOCALFILE i BACKUPPATCH"""
    dbx = _auth()
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print(
            "Zapisanie " + LOCALFILE + " do Dropbox'a jako " + BACKUPPATH
            + " ...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
            print('Plik wysłano na serwer')
        except ApiError as er:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (er.error.is_path() and
                    er.error.get_path().error.is_insufficient_space()):
                sys.exit("BŁĄD: Nie można wgrać pliku, brak miejsca")
            elif er.user_message_text:
                print(er.user_message_text)
                sys.exit()
            else:
                print(er)
                sys.exit()


def download(LOCALFILE=FILE):
    dbx = _auth()
    if os.path.exists(LOCALFILE):
        os.remove(LOCALFILE)
    try:
        with open(LOCALFILE, "wb") as f:
            metadata, res = dbx.files_download(path=BACKUP_PATH)
            f.write(res.content)
        print('Pobrano bazę danych')
        return True
    except DropboxException:
        return False


if __name__ == '__main__':
    dbx = dropbox.Dropbox(TOKEN)
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit(
            "BŁĄD: Błędny Token; Spróbuj wygenerować nowy token")

    print('Wgrywanie')
    backup(LOCALFILE=FILE)
    print('Pobieranie')
    download()
