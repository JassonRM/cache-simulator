from PyQt5.QtWidgets import *
from Processor import Instruction
from PyQt5.QtCore import pyqtSlot
from Cache import State


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
        reset_btn = QPushButton("Reset", self)
        reset_btn.clicked.connect(self.reset_next_instruction)
        grid.addWidget(next_inst_label, 3, 0)
        grid.addWidget(self.next_inst_edit, 3, 1)
        grid.addWidget(next_inst_btn, 3, 2)
        grid.addWidget(reset_btn, 3, 3)

        self.cache_table = QTableWidget()
        self.cache_table.setRowCount(self.core.cache.size)
        self.cache_table.setColumnCount(6)

        self.cache_table.setHorizontalHeaderLabels(
            ["Tags 1", "Way 1", "States 1", "Tags 2", "Way 2", "States 2"])

        self.refresh()

        grid.addWidget(self.cache_table, 4, 0, self.core.cache.size, 4)

        self.setLayout(grid)

    def refresh(self):
        if not self.core.processor.using_mem:
            self.core.processor.instruction_ready.wait()
        instruction = "Current instruction: "
        if self.core.processor.currentInstruction == Instruction.CALC:
            instruction += "calc"
        elif self.core.processor.currentInstruction == Instruction.READ:
            instruction += "read " + self.core.processor.currentAddress[2:].zfill(4)
        elif self.core.processor.currentInstruction == Instruction.WRITE:
            instruction += "write " + self.core.processor.currentAddress[2:].zfill(4) \
                           + " " + self.core.processor.currentData
        self.current_inst_label.setText(instruction)

        for i in range(self.core.cache.size):
            self.cache_table.setVerticalHeaderItem(i, QTableWidgetItem(str(i)))
            self.cache_table.setItem(i, 0, QTableWidgetItem(
                bin(self.core.cache.tags1[i])[2:].zfill(3)))
            self.cache_table.setItem(i, 1, QTableWidgetItem(
                self.core.cache.data1[i]))
            self.cache_table.setItem(i, 2, QTableWidgetItem(
                self.get_state_letter(self.core.cache.states1[i])))
            self.cache_table.setItem(i, 3, QTableWidgetItem(
                bin(self.core.cache.tags2[i])[2:].zfill(3)))
            self.cache_table.setItem(i, 4, QTableWidgetItem(
                self.core.cache.data2[i]))
            self.cache_table.setItem(i, 5, QTableWidgetItem(
                self.get_state_letter(self.core.cache.states2[i])))

        self.cache_table.resizeColumnsToContents()
        self.repaint()
        self.core.processor.instruction_ready.clear()

    @pyqtSlot()
    def set_next_instruction(self):
        instruction = self.next_inst_edit.text()
        try:
            self.core.processor.set_next_instruction(instruction)
        except ValueError as err:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(err.__str__())
            msg.setWindowTitle("Error")
            msg.exec_()

    @pyqtSlot()
    def reset_next_instruction(self):
        self.core.processor.reset_next_instruction()

    def get_state_letter(self, state):
        if state == State.MODIFIED:
            return "M"
        elif state == State.OWNED:
            return "O"
        elif state == State.EXCLUSIVE:
            return "E"
        elif state == State.SHARED:
            return "S"
        elif state == State.INVALID:
            return "I"
