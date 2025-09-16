import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Currency Converter Pro",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for attractive UI
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #6dd5ed 100%);
        background-attachment: fixed;
    }
    
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sub-header {
        text-align: center;
        color: #e8f4f8;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .converter-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        margin: 2rem 0;
    }
    
    .result-box {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b95 50%, #c44569 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(255, 107, 149, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .rate-info {
        background: rgba(255, 255, 255, 100.15);
        backdrop-filter: blur(8px);
        padding: 1rem;
        border-radius: 15px;
        border-left: 4px solid #4ecdc4;
        margin: 1rem 0;
        color: #2c3e50 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .rate-info strong {
        color: #2c3e50 !important;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, rgba(255,255,255,0.25), rgba(255,255,255,0.15));
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
    }
    
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        font-size: 1.1rem !important;
        background: rgba(0,0,0,0.3);
        padding: 2px 8px;
        border-radius: 5px;
        backdrop-filter: blur(3px);
    }
    
    .stSelectbox > div > div > div {
        color: #2c3e50 !important;
        font-weight: bold;
    }
    
    .stNumberInput > div > div > input {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.8));
        backdrop-filter: blur(5px);
        border: 2px solid rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        color: #2c3e50 !important;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .stNumberInput label {
        color: #ffffff !important;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        font-size: 1.1rem !important;
        background: rgba(0,0,0,0.3);
        padding: 2px 8px;
        border-radius: 5px;
        backdrop-filter: blur(3px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.6);
    }
    
    .footer {
        text-align: center;
        color: #e8f4f8;
        margin-top: 3rem;
        font-style: italic;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Metric styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(5px);
        border-radius: 10px;
        padding: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: #2c3e50 !important;
    }
    
    /* Fix ALL metric text visibility with stronger selectors */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 2px solid rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        margin: 0.5rem 0 !important;
    }
    
    div[data-testid="metric-container"] * {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        color: #1a1a1a !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="metric-label"] {
        color: #2c3e50 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    /* Fix info box with stronger selectors */
    div[data-testid="stInfo"] {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-left: 5px solid #4ecdc4 !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        padding: 1.5rem !important;
    }
    
    div[data-testid="stInfo"] * {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stInfo"] p {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Warning and error styling */
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.2), rgba(255, 152, 0, 0.2));
        backdrop-filter: blur(5px);
        border-left: 4px solid #ffc107;
        border-radius: 10px;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.2), rgba(255, 107, 149, 0.2));
        backdrop-filter: blur(5px);
        border-left: 4px solid #dc3545;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Currency data with flags and names
CURRENCIES = {
    'USD': {'name': 'US Dollar', 'flag': '🇺🇸'},
    'EUR': {'name': 'Euro', 'flag': '🇪🇺'},
    'GBP': {'name': 'British Pound', 'flag': '🇬🇧'},
    'JPY': {'name': 'Japanese Yen', 'flag': '🇯🇵'},
    'AUD': {'name': 'Australian Dollar', 'flag': '🇦🇺'},
    'CAD': {'name': 'Canadian Dollar', 'flag': '🇨🇦'},
    'CHF': {'name': 'Swiss Franc', 'flag': '🇨🇭'},
    'CNY': {'name': 'Chinese Yuan', 'flag': '🇨🇳'},
    'SEK': {'name': 'Swedish Krona', 'flag': '🇸🇪'},
    'NZD': {'name': 'New Zealand Dollar', 'flag': '🇳🇿'},
    'MXN': {'name': 'Mexican Peso', 'flag': '🇲🇽'},
    'SGD': {'name': 'Singapore Dollar', 'flag': '🇸🇬'},
    'HKD': {'name': 'Hong Kong Dollar', 'flag': '🇭🇰'},
    'NOK': {'name': 'Norwegian Krone', 'flag': '🇳🇴'},
    'KRW': {'name': 'South Korean Won', 'flag': '🇰🇷'},
    'TRY': {'name': 'Turkish Lira', 'flag': '🇹🇷'},
    'RUB': {'name': 'Russian Ruble', 'flag': '🇷🇺'},
    'INR': {'name': 'Indian Rupee', 'flag': '🇮🇳'},
    'BRL': {'name': 'Brazilian Real', 'flag': '🇧🇷'},
    'ZAR': {'name': 'South African Rand', 'flag': '🇿🇦'}
}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_exchange_rate(from_currency, to_currency):
    """
    Fetch exchange rate from a free API service
    """
    try:
        # Using exchangerate-api.com (free tier)
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if to_currency in data['rates']:
            return data['rates'][to_currency], data['date']
        else:
            return None, None
    except Exception as e:
        st.error(f"Error fetching exchange rate: {str(e)}")
        return None, None

def format_currency_display(code):
    """Format currency for display in dropdown"""
    return f"{CURRENCIES[code]['flag']} {code} - {CURRENCIES[code]['name']}"

def main():
    # Header
    st.markdown('<h1 class="main-header">💱 Currency Converter Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Convert currencies with real-time exchange rates</p>', unsafe_allow_html=True)
    
    # Create columns for layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        #st.markdown('<div class="converter-box">', unsafe_allow_html=True)
        
        # Currency selection
        col_from, col_to = st.columns(2)
        
        with col_from:
            st.markdown('<p style="color: white; font-weight: bold; font-size: 1.1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.8); background: rgba(0,0,0,0.3); padding: 4px 8px; border-radius: 5px; margin-bottom: 5px;">From Currency:</p>', unsafe_allow_html=True)
            from_currency = st.selectbox(
                "Select source currency",
                options=list(CURRENCIES.keys()),
                format_func=format_currency_display,
                index=0,  # Default to USD
                label_visibility="collapsed"
            )
        
        with col_to:
            st.markdown('<p style="color: white; font-weight: bold; font-size: 1.1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.8); background: rgba(0,0,0,0.3); padding: 4px 8px; border-radius: 5px; margin-bottom: 5px;">To Currency:</p>', unsafe_allow_html=True)
            to_currency = st.selectbox(
                "Select target currency",
                options=list(CURRENCIES.keys()),
                format_func=format_currency_display,
                index=1,  # Default to EUR
                label_visibility="collapsed"
            )
        
        # Amount input
        st.markdown('<p style="color: white; font-weight: bold; font-size: 1.1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.8); background: rgba(0,0,0,0.3); padding: 4px 8px; border-radius: 5px; margin-bottom: 5px;">Amount:</p>', unsafe_allow_html=True)
        amount = st.number_input(
            "Enter amount to convert",
            min_value=0.01,
            value=100.0,
            step=0.01,
            format="%.2f",
            label_visibility="collapsed"
        )
        
        # Swap button
        col_swap1, col_swap2, col_swap3 = st.columns([1, 1, 1])
        with col_swap2:
            if st.button("🔄 Swap Currencies", use_container_width=True):
                # Store the values to swap
                st.session_state.temp_from = to_currency
                st.session_state.temp_to = from_currency
                st.rerun()
        
        # Handle currency swapping
        if hasattr(st.session_state, 'temp_from'):
            from_currency = st.session_state.temp_from
            to_currency = st.session_state.temp_to
            del st.session_state.temp_from
            del st.session_state.temp_to
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Convert button and results
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💰 Convert Currency", use_container_width=True, type="primary"):
            if from_currency == to_currency:
                st.warning("⚠️ Please select different currencies for conversion.")
            else:
                with st.spinner("Fetching latest exchange rates..."):
                    rate, date = get_exchange_rate(from_currency, to_currency)
                    
                    if rate:
                        converted_amount = amount * rate
                        
                        # Display result
                        st.markdown(f'''
                        <div class="result-box">
                            {CURRENCIES[from_currency]['flag']} {amount:.2f} {from_currency} = 
                            {CURRENCIES[to_currency]['flag']} {converted_amount:.2f} {to_currency}
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Display rate information
                        st.markdown(f'''
                        <div class="rate-info">
                            <strong>📊 Exchange Rate Information:</strong><br>
                            1 {from_currency} = {rate:.6f} {to_currency}<br>
                            1 {to_currency} = {1/rate:.6f} {from_currency}<br>
                            <small>📅 Last updated: {date}</small>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Additional conversion amounts
                        st.markdown('<p style="color: white; font-weight: bold; font-size: 1.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.8); background: rgba(0,0,0,0.3); padding: 4px 8px; border-radius: 5px; margin-bottom: 10px; text-align: center;">💡 Quick Reference:</p>', unsafe_allow_html=True)
                        reference_amounts = [1, 10, 100, 1000]
                        cols = st.columns(len(reference_amounts))
                        
                        for i, ref_amount in enumerate(reference_amounts):
                            with cols[i]:
                                ref_converted = ref_amount * rate
                                st.metric(
                                    label=f"{ref_amount} {from_currency}",
                                    value=f"{ref_converted:.2f} {to_currency}"
                                )
                    else:
                        st.error("❌ Unable to fetch exchange rate. Please try again later.")
    
    # Historical rate chart placeholder
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        #st.info("📈 **Pro Tip:** Exchange rates fluctuate throughout the day. For large transactions, consider the timing of your conversion!", font_color="white")
        st.markdown(
            "<div style='background-color:#2196F3;padding:10px;border-radius:8px;color:white;'>"
            "📈 <b>Pro Tip:</b> Exchange rates fluctuate throughout the day. For large transactions, consider the timing of your conversion!"
            "</div>",
            unsafe_allow_html=True
        )
    
    # Footer
    st.markdown('''
    <div class="footer">
        <p>💡 Powered by real-time exchange rate APIs | Built with Streamlit</p>
        <p>⚠️ Disclaimer: Rates are for informational purposes only. Please verify with your bank for actual transaction rates.</p>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()