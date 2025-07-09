CREATE DATABASE IF NOT EXISTS login_db;
USE login_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  phone VARCHAR(50),
  username VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

INSERT INTO users (first_name, last_name, email, phone, username, password)
VALUES ('Admin', 'General', 'admin@mail.com', '0999999999', 'admin', '$2b$12$8YrjDQWJj9clX..0K2B1xOgQntcUEobdYJjLzCET0jGkmN4EPzKme');
