import os
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QAction, QTextEdit, QTabWidget,
    QFileDialog, QMessageBox, QFontDialog, QWidget, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import Qt

class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Notepad')
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_status_bar)
        self.setCentralWidget(self.tab_widget)

        self.create_actions()
        self.create_menu_bar()
        self.create_status_bar()

        self.new_tab() # Start with one new tab

    def create_actions(self):
        # File actions
        self.new_tab_action = QAction('새 탭', self)
        self.new_tab_action.setShortcut('Ctrl+T')
        self.new_tab_action.setStatusTip('새로운 빈 탭 열기')
        self.new_tab_action.triggered.connect(self.new_tab)

        self.open_action = QAction('열기', self)
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setStatusTip('파일 열기')
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction('저장', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setStatusTip('현재 탭 저장')
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction('다른 이름으로 저장', self)
        self.save_as_action.setShortcut('Ctrl+Shift+S')
        self.save_as_action.setStatusTip('현재 탭을 다른 이름으로 저장')
        self.save_as_action.triggered.connect(self.save_file_as)

        self.exit_action = QAction('종료', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('애플리케이션 종료')
        self.exit_action.triggered.connect(self.close)

        # Edit actions
        self.undo_action = QAction('실행 취소', self)
        self.undo_action.setShortcut('Ctrl+Z')
        self.undo_action.triggered.connect(lambda: self.current_text_edit().undo())

        self.redo_action = QAction('다시 실행', self)
        self.redo_action.setShortcut('Ctrl+Y')
        self.redo_action.triggered.connect(lambda: self.current_text_edit().redo())

        self.cut_action = QAction('잘라내기', self)
        self.cut_action.setShortcut('Ctrl+X')
        self.cut_action.triggered.connect(lambda: self.current_text_edit().cut())

        self.copy_action = QAction('복사', self)
        self.copy_action.setShortcut('Ctrl+C')
        self.copy_action.triggered.connect(lambda: self.current_text_edit().copy())

        self.paste_action = QAction('붙여넣기', self)
        self.paste_action.setShortcut('Ctrl+V')
        self.paste_action.triggered.connect(lambda: self.current_text_edit().paste())

        # Format actions
        self.font_action = QAction('글꼴', self)
        self.font_action.setStatusTip('글꼴 설정')
        self.font_action.triggered.connect(self.set_font)

        self.word_wrap_action = QAction('자동 줄 바꿈', self, checkable=True)
        self.word_wrap_action.setStatusTip('자동 줄 바꿈 설정')
        self.word_wrap_action.setChecked(True) # Default to word wrap on
        self.word_wrap_action.triggered.connect(self.toggle_word_wrap)

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('파일')
        file_menu.addAction(self.new_tab_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = menubar.addMenu('편집')
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)

        format_menu = menubar.addMenu('서식')
        format_menu.addAction(self.font_action)
        format_menu.addAction(self.word_wrap_action)

    def create_status_bar(self):
        self.statusBar()
        self.cursor_pos_label = QLabel("줄: 1, 열: 1")
        self.statusBar().addPermanentWidget(self.cursor_pos_label)

    def new_tab(self, file_path=None, content=""):
        text_edit = QTextEdit()
        text_edit.textChanged.connect(lambda: self.handle_text_changed(text_edit))
        text_edit.cursorPositionChanged.connect(self.update_status_bar)

        # Store file path and modified status directly on the text_edit widget
        text_edit.file_path = file_path
        text_edit.modified = False
        text_edit.setPlainText(content)

        # Ensure title is a string before passing to os.path.basename
        tab_title = "새 파일"
        if file_path: # This will be true for non-empty strings, and false for None or empty string
            tab_title = os.path.basename(file_path)

        tab_index = self.tab_widget.addTab(text_edit, tab_title)
        self.tab_widget.setCurrentIndex(tab_index)
        self.update_tab_title(text_edit)
        self.update_status_bar()

    def current_text_edit(self):
        return self.tab_widget.currentWidget()

    def handle_text_changed(self, text_edit):
        if not text_edit.modified:
            text_edit.modified = True
            self.update_tab_title(text_edit)

    def update_tab_title(self, text_edit):
        index = self.tab_widget.indexOf(text_edit)
        if index != -1:
            title = os.path.basename(text_edit.file_path) if text_edit.file_path else "새 파일"
            if text_edit.modified:
                title += "*"
            self.tab_widget.setTabText(index, title)

    def update_status_bar(self):
        text_edit = self.current_text_edit()
        if text_edit:
            cursor = text_edit.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.cursor_pos_label.setText(f"줄: {line}, 열: {col}")
        else:
            self.cursor_pos_label.setText("줄: 1, 열: 1") # Default when no tab is open

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 열기", "", "모든 파일 (*);;텍스트 파일 (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.new_tab(file_path, content)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 열 수 없습니다: {e}")

    def save_file(self):
        text_edit = self.current_text_edit()
        if not text_edit:
            return

        if text_edit.file_path:
            self._save_to_path(text_edit.file_path, text_edit)
        else:
            self.save_file_as()

    def save_file_as(self):
        text_edit = self.current_text_edit()
        if not text_edit:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "다른 이름으로 저장", "", "모든 파일 (*);;텍스트 파일 (*.txt)")
        if file_path:
            self._save_to_path(file_path, text_edit)

    def _save_to_path(self, file_path, text_edit):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_edit.toPlainText())
            text_edit.file_path = file_path
            text_edit.modified = False
            self.update_tab_title(text_edit)
            self.statusBar().showMessage(f"'{os.path.basename(file_path)}' 저장됨", 2000)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"파일을 저장할 수 없습니다: {e}")

    def close_tab(self, index):
        text_edit = self.tab_widget.widget(index)
        if text_edit.modified:
            reply = QMessageBox.question(self, '저장 확인',
                                         f"'{self.tab_widget.tabText(index).replace('*', '')}' 파일이 변경되었습니다. 저장하시겠습니까?",
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                         QMessageBox.Save)
            if reply == QMessageBox.Save:
                self.tab_widget.setCurrentIndex(index) # Switch to the tab to save it
                self.save_file()
                if text_edit.modified: # If save failed or user cancelled save dialog
                    return
            elif reply == QMessageBox.Cancel:
                return
        self.tab_widget.removeTab(index)
        self.update_status_bar() # Update status bar after tab is closed

    def closeEvent(self, event):
        for i in range(self.tab_widget.count()):
            text_edit = self.tab_widget.widget(i)
            if text_edit.modified:
                self.tab_widget.setCurrentIndex(i) # Switch to the tab to prompt for save
                reply = QMessageBox.question(self, '저장 확인',
                                             f"'{self.tab_widget.tabText(i).replace('*', '')}' 파일이 변경되었습니다. 저장하시겠습니까?",
                                             QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                             QMessageBox.Save)
                if reply == QMessageBox.Save:
                    self.save_file()
                    if text_edit.modified: # If save failed or user cancelled save dialog
                        event.ignore() # Prevent closing if save was cancelled
                        return
                elif reply == QMessageBox.Cancel:
                    event.ignore() # Prevent closing
                    return
        event.accept()

    def set_font(self):
        text_edit = self.current_text_edit()
        if text_edit:
            font, ok = QFontDialog.getFont(text_edit.font(), self)
            if ok:
                text_edit.setFont(font)

    def toggle_word_wrap(self):
        text_edit = self.current_text_edit()
        if text_edit:
            if self.word_wrap_action.isChecked():
                text_edit.setWordWrapMode(QTextEdit.WidgetWidth)
            else:
                text_edit.setWordWrapMode(QTextEdit.NoWrap)
