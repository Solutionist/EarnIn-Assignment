CREATE TABLE IF NOT EXISTS flights (
    id VARCHAR(8) NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    departure_airport VARCHAR(3) NOT NULL,
    arrival_airport VARCHAR(3) NOT NULL,
    departure_timezone VARCHAR(30) NOT NULL,
    arrival_timezone VARCHAR(30) NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    passport_id VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- Not needed since passport_id is already unique (created in the table definition)
-- CREATE UNIQUE INDEX IF EXISTS customers__passport_id_idx ON customers (passport_id);


CREATE TABLE IF NOT EXISTS passengers (
    flight_id VARCHAR(8) NOT NULL REFERENCES flights(id),
    customer_id INT NOT NULL REFERENCES customers(id),
    PRIMARY KEY (flight_id, customer_id)
);

-- Test flights with IDs matching test scenario numbers
-- Tests 1, 2, 5, 6, 7: Booking operations (LHR -> BKK, different timezones)
INSERT INTO flights VALUES('AA001', '2024-12-01T10:00:00Z', '2024-12-01T14:00:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok');
INSERT INTO flights VALUES('AA002', '2024-12-01T10:00:00Z', '2024-12-01T14:00:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok');
INSERT INTO flights VALUES('AA005', '2024-12-01T10:00:00Z', '2024-12-01T14:00:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok');
INSERT INTO flights VALUES('AA006', '2024-12-01T10:00:00Z', '2024-12-01T14:00:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok');
INSERT INTO flights VALUES('AA007', '2024-12-01T10:00:00Z', '2024-12-01T14:00:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok');
-- Test 3: Different timezones (LHR -> BKK, different timezones)
INSERT INTO flights VALUES('AA003', '2024-12-01T10:00:00Z', '2024-12-01T18:00:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok');
-- Test 4: Same timezone (DMK -> BKK, both Asia/Bangkok)
INSERT INTO flights VALUES('AA004', '2024-12-01T08:00:00Z', '2024-12-01T10:00:00Z', 'DMK', 'BKK', 'Asia/Bangkok', 'Asia/Bangkok');