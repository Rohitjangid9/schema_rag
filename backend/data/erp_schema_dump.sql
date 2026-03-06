CREATE TABLE IF NOT EXISTS global_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS sales_order (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS sales_order_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_order_detail_main FOREIGN KEY (parent_id) REFERENCES sales_order(id)
);

CREATE TABLE IF NOT EXISTS sales_order_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_order_history_main FOREIGN KEY (parent_id) REFERENCES sales_order(id)
);

CREATE TABLE IF NOT EXISTS sales_order_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_order_comment_main FOREIGN KEY (parent_id) REFERENCES sales_order(id)
);

CREATE TABLE IF NOT EXISTS sales_order_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_order_attachment_main FOREIGN KEY (parent_id) REFERENCES sales_order(id)
);

CREATE TABLE IF NOT EXISTS sales_quote (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS sales_quote_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_quote_detail_main FOREIGN KEY (parent_id) REFERENCES sales_quote(id)
);

CREATE TABLE IF NOT EXISTS sales_quote_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_quote_history_main FOREIGN KEY (parent_id) REFERENCES sales_quote(id)
);

CREATE TABLE IF NOT EXISTS sales_quote_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_quote_comment_main FOREIGN KEY (parent_id) REFERENCES sales_quote(id)
);

CREATE TABLE IF NOT EXISTS sales_quote_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_quote_attachment_main FOREIGN KEY (parent_id) REFERENCES sales_quote(id)
);

CREATE TABLE IF NOT EXISTS sales_invoice (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS sales_invoice_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_invoice_detail_main FOREIGN KEY (parent_id) REFERENCES sales_invoice(id)
);

CREATE TABLE IF NOT EXISTS sales_invoice_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_invoice_history_main FOREIGN KEY (parent_id) REFERENCES sales_invoice(id)
);

CREATE TABLE IF NOT EXISTS sales_invoice_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_invoice_comment_main FOREIGN KEY (parent_id) REFERENCES sales_invoice(id)
);

CREATE TABLE IF NOT EXISTS sales_invoice_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_invoice_attachment_main FOREIGN KEY (parent_id) REFERENCES sales_invoice(id)
);

CREATE TABLE IF NOT EXISTS sales_lead (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS sales_lead_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_lead_detail_main FOREIGN KEY (parent_id) REFERENCES sales_lead(id)
);

CREATE TABLE IF NOT EXISTS sales_lead_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_lead_history_main FOREIGN KEY (parent_id) REFERENCES sales_lead(id)
);

CREATE TABLE IF NOT EXISTS sales_lead_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_lead_comment_main FOREIGN KEY (parent_id) REFERENCES sales_lead(id)
);

CREATE TABLE IF NOT EXISTS sales_lead_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_lead_attachment_main FOREIGN KEY (parent_id) REFERENCES sales_lead(id)
);

CREATE TABLE IF NOT EXISTS sales_opportunity (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS sales_opportunity_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_opportunity_detail_main FOREIGN KEY (parent_id) REFERENCES sales_opportunity(id)
);

CREATE TABLE IF NOT EXISTS sales_opportunity_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_opportunity_history_main FOREIGN KEY (parent_id) REFERENCES sales_opportunity(id)
);

CREATE TABLE IF NOT EXISTS sales_opportunity_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_opportunity_comment_main FOREIGN KEY (parent_id) REFERENCES sales_opportunity(id)
);

CREATE TABLE IF NOT EXISTS sales_opportunity_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_opportunity_attachment_main FOREIGN KEY (parent_id) REFERENCES sales_opportunity(id)
);

CREATE TABLE IF NOT EXISTS sales_contract (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS sales_contract_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_contract_detail_main FOREIGN KEY (parent_id) REFERENCES sales_contract(id)
);

CREATE TABLE IF NOT EXISTS sales_contract_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_contract_history_main FOREIGN KEY (parent_id) REFERENCES sales_contract(id)
);

CREATE TABLE IF NOT EXISTS sales_contract_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_contract_comment_main FOREIGN KEY (parent_id) REFERENCES sales_contract(id)
);

CREATE TABLE IF NOT EXISTS sales_contract_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_contract_attachment_main FOREIGN KEY (parent_id) REFERENCES sales_contract(id)
);

CREATE TABLE IF NOT EXISTS sales_refund (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS sales_refund_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_refund_detail_main FOREIGN KEY (parent_id) REFERENCES sales_refund(id)
);

CREATE TABLE IF NOT EXISTS sales_refund_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_refund_history_main FOREIGN KEY (parent_id) REFERENCES sales_refund(id)
);

CREATE TABLE IF NOT EXISTS sales_refund_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_refund_comment_main FOREIGN KEY (parent_id) REFERENCES sales_refund(id)
);

CREATE TABLE IF NOT EXISTS sales_refund_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_refund_attachment_main FOREIGN KEY (parent_id) REFERENCES sales_refund(id)
);

CREATE TABLE IF NOT EXISTS sales_forecast (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS sales_forecast_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_forecast_detail_main FOREIGN KEY (parent_id) REFERENCES sales_forecast(id)
);

CREATE TABLE IF NOT EXISTS sales_forecast_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_forecast_history_main FOREIGN KEY (parent_id) REFERENCES sales_forecast(id)
);

CREATE TABLE IF NOT EXISTS sales_forecast_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_forecast_comment_main FOREIGN KEY (parent_id) REFERENCES sales_forecast(id)
);

CREATE TABLE IF NOT EXISTS sales_forecast_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_sales_forecast_attachment_main FOREIGN KEY (parent_id) REFERENCES sales_forecast(id)
);

CREATE TABLE IF NOT EXISTS hr_employee (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS hr_employee_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_employee_detail_main FOREIGN KEY (parent_id) REFERENCES hr_employee(id)
);

CREATE TABLE IF NOT EXISTS hr_employee_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_employee_history_main FOREIGN KEY (parent_id) REFERENCES hr_employee(id)
);

CREATE TABLE IF NOT EXISTS hr_employee_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_employee_comment_main FOREIGN KEY (parent_id) REFERENCES hr_employee(id)
);

CREATE TABLE IF NOT EXISTS hr_employee_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_employee_attachment_main FOREIGN KEY (parent_id) REFERENCES hr_employee(id)
);

CREATE TABLE IF NOT EXISTS hr_department (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS hr_department_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_department_detail_main FOREIGN KEY (parent_id) REFERENCES hr_department(id)
);

CREATE TABLE IF NOT EXISTS hr_department_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_department_history_main FOREIGN KEY (parent_id) REFERENCES hr_department(id)
);

CREATE TABLE IF NOT EXISTS hr_department_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_department_comment_main FOREIGN KEY (parent_id) REFERENCES hr_department(id)
);

CREATE TABLE IF NOT EXISTS hr_department_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_department_attachment_main FOREIGN KEY (parent_id) REFERENCES hr_department(id)
);

CREATE TABLE IF NOT EXISTS hr_payroll (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS hr_payroll_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_payroll_detail_main FOREIGN KEY (parent_id) REFERENCES hr_payroll(id)
);

CREATE TABLE IF NOT EXISTS hr_payroll_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_payroll_history_main FOREIGN KEY (parent_id) REFERENCES hr_payroll(id)
);

CREATE TABLE IF NOT EXISTS hr_payroll_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_payroll_comment_main FOREIGN KEY (parent_id) REFERENCES hr_payroll(id)
);

CREATE TABLE IF NOT EXISTS hr_payroll_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_payroll_attachment_main FOREIGN KEY (parent_id) REFERENCES hr_payroll(id)
);

CREATE TABLE IF NOT EXISTS hr_benefit (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS hr_benefit_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_benefit_detail_main FOREIGN KEY (parent_id) REFERENCES hr_benefit(id)
);

CREATE TABLE IF NOT EXISTS hr_benefit_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_benefit_history_main FOREIGN KEY (parent_id) REFERENCES hr_benefit(id)
);

CREATE TABLE IF NOT EXISTS hr_benefit_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_benefit_comment_main FOREIGN KEY (parent_id) REFERENCES hr_benefit(id)
);

CREATE TABLE IF NOT EXISTS hr_benefit_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_benefit_attachment_main FOREIGN KEY (parent_id) REFERENCES hr_benefit(id)
);

CREATE TABLE IF NOT EXISTS hr_attendance (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS hr_attendance_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_attendance_detail_main FOREIGN KEY (parent_id) REFERENCES hr_attendance(id)
);

CREATE TABLE IF NOT EXISTS hr_attendance_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_attendance_history_main FOREIGN KEY (parent_id) REFERENCES hr_attendance(id)
);

CREATE TABLE IF NOT EXISTS hr_attendance_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_attendance_comment_main FOREIGN KEY (parent_id) REFERENCES hr_attendance(id)
);

CREATE TABLE IF NOT EXISTS hr_attendance_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_attendance_attachment_main FOREIGN KEY (parent_id) REFERENCES hr_attendance(id)
);

CREATE TABLE IF NOT EXISTS hr_candidate (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS hr_candidate_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_candidate_detail_main FOREIGN KEY (parent_id) REFERENCES hr_candidate(id)
);

CREATE TABLE IF NOT EXISTS hr_candidate_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_candidate_history_main FOREIGN KEY (parent_id) REFERENCES hr_candidate(id)
);

CREATE TABLE IF NOT EXISTS hr_candidate_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_candidate_comment_main FOREIGN KEY (parent_id) REFERENCES hr_candidate(id)
);

CREATE TABLE IF NOT EXISTS hr_candidate_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_candidate_attachment_main FOREIGN KEY (parent_id) REFERENCES hr_candidate(id)
);

CREATE TABLE IF NOT EXISTS hr_review (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS hr_review_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_review_detail_main FOREIGN KEY (parent_id) REFERENCES hr_review(id)
);

CREATE TABLE IF NOT EXISTS hr_review_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_review_history_main FOREIGN KEY (parent_id) REFERENCES hr_review(id)
);

CREATE TABLE IF NOT EXISTS hr_review_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_review_comment_main FOREIGN KEY (parent_id) REFERENCES hr_review(id)
);

CREATE TABLE IF NOT EXISTS hr_review_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_review_attachment_main FOREIGN KEY (parent_id) REFERENCES hr_review(id)
);

CREATE TABLE IF NOT EXISTS hr_training (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS hr_training_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_training_detail_main FOREIGN KEY (parent_id) REFERENCES hr_training(id)
);

CREATE TABLE IF NOT EXISTS hr_training_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_training_history_main FOREIGN KEY (parent_id) REFERENCES hr_training(id)
);

CREATE TABLE IF NOT EXISTS hr_training_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_training_comment_main FOREIGN KEY (parent_id) REFERENCES hr_training(id)
);

CREATE TABLE IF NOT EXISTS hr_training_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_hr_training_attachment_main FOREIGN KEY (parent_id) REFERENCES hr_training(id)
);

CREATE TABLE IF NOT EXISTS inventory_product (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS inventory_product_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_product_detail_main FOREIGN KEY (parent_id) REFERENCES inventory_product(id)
);

CREATE TABLE IF NOT EXISTS inventory_product_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_product_history_main FOREIGN KEY (parent_id) REFERENCES inventory_product(id)
);

CREATE TABLE IF NOT EXISTS inventory_product_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_product_comment_main FOREIGN KEY (parent_id) REFERENCES inventory_product(id)
);

CREATE TABLE IF NOT EXISTS inventory_product_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_product_attachment_main FOREIGN KEY (parent_id) REFERENCES inventory_product(id)
);

CREATE TABLE IF NOT EXISTS inventory_warehouse (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS inventory_warehouse_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_warehouse_detail_main FOREIGN KEY (parent_id) REFERENCES inventory_warehouse(id)
);

CREATE TABLE IF NOT EXISTS inventory_warehouse_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_warehouse_history_main FOREIGN KEY (parent_id) REFERENCES inventory_warehouse(id)
);

CREATE TABLE IF NOT EXISTS inventory_warehouse_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_warehouse_comment_main FOREIGN KEY (parent_id) REFERENCES inventory_warehouse(id)
);

CREATE TABLE IF NOT EXISTS inventory_warehouse_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_warehouse_attachment_main FOREIGN KEY (parent_id) REFERENCES inventory_warehouse(id)
);

CREATE TABLE IF NOT EXISTS inventory_stock_movement (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS inventory_stock_movement_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_stock_movement_detail_main FOREIGN KEY (parent_id) REFERENCES inventory_stock_movement(id)
);

CREATE TABLE IF NOT EXISTS inventory_stock_movement_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_stock_movement_history_main FOREIGN KEY (parent_id) REFERENCES inventory_stock_movement(id)
);

CREATE TABLE IF NOT EXISTS inventory_stock_movement_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_stock_movement_comment_main FOREIGN KEY (parent_id) REFERENCES inventory_stock_movement(id)
);

CREATE TABLE IF NOT EXISTS inventory_stock_movement_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_stock_movement_attachment_main FOREIGN KEY (parent_id) REFERENCES inventory_stock_movement(id)
);

CREATE TABLE IF NOT EXISTS inventory_supplier (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS inventory_supplier_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_supplier_detail_main FOREIGN KEY (parent_id) REFERENCES inventory_supplier(id)
);

CREATE TABLE IF NOT EXISTS inventory_supplier_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_supplier_history_main FOREIGN KEY (parent_id) REFERENCES inventory_supplier(id)
);

CREATE TABLE IF NOT EXISTS inventory_supplier_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_supplier_comment_main FOREIGN KEY (parent_id) REFERENCES inventory_supplier(id)
);

CREATE TABLE IF NOT EXISTS inventory_supplier_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_supplier_attachment_main FOREIGN KEY (parent_id) REFERENCES inventory_supplier(id)
);

CREATE TABLE IF NOT EXISTS inventory_purchase_order (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS inventory_purchase_order_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_purchase_order_detail_main FOREIGN KEY (parent_id) REFERENCES inventory_purchase_order(id)
);

CREATE TABLE IF NOT EXISTS inventory_purchase_order_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_purchase_order_history_main FOREIGN KEY (parent_id) REFERENCES inventory_purchase_order(id)
);

CREATE TABLE IF NOT EXISTS inventory_purchase_order_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_purchase_order_comment_main FOREIGN KEY (parent_id) REFERENCES inventory_purchase_order(id)
);

CREATE TABLE IF NOT EXISTS inventory_purchase_order_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_purchase_order_attachment_main FOREIGN KEY (parent_id) REFERENCES inventory_purchase_order(id)
);

CREATE TABLE IF NOT EXISTS inventory_category (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS inventory_category_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_category_detail_main FOREIGN KEY (parent_id) REFERENCES inventory_category(id)
);

CREATE TABLE IF NOT EXISTS inventory_category_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_category_history_main FOREIGN KEY (parent_id) REFERENCES inventory_category(id)
);

CREATE TABLE IF NOT EXISTS inventory_category_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_category_comment_main FOREIGN KEY (parent_id) REFERENCES inventory_category(id)
);

CREATE TABLE IF NOT EXISTS inventory_category_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_category_attachment_main FOREIGN KEY (parent_id) REFERENCES inventory_category(id)
);

CREATE TABLE IF NOT EXISTS inventory_batch (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS inventory_batch_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_batch_detail_main FOREIGN KEY (parent_id) REFERENCES inventory_batch(id)
);

CREATE TABLE IF NOT EXISTS inventory_batch_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_batch_history_main FOREIGN KEY (parent_id) REFERENCES inventory_batch(id)
);

CREATE TABLE IF NOT EXISTS inventory_batch_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_batch_comment_main FOREIGN KEY (parent_id) REFERENCES inventory_batch(id)
);

CREATE TABLE IF NOT EXISTS inventory_batch_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_inventory_batch_attachment_main FOREIGN KEY (parent_id) REFERENCES inventory_batch(id)
);

CREATE TABLE IF NOT EXISTS finance_ledger (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS finance_ledger_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_ledger_detail_main FOREIGN KEY (parent_id) REFERENCES finance_ledger(id)
);

CREATE TABLE IF NOT EXISTS finance_ledger_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_ledger_history_main FOREIGN KEY (parent_id) REFERENCES finance_ledger(id)
);

CREATE TABLE IF NOT EXISTS finance_ledger_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_ledger_comment_main FOREIGN KEY (parent_id) REFERENCES finance_ledger(id)
);

CREATE TABLE IF NOT EXISTS finance_ledger_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_ledger_attachment_main FOREIGN KEY (parent_id) REFERENCES finance_ledger(id)
);

CREATE TABLE IF NOT EXISTS finance_asset (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS finance_asset_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_asset_detail_main FOREIGN KEY (parent_id) REFERENCES finance_asset(id)
);

CREATE TABLE IF NOT EXISTS finance_asset_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_asset_history_main FOREIGN KEY (parent_id) REFERENCES finance_asset(id)
);

CREATE TABLE IF NOT EXISTS finance_asset_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_asset_comment_main FOREIGN KEY (parent_id) REFERENCES finance_asset(id)
);

CREATE TABLE IF NOT EXISTS finance_asset_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_asset_attachment_main FOREIGN KEY (parent_id) REFERENCES finance_asset(id)
);

CREATE TABLE IF NOT EXISTS finance_tax_record (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS finance_tax_record_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_tax_record_detail_main FOREIGN KEY (parent_id) REFERENCES finance_tax_record(id)
);

CREATE TABLE IF NOT EXISTS finance_tax_record_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_tax_record_history_main FOREIGN KEY (parent_id) REFERENCES finance_tax_record(id)
);

CREATE TABLE IF NOT EXISTS finance_tax_record_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_tax_record_comment_main FOREIGN KEY (parent_id) REFERENCES finance_tax_record(id)
);

CREATE TABLE IF NOT EXISTS finance_tax_record_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_tax_record_attachment_main FOREIGN KEY (parent_id) REFERENCES finance_tax_record(id)
);

CREATE TABLE IF NOT EXISTS finance_budget (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS finance_budget_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_budget_detail_main FOREIGN KEY (parent_id) REFERENCES finance_budget(id)
);

CREATE TABLE IF NOT EXISTS finance_budget_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_budget_history_main FOREIGN KEY (parent_id) REFERENCES finance_budget(id)
);

CREATE TABLE IF NOT EXISTS finance_budget_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_budget_comment_main FOREIGN KEY (parent_id) REFERENCES finance_budget(id)
);

CREATE TABLE IF NOT EXISTS finance_budget_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_budget_attachment_main FOREIGN KEY (parent_id) REFERENCES finance_budget(id)
);

CREATE TABLE IF NOT EXISTS finance_expense (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS finance_expense_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_expense_detail_main FOREIGN KEY (parent_id) REFERENCES finance_expense(id)
);

CREATE TABLE IF NOT EXISTS finance_expense_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_expense_history_main FOREIGN KEY (parent_id) REFERENCES finance_expense(id)
);

CREATE TABLE IF NOT EXISTS finance_expense_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_expense_comment_main FOREIGN KEY (parent_id) REFERENCES finance_expense(id)
);

CREATE TABLE IF NOT EXISTS finance_expense_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_expense_attachment_main FOREIGN KEY (parent_id) REFERENCES finance_expense(id)
);

CREATE TABLE IF NOT EXISTS finance_revenue (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS finance_revenue_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_revenue_detail_main FOREIGN KEY (parent_id) REFERENCES finance_revenue(id)
);

CREATE TABLE IF NOT EXISTS finance_revenue_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_revenue_history_main FOREIGN KEY (parent_id) REFERENCES finance_revenue(id)
);

CREATE TABLE IF NOT EXISTS finance_revenue_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_revenue_comment_main FOREIGN KEY (parent_id) REFERENCES finance_revenue(id)
);

CREATE TABLE IF NOT EXISTS finance_revenue_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_revenue_attachment_main FOREIGN KEY (parent_id) REFERENCES finance_revenue(id)
);

CREATE TABLE IF NOT EXISTS finance_bank_account (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS finance_bank_account_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_bank_account_detail_main FOREIGN KEY (parent_id) REFERENCES finance_bank_account(id)
);

CREATE TABLE IF NOT EXISTS finance_bank_account_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_bank_account_history_main FOREIGN KEY (parent_id) REFERENCES finance_bank_account(id)
);

CREATE TABLE IF NOT EXISTS finance_bank_account_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_bank_account_comment_main FOREIGN KEY (parent_id) REFERENCES finance_bank_account(id)
);

CREATE TABLE IF NOT EXISTS finance_bank_account_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_finance_bank_account_attachment_main FOREIGN KEY (parent_id) REFERENCES finance_bank_account(id)
);

CREATE TABLE IF NOT EXISTS crm_customer (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS crm_customer_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_customer_detail_main FOREIGN KEY (parent_id) REFERENCES crm_customer(id)
);

CREATE TABLE IF NOT EXISTS crm_customer_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_customer_history_main FOREIGN KEY (parent_id) REFERENCES crm_customer(id)
);

CREATE TABLE IF NOT EXISTS crm_customer_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_customer_comment_main FOREIGN KEY (parent_id) REFERENCES crm_customer(id)
);

CREATE TABLE IF NOT EXISTS crm_customer_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_customer_attachment_main FOREIGN KEY (parent_id) REFERENCES crm_customer(id)
);

CREATE TABLE IF NOT EXISTS crm_ticket (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS crm_ticket_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_ticket_detail_main FOREIGN KEY (parent_id) REFERENCES crm_ticket(id)
);

CREATE TABLE IF NOT EXISTS crm_ticket_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_ticket_history_main FOREIGN KEY (parent_id) REFERENCES crm_ticket(id)
);

CREATE TABLE IF NOT EXISTS crm_ticket_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_ticket_comment_main FOREIGN KEY (parent_id) REFERENCES crm_ticket(id)
);

CREATE TABLE IF NOT EXISTS crm_ticket_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_ticket_attachment_main FOREIGN KEY (parent_id) REFERENCES crm_ticket(id)
);

CREATE TABLE IF NOT EXISTS crm_interaction (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS crm_interaction_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_interaction_detail_main FOREIGN KEY (parent_id) REFERENCES crm_interaction(id)
);

CREATE TABLE IF NOT EXISTS crm_interaction_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_interaction_history_main FOREIGN KEY (parent_id) REFERENCES crm_interaction(id)
);

CREATE TABLE IF NOT EXISTS crm_interaction_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_interaction_comment_main FOREIGN KEY (parent_id) REFERENCES crm_interaction(id)
);

CREATE TABLE IF NOT EXISTS crm_interaction_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_interaction_attachment_main FOREIGN KEY (parent_id) REFERENCES crm_interaction(id)
);

CREATE TABLE IF NOT EXISTS crm_survey (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS crm_survey_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_survey_detail_main FOREIGN KEY (parent_id) REFERENCES crm_survey(id)
);

CREATE TABLE IF NOT EXISTS crm_survey_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_survey_history_main FOREIGN KEY (parent_id) REFERENCES crm_survey(id)
);

CREATE TABLE IF NOT EXISTS crm_survey_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_survey_comment_main FOREIGN KEY (parent_id) REFERENCES crm_survey(id)
);

CREATE TABLE IF NOT EXISTS crm_survey_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_survey_attachment_main FOREIGN KEY (parent_id) REFERENCES crm_survey(id)
);

CREATE TABLE IF NOT EXISTS crm_loyalty_point (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS crm_loyalty_point_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_loyalty_point_detail_main FOREIGN KEY (parent_id) REFERENCES crm_loyalty_point(id)
);

CREATE TABLE IF NOT EXISTS crm_loyalty_point_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_loyalty_point_history_main FOREIGN KEY (parent_id) REFERENCES crm_loyalty_point(id)
);

CREATE TABLE IF NOT EXISTS crm_loyalty_point_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_loyalty_point_comment_main FOREIGN KEY (parent_id) REFERENCES crm_loyalty_point(id)
);

CREATE TABLE IF NOT EXISTS crm_loyalty_point_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_loyalty_point_attachment_main FOREIGN KEY (parent_id) REFERENCES crm_loyalty_point(id)
);

CREATE TABLE IF NOT EXISTS crm_campaign (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS crm_campaign_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_campaign_detail_main FOREIGN KEY (parent_id) REFERENCES crm_campaign(id)
);

CREATE TABLE IF NOT EXISTS crm_campaign_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_campaign_history_main FOREIGN KEY (parent_id) REFERENCES crm_campaign(id)
);

CREATE TABLE IF NOT EXISTS crm_campaign_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_campaign_comment_main FOREIGN KEY (parent_id) REFERENCES crm_campaign(id)
);

CREATE TABLE IF NOT EXISTS crm_campaign_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_crm_campaign_attachment_main FOREIGN KEY (parent_id) REFERENCES crm_campaign(id)
);

CREATE TABLE IF NOT EXISTS logistics_shipment (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS logistics_shipment_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_shipment_detail_main FOREIGN KEY (parent_id) REFERENCES logistics_shipment(id)
);

CREATE TABLE IF NOT EXISTS logistics_shipment_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_shipment_history_main FOREIGN KEY (parent_id) REFERENCES logistics_shipment(id)
);

CREATE TABLE IF NOT EXISTS logistics_shipment_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_shipment_comment_main FOREIGN KEY (parent_id) REFERENCES logistics_shipment(id)
);

CREATE TABLE IF NOT EXISTS logistics_shipment_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_shipment_attachment_main FOREIGN KEY (parent_id) REFERENCES logistics_shipment(id)
);

CREATE TABLE IF NOT EXISTS logistics_route (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS logistics_route_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_route_detail_main FOREIGN KEY (parent_id) REFERENCES logistics_route(id)
);

CREATE TABLE IF NOT EXISTS logistics_route_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_route_history_main FOREIGN KEY (parent_id) REFERENCES logistics_route(id)
);

CREATE TABLE IF NOT EXISTS logistics_route_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_route_comment_main FOREIGN KEY (parent_id) REFERENCES logistics_route(id)
);

CREATE TABLE IF NOT EXISTS logistics_route_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_route_attachment_main FOREIGN KEY (parent_id) REFERENCES logistics_route(id)
);

CREATE TABLE IF NOT EXISTS logistics_vehicle (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS logistics_vehicle_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_vehicle_detail_main FOREIGN KEY (parent_id) REFERENCES logistics_vehicle(id)
);

CREATE TABLE IF NOT EXISTS logistics_vehicle_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_vehicle_history_main FOREIGN KEY (parent_id) REFERENCES logistics_vehicle(id)
);

CREATE TABLE IF NOT EXISTS logistics_vehicle_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_vehicle_comment_main FOREIGN KEY (parent_id) REFERENCES logistics_vehicle(id)
);

CREATE TABLE IF NOT EXISTS logistics_vehicle_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_vehicle_attachment_main FOREIGN KEY (parent_id) REFERENCES logistics_vehicle(id)
);

CREATE TABLE IF NOT EXISTS logistics_driver (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS logistics_driver_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_driver_detail_main FOREIGN KEY (parent_id) REFERENCES logistics_driver(id)
);

CREATE TABLE IF NOT EXISTS logistics_driver_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_driver_history_main FOREIGN KEY (parent_id) REFERENCES logistics_driver(id)
);

CREATE TABLE IF NOT EXISTS logistics_driver_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_driver_comment_main FOREIGN KEY (parent_id) REFERENCES logistics_driver(id)
);

CREATE TABLE IF NOT EXISTS logistics_driver_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_driver_attachment_main FOREIGN KEY (parent_id) REFERENCES logistics_driver(id)
);

CREATE TABLE IF NOT EXISTS logistics_delivery (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS logistics_delivery_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_delivery_detail_main FOREIGN KEY (parent_id) REFERENCES logistics_delivery(id)
);

CREATE TABLE IF NOT EXISTS logistics_delivery_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_delivery_history_main FOREIGN KEY (parent_id) REFERENCES logistics_delivery(id)
);

CREATE TABLE IF NOT EXISTS logistics_delivery_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_delivery_comment_main FOREIGN KEY (parent_id) REFERENCES logistics_delivery(id)
);

CREATE TABLE IF NOT EXISTS logistics_delivery_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_delivery_attachment_main FOREIGN KEY (parent_id) REFERENCES logistics_delivery(id)
);

CREATE TABLE IF NOT EXISTS logistics_customs_entry (
    id SERIAL PRIMARY KEY,
    ref_code VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT
);

CREATE TABLE IF NOT EXISTS logistics_customs_entry_detail (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INT,
    price_per_unit DECIMAL,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_customs_entry_detail_main FOREIGN KEY (parent_id) REFERENCES logistics_customs_entry(id)
);

CREATE TABLE IF NOT EXISTS logistics_customs_entry_history (
    id SERIAL PRIMARY KEY,
    change_log TEXT,
    changed_by INT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_customs_entry_history_main FOREIGN KEY (parent_id) REFERENCES logistics_customs_entry(id)
);

CREATE TABLE IF NOT EXISTS logistics_customs_entry_comment (
    id SERIAL PRIMARY KEY,
    comment_text TEXT,
    is_private BOOLEAN,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_customs_entry_comment_main FOREIGN KEY (parent_id) REFERENCES logistics_customs_entry(id)
);

CREATE TABLE IF NOT EXISTS logistics_customs_entry_attachment (
    id SERIAL PRIMARY KEY,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    CONSTRAINT fk_logistics_customs_entry_attachment_main FOREIGN KEY (parent_id) REFERENCES logistics_customs_entry(id)
);