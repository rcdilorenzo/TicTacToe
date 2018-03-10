import app
import thread

(loop, ui) = app.setup()

print("Starting...")
thread.start_new_thread(app.run, (loop, ui))
loop.run()
