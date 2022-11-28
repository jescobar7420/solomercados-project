import { Component, ViewChild, ElementRef, Output, EventEmitter, Input, SimpleChanges } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginService } from 'src/app/services/login.service';
import { ProductosService } from 'src/app/services/productos.service';
import { JwtHelperService } from '@auth0/angular-jwt';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent { 
  showList: boolean = false;
  Productos:any[] = [];
  name_user:string = '';
  
  helper = new JwtHelperService();
    
  constructor(private http_login:LoginService, private http_product:ProductosService, private router: Router, private route: ActivatedRoute) {}
 
  ngOnInit(): void {
  }
    
  get_name_user():string {
    var token = localStorage.getItem('token') ?? '';
    if (token != '') {
      var decodetoken = this.helper.decodeToken(token);
      var name_user:string = decodetoken['data']['nombre'];
      return name_user;
    }
    return '';
  }
  
  isLoggedIn():boolean {
    return this.http_login.loggedIn();
  }
  
  search_product() {
    const input = document.getElementById('search') as HTMLInputElement | null;
    const value_search = input?.value;
    this.Productos = [];
  
    this.http_product.GetAllProductsName(value_search).subscribe(datos => {
      if (datos.items.length == 0) {
        this.showList = false;
      } else {
        this.showList = true;
        for(let i=0; i<datos.items.length; i++) {
          this.Productos.push(datos.items[i]);
        }
      }
    })
  }
  
  clear_search() {
    this.showList  = false;
    this.Productos = [];
    const input = document.getElementById('search') as HTMLInputElement | null;
    /* input. */
  }
  
  logout() {
    this.http_login.logout();
    localStorage.clear();
    Swal.fire({
      icon: 'info',
      title: '¡Hasta luego!',
      text: 'Has cerrado sesión.',
      confirmButtonColor: '#FF6F1E'
    }).then(a => {
      this.router.navigate(['login']);
    })
  }
}
