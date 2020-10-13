import threading
from Bus import Bus
from Core import Core
from Memory import Memory
import sys, os
from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class Window(QWidget):
    def __init__(self, cores, memory):
        super().__init__()
        self.cores = cores
        self.memory = memory
        self.initUI()

    def initUI(self):
        self.resize(600, 900)
        self.setWindowTitle("Cache Simulator")
        next_step_btn = QPushButton("Next step", self)
        next_n_steps_btn = QPushButton("Next n steps", self)
        play_btn = QPushButton("Play", self)
        stop_btn = QPushButton("Stop", self)

        vbox = QVBoxLayout()

        core12_hbox = QHBoxLayout()
        core12_hbox.addWidget(Core_Widget(self.cores[0]))
        core12_hbox.addWidget(Core_Widget(self.cores[1]))
        vbox.addLayout(core12_hbox)

        core34_hbox = QHBoxLayout()
        core34_hbox.addWidget(Core_Widget(self.cores[2]))
        core34_hbox.addWidget(Core_Widget(self.cores[3]))
        vbox.addLayout(core34_hbox)

        vbox.addWidget(Memory_Widget(self.memory))

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(next_step_btn)
        btn_hbox.addWidget(next_n_steps_btn)
        btn_hbox.addWidget(play_btn)
        btn_hbox.addWidget(stop_btn)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)

        self.show()


class Core_Widget(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        title = "Core " + str(self.core.id)
        label = QLabel(title)
        grid.addWidget(label, 1, 0, 1, 3)

        next_inst_label = QLabel("Next instruction:")
        next_inst_edit = QLineEdit()
        next_inst_btn = QPushButton("Set", self)
        grid.addWidget(next_inst_label, 2, 0)
        grid.addWidget(next_inst_edit, 2, 1)
        grid.addWidget(next_inst_btn, 2, 2)

        self.setLayout(grid)


class Memory_Widget(QWidget):
    def __init__(self, memory):
        super().__init__()
        self.memory = memory
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        label = QLabel("Memory")
        grid.addWidget(label, 1, 0, 1, 3)

        latency = "Latency: " + str(memory.latency)
        latency_label = QLabel(latency)
        grid.addWidget(latency_label, 1, 2, 1, 3)

        self.setLayout(grid)


if __name__ == '__main__':
    clock = threading.Event()
    memory = Memory()
    bus = Bus(memory)
    cores = [Core(1, bus), Core(2, bus), Core(3, bus), Core(4, bus)]
    bus.set_cores(cores)

    core_threads = []
    for core in cores:
        thread = threading.Thread(target=core.processor.run, args=(clock,))
        thread.start()
        core_threads.append(thread)
    mem_thread = threading.Thread(target=memory.run, args=(clock,))
    mem_thread.start()

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    window = Window(cores, memory)
    sys.exit(app.exec_())

    # for i in range(1000):
    #     for core in cores:
    #         print("Core ", core.id)
    #         print("Current instruction: ", core.processor.currentInstruction, core.processor.currentAddress,
    #               core.processor.currentData)
    #         print(core.cache.tags1)
    #         print(core.cache.tags2)
    #         print(core.cache.data1)
    #         print(core.cache.data2)
    #
    #     print("Memory")
    #     print(memory.data)
    #
    #     clock.set()
    #     clock.clear()
    #     print("--------------------------------------------CLOCK------------------------------------------")


