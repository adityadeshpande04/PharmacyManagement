create database pharmacy;
show databases;
use pharmacy;
select database();

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE medications (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  dosage VARCHAR(50),
  manufacturer VARCHAR(100),
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE inventory (
  id INT PRIMARY KEY AUTO_INCREMENT,
  medication_id INT NOT NULL,
  quantity INT NOT NULL,
  expiration_date DATE,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  selling_price INT NOT NULL,
  FOREIGN KEY (medication_id) REFERENCES medications(id)
 );

CREATE TABLE sales_records (
  id INT PRIMARY KEY AUTO_INCREMENT,
  medication_id INT NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  date_sold DATE NOT NULL,
  first_name varchar(50),
  last_name varchar(50),
  FOREIGN KEY (medication_id) REFERENCES medications(id)
);

CREATE TABLE sales (
  id INT PRIMARY KEY AUTO_INCREMENT,
  sales_record_id INT NOT NULL,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sales_record_id) REFERENCES sales_records(id)
);