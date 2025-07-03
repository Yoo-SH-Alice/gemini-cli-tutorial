import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
from ultralytics import YOLO

class ObjectDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt YOLO Object Detection")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Image display area
        self.image_label = QLabel("Load an image to start object detection")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid gray;")
        self.main_layout.addWidget(self.image_label)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.load_image_button = QPushButton("Load Image")
        self.detect_objects_button = QPushButton("Detect Objects")
        self.button_layout.addWidget(self.load_image_button)
        self.button_layout.addWidget(self.detect_objects_button)
        self.main_layout.addLayout(self.button_layout)

        # Connect buttons to functions
        self.load_image_button.clicked.connect(self.load_image)
        self.detect_objects_button.clicked.connect(self.detect_objects)

        self.current_image_path = None
        self.yolo_model = YOLO('yolov8n.pt') # Load a pretrained YOLOv8n model

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            self.current_image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image_label.setText("") # Clear text when image is loaded

    def detect_objects(self):
        if self.current_image_path:
            # Perform object detection
            results = self.yolo_model(self.current_image_path)

            # Draw bounding boxes and labels
            image = cv2.imread(self.current_image_path)
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = round(float(box.conf[0]), 2)
                    cls = int(box.cls[0])
                    label = self.yolo_model.names[cls]

                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(image, f"{label} {conf}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Convert OpenCV image to QPixmap and display
            h, w, ch = image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image_label.setText("Please load an image first!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ObjectDetectionApp()
    window.show()
    sys.exit(app.exec_())
