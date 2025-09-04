-- Create database
CREATE DATABASE IF NOT EXISTS LostAndFound;
USE LostAndFound;

-- Registered students (controls who can register)
CREATE TABLE IF NOT EXISTS registered_students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100)
);

-- Users (students/admins)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_number VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role ENUM('student', 'admin') DEFAULT 'student',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Items
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    category ENUM('Accessories','Cards','Clothing','Electronics','Others') NOT NULL,
    status ENUM('lost','found','claimed') NOT NULL DEFAULT 'lost',
    location VARCHAR(255) NULL,
    contact_phone VARCHAR(100),
    image_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


select * from logs;


-- Logs
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,
    old_status ENUM('lost','found','claimed'),
    new_status ENUM('lost','found','claimed'),
    changed_by INT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (changed_by) REFERENCES users(id)
);

-- Insert sample registered students
INSERT INTO registered_students (student_number, name, email) VALUES
('202215553', 'Tumelo Reiners', '202215553@spu.ac.za'),
('202100860', 'Walefa Bosele', '202100860@spu.ac.za'),
('202204500', 'Mothibi Isaac Bantjies', '202204500@spu.ac.za'),
('202204682', 'Amogelang Plaatje', '202204682@spu.ac.za');

;
