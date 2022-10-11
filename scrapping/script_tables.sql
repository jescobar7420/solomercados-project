CREATE TABLE categorias (
    id_categoria  SERIAL NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    CONSTRAINT pk_categoria PRIMARY KEY (id_categoria)
);

CREATE TABLE marcas (
    id_marca  SERIAL NOT NULL,
    marca VARCHAR(255) NOT NULL,
    CONSTRAINT pk_marca PRIMARY KEY (id_marca)
);

CREATE TABLE tipos (
    id_tipo  SERIAL NOT NULL,
    tipo VARCHAR(255) NOT NULL,
    CONSTRAINT pk_tipo PRIMARY KEY (id_tipo)
);

CREATE TABLE productos (
    id_producto SERIAL NOT NULL,
    categoria INTEGER NOT NULL,
    marca INTEGER NOT NULL,
    tipo_producto INTEGER NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    imagen VARCHAR(255) NOT NULL,
    descripcion VARCHAR(8000) NOT NULL,
    ingredientes VARCHAR(8000) NOT NULL,
    CONSTRAINT pk_productos PRIMARY KEY (id_producto),
    CONSTRAINT fk_productos_categorias FOREIGN KEY (categoria) REFERENCES categorias(id_categoria)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_productos_marcas FOREIGN KEY (marca) REFERENCES marcas(id_marca)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_productos_tipos FOREIGN KEY (tipo_producto) REFERENCES tipos(id_tipo)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE supermercados (
    id_supermercado SERIAL NOT NULL,
    supermercado VARCHAR(255) NOT NULL,
    logo VARCHAR(255) NOT NULL,
    CONSTRAINT pk_supermercados PRIMARY KEY (id_supermercado)
);

CREATE TABLE supermercados_productos (
    id_supermercado INTEGER,
    id_producto INTEGER,
    precio_oferta VARCHAR(10),
    precio_normal VARCHAR(10),
    url_product VARCHAR(255) NOT NULL,
    fecha DATE DEFAULT to_date('1/1/1900','DD/MM/YYYY'),
    disponibilidad VARCHAR(3) NOT NULL,
    PRIMARY KEY (id_supermercado, id_producto),
    CONSTRAINT fk_supermercados_productos_supermercados FOREIGN KEY (id_supermercado) REFERENCES supermercados(id_supermercado)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_supermercados_productos_productos FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
    ON DELETE CASCADE ON UPDATE CASCADE
);