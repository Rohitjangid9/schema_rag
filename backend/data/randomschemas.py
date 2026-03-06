import json

# --- REALISTIC ERP SCHEMA DEFINITION ---
SCHEMA_DEFINITION = {
    # ------------------- HR MODULE -------------------
    "hr_employee": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "first_name VARCHAR(50)",
            "last_name VARCHAR(50)",
            "email VARCHAR(100)",
            "department_id INT",
            "hire_date DATE",
            "salary DECIMAL(10,2)",
            "status VARCHAR(20)"
        ],
        "foreign_keys": [
            "FOREIGN KEY (department_id) REFERENCES hr_department(id)"
        ],
        "description": "Stores employee personnel records."
    },
    "hr_department": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name VARCHAR(100)",
            "manager_id INT"
        ],
        "foreign_keys": [
            "FOREIGN KEY (manager_id) REFERENCES hr_employee(id)"
        ],
        "description": "Stores company departments."
    },

    # ------------------- CRM MODULE -------------------
    "crm_customer": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "company_name VARCHAR(150)",
            "contact_name VARCHAR(100)",
            "email VARCHAR(100)",
            "phone VARCHAR(50)",
            "industry VARCHAR(50)",
            "account_manager_id INT",
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ],
        "foreign_keys": [
            "FOREIGN KEY (account_manager_id) REFERENCES hr_employee(id)"
        ],
        "description": "Stores client and customer accounts."
    },
    "crm_interaction": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "customer_id INT",
            "employee_id INT",
            "interaction_type VARCHAR(50)",
            "interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "notes TEXT"
        ],
        "foreign_keys": [
            "FOREIGN KEY (customer_id) REFERENCES crm_customer(id)",
            "FOREIGN KEY (employee_id) REFERENCES hr_employee(id)"
        ],
        "description": "Logs calls, emails, and meetings with customers."
    },

    # ------------------- SALES MODULE -------------------
    "sales_order": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "ref_code VARCHAR(20)",
            "customer_id INT",
            "sales_rep_id INT",
            "order_date DATE",
            "status VARCHAR(20)",
            "total_amount DECIMAL(10,2)"
        ],
        "foreign_keys": [
            "FOREIGN KEY (customer_id) REFERENCES crm_customer(id)",
            "FOREIGN KEY (sales_rep_id) REFERENCES hr_employee(id)"
        ],
        "description": "Stores created sales orders."
    },
    "sales_order_item": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "order_id INT",
            "product_id INT",
            "quantity INT",
            "unit_price DECIMAL(10,2)",
            "discount DECIMAL(5,2)"
        ],
        "foreign_keys": [
            "FOREIGN KEY (order_id) REFERENCES sales_order(id)",
            "FOREIGN KEY (product_id) REFERENCES inventory_product(id)"
        ],
        "description": "Stores individual line items of a sales order."
    },
    "sales_invoice": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "order_id INT",
            "customer_id INT",
            "invoice_date DATE",
            "due_date DATE",
            "amount DECIMAL(10,2)",
            "status VARCHAR(20)"
        ],
        "foreign_keys": [
            "FOREIGN KEY (order_id) REFERENCES sales_order(id)",
            "FOREIGN KEY (customer_id) REFERENCES crm_customer(id)"
        ],
        "description": "Stores finalized invoices sent to customers."
    },

    # ------------------- INVENTORY MODULE -------------------
    "inventory_product": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "sku VARCHAR(50)",
            "name VARCHAR(150)",
            "category_id INT",
            "unit_cost DECIMAL(10,2)",
            "selling_price DECIMAL(10,2)",
            "stock_quantity INT"
        ],
        "foreign_keys": [
            "FOREIGN KEY (category_id) REFERENCES inventory_category(id)"
        ],
        "description": "Stores master product details."
    },
    "inventory_category": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name VARCHAR(100)",
            "description TEXT"
        ],
        "foreign_keys": [],
        "description": "Stores product categories."
    },
    "inventory_warehouse": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "name VARCHAR(100)",
            "location VARCHAR(200)",
            "manager_id INT"
        ],
        "foreign_keys": [
            "FOREIGN KEY (manager_id) REFERENCES hr_employee(id)"
        ],
        "description": "Stores physical warehouse locations."
    },
    "inventory_stock": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "product_id INT",
            "warehouse_id INT",
            "quantity INT",
            "last_restock_date DATE"
        ],
        "foreign_keys": [
            "FOREIGN KEY (product_id) REFERENCES inventory_product(id)",
            "FOREIGN KEY (warehouse_id) REFERENCES inventory_warehouse(id)"
        ],
        "description": "Tracks exact stock levels per warehouse."
    },

    # ------------------- LOGISTICS MODULE -------------------
    "logistics_shipment": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "order_id INT",
            "warehouse_id INT",
            "carrier VARCHAR(100)",
            "tracking_number VARCHAR(100)",
            "shipment_date DATE",
            "estimated_delivery DATE",
            "status VARCHAR(20)"
        ],
        "foreign_keys": [
            "FOREIGN KEY (order_id) REFERENCES sales_order(id)",
            "FOREIGN KEY (warehouse_id) REFERENCES inventory_warehouse(id)"
        ],
        "description": "Tracks outbound shipments for sales orders."
    },

    # ------------------- FINANCE MODULE -------------------
    "finance_payment": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "invoice_id INT",
            "customer_id INT",
            "payment_date DATE",
            "amount DECIMAL(10,2)",
            "payment_method VARCHAR(50)",
            "status VARCHAR(20)"
        ],
        "foreign_keys": [
            "FOREIGN KEY (invoice_id) REFERENCES sales_invoice(id)",
            "FOREIGN KEY (customer_id) REFERENCES crm_customer(id)"
        ],
        "description": "Logs financial payments received."
    },
    "finance_expense": {
        "columns": [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "employee_id INT",
            "department_id INT",
            "expense_date DATE",
            "amount DECIMAL(10,2)",
            "category VARCHAR(50)",
            "description TEXT",
            "status VARCHAR(20)"
        ],
        "foreign_keys": [
            "FOREIGN KEY (employee_id) REFERENCES hr_employee(id)",
            "FOREIGN KEY (department_id) REFERENCES hr_department(id)"
        ],
        "description": "Tracks internal company expenses."
    }
}

# --- GENERATION ---
table_summaries = {}

sql_statements = []
for index, (table_name, details) in enumerate(SCHEMA_DEFINITION.items()):
    cols_str = ",\n    ".join(details["columns"])
    if details["foreign_keys"]:
        fk_str = ",\n    " + ",\n    ".join(details["foreign_keys"])
    else:
        fk_str = ""
    
    table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {cols_str}{fk_str}\n);"
    sql_statements.append(table_sql)
    
    # Generate simplified metadata mappings for downstream use
    table_summaries[table_name] = details["description"]

final_script = "\n\n".join(sql_statements)

with open("erp_schema_dump.sql", "w") as f:
    f.write(final_script)

# Also dump a summary JSON for reference if needed
with open("schema_logic.json", "w") as f:
    json.dump(table_summaries, f, indent=4)

print(f"Successfully generated connected schema 'erp_schema_dump.sql' with {len(sql_statements)} tables.")