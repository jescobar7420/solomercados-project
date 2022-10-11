import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProductosService } from 'src/app/services/productos.service';
import { SupermercadosProductosService } from 'src/app/services/supermercados-productos.service';
import { SupermercadosProductos } from 'src/app/interfaces/supermercados-productos';

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss']
})
export class DetailsComponent implements OnInit {

  id_producto:any;
  Producto:any;
  ListaSuperProducto = new Array<SupermercadosProductos>();

  constructor(private route: ActivatedRoute, private httpProduct:ProductosService, private httpSuperProduct:SupermercadosProductosService) { 
    this.route.params.subscribe(datos => {
      this.id_producto = datos["id"]
    })
  }

  ngOnInit(): void {
    this.httpProduct.GetProducto(this.id_producto).subscribe(datos => {
      this.Producto = datos[0];
    })

    this.httpSuperProduct.GetListSuperProductsId(this.id_producto).subscribe(datos =>{
      for(let i=0; i<datos.items.length; i++) {
        this.ListaSuperProducto.push(datos.items[i]);
      }
    })
  }
  
  exists_ingredients(ingredients:string) {
    if (ingredients == 'No disponible') {
      return false
    }
    else {
      return true
    }
  }
}
