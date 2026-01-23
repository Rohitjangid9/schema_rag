import random

# --- CONFIGURATION ---
MODULES = ['sales', 'hr', 'inventory', 'finance', 'crm', 'logistics']
ENTITIES = {
    'sales': ['order', 'quote', 'invoice', 'lead', 'opportunity', 'contract', 'refund', 'forecast'],
    'hr': ['employee', 'department', 'payroll', 'benefit', 'attendance', 'candidate', 'review', 'training'],
    'inventory': ['product', 'warehouse', 'stock_movement', 'supplier', 'purchase_order', 'category', 'batch'],
    'finance': ['ledger', 'asset', 'tax_record', 'budget', 'expense', 'revenue', 'bank_account'],
    'crm': ['customer', 'ticket', 'interaction', 'survey', 'loyalty_point', 'campaign'],
    'logistics': ['shipment', 'route', 'vehicle', 'driver', 'delivery', 'customs_entry']
}

# Standard columns that every table gets
BASE_COLS = [
    "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "updated_at TIMESTAMP",
    "is_active BOOLEAN DEFAULT TRUE",
    "created_by INT" # Assume connection to a user table
]

sql_statements = []

# --- HELPER TO CREATE SQL ---
def create_table_sql(table_name, columns, foreign_keys=[]):
    cols_str = ",\n    ".join(columns + BASE_COLS)
    fk_str = ""
    if foreign_keys:
        fk_str = ",\n    " + ",\n    ".join(foreign_keys)
    
    return f"CREATE TABLE IF NOT EXISTS {table_name} (\n    id SERIAL PRIMARY KEY,\n    {cols_str}{fk_str}\n);"

# --- MAIN GENERATION LOOP ---
print("Generating Schema...")

# 1. Create a Global 'Users' table first (so everyone can link to it)
sql_statements.append(create_table_sql("global_users", ["username VARCHAR(50)", "email VARCHAR(100)"]))

generated_tables = []

for module, entities in ENTITIES.items():
    for entity in entities:
        # Construct Main Table Name (e.g., sales_orders)
        main_table = f"{module}_{entity}"
        generated_tables.append(main_table)
        
        # Define random realistic columns
        main_cols = [
            f"ref_code VARCHAR(20)",
            f"status VARCHAR(20)",
            f"description TEXT",
            f"total_amount DECIMAL(10,2)"
        ]
        
        # Create the MAIN Table
        sql_statements.append(create_table_sql(main_table, main_cols))
        
        # --- THE MULTIPLIER (Create Satellite Tables) ---
        
        # A. Details Table (1-to-Many) - Connects back to Main Table
        # e.g., sales_order_details
        det_table = f"{main_table}_detail"
        det_cols = ["item_name VARCHAR(100)", "quantity INT", "price_per_unit DECIMAL"]
        det_fk = [f"CONSTRAINT fk_{det_table}_main FOREIGN KEY (parent_id) REFERENCES {main_table}(id)"]
        # Add parent_id column
        det_cols.append("parent_id INT") 
        sql_statements.append(create_table_sql(det_table, det_cols, det_fk))

        # B. History/Audit Table (Log changes)
        hist_table = f"{main_table}_history"
        hist_cols = ["change_log TEXT", "changed_by INT", "parent_id INT"]
        hist_fk = [f"CONSTRAINT fk_{hist_table}_main FOREIGN KEY (parent_id) REFERENCES {main_table}(id)"]
        sql_statements.append(create_table_sql(hist_table, hist_cols, hist_fk))

        # C. Comments/Notes Table
        note_table = f"{main_table}_comment"
        note_cols = ["comment_text TEXT", "is_private BOOLEAN", "parent_id INT"]
        note_fk = [f"CONSTRAINT fk_{note_table}_main FOREIGN KEY (parent_id) REFERENCES {main_table}(id)"]
        sql_statements.append(create_table_sql(note_table, note_cols, note_fk))
        
        # D. Attachments Table
        att_table = f"{main_table}_attachment"
        att_cols = ["file_url VARCHAR(255)", "file_type VARCHAR(50)", "parent_id INT"]
        att_fk = [f"CONSTRAINT fk_{att_table}_main FOREIGN KEY (parent_id) REFERENCES {main_table}(id)"]
        sql_statements.append(create_table_sql(att_table, att_cols, att_fk))

# --- CROSS-LINKING (Making it complex!) ---
# Randomly link tables to simulate complex ERP relationships
# e.g. Link 'sales_order' to 'crm_customer'
# NOTE: SQLite doesn't support ALTER TABLE ADD CONSTRAINT, so we skip this for now
# If using PostgreSQL/MySQL, uncomment the code below
extra_links = []
# sales_tables = [t for t in generated_tables if t.startswith('sales_')]
# crm_tables = [t for t in generated_tables if t.startswith('crm_')]
#
# for sales_t in sales_tables:
#     if crm_tables:
#         target = random.choice(crm_tables)
#         # Alter table to add foreign key (PostgreSQL/MySQL only)
#         alter_sql = f"ALTER TABLE {sales_t} ADD COLUMN linked_{target}_id INT;"
#         alter_sql += f"\nALTER TABLE {sales_t} ADD CONSTRAINT fk_{sales_t}_link FOREIGN KEY (linked_{target}_id) REFERENCES {target}(id);"
#         extra_links.append(alter_sql)

# --- OUTPUT ---
final_script = "\n\n".join(sql_statements + extra_links)

# Write to file
with open("erp_schema_dump.sql", "w") as f:
    f.write(final_script)

print(f"Successfully generated 'erp_schema_dump.sql' with approx {len(sql_statements)} tables.")