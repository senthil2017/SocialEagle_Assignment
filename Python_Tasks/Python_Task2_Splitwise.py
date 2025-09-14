import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Streamlit page setup ---
st.set_page_config(page_title="Splitwise Expense App", layout="centered")
st.title("💸 My Expense Splitter")

# --- Inputs ---
st.header("🌗 Choose Split Mode")

split_mode = st.radio("How do you want to split the expense?",
                      ["Equal Split", "Individual Contribution"])

# Common Inputs
total_amount = st.number_input("Total Expense Amount (₹)", min_value=0.0, format="%.2f")
num_people = st.number_input("Number of People", min_value=1, step=1)

# Container to collect people data
names = []
contributions = []

if split_mode == "Equal Split":
    st.header("👥 Enter Names")
    for i in range(int(num_people)):
        name = st.text_input(f"Person #{i+1} Name", value=f"Person {i+1}", key=f"name_{i}")
        names.append(name)

    if total_amount:
        equal_share = total_amount / num_people
        contributions = [equal_share for _ in range(int(num_people))]
        st.success(f"Each person should pay: ₹{equal_share:.2f}")

else:  # Individual Contribution Mode
    st.header("✍️ Enter Individual Contributions")
    for i in range(int(num_people)):
        cols = st.columns([2, 1])
        with cols[0]:
            name = st.text_input(f"Person #{i+1} Name", value=f"Person {i+1}", key=f"name_{i}")
        with cols[1]:
            amount = st.number_input(f"Contribution", min_value=0.0, format="%.2f", key=f"amt_{i}")
        names.append(name)
        contributions.append(amount)

# --- Calculation & Display ---
if st.button("💡 Calculate Settlements") and total_amount > 0 and num_people > 0:
    df = pd.DataFrame({
        "Name": names,
        "Contribution": contributions
    })

    equal_share = total_amount / num_people
    df["Expected"] = equal_share
    df["Balance"] = df["Contribution"] - df["Expected"]

    # Total contributed and gap from the total
    total_contributed = sum(contributions)
    unaccounted = total_amount - total_contributed

    # Display summary
    st.subheader("💰 Summary Table")
    st.dataframe(df.style.format({"Contribution": "₹{:.2f}", "Expected": "₹{:.2f}", "Balance": "₹{:.2f}"}))

    if split_mode == "Individual Contribution":
        if abs(unaccounted) < 0.01:
            st.success("✅ All contributions match the total expense.")
        elif unaccounted > 0:
            st.warning(f"⚠️ ₹{unaccounted:.2f} is **unaccounted for** (less than total).")
        else:
            st.info(f"ℹ️ ₹{abs(unaccounted):.2f} is **overpaid** (more than total).")

    # --- Pie Chart ---
    st.subheader("📊 Contributions Pie Chart")

    # Use distinct colors per person
    distinct_colors = plt.get_cmap('tab20').colors  # Up to 20 unique colors

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')

    ax.pie(
        df["Contribution"],
        labels=df["Name"],
        autopct=lambda pct: f'₹{(pct/100)*sum(df["Contribution"]):.2f}' if pct > 0 else '',
        colors=distinct_colors[:len(df)],
        startangle=90
    )

    ax.set_title("Individual Contributions")
    ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
    st.pyplot(fig)

    # --- Settlement Summary ---
    st.subheader("🔁 Settlement Summary")
    for _, row in df.iterrows():
        if row["Balance"] < -0.01:
            st.write(f"💸 {row['Name']} should **pay** ₹{abs(row['Balance']):.2f}")
        elif row["Balance"] > 0.01:
            st.write(f"💵 {row['Name']} should **receive** ₹{row['Balance']:.2f}")
        else:
            st.write(f"✅ {row['Name']} is settled.")
