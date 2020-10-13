import threading
from Bus import Bus
from Core import Core
from Memory import Memory

if __name__ == '__main__':
    clock = threading.Event()
    memory = Memory()
    bus = Bus(memory)
    cores = [Core(1, bus), Core(2, bus)]
    bus.set_cores(cores)

    core_threads = []
    for core in cores:
        thread = threading.Thread(target=core.processor.run, args=(clock,))
        thread.start()
        core_threads.append(thread)
    mem_thread = threading.Thread(target=memory.run, args=(clock,))
    mem_thread.start()

    for i in range(1000):
        for core in cores:
            print("Core ", core.id)
            print("Current instruction: ", core.processor.currentInstruction, core.processor.currentAddress,
                  core.processor.currentData)
            print(core.cache.tags1)
            print(core.cache.tags2)
            print(core.cache.data1)
            print(core.cache.data2)

        print("Memory")
        print(memory.data)

        clock.set()
        clock.clear()
        print("--------------------------------------------CLOCK------------------------------------------")


