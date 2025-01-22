import threading
import time

def print_cube(num):
    print("Cube: {}" .format(num * num * num))


def print_square(num):
    time.sleep(0.5)
    print("Square: {}" .format(num * num))


if __name__ =="__main__":
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))

    t1.start()
    t2.start()
    print("Done!")
    t1.join()
    t2.join()

   
