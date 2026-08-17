import streamlit as st 
import pandas as pd 
from functions.storage import load_expenses, save_expenses
from functions.addnew import add_expense 

# Set page config first
st.set_page_config(page_title="Expense Tracker", layout="wide", initial_sidebar_state="collapsed")

# Load CSS
with open("styles/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 

if "expenses" not in st.session_state: 
    st.session_state.expenses = load_expenses()

st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.title("Expense Tracker") 
st.write("Track your daily expenses efficiently and stay on budget.")
st.markdown('</div>', unsafe_allow_html=True) 

st.markdown('<div class="form-container">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1: 
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    title = st.text_input("Expense Description", placeholder="e.g., Grocery shopping, Gas, Rent...") 
    date = st.date_input("Date") 
    value = st.text_input("Amount", key="val_ex", placeholder="e.g., 50.00") 
    st.markdown('</div>', unsafe_allow_html=True)

with col2: 
    st.markdown("""<div style="margin-top: 28px;">""", unsafe_allow_html=True) 
    if st.button("Add Expense", key="add_btn", use_container_width=True): 
        if not title.strip():
            st.error("Please enter an expense description")
        elif not value.strip():
            st.error("Please enter an amount")
        else:
            try:
                float_value = float(value)
                if float_value <= 0:
                    st.error("Amount must be greater than 0")
                else:
                    add_expense(st.session_state.expenses, title.strip(), str(date), str(float_value))
                    st.success(f"'{title}' added for ${float_value:.2f}")
                    st.rerun()
            except ValueError:
                st.error("Please enter a valid number for the amount")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- FIXED SECTION: USING ST.SWITCH_PAGE ---

st.markdown('---', unsafe_allow_html=True)

# Summary Statistics
if st.session_state.expenses:
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    
    values = [float(exp['value']) for exp in st.session_state.expenses]
    total = sum(values)
    avg = total / len(values) if values else 0
    max_exp = max(values) if values else 0
    
    with col_s1:
        st.metric("Total Spent", f"rs{total:.2f}")
    with col_s2:
        st.metric("Average", f"rs{avg:.2f}")
    with col_s3:
        st.metric("Highest", f"rs{max_exp:.2f}")
    with col_s4:
        st.metric("Entries", len(values))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('---', unsafe_allow_html=True)

# --- NEW SECTION: HISTORY SYSTEM ---
st.subheader("Expense History")

if st.session_state.expenses:
    # Convert your raw saved memory into a readable dataframe layout
    history_df = pd.DataFrame(st.session_state.expenses)
    
    # Capitalize layout column labels for a cleaner user interface
    history_df.columns = [str(col).capitalize() for col in history_df.columns]
    
    # Display historical logs in reverse order (newest updates first)
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.dataframe(
        history_df.iloc[::-1], 
        use_container_width=True, 
        hide_index=True
    )
    
    st.markdown('<div class="delete-section">', unsafe_allow_html=True)
    delete_index = st.selectbox("Delete an expense:", 
                                options=range(len(st.session_state.expenses)),
                                format_func=lambda x: f"{st.session_state.expenses[len(st.session_state.expenses)-1-x]['title']} - ${st.session_state.expenses[len(st.session_state.expenses)-1-x]['value']}")
    
    if st.button("Delete Selected", key="delete_btn"):
        actual_index = len(st.session_state.expenses) - 1 - delete_index
        deleted_exp = st.session_state.expenses.pop(actual_index)
        save_expenses(st.session_state.expenses)
        st.success(f"Deleted: {deleted_exp['title']}")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("📭 No expenses yet. Add your first expense above!")

st.markdown('---', unsafe_allow_html=True)

# Navigation Section
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col3, col4, col5 = st.columns([2, 2, 1])

with col3:
    if st.button("Analytics & Insights", key="goto_graphs_btn", use_container_width=True):
        st.switch_page("pages/graph.py")

with col4:
    if st.button("Clear All Data", key="clear_btn", use_container_width=True):
        if st.session_state.get("confirm_clear"):
            st.session_state.expenses = []
            save_expenses([])
            st.success("All expenses cleared!")
            st.session_state.confirm_clear = False
            st.rerun()
        else:
            st.session_state.confirm_clear = True
            st.warning("Click again to confirm clearing all data")

with col5:
    st.empty()

st.markdown('</div>', unsafe_allow_html=True)

st.write("Made By Ruhaan For Internship 2026")
   