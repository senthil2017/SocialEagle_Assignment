import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List
import time

# Page configuration
st.set_page_config(
    page_title="💪 Gym Workout Logger",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced visual effects
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 5px rgba(255, 107, 107, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(69, 183, 209, 0.8)); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    .exercise-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        font-weight: 500;
    }
    
    .success-animation {
        animation: bounce 0.6s ease-in-out;
    }
    
    @keyframes bounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        80% { transform: translateY(-5px); }
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2C3E50 0%, #3498DB 100%);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = []

if 'current_workout' not in st.session_state:
    st.session_state.current_workout = []

# Main header with animation
st.markdown('<h1 class="main-header">💪 Gym Workout Logger 🏋️‍♂️</h1>', unsafe_allow_html=True)

# Sidebar for workout input
with st.sidebar:
    st.markdown("## 🔥 Log Your Workout")
    
    # Exercise selection with popular options
    exercise_options = [
        "Bench Press", "Squat", "Deadlift", "Overhead Press", "Barbell Row",
        "Pull-ups", "Push-ups", "Dips", "Bicep Curls", "Tricep Extensions",
        "Leg Press", "Lat Pulldown", "Chest Fly", "Shoulder Raise", "Lunges",
        "Custom Exercise"
    ]
    
    selected_exercise = st.selectbox("🏃 Select Exercise", exercise_options)
    
    if selected_exercise == "Custom Exercise":
        exercise_name = st.text_input("Enter custom exercise name")
    else:
        exercise_name = selected_exercise
    
    # Input fields with enhanced styling
    col1, col2 = st.columns(2)
    with col1:
        sets = st.number_input("Sets", min_value=1, max_value=20, value=3, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, value=20.0, step=2.5)
    
    with col2:
        reps = st.number_input("Reps", min_value=1, max_value=50, value=10, step=1)
        rest_time = st.number_input("Rest (sec)", min_value=30, max_value=600, value=90, step=15)
    
    # Add exercise to current workout
    if st.button("➕ Add Exercise", key="add_exercise"):
        if exercise_name:
            exercise_data = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'exercise': exercise_name,
                'sets': sets,
                'reps': reps,
                'weight': weight,
                'rest_time': rest_time,
                'total_volume': sets * reps * weight
            }
            st.session_state.current_workout.append(exercise_data)
            st.success(f"✅ {exercise_name} added to workout!")
            time.sleep(0.5)
            st.rerun()
    
    st.markdown("---")
    
    # Current workout display
    if st.session_state.current_workout:
        st.markdown("### 🔄 Current Workout Session")
        for i, exercise in enumerate(st.session_state.current_workout):
            with st.container():
                st.markdown(f"""
                <div class="exercise-card">
                    <strong>{exercise['exercise']}</strong><br>
                    {exercise['sets']} sets × {exercise['reps']} reps @ {exercise['weight']}kg
                </div>
                """, unsafe_allow_html=True)
        
        # Save workout button
        if st.button("💾 Save Workout", key="save_workout"):
            st.session_state.workout_data.extend(st.session_state.current_workout)
            workout_count = len(st.session_state.current_workout)
            st.session_state.current_workout = []
            st.success(f"🎉 Workout saved! {workout_count} exercises logged.")
            st.balloons()
            time.sleep(1)
            st.rerun()
        
        if st.button("🗑️ Clear Current Workout", key="clear_current"):
            st.session_state.current_workout = []
            st.info("Current workout cleared!")
            st.rerun()

# Main content area
if st.session_state.workout_data:
    df = pd.DataFrame(st.session_state.workout_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Dashboard metrics
    st.markdown("## 📊 Workout Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_workouts = len(df['date'].unique())
        st.markdown(f"""
        <div class="metric-card">
            <h3>🗓️ Total Workouts</h3>
            <h2>{total_workouts}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_exercises = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <h3>💪 Total Exercises</h3>
            <h2>{total_exercises}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_volume = df['total_volume'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚖️ Total Volume</h3>
            <h2>{total_volume:,.0f} kg</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_weight = df['weight'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Avg Weight</h3>
            <h2>{avg_weight:.1f} kg</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Progress Charts", "📋 Workout History", "🎯 Exercise Analysis", "📊 Weekly Summary"])
    
    with tab1:
        st.markdown("### 📈 Progress Visualization")
        
        # Exercise selection for progress tracking
        exercises_list = df['exercise'].unique().tolist()
        selected_ex = st.selectbox("Select exercise to track progress:", exercises_list)
        
        if selected_ex:
            exercise_data = df[df['exercise'] == selected_ex].copy()
            exercise_data = exercise_data.sort_values('date')
            
            # Create progress charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Weight progression
                fig_weight = px.line(
                    exercise_data, 
                    x='date', 
                    y='weight',
                    title=f'Weight Progress - {selected_ex}',
                    markers=True,
                    color_discrete_sequence=['#FF6B6B']
                )
                fig_weight.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    title_font_size=16,
                    showlegend=False
                )
                fig_weight.update_traces(line=dict(width=3), marker=dict(size=8))
                st.plotly_chart(fig_weight, use_container_width=True)
            
            with col2:
                # Volume progression
                fig_volume = px.bar(
                    exercise_data, 
                    x='date', 
                    y='total_volume',
                    title=f'Volume Progress - {selected_ex}',
                    color='total_volume',
                    color_continuous_scale='plasma'
                )
                fig_volume.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    title_font_size=16,
                    showlegend=False
                )
                st.plotly_chart(fig_volume, use_container_width=True)
    
    with tab2:
        st.markdown("### 📋 Complete Workout History")
        
        # Date filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=df['date'].min().date())
        with col2:
            end_date = st.date_input("End Date", value=df['date'].max().date())
        
        # Filter data
        mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
        filtered_df = df.loc[mask]
        
        # Display table with enhanced styling
        if not filtered_df.empty:
            display_df = filtered_df[['datetime', 'exercise', 'sets', 'reps', 'weight', 'total_volume']].copy()
            display_df.columns = ['Date & Time', 'Exercise', 'Sets', 'Reps', 'Weight (kg)', 'Volume (kg)']
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Volume (kg)": st.column_config.NumberColumn(format="%.0f"),
                    "Weight (kg)": st.column_config.NumberColumn(format="%.1f")
                }
            )
        else:
            st.info("No workouts found in the selected date range.")
    
    with tab3:
        st.markdown("### 🎯 Exercise Analysis")
        
        # Most popular exercises
        exercise_counts = df['exercise'].value_counts().head(10)
        
        fig_popular = px.bar(
            x=exercise_counts.values,
            y=exercise_counts.index,
            orientation='h',
            title='Most Performed Exercises',
            color=exercise_counts.values,
            color_continuous_scale='viridis'
        )
        fig_popular.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=18,
            yaxis_title="Exercise",
            xaxis_title="Times Performed"
        )
        st.plotly_chart(fig_popular, use_container_width=True)
        
        # Exercise volume comparison
        volume_by_exercise = df.groupby('exercise')['total_volume'].sum().sort_values(ascending=False).head(10)
        
        fig_volume_comparison = px.pie(
            values=volume_by_exercise.values,
            names=volume_by_exercise.index,
            title='Volume Distribution by Exercise',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_volume_comparison.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=18
        )
        st.plotly_chart(fig_volume_comparison, use_container_width=True)
    
    with tab4:
        st.markdown("### 📊 Weekly Summary")
        
        # Calculate weekly data
        df['week'] = df['date'].dt.isocalendar().week
        df['year'] = df['date'].dt.year
        df['week_year'] = df['year'].astype(str) + '-W' + df['week'].astype(str).str.zfill(2)
        
        weekly_stats = df.groupby('week_year').agg({
            'exercise': 'count',
            'total_volume': 'sum',
            'weight': 'mean'
        }).round(1)
        
        weekly_stats.columns = ['Total Exercises', 'Total Volume (kg)', 'Avg Weight (kg)']
        weekly_stats = weekly_stats.tail(8)  # Last 8 weeks
        
        # Weekly volume chart
        fig_weekly = px.bar(
            x=weekly_stats.index,
            y=weekly_stats['Total Volume (kg)'],
            title='Weekly Volume Progression',
            color=weekly_stats['Total Volume (kg)'],
            color_continuous_scale='rainbow'
        )
        fig_weekly.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=18,
            xaxis_title="Week",
            yaxis_title="Volume (kg)"
        )
        st.plotly_chart(fig_weekly, use_container_width=True)
        
        # Weekly summary table
        st.markdown("#### Weekly Statistics")
        st.dataframe(weekly_stats, use_container_width=True)

else:
    # Welcome screen when no data exists
    st.markdown("## 🚀 Welcome to Your Fitness Journey!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white; margin: 2rem 0;">
            <h2>🎯 Start Your First Workout</h2>
            <p style="font-size: 1.2rem; margin: 1rem 0;">
                Use the sidebar to log your exercises and track your progress!
            </p>
            <div style="margin: 2rem 0;">
                <p>✅ Log sets, reps, and weights</p>
                <p>📊 View progress charts</p>
                <p>📈 Track weekly improvements</p>
                <p>🏆 Achieve your fitness goals</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "💪 Keep pushing your limits! Every rep counts towards your goals. 🏆"
    "</div>",
    unsafe_allow_html=True
)

# Data export functionality
if st.session_state.workout_data:
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📤 Export Data")
        if st.button("💾 Download Workout Data"):
            df = pd.DataFrame(st.session_state.workout_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"workout_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )