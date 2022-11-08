import { Component, OnInit } from '@angular/core';
import { Supermarket } from 'src/app/interfaces/supermarket';
import { ProductCart } from 'src/app/interfaces/product-cart';
import { CartService } from 'src/app/services/cart.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss']
})
export class CartComponent implements OnInit {

  ListaSupermercados = new Array<Supermarket>();
  ListaSanta = new Array<ProductCart>();
  ListaJumbo = new Array<ProductCart>();
  ListProducts = new Array <ProductCart>();
  ListRow:any[] = [];
  ProductsInCart:any[] = [];
  total_santa:number = 0;
  total_jumbo:number = 0;

  constructor(private http:CartService) { }

  
  ngOnInit(): void {
    this.load_supermarkets();
    
    this.ProductsInCart = JSON.parse(localStorage.getItem('cart')!) || [];
    
    let list_id:string = '';
    if (this.ProductsInCart.length > 0) {
      list_id = this.get_products_supermarkets();
    }
    
    this.refresh_rows(list_id);
  }

  numberWithPoints(precio:any) {
    return precio.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }
  
  calculate_total() {
    this.total_santa = 0;
    this.total_jumbo = 0;
    for(let i=0; i<this.ListRow.length; i++) {
      if(this.ListRow[i]['value_santa'] != 'no-stock' && this.ListRow[i]['value_santa'] != 'no-distribuye') {
        this.total_santa = this.total_santa + parseInt(this.ListRow[i]['value_santa']);
      }
      
      if(this.ListRow[i]['value_jumbo'] != 'no-stock' && this.ListRow[i]['value_jumbo'] != 'no-distribuye') {
        this.total_jumbo = this.total_jumbo + parseInt(this.ListRow[i]['value_jumbo']);
      }
    }
  }
  
  best_price(total:number) {
    if (total <= this.total_jumbo && total <= this.total_santa) {
      return true;
    }
    return false;
  }
  
  load_supermarkets() {
    this.http.GetSupermarkets().subscribe(datos => {
      for(let i=0; i<datos.items.length; i++) {
        this.ListaSupermercados.push(datos.items[i]);
      }
    })
  }
  
  get_products_supermarkets():string {
    let list_id:string = '';
    for(let i=0; i<this.ProductsInCart.length; i++) {
      if (i == 0) {
        list_id = this.ProductsInCart[i]['id_producto'];
      } else {
        list_id = list_id + ',' + this.ProductsInCart[i]['id_producto']
      }
    }
    return list_id;
  }

  exists_product_row(id_producto:number):boolean {
    for(let i=0; i<this.ListRow.length; i++) {
      if(this.ListRow[i]['id_producto'] == id_producto) {
        return true;
      }
    }
    return false;
  }
  
  refresh_rows(list_id:string) {
    if (list_id != '') {
      this.ListRow = [];
      this.ListProducts = [];
      this.http.GetProductsCart(list_id).subscribe(datos => {
        for(let i=0; i<datos.items.length; i++) {
          this.ListProducts.push(datos.items[i]);
        }
        
        for(let i=0; i<this.ProductsInCart.length; i++) {
          let flag_santa:boolean = false;
          let flag_jumbo:boolean = false;
          
          let initial_value_santa:string = '';
          let value_santa:string = '';
          let status_santa:string = '';
          
          let initial_value_jumbo:string = '';
          let value_jumbo:string = '';
          let status_jumbo:string = '';
          
          let multiplicador:number = this.ProductsInCart[i]['multiplicador'];
          
          if (this.exists_product_row(this.ProductsInCart[i]['id_producto']) == false) {
            for(let j=0; j<this.ListProducts.length; j++) {           
              if (this.ListProducts[j].supermercado == 'Santa Isabel' && this.ListProducts[j].id_producto == this.ProductsInCart[i]['id_producto']) {
                if (this.ListProducts[j].disponibilidad == 'No') {
                  status_santa = 'no-stock';
                  value_santa = 'no-stock';
                } else {
                  if (this.ListProducts[j].precio_oferta != '-') {
                    initial_value_santa = this.ListProducts[j].precio_oferta;
                    value_santa = String(parseInt(this.ListProducts[j].precio_oferta) * multiplicador);
                    status_santa = 'oferta';
                  } else {
                    initial_value_santa = this.ListProducts[j].precio_normal;
                    value_santa = String(parseInt(this.ListProducts[j].precio_normal) * multiplicador);
                    status_santa = 'normal';
                  }
                }
                flag_santa = true;
              }
              
              if (this.ListProducts[j].supermercado == 'Jumbo' && this.ListProducts[j].id_producto == this.ProductsInCart[i]['id_producto']) {
                if (this.ListProducts[j].disponibilidad == 'No') {
                  value_jumbo = 'no-stock';
                  status_jumbo = 'no-stock';
                } else {
                  if (this.ListProducts[j].precio_oferta != '-') {
                    initial_value_jumbo = this.ListProducts[j].precio_oferta;
                    value_jumbo = String(parseInt(this.ListProducts[j].precio_oferta) * multiplicador);
                    status_jumbo = 'oferta';
                  } else {
                    initial_value_jumbo = this.ListProducts[j].precio_normal;
                    value_jumbo = String(parseInt(this.ListProducts[j].precio_normal) * multiplicador);
                    status_jumbo= 'normal';
                  }
                }
                flag_jumbo = true;
              }
              
              if (flag_santa == false) {
                value_santa = 'no-distribuye';
                status_santa = 'no-distribuye';
              }
              
              if (flag_jumbo == false) {
                value_jumbo = 'no-distribuye';
                status_jumbo = 'no-distribuye';
              }
            }
            
            this.ListRow.push({id_producto: this.ProductsInCart[i]['id_producto'], 
                               nombre: this.ProductsInCart[i]['nombre'], 
                               marca: this.ProductsInCart[i]['marca'],
                               imagen: this.ProductsInCart[i]['imagen'],
                               value_santa: value_santa, 
                               status_santa: status_santa, 
                               value_jumbo: value_jumbo, 
                               status_jumbo: status_jumbo,
                               multiplicador: multiplicador,
                               initial_value_jumbo: initial_value_jumbo,
                               initial_value_santa: initial_value_santa})
          }
        }
        this.calculate_total(); 
      })
    }
  }
  
  delete_row(id_producto:number) {
    for(let i=0; i<this.ProductsInCart.length; i++) {
      if (this.ProductsInCart[i]['id_producto'] == id_producto) {
        this.ProductsInCart.splice(i, 1);
        localStorage.setItem('cart', JSON.stringify(this.ProductsInCart));
        
        let list_id:string = '';
        if (this.ProductsInCart.length > 0) {
          list_id = this.get_products_supermarkets();
        } else {
          
        }
        
        this.refresh_rows(list_id);
      }
    }
    console.log(this.ProductsInCart.length)
  }
  
  subtract_multiplier(id_producto:number) {
    for(let i=0; i<this.ListRow.length; i++) {
      if (this.ListRow[i]['id_producto'] == id_producto) {
        this.ListRow[i]['multiplicador'] = this.ListRow[i]['multiplicador'] - 1;
        this.replace_multiplicador(id_producto, this.ListRow[i]['multiplicador']);
        if (this.ListRow[i]['value_santa'] != 'no-stock' && this.ListRow[i]['value_santa'] != 'no-distribuye') {
          this.ListRow[i]['value_santa'] = String(parseInt(this.ListRow[i]['initial_value_santa']) * this.ListRow[i]['multiplicador'])
        }
        
        if (this.ListRow[i]['value_jumbo'] != 'no-stock' && this.ListRow[i]['value_jumbo'] != 'no-distribuye') {
          this.ListRow[i]['value_jumbo'] = String(parseInt(this.ListRow[i]['initial_value_jumbo']) * this.ListRow[i]['multiplicador'])
        }
      }
    }
    this.calculate_total(); 
  }
  
  replace_multiplicador(id_producto:number, multiplicador:number) {
    for(let i=0; i<this.ProductsInCart.length; i++) {
      if(this.ProductsInCart[i]['id_producto'] == id_producto) {
        this.ProductsInCart[i]['multiplicador'] = multiplicador;
        localStorage.setItem('cart', JSON.stringify(this.ProductsInCart));
        return
      }
    }
  }
  
  add_multiplier(id_producto:number) {
    for(let i=0; i<this.ListRow.length; i++) {
      if (this.ListRow[i]['id_producto'] == id_producto) {
        this.ListRow[i]['multiplicador'] = this.ListRow[i]['multiplicador'] + 1;
        this.replace_multiplicador(id_producto, this.ListRow[i]['multiplicador']);
        if (this.ListRow[i]['value_santa'] != 'no-stock' && this.ListRow[i]['value_santa'] != 'no-distribuye') {
          this.ListRow[i]['value_santa'] = String(parseInt(this.ListRow[i]['initial_value_santa']) * this.ListRow[i]['multiplicador'])
        }
        
        if (this.ListRow[i]['value_jumbo'] != 'no-stock' && this.ListRow[i]['value_jumbo'] != 'no-distribuye') {
          this.ListRow[i]['value_jumbo'] = String(parseInt(this.ListRow[i]['initial_value_jumbo']) * this.ListRow[i]['multiplicador'])
        }
      }
    }
    this.calculate_total(); 
  }
  
  clear_cart() {
    this.ListRow = [];
    this.ProductsInCart = [];
    localStorage.removeItem('cart');
  }
}
