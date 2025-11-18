# DBMS-Mini-Project

Pre-owned Vehicle Management System
A full-stack database application for managing a pre-owned car dealership. This system features a MySQL backend with advanced logic (triggers, procedures, functions) and a Streamlit (Python) frontend interface.
It supports Role-Based Access Control (RBAC) for three distinct user types: Admin, Salesperson, and Customer.

📂 Repository Structure

app.py: The main Python application file (Streamlit frontend).
database_setup.sql: The complete SQL script to create the database, tables, data, and all advanced logic (procedures, triggers, etc.).
requirements.txt: List of Python dependencies required to run the app.
credentials.txt: Admin, Salesperson, Customer credentials.
README.md: This file.

🚀 How to Run the Project
Prerequisites
Python 3.7+
MySQL Server (8.0 or higher)

Step 1: Database Setup
Open MySQL Workbench.
Open the file database_setup.sql.
Run the entire script to create the car_dealership database and populate it with sample data.

Step 2: Install Dependencies
Open your terminal/command prompt in the project folder and run:

pip install -r requirements.txt

Step 3: Configure Credentials
Open app.py in a text editor.
Update the YOUR_MYSQL_PASSWORD variable (around line 15) with your local MySQL root password.

Step 4: Launch the App
Run the following command in your terminal:

python -m streamlit run app.py

(Note: Use python3 -m streamlit run app.py on Mac/Linux if needed)

The application will open automatically in your web browser at http://localhost:8501.

🔑 Test Credentials (Login Details)

Use these credentials to test the different user roles and functionalities.

1. Admin
Full system access: Manage users, inventory, view all tables, and access reports.
Username: superadmin
Password: adminpass123

2. Salesperson
Sales operations: Sell cars, buy trade-ins, reserve vehicles.
Username: amit_p
Password: spass1

3. Customer
Browsing: Search inventory, view history, manage profile.
Username: rohan_s
Password: pass1

🛠️ Key Features Implemented
Advanced SQL:
Triggers: LogCarSale (Auto-logging sales), CheckSalePrerequisites (Data validation).
Procedures: SellCar (Transaction logic), SearchAvailableCars (Dynamic filtering), AddCustomer (Atomic inserts).
Functions: GetSalespersonTotalSales (Revenue calculation).

Complex Queries:
JOINs: Used in Sales Reports to combine data from 5 tables.
Nested Queries: Used for Price Analysis.
Aggregations: Used for Revenue Reports.

Frontend:
User-friendly Streamlit interface.
Secure session management.
Dynamic dataframes and metric displays.
