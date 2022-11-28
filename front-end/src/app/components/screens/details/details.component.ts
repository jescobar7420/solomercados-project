import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProductosService } from 'src/app/services/productos.service';
import { SupermercadosProductosService } from 'src/app/services/supermercados-productos.service';
import { SupermercadosProductos } from 'src/app/interfaces/supermercados-productos';
import { Product } from 'src/app/interfaces/product';
import Swal from 'sweetalert2';

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
    this.cambioDeRuta();
  }
  
  get_product():void {
    this.httpProduct.GetProducto(this.id_producto).subscribe(datos => {
      this.Producto = datos[0];
    })
  }
  
  get_list_supermarket(): void {
    this.ListaSuperProducto = [];
    this.httpSuperProduct.GetListSuperProductsId(this.id_producto).subscribe(datos =>{
      for(let i=0; i<datos.items.length; i++) {
        this.ListaSuperProducto.push(datos.items[i]);
        this.ListaSuperProducto[i].fecha = this.convert_date(datos.items[i].fecha)
      }
    })
  }
  
  onImgError(event:any) { 
    event.target.src = '../../../assets/icon-alert.png';
  }
  
  convert_date(fecha:Date) {
    var new_fecha = new Date(fecha);
    var dd = String(new_fecha.getDate()).padStart(2, '0');
    var mm = String(new_fecha.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = String(new_fecha.getFullYear());
    return dd + '/' + mm + '/' + yyyy;
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
    const Toast = Swal.mixin({
      toast: true,
      position: 'bottom-end',
      showConfirmButton: false,
      background: '#ededed',
      color: '#575757',
      timer: 2500,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
      }
    })
    
    Toast.fire({
      icon: 'success',
      title: 'Agregado con éxito.',
      text: nombre
    })
  
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
  
  cambioDeRuta(): void {
    this.route.params.subscribe(params => {
      this.id_producto = params['id'];
      this.get_product();
      this.get_list_supermarket();
   });
  }
}
