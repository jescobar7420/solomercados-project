import { Component, ViewChild, ElementRef, Output, EventEmitter, Input } from '@angular/core';
import { fromEvent, of } from 'rxjs';
import { debounceTime, filter, pluck, switchMap, tap } from 'rxjs/operators';
import { LoginService } from 'src/app/services/login.service';
import { ProductosService } from 'src/app/services/productos.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent { 
  showList: boolean = false;
  Productos:any[] = [];
    
  constructor(private http_login:LoginService, private http_product:ProductosService) {}

  current_user:any;
  
  ngOnInit(): void {
    this.current_user = this.http_login.currentUser;
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
  }
  
  logout() {
    this.http_login.logout();
  }
}
