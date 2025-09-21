import streamlit as st
import random
import time

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [''] * 9
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = 'two_player'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'winning_line' not in st.session_state:
    st.session_state.winning_line = None
if 'x_score' not in st.session_state:
    st.session_state.x_score = 0
if 'o_score' not in st.session_state:
    st.session_state.o_score = 0
if 'draws' not in st.session_state:
    st.session_state.draws = 0

def reset_game():
    """Reset the game state but keep scores"""
    st.session_state.board = [''] * 9
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = None

def reset_scores():
    """Reset all scores"""
    st.session_state.x_score = 0
    st.session_state.o_score = 0
    st.session_state.draws = 0
    reset_game()

def check_winner(board):
    """Check if there's a winner and return the winning line"""
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for line in winning_lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != '':
            return line
    return None

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell != '' for cell in board) and check_winner(board) is None

def computer_move():
    """Simple AI for computer move"""
    # Check for winning move
    for i in range(9):
        if st.session_state.board[i] == '':
            temp_board = st.session_state.board.copy()
            temp_board[i] = 'O'
            if check_winner(temp_board):
                return i
    
    # Block opponent's winning move
    for i in range(9):
        if st.session_state.board[i] == '':
            temp_board = st.session_state.board.copy()
            temp_board[i] = 'X'
            if check_winner(temp_board):
                return i
    
    # Take center if available
    if st.session_state.board[4] == '':
        return 4
    
    # Take corners
    corners = [0, 2, 6, 8]
    available_corners = [i for i in corners if st.session_state.board[i] == '']
    if available_corners:
        return random.choice(available_corners)
    
    # Take any available move
    available_moves = [i for i in range(9) if st.session_state.board[i] == '']
    if available_moves:
        return random.choice(available_moves)
    
    return None

def make_move(position):
    """Handle a move by a player"""
    if st.session_state.game_over or st.session_state.board[position] != '':
        return
    
    # Make the move
    st.session_state.board[position] = st.session_state.current_player
    
    # Check for winner
    winning_line = check_winner(st.session_state.board)
    if winning_line:
        st.session_state.winner = st.session_state.current_player
        st.session_state.winning_line = winning_line
        st.session_state.game_over = True
        if st.session_state.winner == 'X':
            st.session_state.x_score += 1
        else:
            st.session_state.o_score += 1
        return
    
    # Check for draw
    if check_draw(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.draws += 1
        return
    
    # Switch player
    st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
    
    # If it's computer's turn and in vs computer mode
    if (st.session_state.game_mode == 'vs_computer' and 
        st.session_state.current_player == 'O' and 
        not st.session_state.game_over):
        # Add a small delay for better UX
        time.sleep(0.5)
        computer_position = computer_move()
        if computer_position is not None:
            make_move(computer_position)

def get_button_style(position):
    """Get the style for a button based on its state"""
    base_style = """
        height: 80px;
        width: 80px;
        font-size: 32px;
        font-weight: bold;
        border-radius: 10px;
        margin: 2px;
        border: 2px solid #4a4a4a;
        transition: all 0.3s ease;
    """
    
    if st.session_state.winning_line and position in st.session_state.winning_line:
        return f"""
            {base_style}
            background-color: #4CAF50;
            color: white;
            border-color: #45a049;
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(76, 175, 80, 0.5);
        """
    elif st.session_state.board[position] == 'X':
        return f"""
            {base_style}
            background-color: #ff6b6b;
            color: white;
            border-color: #ff5252;
        """
    elif st.session_state.board[position] == 'O':
        return f"""
            {base_style}
            background-color: #4ecdc4;
            color: white;
            border-color: #45b7af;
        """
    else:
        return f"""
            {base_style}
            background-color: #f8f9fa;
            color: #495057;
            border-color: #dee2e6;
        """

# Page configuration
st.set_page_config(
    page_title="Tic-Tac-Toe Game",
    page_icon="🎮",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .title {
        text-align: center;
        color: white;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.8);
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .status {
        text-align: center;
        color: white;
        font-size: 1.5em;
        font-weight: bold;
        margin: 20px 0;
        padding: 15px;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .game-container {
        background: rgba(255,255,255,0.95);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        margin: 20px auto;
        max-width: 400px;
    }
    .score-board {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .score-item {
        text-align: center;
        color: white;
        font-weight: bold;
    }
    .score-value {
        font-size: 2em;
        margin: 5px 0;
    }
    .score-label {
        font-size: 1em;
        opacity: 0.8;
    }
    .reset-btn {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 10px auto;
        display: block;
        width: 100%;
    }
    .reset-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .mode-btn {
        background: rgba(255,255,255,0.15);
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
        padding: 10px;
        border-radius: 15px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        text-align: center;
    }
    .mode-btn:hover {
        background: rgba(255,255,255,0.25);
    }
    .active-mode {
        background: rgba(255,255,255,0.3);
        border: 1px solid rgba(255,255,255,0.5);
        box-shadow: 0 0 15px rgba(255,255,255,0.2);
    }
    .instructions {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin-top: 30px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">🎮 Tic-Tac-Toe</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A classic game with a modern twist</div>', unsafe_allow_html=True)

# Score board
st.markdown("""
    <div class="score-board">
        <div class="score-item">
            <div class="score-label">Player X</div>
            <div class="score-value" style="color: #ff6b6b;">{}</div>
        </div>
        <div class="score-item">
            <div class="score-label">Draws</div>
            <div class="score-value">{}</div>
        </div>
        <div class="score-item">
            <div class="score-label">Player O</div>
            <div class="score-value" style="color: #4ecdc4;">{}</div>
        </div>
    </div>
""".format(st.session_state.x_score, st.session_state.draws, st.session_state.o_score), unsafe_allow_html=True)

# Game mode selection
col1, col2 = st.columns(2)
with col1:
    if st.button("👥 Two Players", use_container_width=True, key="two_player_btn"):
        st.session_state.game_mode = 'two_player'
        reset_game()
    mode_class = "mode-btn active-mode" if st.session_state.game_mode == 'two_player' else "mode-btn"
    #st.markdown(f'<div class="{mode_class}">👥 Two Players</div>', unsafe_allow_html=True)

with col2:
    if st.button("🤖 VS Computer", use_container_width=True, key="vs_computer_btn"):
        st.session_state.game_mode = 'vs_computer'
        reset_game()
    mode_class = "mode-btn active-mode" if st.session_state.game_mode == 'vs_computer' else "mode-btn"
    #st.markdown(f'<div class="{mode_class}">🤖 VS Computer</div>', unsafe_allow_html=True)

# Game container
#st.markdown('<div class="game-container">', unsafe_allow_html=True)

# Game status
if st.session_state.game_over:
    if st.session_state.winner:
        status_text = f"🎉 Player {st.session_state.winner} wins!"
        # Show winning line info
        if st.session_state.winning_line:
            line_type = ""
            if st.session_state.winning_line in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
                line_type = "row"
            elif st.session_state.winning_line in [[0, 3, 6], [1, 4, 7], [2, 5, 8]]:
                line_type = "column"
            else:
                line_type = "diagonal"
            status_text += f" (Winning {line_type})"
    else:
        status_text = "🤝 It's a draw!"
else:
    mode_text = " (Your turn)" if st.session_state.game_mode == 'two_player' or st.session_state.current_player == 'X' else " (Computer's turn)"
    status_text = f"🔄 Player {st.session_state.current_player}'s turn{mode_text}"
    
st.markdown(f'<div class="status">{status_text}</div>', unsafe_allow_html=True)

# Game board
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        for j in range(3):
            position = i * 3 + j
            button_label = st.session_state.board[position] if st.session_state.board[position] else " "
            st.markdown(f"<style>.btn-{position} {{{get_button_style(position)}}}</style>", unsafe_allow_html=True)
            if st.button(
                button_label,
                key=f"btn_{position}",
                on_click=make_move,
                args=(position,),
                use_container_width=True
            ):
                pass

st.markdown('</div>', unsafe_allow_html=True)  # Close game-container

# Control buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 New Game", use_container_width=True, type="primary", key="new_game_btn"):
        reset_game()
with col2:
    if st.button("📊 Reset Scores", use_container_width=True, key="reset_scores_btn"):
        reset_scores()

# Instructions
st.markdown("""
    <div class="instructions">
        <h3 style='color: white; text-align: center; margin-bottom: 15px;'>🎯 How to Play</h3>
        <p style='color: white;'>• Click on any empty cell to make your move</p>
        <p style='color: white;'>• Get three in a row (horizontally, vertically, or diagonally) to win</p>
        <p style='color: white;'>• The winning line will be highlighted in green</p>
        <p style='color: white;'>• Choose between two-player mode or play against the computer</p>
    </div>
""", unsafe_allow_html=True)