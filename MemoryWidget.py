from PyQt5.QtWidgets import *


class MemoryWidget(QWidget):
    def __init__(self, memory):
        super().__init__()
        self.memory = memory
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        label = QLabel("Memory")
        grid.addWidget(label, 1, 0, 1, 3)

        latency = "Latency: " + str(self.memory.latency)
        latency_label = QLabel(latency)
        grid.addWidget(latency_label, 1, 2, 1, 3)

        self.setLayout(grid)
