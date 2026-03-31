import streamlit as st
from datetime import date

# ============ SETUP THE APP ============
st.set_page_config(page_title="My Budget Tracker", page_icon="💰")
st.title("Personal Budget Tracker")

# ============ CREATE A PLACE TO STORE EXPENSES ============
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# ============ SECTION 1: ADD A NEW EXPENSE ============
st.subheader("Manage your Expense")

# Create 3 input boxes
expense_date = st.date_input("Date", value=date.today())
expense_item = st.text_input("Expense Item")
amount_spent = st.text_input("Amount Spent (RM)", value="0.00")

# Submit button
if st.button("Add"):
    try:
        amount = float(amount_spent)
        
        if amount < 0:
            st.error("❌ Error: Amount cannot be negative!")
        else:
            # Store as a simple dictionary (no pandas needed)
            new_expense = {
                'Date': expense_date.strftime('%Y-%m-%d'),  # Convert date to string
                'Expense Item': expense_item,
                'Amount Spent (RM)': amount
            }
            st.session_state.expenses.append(new_expense)
            st.success(f"✅ Expense '{expense_item}' added successfully!")
            
    except ValueError:
        st.error("❌ Error: Please enter a valid number for Amount Spent!")

# ============ SECTION 2: SHOW ALL EXPENSES ============
st.subheader("Expense Summary")

if len(st.session_state.expenses) > 0:
    
    st.table(st.session_state.expenses)
    
    # Calculate total
    total = sum(expense['Amount Spent (RM)'] for expense in st.session_state.expenses)
    st.markdown(f"### 💰 TOTAL EXPENSES: RM {total:.2f}")
        
else:
    st.info("No expenses yet. Add your first expense above!")

# ============ CLEAR BUTTON ============
st.divider()
if st.button("🗑️ Clear All Expenses"):
    st.session_state.expenses = []
    st.success("All expenses cleared!")
    st.rerun()