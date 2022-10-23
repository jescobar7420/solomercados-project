import { Component, OnInit } from '@angular/core';
import { ProductosService } from 'src/app/services/productos.service';
import { ProductBestPrice } from 'src/app/interfaces/product-best-price';

@Component({
  selector: 'app-list-products',
  templateUrl: './list-products.component.html',
  styleUrls: ['./list-products.component.scss']
})
export class ListProductsComponent implements OnInit {

  ListaProductos = new Array<ProductBestPrice>();

  constructor(private http:ProductosService) {}

  ngOnInit(): void {
    this.http.GetListProductsBestPrice().subscribe(datos => {
      for(let i=0; i<datos.items.length && i<40; i++) {
        this.ListaProductos.push(datos.items[i]);
      }
    })
  }

  product_on_offer(precio_oferta:string) {
    if (precio_oferta == '999999999') {
      return false;
    }
    return true;
  }
  
  numberWithPoints(precio:string) {
    return precio.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }
}