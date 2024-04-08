import threading


def run_in_new_thread(func):
    # Create a new thread and run the function in it
    thread = threading.Thread(target=func)

    # Start the new thread
    thread.start()

    # Return the thread
    return thread
