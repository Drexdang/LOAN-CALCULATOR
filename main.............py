import streamlit as st
import sqlite3

# Function to create the customer table
def create_table():
    conn = sqlite3.connect('customer_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )''')
    conn.commit()
    conn.close()

# Function to insert a new customer name into the database
def insert_customer_name(name):
    conn = sqlite3.connect('customer_data.db')
    c = conn.cursor()
    c.execute('''INSERT INTO customers (name) VALUES (?)''', (name,))
    conn.commit()
    conn.close()

# Function to retrieve all customer names from the database
def get_customer_names():
    conn = sqlite3.connect('customer_data.db')
    c = conn.cursor()
    c.execute('''SELECT name FROM customers''')
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

# Function to calculate recoverable amount
def calculate_recoverable_amount(loan_amount, duration, interest_rate, admin_charges):
    # Calculate total interest for the entire loan duration
    total_interest = (loan_amount * (interest_rate / 100)) * duration
    
    # Total loan amount
    total_loan_amount = loan_amount + total_interest + admin_charges
    
    return total_loan_amount

# Function to calculate monthly installment
def calculate_monthly_installment(total_loan_amount, duration):
    # Calculate monthly installment
    monthly_installment = total_loan_amount / duration
    
    return monthly_installment

def main():
    # Create the customer table if it doesn't exist
    create_table()

    # Markdown and Headings
    html_temp = """ 
    <div style="background-color: green; padding: 16px">
    <h2 style="color: gold; text-align: center;">TRUSTED FRIENDS VENTURES LOAN CALCULATOR</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.write('')
    st.write('')

    # Streamlit UI
    st.subheader("Trusted Friends Ventures")

    # Information display
    st.write("""
    OFFICE ADDRESS : Gura Loh-Gyang,
    Behind Abattior Market
    Jos.

    CONTACT : 07054989311, 07068715470, 08036100256, 08142681069

    E-MAIL: trustedfriendsventures@gmail.com
    """)

    st.subheader("MISSION STATEMENT")
    st.write("""
    At Trusted Friends Ventures, our mission is to help our customers optimize their financial situation by providing effective solutions for their short, medium, and long-term goals.
    """)

    st.subheader("VISION STATEMENT")
    st.write("""
    To grow our business by saving capital for investment. To be the client's most trusted business partner in providing clients the best and easiest access to loans.
    """)

    st.subheader("OTHER CONDITIONS")
    st.write("""
    Payments must be made on the due date as agreed. Payments must be in our account with GOWANS MICRO-FINANCE BANK.
    Account Name : TRUSTED FRIENDS VENTURES
    Account Number : 1100123388
    """)

    # Input features
    name = st.text_input("Enter customer's name:")
    loan_amount = st.number_input("Enter loan amount:")
    duration = st.number_input("Enter duration (in months):", min_value=1, step=1, value=12)
    interest_rate = st.number_input("Enter interest rate (in percentage):", min_value=0.0, step=0.01, value=5.0)
    admin_charges = st.number_input("Enter admin charges:", min_value=0.0, step=0.01, value=0.0)

    store_name = st.checkbox("Store this customer's name")

    if store_name and name:
        # Insert the customer name into the database
        insert_customer_name(name)
        st.success(f"Stored customer's name: {name}")

    if st.button("Calculate"):
        # Calculate recoverable amount
        recoverable_amount = calculate_recoverable_amount(loan_amount, duration, interest_rate, admin_charges)

        # Calculate monthly installment
        monthly_installment = calculate_monthly_installment(recoverable_amount, duration)

        # Output
        st.write("\nCustomer's Name:", name)
        st.write("Loan Amount:", loan_amount)
        st.write("Duration (months):", duration)
        st.write("Interest Rate (%):", interest_rate)
        st.write("Admin Charges:", admin_charges)
        st.write("Recoverable Amount:", recoverable_amount)
        st.write("Monthly Installment:", monthly_installment)

    # Display the list of stored customer names in a dropdown
    st.subheader("Select Customer Name")
    selected_customer = st.selectbox("Choose a customer:", options=get_customer_names(), index=0)
    st.write("Selected Customer:", selected_customer)

if __name__ == "__main__":
    main()