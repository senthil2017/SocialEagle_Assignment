import streamlit as st
import time

# Configure page settings
st.set_page_config(
    page_title="🤖 AI Knowledge Quiz",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better visuals
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .question-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .score-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .progress-text {
        font-size: 1.2rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        margin: 1rem 0;
    }
    
    .quiz-complete {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
    }
    
    .stRadio > div {
        background-color: #f8f9ff;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e6e9ff;
        margin: 0.5rem 0;
    }
    
    .stRadio > div:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Quiz questions data - AI-related questions for 12th grade
quiz_questions = [
    {
        "question": "What does 'AI' stand for?",
        "options": ["Automated Intelligence", "Artificial Intelligence", "Advanced Integration", "Algorithmic Implementation"],
        "correct": 1,
        "explanation": "AI stands for Artificial Intelligence - the simulation of human intelligence in machines."
    },
    {
        "question": "Which of the following is considered the father of Artificial Intelligence?",
        "options": ["Alan Turing", "John McCarthy", "Marvin Minsky", "Claude Shannon"],
        "correct": 1,
        "explanation": "John McCarthy coined the term 'Artificial Intelligence' and is considered the father of AI."
    },
    {
        "question": "What is Machine Learning?",
        "options": ["A type of computer hardware", "A subset of AI that learns from data", "A programming language", "A database system"],
        "correct": 1,
        "explanation": "Machine Learning is a subset of AI that enables computers to learn and improve from data without explicit programming."
    },
    {
        "question": "Which algorithm is commonly used for decision-making in AI?",
        "options": ["Bubble Sort", "Decision Tree", "Linear Search", "Binary Search"],
        "correct": 1,
        "explanation": "Decision Trees are widely used in AI for classification and decision-making tasks."
    },
    {
        "question": "What is the Turing Test designed to evaluate?",
        "options": ["Computer processing speed", "Machine's ability to exhibit intelligent behavior", "Network connectivity", "Data storage capacity"],
        "correct": 1,
        "explanation": "The Turing Test evaluates a machine's ability to exhibit intelligent behavior equivalent to human intelligence."
    },
    {
        "question": "Which of these is NOT a type of machine learning?",
        "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Distributed Learning"],
        "correct": 3,
        "explanation": "The three main types of machine learning are Supervised, Unsupervised, and Reinforcement Learning."
    },
    {
        "question": "What does 'NLP' stand for in AI?",
        "options": ["Network Layer Protocol", "Natural Language Processing", "Numerical Linear Programming", "Neural Learning Pattern"],
        "correct": 1,
        "explanation": "NLP stands for Natural Language Processing - AI's ability to understand and process human language."
    },
    {
        "question": "Which company developed the AI system 'Watson'?",
        "options": ["Google", "Microsoft", "IBM", "Amazon"],
        "correct": 2,
        "explanation": "IBM developed Watson, famous for winning on the game show Jeopardy!"
    },
    {
        "question": "What is a Neural Network inspired by?",
        "options": ["Computer circuits", "The human brain", "Internet protocols", "Database structures"],
        "correct": 1,
        "explanation": "Neural Networks are inspired by the structure and function of the human brain's neural networks."
    },
    {
        "question": "Which field combines AI with robotics?",
        "options": ["Cybernetics", "Mechatronics", "Robotics AI", "All of the above"],
        "correct": 3,
        "explanation": "All these fields contribute to combining AI with robotics, creating intelligent robotic systems."
    }
]

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False

def reset_quiz():
    """Reset all quiz variables"""
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_completed = False
    st.session_state.quiz_started = False
    st.session_state.user_answers = []
    st.session_state.show_explanation = False

def get_performance_message(score, total):
    """Get performance message based on score"""
    percentage = (score / total) * 100
    if percentage >= 90:
        return "🌟 Outstanding! You're an AI expert!", "#4CAF50"
    elif percentage >= 80:
        return "🎉 Excellent work! Great understanding of AI!", "#8BC34A"
    elif percentage >= 70:
        return "👏 Good job! You have solid AI knowledge!", "#FFC107"
    elif percentage >= 60:
        return "👍 Not bad! Keep learning about AI!", "#FF9800"
    else:
        return "📚 Keep studying! AI is fascinating to explore!", "#F44336"

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🤖 AI Knowledge Quiz 🧠</div>', unsafe_allow_html=True)
    
    # Welcome message and instructions
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    
    if not st.session_state.quiz_started and not st.session_state.quiz_completed:
        st.markdown("### Welcome to the AI Knowledge Quiz! 🚀")
        st.markdown("**Test your understanding of Artificial Intelligence concepts perfect for beginners.**")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("📋 **Instructions:**\n- Answer 10 multiple-choice questions\n- Click 'Next Question' to proceed\n- Your score will be calculated automatically\n- Good luck! 🍀")
        
        if st.button("🎯 Start Quiz", type="primary", use_container_width=True):
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.rerun()
    
    # Quiz in progress
    elif st.session_state.quiz_started and not st.session_state.quiz_completed:
        current_q = st.session_state.current_question
        question_data = quiz_questions[current_q]
        
        # Progress bar and question counter
        progress = (current_q + 1) / len(quiz_questions)
        st.progress(progress)
        st.markdown(f'<div class="progress-text">Question {current_q + 1} of {len(quiz_questions)}</div>', 
                   unsafe_allow_html=True)
        
        # Question card
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f"### ❓ {question_data['question']}")
        
        # Radio button options
        user_answer = st.radio(
            "Choose your answer:",
            options=range(len(question_data['options'])),
            format_func=lambda x: f"{chr(65+x)}. {question_data['options'][x]}",
            key=f"question_{current_q}"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Next Question", type="primary", use_container_width=True):
                # Check if answer is correct
                if user_answer == question_data['correct']:
                    st.session_state.score += 1
                
                # Store user answer
                st.session_state.user_answers.append(user_answer)
                
                # Move to next question or complete quiz
                if current_q < len(quiz_questions) - 1:
                    st.session_state.current_question += 1
                else:
                    st.session_state.quiz_completed = True
                
                st.rerun()
    
    # Quiz completed - show results
    else:
        total_questions = len(quiz_questions)
        percentage = (st.session_state.score / total_questions) * 100
        message, color = get_performance_message(st.session_state.score, total_questions)
        
        # Results display
        st.markdown('<div class="quiz-complete">', unsafe_allow_html=True)
        st.markdown("# 🎊 Quiz Complete! 🎊")
        st.markdown(f"## Your Score: {st.session_state.score}/{total_questions} ({percentage:.1f}%)")
        st.markdown(f"### {message}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Score visualization
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="score-card">', unsafe_allow_html=True)
            
            # Create a simple score meter
            correct_bar = "🟢" * st.session_state.score
            incorrect_bar = "🔴" * (total_questions - st.session_state.score)
            st.markdown(f"**Score Breakdown:** {correct_bar}{incorrect_bar}")
            st.markdown(f"✅ Correct: {st.session_state.score}")
            st.markdown(f"❌ Incorrect: {total_questions - st.session_state.score}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show detailed results
        if st.button("📊 Show Detailed Results"):
            st.session_state.show_explanation = not st.session_state.show_explanation
        
        if st.session_state.show_explanation:
            st.markdown("## 📚 Review Your Answers")
            for i, question_data in enumerate(quiz_questions):
                user_ans = st.session_state.user_answers[i]
                correct_ans = question_data['correct']
                
                with st.expander(f"Question {i+1}: {question_data['question']}", 
                               expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Your Answer:** {chr(65+user_ans)}. {question_data['options'][user_ans]}")
                        if user_ans == correct_ans:
                            st.success("✅ Correct!")
                        else:
                            st.error("❌ Incorrect")
                    
                    with col2:
                        st.markdown(f"**Correct Answer:** {chr(65+correct_ans)}. {question_data['options'][correct_ans]}")
                        st.info(f"**Explanation:** {question_data['explanation']}")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Retake Quiz", type="primary", use_container_width=True):
                reset_quiz()
                st.rerun()
        
        with col2:
            if st.button("📱 Share Results", use_container_width=True):
                st.balloons()
                st.success(f"🎉 I scored {st.session_state.score}/{total_questions} ({percentage:.1f}%) on the AI Knowledge Quiz!")

    # Sidebar with additional info
    with st.sidebar:
        st.markdown("### 🤖 About This Quiz")
        st.markdown("This quiz tests your knowledge of Artificial Intelligence concepts suitable for beginners.")
        
        st.markdown("### 📖 Topics Covered")
        st.markdown("""
        - AI Fundamentals
        - Machine Learning Basics
        - Key AI Personalities
        - AI Applications
        - Technical Concepts
        """)
        
        if st.session_state.quiz_completed:
            st.markdown("### 🎯 Your Performance")
            if st.session_state.score >= len(quiz_questions) * 0.8:
                st.success("Excellent Understanding! 🌟")
            elif st.session_state.score >= len(quiz_questions) * 0.6:
                st.warning("Good Progress! 📚")
            else:
                st.info("Keep Learning! 🚀")

if __name__ == "__main__":
    main()