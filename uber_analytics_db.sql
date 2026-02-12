-- Create database
CREATE DATABASE uber_analytics_db;
USE uber_analytics_db;

select * from rides;

-- Create rides table
CREATE TABLE rides (
    ride_id INT AUTO_INCREMENT PRIMARY KEY,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    category VARCHAR(50),
    start_location VARCHAR(255),
    end_location VARCHAR(255),
    miles DECIMAL(10, 2),
    purpose VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table (for login system)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_type ENUM('rider', 'driver', 'admin') DEFAULT 'rider',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create drivers table
CREATE TABLE drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    total_rides INT DEFAULT 0,
    total_miles DECIMAL(10, 2) DEFAULT 0,
    rating DECIMAL(3, 2) DEFAULT 5.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 1. Total rides by category
SELECT category, COUNT(*) as total_rides, 
       ROUND(AVG(miles), 2) as avg_miles
FROM rides
GROUP BY category
ORDER BY total_rides DESC;

-- 2. Busiest hours of the day
SELECT HOUR(start_date) as hour, COUNT(*) as ride_count
FROM rides
GROUP BY hour
ORDER BY hour;

-- 3. Most popular routes
SELECT start_location, end_location, 
       COUNT(*) as frequency,
       ROUND(AVG(miles), 2) as avg_distance
FROM rides
GROUP BY start_location, end_location
HAVING frequency > 5
ORDER BY frequency DESC
LIMIT 10;

-- 4. Rides by day of week
SELECT DAYNAME(start_date) as day_name, 
       COUNT(*) as total_rides
FROM rides
GROUP BY day_name
ORDER BY FIELD(day_name, 'Monday', 'Tuesday', 'Wednesday', 
               'Thursday', 'Friday', 'Saturday', 'Sunday');

-- 5. Monthly ride trends
SELECT DATE_FORMAT(start_date, '%Y-%m') as month,
       COUNT(*) as total_rides,
       ROUND(SUM(miles), 2) as total_miles
FROM rides
GROUP BY month
ORDER BY month;

-- 6. Peak demand prediction data
SELECT DATE(start_date) as ride_date,
       HOUR(start_date) as ride_hour,
       COUNT(*) as ride_count
FROM rides
GROUP BY ride_date, ride_hour
ORDER BY ride_date, ride_hour;

-- Create database
CREATE DATABASE uber_analytics_db;
USE uber_analytics_db;

select * from rides;

-- Create rides table
CREATE TABLE rides (
    ride_id INT AUTO_INCREMENT PRIMARY KEY,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    category VARCHAR(50),
    start_location VARCHAR(255),
    end_location VARCHAR(255),
    miles DECIMAL(10, 2),
    purpose VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table (for login system)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_type ENUM('rider', 'driver', 'admin') DEFAULT 'rider',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create drivers table
CREATE TABLE drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    vehicle_number VARCHAR(20),
    vehicle_model VARCHAR(50),
    city VARCHAR(50),
    join_date DATE,
    rating DECIMAL(3,2) DEFAULT 5.00,
    total_rides INT DEFAULT 0,
    total_miles DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from rides;
describe drivers;

INSERT INTO drivers (driver_name, phone, vehicle_number, vehicle_model, city, join_date, rating)
VALUES
('Santhosh', '8610763961', 'TN94C7507', 'TVS Rider', 'Chennai', '2025-06-15', 4.85),
('Kumar',  '8438640798', 'TN34X0834', 'Honda Activa', 'Chennai', '2024-01-10', 4.75);

select * from drivers;

ALTER TABLE rides ADD COLUMN driver_id INT;

-- Example: assign all current rides to driver 1


UPDATE rides SET driver_id = 1;

-- Driver-wise stats
SELECT d.driver_name,
       COUNT(r.ride_id) AS total_rides,
       SUM(r.miles) AS total_miles
FROM drivers d
LEFT JOIN rides r ON d.driver_id = r.driver_id
GROUP BY d.driver_id, d.driver_name;

-- 1. Total rides by category
SELECT category, COUNT(*) as total_rides, 
       ROUND(AVG(miles), 2) as avg_miles
FROM rides
GROUP BY category
ORDER BY total_rides DESC;

-- 2. Busiest hours of the day
SELECT HOUR(start_date) as hour, COUNT(*) as ride_count
FROM rides
GROUP BY hour
ORDER BY hour;

-- 3. Most popular routes
SELECT start_location, end_location, 
       COUNT(*) as frequency,
       ROUND(AVG(miles), 2) as avg_distance
FROM rides
GROUP BY start_location, end_location
HAVING frequency > 5
ORDER BY frequency DESC
LIMIT 10;

-- 4. Rides by day of week
SELECT DAYNAME(start_date) as day_name, 
       COUNT(*) as total_rides
FROM rides
GROUP BY day_name
ORDER BY FIELD(day_name, 'Monday', 'Tuesday', 'Wednesday', 
               'Thursday', 'Friday', 'Saturday', 'Sunday');

-- 5. Monthly ride trends
SELECT DATE_FORMAT(start_date, '%Y-%m') as month,
       COUNT(*) as total_rides,
       ROUND(SUM(miles), 2) as total_miles
FROM rides
GROUP BY month
ORDER BY month;

-- 6. Peak demand prediction data
SELECT DATE(start_date) as ride_date,
       HOUR(start_date) as ride_hour,
       COUNT(*) as ride_count
FROM rides
GROUP BY ride_date, ride_hour
ORDER BY ride_date, ride_hour;

