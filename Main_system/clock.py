import threading
import time

class clock:
    def __init__(self):
        self.clock_id = 0
        self.situation = 1
        self.counter = 0
    
    def run(self):
        while True:
            self.situation *= -1
            # print(self.timer)
            # time.sleep(.1)
            self.counter += 1
            self.counter = self.counter % 1561651651697
            if self.counter == 100_000_000:
                break

