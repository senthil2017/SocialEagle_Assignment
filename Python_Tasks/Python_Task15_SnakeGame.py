import streamlit as st
import random
import time
import numpy as np
from typing import List, Tuple

# Page configuration
st.set_page_config(
    page_title="🐍 Snake Game",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .game-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .game-board {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 2rem auto;
    }
    
    .rules-container {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #ff7675;
    }
    
    .game-over {
        background: linear-gradient(135deg, #ff7675, #d63031);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(255, 118, 117, 0.37);
    }
    
    .victory {
        background: linear-gradient(135deg, #00b894, #00a085);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(0, 184, 148, 0.37);
    }
    
    .control-buttons {
        text-align: center;
        margin: 1rem 0;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
        margin: 0.2rem;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4);
    }
</style>
""", unsafe_allow_html=True)

class SnakeGame:
    def __init__(self, width: int = 20, height: int = 15):
        self.width = width
        self.height = height
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake = [(self.height // 2, self.width // 2)]
        self.direction = (0, 1)  # Initially moving right
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.game_won = False
    
    def generate_food(self) -> Tuple[int, int]:
        """Generate food at random position not occupied by snake"""
        while True:
            food_pos = (random.randint(0, self.height - 1), 
                       random.randint(0, self.width - 1))
            if food_pos not in self.snake:
                return food_pos
    
    def change_direction(self, new_direction: Tuple[int, int]):
        """Change snake direction (prevent reverse direction)"""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def move(self):
        """Move snake one step"""
        if self.game_over or self.game_won:
            return
        
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.height or 
            new_head[1] < 0 or new_head[1] >= self.width):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            
            # Check win condition (snake fills most of the board)
            if len(self.snake) >= (self.width * self.height) * 0.8:
                self.game_won = True
        else:
            self.snake.pop()  # Remove tail if no food eaten
    
    def get_board(self) -> np.ndarray:
        """Generate board representation"""
        board = np.zeros((self.height, self.width), dtype=int)
        
        # Place food
        board[self.food[0], self.food[1]] = 2
        
        # Place snake
        for i, (row, col) in enumerate(self.snake):
            if i == 0:  # Head
                board[row, col] = 3
            else:  # Body
                board[row, col] = 1
        
        return board

def render_board(board: np.ndarray) -> str:
    """Render board as HTML"""
    cell_size = "25px"
    board_html = f'<div style="display: grid; grid-template-columns: repeat({board.shape[1]}, {cell_size}); gap: 2px; justify-content: center; background: #2d3436; padding: 10px; border-radius: 10px;">'
    
    colors = {
        0: "#ddd",      # Empty
        1: "#00b894",   # Snake body
        2: "#e17055",   # Food
        3: "#0984e3"    # Snake head
    }
    
    for row in board:
        for cell in row:
            color = colors[cell]
            board_html += f'<div style="width: {cell_size}; height: {cell_size}; background-color: {color}; border-radius: 3px;"></div>'
    
    board_html += '</div>'
    return board_html

def main():
    st.markdown('<h1 class="main-header">🐍 Snake Game</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'game' not in st.session_state:
        st.session_state.game = SnakeGame()
    if 'auto_play' not in st.session_state:
        st.session_state.auto_play = False
    if 'game_speed' not in st.session_state:
        st.session_state.game_speed = 0.3
    
    # Sidebar for game rules and settings
    with st.sidebar:
        st.markdown("## 🎮 Game Rules")
        st.markdown("""
        <div class="rules-container">
        <h4>📝 How to Play:</h4>
        <ul>
            <li>🎯 Control the snake to eat food (red squares)</li>
            <li>🔄 Snake grows longer each time it eats</li>
            <li>⚠️ Avoid hitting walls or your own body</li>
            <li>🏆 Score increases by 10 points per food</li>
            <li>🎉 Win by filling 80% of the board!</li>
        </ul>
        
        <h4>🕹️ Controls:</h4>
        <ul>
            <li>⬆️ Up Arrow - Move Up</li>
            <li>⬇️ Down Arrow - Move Down</li>
            <li>⬅️ Left Arrow - Move Left</li>
            <li>➡️ Right Arrow - Move Right</li>
        </ul>
        
        <h4>🎨 Legend:</h4>
        <ul>
            <li>🟦 Blue - Snake Head</li>
            <li>🟢 Green - Snake Body</li>
            <li>🟠 Orange - Food</li>
            <li>⬜ Gray - Empty Space</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("## ⚙️ Game Settings")
        
        # Game speed control
        speed_options = {
            "Slow 🐌": 0.5,
            "Normal 🚶": 0.3,
            "Fast 🏃": 0.15,
            "Lightning ⚡": 0.1
        }
        
        selected_speed = st.selectbox(
            "Game Speed:",
            options=list(speed_options.keys()),
            index=1
        )
        st.session_state.game_speed = speed_options[selected_speed]
        
        # Board size
        board_size = st.selectbox(
            "Board Size:",
            options=["Small (15x10)", "Medium (20x15)", "Large (25x20)"],
            index=1
        )
        
        if board_size == "Small (15x10)" and (st.session_state.game.width != 15 or st.session_state.game.height != 10):
            st.session_state.game = SnakeGame(15, 10)
        elif board_size == "Medium (20x15)" and (st.session_state.game.width != 20 or st.session_state.game.height != 15):
            st.session_state.game = SnakeGame(20, 15)
        elif board_size == "Large (25x20)" and (st.session_state.game.width != 25 or st.session_state.game.height != 20):
            st.session_state.game = SnakeGame(25, 20)
    
    # Main game area
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        game = st.session_state.game
        
        # Game statistics
        st.markdown(f"""
        <div class="game-stats">
            <h2>📊 Game Statistics</h2>
            <p><strong>Score:</strong> {game.score} | <strong>Length:</strong> {len(game.snake)} | <strong>Food Position:</strong> {game.food}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Control buttons
        st.markdown('<div class="control-buttons">', unsafe_allow_html=True)
        
        button_col1, button_col2, button_col3, button_col4, button_col5 = st.columns([1, 1, 1, 1, 1])
        
        with button_col1:
            if st.button("⬆️ Up", key="up"):
                game.change_direction((-1, 0))
        
        with button_col2:
            if st.button("⬇️ Down", key="down"):
                game.change_direction((1, 0))
        
        with button_col3:
            if st.button("⬅️ Left", key="left"):
                game.change_direction((0, -1))
        
        with button_col4:
            if st.button("➡️ Right", key="right"):
                game.change_direction((0, 1))
        
        with button_col5:
            if st.button("🔄 Restart", key="restart"):
                st.session_state.game.reset_game()
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-play toggle
        auto_play_col1, auto_play_col2 = st.columns([1, 1])
        with auto_play_col1:
            if st.button("▶️ Start Auto-Play" if not st.session_state.auto_play else "⏸️ Pause"):
                st.session_state.auto_play = not st.session_state.auto_play
                st.rerun()
        
        # Game board
        #st.markdown('<div class="game-board">', unsafe_allow_html=True)
        
        if game.game_over:
            st.markdown(f"""
            <div class="game-over">
                <h2>💀 Game Over!</h2>
                <p>Final Score: <strong>{game.score}</strong></p>
                <p>Snake Length: <strong>{len(game.snake)}</strong></p>
                <p>Click 'Restart' to play again!</p>
            </div>
            """, unsafe_allow_html=True)
        elif game.game_won:
            st.markdown(f"""
            <div class="victory">
                <h2>🎉 Congratulations! You Won!</h2>
                <p>Final Score: <strong>{game.score}</strong></p>
                <p>Snake Length: <strong>{len(game.snake)}</strong></p>
                <p>You're a Snake Master! 🐍👑</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Render game board
        board = game.get_board()
        board_html = render_board(board)
        st.markdown(board_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Game status
        if not game.game_over and not game.game_won:
            status_text = "🎮 Game in Progress"
            if st.session_state.auto_play:
                status_text += " (Auto-Playing)"
            st.success(status_text)
        
        # Auto-play logic
        if st.session_state.auto_play and not game.game_over and not game.game_won:
            time.sleep(st.session_state.game_speed)
            game.move()
            st.rerun()
        
        # Keyboard controls info
        st.info("💡 **Pro Tip:** Use the direction buttons above or enable auto-play to watch the snake move automatically!")
        
        # High score tracking (simple implementation)
        if 'high_score' not in st.session_state:
            st.session_state.high_score = 0
        
        if game.score > st.session_state.high_score:
            st.session_state.high_score = game.score
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 1rem; padding: 1rem; background: linear-gradient(45deg, #fd79a8, #fdcb6e); border-radius: 10px;">
            <h3>🏆 High Score: {st.session_state.high_score}</h3>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()