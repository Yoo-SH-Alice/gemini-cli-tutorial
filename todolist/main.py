import sys
from PyQt5.QtWidgets import QApplication
from todo_app import TodoApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TodoApp()
    ex.show()
    sys.exit(app.exec_())
