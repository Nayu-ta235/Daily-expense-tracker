import streamlit as st
from datetime import date

# ============ SETUP THE APP ============
st.set_page_config(page_title="My Budget Tracker", page_icon="💰")
st.title("Personal Budget Tracker")

# ============ CREATE A PLACE TO STORE EXPENSES ============
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# ============ PRE-DEFINED EXPENSE CATEGORIES ============
expense_categories = [
    "Food & Drinks",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Bills & Utilities",
    "Rent/Mortgage",
    "Healthcare",
    "Education",
    "Savings",
    "Car Loan",
    "Insurance",
    "Gifts & Donations",
    "Travel",
    "Other"
]

# ============ SECTION 1: ADD A NEW EXPENSE ============
st.subheader("📝 Add a New Expense")

# Create input fields
expense_date = st.date_input("Date", value=date.today())

# DROPDOWN for expense item instead of text input
expense_item = st.selectbox(
    "Expense Item",
    options=expense_categories,
    help="Choose from the dropdown menu or select 'Other' to type your own"
)

# Optional: Allow user to type custom item if they select "Other"
if expense_item == "Other":
    custom_item = st.text_input("Please specify expense item:", placeholder="e.g., Haircut, Gift, etc.")
    # Use custom item if provided, otherwise keep "Other"
    final_item = custom_item if custom_item else "Other"
else:
    final_item = expense_item

amount_spent = st.text_input("Amount Spent (RM)", value="0.00")

# Submit button
if st.button("Add Expense"):
    try:
        amount = float(amount_spent)
        
        if amount < 0:
            st.error("❌ Error: Amount cannot be negative!")
        elif amount == 0:
            st.warning("⚠️ Amount is zero. Are you sure?")
            # Still add it but with warning
            new_expense = {
                'Date': expense_date.strftime('%Y-%m-%d'),
                'Expense Item': final_item,
                'Amount Spent (RM)': amount
            }
            st.session_state.expenses.append(new_expense)
            st.warning(f"⚠️ Expense '{final_item}' added with RM 0.00")
        else:
            # Save the expense
            new_expense = {
                'Date': expense_date.strftime('%Y-%m-%d'),
                'Expense Item': final_item,
                'Amount Spent (RM)': amount
            }
            st.session_state.expenses.append(new_expense)
            st.success(f"✅ Expense '{final_item}' added successfully!")
            
    except ValueError:
        st.error("❌ Error: Please enter a valid number for Amount Spent (e.g., 10.50)")

# ============ SECTION 2: SHOW ALL EXPENSES ============
st.subheader("Expense Summary")

if len(st.session_state.expenses) > 0:
    
    # Display as a table
    st.table(st.session_state.expenses)
    
    # Calculate total
    total = sum(expense['Amount Spent (RM)'] for expense in st.session_state.expenses)
    st.markdown(f"### 💰 TOTAL EXPENSES: RM {total:.2f}")
    
    # Optional: Show spending by category
    st.subheader("📊 Spending by Category")
    
    # Group expenses by category
    category_totals = {}
    for expense in st.session_state.expenses:
        category = expense['Expense Item']
        amount = expense['Amount Spent (RM)']
        category_totals[category] = category_totals.get(category, 0) + amount
    
    # Display category breakdown
    for category, amount in category_totals.items():
        percentage = (amount / total) * 100 if total > 0 else 0
        st.write(f"- **{category}:** RM {amount:.2f} ({percentage:.1f}%)")
        
else:
    st.info("Add your first expense above!")

# ============ CLEAR BUTTON ============
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Clear All Expenses"):
        st.session_state.expenses = []
        st.success("All expenses cleared!")
        st.rerun()

with col2:
    if st.button("📊 Show Summary"):
        if len(st.session_state.expenses) > 0:
            st.balloons()
            st.success("Thanks for tracking your expenses! 🎉")
        else:
            st.info("Add some expenses first!")