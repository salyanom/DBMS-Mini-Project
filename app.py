import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Car Dealership System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

YOUR_MYSQL_PASSWORD = "mysqlOm14@"

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background-color: #2196F3;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1976D2;
    }
    /* Style for Delete button to be red */
    div[data-testid*="stButton"] > button[kind="primary"] {
        background-color: #f44336;
        color: white;
        border: none;
    }
    div[data-testid*="stButton"] > button[kind="primary"]:hover {
        background-color: #d32f2f;
        color: white;
    }
    h1, h2, h3 {
        color: #2196F3;
    }
    .stDataFrame {
        background-color: #1e1e1e;
    }
    .stRadio > label {
        padding: 8px 0px;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection function
def get_db_connection():
    """Create and return a database connection."""
    if not YOUR_MYSQL_PASSWORD:
        st.error("DATABASE PASSWORD IS NOT SET. Please edit the streamlit_app.py file and set 'YOUR_MYSQL_PASSWORD'.")
        return None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=YOUR_MYSQL_PASSWORD,
            database="car_dealership"
        )
        return connection
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None

#initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None
    st.session_state.username = None

def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None
    st.session_state.username = None
    st.rerun()

def login_signup_page():
    st.title("🚗 Car Dealership System")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Signup"])
    
    with tab1:
        st.subheader("Login to Your Account")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form(key="login_form"):
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                submit_login = st.form_submit_button("🔐 Login", use_container_width=True)
            
            if submit_login:
                if username and password:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        
                        cursor.execute("SELECT customer_id FROM Customer WHERE username=%s AND passw=%s", (username, password))
                        customer = cursor.fetchone()
                        if customer:
                            st.session_state.logged_in = True
                            st.session_state.user_type = "customer"
                            st.session_state.user_id = customer[0]
                            st.session_state.username = username
                            st.success("Login successful!")
                            st.rerun()
                        
                        cursor.execute("SELECT salesperson_id FROM Salesperson WHERE username=%s AND passw=%s", (username, password))
                        salesperson = cursor.fetchone()
                        if salesperson:
                            st.session_state.logged_in = True
                            st.session_state.user_type = "salesperson"
                            st.session_state.user_id = salesperson[0]
                            st.session_state.username = username
                            st.success("Login successful!")
                            st.rerun()
                        
                        cursor.execute("SELECT admin_id FROM Admin WHERE username=%s AND passw=%s", (username, password))
                        admin = cursor.fetchone()
                        if admin:
                            st.session_state.logged_in = True
                            st.session_state.user_type = "admin"
                            st.session_state.user_id = admin[0]
                            st.session_state.username = username
                            st.success("Login successful!")
                            st.rerun()
                        
                        if not (customer or salesperson or admin):
                            st.error("Invalid username or password!")
                        
                        connection.close()
                else:
                    st.warning("Please enter both username and password!")
    
    with tab2:
        st.subheader("Create New Customer Account")
        st.info("This calls the `AddCustomer` stored procedure.")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form(key="signup_form"):
                first_name = st.text_input("First Name", key="signup_fname")
                last_name = st.text_input("Last Name", key="signup_lname")
                new_username = st.text_input("Username", key="signup_username")
                new_password = st.text_input("Password", type="password", key="signup_password")
                phone = st.text_input("Phone Number", key="signup_phone")
                email = st.text_input("Email", key="signup_email")
                submit_signup = st.form_submit_button("✨ Create Account", use_container_width=True)
            
            if submit_signup:
                if all([first_name, last_name, new_username, new_password, phone, email]):
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            # Calls the new procedure we will add
                            cursor.callproc('AddCustomer', 
                                (first_name, last_name, new_username, new_password, phone, email))
                            connection.commit()
                            st.success("Account created successfully! Please login.")
                        except Error as e:
                            st.error(f"Database Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.warning("Please fill in all fields!")

def customer_dashboard():
    st.title(f"👤 Customer Dashboard")
    st.markdown(f"**Welcome, {st.session_state.username}!** (ID: {st.session_state.user_id})")
    st.markdown("---")
    
    with st.sidebar:
        st.header("Navigation")
        st.markdown("---")
        page = st.radio("Go to", [
            "🚗 View Available Cars",
            "📞 Manage Phone Numbers",
            "📧 Manage Emails",
            "👤 Update Profile",
            "🔐 Change Password"
        ], label_visibility="collapsed")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    if page == "🚗 View Available Cars":
        st.subheader("Available Cars")
        st.info("This calls the `SearchAvailableCars` procedure.")
        
        manufacturers_list = [""]
        models_list = [""]
        
        connection = get_db_connection()
        if connection:
            try:
                df_m = pd.read_sql("SELECT name FROM Manufacturer ORDER BY name", connection)
                manufacturers_list.extend(df_m['name'].tolist())
                
                df_mod = pd.read_sql("SELECT name FROM Model ORDER BY name", connection)
                models_list.extend(df_mod['name'].unique().tolist())
            except Error as e:
                st.warning(f"Could not load filters: {e}")
            finally:
                connection.close()

        col1, col2, col3 = st.columns(3)
        with col1:
            mf_name_in = st.selectbox("Manufacturer", options=manufacturers_list)
        with col2:
            model_name_in = st.selectbox("Model", options=models_list)
        with col3:
            max_price_in = st.number_input("Max Price", min_value=0, value=0, step=100000)

        mf_name_val = mf_name_in if mf_name_in else None
        model_name_val = model_name_in if model_name_in else None
        max_price_val = max_price_in if max_price_in > 0 else None

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.callproc('SearchAvailableCars', (max_price_val, mf_name_val, model_name_val))
                
                results = []
                for result in cursor.stored_results():
                    results.extend(result.fetchall())
                
                if results:
                    df = pd.DataFrame(results)
                    df = df[['Manufacturer', 'Model', 'Year', 'Colour', 'Mileage', 'Price']]
                    st.dataframe(df, use_container_width=True, height=400)
                else:
                    st.info("No cars match your search criteria.")
                    
            except Error as e:
                st.error(f"Error loading cars: {e}")
            finally:
                connection.close()
    
    elif page == "📞 Manage Phone Numbers":
        st.subheader("Manage Phone Numbers")
        
        tab1, tab2, tab3 = st.tabs(["Add Phone", "Update Phone", "Update via Procedure"])
        
        with tab1:
            new_phone = st.text_input("Enter new phone number")
            if st.button("Add Phone Number", key="add_phone"):
                if new_phone:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            cursor.execute(
                                "INSERT INTO CustomerPhone (customer_id, phone) VALUES (%s, %s)",
                                (st.session_state.user_id, new_phone)
                            )
                            connection.commit()
                            st.success("Phone number added successfully!")
                        except Error as e:
                            st.error(f"Database Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.warning("Please enter a phone number!")
        
        with tab2:
            old_phone = st.text_input("Phone number to replace")
            new_phone_update = st.text_input("New phone number", key="update_phone_new")
            if st.button("Update Phone Number", key="update_phone"):
                if new_phone_update and old_phone:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            cursor.execute(
                                "UPDATE CustomerPhone SET phone = %s WHERE customer_id = %s AND phone = %s",
                                (new_phone_update, st.session_state.user_id, old_phone)
                            )
                            connection.commit()
                            if cursor.rowcount > 0:
                                st.success("Phone number updated successfully!")
                            else:
                                st.warning("Old phone number not found!")
                        except Error as e:
                            st.error(f"Database Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.warning("Please enter both old and new phone numbers!")
        
        with tab3:
            st.info("📋 Use `UpdateCustomerInfo` Procedure")
            update_phone_proc = st.text_input("New Phone (leave empty to skip)", key="proc_phone")
            update_email_proc = st.text_input("New Email (leave empty to skip)", key="proc_email")
            
            if st.button("Update via Procedure", key="update_customer_info"):
                phone_val = update_phone_proc if update_phone_proc else None
                email_val = update_email_proc if update_email_proc else None
                
                if phone_val or email_val:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            cursor.callproc('UpdateCustomerInfo', 
                                (st.session_state.user_id, email_val, phone_val))
                            connection.commit()
                            st.success("Customer info updated via procedure!")
                        except Error as e:
                            st.error(f"Database Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.warning("Please enter at least phone or email!")
    
    elif page == "📧 Manage Emails":
        st.subheader("Manage Email Addresses")
        
        tab1, tab2 = st.tabs(["Add Email", "Update Email"])
        
        with tab1:
            new_email = st.text_input("Enter new email address")
            if st.button("Add Email", key="add_email"):
                if new_email:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            cursor.execute(
                                "INSERT INTO CustomerEmail (customer_id, email) VALUES (%s, %s)",
                                (st.session_state.user_id, new_email)
                            )
                            connection.commit()
                            st.success("Email added successfully!")
                        except Error as e:
                            st.error(f"Database Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.warning("Please enter an email address!")
        
        with tab2:
            old_email = st.text_input("Email address to replace")
            new_email_update = st.text_input("New email address", key="update_email_new")
            if st.button("Update Email", key="update_email"):
                if new_email_update and old_email:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            cursor.execute(
                                "UPDATE CustomerEmail SET email = %s WHERE customer_id = %s AND email = %s",
                                (new_email_update, st.session_state.user_id, old_email)
                            )
                            connection.commit()
                            if cursor.rowcount > 0:
                                st.success("Email updated successfully!")
                            else:
                                st.warning("Old email address not found!")
                        except Error as e:
                            st.error(f"Database Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.warning("Please enter both old and new email addresses!")
    
    elif page == "👤 Update Profile":
        st.subheader("Update Username")
        new_username = st.text_input("Enter new username")
        if st.button("Update Username", key="update_username"):
            if new_username:
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.execute(
                            "UPDATE Customer SET username = %s WHERE customer_id = %s",
                            (new_username, st.session_state.user_id)
                        )
                        connection.commit()
                        st.session_state.username = new_username
                        st.success("Username updated successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")
                    finally:
                        connection.close()
            else:
                st.error("Please enter a username!")
    
    elif page == "🔐 Change Password":
        st.subheader("Change Password")
        new_password = st.text_input("Enter new password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        if st.button("Update Password", key="update_password"):
            if new_password and confirm_password:
                if new_password == confirm_password:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            cursor.execute(
                                "UPDATE Customer SET passw = %s WHERE customer_id = %s",
                                (new_password, st.session_state.user_id)
                            )
                            connection.commit()
                            st.success("Password updated successfully!")
                        except Error as e:
                            st.error(f"Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.error("Passwords do not match!")
            else:
                st.error("Please enter both password fields!")

def salesperson_dashboard():
    st.title(f"💼 Salesperson Dashboard")
    st.markdown(f"**Welcome, {st.session_state.username}!** (ID: {st.session_state.user_id})")
    st.markdown("---")
    
    with st.sidebar:
        st.header("Navigation")
        st.markdown("---")
        page = st.radio("Go to", [
            "🚗 View Available Cars",
            "💰 Sell Car to Customer",
            "🛒 Buy Car from Customer",
            "📅 Reserve Car",
            "📞 Manage Phone Numbers",
            "📧 Manage Emails",
            "👤 Update Profile",
            "🔧 Update Profile (Procedure)",
            "🔐 Change Password"
        ], label_visibility="collapsed")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    if page == "🚗 View Available Cars":
        st.subheader("Available Cars")
        st.info("This calls the `SearchAvailableCars` procedure.")
        
        manufacturers_list = [""]
        models_list = [""]
        
        connection = get_db_connection()
        if connection:
            try:
                df_m = pd.read_sql("SELECT name FROM Manufacturer ORDER BY name", connection)
                manufacturers_list.extend(df_m['name'].tolist())
                
                df_mod = pd.read_sql("SELECT name FROM Model ORDER BY name", connection)
                models_list.extend(df_mod['name'].unique().tolist())
            except Error as e:
                st.warning(f"Could not load filters: {e}")
            finally:
                connection.close()

        col1, col2, col3 = st.columns(3)
        with col1:
            mf_name_in = st.selectbox("Manufacturer", options=manufacturers_list)
        with col2:
            model_name_in = st.selectbox("Model", options=models_list)
        with col3:
            max_price_in = st.number_input("Max Price", min_value=0, value=0, step=100000)

        mf_name_val = mf_name_in if mf_name_in else None
        model_name_val = model_name_in if model_name_in else None
        max_price_val = max_price_in if max_price_in > 0 else None

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.callproc('SearchAvailableCars', (max_price_val, mf_name_val, model_name_val))
                
                results = []
                for result in cursor.stored_results():
                    results.extend(result.fetchall())
                
                if results:
                    df = pd.DataFrame(results)
                    df = df[['Manufacturer', 'Model', 'Year', 'Colour', 'Mileage', 'Price']]
                    st.dataframe(df, use_container_width=True, height=400)
                else:
                    st.info("No cars match your search criteria.")
                    
            except Error as e:
                st.error(f"Error loading cars: {e}")
            finally:
                connection.close()
    
    elif page == "💰 Sell Car to Customer":
        st.subheader("Sell Car to Customer")
        st.info("This calls your `SellCar` procedure. Your `LogCarSale` and `CheckSalePrerequisites` triggers will run automatically.")
        
        col1, col2 = st.columns(2)
        with col1:
            car_id = st.number_input("Car ID", min_value=1, step=1)
        with col2:
            customer_id = st.number_input("Customer ID", min_value=1, step=1)
        
        if st.button("💰 Sell Car", use_container_width=True):
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.callproc('SellCar', 
                        (car_id, customer_id, st.session_state.user_id))
                    
                    result_msg = ""
                    for result in cursor.stored_results():
                        msg = result.fetchone()
                        if msg:
                            result_msg = msg[0]

                    connection.commit()
                    st.success(result_msg)
                except Error as e:
                    connection.rollback()
                    st.error(f"Database Error: {e}") 
                finally:
                    connection.close()
    
    elif page == "🛒 Buy Car from Customer":
        st.subheader("Buy Car from Customer")
        st.info("This calls the `SellCarToDealership` procedure.")
        
        col1, col2 = st.columns(2)
        with col1:
            customer_id = st.number_input("Customer ID", min_value=1, step=1, key="buy_customer_id")
            model_id = st.number_input("Model ID", min_value=1, step=1)
            year = st.number_input("Year", min_value=1900, max_value=2025, step=1)
        with col2:
            mileage = st.number_input("Mileage", min_value=0, step=100)
            colour = st.text_input("Colour") # <-- FIXED
            price = st.number_input("Purchase Price", min_value=0.0, step=100.0)
        
        if st.button("🛒 Buy Car", use_container_width=True):
            if colour:
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.callproc('SellCarToDealership', 
                            (customer_id, model_id, year, mileage, colour, price, st.session_state.user_id))
                        connection.commit()
                        st.success("Car purchased from customer successfully!")
                    except Error as e:
                        connection.rollback()
                        st.error(f"Database Error: {e}")
                    finally:
                        connection.close()
            else:
                st.error("Please enter the car colour!")
    
    elif page == "📅 Reserve Car":
        st.subheader("Reserve Car for Customer")
        st.info("This calls the `ReserveCarForCustomer` procedure.")
        
        col1, col2 = st.columns(2)
        with col1:
            car_id_reserve = st.number_input("Car ID", min_value=1, step=1, key="reserve_car_id")
        with col2:
            customer_id_reserve = st.number_input("Customer ID", min_value=1, step=1, key="reserve_customer_id")
        
        if st.button("📅 Reserve Car", use_container_width=True):
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.callproc('ReserveCarForCustomer', (car_id_reserve, customer_id_reserve))
                    connection.commit()
                    st.success("Car reserved successfully!")
                except Error as e:
                    connection.rollback()
                    st.error(f"Database Error: {e}")
                finally:
                    connection.close()
    
    elif page == "📞 Manage Phone Numbers":
        st.subheader("Manage Phone Numbers")
        
        new_phone = st.text_input("Enter phone number")
        if st.button("Add Phone", key="sales_phone"):
            if new_phone:
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO SalespersonPhone (salesperson_id, phone) VALUES (%s, %s)",
                            (st.session_state.user_id, new_phone)
                        )
                        connection.commit()
                        st.success("Phone number added successfully!")
                    except Error as e:
                        st.error(f"Database Error: {e}")
                    finally:
                        connection.close()
            else:
                st.warning("Please enter a phone number!")
    
    elif page == "📧 Manage Emails":
        st.subheader("Manage Email Address")
        
        new_email = st.text_input("Enter email address")
        if st.button("Add Email", key="sales_email"):
            if new_email:
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO SalespersonEmail (salesperson_id, email) VALUES (%s, %s)",
                            (st.session_state.user_id, new_email)
                        )
                        connection.commit()
                        st.success("Email added successfully!")
                    except Error as e:
                        st.error(f"Database Error: {e}")
                    finally:
                        connection.close()
            else:
                st.warning("Please enter an email address!")
    
    elif page == "👤 Update Profile":
        st.subheader("Update Username")
        new_username = st.text_input("Enter new username")
        if st.button("Update Username", key="sales_update_username"):
            if new_username:
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.execute(
                            "UPDATE Salesperson SET username = %s WHERE salesperson_id = %s",
                            (new_username, st.session_state.user_id)
                        )
                        connection.commit()
                        st.session_state.username = new_username
                        st.success("Username updated successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")
                    finally:
                        connection.close()
            else:
                st.error("Please enter a valid username!")
    
    elif page == "🔧 Update Profile (Procedure)":
        st.subheader("Update Salesperson Profile via Procedure")
        st.info("📋 Uses `UpdateSalesperson` stored procedure to update all details at once")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", key="update_fname")
            last_name = st.text_input("Last Name", key="update_lname")
            hire_date = st.date_input("Hire Date", key="update_hire_date", value=datetime.today())
            username = st.text_input("Username", key="update_username_proc")
        with col2:
            password = st.text_input("Password", type="password", key="update_password_proc")
            phone = st.text_input("Phone", key="update_phone_proc")
            email = st.text_input("Email", key="update_email_proc")
        
        if st.button("🔧 Update All via Procedure", use_container_width=True):
            if all([first_name, last_name, username, password, phone, email]):
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.callproc('UpdateSalesperson', 
                            (st.session_state.user_id, first_name, last_name, 
                             hire_date.strftime('%Y-%m-%d'), username, password, phone, email))
                        connection.commit()
                        st.session_state.username = username
                        st.success("Salesperson profile updated successfully via procedure!")
                    except Error as e:
                        st.error(f"Database Error: {e}")
                    finally:
                        connection.close()
            else:
                st.error("Please fill in all fields!")
    
    elif page == "🔐 Change Password":
        st.subheader("Change Password")
        new_password = st.text_input("Enter new password", type="password", key="sales_new_pass")
        confirm_password = st.text_input("Confirm new password", type="password", key="sales_confirm_pass")
        if st.button("Update Password", key="sales_update_password"):
            if new_password and confirm_password:
                if new_password == confirm_password:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            cursor.execute(
                                "UPDATE Salesperson SET passw = %s WHERE salesperson_id = %s",
                                (new_password, st.session_state.user_id)
                            )
                            connection.commit()
                            st.success("Password updated successfully!")
                        except Error as e:
                            st.error(f"Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.error("Passwords do not match!")
            else:
                st.error("Please enter both password fields!")

def admin_dashboard():
    st.title(f"⚙️ Admin Dashboard")
    st.markdown(f"**Welcome, {st.session_state.username}!** (ID: {st.session_state.user_id})")
    st.markdown("---")
    
    with st.sidebar:
        st.header("Navigation")
        st.markdown("---")
        page = st.radio("Go to", [
            "📊 View Tables",
            "👥 Manage Customers",
            "💼 Manage Salespersons",
            "🚗 Manage Cars",
            "🏭 Manage Manufacturers",
            "🚙 Manage Models",
            "📈 Sales Reports",
            "💰 Revenue Reports",
            "💡 Price Analysis (Nested Query)" 
        ], label_visibility="collapsed")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    if page == "📊 View Tables":
        st.subheader("View Database Tables")
        table_name = st.selectbox("Select Table", [
            "Customer", "Salesperson", "Admin", "Car", "Model", "Manufacturer",
            "CustomerPhone", "CustomerEmail", "SalespersonPhone", "SalespersonEmail", "SalesLog"
        ])
        
        if st.button("Load Table Data"):
            connection = get_db_connection()
            if connection:
                df = pd.read_sql(f"SELECT * FROM {table_name}", connection)
                st.dataframe(df, use_container_width=True)
                connection.close()
    
    elif page == "👥 Manage Customers":
        st.subheader("Add New Customer")
        st.info("This calls the `AddCustomer` procedure.")
        
        col1, col2 = st.columns(2)
        with col1:
            fname = st.text_input("First Name")
            lname = st.text_input("Last Name")
            username = st.text_input("Username")
        with col2:
            password = st.text_input("Password", type="password")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
        
        if st.button("Add Customer", use_container_width=True):
            if all([fname, lname, username, password, phone, email]):
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.callproc('AddCustomer', (fname, lname, username, password, phone, email))
                        connection.commit()
                        st.success("Customer added successfully!")
                    except Error as e:
                        st.error(f"Database Error: {e}")
                    finally:
                        connection.close()
            else:
                st.error("Please fill in all fields!")
    
    elif page == "💼 Manage Salespersons":
        st.subheader("Add New Salesperson")
        st.info("This calls the `AddSalesperson` procedure.")
        
        col1, col2 = st.columns(2)
        with col1:
            fname = st.text_input("First Name", key="sales_fname")
            lname = st.text_input("Last Name", key="sales_lname")
            username = st.text_input("Username", key="sales_username")
            hire_date = st.date_input("Hire Date", value=datetime.today())
        with col2:
            password = st.text_input("Password", type="password", key="sales_password")
            phone = st.text_input("Phone", key="sales_phone")
            email = st.text_input("Email", key="sales_email")
        
        if st.button("Add Salesperson", use_container_width=True):
            if all([fname, lname, username, password, phone, email]):
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.callproc('AddSalesperson', 
                            (fname, lname, hire_date.strftime('%Y-%m-%d'), username, password, phone, email))
                        connection.commit()
                        st.success("Salesperson added successfully!")
                    except Error as e:
                        st.error(f"Database Error: {e}")
                    finally:
                        connection.close()
            else:
                st.error("Please fill in all fields!")
    
    elif page == "🚗 Manage Cars":
        st.subheader("Manage Car Inventory")

        tab1, tab2 = st.tabs(["Add Car", "Delete Car"]) 

        with tab1:
            st.info("Add a new car to the dealership's inventory.")
            col1, col2 = st.columns(2)
            with col1:
                model_id = st.number_input("Model ID", min_value=1, step=1)
                year = st.number_input("Year", min_value=1900, max_value=2025, step=1)
                mileage = st.number_input("Mileage", min_value=0, step=100)
                colour = st.text_input("Colour") 
            with col2:
                price = st.number_input("Price", min_value=0.0, step=100.0)
                status = st.selectbox("Status", ["Available", "Sold", "Reserved"])
                customer_id = st.number_input("Customer ID (if Sold/Reserved)", min_value=0, step=1)
                salesperson_id = st.number_input("Salesperson ID (if Sold)", min_value=0, step=1)
            
            if st.button("Add Car", use_container_width=True):
                if colour and price > 0:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            cust_id = customer_id if customer_id > 0 else None
                            sales_id = salesperson_id if salesperson_id > 0 else None
                            
                            query = """
                                INSERT INTO Car (model_id, year, mileage, colour, price, customer_id, salesperson_id, status) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """ 
                            params = (model_id, year, mileage, colour, price, cust_id, sales_id, status)
                            
                            cursor.execute(query, params)
                            connection.commit()
                            st.success("Car added successfully!")
                        except Error as e:
                            st.error(f"Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.error("Please enter at least the Colour and Price!")

        with tab2:
            st.info("Permanently delete a car from the database. This will also delete its sales log entries.")
            st.warning("This action is irreversible.")
            del_car_id = st.number_input("Enter Car ID to Delete", min_value=1, step=1)
            
            if st.button("Delete Car", use_container_width=True, type="primary"):
                if del_car_id > 0:
                    connection = get_db_connection()
                    if connection:
                        cursor = connection.cursor()
                        try:
                            cursor.callproc('DeleteCar', (del_car_id,))
                            connection.commit()
                            st.success(f"Car ID {del_car_id} deleted successfully.")
                        except Error as e:
                            st.error(f"Error: {e}")
                        finally:
                            connection.close()
                else:
                    st.warning("Please enter a valid Car ID.")

    
    elif page == "🏭 Manage Manufacturers":
        st.subheader("Add New Manufacturer")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Manufacturer Name")
        with col2:
            country = st.text_input("Country")
        
        if st.button("Add Manufacturer", use_container_width=True):
            if name and country:
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO Manufacturer (name, country) VALUES (%s, %s)",
                            (name, country)
                        )
                        connection.commit()
                        st.success("Manufacturer added successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")
                    finally:
                        connection.close()
            else:
                st.error("Please fill in all fields!")
    
    elif page == "🚙 Manage Models":
        st.subheader("Add New Model")
        
        col1, col2 = st.columns(2)
        with col1:
            manufacturer_id = st.number_input("Manufacturer ID", min_value=1, step=1)
        with col2:
            model_name = st.text_input("Model Name")
        
        if st.button("Add Model", use_container_width=True):
            if model_name:
                connection = get_db_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO Model (manufacturer_id, name) VALUES (%s, %s)",
                            (manufacturer_id, model_name)
                        )
                        connection.commit()
                        st.success("Model added successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")
                    finally:
                        connection.close()
            else:
                st.error("Please enter the model name!")
    
    elif page == "📈 Sales Reports":
        st.subheader("Sales Data (Join Query)")
        st.info("This view joins Car, Customer, Salesperson, Model, and Manufacturer tables.")
        connection = get_db_connection()
        if connection:
            query = """
                SELECT 
                    Car.car_id,
                    CONCAT(Customer.first_name, ' ', Customer.last_name) AS Customer,
                    CONCAT(Salesperson.first_name, ' ', Salesperson.last_name) AS Salesperson,
                    Manufacturer.name AS Manufacturer,
                    Model.name AS Model,
                    Car.price,
                    Car.status
                FROM Car
                LEFT JOIN Customer ON Car.customer_id = Customer.customer_id
                LEFT JOIN Salesperson ON Car.salesperson_id = Salesperson.salesperson_id
                LEFT JOIN Model ON Car.model_id = Model.model_id
                LEFT JOIN Manufacturer ON Model.manufacturer_id = Manufacturer.manufacturer_id
                WHERE Car.status = 'Sold'
            """ 
            df = pd.read_sql(query, connection)
            st.dataframe(df, use_container_width=True)
            
            if not df.empty:
                st.metric("Total Sales Revenue", f"₹{df['price'].sum():,.2f}")
            
            connection.close()
    
    elif page == "💰 Revenue Reports":
        st.subheader("Salesperson Revenue (Aggregate Function)")
        st.info("This calls your `GetSalespersonTotalSales` and `GetTotalCarsSold` functions.")
        
        salesperson_id = st.number_input("Enter Salesperson ID", min_value=1, step=1)
        
        if st.button("Get Revenue", use_container_width=True):
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("SELECT GetSalespersonTotalSales(%s)", (salesperson_id,))
                    revenue = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT GetTotalCarsSold(%s)", (salesperson_id,))
                    cars_sold = cursor.fetchone()[0]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Revenue", f"₹{revenue or 0:,.2f}")
                    with col2:
                        st.metric("Total Cars Sold", cars_sold or 0)
                    
                except Error as e:
                    st.error(f"Error: {e}")
                finally:
                    connection.close()

    elif page == "💡 Price Analysis (Nested Query)": 
        st.subheader("Price Analysis: High-Value Cars")
        st.info("This demonstrates a **Nested Query**. It finds all cars priced **higher than the average price** of all cars.")
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT AVG(price) FROM Car")
                avg_price = cursor.fetchone()[0]
                st.metric("Average Car Price", f"₹{avg_price:,.2f}")

                query = """
                    SELECT 
                        c.car_id,
                        m.name AS Model,
                        c.year,
                        c.price
                    FROM Car c
                    JOIN Model m ON c.model_id = m.model_id
                    WHERE c.price > (SELECT AVG(price) FROM Car)
                    ORDER BY c.price DESC;
                """
                df = pd.read_sql(query, connection)
                st.dataframe(df, use_container_width=True)
                
            except Error as e:
                st.error(f"Error: {e}")
            finally:
                connection.close()

def main():
    if not st.session_state.logged_in:
        login_signup_page()
    else:
        if st.session_state.user_type == "customer":
            customer_dashboard()
        elif st.session_state.user_type == "salesperson":
            salesperson_dashboard()
        elif st.session_state.user_type == "admin":
            admin_dashboard()

if __name__ == "__main__":
    if YOUR_MYSQL_PASSWORD == "":
        st.error("DATABASE PASSWORD IS NOT SET. Please edit the `streamlit_app.py` file and set 'YOUR_MYSQL_PASSWORD' on line 17.")
    main()