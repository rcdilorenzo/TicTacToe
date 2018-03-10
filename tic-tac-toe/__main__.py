import app
import thread

(loop, ui) = app.setup()

thread.start_new_thread(app.run, (loop, ui))
loop.run()
