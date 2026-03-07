CREATE DATABASE autopartes_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE autopartes_db;

-- 1. Gestión de Accesos
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(150)
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_usuarios_roles
        FOREIGN KEY (rol_id)
        REFERENCES roles(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 2. Catálogo de Productos
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(150)
);

CREATE TABLE autopartes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    categoria_id INT NOT NULL,
    marca VARCHAR(100),
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_autopartes_categorias
        FOREIGN KEY (categoria_id)
        REFERENCES categorias(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 3. Control de Existencias
CREATE TABLE inventarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    autoparte_id INT NOT NULL UNIQUE,
    stock_actual INT NOT NULL CHECK (stock_actual >= 0),
    stock_minimo INT NOT NULL CHECK (stock_minimo >= 0),
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inventarios_autopartes
        FOREIGN KEY (autoparte_id)
        REFERENCES autopartes(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 4. Gestión de Pedidos
CREATE TABLE estados_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    estado_id INT NOT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    CONSTRAINT fk_pedidos_usuarios
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_pedidos_estados
        FOREIGN KEY (estado_id)
        REFERENCES estados_pedido(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE detalle_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    autoparte_id INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
    CONSTRAINT fk_detalle_pedido_pedidos
        FOREIGN KEY (pedido_id)
        REFERENCES pedidos(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_detalle_pedido_autopartes
        FOREIGN KEY (autoparte_id)
        REFERENCES autopartes(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT uk_pedido_autoparte UNIQUE (pedido_id, autoparte_id)
);


-- 1. Inserción de Estados Base
INSERT INTO estados_pedido (nombre)
VALUES ('Recibido'), ('Surtido'), ('Enviado');

-- 2. Creamos el primer rol
INSERT INTO roles (nombre, descripcion) VALUES ('Administrador', 'Acceso total al sistema');

-- 3. Creamos tu usuario administrador (El rol será el ID 1)
-- Nota: Por ahora nuestra API solo verifica que el correo exista, 
-- más adelante activaremos la validación del hash de la contraseña.
INSERT INTO usuarios (nombre, email, password_hash, rol_id, activo, fecha_registro) 
VALUES ('Andrés Castillo', 'andres@macuin.com', 'hash_falso_por_ahora', 1, 1, NOW());

-- 4. Creación de categoría
INSERT INTO categorias (nombre, descripcion) VALUES ('Motor y Transmisión', 'Piezas mecánicas principales');

-- 5. Creación de pedido asegurando existencia de autoparte existente
INSERT INTO autopartes (nombre, descripcion, categoria_id, marca, precio) 
VALUES ('Bomba de Agua', 'Bomba de alta presión para sistema de enfriamiento', 1, 'Gates', 1200.00);

-- Guardamos el ID de la autoparte para los siguientes pasos
SET @id_pieza = LAST_INSERT_ID();

INSERT INTO inventarios (autoparte_id, stock_actual, stock_minimo) 
VALUES (@id_pieza, 25, 5);

INSERT INTO pedidos (usuario_id, estado_id, total) 
VALUES (1, 1, 2400.00);

-- Guardamos el ID del pedido para el detalle
SET @id_pedido = LAST_INSERT_ID();

INSERT INTO detalle_pedido (pedido_id, autoparte_id, cantidad, precio_unitario) 
VALUES (@id_pedido, @id_pieza, 2, 1200.00);


SELECT * FROM inventarios;
