"use strict";
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const Producto = require('./Productos/get_producto');
const ListProducto = require('./Productos/get_list_products');
const ListCategorias = require('./Categorias/get_list_categories');
const ListSuperProducts = require('./Supermercados_Productos/get_list_product_id');
const Categoria = require('./Categorias/get_category');
const ListProductosCategoria = require('./Productos/get_list_products_category');
const config = {
    hostname: "127.0.0.1",
    port: 3000,
};
app.use(cors());
app.use(bodyParser.json());
app.get('/Producto/:id', Producto.GetProducto);
app.get('/ListProductos', ListProducto.GetListProductos);
app.get('/ListCategorias', ListCategorias.GetListCategorias);
app.get('/ListSupermercadosProductos/:id', ListSuperProducts.GetListSuperProductsId);
app.get('/Categoria/:id', Categoria.GetCategory);
app.get('/ProductosCategoria/:id', ListProductosCategoria.GetListProductosCategoria);
app.listen(config, () => {
    console.log(`Conectando al servidor http://${config.hostname}:${config.port}`);
});
