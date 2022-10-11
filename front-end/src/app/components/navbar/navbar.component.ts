import { Component, OnInit } from '@angular/core';
import { CategoriasService } from 'src/app/services/categorias.service';
import { Categorias } from 'src/app/interfaces/categorias';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  ListaCategorias = new Array<Categorias>()

  constructor(private http:CategoriasService) { }

  ngOnInit(): void {
    this.http.GetListCategorias().subscribe(datos => {
      for(let i=0; i<datos.items.length; i++) {
        this.ListaCategorias.push(datos.items[i]);
      }
    })
  }

}
