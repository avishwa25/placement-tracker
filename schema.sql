CREATE DATABASE IF NOT EXISTS placement_tracker;
USE placement_tracker;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    company_name VARCHAR(120) NOT NULL,
    job_role VARCHAR(120) NOT NULL,
    job_link VARCHAR(255),
    status ENUM('Applied','Shortlisted','Interview','Offer','Rejected') DEFAULT 'Applied',
    applied_on DATE,
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);