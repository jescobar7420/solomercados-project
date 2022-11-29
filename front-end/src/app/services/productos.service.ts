import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProductosService {

  constructor(private http:HttpClient) { }
  
  HttpUploadOptions = {
    headers: new HttpHeaders (
      {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, DELETE, PUT',
        'Content-Type': 'application/json',
      }
    ),
  };
  
  GetListProductos():Observable<any> {
    return this.http.get(`${environment.hostname}/ListProductos`);
  }
  
  GetProducto(id:number):Observable<any> {
    return this.http.get(`${environment.hostname}/Producto/${id}`);
  }
  
  GetListProductsCategory(id:number):Observable<any> {
    return this.http.get(`${environment.hostname}/ProductosCategoria/${id}`);
  }
  
  GetListProductsBestPrice():Observable<any> {
    return this.http.get(`${environment.hostname}/ListProductsBestPrice`);
  }
  
  GetAllProductsName(search:any):Observable<any> {
    return this.http.get(`${environment.hostname}/AllProductsName/${search}`);
  }

  GetMostViewProductsDay():Observable<any> {
    return this.http.get(`${environment.hostname}/MostViewProductos`);
  }
}
