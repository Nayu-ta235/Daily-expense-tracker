import streamlit as st
import pandas as pd
from datetime import date

# ============ SETUP THE APP ============
st.set_page_config(page_title="My Budget Tracker", page_icon="💰")
st.title("Personal Budget Tracker")

# ============ CREATE A PLACE TO STORE EXPENSES ============
# This creates an empty list (like a notebook) to store all expenses
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# ============ SECTION 1: ADD A NEW EXPENSE ============
st.subheader("📝 Add a New Expense")

# Create 3 input boxes for the user
expense_date = st.date_input("Date", value=date.today())
expense_item = st.text_input("Expense Item (e.g., Coffee, Rent, Shopping)")
amount_spent = st.text_input("Amount Spent (RM)", value="0.00")

# Submit button
if st.button("✅ Add Expense"):
    # === EXCEPTION HANDLING STARTS HERE ===
    try:
        # Try to convert the amount to a number
        amount = float(amount_spent)
        
        # Check if amount is negative
        if amount < 0:
            st.error("❌ Error: Amount cannot be negative! Please enter a positive number.")
        else:
            # All good! Save the expense
            new_expense = {
                'Date': expense_date,
                'Expense Item': expense_item,
                'Amount Spent (RM)': amount
            }
            st.session_state.expenses.append(new_expense)
            
            # Show success message
            st.success(f"✅ Expense '{expense_item}' added successfully!")
            
    except ValueError:
        # This runs if user didn't enter a number
        st.error("❌ Error: Please enter a valid number for Amount Spent (e.g., 10.50)")
    # === EXCEPTION HANDLING ENDS HERE ===

# ============ SECTION 2: SHOW ALL EXPENSES ============
st.subheader("📊 Expense Summary")

# Check if there are any expenses to show
if len(st.session_state.expenses) > 0:
    
    # Convert the list to a table format
    df = pd.DataFrame(st.session_state.expenses)
    
    # Format the date to look nice
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    
    # Format amounts with 2 decimal places
    df['Amount Spent (RM)'] = df['Amount Spent (RM)'].apply(lambda x: f"{x:.2f}")
    
    # Display the table
    st.dataframe(df, use_container_width=True)
    
    # Calculate and show total
    total = sum(expense['Amount Spent (RM)'] for expense in st.session_state.expenses)
    st.markdown(f"### 💰 TOTAL EXPENSES: RM {total:.2f}")
    
    # Optional: Button to save to file
    if st.button("💾 Save to CSV file"):
        df.to_csv('my_expenses.csv', index=False)
        st.success("Expenses saved to 'my_expenses.csv'!")
        
else:
    # Show this message if no expenses yet
    st.info("📭 No expenses yet. Add your first expense above!")

# ============ EXTRA: BUTTON TO CLEAR EVERYTHING ============
st.divider()  # Draws a line
if st.button("🗑️ Clear All Expenses"):
    st.session_state.expenses = []
    st.success("All expenses cleared!")
    st.rerun()  # Refresh the page