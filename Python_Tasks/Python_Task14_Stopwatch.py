import streamlit as st
import time
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="Stopwatch App",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86C1;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .timer-display {
        text-align: center;
        font-size: 4rem;
        font-weight: bold;
        color: #1B4F72;
        background: linear-gradient(135deg, #EBF5FB, #D6EAF8);
        padding: 40px;
        border-radius: 20px;
        border: 3px solid #AED6F1;
        margin: 30px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        font-family: 'Courier New', monospace;
    }
    
    .status-indicator {
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 20px 0;
        padding: 10px;
        border-radius: 10px;
    }
    
    .status-running {
        color: #27AE60;
        background-color: #D5F4E6;
        border: 2px solid #27AE60;
    }
    
    .status-stopped {
        color: #E74C3C;
        background-color: #FADBD8;
        border: 2px solid #E74C3C;
    }
    
    .status-ready {
        color: #F39C12;
        background-color: #FCF3CF;
        border: 2px solid #F39C12;
    }
    
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px 0;
    }
    
    .stButton button {
        font-size: 1.1rem;
        font-weight: bold;
        padding: 12px 30px;
        border-radius: 25px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .start-btn {
        background: linear-gradient(135deg, #27AE60, #2ECC71) !important;
        color: white !important;
    }
    
    .stop-btn {
        background: linear-gradient(135deg, #E74C3C, #EC7063) !important;
        color: white !important;
    }
    
    .reset-btn {
        background: linear-gradient(135deg, #F39C12, #F7DC6F) !important;
        color: white !important;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #F8F9FA, #E9ECEF);
        padding: 20px;
        border-radius: 15px;
        margin-top: 30px;
        border: 2px solid #DEE2E6;
    }
    
    .stat-item {
        text-align: center;
        margin: 10px 0;
    }
    
    .stat-label {
        font-weight: bold;
        color: #6C757D;
        font-size: 0.9rem;
    }
    
    .stat-value {
        font-size: 1.2rem;
        color: #495057;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'lap_times' not in st.session_state:
    st.session_state.lap_times = []
if 'total_sessions' not in st.session_state:
    st.session_state.total_sessions = 0

def format_time(seconds):
    """Format seconds into HH:MM:SS.ms format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 100)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:02d}"

def get_current_time():
    """Get current elapsed time"""
    if st.session_state.is_running and st.session_state.start_time:
        return st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
    return st.session_state.elapsed_time

def start_stopwatch():
    """Start the stopwatch"""
    st.session_state.start_time = time.time()
    st.session_state.is_running = True

def stop_stopwatch():
    """Stop the stopwatch"""
    if st.session_state.is_running:
        st.session_state.elapsed_time = get_current_time()
        st.session_state.is_running = False
        st.session_state.start_time = None

def reset_stopwatch():
    """Reset the stopwatch"""
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.is_running = False
    st.session_state.lap_times = []
    if st.session_state.elapsed_time > 0:
        st.session_state.total_sessions += 1

def add_lap():
    """Add a lap time"""
    if st.session_state.is_running:
        lap_time = get_current_time()
        st.session_state.lap_times.append(lap_time)

# Main app header
st.markdown('<h1 class="main-header">⏱️ Stopwatch Pro</h1>', unsafe_allow_html=True)

# Get current time for display
current_time = get_current_time()

# Display timer
st.markdown(f'<div class="timer-display">{format_time(current_time)}</div>', 
           unsafe_allow_html=True)

# Status indicator
if st.session_state.is_running:
    status_class = "status-running"
    status_text = "🟢 RUNNING"
elif st.session_state.elapsed_time > 0:
    status_class = "status-stopped"
    status_text = "🔴 STOPPED"
else:
    status_class = "status-ready"
    status_text = "🟡 READY"

st.markdown(f'<div class="status-indicator {status_class}">{status_text}</div>', 
           unsafe_allow_html=True)

# Control buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("▶️ START", key="start", help="Start the stopwatch"):
        if not st.session_state.is_running:
            start_stopwatch()
            st.rerun()

with col2:
    if st.button("⏸️ STOP", key="stop", help="Stop the stopwatch"):
        if st.session_state.is_running:
            stop_stopwatch()
            st.rerun()

with col3:
    if st.button("🔄 RESET", key="reset", help="Reset the stopwatch"):
        reset_stopwatch()
        st.rerun()

with col4:
    if st.button("📍 LAP", key="lap", help="Record lap time"):
        if st.session_state.is_running:
            add_lap()
            st.rerun()

# Statistics section
if st.session_state.elapsed_time > 0 or st.session_state.lap_times:
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Session Stats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="stat-item">', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Current Time</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{format_time(current_time)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-item">', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Lap Count</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{len(st.session_state.lap_times)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        avg_lap = sum(st.session_state.lap_times) / len(st.session_state.lap_times) if st.session_state.lap_times else 0
        st.markdown('<div class="stat-item">', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Avg Lap</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{format_time(avg_lap)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Lap times display
if st.session_state.lap_times:
    st.markdown("### 🏃‍♂️ Lap Times")
    lap_data = []
    for i, lap_time in enumerate(st.session_state.lap_times, 1):
        split_time = lap_time - (st.session_state.lap_times[i-2] if i > 1 else 0)
        lap_data.append({
            "Lap": f"#{i}",
            "Split Time": format_time(split_time),
            "Total Time": format_time(lap_time)
        })
    
    # Display in a nice table format
    for lap in reversed(lap_data[-5:]):  # Show last 5 laps
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{lap['Lap']}**")
        with col2:
            st.write(lap['Split Time'])
        with col3:
            st.write(lap['Total Time'])

# Auto-refresh when running
if st.session_state.is_running:
    time.sleep(0.01)  # Small delay to prevent excessive CPU usage
    st.rerun()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | 📱 Responsive Design | ⚡ Real-time Updates")