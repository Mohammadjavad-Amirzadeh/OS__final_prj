import threading
from clock import clock
import time

clock = clock()

clock_thread = threading.Thread(target=clock.run)

clock_thread.start()



temp_counter = 0
for i in range(100_000_000):
    if clock.situation == 1 and temp_counter != clock.counter:
        print("CLOCK IS : ", clock.situation)
        temp_counter = clock.counter
        print("COUNTER : ", temp_counter)

clock_thread.join()

