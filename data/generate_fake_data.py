import random
import sqlite3
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Database connection
DB_FILE = "erp_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Configuration from randomschemas.py
MODULES = ['sales', 'hr', 'inventory', 'finance', 'crm', 'logistics']
ENTITIES = {
    'sales': ['order', 'quote', 'invoice', 'lead', 'opportunity', 'contract', 'refund', 'forecast'],
    'hr': ['employee', 'department', 'payroll', 'benefit', 'attendance', 'candidate', 'review', 'training'],
    'inventory': ['product', 'warehouse', 'stock_movement', 'supplier', 'purchase_order', 'category', 'batch'],
    'finance': ['ledger', 'asset', 'tax_record', 'budget', 'expense', 'revenue', 'bank_account'],
    'crm': ['customer', 'ticket', 'interaction', 'survey', 'loyalty_point', 'campaign'],
    'logistics': ['shipment', 'route', 'vehicle', 'driver', 'delivery', 'customs_entry']
}

# Number of records to generate per table
RECORDS_PER_TABLE = 50

def generate_fake_users(count=100):
    """Generate fake users"""
    print(f"Generating {count} fake users...")
    for _ in range(count):
        username = fake.user_name()
        email = fake.email()
        cursor.execute(
            "INSERT INTO global_users (username, email) VALUES (?, ?)",
            (username, email)
        )
    conn.commit()
    print(f"✓ Generated {count} users")

def generate_main_table_data(table_name, count=RECORDS_PER_TABLE):
    """Generate fake data for main tables"""
    print(f"  Generating {count} records for {table_name}...")
    for _ in range(count):
        ref_code = fake.bothify(text='??-####')
        status = random.choice(['active', 'pending', 'completed', 'cancelled', 'draft'])
        description = fake.sentence()
        total_amount = round(random.uniform(100, 10000), 2)
        created_at = fake.date_time_this_year()
        updated_at = created_at + timedelta(days=random.randint(0, 30))
        is_active = random.choice([True, False])
        created_by = random.randint(1, 100)
        
        cursor.execute(f"""
            INSERT INTO {table_name} 
            (ref_code, status, description, total_amount, created_at, updated_at, is_active, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (ref_code, status, description, total_amount, created_at, updated_at, is_active, created_by))
    conn.commit()

def generate_detail_table_data(main_table, detail_table, count=RECORDS_PER_TABLE):
    """Generate fake data for detail tables"""
    print(f"  Generating detail records for {detail_table}...")
    # Get all parent IDs
    cursor.execute(f"SELECT id FROM {main_table}")
    parent_ids = [row[0] for row in cursor.fetchall()]
    
    if not parent_ids:
        return
    
    for _ in range(count * 3):  # 3x records per parent
        parent_id = random.choice(parent_ids)
        item_name = fake.word()
        quantity = random.randint(1, 100)
        price_per_unit = round(random.uniform(10, 1000), 2)
        created_at = fake.date_time_this_year()
        updated_at = created_at + timedelta(days=random.randint(0, 30))
        is_active = random.choice([True, False])
        created_by = random.randint(1, 100)
        
        cursor.execute(f"""
            INSERT INTO {detail_table}
            (item_name, quantity, price_per_unit, parent_id, created_at, updated_at, is_active, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (item_name, quantity, price_per_unit, parent_id, created_at, updated_at, is_active, created_by))
    conn.commit()

def generate_history_table_data(main_table, history_table, count=RECORDS_PER_TABLE):
    """Generate fake history/audit data"""
    print(f"  Generating history records for {history_table}...")
    cursor.execute(f"SELECT id FROM {main_table}")
    parent_ids = [row[0] for row in cursor.fetchall()]
    
    if not parent_ids:
        return
    
    for _ in range(count):
        parent_id = random.choice(parent_ids)
        change_log = fake.sentence()
        changed_by = random.randint(1, 100)
        created_at = fake.date_time_this_year()
        updated_at = created_at + timedelta(days=random.randint(0, 30))
        is_active = True
        created_by = random.randint(1, 100)
        
        cursor.execute(f"""
            INSERT INTO {history_table}
            (change_log, changed_by, parent_id, created_at, updated_at, is_active, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (change_log, changed_by, parent_id, created_at, updated_at, is_active, created_by))
    conn.commit()

def generate_comment_table_data(main_table, comment_table, count=RECORDS_PER_TABLE):
    """Generate fake comment data"""
    print(f"  Generating comment records for {comment_table}...")
    cursor.execute(f"SELECT id FROM {main_table}")
    parent_ids = [row[0] for row in cursor.fetchall()]
    
    if not parent_ids:
        return
    
    for _ in range(count):
        parent_id = random.choice(parent_ids)
        comment_text = fake.paragraph()
        is_private = random.choice([True, False])
        created_at = fake.date_time_this_year()
        updated_at = created_at + timedelta(days=random.randint(0, 30))
        is_active = True
        created_by = random.randint(1, 100)
        
        cursor.execute(f"""
            INSERT INTO {comment_table}
            (comment_text, is_private, parent_id, created_at, updated_at, is_active, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (comment_text, is_private, parent_id, created_at, updated_at, is_active, created_by))
    conn.commit()

def generate_attachment_table_data(main_table, attachment_table, count=RECORDS_PER_TABLE):
    """Generate fake attachment data"""
    print(f"  Generating attachment records for {attachment_table}...")
    cursor.execute(f"SELECT id FROM {main_table}")
    parent_ids = [row[0] for row in cursor.fetchall()]
    
    if not parent_ids:
        return
    
    for _ in range(count):
        parent_id = random.choice(parent_ids)
        file_url = fake.url()
        file_type = random.choice(['pdf', 'doc', 'xls', 'jpg', 'png', 'txt'])
        created_at = fake.date_time_this_year()
        updated_at = created_at + timedelta(days=random.randint(0, 30))
        is_active = True
        created_by = random.randint(1, 100)
        
        cursor.execute(f"""
            INSERT INTO {attachment_table}
            (file_url, file_type, parent_id, created_at, updated_at, is_active, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (file_url, file_type, parent_id, created_at, updated_at, is_active, created_by))
    conn.commit()

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("FAKE DATA GENERATOR FOR ERP SCHEMA")
    print("=" * 60)
    
    # Generate users first
    generate_fake_users(100)
    
    # Generate data for all tables
    print("\nGenerating data for all ERP tables...")
    for module, entities in ENTITIES.items():
        print(f"\n[{module.upper()}]")
        for entity in entities:
            main_table = f"{module}_{entity}"
            print(f"Processing {main_table}...")
            
            try:
                generate_main_table_data(main_table, RECORDS_PER_TABLE)
                generate_detail_table_data(main_table, f"{main_table}_detail", RECORDS_PER_TABLE)
                generate_history_table_data(main_table, f"{main_table}_history", RECORDS_PER_TABLE)
                generate_comment_table_data(main_table, f"{main_table}_comment", RECORDS_PER_TABLE)
                generate_attachment_table_data(main_table, f"{main_table}_attachment", RECORDS_PER_TABLE)
            except Exception as e:
                print(f"  ✗ Error processing {main_table}: {e}")
    
    conn.close()
    print("\n" + "=" * 60)
    print(f"✓ Fake data generation complete! Database: {DB_FILE}")
    print("=" * 60)

