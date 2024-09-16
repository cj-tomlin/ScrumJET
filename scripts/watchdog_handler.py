import os
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def is_cache_file(file_path):
    # Ignore __pycache__ directories and .pyc files
    return '__pycache__' in file_path or file_path.endswith('.pyc')


def trigger_flask_reload():
    # Touch the `run.py` to force Flask reload
    with open('run.py', 'a'):
        os.utime('run.py', None)
    print("Flask reload triggered.")


class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and not is_cache_file(event.src_path):
            print(f"File modified: {event.src_path}")
            # Touch the run.py file to trigger Flask reload
            if event.src_path.endswith('.py') or event.src_path.endswith('.html') or event.src_path.endswith('.css'):
                trigger_flask_reload()

    def on_created(self, event):
        if not event.is_directory and not is_cache_file(event.src_path):
            print(f"File created: {event.src_path}")
            if event.src_path.endswith('.py') or event.src_path.endswith('.html') or event.src_path.endswith('.css'):
                trigger_flask_reload()

    def on_deleted(self, event):
        if not event.is_directory and not is_cache_file(event.src_path):
            print(f"File deleted: {event.src_path}")
            if event.src_path.endswith('.py') or event.src_path.endswith('.html') or event.src_path.endswith('.css'):
                trigger_flask_reload()


def start_watchdog(path_to_watch):
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the program running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
