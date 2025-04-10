CREATE TABLE mids (
    mid VARCHAR(255) PRIMARY KEY,
    issue_date DATETIME,
    deposit FLOAT,
    expire_date DATETIME
);

CREATE TABLE suns (
    sun VARCHAR(255) PRIMARY KEY,
    mid VARCHAR(255),
    expire_date DATETIME
);

CREATE TABLE terminals (
    id INT(10) AUTO_INCREMENT PRIMARY KEY,
    terminal_id VARCHAR(255),
    service_area VARCHAR(255),
    serverURL VARCHAR(255),
    controlMIDnumber VARCHAR(255),
    controlSUNnumber VARCHAR(255),
    auth VARCHAR(255),
    ifservernoreaction VARCHAR(255),
    servicetype VARCHAR(255),
    serviceprice VARCHAR(255),
    etc VARCHAR(255),
    last_access TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

