import threading
from Bus import Bus
from Core import Core
from Memory import Memory
import sys, os
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from Window import Window


def main():
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
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Window(clock, cores, memory)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
