from app import create_app
import threading
from scripts.watchdog_handler import start_watchdog

app = create_app()

if __name__ == '__main__':
    path_to_watch = './app'

    # Start Watchdog in a separate thread
    watcher_thread = threading.Thread(target=start_watchdog, args=(path_to_watch,))
    watcher_thread.daemon = True
    watcher_thread.start()

    # Start the Flask app
    app.run(debug=True)
