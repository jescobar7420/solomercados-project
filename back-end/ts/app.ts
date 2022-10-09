const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');

const Producto = require('./Productos/get_producto');
const ListProducto = require('./Productos/get_list_products');

const config = {
  hostname: "127.0.0.1",
  port: 3000,
}

app.use(cors());
app.use(bodyParser.json());

app.get('/Producto/:id', Producto.GetProducto);
app.get('/ListProductos', ListProducto.GetListProductos);

app.listen(config, () =>{
    console.log(`Conectando al servidor http://${config.hostname}:${config.port}`);
});

