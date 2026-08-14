import streamlit as st 
import pandas as pd 
from functions.storage import load_expenses 
from functions.addnew import add_expense 


with open("styles/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



st.set_page_config( page_title="Expense Tracker", layout="wide" ) 

if "expenses" not in st.session_state: 
    st.session_state.expenses = load_expenses() 

st.title("Expense Tracker") 
st.write("Track your daily Expenses.") 

col1, col2 = st.columns([3,1]) 
with col1: 
    title = st.text_input( "NEW EXPENSES", placeholder="Add a new expense" ) 
    date = st.date_input( "Date" ) 
    value = st.text_input( "Value", key="val_ex", placeholder="Amount", ) 
    if "val_ex": 
        isDigit=True 

with col2: 
    st.markdown(""" <div class="butn_1">""", unsafe_allow_html=True) 
    if st.button("Add New", key="add_btn"): 
        if title.strip(): 
            add_expense( st.session_state.expenses, title, str(date), value ) 
            st.success("Expense added successfully!") 
            st.rerun() 
        else: 
            st.warning("Please enter an Expense")

# --- FIXED SECTION: USING ST.SWITCH_PAGE ---

st.divider()

# --- NEW SECTION: HISTORY SYSTEM ---
st.subheader("Saved Expenses History")

if st.session_state.expenses:
    # Convert your raw saved memory into a readable dataframe layout
    history_df = pd.DataFrame(st.session_state.expenses)
    
    # Capitalize layout column labels for a cleaner user interface
    history_df.columns = [str(col).capitalize() for col in history_df.columns]
    
    # Display historical logs in reverse order (newest updates first)
    st.dataframe(
        history_df.iloc[::-1], 
        use_container_width=True, 
        hide_index=True
    )
else:
    st.info("Your expense ledger history is currently empty.")


    st.markdown("""<div class="col_f">""", unsafe_allow_html=True)


col3, col4, col5 = st.columns([2, 2, 1])

with col3:
     st.markdown("""<br>""", unsafe_allow_html=True)
     st.markdown('<div class="nav_btn_container" style="margin-top: 28px;">', unsafe_allow_html=True)
    # Using a native button combined with st.switch_page
     if st.button("View Tracks of Your Expenses", key="goto_graphs_btn", use_container_width=True):
        st.switch_page("pages/graph.py")
st.markdown('</div>', unsafe_allow_html=True)


with col4:
    st.empty()

with col5:
        st.image("images/image1.png", width=125)
        st.markdown("""</div>""", unsafe_allow_html=True)
   