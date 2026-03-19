-- CREATE DATABASE acapulco_api;

-- USE acapulco_api;

CREATE TABLE eventos(

id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(150),
descripcion TEXT,
lugar VARCHAR(150),
hora TIME,
fecha DATE

);

CREATE TABLE api_stats(

id INT AUTO_INCREMENT PRIMARY KEY,
endpoint VARCHAR(100),
formato VARCHAR(20),
ip VARCHAR(50),
username VARCHAR(50),
fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE usuarios(

id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(50) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
rol VARCHAR(20) DEFAULT 'consumidor',
api_key VARCHAR(100) UNIQUE NULL

);

INSERT INTO usuarios(username, password, rol, api_key) VALUES
('adminapiaca', '654321', 'admin', 'admin_secret_key_123');

