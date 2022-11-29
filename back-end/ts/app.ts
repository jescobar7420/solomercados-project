const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');

/* Imports GET */
const Producto = require('./Productos/get_producto');
const ListProducto = require('./Productos/get_list_products');
const ListCategorias = require('./Categorias/get_list_categories');
const ListSuperProducts = require('./Supermercados_Productos/get_list_product_id');
const Categoria = require('./Categorias/get_category');
const ListProductosCategoria = require('./Productos/get_list_products_category');
const ListProductsBestPrice = require('./Productos/get_list_products_best_price');
const Usuario = require('./Usuarios/get_user');
const ProductsFilter = require('./Filter/get_products_filter');
const TotalProductsFilter = require('./Filter/get_total_filter');
const ListSupermarkets = require('./Supermercados/get_supermarkets');
const ProductsCart = require('./Cart/get_products_cart');
const AllProductsName = require('./Productos/get_all_products_name');
const CotizacionesUsuario = require('./Cotizaciones/get_cotizaciones_user');
const CotizacionesProductos = require('./CotizacionesProductos/get_productos_cotizaciones');
const TotalCotizacionUser = require('./Cotizaciones/get_total_cotizaciones_user');
const MostViewProducts = require('./Productos/get_most_view_products_day');

/* Imports POST */
const InsertarUsuario = require('./Usuarios/post_user');
const Login = require('./Usuarios/post_login');
const BrandsFilter = require('./Filter/post_brands_filter');
const CategoriesFilter = require('./Filter/post_categories_filter');
const TypesFilter = require('./Filter/post_types_filter');
const InsertarCotizacion = require('./Cotizaciones/post_cotizacion');
const InsertarCotizacionProductos = require('./CotizacionesProductos/post_cotizaciones_productos');


const config = {
  hostname: "127.0.0.1",
  port: 3000,
};

app.use(cors());
app.use(bodyParser.json());

/* GET methods */
app.get('/Producto/:id', Producto.GetProducto);
app.get('/ListProductos', ListProducto.GetListProductos);
app.get('/ListCategorias', ListCategorias.GetListCategorias);
app.get('/ListSupermercadosProductos/:id', ListSuperProducts.GetListSuperProductsId);
app.get('/Categoria/:id', Categoria.GetCategory);
app.get('/ProductosCategoria/:id', ListProductosCategoria.GetListProductosCategoria);
app.get('/ListProductsBestPrice', ListProductsBestPrice.GetListProductsBestPrice);
app.get('/Usuario/:email', Usuario.GetUser);
app.get('/FilterProducts/:categoria/:marca/:tipo/:precio_inicial/:precio_final/:offset', ProductsFilter.GetProductsFilter);
app.get('/TotalFilter/:categoria/:marca/:tipo/:precio_inicial/:precio_final', TotalProductsFilter.GetTotalProductsFilter);
app.get('/Supermarkets', ListSupermarkets.GetSupermarkets);
app.get('/ProductsCart/:ids', ProductsCart.GetProductsCart);
app.get('/AllProductsName/:search', AllProductsName.GetAllProductsName);
app.get('/CotizacionesUsuario/:id/:offset', CotizacionesUsuario.GetCotizacionesUsuario);
app.get('/CotizacionesProductos/:id', CotizacionesProductos.GetCotizacionProductos);
app.get('/TotalCotizacionesUser/:id', TotalCotizacionUser.GetTotalCotizacionUser);
app.get('/MostViewProductos', MostViewProducts.GetMostViewProductsDay);


/* POST methods */
app.post('/InsertarUsuario', bodyParser.json(), InsertarUsuario.PostUsuario);
app.post('/Login', bodyParser.json(), Login.PostLogin);
app.post('/FilterBrand', bodyParser.json(), BrandsFilter.PostBrandsFilter);
app.post('/FilterCategory', bodyParser.json(), CategoriesFilter.PostCategoriesFilter);
app.post('/FilterType', bodyParser.json(), TypesFilter.PostTypesFilter);
app.post('/InsertarCotizacion', bodyParser.json(), InsertarCotizacion.PostCotizacion);
app.post('/InsertarCotizacionProductos', bodyParser.json(), InsertarCotizacionProductos.PostCotizacionesProductos);


app.listen(config, () =>{
    console.log(`Conectando al servidor http://${config.hostname}:${config.port}`);
});

