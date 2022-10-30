import { Component, OnInit } from '@angular/core';
import { ProductosService } from 'src/app/services/productos.service';
import { ProductBestPrice } from 'src/app/interfaces/product-best-price';
import { FilterService } from 'src/app/services/filter.service';
import { Categorias } from 'src/app/interfaces/categorias';

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.scss']
})
export class FilterComponent implements OnInit {

  ListaProductos = new Array<ProductBestPrice>();
  ListCategorias = new Array<Categorias>();

  constructor(private http_product:ProductosService,
              private http_filter:FilterService) {}

  ngOnInit(): void {
    this.http_product.GetListProductsBestPrice().subscribe(datos => {
      for(let i=0; i<datos.items.length && i<40; i++) {
        this.ListaProductos.push(datos.items[i]);
      }
    })
    
    this.http_filter.GetCategories().subscribe(datos => {
      for(let i=0; i<datos.items.length; i++) {
        this.ListCategorias.push(datos.items[i]);
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

  selectCategory(id:any) {
    console.log(id)
  }
  
  
}
