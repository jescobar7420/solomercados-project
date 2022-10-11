import { Component, OnInit } from '@angular/core';
import { ProductosService } from 'src/app/services/productos.service';
import { CategoriasService } from 'src/app/services/categorias.service';
import { Product } from 'src/app/interfaces/product';
import { Categorias } from 'src/app/interfaces/categorias';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.scss']
})
export class FilterComponent implements OnInit {

  id_category:any;
  ListaProductos = new Array<Product>();
  Categoria:any;

  constructor(private route: ActivatedRoute, private httpProducts:ProductosService, private httpCategory:CategoriasService) { 
    this.route.params.subscribe(datos => {
      this.id_category = datos["id"]
    })
  }

  ngOnInit(): void {
    this.httpProducts.GetListProductsCategory(this.id_category).subscribe(datos => {
      for(let i=0; i<datos.items.length && i<40; i++) {
        this.ListaProductos.push(datos.items[i]);
      }
    })
    
    this.httpCategory.GetCategory(this.id_category).subscribe(datos => {
      this.Categoria = datos[0];
    })
  }

}
