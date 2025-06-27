-- VitaPink BloodBank Database Schema
-- MySQL 8.0+ Compatible

-- Create database
CREATE DATABASE IF NOT EXISTS vitapink_bloodbank;
USE vitapink_bloodbank;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('donor', 'admin', 'lab') NOT NULL DEFAULT 'donor',
    
    -- Personal Information
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    birth_date DATE,
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    
    -- Address Information
    address VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100),
    
    -- Account Status
    is_active BOOLEAN DEFAULT TRUE,
    is_eligible BOOLEAN DEFAULT TRUE,
    last_donation_date DATETIME,
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_blood_type (blood_type),
    INDEX idx_city (city),
    INDEX idx_state (state),
    INDEX idx_is_active (is_active),
    INDEX idx_is_eligible (is_eligible),
    INDEX idx_created_at (created_at)
);

-- Create locations table
CREATE TABLE IF NOT EXISTS locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    
    -- Contact Information
    contact_info VARCHAR(255),
    phone_number VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    
    -- Operating Hours
    opening_hours TEXT,
    monday_open TIME,
    monday_close TIME,
    tuesday_open TIME,
    tuesday_close TIME,
    wednesday_open TIME,
    wednesday_close TIME,
    thursday_open TIME,
    thursday_close TIME,
    friday_open TIME,
    friday_close TIME,
    saturday_open TIME,
    saturday_close TIME,
    sunday_open TIME,
    sunday_close TIME,
    
    -- Additional Information
    location_type VARCHAR(50),
    capacity INT,
    amenities TEXT,
    languages_spoken VARCHAR(255),
    
    -- Status and Availability
    is_active BOOLEAN DEFAULT TRUE,
    is_accepting_donations BOOLEAN DEFAULT TRUE,
    current_wait_time INT DEFAULT 0,
    appointments_required BOOLEAN DEFAULT FALSE,
    
    -- Statistics
    total_donations_collected INT DEFAULT 0,
    rating DECIMAL(3,2),
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_name (name),
    INDEX idx_location_type (location_type),
    INDEX idx_is_active (is_active),
    INDEX idx_is_accepting_donations (is_accepting_donations),
    INDEX idx_coordinates (latitude, longitude)
);

-- Create donations table
CREATE TABLE IF NOT EXISTS donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    donation_date DATETIME NOT NULL,
    location_id INT,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
    
    -- Additional donation information
    hemoglobin_level DECIMAL(4,2),
    blood_pressure_systolic INT,
    blood_pressure_diastolic INT,
    weight DECIMAL(5,2),
    temperature DECIMAL(4,1),
    
    -- Processing information
    collection_bag_number VARCHAR(50),
    expiry_date DATETIME,
    processing_notes TEXT,
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE SET NULL,
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_blood_type (blood_type),
    INDEX idx_donation_date (donation_date),
    INDEX idx_location_id (location_id),
    INDEX idx_status (status),
    INDEX idx_user_blood_type (user_id, blood_type),
    INDEX idx_date_status (donation_date, status)
);

-- Create blood_inventory table
CREATE TABLE IF NOT EXISTS blood_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') UNIQUE NOT NULL,
    current_stock DECIMAL(10,2) NOT NULL DEFAULT 0,
    min_threshold DECIMAL(10,2) DEFAULT 1000,
    max_capacity DECIMAL(10,2) DEFAULT 10000,
    
    -- Additional inventory information
    reserved_stock DECIMAL(10,2) DEFAULT 0,
    expired_stock DECIMAL(10,2) DEFAULT 0,
    units_dispensed_today DECIMAL(10,2) DEFAULT 0,
    units_received_today DECIMAL(10,2) DEFAULT 0,
    
    -- Tracking information
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_donation_date DATETIME,
    last_dispensed_date DATETIME,
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_blood_type (blood_type),
    INDEX idx_current_stock (current_stock),
    INDEX idx_last_updated (last_updated)
);

-- Insert default blood inventory records
INSERT INTO blood_inventory (blood_type, current_stock, min_threshold, max_capacity) VALUES
('A+', 2000, 1000, 10000),
('A-', 1500, 800, 8000),
('B+', 1800, 900, 9000),
('B-', 1200, 600, 6000),
('AB+', 800, 400, 4000),
('AB-', 600, 300, 3000),
('O+', 2500, 1500, 15000),
('O-', 2000, 1200, 12000)
ON DUPLICATE KEY UPDATE
    current_stock = VALUES(current_stock),
    min_threshold = VALUES(min_threshold),
    max_capacity = VALUES(max_capacity);

-- Create sample locations
INSERT INTO locations (name, address, latitude, longitude, phone_number, location_type, is_active, is_accepting_donations, monday_open, monday_close, tuesday_open, tuesday_close, wednesday_open, wednesday_close, thursday_open, thursday_close, friday_open, friday_close, saturday_open, saturday_close, languages_spoken) VALUES
('Centro de Sangre de San Juan', 'Ave. Roosevelt 1234, San Juan, PR 00920', 18.4655, -66.1057, '(787) 555-0101', 'blood_bank', TRUE, TRUE, '08:00', '17:00', '08:00', '17:00', '08:00', '17:00', '08:00', '17:00', '08:00', '17:00', '08:00', '16:00', 'Spanish, English'),
('Hospital Universitario Dr. Ramón Ruiz Arnau', 'Carr. 129 Km 1.2, Bayamón, PR 00956', 18.4177, -66.1537, '(787) 555-0102', 'hospital', TRUE, TRUE, '07:00', '19:00', '07:00', '19:00', '07:00', '19:00', '07:00', '19:00', '07:00', '19:00', '08:00', '15:00', 'Spanish, English'),
('Cruz Roja Americana - Capítulo de Puerto Rico', 'Ave. Barbosa 1456, Bayamón, PR 00961', 18.4036, -66.1538, '(787) 555-0103', 'community_center', TRUE, TRUE, '09:00', '16:00', '09:00', '16:00', '09:00', '16:00', '09:00', '16:00', '09:00', '16:00', NULL, NULL, 'Spanish, English'),
('Hospital Central de Ponce', 'Ave. Las Américas 2213, Ponce, PR 00717', 18.0110, -66.6140, '(787) 555-0104', 'hospital', TRUE, TRUE, '06:00', '18:00', '06:00', '18:00', '06:00', '18:00', '06:00', '18:00', '06:00', '18:00', '07:00', '14:00', 'Spanish, English'),
('Centro de Donación Móvil', 'Ubicación Variable, PR', NULL, NULL, '(787) 555-0105', 'mobile_unit', TRUE, TRUE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Spanish, English');

-- Create admin user (password: admin123)
INSERT INTO users (username, email, password_hash, role, first_name, last_name, is_active, is_eligible) VALUES
('admin', 'admin@vitapink.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkNrKrF/QdvfMK2', 'admin', 'System', 'Administrator', TRUE, FALSE),
('lab_tech', 'lab@vitapink.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkNrKrF/QdvfMK2', 'lab', 'Lab', 'Technician', TRUE, FALSE);

-- Create sample donor users
INSERT INTO users (username, email, password_hash, role, first_name, last_name, blood_type, phone_number, city, state, country, is_active, is_eligible) VALUES
('donor1', 'maria.rodriguez@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkNrKrF/QdvfMK2', 'donor', 'María', 'Rodríguez', 'O+', '(787) 555-1001', 'San Juan', 'Puerto Rico', 'Puerto Rico', TRUE, TRUE),
('donor2', 'carlos.martinez@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkNrKrF/QdvfMK2', 'donor', 'Carlos', 'Martínez', 'A+', '(787) 555-1002', 'Bayamón', 'Puerto Rico', 'Puerto Rico', TRUE, TRUE),
('donor3', 'ana.lopez@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewkNrKrF/QdvfMK2', 'donor', 'Ana', 'López', 'B+', '(787) 555-1003', 'Ponce', 'Puerto Rico', 'Puerto Rico', TRUE, TRUE);

-- Create sample donations
INSERT INTO donations (user_id, blood_type, quantity, donation_date, location_id, status, hemoglobin_level, collection_bag_number) VALUES
(3, 'O+', 450.00, '2024-01-15 10:30:00', 1, 'completed', 14.2, 'BAG001'),
(4, 'A+', 450.00, '2024-01-20 14:15:00', 2, 'completed', 13.8, 'BAG002'),
(5, 'B+', 450.00, '2024-01-25 09:45:00', 3, 'completed', 14.5, 'BAG003'),
(3, 'O+', 450.00, '2024-02-15 11:00:00', 1, 'pending', 14.0, NULL);

-- Create indexes for better performance
CREATE INDEX idx_donations_user_date ON donations(user_id, donation_date DESC);
CREATE INDEX idx_donations_blood_type_status ON donations(blood_type, status);
CREATE INDEX idx_users_role_active ON users(role, is_active);
CREATE INDEX idx_locations_active_accepting ON locations(is_active, is_accepting_donations);

-- Create views for common queries
CREATE VIEW donor_stats AS
SELECT 
    u.id,
    u.username,
    u.email,
    u.first_name,
    u.last_name,
    u.blood_type,
    u.city,
    u.state,
    u.is_eligible,
    u.last_donation_date,
    COUNT(d.id) as total_donations,
    SUM(CASE WHEN d.status = 'completed' THEN d.quantity ELSE 0 END) as total_volume_donated,
    MAX(d.donation_date) as last_donation_date_actual
FROM users u
LEFT JOIN donations d ON u.id = d.user_id
WHERE u.role = 'donor' AND u.is_active = TRUE
GROUP BY u.id;

CREATE VIEW inventory_summary AS
SELECT 
    blood_type,
    current_stock,
    min_threshold,
    max_capacity,
    available_stock,
    reserved_stock,
    expired_stock,
    CASE 
        WHEN current_stock <= (min_threshold * 0.5) THEN 'critical'
        WHEN current_stock <= min_threshold THEN 'low'
        WHEN current_stock >= (max_capacity * 0.9) THEN 'high'
        ELSE 'normal'
    END as stock_status,
    last_updated
FROM blood_inventory;

-- Stored procedures for common operations
DELIMITER //

CREATE PROCEDURE GetDonationHistory(IN donor_id INT)
BEGIN
    SELECT 
        d.id,
        d.blood_type,
        d.quantity,
        d.donation_date,
        d.status,
        l.name as location_name,
        l.address as location_address
    FROM donations d
    LEFT JOIN locations l ON d.location_id = l.id
    WHERE d.user_id = donor_id
    ORDER BY d.donation_date DESC;
END //

CREATE PROCEDURE GetInventoryAlerts()
BEGIN
    SELECT 
        blood_type,
        current_stock,
        min_threshold,
        CASE 
            WHEN current_stock <= (min_threshold * 0.5) THEN 'critical'
            WHEN current_stock <= min_threshold THEN 'low'
            ELSE 'normal'
        END as alert_level
    FROM blood_inventory
    WHERE current_stock <= min_threshold
    ORDER BY current_stock ASC;
END //

DELIMITER ;

-- Create triggers for automatic updates
DELIMITER //

CREATE TRIGGER update_user_last_donation 
AFTER UPDATE ON donations
FOR EACH ROW
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        UPDATE users 
        SET last_donation_date = NEW.donation_date
        WHERE id = NEW.user_id;
    END IF;
END //

CREATE TRIGGER increment_location_donations
AFTER UPDATE ON donations
FOR EACH ROW
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        UPDATE locations 
        SET total_donations_collected = total_donations_collected + 1
        WHERE id = NEW.location_id;
    END IF;
END //

DELIMITER ;

-- Grant permissions (adjust as needed for your MySQL user)
-- GRANT ALL PRIVILEGES ON vitapink_bloodbank.* TO 'your_username'@'localhost';
-- FLUSH PRIVILEGES;

-- Show table structure
SHOW TABLES;

-- Display sample data
SELECT 'Users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'Locations', COUNT(*) FROM locations
UNION ALL
SELECT 'Donations', COUNT(*) FROM donations
UNION ALL
SELECT 'Blood Inventory', COUNT(*) FROM blood_inventory; 