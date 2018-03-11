# Fancy CLI
import urwid as uw

# Time-estimated progress bar
from urwid_timed_progress import TimedProgressBar

# Pretty-print AI rewards
from tabulate import tabulate

from board_move import State as Move
import board, agent, app

PROGRESS = 'progress'
METADATA = 'metadata'
BUTTONS = 'buttons'
STATUS = 'status'
LOOP = 'loop'
AI_DESCRIPTION = 'ai-description'

# Color palette to reference by first key
PALETTE = [
    ('normal',   'white', 'black', 'standout'),
    ('complete', 'white', 'dark green'),
]

def setup(epochs):
    """Setup training interface """
    (screen, ui) = _training_screen(epochs)

    # Return main loop with color palette
    return (uw.MainLoop(screen, PALETTE), ui)

# @mutates
def train_epoch_finished(loop, ui):
    """Update UI for epoch being finished"""
    ui[PROGRESS].add_progress(1)
    _draw(loop)

# @mutates
def setup_game_play(loop, app_state, button_callback):
    """Replace training progress with game screen"""
    (screen, app_state) = _game_screen(app_state, button_callback)
    loop.widget = screen
    _draw(loop)
    app_state.ui[LOOP] = loop
    return app_state

# @mutates
def update_board(app_state):
    """Generic update to the game screen"""

    # Update button labels based on board state
    board_state = app_state.board_state
    buttons = app_state.ui[BUTTONS]
    for i in range(0, len(buttons)):
        buttons[i].set_label(board.at(board_state, i))

    # Display current rewards for various positions
    reward_matrix = agent.reward_matrix(app_state.agent_state, board_state)
    text = tabulate(reward_matrix, floatfmt = '.3f', tablefmt = 'fancy_grid')
    app_state.ui[AI_DESCRIPTION].set_text(text)

    # Update status text
    app_state.ui[STATUS].set_text('Status: Your Move')

    # Explicitly update UI
    _draw(app_state.ui[LOOP])

# @mutates
def set_invalid_move_state(app_state):
    """Display invalid move as status message"""
    app_state.ui[STATUS].set_text('Status: Invalid Move')

# @mutates
def game_finished(app_state):
    """
    Display overlay of current screen of game result and ask about whether to
    start another game
    """
    loop = app_state.ui[LOOP]

    # Set status
    app_state.ui[STATUS].set_text('Status: Game Over')

    # Create restart callback for communicating with app
    restart = lambda _: app.play_game(loop, app_state.rewards_state)

    # Setup dialog as overlay of current widget
    (dialog, app_state) = _start_over_screen(app_state, restart)
    loop.widget = uw.Overlay(dialog, loop.widget,
                             'center', ('relative', 50), 'middle',
                             10, 30, 8)
    _draw(loop)

def _training_screen(epochs):
    """Progress view of training epochs"""
    # Basic title
    title = uw.Text('Tic Tac Toe Reinforcement Learning', align = 'center')

    # Progress bar that estimates remaining time
    progress = TimedProgressBar('normal', 'complete', units = 'epochs',
                                label = 'Training', done = epochs)

    # Combine title and progress bar and center vertically
    items = uw.ListBox([title, uw.Divider(), progress])
    screen = uw.Padding(uw.Filler(items, height = 4), left = 5, right = 5)
    return (screen, { PROGRESS: progress })

# @mutates
def _game_screen(app_state, callback):
    """Create game screen of board, AI view, and status"""
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
    ai_description = uw.Text('Waiting for first move...', align = 'center')
    ai_column = uw.ListBox([
        uw.Divider(), uw.Text('AI Brain', align = 'center'),
        uw.Divider(), uw.LineBox(ai_description)])

    # Assemble composite screen
    status = uw.Text('Status: Your Move', align = 'center')
    columns = uw.Columns([game_column, ai_column])
    screen = uw.Pile([
        ('weight', 1, columns),
        ('pack', status), ('pack', uw.Divider())
    ])

    # Assign elements to UI state for later updating
    app_state.ui[BUTTONS] = buttons
    app_state.ui[STATUS] = status
    app_state.ui[AI_DESCRIPTION] = ai_description

    return (screen, app_state)

def _start_over_screen(app_state, callback):
    """Dialog for last game result and prompt for new one"""
    question = " Would you like to start another game?"
    text = uw.Text(_winner_description(app_state) + question, align = 'center')

    # Create two questions on bottom of dialog
    grid = uw.GridFlow([
        uw.Button('Yes', on_press = callback),
        uw.Button('No', on_press = _exit)
    ], 7, 2, 2, 'center')

    # Create vertical flow of message and buttons
    screen = uw.Padding(uw.ListBox([uw.Divider(), text, uw.Divider(), grid]),
                        left = 5, right = 5)

    return (screen, app_state)

def _exit(_sender):
    """Exit the interface"""
    raise uw.ExitMainLoop()

def _winner_description(app_state):
    """Helper function for describing the game result in the UI"""
    agent_id = app_state.agent_state.identifier
    if board.is_win(app_state.board_state, agent_id):
        return "The AI wins!"
    elif board.is_win(app_state.board_state, board.not_id(agent_id)):
        return "You win!"
    else:
        return "Bummer. It's a draw."

def _move_btn(column, row, callback):
    """Helper function for creating position buttons"""
    return uw.Button(' ', on_press = callback,
                     user_data = Move(row = row, column = column))

# @mutates
def _draw(loop):
    """Helper method to request a UI repaint"""
    loop.draw_screen()
