import { Producto } from "../interfaces/Producto";

const pool = require('../connect_database');

const GetProducto = (req: any, res: any) => {
    const id = parseInt(req.params.id);
    let Producto:Producto;
    let query = `SELECT * FROM productos WHERE id_producto = $1`;
    
    pool.query(query, [id], (err: any, response: any) => {
        if(err) {
            console.log(err);
            return;
        }
        
        Producto = response.rows;
        console.log(Producto);
        
        res.send(JSON.stringify(Producto))
    })
}

module.exports = { 
    GetProducto 
}