import { Component, OnInit } from '@angular/core';
import { ProductosService } from 'src/app/services/productos.service';
import { Product } from 'src/app/interfaces/product';

@Component({
  selector: 'app-buscar',
  templateUrl: './buscar.component.html',
  styleUrls: ['./buscar.component.scss']
})
export class BuscarComponent implements OnInit {

  ListaProductos = new Array<Product>();

  constructor(private http:ProductosService) { }

  ngOnInit(): void {
    this.http.GetListProductos().subscribe(datos => {
      for(let i=0; i<datos.items.length; i++) {
        this.ListaProductos.push(datos.items[i]);
      }
    })
  }

}
