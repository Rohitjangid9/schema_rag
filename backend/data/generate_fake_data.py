import random
import sqlite3
from datetime import datetime, timedelta
from faker import Faker

# Connect to the exact schema definition we just wrote
from randomschemas import SCHEMA_DEFINITION

fake = Faker()
DB_FILE = "erp_data.db"

def connect_db():
    conn = sqlite3.connect(DB_FILE)
    # Enable foreign keys for SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Determine the insertion order to avoid Foreign Key violation errors.
# Tables with fewer/no foreign keys must be created first.
INSERTION_ORDER = [
    "inventory_category",
    "hr_employee", # Moved this up since departments need managers
    "hr_department",
    "crm_customer",
    "crm_interaction",
    "inventory_product",
    "inventory_warehouse",
    "inventory_stock",
    "sales_order",
    "sales_order_item",
    "sales_invoice",
    "logistics_shipment",
    "finance_payment",
    "finance_expense"
]

def generate_records(conn):
    cursor = conn.cursor()
    
    # Store primary keys to populate foreign keys safely
    pks = {table: [] for table in SCHEMA_DEFINITION.keys()}

    def get_fk(table_name):
        """Helper to get a random primary key from an already populated table."""
        if not pks[table_name]:
            return None # Use None instead of a fake ID to avoid hard FK crash
        return random.choice(pks[table_name])

    print("Generating relational data...")

    for table in INSERTION_ORDER:
        print(f"  Populating {table}...")
        
        # Decide how many rows to generate for this table
        num_rows = 50 
        if table in ["inventory_category", "hr_department", "inventory_warehouse"]:
            num_rows = 10
        elif table in ["sales_order_item", "crm_interaction", "inventory_stock", "finance_payment"]:
            num_rows = 150

        for _ in range(num_rows):
            # ---------------- HR ----------------
            if table == "hr_department":
                cursor.execute("INSERT INTO hr_department (name, manager_id) VALUES (?, ?)", 
                               (fake.company_suffix() + " Dept", get_fk("hr_employee") if pks["hr_employee"] else None))
            elif table == "hr_employee":
                cursor.execute("INSERT INTO hr_employee (first_name, last_name, email, department_id, hire_date, salary, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (fake.first_name(), fake.last_name(), fake.company_email(), get_fk("hr_department"), fake.date_between(start_date='-5y', end_date='today').isoformat(), round(random.uniform(40000, 150000), 2), random.choice(['Active', 'Active', 'On Leave'])))
            
            # ---------------- CRM ----------------
            elif table == "crm_customer":
                cursor.execute("INSERT INTO crm_customer (company_name, contact_name, email, phone, industry, account_manager_id) VALUES (?, ?, ?, ?, ?, ?)",
                               (fake.company(), fake.name(), fake.company_email(), fake.phone_number(), fake.job(), get_fk("hr_employee")))
            elif table == "crm_interaction":
                cursor.execute("INSERT INTO crm_interaction (customer_id, employee_id, interaction_type, notes) VALUES (?, ?, ?, ?)",
                               (get_fk("crm_customer"), get_fk("hr_employee"), random.choice(['Call', 'Email', 'Meeting', 'Support Ticket']), fake.sentence()))

            # ---------------- INVENTORY ----------------
            elif table == "inventory_category":
                cursor.execute("INSERT INTO inventory_category (name, description) VALUES (?, ?)",
                               (fake.color_name() + " Supplies", fake.sentence()))
            elif table == "inventory_product":
                cost = round(random.uniform(5, 500), 2)
                cursor.execute("INSERT INTO inventory_product (sku, name, category_id, unit_cost, selling_price, stock_quantity) VALUES (?, ?, ?, ?, ?, ?)",
                               (fake.bothify(text='SKU-####-???'), fake.catch_phrase(), get_fk("inventory_category"), cost, round(cost * 1.5, 2), random.randint(0, 1000)))
            elif table == "inventory_warehouse":
                cursor.execute("INSERT INTO inventory_warehouse (name, location, manager_id) VALUES (?, ?, ?)",
                               (fake.city() + " Hub", fake.address(), get_fk("hr_employee")))
            elif table == "inventory_stock":
                cursor.execute("INSERT INTO inventory_stock (product_id, warehouse_id, quantity, last_restock_date) VALUES (?, ?, ?, ?)",
                               (get_fk("inventory_product"), get_fk("inventory_warehouse"), random.randint(10, 500), fake.date_this_year().isoformat()))

            # ---------------- SALES ----------------
            elif table == "sales_order":
                cursor.execute("INSERT INTO sales_order (ref_code, customer_id, sales_rep_id, order_date, status, total_amount) VALUES (?, ?, ?, ?, ?, ?)",
                               (fake.bothify(text='ORD-####'), get_fk("crm_customer"), get_fk("hr_employee"), fake.date_this_year().isoformat(), random.choice(['Pending', 'Processing', 'Shipped', 'Delivered']), round(random.uniform(100, 5000), 2)))
            elif table == "sales_order_item":
                cursor.execute("INSERT INTO sales_order_item (order_id, product_id, quantity, unit_price, discount) VALUES (?, ?, ?, ?, ?)",
                               (get_fk("sales_order"), get_fk("inventory_product"), random.randint(1, 20), round(random.uniform(10, 500), 2), random.choice([0, 0, 0, 5, 10, 15])))
            elif table == "sales_invoice":
                date = fake.date_this_year().isoformat()
                cursor.execute("INSERT INTO sales_invoice (order_id, customer_id, invoice_date, due_date, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                               (get_fk("sales_order"), get_fk("crm_customer"), date, date, round(random.uniform(100, 5000), 2), random.choice(['Paid', 'Paid', 'Pending', 'Overdue'])))

            # ---------------- LOGISTICS ----------------
            elif table == "logistics_shipment":
                cursor.execute("INSERT INTO logistics_shipment (order_id, warehouse_id, carrier, tracking_number, shipment_date, estimated_delivery, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (get_fk("sales_order"), get_fk("inventory_warehouse"), random.choice(['FedEx', 'UPS', 'DHL', 'USPS']), fake.bothify(text='TRK##########'), fake.date_this_year().isoformat(), fake.date_this_year().isoformat(), random.choice(['In Transit', 'Delivered', 'Pending'])))

            # ---------------- FINANCE ----------------
            elif table == "finance_payment":
                cursor.execute("INSERT INTO finance_payment (invoice_id, customer_id, payment_date, amount, payment_method, status) VALUES (?, ?, ?, ?, ?, ?)",
                               (get_fk("sales_invoice"), get_fk("crm_customer"), fake.date_this_year().isoformat(), round(random.uniform(100, 5000), 2), random.choice(['Credit Card', 'Bank Transfer', 'PayPal', 'Check']), 'Completed'))
            elif table == "finance_expense":
                cursor.execute("INSERT INTO finance_expense (employee_id, department_id, expense_date, amount, category, description, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (get_fk("hr_employee"), get_fk("hr_department"), fake.date_this_year().isoformat(), round(random.uniform(10, 1000), 2), random.choice(['Travel', 'Meals', 'Office Supplies', 'Software']), fake.sentence(), random.choice(['Approved', 'Pending', 'Rejected'])))

            pks[table].append(cursor.lastrowid)
        
        conn.commit()
    
    print("Successfully populated realistic DB.")

if __name__ == "__main__":
    import os
    
    # Initialize DB schema first
    print("Setting up fresh database via erp_schema_dump.sql...")
    
    # Start fresh by deleting old DB if it exists to avoid locking/conflicts
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = connect_db()
    
    if os.path.exists('erp_schema_dump.sql'):
        with open('erp_schema_dump.sql', 'r') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
    else:
        print("ERROR: erp_schema_dump.sql not found! Please run randomschemas.py first.")
        exit(1)

    try:
        generate_records(conn)
    except sqlite3.IntegrityError as e:
        print(f"FATAL Integrity Error: {e}")
        conn.rollback()
    
    conn.close()

