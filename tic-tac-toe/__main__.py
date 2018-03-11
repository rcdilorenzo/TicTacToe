import app
import thread

(loop, ui) = app.setup()

# Spawn thread for running app in background
thread.start_new_thread(app.run, (loop, ui))

# Urwid requires being on main thread
loop.run()
