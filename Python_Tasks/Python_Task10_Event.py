import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import csv

# Configure page
st.set_page_config(
    page_title="Hackathon Event Registration",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
CSV_FILE = "registrations.csv"
EVENT_OPTIONS = [
    "Web Development Hackathon",
    "AI/ML Hackathon", 
    "Mobile App Hackathon",
    "Blockchain Hackathon",
    "IoT Hackathon",
    "Game Development Hackathon"
]

def initialize_csv():
    """Initialize CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Email', 'Registration Date', 'Event Choice', 'Timestamp'])

def save_registration(name, email, reg_date, event_choice):
    """Save registration data to CSV"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, reg_date, event_choice, timestamp])

def load_registrations():
    """Load registrations from CSV"""
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=['Name', 'Email', 'Registration Date', 'Event Choice', 'Timestamp'])
    return pd.DataFrame(columns=['Name', 'Email', 'Registration Date', 'Event Choice', 'Timestamp'])

def get_registration_count():
    """Get total number of registrations"""
    df = load_registrations()
    return len(df)

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Initialize CSV file
initialize_csv()

# Main app
def main():
    # Header
    st.title("🚀 Hackathon Event Registration")
    st.markdown("---")
    
    # Sidebar - Live Stats
    with st.sidebar:
        st.header("📊 Live Statistics")
        total_registrations = get_registration_count()
        st.metric("Total Registrations", total_registrations)
        
        # Event-wise count
        if total_registrations > 0:
            df = load_registrations()
            event_counts = df['Event Choice'].value_counts()
            st.subheader("Registrations by Event")
            for event, count in event_counts.items():
                st.write(f"• {event}: {count}")
        
        st.markdown("---")
        
        # CSV Export
        st.header("📥 Export Data")
        if st.button("Download CSV", type="secondary"):
            df = load_registrations()
            if not df.empty:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Click to Download",
                    data=csv_data,
                    file_name=f"registrations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data to export!")
    
    # Registration Form Section
    st.header("🎯 Register for Event")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Name input
            name = st.text_input(
                "Full Name *",
                placeholder="Enter your full name",
                help="Please enter your complete name"
            )
            
            # Email input
            email = st.text_input(
                "Email Address *",
                placeholder="Enter your email address",
                help="We'll use this to send you event updates"
            )
        
        with col2:
            # Date input
            reg_date = st.date_input(
                "Registration Date *",
                value=date.today(),
                help="Select your preferred registration date"
            )
            
            # Event choice
            event_choice = st.selectbox(
                "Choose Your Event *",
                options=EVENT_OPTIONS,
                help="Select the hackathon event you want to participate in"
            )
        
        # Terms and conditions
        terms_accepted = st.checkbox(
            "I agree to the terms and conditions *",
            help="You must accept the terms to register"
        )
        
        # Submit button
        submitted = st.form_submit_button(
            "🚀 Register Now",
            type="primary",
            use_container_width=True
        )
        
        # Form validation and submission
        if submitted:
            # Validation
            errors = []
            
            if not name.strip():
                errors.append("Name is required")
            
            if not email.strip():
                errors.append("Email is required")
            elif not validate_email(email):
                errors.append("Please enter a valid email address")
            
            if not terms_accepted:
                errors.append("You must accept the terms and conditions")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Check for duplicate registration
                df = load_registrations()
                if not df.empty and email.lower() in df['Email'].str.lower().values:
                    st.warning("⚠️ This email is already registered!")
                else:
                    # Save registration
                    try:
                        save_registration(name.strip(), email.lower().strip(), str(reg_date), event_choice)
                        st.success("🎉 Registration successful!")
                        st.balloons()
                        
                        # Show confirmation details
                        st.info(f"""
                        **Registration Confirmed!**
                        - Name: {name}
                        - Email: {email}
                        - Event: {event_choice}
                        - Date: {reg_date}
                        
                        You'll receive a confirmation email shortly!
                        """)
                        
                        # Auto-refresh the page
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Registration failed: {str(e)}")
    
    st.markdown("---")
    
    # Registration Details Table Section
    st.header("📋 All Registration Details")
    
    df = load_registrations()
    if not df.empty:
        # Add search and filter options
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_term = st.text_input("🔍 Search by Name or Email", placeholder="Enter name or email to search...")
        
        with col2:
            event_filter = st.selectbox("Filter by Event", ["All Events"] + EVENT_OPTIONS)
        
        with col3:
            sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Name A-Z", "Name Z-A"])
        
        # Apply filters
        filtered_df = df.copy()
        
        # Search filter
        if search_term:
            filtered_df = filtered_df[
                filtered_df['Name'].str.contains(search_term, case=False, na=False) |
                filtered_df['Email'].str.contains(search_term, case=False, na=False)
            ]
        
        # Event filter
        if event_filter != "All Events":
            filtered_df = filtered_df[filtered_df['Event Choice'] == event_filter]
        
        # Sorting
        if sort_by == "Newest First":
            filtered_df = filtered_df.sort_values('Timestamp', ascending=False)
        elif sort_by == "Oldest First":
            filtered_df = filtered_df.sort_values('Timestamp', ascending=True)
        elif sort_by == "Name A-Z":
            filtered_df = filtered_df.sort_values('Name', ascending=True)
        elif sort_by == "Name Z-A":
            filtered_df = filtered_df.sort_values('Name', ascending=False)
        
        # Display results count
        st.write(f"Showing {len(filtered_df)} of {len(df)} registrations")
        
        if not filtered_df.empty:
            # Format the dataframe for better display
            display_df = filtered_df.copy()
            display_df.index = range(1, len(display_df) + 1)  # Start index from 1
            
            # Rename columns for better display
            display_df = display_df.rename(columns={
                'Name': '👤 Name',
                'Email': '📧 Email',
                'Registration Date': '📅 Registration Date',
                'Event Choice': '🎯 Event',
                'Timestamp': '⏰ Registered At'
            })
            
            # Display the table with custom styling
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=False,
                column_config={
                    "👤 Name": st.column_config.TextColumn(
                        width="medium"
                    ),
                    "📧 Email": st.column_config.TextColumn(
                        width="large"
                    ),
                    "📅 Registration Date": st.column_config.DateColumn(
                        width="small"
                    ),
                    "🎯 Event": st.column_config.TextColumn(
                        width="large"
                    ),
                    "⏰ Registered At": st.column_config.DatetimeColumn(
                        width="medium",
                        format="DD/MM/YYYY HH:mm"
                    )
                }
            )
        else:
            st.info("🔍 No registrations match your search criteria. Try adjusting your filters.")
    else:
        st.info("📝 No registrations yet. Be the first to register! 🚀")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🏆 Hackathon Event Registration System | Built with Streamlit</p>
            <p>Questions? Contact us at support@hackathon.com</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()