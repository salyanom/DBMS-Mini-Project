DROP DATABASE IF EXISTS car_dealership;
CREATE DATABASE car_dealership;
USE car_dealership;

CREATE TABLE Manufacturer (
    manufacturer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100)
);

CREATE TABLE Admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    passw VARCHAR(255) NOT NULL
);

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    passw VARCHAR(255) NOT NULL
);

CREATE TABLE Salesperson (
    salesperson_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    hire_date DATE,
    username VARCHAR(50) NOT NULL UNIQUE,
    passw VARCHAR(255) NOT NULL
);

CREATE TABLE Model (
    model_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    manufacturer_id INT,
    CONSTRAINT fk_manufacturer FOREIGN KEY (manufacturer_id) REFERENCES Manufacturer(manufacturer_id)
);

CREATE TABLE Car (
    car_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    year YEAR,
    colour VARCHAR(30),
    mileage INT,
    price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Available',
    customer_id INT NULL,
    salesperson_id INT NULL,
    CONSTRAINT fk_model FOREIGN KEY (model_id) REFERENCES Model(model_id),
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    CONSTRAINT fk_salesperson FOREIGN KEY (salesperson_id) REFERENCES Salesperson(salesperson_id)
);

CREATE TABLE CustomerPhone (
    customer_id INT,
    phone VARCHAR(20),
    PRIMARY KEY (customer_id, phone),
    CONSTRAINT fk_customer_phone FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE CustomerEmail (
    customer_id INT,
    email VARCHAR(100),
    PRIMARY KEY (customer_id, email),
    CONSTRAINT fk_customer_email FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE SalespersonPhone (
    salesperson_id INT,
    phone VARCHAR(20),
    PRIMARY KEY (salesperson_id, phone),
    CONSTRAINT fk_salesperson_phone FOREIGN KEY (salesperson_id) REFERENCES Salesperson(salesperson_id)
);

CREATE TABLE SalespersonEmail (
    salesperson_id INT,
    email VARCHAR(100),
    PRIMARY KEY (salesperson_id, email),
    CONSTRAINT fk_salesperson_email FOREIGN KEY (salesperson_id) REFERENCES Salesperson(salesperson_id)
);

CREATE TABLE SalesLog (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    car_id INT NOT NULL,
    customer_id INT,
    salesperson_id INT,
    sale_price DECIMAL(10, 2),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



INSERT INTO Manufacturer (name, country) VALUES
('Toyota', 'Japan'),
('Ford', 'USA'),
('Volkswagen', 'Germany'),
('Honda', 'Japan'),
('BMW', 'Germany'),
('Hyundai', 'South Korea'),
('Maruti Suzuki', 'India');

INSERT INTO Admin (username, passw) VALUES
('superadmin', 'adminpass123'),
('data_manager', 'managerpass');

INSERT INTO Customer (first_name, last_name, username, passw) VALUES
('Rohan', 'Sharma', 'rohan_s', 'pass1'),
('Priya', 'Singh', 'priya_s', 'pass2'),
('Anita', 'Desai', 'anita_d', 'pass3'),
('Vikram', 'Rathod', 'vikram_r', 'pass4'),
('Sneha', 'Reddy', 'sneha_r', 'pass5');

INSERT INTO Salesperson (first_name, last_name, hire_date, username, passw) VALUES
('Amit', 'Patel', '2023-05-15', 'amit_p', 'spass1'),
('Sunita', 'Gupta', '2022-08-20', 'sunita_g', 'spass2'),
('Pooja', 'Sharma', '2024-01-10', 'pooja_s', 'spass3');

INSERT INTO Model (name, manufacturer_id) VALUES
('Camry', 1),       -- Toyota
('Fortuner', 1),    -- Toyota
('Mustang', 2),     -- Ford
('Golf', 3),        -- Volkswagen
('Polo', 3),        -- Volkswagen
('Civic', 4),       -- Honda
('X5', 5),          -- BMW
('3 Series', 5),    -- BMW
('Creta', 6),       -- Hyundai
('Swift', 7);      -- Maruti Suzuki

INSERT INTO Car (model_id, year, colour, mileage, price, status, customer_id, salesperson_id) VALUES
(1, '2024', 'Blue', 150, 2500000.00, 'Sold', 1, 1),       -- Camry sold to Rohan by Amit
(3, '2023', 'Red', 500, 4500000.00, 'Available', NULL, NULL),  -- Mustang is available
(4, '2022', 'Black', 12000, 2200000.00, 'Sold', 2, 1),      -- Golf sold to Priya by Amit
(6, '2024', 'White', 20, 1800000.00, 'Sold', 3, 2),       -- Civic sold to Anita by Sunita
(7, '2023', 'Grey', 8000, 8500000.00, 'Available', NULL, NULL), -- BMW X5 is available
(9, '2023', 'Silver', 25000, 1400000.00, 'Sold', 4, 3),      -- Creta sold to Vikram by Pooja
(10, '2024', 'Red', 10, 850000.00, 'Available', NULL, NULL),   -- Swift is available
(2, '2022', 'Black', 45000, 3500000.00, 'Available', NULL, NULL); -- Fortuner is available

INSERT INTO CustomerPhone (customer_id, phone) VALUES
(1, '9876543210'),
(2, '8765432109'),
(3, '7654321098'),
(4, '6543210987'),
(4, '6543210988'), -- Vikram has a second number
(5, '5432109876');

INSERT INTO CustomerEmail (customer_id, email) VALUES
(1, 'rohan.s@email.com'),
(2, 'priya.singh@email.com'),
(3, 'anita.d@email.com'),
(4, 'vikram.r@email.com'),
(5, 'sneha.reddy@email.com');

INSERT INTO SalespersonPhone (salesperson_id, phone) VALUES
(1, '7890123456'),
(1, '7890123457'), -- Amit has two numbers
(2, '8901234567'),
(3, '9012345678');

INSERT INTO SalespersonEmail (salesperson_id, email) VALUES
(1, 'amit.patel@cars.com'),
(2, 'sunita.g@cars.com'),
(3, 'pooja.s@cars.com');


-- --- 3. ORIGINAL QUERIES (Views, Alters) ---
.
ALTER TABLE Car DROP FOREIGN KEY fk_model;

ALTER TABLE Car ADD insurance_provider VARCHAR(100);


CREATE VIEW FullModelDetails AS
SELECT
    M.name AS model_name,
    Man.name AS manufacturer_name,
    Man.country
FROM
    Model M
JOIN
    Manufacturer Man ON M.manufacturer_id = Man.manufacturer_id;
    



DELIMITER //

-- FUNCTION 1: Get Total Sales Amount for a Salesperson
CREATE FUNCTION GetSalespersonTotalSales(sp_id INT)
RETURNS DECIMAL(12, 2)
READS SQL DATA
BEGIN
    DECLARE total_sales DECIMAL(12, 2);
    
    SELECT IFNULL(SUM(price), 0)
    INTO total_sales
    FROM Car
    WHERE salesperson_id = sp_id AND status = 'Sold';
    
    RETURN total_sales;
END //

-- FUNCTION 2: Count Available Cars by Manufacturer
CREATE FUNCTION CountAvailableCarsByManufacturer(mf_name VARCHAR(100))
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE car_count INT;
    
    SELECT COUNT(c.car_id)
    INTO car_count
    FROM Car c
    JOIN Model m ON c.model_id = m.model_id
    JOIN Manufacturer mf ON m.manufacturer_id = mf.manufacturer_id
    WHERE mf.name = mf_name AND c.status = 'Available';
    
    RETURN car_count;
END //

-- TRIGGER 1: Log Car Sale
CREATE TRIGGER LogCarSale
AFTER UPDATE ON Car
FOR EACH ROW
BEGIN
    -- Fire only when the status changes to 'Sold'
    IF NEW.status = 'Sold' AND OLD.status != 'Sold' THEN
        INSERT INTO SalesLog (car_id, customer_id, salesperson_id, sale_price)
        VALUES (NEW.car_id, NEW.customer_id, NEW.salesperson_id, NEW.price);
    END IF;
END //

-- TRIGGER 2: Check Sale Prerequisites
CREATE TRIGGER CheckSalePrerequisites
BEFORE UPDATE ON Car
FOR EACH ROW
BEGIN
    IF NEW.status = 'Sold' AND (NEW.customer_id IS NULL OR NEW.salesperson_id IS NULL) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'A car cannot be marked as "Sold" without a valid customer_id and salesperson_id.';
    END IF;
END //

-- PROCEDURE 1: Sell a Car
CREATE PROCEDURE SellCar(IN c_id INT, IN cust_id INT, IN sp_id INT)
BEGIN
    DECLARE current_status VARCHAR(20);
    
    -- Check if the car is available
    SELECT status INTO current_status
    FROM Car
    WHERE car_id = c_id;
    
    IF current_status = 'Available' THEN
        -- Sell the car. This will fire the CheckSalePrerequisites
        -- and LogCarSale triggers automatically.
        UPDATE Car
        SET 
            status = 'Sold',
            customer_id = cust_id,
            salesperson_id = sp_id
        WHERE car_id = c_id;
        
        SELECT 'Car sold successfully.' AS message;
    ELSE
        SELECT 'Car is not available for sale or does not exist.' AS message;
    END IF;
END //

-- PROCEDURE 2: Search Available Cars
CREATE PROCEDURE SearchAvailableCars(
    IN max_price_in DECIMAL(10, 2), 
    IN mf_name_in VARCHAR(100), 
    IN model_name_in VARCHAR(100)
)
BEGIN
    SELECT
        mf.name AS Manufacturer,
        m.name AS Model,
        c.year AS Year,
        c.colour AS Colour,
        c.mileage AS Mileage,
        c.price AS Price
    FROM Car c
    JOIN Model m ON c.model_id = m.model_id
    JOIN Manufacturer mf ON m.manufacturer_id = mf.manufacturer_id
    WHERE c.status = 'Available'
    -- Use IS NULL checks to make parameters optional
    AND (c.price <= max_price_in OR max_price_in IS NULL)
    AND (mf.name = mf_name_in OR mf_name_in IS NULL)
    AND (m.name = model_name_in OR model_name_in IS NULL);
END //


-- --- 5. PROCEDURES FOR STREAMLIT APP ---

-- Procedure to add a new customer (for Signup and Admin)
CREATE PROCEDURE AddCustomer(
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_username VARCHAR(50),
    IN p_passw VARCHAR(255),
    IN p_phone VARCHAR(20),
    IN p_email VARCHAR(100)
)
BEGIN
    DECLARE new_customer_id INT;

    -- Insert into the main Customer table
    INSERT INTO Customer (first_name, last_name, username, passw)
    VALUES (p_first_name, p_last_name, p_username, p_passw);
    
    -- Get the new customer_id that was auto-incremented
    SET new_customer_id = LAST_INSERT_ID();
    
    -- Insert into the multi-valued attribute tables
    INSERT INTO CustomerPhone (customer_id, phone) VALUES (new_customer_id, p_phone);
    INSERT INTO CustomerEmail (customer_id, email) VALUES (new_customer_id, p_email);
END //


-- Procedure to add a new salesperson (for Admin)
CREATE PROCEDURE AddSalesperson(
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_hire_date DATE,
    IN p_username VARCHAR(50),
    IN p_passw VARCHAR(255),
    IN p_phone VARCHAR(20),
    IN p_email VARCHAR(100)
)
BEGIN
    DECLARE new_salesperson_id INT;

    INSERT INTO Salesperson (first_name, last_name, hire_date, username, passw)
    VALUES (p_first_name, p_last_name, p_hire_date, p_username, p_passw);
    
    SET new_salesperson_id = LAST_INSERT_ID();
    
    INSERT INTO SalespersonPhone (salesperson_id, phone) VALUES (new_salesperson_id, p_phone);
    INSERT INTO SalespersonEmail (salesperson_id, email) VALUES (new_salesperson_id, p_email);
END //


-- Procedure to let a salesperson buy a car FROM a customer
CREATE PROCEDURE SellCarToDealership(
    IN p_customer_id INT,
    IN p_model_id INT,
    IN p_year YEAR,
    IN p_mileage INT,
    IN p_colour VARCHAR(30),
    IN p_price DECIMAL(10, 2),
    IN p_salesperson_id INT
)
BEGIN
    -- Add the car to the inventory
    INSERT INTO Car (model_id, year, colour, mileage, price, status, salesperson_id)
    VALUES (p_model_id, p_year, p_colour, p_mileage, p_price, 'Available', p_salesperson_id);
    
    -- We could log this transaction, but for now, just adding the car is enough.
END //


-- Procedure to reserve a car for a customer
CREATE PROCEDURE ReserveCarForCustomer(
    IN p_car_id INT,
    IN p_customer_id INT
)
BEGIN
    UPDATE Car
    SET 
        status = 'Reserved',
        customer_id = p_customer_id
    WHERE 
        car_id = p_car_id AND status = 'Available';
END //


-- Procedure for a customer to update their own info (multi-valued tables)
CREATE PROCEDURE UpdateCustomerInfo(
    IN p_customer_id INT,
    IN p_new_email VARCHAR(100),
    IN p_new_phone VARCHAR(20)
)
BEGIN
    IF p_new_email IS NOT NULL THEN
        INSERT INTO CustomerEmail (customer_id, email)
        VALUES (p_customer_id, p_new_email)
        ON DUPLICATE KEY UPDATE email = p_new_email; -- Handles if it already exists
    END IF;
    
    IF p_new_phone IS NOT NULL THEN
        INSERT INTO CustomerPhone (customer_id, phone)
        VALUES (p_customer_id, p_new_phone)
        ON DUPLICATE KEY UPDATE phone = p_new_phone; -- Handles if it already exists
    END IF;
END //


-- Procedure for a salesperson to update their profile
CREATE PROCEDURE UpdateSalesperson(
    IN p_salesperson_id INT,
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_hire_date DATE,
    IN p_username VARCHAR(50),
    IN p_passw VARCHAR(255),
    IN p_phone VARCHAR(20),
    IN p_email VARCHAR(100)
)
BEGIN
    -- Update main table
    UPDATE Salesperson
    SET
        first_name = p_first_name,
        last_name = p_last_name,
        hire_date = p_hire_date,
        username = p_username,
        passw = p_passw
    WHERE salesperson_id = p_salesperson_id;
    
    -- Update multi-valued tables (simple version: add/update)
    INSERT INTO SalespersonPhone (salesperson_id, phone)
    VALUES (p_salesperson_id, p_phone)
    ON DUPLICATE KEY UPDATE phone = p_phone;
    
    INSERT INTO SalespersonEmail (salesperson_id, email)
    VALUES (p_salesperson_id, p_email)
    ON DUPLICATE KEY UPDATE email = p_email;
END //


-- Function to get total cars sold (for Admin report)
CREATE FUNCTION GetTotalCarsSold(sp_id INT)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE car_count INT;
    
    SELECT COUNT(car_id)
    INTO car_count
    FROM Car
    WHERE salesperson_id = sp_id AND status = 'Sold';
    
    RETURN IFNULL(car_count, 0);
END //

DELIMITER ;