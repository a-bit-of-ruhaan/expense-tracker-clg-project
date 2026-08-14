import streamlit as st
import pandas as pd
from functions.storage import load_expenses


with open("styles/graph_style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(page_title="Expense Analytics", layout="wide")

st.title("Expense Analytics & History")
st.write("Visualizing data saved from your Expense Tracker JSON file.")

# Fetch raw data using your original function logic
expenses_data = load_expenses()

if expenses_data:
    # Convert your raw data into a working DataFrame
    df = pd.DataFrame(expenses_data)
    
    # Standardize dictionary keys to proper column types
    # Adjust dictionary naming ("title", "date", "value") if your JSON properties differ
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # --- SECTION 1: DATA DISPLAY TABLE ---
    st.subheader("Saved Expenses History Table")
    st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)
    
    st.divider()
    
    # --- PREPARE DATA FOR TIMELINE CHARTS ---
    # Group together any items purchased on identical calendar dates
    daily_totals = df.groupby('date')['value'].sum().reset_index()
    daily_totals = daily_totals.set_index('date')
    
    # --- SECTION 2: CHARTS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Spending Trend Line Chart")
        st.line_chart(daily_totals['value'], use_container_width=True)
        
    with col2:
        st.subheader("Daily Volume Bar Chart")
        st.bar_chart(daily_totals['value'], use_container_width=True)
        
else:
    st.info("No expense data found in your storage file. Add some items using app.py first!")
