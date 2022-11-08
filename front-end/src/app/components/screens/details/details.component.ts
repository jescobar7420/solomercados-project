import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProductosService } from 'src/app/services/productos.service';
import { SupermercadosProductosService } from 'src/app/services/supermercados-productos.service';
import { SupermercadosProductos } from 'src/app/interfaces/supermercados-productos';
import { Product } from 'src/app/interfaces/product';

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss']
})
export class DetailsComponent implements OnInit {

  id_producto:any;
  Producto:Product;
  ListaSuperProducto = new Array<SupermercadosProductos>();
  flag_alert:boolean = false;

  constructor(private route: ActivatedRoute, private httpProduct:ProductosService, private httpSuperProduct:SupermercadosProductosService) { 
    this.route.params.subscribe(datos => {
      this.id_producto = datos["id"]
    })
    
    this.Producto = {
      id_producto: 0,
      categoria: '',
      marca: '',
      tipo_producto: '',
      nombre: '',
      imagen: '',
      descripcion: '',
      ingredientes: ''
    }
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
    return true
  }
  
  numberWithPoints(precio:string) {
    if (precio != '-') {
      return '$ ' + precio.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }
    return '-'
  }
  
  delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }
  
  async add_product_cart(id_producto:number, nombre:string, marca:string, imagen:string) {
    let products = JSON.parse(localStorage.getItem('cart')!)|| [];
    
    for(let i=0; i<products.length; i++) {
      if(products[i]['id_producto'] == id_producto) {
        products[i]['multiplicador'] = products[i]['multiplicador'] + 1;
        localStorage.setItem('cart', JSON.stringify(products));
        
        this.flag_alert = true;
        await this.delay(3000);
        this.flag_alert = false;
        return
      }
    }
    
    products.push({id_producto: id_producto, nombre: nombre, marca: marca, imagen: imagen, multiplicador: 1});
    localStorage.setItem('cart', JSON.stringify(products));
  }
}
