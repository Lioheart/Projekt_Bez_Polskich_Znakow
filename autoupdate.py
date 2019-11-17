"""Moduł odpowiedzialny za sprawdzanie ostatniej wersji oprogramowania
w repozytorium GitHub i w razie konieczności uruchomienie automatycznej
aktualizacji"""
import json
import urllib.request

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication


class MessageBox(QMessageBox):

    def __init__(self, wersja):
        super().__init__()
        acceptbtn = self.addButton('Tak', self.AcceptRole)
        acceptbtn = self.standardButton(acceptbtn)
        nobtn = self.addButton('Nie', self.RejectRole)
        nobtn = self.standardButton(nobtn)
        self.setWindowIcon(QIcon('icons/cow.png'))
        self.setWindowTitle('Aktualizacja PBPZ')
        self.setIcon(QMessageBox.Information)
        self.setText('Pojawiła się nowa aktualizacja programu PBPZ ({}).\nCzy chcesz ja teraz pobrać?'.format(wersja))
        self.setStandardButtons(acceptbtn | nobtn)
        self.show()


def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if operUrl.getcode() == 200:
        data = operUrl.read()
        jsonData = json.loads(data)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData


def showDialog(wersja=None):
    print(wersja)
    import sys
    app = QApplication(sys.argv)
    from PyQt5.QtWidgets import QStyleFactory
    app.setStyle(QStyleFactory.create('Fusion'))
    message = MessageBox(wersja)
    if message.exec() != QMessageBox.Accepted:
        print('Wybrano tak')
        import webbrowser
        webbrowser.open('https://github.com/Lioheart/Projekt_Bez_Polskich_Znakow/releases/latest')
        sys.exit(0)
    else:
        print('Wybrano nie')


# https://api.github.com/repos/Lioheart/Projekt_Bez_Polskich_Znakow/releases/latest
if __name__ == "__main__":
    jsonData = getResponse('https://api.github.com/repos/Lioheart/Projekt_Bez_Polskich_Znakow/releases/latest')
    print(jsonData['tag_name'][1:])
