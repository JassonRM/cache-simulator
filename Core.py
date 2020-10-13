from Cache import Cache
from Processor import Processor
from Control import Control


class Core:
    def __init__(self, identifier, bus):
        self.id = identifier
        self.cache = Cache()
        self.controller = Control(identifier, self.cache, bus)
        self.processor = Processor(self.controller)
