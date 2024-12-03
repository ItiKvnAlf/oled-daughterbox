import threading

def start_thread(target: callable):
    """
    Start a new thread with the given target function.
    The thread is set as a daemon thread, so it will not block the main thread from exiting.
    Args:
        target (function): The function to run in the thread.
    """    
    thread = threading.Thread(target=target, daemon=True)
    thread.start()
