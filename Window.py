from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from MemoryWidget import MemoryWidget
from CoreWidget import CoreWidget
import time
import threading


class Window(QWidget):
    refresh = pyqtSignal()

    def __init__(self, clock, cores, memory):
        super().__init__()
        self.clock = clock
        self.cores = cores
        self.memory = memory
        self.cores_widgets = []
        self.memory_widget = None
        self.running = False
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle("Cache Simulator")

        for core in self.cores:
            self.cores_widgets.append(CoreWidget(core))

        next_step_btn = QPushButton("Next step", self)
        next_step_btn.clicked.connect(self.next_step_clicked)
        self.next_n_steps_edit = QLineEdit()
        self.next_n_steps_edit.setPlaceholderText("Number of steps")
        self.next_n_steps_edit.setFixedWidth(140)
        next_n_steps_btn = QPushButton("Next n steps", self)
        next_n_steps_btn.clicked.connect(self.next_n_steps_clicked)
        play_btn = QPushButton("Play", self)
        play_btn.clicked.connect(self.play_clicked)
        self.refresh.connect(self.next_step_clicked)
        stop_btn = QPushButton("Stop", self)
        stop_btn.clicked.connect(self.stop_clicked)

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
        btn_hbox.addWidget(self.next_n_steps_edit)
        btn_hbox.addWidget(next_n_steps_btn)
        btn_hbox.addWidget(play_btn)
        btn_hbox.addWidget(stop_btn)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)

        self.show()

    @pyqtSlot()
    def next_step_clicked(self):
        self.clock.set()
        for core_widget in self.cores_widgets:
            core_widget.refresh()
        self.memory_widget.refresh()

    @pyqtSlot()
    def next_n_steps_clicked(self):
        self.running = True
        threading.Thread(target=self.next_n_steps).start()

    def next_n_steps(self):
        n = int(self.next_n_steps_edit.text())
        for i in range(n):
            if not self.running:
                return
            self.refresh.emit()
            time.sleep(1)

    @pyqtSlot()
    def play_clicked(self):
        self.running = True
        threading.Thread(target=self.play).start()

    def play(self):
        while self.running:
            self.refresh.emit()
            time.sleep(1)

    @pyqtSlot()
    def stop_clicked(self):
        self.running = False
