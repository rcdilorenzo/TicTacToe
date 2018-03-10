import urwid as uw
from urwid_timed_progress import TimedProgressBar
import threading

from board_move import State as Move
import board

PROGRESS = 'progress'
METADATA = 'metadata'
BUTTONS = 'buttons'
STATUS = 'status'
LOOP = 'loop'

PALETTE = [
    ('normal',   'white', 'black', 'standout'),
    ('complete', 'white', 'dark green'),
]

def setup(epochs):
    (screen, ui) = _training_screen(epochs)
    return (uw.MainLoop(screen, PALETTE), ui)

# @mutates
def train_epoch_finished(loop, ui):
    ui[PROGRESS].add_progress(1)
    _draw(loop)

# @mutates
def setup_game_play(loop, app_state, button_callback):
    (screen, app_state) = _game_screen(app_state, button_callback)
    loop.widget = screen
    _draw(loop)
    app_state.ui[LOOP] = loop
    return app_state

# @mutates
def update_board(app_state):
    board_state = app_state.board_state
    buttons = app_state.ui[BUTTONS]
    for i in range(0, len(buttons)):
        buttons[i].set_label(board.at(board_state, i))

def game_finished(app_state):
    print("TODO: Implement game_finished")

def _training_screen(epochs):
    title = uw.Text('Tic Tac Toe Reinforcement Learning', align = 'center')
    progress = TimedProgressBar('normal', 'complete', units = 'epochs',
                                label = 'Training', done = epochs)
    items = uw.ListBox([title, uw.Divider(), progress])
    screen = uw.Padding(uw.Filler(items, height = 4), left = 5, right = 5)
    return (screen, { PROGRESS: progress })

# @mutates
def _game_screen(app_state, callback):
    buttons = [
        _move_btn(0, 0, callback), _move_btn(1, 0, callback),
        _move_btn(2, 0, callback), _move_btn(0, 1, callback),
        _move_btn(1, 1, callback), _move_btn(2, 1, callback),
        _move_btn(0, 2, callback), _move_btn(1, 2, callback),
        _move_btn(2, 2, callback)
    ]
    # Create game column
    grid = uw.GridFlow(buttons, 5, 2, 2, 'center')
    padded_grid = uw.Padding(grid, align = 'center', width = 20)
    header = uw.Text('Tic Tac Toe', align = 'center')
    game_column = uw.ListBox([uw.Divider(), header, uw.Divider(), padded_grid])

    # Describe AI view
    ai_column = uw.ListBox([
        uw.Divider(), uw.Text('AI Brain', align = 'center'),
        uw.Divider(), uw.LineBox(uw.Text('Blah', align = 'center'))])

    # Assemble composite screen
    status = uw.Text('Status: Your Move', align = 'center')
    columns = uw.Columns([game_column, ai_column])
    screen = uw.Pile([
        ('weight', 1, columns),
        ('pack', status), ('pack', uw.Divider())
    ])

    app_state.ui[BUTTONS] = buttons
    app_state.ui[STATUS] = status
    return (screen, app_state)

def _move_btn(column, row, callback):
    return uw.Button(' ', on_press = callback,
                     user_data = Move(row = row, column = column))

# @mutates
def _draw(loop):
    loop.draw_screen()
