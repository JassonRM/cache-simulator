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
        grid.addWidget(label, 0, 0, 1, 3)

        latency = "Latency: " + str(self.memory.latency)
        self.latency_label = QLabel(latency)
        grid.addWidget(self.latency_label, 0, 2, 1, 2)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setRowCount(self.memory.size // 4)

        for i in range(4):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(str(i)))

        for i in range(self.memory.size):
            self.table.setItem(i // 4, i % 4, QTableWidgetItem(self.memory.data[i]))

        grid.addWidget(self.table, 1, 0, 2, 6)

        self.setLayout(grid)

    def refresh(self):
        latency = "Latency: " + str(self.memory.latency)
        self.latency_label = QLabel(latency)
        for i in range(self.memory.size):
            self.table.setItem(i // 4, i % 4, QTableWidgetItem(self.memory.data[i]))
        self.repaint()
