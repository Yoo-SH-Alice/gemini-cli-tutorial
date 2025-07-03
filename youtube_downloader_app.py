import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import yt_dlp
import os

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)
    message_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, url, download_path):
        super().__init__()
        self.url = url
        self.download_path = download_path

    def run(self):
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'progress_hooks': [self.hook],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.message_signal.emit("다운로드 완료!")
        except Exception as e:
            self.error_signal.emit(f"다운로드 중 오류 발생: {e}")

    def hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes')
            if total_bytes and downloaded_bytes:
                progress = int(downloaded_bytes / total_bytes * 100)
                self.progress_signal.emit(progress)
        elif d['status'] == 'finished':
            self.progress_signal.emit(100)

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube 다운로더')
        self.setGeometry(100, 100, 600, 200)

        main_layout = QVBoxLayout()

        # URL 입력
        url_layout = QHBoxLayout()
        self.url_label = QLabel('YouTube URL:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('여기에 YouTube URL을 입력하세요.')
        url_layout.addWidget(self.url_label)
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # 다운로드 버튼
        self.download_button = QPushButton('다운로드')
        self.download_button.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_button)

        # 진행률 표시줄
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # 상태 메시지
        self.status_label = QLabel('대기 중...')
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def start_download(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, '경고', 'YouTube URL을 입력해주세요.')
            return

        # 다운로드 경로 설정 (현재 실행 디렉토리의 'downloads' 폴더)
        download_path = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        self.status_label.setText('다운로드 시작...')
        self.progress_bar.setValue(0)
        self.download_button.setEnabled(False)

        self.download_thread = DownloadThread(url, download_path)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.message_signal.connect(self.show_message)
        self.download_thread.error_signal.connect(self.show_error)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def show_message(self, message):
        self.status_label.setText(message)
        QMessageBox.information(self, '알림', message)

    def show_error(self, message):
        self.status_label.setText(message)
        QMessageBox.critical(self, '오류', message)

    def download_finished(self):
        self.download_button.setEnabled(True)
        self.status_label.setText('대기 중...')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloaderApp()
    ex.show()
    sys.exit(app.exec_())
