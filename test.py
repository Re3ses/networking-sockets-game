from _thread import start_new_thread
import time

def print_numbers(number):
    for i in range(number):
        print(i)

start_new_thread(print_numbers, (10,))

# Add a delay to give the new thread time to execute
time.sleep(5)