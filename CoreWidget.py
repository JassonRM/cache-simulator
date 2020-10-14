from PyQt5.QtWidgets import *
from Processor import Instruction


class CoreWidget(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        title = "Core " + str(self.core.id)
        self.title_label = QLabel(title)
        grid.addWidget(self.title_label, 1, 0, 1, 3)

        self.current_inst_label = QLabel("Current instruction: ")
        grid.addWidget(self.current_inst_label, 2, 0, 1, 3)

        next_inst_label = QLabel("Next instruction:")
        next_inst_edit = QLineEdit()
        next_inst_btn = QPushButton("Set", self)
        grid.addWidget(next_inst_label, 3, 0)
        grid.addWidget(next_inst_edit, 3, 1)
        grid.addWidget(next_inst_btn, 3, 2)

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
        self.repaint()
