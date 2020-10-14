from PyQt5.QtWidgets import *
from Processor import Instruction
from PyQt5.QtCore import pyqtSlot


class CoreWidget(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        title = "Core " + str(self.core.id)
        title_label = QLabel(title)
        grid.addWidget(title_label, 1, 0, 1, 3)

        self.current_inst_label = QLabel("Current instruction: ")
        grid.addWidget(self.current_inst_label, 2, 0, 1, 3)

        next_inst_label = QLabel("Next instruction:")
        self.next_inst_edit = QLineEdit()
        next_inst_btn = QPushButton("Set", self)
        next_inst_btn.clicked.connect(self.set_next_instruction)
        grid.addWidget(next_inst_label, 3, 0)
        grid.addWidget(self.next_inst_edit, 3, 1)
        grid.addWidget(next_inst_btn, 3, 2)

        self.cache_table = QTableWidget()
        self.cache_table.setRowCount(self.core.cache.size)
        self.cache_table.setColumnCount(2)

        self.cache_table.setHorizontalHeaderLabels(["Set 1", "Set 2"])

        for i in range(self.core.cache.size):
            self.cache_table.setVerticalHeaderItem(i, QTableWidgetItem(str(i)))
            self.cache_table.setItem(i, 0, QTableWidgetItem(self.core.cache.data1[i]))
            self.cache_table.setItem(i, 1, QTableWidgetItem(self.core.cache.data2[i]))

        grid.addWidget(self.cache_table, 4, 0, self.core.cache.size, 3)

        self.setLayout(grid)

    def refresh(self):
        print(self.core.processor.currentInstruction)
        instruction = "Current instruction: "
        if self.core.processor.currentInstruction == Instruction.CALC:
            instruction += "calc"
        elif self.core.processor.currentInstruction == Instruction.READ:
            instruction += "read " + self.core.processor.currentAddress[2:]
        elif self.core.processor.currentInstruction == Instruction.WRITE:
            instruction += "write " + self.core.processor.currentAddress[2:] \
                           + " " + self.core.processor.currentData

        self.current_inst_label.setText(instruction)

        for i in range(self.core.cache.size):
            self.cache_table.setItem(i, 0, QTableWidgetItem(self.core.cache.data1[i]))
            self.cache_table.setItem(i, 1, QTableWidgetItem(self.core.cache.data2[i]))

        self.repaint()

    @pyqtSlot()
    def set_next_instruction(self):
        instruction = self.next_inst_edit.text()
        self.core.processor.set_next_instruction(instruction)