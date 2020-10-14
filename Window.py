from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from MemoryWidget import MemoryWidget
from CoreWidget import CoreWidget


class Window(QWidget):
    def __init__(self, clock, cores, memory):
        super().__init__()
        self.clock = clock
        self.cores = cores
        self.memory = memory
        self.initUI()

    def initUI(self):
        self.resize(600, 900)
        self.setWindowTitle("Cache Simulator")

        self.cores_widgets = []
        for core in self.cores:
            self.cores_widgets.append(CoreWidget(core))

        next_step_btn = QPushButton("Next step", self)
        next_step_btn.clicked.connect(self.next_step_clicked)
        next_n_steps_btn = QPushButton("Next n steps", self)
        play_btn = QPushButton("Play", self)
        stop_btn = QPushButton("Stop", self)

        vbox = QVBoxLayout()

        core12_hbox = QHBoxLayout()
        core12_hbox.addWidget(self.cores_widgets[0])
        core12_hbox.addWidget(self.cores_widgets[1])
        vbox.addLayout(core12_hbox)

        core34_hbox = QHBoxLayout()
        core34_hbox.addWidget(self.cores_widgets[2])
        core34_hbox.addWidget(self.cores_widgets[3])
        vbox.addLayout(core34_hbox)

        self.memory_widget = MemoryWidget(self.memory)
        vbox.addWidget(self.memory_widget)

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(next_step_btn)
        btn_hbox.addWidget(next_n_steps_btn)
        btn_hbox.addWidget(play_btn)
        btn_hbox.addWidget(stop_btn)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)

        self.show()

    @pyqtSlot()
    def next_step_clicked(self):
        self.clock.set()
        self.clock.clear()
        for core_widget in self.cores_widgets:
            core_widget.refresh()
