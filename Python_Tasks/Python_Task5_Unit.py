import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="🔄 Universal Unit Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .converter-card {
        background: linear-gradient(145deg, #f0f0f0, #ffffff);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid;
    }
    
    .currency-card { border-left-color: #28a745; }
    .temperature-card { border-left-color: #dc3545; }
    .length-card { border-left-color: #007bff; }
    .weight-card { border-left-color: #ffc107; }
    
    .result-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🔄 Universal Unit Converter</h1>
    <p>Your one-stop solution for all conversion needs!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for converter selection
st.sidebar.title("🎛️ Converter Selection")
converter_type = st.sidebar.selectbox(
    "Choose a converter:",
    ["💱 Currency", "🌡️ Temperature", "📏 Length", "⚖️ Weight"],
    index=0
)

# Currency Converter
def currency_converter():
    st.markdown('<div class="converter-card currency-card">', unsafe_allow_html=True)
    st.markdown("### 💱 Currency Converter")
    
    # Popular currency pairs
    currency_options = {
        "USD": "US Dollar 🇺🇸",
        "EUR": "Euro 🇪🇺", 
        "GBP": "British Pound 🇬🇧",
        "JPY": "Japanese Yen 🇯🇵",
        "AUD": "Australian Dollar 🇦🇺",
        "CAD": "Canadian Dollar 🇨🇦",
        "CHF": "Swiss Franc 🇨🇭",
        "CNY": "Chinese Yuan 🇨🇳",
        "INR": "Indian Rupee 🇮🇳",
        "KRW": "South Korean Won 🇰🇷"
    }
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        from_currency = st.selectbox("From:", list(currency_options.keys()), 
                                   format_func=lambda x: currency_options[x])
        amount = st.number_input("Amount:", min_value=0.01, value=100.0, step=0.01)
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🔄", help="Swap currencies"):
            st.session_state.swap_currency = True
    
    with col3:
        to_currency = st.selectbox("To:", list(currency_options.keys()), 
                                 index=1, format_func=lambda x: currency_options[x])
    
    # Mock exchange rates (in real app, you'd use an API like exchangerate-api.com)
    exchange_rates = {
        "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0, "AUD": 1.35, "CAD": 1.25, "CHF": 0.92, "CNY": 6.45, "INR": 74.5, "KRW": 1180.0},
        "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 129.5, "AUD": 1.59, "CAD": 1.47, "CHF": 1.08, "CNY": 7.6, "INR": 87.8, "KRW": 1391.0},
        "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150.7, "AUD": 1.85, "CAD": 1.71, "CHF": 1.26, "CNY": 8.84, "INR": 102.1, "KRW": 1617.0},
    }
    
    if from_currency != to_currency:
        # Simple conversion calculation (using mock rates)
        if from_currency in exchange_rates and to_currency in exchange_rates[from_currency]:
            rate = exchange_rates[from_currency][to_currency]
        else:
            rate = 1.0  # Default rate for unsupported pairs
        
        converted_amount = amount * rate
        
        st.markdown(f"""
        <div class="result-box">
            {amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}
        </div>
        """, unsafe_allow_html=True)
        
        # Rate visualization
        fig = go.Figure(data=go.Bar(
            x=[f"{from_currency} to {to_currency}"],
            y=[rate],
            marker_color=['#28a745'],
            text=[f"Rate: {rate:.4f}"],
            textposition='auto'
        ))
        fig.update_layout(
            title="Exchange Rate",
            showlegend=False,
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Temperature Converter
def temperature_converter():
    st.markdown('<div class="converter-card temperature-card">', unsafe_allow_html=True)
    st.markdown("### 🌡️ Temperature Converter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        temp_input = st.number_input("Enter temperature:", value=25.0, step=0.1)
        from_unit = st.selectbox("From:", ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"])
    
    with col2:
        to_unit = st.selectbox("To:", ["Fahrenheit (°F)", "Celsius (°C)", "Kelvin (K)"])
    
    # Temperature conversion functions
    def celsius_to_fahrenheit(c): return (c * 9/5) + 32
    def fahrenheit_to_celsius(f): return (f - 32) * 5/9
    def celsius_to_kelvin(c): return c + 273.15
    def kelvin_to_celsius(k): return k - 273.15
    def fahrenheit_to_kelvin(f): return celsius_to_kelvin(fahrenheit_to_celsius(f))
    def kelvin_to_fahrenheit(k): return celsius_to_fahrenheit(kelvin_to_celsius(k))
    
    # Conversion logic
    if from_unit == to_unit:
        result = temp_input
    else:
        conversions = {
            ("Celsius (°C)", "Fahrenheit (°F)"): celsius_to_fahrenheit,
            ("Celsius (°C)", "Kelvin (K)"): celsius_to_kelvin,
            ("Fahrenheit (°F)", "Celsius (°C)"): fahrenheit_to_celsius,
            ("Fahrenheit (°F)", "Kelvin (K)"): fahrenheit_to_kelvin,
            ("Kelvin (K)", "Celsius (°C)"): kelvin_to_celsius,
            ("Kelvin (K)", "Fahrenheit (°F)"): kelvin_to_fahrenheit,
        }
        result = conversions[(from_unit, to_unit)](temp_input)
    
    st.markdown(f"""
    <div class="result-box">
        {temp_input:.2f}° {from_unit.split('(')[1].rstrip(')')} = {result:.2f}° {to_unit.split('(')[1].rstrip(')')}
    </div>
    """, unsafe_allow_html=True)
    
    # Temperature scale comparison
    temps_c = [temp_input if "Celsius" in from_unit else 
              fahrenheit_to_celsius(temp_input) if "Fahrenheit" in from_unit else 
              kelvin_to_celsius(temp_input)]
    temps_f = [celsius_to_fahrenheit(temps_c[0])]
    temps_k = [celsius_to_kelvin(temps_c[0])]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Celsius', x=['Temperature'], y=temps_c, marker_color='#dc3545'))
    fig.add_trace(go.Bar(name='Fahrenheit', x=['Temperature'], y=temps_f, marker_color='#fd7e14'))
    fig.add_trace(go.Bar(name='Kelvin', x=['Temperature'], y=temps_k, marker_color='#6f42c1'))
    
    fig.update_layout(
        title="Temperature Comparison",
        yaxis_title="Temperature",
        barmode='group',
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Length Converter
def length_converter():
    st.markdown('<div class="converter-card length-card">', unsafe_allow_html=True)
    st.markdown("### 📏 Length Converter")
    
    length_units = {
        "mm": {"name": "Millimeter", "to_meters": 0.001},
        "cm": {"name": "Centimeter", "to_meters": 0.01},
        "m": {"name": "Meter", "to_meters": 1.0},
        "km": {"name": "Kilometer", "to_meters": 1000.0},
        "in": {"name": "Inch", "to_meters": 0.0254},
        "ft": {"name": "Foot", "to_meters": 0.3048},
        "yd": {"name": "Yard", "to_meters": 0.9144},
        "mi": {"name": "Mile", "to_meters": 1609.34}
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        length_input = st.number_input("Enter length:", min_value=0.0, value=1.0, step=0.1)
        from_unit = st.selectbox("From:", list(length_units.keys()), 
                               format_func=lambda x: f"{length_units[x]['name']} ({x})")
    
    with col2:
        to_unit = st.selectbox("To:", list(length_units.keys()), index=2,
                             format_func=lambda x: f"{length_units[x]['name']} ({x})")
    
    # Conversion calculation
    meters = length_input * length_units[from_unit]["to_meters"]
    result = meters / length_units[to_unit]["to_meters"]
    
    st.markdown(f"""
    <div class="result-box">
        {length_input:.4f} {from_unit} = {result:.4f} {to_unit}
    </div>
    """, unsafe_allow_html=True)
    
    # Visual comparison
    common_units = ["mm", "cm", "m", "km", "in", "ft"]
    values = [meters / length_units[unit]["to_meters"] for unit in common_units]
    
    fig = px.bar(
        x=common_units, 
        y=values,
        title="Length in Different Units",
        color=values,
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Weight Converter
def weight_converter():
    st.markdown('<div class="converter-card weight-card">', unsafe_allow_html=True)
    st.markdown("### ⚖️ Weight Converter")
    
    weight_units = {
        "mg": {"name": "Milligram", "to_grams": 0.001},
        "g": {"name": "Gram", "to_grams": 1.0},
        "kg": {"name": "Kilogram", "to_grams": 1000.0},
        "oz": {"name": "Ounce", "to_grams": 28.3495},
        "lb": {"name": "Pound", "to_grams": 453.592},
        "st": {"name": "Stone", "to_grams": 6350.29},
        "t": {"name": "Metric Ton", "to_grams": 1000000.0}
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight_input = st.number_input("Enter weight:", min_value=0.0, value=1.0, step=0.1)
        from_unit = st.selectbox("From:", list(weight_units.keys()), index=2,
                               format_func=lambda x: f"{weight_units[x]['name']} ({x})")
    
    with col2:
        to_unit = st.selectbox("To:", list(weight_units.keys()), index=4,
                             format_func=lambda x: f"{weight_units[x]['name']} ({x})")
    
    # Conversion calculation
    grams = weight_input * weight_units[from_unit]["to_grams"]
    result = grams / weight_units[to_unit]["to_grams"]
    
    st.markdown(f"""
    <div class="result-box">
        {weight_input:.4f} {from_unit} = {result:.4f} {to_unit}
    </div>
    """, unsafe_allow_html=True)
    
    # Weight comparison chart
    common_units = ["g", "kg", "oz", "lb"]
    values = [grams / weight_units[unit]["to_grams"] for unit in common_units]
    
    fig = go.Figure(data=go.Scatter(
        x=common_units,
        y=values,
        mode='markers+lines',
        marker=dict(size=12, color=['#ffc107', '#fd7e14', '#dc3545', '#6f42c1']),
        line=dict(color='#17a2b8', width=3)
    ))
    fig.update_layout(
        title="Weight Across Different Units",
        xaxis_title="Unit",
        yaxis_title="Value",
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main application logic
if converter_type == "💱 Currency":
    currency_converter()
elif converter_type == "🌡️ Temperature":
    temperature_converter()
elif converter_type == "📏 Length":
    length_converter()
elif converter_type == "⚖️ Weight":
    weight_converter()

# Footer with additional info
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4>🎯 Accurate</h4>
        <p>Precise conversion formulas</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4>🚀 Fast</h4>
        <p>Instant results</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h4>📱 Responsive</h4>
        <p>Works on all devices</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: #666;">
    <p>Made with ❤️ using Streamlit | © 2024 Universal Unit Converter</p>
</div>
""", unsafe_allow_html=True)