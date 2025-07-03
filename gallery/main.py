import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QAction, QFileDialog
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt
import os

class ImageGalleryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Gallery")
        self.setGeometry(100, 100, 800, 600)

        self.image_files = []
        self.current_image_index = -1
        self.rotation_angle = 0 # Initialize rotation angle

        self.init_ui()

    def init_ui(self):
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout() # Main vertical layout
        self.image_nav_layout = QHBoxLayout() # Layout for image and navigation buttons
        self.rotate_button_layout = QHBoxLayout() # Layout for rotate button

        # Navigation Buttons
        self.prev_button = QPushButton("<")
        self.prev_button.clicked.connect(self.show_previous_image)
        self.prev_button.setFixedSize(50, 50)
        self.image_nav_layout.addWidget(self.prev_button, alignment=Qt.AlignVCenter)

        # Image Display
        self.image_label = QLabel("No Image Loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_nav_layout.addWidget(self.image_label, 1) # Stretch factor for image label

        self.next_button = QPushButton(">")
        self.next_button.clicked.connect(self.show_next_image)
        self.next_button.setFixedSize(50, 50)
        self.image_nav_layout.addWidget(self.next_button, alignment=Qt.AlignVCenter)

        # Rotate Button
        self.rotate_button = QPushButton("Rotate")
        self.rotate_button.clicked.connect(self.rotate_image)
        self.rotate_button.setFixedSize(100, 50) # Adjusted size for better appearance
        self.rotate_button_layout.addStretch(1) # Add stretch to center the button
        self.rotate_button_layout.addWidget(self.rotate_button)
        self.rotate_button_layout.addStretch(1) # Add stretch to center the button

        # Add sub-layouts to main layout
        self.main_layout.addLayout(self.image_nav_layout)
        self.main_layout.addLayout(self.rotate_button_layout)

        self.central_widget.setLayout(self.main_layout)

        # Menu Bar
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder_path:
            self.image_files = []
            valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith(valid_extensions):
                    self.image_files.append(os.path.join(folder_path, file_name))
            
            self.image_files.sort() # Sort files for consistent order

            if self.image_files:
                self.current_image_index = 0
                self.rotation_angle = 0 # Reset rotation when opening new folder
                self.display_image()
            else:
                self.image_label.setText("No images found in selected folder.")
                self.current_image_index = -1

    def display_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            image_path = self.image_files[self.current_image_index]
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Apply rotation
                transform = QTransform().rotate(self.rotation_angle)
                rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

                # Scale pixmap to fit label while maintaining aspect ratio
                scaled_pixmap = rotated_pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setText("") # Clear "No Image Loaded" text
            else:
                self.image_label.setText(f"Could not load image: {os.path.basename(image_path)}")
        else:
            self.image_label.setText("No Image Loaded")

    def show_previous_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
            self.rotation_angle = 0 # Reset rotation when changing image
            self.display_image()

    def show_next_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.rotation_angle = 0 # Reset rotation when changing image
            self.display_image()

    def rotate_image(self):
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.display_image()

    def resizeEvent(self, event):
        # Recalculate and display image when window is resized
        self.display_image()
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gallery_app = ImageGalleryApp()
    gallery_app.show()
    sys.exit(app.exec_())
