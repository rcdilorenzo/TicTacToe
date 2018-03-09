import urwid as uw
from urwid_timed_progress import TimedProgressBar

PROGRESS = 'progress'
METADATA = 'metadata'

PALETTE = [
    ('normal',   'white', 'black', 'standout'),
    ('complete', 'white', 'dark green'),
]

def setup(epochs):
    (screen, ui) = training_screen(epochs)
    return (uw.MainLoop(screen, PALETTE), ui)

# @mutates
def train_cycle_finished(loop, ui):
    ui[PROGRESS].add_progress(1)
    draw(loop)

# Private Functions

def training_screen(epochs):
    title = uw.Text(u"Tic-Tac-Toe Reinforcement Learning", align = 'center')
    progress = TimedProgressBar('normal', 'complete', units = 'epochs',
                                label = 'Training', done = epochs)
    items = uw.ListBox([title, uw.Divider(), progress])
    screen = uw.Padding(uw.Filler(items, height = 4), left = 5, right = 5)
    return (screen, { PROGRESS: progress })

# @mutates
def draw(loop):
    loop.draw_screen()
