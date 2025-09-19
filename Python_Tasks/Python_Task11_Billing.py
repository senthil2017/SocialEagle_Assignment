import streamlit as st
import pandas as pd
from datetime import datetime, date
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import json

# Configure page
st.set_page_config(
    page_title="🥗 Veg Restaurant Order & Billing",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #2E8B57;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: bold;
}
.section-header {
    font-size: 1.5rem;
    color: #4CAF50;
    margin: 1rem 0;
    border-bottom: 2px solid #4CAF50;
    padding-bottom: 0.5rem;
}
.order-summary {
    background-color: #f0f8f0;
    padding: 1rem;
    border-radius: 10px;
    border: 2px solid #4CAF50;
}
.total-amount {
    font-size: 1.5rem;
    font-weight: bold;
    color: #2E8B57;
}
.metric-container {
    background: linear-gradient(90deg, #4CAF50, #2E8B57);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Menu items with prices
MENU_ITEMS = {
    "Idly (2 pcs)": 40,
    "Pongal": 60,
    "Vada (2 pcs)": 45,
    "Chappathi (2 pcs)": 50,
    "Masala Dosa": 80,
    "Ghee Dosa": 90
}

# Tax rate
TAX_RATE = 0.18  # 18% GST

# Initialize session state
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'current_order' not in st.session_state:
    st.session_state.current_order = {}

def reset_current_order():
    st.session_state.current_order = {}

def add_to_orders(order_data):
    st.session_state.orders.append(order_data)

def calculate_bill(items):
    subtotal = sum(MENU_ITEMS[item] * qty for item, qty in items.items() if qty > 0)
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    return subtotal, tax, total

def generate_invoice_pdf(order_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.green,
        alignment=1,
        spaceAfter=30
    )
    
    story = []
    
    # Restaurant header
    story.append(Paragraph("🥗 Green Garden Restaurant", title_style))
    story.append(Paragraph("Vegetarian Delights", styles['Normal']))
    story.append(Paragraph("Address: 123 Garden Street, Green City", styles['Normal']))
    story.append(Paragraph("Phone: +91 98765 43210", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Invoice details
    story.append(Paragraph(f"<b>Invoice #{order_data['order_id']}</b>", styles['Heading2']))
    story.append(Paragraph(f"Date: {order_data['date']}", styles['Normal']))
    story.append(Paragraph(f"Customer: {order_data['customer_name']}", styles['Normal']))
    story.append(Paragraph(f"Phone: {order_data['phone']}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Order items table
    table_data = [['Item', 'Quantity', 'Rate (₹)', 'Amount (₹)']]
    for item, qty in order_data['items'].items():
        if qty > 0:
            rate = MENU_ITEMS[item]
            amount = rate * qty
            table_data.append([item, str(qty), f"₹{rate}", f"₹{amount}"])
    
    # Add totals
    table_data.append(['', '', 'Subtotal:', f"₹{order_data['subtotal']:.2f}"])
    table_data.append(['', '', 'Tax (18%):', f"₹{order_data['tax']:.2f}"])
    table_data.append(['', '', 'Total:', f"₹{order_data['total']:.2f}"])
    
    table = Table(table_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -3), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 30))
    story.append(Paragraph("Thank you for dining with us!", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def main():
    st.markdown('<h1 class="main-header">🥗 Green Garden Restaurant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Authentic Vegetarian Delights</p>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("🍽️ Navigation")
    page = st.sidebar.selectbox("Choose a page", ["📝 New Order", "📊 Sales Analysis", "📋 Order History"])
    
    if page == "📝 New Order":
        show_order_page()
    elif page == "📊 Sales Analysis":
        show_analytics_page()
    elif page == "📋 Order History":
        show_order_history()

def show_order_page():
    st.markdown('<div class="section-header">📝 New Order</div>', unsafe_allow_html=True)
    
    # Customer Information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        customer_name = st.text_input("👤 Customer Name", placeholder="Enter customer name")
    
    with col2:
        phone = st.text_input("📱 Phone Number", placeholder="Enter phone number")
    
    with col3:
        order_date = st.date_input("📅 Order Date", value=date.today())
    
    st.divider()
    
    # Menu Selection
    st.markdown('<div class="section-header">🍽️ Menu Selection</div>', unsafe_allow_html=True)
    
    # Create columns for menu items
    col1, col2 = st.columns(2)
    
    order_items = {}
    
    menu_list = list(MENU_ITEMS.items())
    
    with col1:
        for i in range(0, len(menu_list), 2):
            item, price = menu_list[i]
            st.markdown(f"**{item}** - ₹{price}")
            quantity = st.number_input(f"Quantity", min_value=0, max_value=20, value=0, key=f"qty_{item}")
            order_items[item] = quantity
            st.markdown("---")
    
    with col2:
        for i in range(1, len(menu_list), 2):
            if i < len(menu_list):
                item, price = menu_list[i]
                st.markdown(f"**{item}** - ₹{price}")
                quantity = st.number_input(f"Quantity", min_value=0, max_value=20, value=0, key=f"qty_{item}")
                order_items[item] = quantity
                st.markdown("---")
    
    # Order Summary
    if any(qty > 0 for qty in order_items.values()):
        st.markdown('<div class="section-header">📄 Order Summary</div>', unsafe_allow_html=True)
        
        subtotal, tax, total = calculate_bill(order_items)
        
        # Create summary DataFrame
        summary_data = []
        for item, qty in order_items.items():
            if qty > 0:
                price = MENU_ITEMS[item]
                amount = price * qty
                summary_data.append({
                    "Item": item,
                    "Quantity": qty,
                    "Rate (₹)": price,
                    "Amount (₹)": amount
                })
        
        if summary_data:
            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
            
            # Bill totals
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Subtotal", f"₹{subtotal:.2f}")
            with col2:
                st.metric("Tax (18%)", f"₹{tax:.2f}")
            with col3:
                st.metric("**Total**", f"₹{total:.2f}", delta=None)
            
            # Place Order Button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🛒 Place Order", type="primary", use_container_width=True):
                    if customer_name and phone:
                        order_data = {
                            'order_id': f"ORD{len(st.session_state.orders) + 1:04d}",
                            'customer_name': customer_name,
                            'phone': phone,
                            'date': str(order_date),
                            'items': order_items.copy(),
                            'subtotal': subtotal,
                            'tax': tax,
                            'total': total,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        add_to_orders(order_data)
                        st.success("🎉 Order placed successfully!")
                        st.balloons()
                        
                        # Download options
                        st.markdown("### 📥 Download Invoice")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # CSV Download
                            csv_data = pd.DataFrame([{
                                'Order ID': order_data['order_id'],
                                'Customer': order_data['customer_name'],
                                'Phone': order_data['phone'],
                                'Date': order_data['date'],
                                'Items': ', '.join([f"{item}({qty})" for item, qty in order_items.items() if qty > 0]),
                                'Subtotal': subtotal,
                                'Tax': tax,
                                'Total': total
                            }])
                            
                            csv = csv_data.to_csv(index=False)
                            st.download_button(
                                label="📊 Download CSV",
                                data=csv,
                                file_name=f"invoice_{order_data['order_id']}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        
                        with col2:
                            # PDF Download
                            pdf_buffer = generate_invoice_pdf(order_data)
                            st.download_button(
                                label="📄 Download PDF",
                                data=pdf_buffer,
                                file_name=f"invoice_{order_data['order_id']}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                    else:
                        st.error("Please enter customer name and phone number!")

def show_analytics_page():
    st.markdown('<div class="section-header">📊 Sales Analysis</div>', unsafe_allow_html=True)
    
    if not st.session_state.orders:
        st.info("No orders available for analysis. Please place some orders first.")
        return
    
    # Convert orders to DataFrame
    orders_df = pd.DataFrame(st.session_state.orders)
    orders_df['date'] = pd.to_datetime(orders_df['date'])
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", len(orders_df))
    
    with col2:
        total_revenue = orders_df['total'].sum()
        st.metric("Total Revenue", f"₹{total_revenue:.2f}")
    
    with col3:
        avg_order = orders_df['total'].mean()
        st.metric("Avg Order Value", f"₹{avg_order:.2f}")
    
    with col4:
        total_tax = orders_df['tax'].sum()
        st.metric("Total Tax Collected", f"₹{total_tax:.2f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Daily Sales")
        daily_sales = orders_df.groupby(orders_df['date'].dt.date)['total'].sum().reset_index()
        st.bar_chart(daily_sales.set_index('date'))
    
    with col2:
        st.subheader("🥘 Popular Items")
        # Extract item popularity
        item_counts = {}
        for order in st.session_state.orders:
            for item, qty in order['items'].items():
                if qty > 0:
                    item_counts[item] = item_counts.get(item, 0) + qty
        
        if item_counts:
            items_df = pd.DataFrame(list(item_counts.items()), columns=['Item', 'Quantity'])
            st.bar_chart(items_df.set_index('Item'))
    
    # Recent Orders Table
    st.subheader("🕒 Recent Orders")
    display_df = orders_df[['order_id', 'customer_name', 'phone', 'date', 'total']].copy()
    display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
    display_df.columns = ['Order ID', 'Customer', 'Phone', 'Date', 'Total (₹)']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

def show_order_history():
    st.markdown('<div class="section-header">📋 Order History</div>', unsafe_allow_html=True)
    
    if not st.session_state.orders:
        st.info("No order history available.")
        return
    
    # Search and filter options
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("🔍 Search by customer name or order ID")
    with col2:
        date_filter = st.date_input("📅 Filter by date (optional)")
    
    # Filter orders
    filtered_orders = st.session_state.orders
    
    if search_term:
        filtered_orders = [
            order for order in filtered_orders
            if search_term.lower() in order['customer_name'].lower() or 
               search_term.lower() in order['order_id'].lower()
        ]
    
    if date_filter:
        filtered_orders = [
            order for order in filtered_orders
            if order['date'] == str(date_filter)
        ]
    
    # Display orders
    for order in reversed(filtered_orders):  # Show recent orders first
        with st.expander(f"Order {order['order_id']} - {order['customer_name']} - ₹{order['total']:.2f}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Customer:** {order['customer_name']}")
                st.write(f"**Phone:** {order['phone']}")
                st.write(f"**Date:** {order['date']}")
                st.write(f"**Time:** {order['timestamp']}")
            
            with col2:
                st.write(f"**Subtotal:** ₹{order['subtotal']:.2f}")
                st.write(f"**Tax:** ₹{order['tax']:.2f}")
                st.write(f"**Total:** ₹{order['total']:.2f}")
            
            # Items ordered
            st.write("**Items Ordered:**")
            items_data = []
            for item, qty in order['items'].items():
                if qty > 0:
                    items_data.append({
                        'Item': item,
                        'Quantity': qty,
                        'Rate': f"₹{MENU_ITEMS[item]}",
                        'Amount': f"₹{MENU_ITEMS[item] * qty}"
                    })
            
            if items_data:
                st.dataframe(pd.DataFrame(items_data), use_container_width=True, hide_index=True)
    
    # Export all data
    if st.session_state.orders:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            # Export to CSV
            all_orders_data = []
            for order in st.session_state.orders:
                items_str = ', '.join([f"{item}({qty})" for item, qty in order['items'].items() if qty > 0])
                all_orders_data.append({
                    'Order ID': order['order_id'],
                    'Customer': order['customer_name'],
                    'Phone': order['phone'],
                    'Date': order['date'],
                    'Time': order['timestamp'],
                    'Items': items_str,
                    'Subtotal': order['subtotal'],
                    'Tax': order['tax'],
                    'Total': order['total']
                })
            
            csv_data = pd.DataFrame(all_orders_data).to_csv(index=False)
            st.download_button(
                "📊 Export All Orders (CSV)",
                csv_data,
                "all_orders.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            if st.button("🗑️ Clear All Orders", type="secondary", use_container_width=True):
                st.session_state.orders = []
                st.success("All orders cleared!")
                st.experimental_rerun()

if __name__ == "__main__":
    main()