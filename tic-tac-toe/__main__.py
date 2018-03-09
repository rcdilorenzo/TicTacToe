import app
import thread

(loop, ui, state) = app.setup()

print("Starting...")
thread.start_new_thread(app.run, (loop, ui, state))
loop.run()
