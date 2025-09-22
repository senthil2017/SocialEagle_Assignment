import streamlit as st
import random
import time
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="✊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(-10px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .shake {
        animation: shake 0.5s ease-in-out;
    }
    
    .bounce {
        animation: bounce 0.6s ease-in-out;
    }
    
    .pulse {
        animation: pulse 0.5s ease-in-out;
    }
    
    .choice-button {
        transition: all 0.3s ease;
        border: 3px solid transparent;
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    
    .choice-button:hover {
        transform: scale(1.05);
        border-color: #ffd700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }
    
    .result-win {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
    
    .result-lose {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
    
    .result-draw {
        background: linear-gradient(135deg, #8e9eab 0%, #eef2f3 100%);
        padding: 20px;
        border-radius: 15px;
        color: #333;
        text-align: center;
        margin: 20px 0;
    }
    
    .emoji-large {
        font-size: 80px;
        margin: 10px;
    }
    
    .score-board {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

class RockPaperScissorsGame:
    def __init__(self):
        self.choices = {
            "rock": {"emoji": "✊", "beats": "scissors"},
            "paper": {"emoji": "✋", "beats": "rock"},
            "scissors": {"emoji": "✌️", "beats": "paper"}
        }
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'user_score' not in st.session_state:
            st.session_state.user_score = 0
        if 'computer_score' not in st.session_state:
            st.session_state.computer_score = 0
        if 'draws' not in st.session_state:
            st.session_state.draws = 0
        if 'last_result' not in st.session_state:
            st.session_state.last_result = None
        if 'animation_key' not in st.session_state:
            st.session_state.animation_key = 0
        if 'game_history' not in st.session_state:
            st.session_state.game_history = []
    
    def get_computer_choice(self):
        """Get random computer choice"""
        return random.choice(list(self.choices.keys()))
    
    def determine_winner(self, user_choice, computer_choice):
        """Determine the winner of the game"""
        if user_choice == computer_choice:
            return "draw"
        elif self.choices[user_choice]["beats"] == computer_choice:
            return "user"
        else:
            return "computer"
    
    def update_scores(self, result):
        """Update scores based on game result"""
        if result == "user":
            st.session_state.user_score += 1
        elif result == "computer":
            st.session_state.computer_score += 1
        else:
            st.session_state.draws += 1
    
    def play_round(self, user_choice):
        """Play one round of the game"""
        # Trigger animation
        st.session_state.animation_key += 1
        
        # Show thinking animation
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("<div class='pulse'><h3>🤔 Computer is thinking...</h3></div>", unsafe_allow_html=True)
        
        # Simulate computer thinking time
        time.sleep(1.5)
        thinking_placeholder.empty()
        
        # Get computer choice and determine winner
        computer_choice = self.get_computer_choice()
        result = self.determine_winner(user_choice, computer_choice)
        
        # Update scores and history
        self.update_scores(result)
        st.session_state.last_result = {
            "user_choice": user_choice,
            "computer_choice": computer_choice,
            "result": result
        }
        st.session_state.game_history.append(st.session_state.last_result)
        
        return computer_choice, result
    
    def display_result(self, user_choice, computer_choice, result):
        """Display the game result with animations"""
        user_emoji = self.choices[user_choice]["emoji"]
        computer_emoji = self.choices[computer_choice]["emoji"]
        
        # Create columns for VS display
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown(f"<div class='bounce'><h2>You</h2><div class='emoji-large'>{user_emoji}</div><p>{user_choice.title()}</p></div>", 
                       unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h2>VS</h2>", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"<div class='bounce'><h2>Computer</h2><div class='emoji-large'>{computer_emoji}</div><p>{computer_choice.title()}</p></div>", 
                       unsafe_allow_html=True)
        
        # Display result with appropriate styling
        if result == "user":
            st.markdown(f"""
                <div class='result-win'>
                    <h2>🎉 You Win! 🎉</h2>
                    <p>{user_choice.title()} beats {computer_choice.title()}</p>
                </div>
            """, unsafe_allow_html=True)
        elif result == "computer":
            st.markdown(f"""
                <div class='result-lose'>
                    <h2>💻 Computer Wins! 🤖</h2>
                    <p>{computer_choice.title()} beats {user_choice.title()}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='result-draw'>
                    <h2>🤝 It's a Draw! 🤝</h2>
                    <p>Both chose {user_choice.title()}</p>
                </div>
            """, unsafe_allow_html=True)
    
    def display_scoreboard(self):
        """Display the current scoreboard"""
        st.markdown(f"""
            <div class='score-board'>
                <h3>📊 Score Board</h3>
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <h4>👤 You</h4>
                        <h2>{st.session_state.user_score}</h2>
                    </div>
                    <div>
                        <h4>🤝 Draws</h4>
                        <h2>{st.session_state.draws}</h2>
                    </div>
                    <div>
                        <h4>🤖 Computer</h4>
                        <h2>{st.session_state.computer_score}</h2>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    def reset_game(self):
        """Reset the game scores and history"""
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.session_state.draws = 0
        st.session_state.game_history = []
        st.session_state.last_result = None
        st.session_state.animation_key += 1

def main():
    # Initialize game
    game = RockPaperScissorsGame()
    
    # Header
    st.markdown("<h1 style='text-align: center; color: #ff6b6b;'>🎮 Rock Paper Scissors 🎮</h1>", 
                unsafe_allow_html=True)
    
    # Display scoreboard
    game.display_scoreboard()
    
    # Game instructions
    with st.expander("ℹ️ How to Play"):
        st.markdown("""
        **Rules:**
        - ✊ Rock crushes ✌️ Scissors
        - ✋ Paper covers ✊ Rock  
        - ✌️ Scissors cut ✋ Paper
        
        **Instructions:**
        1. Choose your move by clicking one of the buttons below
        2. The computer will randomly select its move
        3. See who wins and watch the scores update!
        4. Play as many rounds as you want!
        """)
    
    # Choice buttons
    st.markdown("<h3>Choose your move:</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✊ Rock", key="rock_btn", use_container_width=True):
            computer_choice, result = game.play_round("rock")
            game.display_result("rock", computer_choice, result)
    
    with col2:
        if st.button("✋ Paper", key="paper_btn", use_container_width=True):
            computer_choice, result = game.play_round("paper")
            game.display_result("paper", computer_choice, result)
    
    with col3:
        if st.button("✌️ Scissors", key="scissors_btn", use_container_width=True):
            computer_choice, result = game.play_round("scissors")
            game.display_result("scissors", computer_choice, result)
    
    # Display last result if available
    if st.session_state.last_result:
        st.markdown("---")
        st.markdown("<h3>Last Game Result:</h3>", unsafe_allow_html=True)
        last = st.session_state.last_result
        game.display_result(last["user_choice"], last["computer_choice"], last["result"])
    
    # Game history
    if st.session_state.game_history:
        with st.expander("📜 Game History"):
            for i, game_data in enumerate(st.session_state.game_history[-10:][::-1], 1):
                user_emoji = game.choices[game_data["user_choice"]]["emoji"]
                computer_emoji = game.choices[game_data["computer_choice"]]["emoji"]
                
                if game_data["result"] == "user":
                    result_text = "✅ You Won"
                elif game_data["result"] == "computer":
                    result_text = "❌ Computer Won"
                else:
                    result_text = "🤝 Draw"
                
                st.write(f"Game {len(st.session_state.game_history) - i + 1}: {user_emoji} vs {computer_emoji} - {result_text}")
    
    # Reset button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Reset Game", use_container_width=True):
            game.reset_game()
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666;'>Made with ❤️ using Streamlit</div>", 
                unsafe_allow_html=True)

if __name__ == "__main__":
    main()