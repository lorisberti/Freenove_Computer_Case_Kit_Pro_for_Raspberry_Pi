from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class TestTab(QWidget):
    def __init__(self, width=480, height=740):
        super().__init__()
        
        # Initialize dimensions and scale factor
        self.window_width = width
        self.window_height = height
        self.scale_factor = 1.0
        
        # Initialize interface
        self.initUI()
        
    def initUI(self):
        """Initialize UI function"""
        layout = QVBoxLayout()
        label = QLabel("Debug Tab")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
        
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))
        self.setStyleSheet("background-color: #333333;")  

    def resetUiSize(self, width, height):
        """Reset UI size"""
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

    def reloadUi(self):
        """Reload UI function"""
        pass

    def resizeEvent(self, event):
        """Handle window resize event"""
        super().resizeEvent(event)
        self.reloadUi()

    def keyPressEvent(self, event):
        """Handle keyboard key press events"""
        pass