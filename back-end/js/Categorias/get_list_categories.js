"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const pool = require('../connect_database');
const GetListCategorias = (req, res) => {
    let ListaCategorias = new Array();
    let query = `SELECT id_categoria, categoria FROM categorias
                 WHERE categoria <> 'NA'
                 ORDER BY categoria ASC`;
    pool.query(query, (err, respuesta) => {
        if (err) {
            console.log(err);
            return;
        }
        for (let row of respuesta.rows) {
            ListaCategorias.push(row);
        }
        console.log(ListaCategorias);
        res.send(JSON.stringify({ "satus": "ok", "items": ListaCategorias }));
    });
};
module.exports = {
    GetListCategorias
};
