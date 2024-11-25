from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import subprocess
import sys
import os

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Inicial")
        self.setGeometry(100, 100, 1920, 1080)

        # Fundo da tela de menu inicial
        self.background_label_menu = QLabel(self)
        self.pixmap_menu = QPixmap("Menu-inicial.png")
        self.background_label_menu.setPixmap(self.pixmap_menu)
        self.background_label_menu.setScaledContents(True)
        self.background_label_menu.setGeometry(0, 0, self.width(), self.height())

        # Botão de iniciar jogo
        self.start_button = QPushButton(self)
        self.start_button.setFixedWidth(400)
        self.start_button.setFixedHeight(200)
        self.start_button.move(1100, 450)
        self.start_button.setStyleSheet("""
            QPushButton {
                border-image: url('start.png');
                border: none;
            }
            QPushButton:hover {
                border: 50px solid blue;
            }
        """)
        self.start_button.clicked.connect(self.iniciar_jogo)

        # Criar o player de música
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(os.path.abspath("musica_menu.mp3")))
        self.audio_output.setVolume(0.5)  # Volume de 0.0 a 1.0

        # Iniciar a música
        self.player.play()

    def iniciar_jogo(self):
        # Executar o arquivo do jogo
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "jogo.py")])
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MenuWindow()
    window.show()
    app.exec()