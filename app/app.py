import sys
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LostARK StoneHelper")
        self.setFixedSize(QSize(560, 460))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # settings layout
        layout1 = QHBoxLayout()
        layout1.addWidget(self.setModeLayout())
        layout1.addWidget(self.setMonitorLayout())
        main_layout.addLayout(layout1)

        # detection layout
        layout2 = QVBoxLayout()
        layout2.addWidget(self.setDetectionLayout())
        main_layout.addLayout(layout2)

        # engraving layout
        layout3 = QVBoxLayout()
        layout3.addWidget(self.setEngravingLayout())
        main_layout.addLayout(layout3)

        central_widget.setLayout(main_layout)

    def setModeLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(300, 70))
        widget.setObjectName("layout")

        label = QLabel("ModeLayout")

        layout = QHBoxLayout()
        layout.addWidget(label)

        widget.setLayout(layout)
        return widget

    def setMonitorLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(234, 70))
        widget.setObjectName("layout")

        label = QLabel("MonitorLayout")

        layout = QVBoxLayout()
        layout.addWidget(label)

        widget.setLayout(layout)
        return widget

    def setDetectionLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(540, 140))
        widget.setObjectName("layout")

        label = QLabel("DetectionLayout")

        layout = QVBoxLayout()
        layout.addWidget(label)

        widget.setLayout(layout)
        return widget

    def setEngravingLayout(self):
        widget = QWidget()
        widget.setFixedSize(QSize(540, 220))
        widget.setObjectName("layout")

        label = QLabel("EngravingLayout")

        layout = QVBoxLayout()
        layout.addWidget(label)

        widget.setLayout(layout)
        return widget


app = QApplication(sys.argv)
app.setStyleSheet(Path("qss/main.qss").read_text())

window = MainWindow()
window.show()

app.exec()
