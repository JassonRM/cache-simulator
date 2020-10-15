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
        grid.addWidget(label, 0, 0, 1, 2)

        latency = "Latency: " + str(self.memory.latency)
        self.latency_label = QLabel(latency)
        grid.addWidget(self.latency_label, 0, 2, 1, 2)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setRowCount(self.memory.size // 8)

        for i in range(8):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(bin(i)[2:].zfill(3)))

        self.table.setVerticalHeaderItem(0, QTableWidgetItem("0"))
        self.table.setVerticalHeaderItem(1, QTableWidgetItem("1"))

        for i in range(self.memory.size):
            self.table.setItem(i // 8, i % 8, QTableWidgetItem(self.memory.data[i]))

        self.table.resizeColumnsToContents()
        grid.addWidget(self.table, 1, 0, 1, 4)

        self.setLayout(grid)

    def refresh(self):
        latency = "Latency: " + str(self.memory.latency)
        self.latency_label.setText(latency)
        for i in range(self.memory.size):
            self.table.setItem(i // 8, i % 8, QTableWidgetItem(self.memory.data[i]))
        self.repaint()
