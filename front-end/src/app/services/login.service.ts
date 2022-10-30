import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Usuario } from '../interfaces/usuario';
import { map } from 'rxjs';
import { JwtHelperService } from '@auth0/angular-jwt';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  currentUser:Usuario = {
    id_usuario: 0,
    nombre: '',
    email: '',
  };
  
  isLoggedIn:boolean = false;

  helper = new JwtHelperService();

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
  
  GetUsuario(email:string):Observable<any> {
    return this.http.get(`${environment.hostname}/Usuario/${email}`);
  }
  
  PostUsuario(nombre:string, password:string, email:string):Observable<any> {
    return this.http.post(`${environment.hostname}/InsertarUsuario`, JSON.stringify({"nombre": nombre, "password": password, "email": email}), this.HttpUploadOptions);
  }
  
  PostLogin(email:string, password:string):Observable<any> {
    return this.http.post(`${environment.hostname}/Login`, JSON.stringify({"email": email, "password": password}), this.HttpUploadOptions).pipe(
      map((response:any) => {
        
        const decodedToken = this.helper.decodeToken(response.token);

        this.currentUser.nombre = decodedToken.data.nombre;
        this.currentUser.email = decodedToken.data.email;
        this.currentUser.id_usuario = decodedToken.data.id_usuario;
        
        localStorage.setItem('token', response.token);

        return this.currentUser;
      })
    );
  }
  


  logout() {
    localStorage.removeItem('token');
  }
  
  loggedIn():any {
    const token =  JSON.parse(localStorage.getItem('token') || '{}');
    return !this.helper.isTokenExpired(token);
  }
}
