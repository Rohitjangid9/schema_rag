CREATE TABLE IF NOT EXISTS hr_employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    department_id INT,
    hire_date DATE,
    salary DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (department_id) REFERENCES hr_department(id)
);

CREATE TABLE IF NOT EXISTS hr_department (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES hr_employee(id)
);

CREATE TABLE IF NOT EXISTS crm_customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name VARCHAR(150),
    contact_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    industry VARCHAR(50),
    account_manager_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_manager_id) REFERENCES hr_employee(id)
);

CREATE TABLE IF NOT EXISTS crm_interaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT,
    employee_id INT,
    interaction_type VARCHAR(50),
    interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES crm_customer(id),
    FOREIGN KEY (employee_id) REFERENCES hr_employee(id)
);

CREATE TABLE IF NOT EXISTS sales_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ref_code VARCHAR(20),
    customer_id INT,
    sales_rep_id INT,
    order_date DATE,
    status VARCHAR(20),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES crm_customer(id),
    FOREIGN KEY (sales_rep_id) REFERENCES hr_employee(id)
);

CREATE TABLE IF NOT EXISTS sales_order_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(5,2),
    FOREIGN KEY (order_id) REFERENCES sales_order(id),
    FOREIGN KEY (product_id) REFERENCES inventory_product(id)
);

CREATE TABLE IF NOT EXISTS sales_invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INT,
    customer_id INT,
    invoice_date DATE,
    due_date DATE,
    amount DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (order_id) REFERENCES sales_order(id),
    FOREIGN KEY (customer_id) REFERENCES crm_customer(id)
);

CREATE TABLE IF NOT EXISTS inventory_product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku VARCHAR(50),
    name VARCHAR(150),
    category_id INT,
    unit_cost DECIMAL(10,2),
    selling_price DECIMAL(10,2),
    stock_quantity INT,
    FOREIGN KEY (category_id) REFERENCES inventory_category(id)
);

CREATE TABLE IF NOT EXISTS inventory_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    description TEXT
);

CREATE TABLE IF NOT EXISTS inventory_warehouse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    location VARCHAR(200),
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES hr_employee(id)
);

CREATE TABLE IF NOT EXISTS inventory_stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INT,
    warehouse_id INT,
    quantity INT,
    last_restock_date DATE,
    FOREIGN KEY (product_id) REFERENCES inventory_product(id),
    FOREIGN KEY (warehouse_id) REFERENCES inventory_warehouse(id)
);

CREATE TABLE IF NOT EXISTS logistics_shipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INT,
    warehouse_id INT,
    carrier VARCHAR(100),
    tracking_number VARCHAR(100),
    shipment_date DATE,
    estimated_delivery DATE,
    status VARCHAR(20),
    FOREIGN KEY (order_id) REFERENCES sales_order(id),
    FOREIGN KEY (warehouse_id) REFERENCES inventory_warehouse(id)
);

CREATE TABLE IF NOT EXISTS finance_payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INT,
    customer_id INT,
    payment_date DATE,
    amount DECIMAL(10,2),
    payment_method VARCHAR(50),
    status VARCHAR(20),
    FOREIGN KEY (invoice_id) REFERENCES sales_invoice(id),
    FOREIGN KEY (customer_id) REFERENCES crm_customer(id)
);

CREATE TABLE IF NOT EXISTS finance_expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INT,
    department_id INT,
    expense_date DATE,
    amount DECIMAL(10,2),
    category VARCHAR(50),
    description TEXT,
    status VARCHAR(20),
    FOREIGN KEY (employee_id) REFERENCES hr_employee(id),
    FOREIGN KEY (department_id) REFERENCES hr_department(id)
);